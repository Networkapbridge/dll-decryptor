from __future__ import annotations

import math
from pathlib import Path

import pefile


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts if c)


def section_report(path: Path) -> list[dict]:
    pe = pefile.PE(str(path), fast_load=True)
    rows = []
    for section in pe.sections:
        name = section.Name.rstrip(b"\x00").decode(errors="replace")
        data = section.get_data()
        rows.append(
            {
                "name": name,
                "size": len(data),
                "entropy": round(shannon_entropy(data), 3),
                "executable": bool(section.Characteristics & 0x20000000),
            }
        )
    return rows