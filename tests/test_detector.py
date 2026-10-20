from __future__ import annotations

from dll_decryptor.pipeline.analyze.detector import SchemeDetector


def test_detector_loads_signatures():
    detector = SchemeDetector()
    assert "xor_single_byte" in detector.schemes
    assert "rc4_standard" in detector.schemes


def test_detector_returns_empty_for_low_entropy():
    class _Pe:
        sections: list = []
        DIRECTORY_ENTRY_IMPORT: list = []

    assert SchemeDetector().detect(_Pe()) == []
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>