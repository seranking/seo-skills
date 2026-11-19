#!/usr/bin/env python3
"""Build the Claude Plugins Directory edition of seo-skills and check it.

The directory accepts only Markdown, text, JSON, YAML and image files from
organizations it hasn't verified, and it refuses plugins whose files read
credentials from the user's machine or download and run code. The GitHub
edition needs its Python scripts, installers and examples, so the directory
gets an edition without them, built from the same source:

1. Copy the plugin files the directory accepts (see INCLUDE and EXCLUDE).
2. Turn `.html` templates under skills/ into Markdown files with a code block.
3. Apply the markers in Markdown files:

       <!-- dir-edition:remove -->
       ...text that only the GitHub edition has...
       <!-- dir-edition:end -->

       <!-- dir-edition:only
       ...text that only the directory edition has...
       -->

4. Copy directory-edition/overrides/ over the result (whole-file replacements).
5. Point relative links to files the edition lacks at GitHub.
6. Check every file, and exit non-zero with the list of problems.

Usage: python3 directory-edition/build.py --out DIR [--src REPO_ROOT]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

INCLUDE = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "skills",
    "README.md",
    "LICENSE",
]

# Paths (prefixes, relative to the repo root) left out of the edition.
EXCLUDE = [
    # seo-google runs on local Python scripts; the edition ships a pointer skill
    # (overrides/skills/seo-google/SKILL.md) instead of its references and templates.
    "skills/seo-google/references/",
    "skills/seo-google/assets/",
]

ALLOWED_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
ALLOWED_NAMES = {"LICENSE", ".gitignore"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}

REMOVE_BLOCK = re.compile(r"^[ \t]*<!-- dir-edition:remove -->[ \t]*\n.*?^[ \t]*<!-- dir-edition:end -->[ \t]*\n", re.S | re.M)
ONLY_BLOCK = re.compile(r"^[ \t]*<!-- dir-edition:only[ \t]*\n(.*?)^[ \t]*-->[ \t]*\n", re.S | re.M)

# Text the directory refuses or flags, or that points at files the edition doesn't ship.
FORBIDDEN = [
    (re.compile(r"\$\{?[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET)\b"), "reads a credential from the environment"),
    (re.compile(r"\|\s*(?:sudo\s+)?(?:ba|z)?sh\b"), "pipes a download into a shell"),
    (re.compile(r"\bnpx\s+-y\b"), "downloads and runs a package (npx -y)"),
    (re.compile(r"\buvx\s"), "downloads and runs a package (uvx)"),
    (re.compile(r"\.config/seo-skills"), "reads the local Google credentials file"),
    (re.compile(r"GOOGLE_APPLICATION_CREDENTIALS|FIRECRAWL_API_KEY|GOOGLE_API_KEY"), "names a credential variable"),
    (re.compile(r"\bscripts/[A-Za-z0-9_]+\.py\b"), "runs a script the edition doesn't ship"),
    (re.compile(r"\bextensions/(?:google|firecrawl)\b"), "runs an installer the edition doesn't ship"),
    (re.compile(r"\binstall\.sh\b"), "runs an installer the edition doesn't ship"),
    (re.compile(r"dir-edition:"), "leftover directory-edition marker"),
]


def excluded(rel: str) -> bool:
    return any(rel.startswith(prefix) for prefix in EXCLUDE)


def copy_sources(src: Path, out: Path) -> None:
    for entry in INCLUDE:
        path = src / entry
        files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
        for file in files:
            rel = file.relative_to(src).as_posix()
            if excluded(rel):
                continue
            target = out / rel
            if file.suffix == ".html" and rel.startswith("skills/"):
                target = target.with_suffix(".md")
                body = file.read_text(encoding="utf-8").rstrip("\n")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"# {file.name}\n\n```html\n{body}\n```\n", encoding="utf-8")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, target)


def apply_markers(out: Path) -> None:
    for file in out.rglob("*.md"):
        text = file.read_text(encoding="utf-8")
        new = REMOVE_BLOCK.sub("", text)
        new = ONLY_BLOCK.sub(lambda m: m.group(1), new)
        if new != text:
            file.write_text(new, encoding="utf-8")


def apply_overrides(src: Path, out: Path) -> None:
    overrides = src / "directory-edition" / "overrides"
    if not overrides.is_dir():
        return
    for file in sorted(p for p in overrides.rglob("*") if p.is_file()):
        target = out / file.relative_to(overrides)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file, target)


MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
GITHUB_BLOB = "https://github.com/seranking/seo-skills/blob/main/"


def rewrite_missing_links(out: Path) -> None:
    """Point relative Markdown links at GitHub when the edition lacks their target."""
    for file in out.rglob("*.md"):
        text = file.read_text(encoding="utf-8")

        def fix(match: re.Match[str]) -> str:
            target = match.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:|^#", target, re.I):
                return match.group(0)
            path, _, anchor = target.partition("#")
            resolved = (file.parent / path).resolve()
            if not resolved.is_relative_to(out) or resolved.exists():
                return match.group(0)
            url = GITHUB_BLOB + resolved.relative_to(out).as_posix() + (f"#{anchor}" if anchor else "")
            return f"]({url})"

        new = MD_LINK.sub(fix, text)
        if new != text:
            file.write_text(new, encoding="utf-8")


def check(out: Path) -> list[str]:
    problems: list[str] = []
    for file in sorted(p for p in out.rglob("*") if p.is_file()):
        rel = file.relative_to(out).as_posix()
        if file.suffix.lower() not in ALLOWED_SUFFIXES and file.name not in ALLOWED_NAMES:
            problems.append(f"{rel}: file type not accepted from organizations that aren't Verified")
            continue
        data = file.read_bytes()
        if data.startswith(b"#!"):
            problems.append(f"{rel}: starts with #!")
        if file.suffix.lower() not in TEXT_SUFFIXES and file.name not in ALLOWED_NAMES:
            continue
        if b"\x00" in data:
            problems.append(f"{rel}: contains NUL bytes")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel}: not UTF-8")
            continue
        if file.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                problems.append(f"{rel}: invalid JSON ({exc})")
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern, why in FORBIDDEN:
                if pattern.search(line):
                    problems.append(f"{rel}:{lineno}: {why}: {line.strip()[:120]}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path, help="output directory (emptied first)")
    parser.add_argument("--src", default=Path(__file__).resolve().parent.parent, type=Path, help="repo root")
    args = parser.parse_args()

    src, out = args.src.resolve(), args.out.resolve()
    if out == src or src.is_relative_to(out) or any(out.is_relative_to(src / entry) for entry in INCLUDE):
        print("--out must be a separate folder, not the repo root or a folder the edition copies from", file=sys.stderr)
        return 2
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    copy_sources(src, out)
    apply_markers(out)
    apply_overrides(src, out)
    rewrite_missing_links(out)

    problems = check(out)
    files = sum(1 for p in out.rglob("*") if p.is_file())
    if problems:
        print(f"Directory edition in {out}: {files} files, {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print(f"Directory edition in {out}: {files} files, all accepted types, no forbidden text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
