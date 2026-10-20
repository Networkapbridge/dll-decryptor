from __future__ import annotations

from pathlib import Path

import pefile

from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)

MAX_SIZE = 512 * 1024 * 1024


class PeLoader:
    """Loads a Windows PE (DLL/EXE) with sanity checks."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> pefile.PE:
        size = self.path.stat().st_size
        if size > MAX_SIZE:
            raise ValueError(f"{self.path} exceeds {MAX_SIZE} bytes")
        pe = pefile.PE(str(self.path), fast_load=True)
        pe.parse_data_directories(
            directories=[
                pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],
                pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"],
                pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"],
            ]
        )
        log.debug("loaded %s (%d bytes, %d sections)", self.path, size, len(pe.sections))
        return pe