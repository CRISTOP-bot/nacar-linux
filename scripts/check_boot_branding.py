#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Ensure extracted BIOS/UEFI boot-menu directives use Nácar branding."""
from __future__ import annotations

import re
import sys
from pathlib import Path

VISIBLE_DIRECTIVE = re.compile(
    r"^\s*(?:menu\s+(?:title|label)|menuentry|submenu|title|say)\b", re.IGNORECASE
)
DEBIAN = re.compile(r"\bdebian\b", re.IGNORECASE)
NACAR = re.compile(r"\bnacar\b", re.IGNORECASE)


def check_boot_configs(roots: list[Path]) -> tuple[int, int]:
    violations: list[str] = []
    branded = 0
    directives = 0
    for root in roots:
        if not root.is_dir():
            raise ValueError(f"boot configuration directory missing from ISO: {root}")
        for path in sorted(root.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            raw = path.read_bytes()
            if b"\0" in raw:
                continue
            try:
                lines = raw.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for number, line in enumerate(lines, start=1):
                stripped = line.lstrip()
                if stripped.startswith(("#", ";", "//", "/*", "*")) or not VISIBLE_DIRECTIVE.match(line):
                    continue
                directives += 1
                if DEBIAN.search(line):
                    violations.append(f"{path}:{number}: {line.strip()}")
                if NACAR.search(line):
                    branded += 1
    if violations:
        raise ValueError("Debian appears in visible boot directives:\n" + "\n".join(violations))
    if directives == 0 or branded == 0:
        raise ValueError("no Nácar-branded BIOS/UEFI menu directive found")
    return directives, branded


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(f"Usage: {argv[0]} BOOT-CONFIG-DIR [BOOT-CONFIG-DIR ...]", file=sys.stderr)
        return 2
    try:
        directives, branded = check_boot_configs([Path(item) for item in argv[1:]])
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Boot branding verification failed: {error}", file=sys.stderr)
        return 1
    print(f"Boot menus verified: {branded}/{directives} visible directive(s) identify Nacar; none identify Debian.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
