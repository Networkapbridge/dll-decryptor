from __future__ import annotations

from dll_decryptor.pipeline.decryptors.aes_cbc import AesCbcDecryptor
from dll_decryptor.pipeline.decryptors.base import BaseDecryptor
from dll_decryptor.pipeline.decryptors.rc4 import Rc4Decryptor
from dll_decryptor.pipeline.decryptors.xor import XorDecryptor

_REGISTRY: dict[str, type[BaseDecryptor]] = {
    "xor_single_byte": XorDecryptor,
    "custom_rolling_xor": XorDecryptor,
    "rc4_standard": Rc4Decryptor,
    "aes_cbc_embedded_key": AesCbcDecryptor,
}


def build_decryptor(scheme: str) -> BaseDecryptor | None:
    cls = _REGISTRY.get(scheme)
    return cls() if cls else None


__all__ = ["BaseDecryptor", "build_decryptor"]