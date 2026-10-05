#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate user-facing ISO9660 metadata for the Nácar image."""
from __future__ import annotations

import sys
from pathlib import Path

SECTOR_SIZE = 2048
PVD_SECTOR = 16
FIELDS = {
    "volume": (40, 32),
    "publisher": (318, 128),
    "preparer": (446, 128),
    "application": (574, 128),
}
EXPECTED = {
    "volume": "NACAR_LINUX",
    "publisher": "Nacar GNU/Linux Project",
    "preparer": "Nacar GNU/Linux build",
    "application": "Nacar GNU/Linux Live",
}


def read_primary_volume_descriptor(path: Path) -> dict[str, str]:
    with path.open("rb") as image:
        image.seek(PVD_SECTOR * SECTOR_SIZE)
        descriptor = image.read(SECTOR_SIZE)
    if len(descriptor) != SECTOR_SIZE or descriptor[0] != 1 or descriptor[1:6] != b"CD001":
        raise ValueError("ISO has no valid primary volume descriptor at sector 16")
    return {
        key: descriptor[offset : offset + size].decode("ascii", errors="strict").strip(" \0")
        for key, (offset, size) in FIELDS.items()
    }


def verify_iso(path: Path) -> dict[str, str]:
    actual = read_primary_volume_descriptor(path)
    for key, expected in EXPECTED.items():
        if actual[key] != expected:
            raise ValueError(f"unexpected ISO {key} field: {actual[key]!r}")
    if any("debian" in value.lower() for value in actual.values()):
        raise ValueError("Debian branding remains in user-facing ISO metadata")
    return actual


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} IMAGE.iso", file=sys.stderr)
        return 2
    try:
        metadata = verify_iso(Path(argv[1]))
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ISO branding verification failed: {error}", file=sys.stderr)
        return 1
    print("ISO metadata verified:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
