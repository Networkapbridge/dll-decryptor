from __future__ import annotations


def hexdump(data: bytes, width: int = 16, limit: int = 256) -> str:
    """Compact hexdump for debug output; truncates after `limit` bytes."""
    data = data[:limit]
    lines = []
    for offset in range(0, len(data), width):
        chunk = data[offset : offset + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{offset:08x}  {hex_part:<{width * 3}}  {ascii_part}")
    return "\n".join(lines)