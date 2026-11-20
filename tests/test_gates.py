#!/usr/bin/env python3
"""Unit and regression tests for ArchPilot CI quality gates."""

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
    def _create_valid_kits(self, root: Path, *, skill_version: str = "0.1.0") -> None:
        (root / "prompts").mkdir(parents=True)
        (root / "docs" / "ai-kit").mkdir(parents=True)
        for kit_id, slug in check_prompt_sync.KIT_SPECS:
            (root / "prompts" / f"{kit_id}.prompt.md").write_text(
                f'---\nid: {kit_id}\nversion: "0.1.0"\n---\n# body\n',
                encoding="utf-8",
            )
            skill_dir = root / "skills" / kit_id
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f'---\nname: {kit_id}\nversion: "{skill_version}"\n---\n# skill\n',
                encoding="utf-8",
            )
            (root / "docs" / "ai-kit" / f"{slug}.md").write_text(
                f"import p from '../../prompts/{kit_id}.prompt.md?raw'\nv0.1.0\n",
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
            self._create_valid_kits(root, skill_version="0.2.0")
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


if __name__ == "__main__":
    unittest.main()
