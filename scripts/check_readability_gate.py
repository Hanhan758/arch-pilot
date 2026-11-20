#!/usr/bin/env python3
"""GATE-05: Readability, completeness, and clean Mermaid gate for ArchPilot v1.0."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WEEK_FILES = (
    "week-01-data-rules.md",
    "week-02-git-truth.md",
    "week-03-oop-layers.md",
    "week-04-concurrency-guard.md",
    "week-05-tdd-migration.md",
    "week-06-packaging-boundary.md",
)

PLACEHOLDER_PHRASES = (
    "预习导览版",
    "滚动解锁",
    "即将解锁",
    "敬请期待",
)

MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
HTML_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
TERM_HEADING_RE = re.compile(r"^###\s+\d+\.\s+.+$", re.MULTILINE)
EXPLICIT_ANCHOR_RE = re.compile(r"\{#[A-Za-z0-9\u4e00-\u9fff._-]+\}\s*$")


def check_readability(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    guide_dir = root / "docs" / "guide"
    for filename in WEEK_FILES:
        path = guide_dir / filename
        if not path.is_file():
            errors.append(f"[missing-week] docs/guide/{filename} does not exist")
            continue
        text = path.read_text(encoding="utf-8")

        for placeholder in PLACEHOLDER_PHRASES:
            if placeholder in text:
                errors.append(
                    f"[placeholder-found] docs/guide/{filename} contains placeholder phrase {placeholder!r}"
                )

        if not MERMAID_BLOCK_RE.search(text):
            errors.append(f"[missing-mermaid] docs/guide/{filename} must contain at least 1 Mermaid block")

        if "免费" not in text:
            errors.append(f"[missing-free-resources] docs/guide/{filename} must recommend free external resources")

        details_count = len(re.findall(r"<details>", text))
        if details_count < 3:
            errors.append(
                f"[insufficient-self-checks] docs/guide/{filename} has {details_count} <details> blocks (need >= 3)"
            )

        if not any(
            token in text
            for token in ("arch-tutor", "arch-examiner", "/ai-kit/tutor", "/ai-kit/examiner")
        ):
            errors.append(
                f"[missing-kit-prompt] docs/guide/{filename} should guide using arch-tutor or arch-examiner"
            )

    glossary_path = root / "docs" / "toolkit" / "glossary.md"
    if not glossary_path.is_file():
        errors.append("[missing-glossary] docs/toolkit/glossary.md does not exist")
    else:
        g_text = glossary_path.read_text(encoding="utf-8")
        analogy_count = len(re.findall(r"一句话生活类比", g_text))
        if analogy_count < 16:
            errors.append(
                f"[glossary-count] docs/toolkit/glossary.md has {analogy_count} analogy entries (need >= 16)"
            )
        headings = TERM_HEADING_RE.findall(g_text)
        if len(headings) < 16:
            errors.append(
                f"[glossary-headings] docs/toolkit/glossary.md has {len(headings)} numbered headings (need >= 16)"
            )
        for heading in headings:
            if not EXPLICIT_ANCHOR_RE.search(heading.strip()):
                errors.append(
                    f"[missing-anchor] glossary heading lacks explicit {{#id}} anchor: {heading!r}"
                )

    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for md_path in sorted(docs_dir.rglob("*.md")):
            rel = md_path.relative_to(root).as_posix()
            md_text = md_path.read_text(encoding="utf-8")
            for idx, match in enumerate(MERMAID_BLOCK_RE.finditer(md_text), start=1):
                if HTML_BR_RE.search(match.group(1)):
                    errors.append(
                        f"[mermaid-html-tag] {rel} mermaid block #{idx} contains disallowed <br> tag"
                    )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify GATE-05 readability and Mermaid cleanliness.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root directory.",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors = check_readability(root)
    if errors:
        print("Readability gate FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"Readability gate PASSED ({len(WEEK_FILES)} weeks & glossary verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
