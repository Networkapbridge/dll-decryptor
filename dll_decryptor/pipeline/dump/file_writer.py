from __future__ import annotations

import hashlib
from pathlib import Path

import pefile

from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)


class DumpWriter:
    """Persists recovered payloads to disk with provenance metadata."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, pe: pefile.PE, payload: bytes, scheme: str) -> Path:
        digest = hashlib.sha256(payload).hexdigest()[:12]
        stem = Path(pe.filename).stem if getattr(pe, "filename", None) else "sample"
        out_path = self.output_dir / f"{stem}.{scheme}.{digest}.recovered"
        out_path.write_bytes(payload)
        log.info("wrote %d bytes -> %s", len(payload), out_path)
        return out_path