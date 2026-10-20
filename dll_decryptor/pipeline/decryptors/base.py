from __future__ import annotations

from abc import ABC, abstractmethod

import pefile


class BaseDecryptor(ABC):
    """Contract for a single-scheme DLL payload decryptor."""

    name: str = "base"

    @abstractmethod
    def try_decrypt(self, pe: pefile.PE) -> bytes | None:
        """Return recovered plaintext bytes, or None if this scheme doesn't apply."""

    def _target_sections(self, pe: pefile.PE) -> list[pefile.SectionStructure]:
        return [s for s in pe.sections if s.Characteristics & 0x20000000]