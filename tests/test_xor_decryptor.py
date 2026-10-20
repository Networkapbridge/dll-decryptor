from __future__ import annotations

import pytest

from dll_decryptor.pipeline.decryptors.xor import XorDecryptor


class _FakeSection:
    def __init__(self, data: bytes) -> None:
        self._data = data
        self.Name = b".text"
        self.Characteristics = 0x20000000

    def get_data(self) -> bytes:
        return self._data


class _FakePe:
    def __init__(self, sections: list[_FakeSection]) -> None:
        self.sections = sections


def test_xor_recovers_mz_prologue():
    plain = b"MZ\x90\x00" + b"\x00" * 60
    key = 0x5A
    encrypted = bytes(b ^ key for b in plain)
    pe = _FakePe([_FakeSection(encrypted)])
    recovered = XorDecryptor().try_decrypt(pe)
    assert recovered == plain


def test_xor_returns_none_for_plain_section():
    pe = _FakePe([_FakeSection(b"\x00" * 64)])
    assert XorDecryptor().try_decrypt(pe) is None