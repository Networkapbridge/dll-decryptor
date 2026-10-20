from __future__ import annotations

import pefile

from dll_decryptor.pipeline.decryptors.base import BaseDecryptor
from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)


class Rc4Decryptor(BaseDecryptor):
    """Tries RC4 against embedded keys found in readable sections."""

    name = "rc4_standard"

    def try_decrypt(self, pe: pefile.PE) -> bytes | None:
        keys = self._candidate_keys(pe)
        for section in self._target_sections(pe):
            blob = section.get_data()
            for key in keys:
                plain = self._rc4(key, blob)
                if plain.startswith(b"MZ"):
                    log.info("rc4 key hit (%d bytes) on %s", len(key), section.Name)
                    return plain
        return None

    @staticmethod
    def _candidate_keys(pe: pefile.PE) -> list[bytes]:
        keys: list[bytes] = []
        for section in pe.sections:
            if section.Name.rstrip(b"\x00") in (b".rdata", b".data"):
                data = section.get_data()
                for size in (8, 16, 24, 32):
                    for off in range(0, min(len(data) - size, 4096), 4):
                        chunk = data[off : off + size]
                        if len(set(chunk)) >= size // 2:
                            keys.append(chunk)
        return keys[:64]

    @staticmethod
    def _rc4(key: bytes, data: bytes) -> bytes:
        s = list(range(256))
        j = 0
        for i in range(256):
            j = (j + s[i] + key[i % len(key)]) & 0xFF
            s[i], s[j] = s[j], s[i]
        out = bytearray(len(data))
        i = j = 0
        for k, b in enumerate(data):
            i = (i + 1) & 0xFF
            j = (j + s[i]) & 0xFF
            s[i], s[j] = s[j], s[i]
            out[k] = b ^ s[(s[i] + s[j]) & 0xFF]
        return bytes(out)