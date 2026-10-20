from __future__ import annotations

from pathlib import Path

import pefile
import yaml

from dll_decryptor.pipeline.analyze.entropy import shannon_entropy
from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)

SIG_PATH = Path(__file__).resolve().parents[3] / "config" / "signatures.yaml"


class SchemeDetector:
    """Matches a loaded PE against configured protection signatures."""

    def __init__(self, sig_path: Path = SIG_PATH) -> None:
        with sig_path.open("r", encoding="utf-8") as fh:
            self.schemes: dict = yaml.safe_load(fh).get("schemes", {})

    def detect(self, pe: pefile.PE) -> list[str]:
        hits: list[str] = []
        section_names = [s.Name.rstrip(b"\x00").decode(errors="replace") for s in pe.sections]
        max_entropy = max(
            (shannon_entropy(s.get_data()) for s in pe.sections), default=0.0
        )
        imports = self._collect_imports(pe)

        for name, sig in self.schemes.items():
            if max_entropy < sig.get("entropy_min", 0.0):
                continue
            hints = sig.get("section_hint", [])
            if hints and not any(h in section_names for h in hints):
                continue
            import_hints = sig.get("import_hints", [])
            if import_hints and not any(i in imports for i in import_hints):
                continue
            hits.append(name)

        log.debug("detected schemes: %s (max entropy %.2f)", hits, max_entropy)
        return hits

    @staticmethod
    def _collect_imports(pe: pefile.PE) -> set[str]:
        names: set[str] = set()
        for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []) or []:
            for imp in entry.imports:
                if imp.name:
                    names.add(imp.name.decode(errors="replace"))
        return names