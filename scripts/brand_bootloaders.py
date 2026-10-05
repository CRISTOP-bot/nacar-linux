#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Brand live-build's temporary bootloader templates without altering notices."""
from __future__ import annotations

import re
import sys
from pathlib import Path

VISIBLE_DIRECTIVE = re.compile(
    r"^\s*(?:menu\s+(?:title|label)|menuentry|submenu|title|say)\b", re.IGNORECASE
)
MENU_TITLE = re.compile(r"^(\s*menu\s+title\s+).*$", re.IGNORECASE)
DEBIAN = re.compile(r"\bdebian\b", re.IGNORECASE)
REPLACEMENTS = (
    (re.compile(r"\bDebian\s+GNU/Linux\s+Live\b", re.IGNORECASE), "Nacar GNU/Linux Live"),
    (re.compile(r"\bDebian\s+Live\b", re.IGNORECASE), "Nacar GNU/Linux Live"),
    (re.compile(r"\bDebian\s+GNU/Linux\b", re.IGNORECASE), "Nacar GNU/Linux"),
    (re.compile(r"\bDebian\b", re.IGNORECASE), "Nacar"),
)


def is_comment(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("#", ";", "//", "/*", "*"))


def brand_bootloaders(root: Path) -> int:
    if not root.is_dir():
        raise ValueError(f"bootloader template directory does not exist: {root}")

    changed = 0
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue

        output: list[str] = []
        dirty = False
        for line in text.splitlines(keepends=True):
            if is_comment(line) or not VISIBLE_DIRECTIVE.match(line):
                output.append(line)
                continue
            title = MENU_TITLE.match(line)
            if title:
                newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
                branded = f"{title.group(1)}Nacar GNU/Linux Live{newline}"
            else:
                branded = line
                for pattern, replacement in REPLACEMENTS:
                    branded = pattern.sub(replacement, branded)
            if branded != line:
                dirty = True
                changed += 1
            output.append(branded)

        if dirty:
            path.write_text("".join(output), encoding="utf-8")

    remaining: list[str] = []
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
            if not is_comment(line) and VISIBLE_DIRECTIVE.match(line) and DEBIAN.search(line):
                remaining.append(f"{path}:{number}: {line.strip()}")
    if remaining:
        raise ValueError("Debian branding remains in visible boot directives:\n" + "\n".join(remaining))
    return changed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} BOOTLOADER-DIRECTORY", file=sys.stderr)
        return 2
    try:
        changed = brand_bootloaders(Path(argv[1]))
    except (OSError, ValueError) as error:
        print(f"Bootloader branding failed: {error}", file=sys.stderr)
        return 1
    print(f"Nacar boot branding verified; customized {changed} visible directive(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
