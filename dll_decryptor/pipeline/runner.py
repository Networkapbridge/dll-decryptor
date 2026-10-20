from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dll_decryptor.pipeline.analyze.detector import SchemeDetector
from dll_decryptor.pipeline.decryptors import build_decryptor
from dll_decryptor.pipeline.dump.file_writer import DumpWriter
from dll_decryptor.pipeline.ingest.pe_loader import PeLoader
from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)


@dataclass
class PipelineResult:
    recovered: bool
    output_path: Path | None = None
    scheme: str | None = None


class PipelineRunner:
    """Orchestrates ingest -> analyze -> decrypt -> dump for one DLL."""

    def __init__(self, output_dir: Path, forced_scheme: str | None = None) -> None:
        self.output_dir = output_dir
        self.forced_scheme = forced_scheme

    def run(self, target: Path) -> PipelineResult:
        log.info("ingest %s", target)
        pe = PeLoader(target).load()

        detector = SchemeDetector()
        candidates = [self.forced_scheme] if self.forced_scheme else detector.detect(pe)
        log.info("candidate schemes: %s", candidates)

        for scheme in candidates:
            decryptor = build_decryptor(scheme)
            if decryptor is None:
                continue
            recovered = decryptor.try_decrypt(pe)
            if recovered is None:
                continue
            out_path = DumpWriter(self.output_dir).write(pe, recovered, scheme)
            return PipelineResult(True, out_path, scheme)

        return PipelineResult(False)