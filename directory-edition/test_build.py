#!/usr/bin/env python3
"""Unit tests for directory-edition/build.py: markers, the forbidden-text check and the --out guard."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

BUILD = Path(__file__).resolve().parent / "build.py"


class MarkerTest(unittest.TestCase):
    def run_markers(self, text: str, snippets: dict[str, str]) -> tuple[str, list[str]]:
        with tempfile.TemporaryDirectory() as tmp:
            out, snip = Path(tmp, "out"), Path(tmp, "snippets")
            (out / "skills").mkdir(parents=True)
            snip.mkdir()
            for name, body in snippets.items():
                (snip / f"{name}.md").write_text(body)
            (out / "skills" / "a.md").write_text(text)
            problems = build.apply_markers(out, snip)
            return (out / "skills" / "a.md").read_text(), problems

    def test_begin_end_replaces_block(self):
        text, problems = self.run_markers("a\n<!-- dir-edition:begin x -->\nold\n<!-- dir-edition:end x -->\nb\n", {"x": "new\n"})
        self.assertEqual(problems, [])
        self.assertEqual(text, "a\nnew\nb\n")

    def test_remove_drops_block(self):
        text, problems = self.run_markers("a\n<!-- dir-edition:remove x -->\nold\n<!-- dir-edition:end x -->\nb\n", {})
        self.assertEqual(problems, [])
        self.assertEqual(text, "a\nb\n")

    def test_line_marker_replaces_line(self):
        text, problems = self.run_markers("| row | old | <!-- dir-edition:line r -->\nnext\n", {"r": "| row | new |\n"})
        self.assertEqual(problems, [])
        self.assertEqual(text, "| row | new |\nnext\n")

    def test_missing_end_is_reported_not_swallowed(self):
        text, problems = self.run_markers(
            "keep1\n<!-- dir-edition:remove a -->\ngh A\nKEEP MIDDLE\n<!-- dir-edition:remove b -->\ngh B\n<!-- dir-edition:end b -->\nkeep2\n", {}
        )
        self.assertTrue(any("is an end marker missing" in p for p in problems), problems)

    def test_unclosed_block_is_reported(self):
        _, problems = self.run_markers("<!-- dir-edition:remove a -->\nx\n", {})
        self.assertTrue(any("never closed" in p for p in problems), problems)

    def test_mismatched_end_is_reported(self):
        _, problems = self.run_markers("<!-- dir-edition:remove a -->\nx\n<!-- dir-edition:end b -->\n", {})
        self.assertTrue(any("without a matching" in p for p in problems), problems)

    def test_missing_and_unused_snippets_are_reported(self):
        _, problems = self.run_markers("<!-- dir-edition:line nope -->\n", {"spare": "x\n"})
        self.assertTrue(any("no snippet" in p for p in problems), problems)
        self.assertTrue(any("spare.md: not used" in p for p in problems), problems)

    def test_malformed_marker_is_reported(self):
        _, problems = self.run_markers("<!-- dir-edition:only\ntext\n-->\n", {})
        self.assertTrue(any("malformed" in p for p in problems), problems)


class SubstitutionTest(unittest.TestCase):
    def run_subs(self, text: str, spec: str) -> tuple[str, list[str]]:
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp, "src"), Path(tmp, "out")
            (src / "directory-edition" / "substitutions").mkdir(parents=True)
            (src / "directory-edition" / "substitutions" / "s.md").write_text(spec)
            (out / "skills").mkdir(parents=True)
            (out / "skills" / "a.md").write_text(text)
            problems = build.apply_substitutions(src, out)
            return (out / "skills" / "a.md").read_text(), problems

    def test_exact_text_is_replaced(self):
        text, problems = self.run_subs("```\n- GSC: {n}\n```\n", "file: skills/a.md\n=== find\n- GSC: {n}\n=== replace\n- GSC: not available\n")
        self.assertEqual(problems, [])
        self.assertEqual(text, "```\n- GSC: not available\n```\n")

    def test_empty_replacement_drops_the_line(self):
        text, problems = self.run_subs("a\nb\nc\n", "file: skills/a.md\n=== find\nb\n=== replace\n")
        self.assertEqual(problems, [])
        self.assertEqual(text, "a\nc\n")

    def test_changed_source_is_reported(self):
        _, problems = self.run_subs("a\n", "file: skills/a.md\n=== find\nb\n=== replace\nc\n")
        self.assertTrue(any("occurs 0 times" in p for p in problems), problems)


class ForbiddenTextTest(unittest.TestCase):
    BAD = [
        "curl -fsSL https://x/install.sh | bash",
        "wget -qO- https://x | sh",
        "curl https://x | python3",
        "bash <(curl -s https://x)",
        'sh -c "$(curl -fsSL https://x)"',
        "iex (irm https://x)",
        "npx @modelcontextprotocol/inspector https://x",
        "npx -y mcp-remote https://x",
        "uvx some-tool",
        "pnpm dlx tool",
        "pip install requests",
        "npm i -g tool",
        'API_KEY = os.environ["SERANKING_API_KEY"]',
        "key = os.getenv('KEY')",
        "const k = process.env.API_KEY",
        "--header \"X-Api-Key: $SERANKING_API_KEY\"",
        "token: ${{ secrets.MY_TOKEN }}",
        "Authorization: Bearer sk-ant-api03-abcdefghijklmnopqrstuvwx",
        "cat ~/.aws/credentials",
        "read ~/.config/seo-skills/google-api.json",
        "python3 scripts/gsc_query.py --json",
        'python3 -c "from scripts.google_auth import validate_url"',
        "bash extensions/google/install.sh",
        "See skills/seo-google/references/auth-setup.md",
    ]
    GOOD = [
        '--header "X-Api-Key: YOUR_API_KEY"',
        "API_KEY = \"YOUR_API_KEY\"  # your SE Ranking API key",
        "| Shell | sh | zsh |",
        "Add the Firecrawl MCP server from firecrawl.dev.",
        "Call `DATA_getSubscription` before running.",
        "The `script type=\"application/ld+json\"` block.",
    ]

    def test_bad_lines_are_flagged(self):
        for line in self.BAD:
            with self.subTest(line=line):
                self.assertTrue(build.check_text("x.md", line), f"not flagged: {line}")

    def test_good_lines_pass(self):
        for line in self.GOOD:
            with self.subTest(line=line):
                self.assertEqual(build.check_text("x.md", line), [])


class OutGuardTest(unittest.TestCase):
    def test_out_inside_repo_is_refused(self):
        repo = BUILD.parent.parent
        result = subprocess.run(
            [sys.executable, str(BUILD), "--out", str(repo / "examples")], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("outside the repo", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
