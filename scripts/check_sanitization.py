#!/usr/bin/env python3
"""GATE-01 & GATE-02: Automated privacy sanitization and example size gate."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Iterable

SKIP_DIRS = frozenset({
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
})

SKIP_REL_PREFIXES = (
    "docs/.vitepress/cache",
    "docs/.vitepress/dist",
)

TEXT_EXTENSIONS = frozenset({
    ".md",
    ".mts",
    ".ts",
    ".js",
    ".mjs",
    ".vue",
    ".json",
    ".py",
    ".yml",
    ".yaml",
    ".css",
    ".txt",
    ".sh",
})

MAX_EXAMPLE_LINES = 60

# Construct sensitive literals dynamically to avoid self-matching during scans.
LOCAL_PATH_PATTERNS = (
    (
        "local-abs-path",
        re.compile(
            r"(?:"
            + "/" + r"Users/"
            + r"|"
            + "/" + r"home/"
            + r"|"
            + "/" + r"Volumes/"
            + r"|[A-Za-z]:\\" + r"Users\\"
            + r")"
        ),
    ),
    (
        "private-dir-marker",
        re.compile(
            r"(?:"
            + re.escape("." + "talos-private")
            + r"|"
            + "\u79c1\u4eba\u6570\u636e"
            + r"|"
            + "\u90e8\u7f72\u8d44\u4ea7"
            + r")"
        ),
    ),
    (
        "suspected-secret",
        re.compile(
            r"(?:"
            + r"\bsk-[A-Za-z0-9_-]{20,}"
            + r"|\bghp_[A-Za-z0-9]{20,}"
            + r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
            + r")"
        ),
    ),
)


def _iter_scannable_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = current.relative_to(root).as_posix()
        dirnames[:] = [
            name
            for name in sorted(dirnames)
            if name not in SKIP_DIRS
            and (
                rel_dir == "."
                and name not in SKIP_REL_PREFIXES
                or f"{rel_dir}/{name}" not in SKIP_REL_PREFIXES
            )
        ]
        for filename in sorted(filenames):
            path = current / filename
            if path.suffix.lower() in TEXT_EXTENSIONS or filename in {
                "LICENSE-CODE",
                "LICENSE-CONTENT",
                ".gitignore",
            }:
                yield path


def scan_repository(root: Path) -> list[str]:
    root = root.resolve()
    violations: list[str] = []

    for path in _iter_scannable_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            raw = path.read_bytes()
        except OSError as exc:
            violations.append(f"[io-error] {rel}: {exc}")
            continue
        if b"\x00" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            violations.append(f"[encoding] {rel}: file is not valid UTF-8")
            continue

        lines = text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            for rule_name, pattern in LOCAL_PATH_PATTERNS:
                if pattern.search(line):
                    violations.append(f"[{rule_name}] {rel}:{line_no}: matched restricted pattern")

        if rel.startswith("docs/talos-lite/examples/") and len(lines) > MAX_EXAMPLE_LINES:
            violations.append(
                f"[example-size] {rel}: {len(lines)} lines exceeds limit {MAX_EXAMPLE_LINES}"
            )

    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check ArchPilot sanitization and example gates.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root directory to scan.",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    violations = scan_repository(root)
    if violations:
        print("Sanitization check FAILED:", file=sys.stderr)
        for item in violations:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print(f"Sanitization check PASSED ({root.name}): 0 violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
