#!/usr/bin/env python3
"""GATE-03: Verify prompts/, skills/, and docs/ai-kit/ stay synchronized."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KIT_SPECS = (
    ("arch-tutor", "tutor"),
    ("arch-examiner", "examiner"),
    ("arch-auditor", "auditor"),
)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return meta
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return {}


def check_sync(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for kit_id, doc_slug in KIT_SPECS:
        prompt_file = root / "prompts" / f"{kit_id}.prompt.md"
        skill_file = root / "skills" / kit_id / "SKILL.md"
        doc_file = root / "docs" / "ai-kit" / f"{doc_slug}.md"

        if not prompt_file.is_file():
            errors.append(f"[missing-prompt] prompts/{kit_id}.prompt.md does not exist")
            continue
        if not skill_file.is_file():
            errors.append(f"[missing-skill] skills/{kit_id}/SKILL.md does not exist")
            continue
        if not doc_file.is_file():
            errors.append(f"[missing-doc] docs/ai-kit/{doc_slug}.md does not exist")
            continue

        prompt_meta = parse_frontmatter(prompt_file.read_text(encoding="utf-8"))
        skill_meta = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        doc_text = doc_file.read_text(encoding="utf-8")

        if prompt_meta.get("id") != kit_id:
            errors.append(
                f"[prompt-id] prompts/{kit_id}.prompt.md expected id={kit_id!r}, got {prompt_meta.get('id')!r}"
            )
        if skill_meta.get("name") != kit_id:
            errors.append(
                f"[skill-name] skills/{kit_id}/SKILL.md expected name={kit_id!r}, got {skill_meta.get('name')!r}"
            )

        p_ver = prompt_meta.get("version")
        s_ver = skill_meta.get("version")
        if not p_ver:
            errors.append(f"[prompt-version] prompts/{kit_id}.prompt.md missing version")
        if not s_ver:
            errors.append(f"[skill-version] skills/{kit_id}/SKILL.md missing version")
        if p_ver and s_ver and p_ver != s_ver:
            errors.append(
                f"[version-mismatch] {kit_id}: prompt={p_ver!r} != skill={s_ver!r}"
            )

        expected_import = f"prompts/{kit_id}.prompt.md?raw"
        if expected_import not in doc_text:
            errors.append(
                f"[doc-import] docs/ai-kit/{doc_slug}.md must import {expected_import}"
            )
        if p_ver and not re.search(rf"\bv?{re.escape(p_ver)}\b", doc_text):
            errors.append(
                f"[doc-version] docs/ai-kit/{doc_slug}.md does not reference version {p_ver}"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify AI companion kit synchronization.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Repository root directory.",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors = check_sync(root)
    if errors:
        print("Prompt/Skill sync check FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"Prompt/Skill sync check PASSED ({len(KIT_SPECS)} kits verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
