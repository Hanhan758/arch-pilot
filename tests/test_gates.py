#!/usr/bin/env python3
"""Unit and regression tests for ArchPilot CI quality gates (GATE-01..05)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_prompt_sync  # noqa: E402
import check_readability_gate  # noqa: E402
import check_sanitization  # noqa: E402


class SanitizationGateTests(unittest.TestCase):
    def _write_clean_repo(self, root: Path) -> None:
        (root / "docs" / "talos-lite" / "examples").mkdir(parents=True)
        (root / "docs" / "index.md").write_text("# Clean Doc\n", encoding="utf-8")
        (root / "docs" / "talos-lite" / "examples" / "sample.json").write_text(
            '{\n  "status": "active"\n}\n',
            encoding="utf-8",
        )

    def test_clean_repo_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_clean_repo(root)
            self.assertEqual(check_sanitization.scan_repository(root), [])

    def test_blocks_local_absolute_path_prefixes(self) -> None:
        bad_paths = [
            "/" + "Users/" + "tester/secret",
            "/" + "home/" + "tester/project",
            "/" + "Volumes/" + "Disk/data",
            "C:\\" + "Users\\" + "tester\\file",
        ]
        for bad in bad_paths:
            with self.subTest(bad=bad):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self._write_clean_repo(root)
                    (root / "docs" / "leak.md").write_text(f"path: {bad}\n", encoding="utf-8")
                    violations = check_sanitization.scan_repository(root)
                    self.assertTrue(any("local-abs-path" in v for v in violations))

    def test_blocks_private_markers_and_secrets(self) -> None:
        markers = [
            ("private-dir-marker", "." + "talos-private"),
            ("private-dir-marker", "\u79c1\u4eba\u6570\u636e"),
            ("private-dir-marker", "\u90e8\u7f72\u8d44\u4ea7"),
            ("suspected-secret", "sk-" + "1234567890abcdefghij1234"),
            ("suspected-secret", "-----BEGIN " + "PRIVATE KEY-----"),
        ]
        for rule, payload in markers:
            with self.subTest(rule=rule, payload=payload):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    self._write_clean_repo(root)
                    (root / "docs" / "bad.md").write_text(f"{payload}\n", encoding="utf-8")
                    violations = check_sanitization.scan_repository(root)
                    self.assertTrue(any(rule in v for v in violations))

    def test_blocks_oversized_example_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_clean_repo(root)
            oversized = "\n".join(f'  "k{i}": {i}' for i in range(65))
            (root / "docs" / "talos-lite" / "examples" / "too-big.json").write_text(
                oversized,
                encoding="utf-8",
            )
            violations = check_sanitization.scan_repository(root)
            self.assertTrue(any("example-size" in v for v in violations))

    def test_real_repository_passes_cli(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_sanitization.py"), "--root", str(REPO_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)


class PromptSyncGateTests(unittest.TestCase):
    def _create_valid_kits(self, root: Path, *, skill_version: str = "1.0.0") -> None:
        (root / "prompts").mkdir(parents=True)
        (root / "docs" / "ai-kit").mkdir(parents=True)
        for kit_id, slug in check_prompt_sync.KIT_SPECS:
            (root / "prompts" / f"{kit_id}.prompt.md").write_text(
                f'---\nid: {kit_id}\nversion: "1.0.0"\n---\n# body\n',
                encoding="utf-8",
            )
            skill_dir = root / "skills" / kit_id
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f'---\nname: {kit_id}\nversion: "{skill_version}"\n---\n# skill\n',
                encoding="utf-8",
            )
            (root / "docs" / "ai-kit" / f"{slug}.md").write_text(
                f"import p from '../../prompts/{kit_id}.prompt.md?raw'\nv1.0.0\n",
                encoding="utf-8",
            )

    def test_valid_sync_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_kits(root)
            self.assertEqual(check_prompt_sync.check_sync(root), [])

    def test_detects_missing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_kits(root)
            (root / "skills" / "arch-tutor" / "SKILL.md").unlink()
            errors = check_prompt_sync.check_sync(root)
            self.assertTrue(any("missing-skill" in e for e in errors))

    def test_detects_version_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_kits(root, skill_version="1.1.0")
            errors = check_prompt_sync.check_sync(root)
            self.assertTrue(any("version-mismatch" in e for e in errors))

    def test_real_repository_passes_cli(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_prompt_sync.py"), "--root", str(REPO_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)


class ReadabilityGateTests(unittest.TestCase):
    def _create_valid_docs(self, root: Path) -> None:
        guide_dir = root / "docs" / "guide"
        toolkit_dir = root / "docs" / "toolkit"
        guide_dir.mkdir(parents=True)
        toolkit_dir.mkdir(parents=True)
        valid_week = (
            "# Week\n\n"
            "```mermaid\nflowchart LR\n  A --> B\n```\n\n"
            "免费外部科普资源\n\n"
            "<details><summary>1</summary>a</details>\n"
            "<details><summary>2</summary>b</details>\n"
            "<details><summary>3</summary>c</details>\n\n"
            "使用 arch-tutor 与 arch-examiner。\n"
        )
        for filename in check_readability_gate.WEEK_FILES:
            (guide_dir / filename).write_text(valid_week, encoding="utf-8")
        terms = "\n".join(
            f"### {i}. 术语{i} {{#term-{i}}}\n- 一句话生活类比：类比{i}\n"
            for i in range(1, 18)
        )
        (toolkit_dir / "glossary.md").write_text(f"# 术语表\n\n{terms}", encoding="utf-8")

    def test_clean_docs_pass_readability_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_docs(root)
            self.assertEqual(check_readability_gate.check_readability(root), [])

    def test_blocks_placeholder_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_docs(root)
            p = root / "docs" / "guide" / "week-02-git-truth.md"
            p.write_text(p.read_text(encoding="utf-8") + "\n预习导览版\n", encoding="utf-8")
            errors = check_readability_gate.check_readability(root)
            self.assertTrue(any("placeholder-found" in e for e in errors))

    def test_blocks_missing_mermaid_and_insufficient_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_docs(root)
            (root / "docs" / "guide" / "week-03-oop-layers.md").write_text(
                "# 缺少图表与自检题\n免费课程 arch-tutor\n<details>1</details>\n",
                encoding="utf-8",
            )
            errors = check_readability_gate.check_readability(root)
            self.assertTrue(any("missing-mermaid" in e for e in errors))
            self.assertTrue(any("insufficient-self-checks" in e for e in errors))

    def test_blocks_mermaid_br_html_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_valid_docs(root)
            (root / "docs" / "guide" / "week-04-concurrency-guard.md").write_text(
                "```mermaid\nflowchart LR\n  A[\"a<br/>b\"] --> B\n```\n"
                "免费 arch-tutor\n<details>1</details><details>2</details><details>3</details>\n",
                encoding="utf-8",
            )
            errors = check_readability_gate.check_readability(root)
            self.assertTrue(any("mermaid-html-tag" in e for e in errors))

    def test_real_repository_passes_cli(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_readability_gate.py"), "--root", str(REPO_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)


if __name__ == "__main__":
    unittest.main()
