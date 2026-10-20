from __future__ import annotations

import pefile

from dll_decryptor.pipeline.decryptors.base import BaseDecryptor
from dll_decryptor.utils.log import get_logger

log = get_logger(__name__)

# Common MZ/PE prologues used to score XOR key candidates.
PROLOGUES = (b"MZ\x90\x00", b"\x4d\x5a", b"\x90\x00\x03\x00")


class XorDecryptor(BaseDecryptor):
    name = "xor_single_byte"

    def try_decrypt(self, pe: pefile.PE) -> bytes | None:
        for section in self._target_sections(pe):
            data = section.get_data()
            if not data:
                continue
            for key in range(1, 256):
                sample = bytes(b ^ key for b in data[:8])
                if sample.startswith(PROLOGUES):
                    log.info("xor key 0x%02x matched on section %s", key, section.Name)
                    return bytes(b ^ key for b in data)
        return None