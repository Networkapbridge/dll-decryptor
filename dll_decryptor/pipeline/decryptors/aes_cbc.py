from __future__ import annotations

import pefile
from Crypto.Cipher import AES

from dll_decryptor.pipeline.decryptors.base import BaseDecryptor
from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)


class AesCbcDecryptor(BaseDecryptor):
    """Attempts AES-CBC with keys/IVs recovered from .rdata trailers."""

    name = "aes_cbc_embedded_key"

    def try_decrypt(self, pe: pefile.PE) -> bytes | None:
        material = self._scrape_material(pe)
        if material is None:
            return None
        key, iv = material
        for section in self._target_sections(pe):
            blob = section.get_data()
            if len(blob) < 32 or len(blob) % 16:
                continue
            try:
                plain = AES.new(key, AES.MODE_CBC, iv).decrypt(blob)
            except ValueError:
                continue
            if plain.startswith(b"MZ"):
                log.info("aes-cbc hit on %s", section.Name)
                return plain
        return None

    @staticmethod
    def _scrape_material(pe: pefile.PE) -> tuple[bytes, bytes] | None:
        for section in pe.sections:
            if section.Name.rstrip(b"\x00") != b".rdata":
                continue
            data = section.get_data()
            if len(data) < 48:
                continue
            trailer = data[-48:]
            return trailer[:32], trailer[32:48]
        return None