#!/usr/bin/env python3
"""Build the Claude Plugins Directory edition of seo-skills and check it.

The directory accepts only Markdown, text, JSON, YAML and image files from
organizations it hasn't verified, and it refuses plugins whose files read
credentials from the user's machine or download and run code. The GitHub
edition needs its Python scripts, installers and examples, so the directory
gets an edition without them, built from the same source:

1. Copy the plugin files the directory accepts (see INCLUDE and EXCLUDE).
2. Turn `.html` templates under skills/ into Markdown files with a code block.
3. Apply the markers in Markdown files. They carry only an id, so agents that
   read the GitHub edition's raw Markdown see no directory-only instructions:

       <!-- dir-edition:begin ID -->   text only the GitHub edition has
       <!-- dir-edition:end ID -->     → replaced by snippets/ID.md

       <!-- dir-edition:remove ID -->  text only the GitHub edition has
       <!-- dir-edition:end ID -->     → dropped

       any line <!-- dir-edition:line ID -->  → the whole line is replaced by snippets/ID.md

4. Copy overrides/ over the result (whole-file replacements).
5. Set the manifests' description to description.txt.
6. Point relative links to files the edition lacks at GitHub, at --ref.
7. Check every file (type, content sniffing with `file`, forbidden text) and
   exit non-zero with the list of problems.

Usage: python3 directory-edition/build.py --out DIR [--src REPO_ROOT] [--ref TAG]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
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

ALLOWED_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_NAMES = {"LICENSE", ".gitignore"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}
# What `file --mime-type` (libmagic) may report for a shipped file. Markdown that
# libmagic reads as HTML or as source code can count as a refused file type.
ALLOWED_MIME = {"text/plain", "application/json", "text/markdown", "image/png", "image/jpeg", "image/gif", "image/webp"}

MARKER = re.compile(r"<!-- dir-edition:(begin|remove|end|line) ([a-z0-9][a-z0-9-]*) -->")
MARKETPLACE_DESCRIPTION = "SE Ranking's plugin marketplace for Claude: SEO skills built on the SE Ranking MCP server."
BRAND_WORDS = {"anthropic"}
GITHUB_REPO = "https://github.com/seranking/seo-skills"

# Text the directory refuses or flags, or that points at files the edition doesn't ship.
FORBIDDEN = [
    # Credentials read from the user's machine (the checklist forbids it "even in a README example").
    (r"\$\{?(?!YOUR_)[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PAT)\w*", "reads a credential from the environment"),
    (r"\bos\.environ\b|\bos\.getenv\b|\bgetenv\(|\bprocess\.env\b|\bENV\[|\$env:|\bsecrets\.[A-Za-z_]", "reads a credential from the environment"),
    (r"\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bp]-[A-Za-z0-9-]{10,})", "looks like a real token"),
    (r"~/\.(?:aws|ssh|netrc|config/gcloud)\b|\.config/seo-skills|google-api\.json", "reads a local credentials file"),
    (r"GOOGLE_APPLICATION_CREDENTIALS|FIRECRAWL_API_KEY|GOOGLE_API_KEY", "names a credential variable"),
    # Download-and-run commands.
    (r"\b(?:curl|wget|irm|iwr|Invoke-WebRequest|Invoke-RestMethod)\b[^\n]*\|\s*(?:sudo\s+(?:-\S+\s+)*)?(?:/\S*/)?(?:env\s+)?(?:ba|z|da|k|fi)?sh\b", "pipes a download into a shell"),
    (r"\b(?:curl|wget)\b[^\n]*\|\s*(?:sudo\s+)?(?:python3?|node|ruby|perl)\b", "pipes a download into an interpreter"),
    (r"\b(?:ba|z)?sh\s+<\(|\bsh\s+-c\s+[\"']\$\(\s*(?:curl|wget)|\biex\b", "runs downloaded code"),
    (r"\b(?:npx|bunx|uvx)\s|\b(?:pnpm|yarn)\s+dlx\b|\bpipx\s+run\b|\buv\s+tool\s+run\b", "downloads and runs a package"),
    (r"\bpip3?\s+install\b|\bnpm\s+(?:i|install)\s+(?:-g|--global)\b", "installs a package"),
    # Things the edition doesn't ship.
    (r"\bscripts/[\w-]+\.(?:py|sh|js|ts)\b|-m\s+scripts\.|\bscripts\.[a-z_]+\b|\bpython3?\s+-c\b", "runs a script the edition doesn't ship"),
    (r"\bextensions/(?:google|firecrawl)\b|\binstall\.sh\b", "runs an installer the edition doesn't ship"),
    (r"seo-google/(?:references|assets)/|cross-skill-integration", "points at a file the edition doesn't ship"),
    (r"dir-edition:", "leftover directory-edition marker"),
]
FORBIDDEN_RE = [(re.compile(pattern), why) for pattern, why in FORBIDDEN]


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
            target.parent.mkdir(parents=True, exist_ok=True)
            if file.suffix == ".html" and rel.startswith("skills/"):
                body = file.read_text(encoding="utf-8").rstrip("\n")
                target.with_suffix(".md").write_text(f"Template `{file.name}`:\n\n```html\n{body}\n```\n", encoding="utf-8")
                continue
            shutil.copyfile(file, target)


def apply_markers(out: Path, snippets: Path, ref: str = "main") -> list[str]:
    """Replace or drop the marked text; every marker must pair up and every snippet must be used once.

    `{ref}` in a snippet becomes the git ref the edition is built from.
    """
    problems: list[str] = []
    available = {p.stem: p for p in snippets.glob("*.md")} if snippets.is_dir() else {}
    used: dict[str, str] = {}

    def take(snippet_id: str, where: str) -> str:
        if snippet_id in used:
            problems.append(f"{where}: id '{snippet_id}' is already used at {used[snippet_id]}")
        used[snippet_id] = where
        if snippet_id not in available:
            problems.append(f"{where}: no snippet directory-edition/snippets/{snippet_id}.md")
            return ""
        text = available[snippet_id].read_text(encoding="utf-8").replace("{ref}", ref)
        if "dir-edition:" in text:
            problems.append(f"{where}: snippet {snippet_id}.md contains a marker")
        return text if text.endswith("\n") else text + "\n"

    for file in sorted(out.rglob("*.md")):
        rel = file.relative_to(out).as_posix()
        lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
        result: list[str] = []
        block: tuple[str, str, int] | None = None
        for lineno, line in enumerate(lines, 1):
            where = f"{rel}:{lineno}"
            marks = MARKER.findall(line)
            if "dir-edition:" in line and not marks:
                problems.append(f"{where}: malformed dir-edition marker")
            if len(marks) > 1:
                problems.append(f"{where}: more than one dir-edition marker on a line")
                continue
            if not marks:
                if block is None:
                    result.append(line)
                continue
            kind, snippet_id = marks[0]
            if kind == "line":
                if block is not None:
                    problems.append(f"{where}: line marker inside the block opened at line {block[2]}")
                    continue
                result.append(take(snippet_id, where))
            elif kind in ("begin", "remove"):
                if line.strip() != f"<!-- dir-edition:{kind} {snippet_id} -->":
                    problems.append(f"{where}: a {kind} marker must be alone on its line")
                if block is not None:
                    problems.append(f"{where}: '{snippet_id}' opens inside '{block[1]}' (line {block[2]}); is an end marker missing?")
                block = (kind, snippet_id, lineno)
            else:  # end
                if block is None or block[1] != snippet_id:
                    problems.append(f"{where}: end '{snippet_id}' without a matching begin/remove")
                    continue
                if block[0] == "begin":
                    result.append(take(snippet_id, where))
                block = None
        if block is not None:
            problems.append(f"{rel}:{block[2]}: '{block[1]}' is never closed")
        file.write_text("".join(result), encoding="utf-8")

    for snippet_id in sorted(set(available) - set(used)):
        problems.append(f"directory-edition/snippets/{snippet_id}.md: not used by any marker")
    return problems


SUBSTITUTION = re.compile(r"file: (\S+)\n=== find\n(.*?)\n=== replace\n(.*?)\n?", re.S)


def apply_substitutions(src: Path, out: Path) -> list[str]:
    """Exact-text replacements for text markers can't wrap, such as lines inside fenced templates.

    Each substitutions/*.md file names one file and the text to find there, which must occur
    exactly once, so a change to the source text fails the build instead of shipping stale text.
    """
    problems: list[str] = []
    folder = src / "directory-edition" / "substitutions"
    for spec in sorted(folder.glob("*.md")) if folder.is_dir() else []:
        name = spec.relative_to(src).as_posix()
        match = SUBSTITUTION.fullmatch(spec.read_text(encoding="utf-8"))
        if not match:
            problems.append(f"{name}: expected a 'file:' line, then '=== find' and '=== replace' sections")
            continue
        rel, find, replace = match.groups()
        target = out / rel
        if not target.is_file():
            problems.append(f"{name}: {rel} is not in the edition")
            continue
        body = target.read_text(encoding="utf-8")
        count = body.count(find)
        if count != 1:
            problems.append(f"{name}: the find text occurs {count} times in {rel} (expected once); update it to match the source")
            continue
        if replace == "" and body.count(find + "\n") == 1:
            find += "\n"  # an empty replacement drops the whole line
        target.write_text(body.replace(find, replace), encoding="utf-8")
    return problems


def apply_overrides(src: Path, out: Path) -> None:
    overrides = src / "directory-edition" / "overrides"
    if not overrides.is_dir():
        return
    for file in sorted(p for p in overrides.rglob("*") if p.is_file()):
        target = out / file.relative_to(overrides)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file, target)


def set_description(src: Path, out: Path) -> list[str]:
    """The listing shows the manifest description, so it must describe this edition."""
    path = src / "directory-edition" / "description.txt"
    if not path.is_file():
        return [f"{path.relative_to(src)}: missing"]
    description = " ".join(path.read_text(encoding="utf-8").split())
    plugin_path = out / ".claude-plugin" / "plugin.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    plugin["description"] = description
    plugin_path.write_text(json.dumps(plugin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    market_path = out / ".claude-plugin" / "marketplace.json"
    market = json.loads(market_path.read_text(encoding="utf-8"))
    # Nothing in the edition should read as an Anthropic or "official" listing.
    market.setdefault("metadata", {})["description"] = MARKETPLACE_DESCRIPTION
    for entry in market.get("plugins", []):
        if entry.get("name") == plugin.get("name"):
            entry["description"] = description
            for key in ("tags", "keywords"):
                if key in entry:
                    entry[key] = [word for word in entry[key] if word not in BRAND_WORDS]
    if "keywords" in plugin:
        plugin["keywords"] = [word for word in plugin["keywords"] if word not in BRAND_WORDS]
        plugin_path.write_text(json.dumps(plugin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    market_path.write_text(json.dumps(market, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return []


MD_LINK = re.compile(r"\]\(([^)\s]+)\)")


def rewrite_missing_links(out: Path, ref: str) -> None:
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
            kind = "tree" if path.endswith("/") else "blob"
            url = f"{GITHUB_REPO}/{kind}/{ref}/{resolved.relative_to(out).as_posix()}" + (f"#{anchor}" if anchor else "")
            return f"]({url})"

        new = MD_LINK.sub(fix, text)
        if new != text:
            file.write_text(new, encoding="utf-8")


def sniff(files: list[Path]) -> dict[Path, str] | None:
    """libmagic's MIME type per file, or None when `file` isn't installed."""
    if not shutil.which("file") or not files:
        return None
    output = subprocess.run(
        ["file", "--brief", "--mime-type", *map(str, files)], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    return dict(zip(files, output))


def check_text(rel: str, text: str) -> list[str]:
    problems = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, why in FORBIDDEN_RE:
            if pattern.search(line):
                problems.append(f"{rel}:{lineno}: {why}: {line.strip()[:120]}")
    return problems


def check(out: Path, require_sniff: bool = False) -> list[str]:
    problems: list[str] = []
    files = sorted(p for p in out.rglob("*") if p.is_file())
    for file in files:
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
        problems.extend(check_text(rel, text))
    mime = sniff(files)
    if mime is None:
        if require_sniff:
            problems.append("`file` (libmagic) is not installed, so content sniffing wasn't checked")
    else:
        for file, kind in mime.items():
            if kind not in ALLOWED_MIME:
                problems.append(f"{file.relative_to(out).as_posix()}: libmagic reads it as {kind}")
    return problems


def build(src: Path, out: Path, ref: str, require_sniff: bool = False) -> list[str]:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    copy_sources(src, out)
    problems = apply_markers(out, src / "directory-edition" / "snippets", ref)
    problems += apply_substitutions(src, out)
    apply_overrides(src, out)
    problems += set_description(src, out)
    rewrite_missing_links(out, ref)
    return problems + check(out, require_sniff)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path, help="output directory (emptied first)")
    parser.add_argument("--src", default=Path(__file__).resolve().parent.parent, type=Path, help="repo root")
    parser.add_argument("--ref", default="main", help="git ref that links to files the edition lacks point at")
    parser.add_argument("--require-sniff", action="store_true", help="fail when `file` (libmagic) is missing")
    args = parser.parse_args()

    src, out = args.src.resolve(), args.out.resolve()
    if out.is_relative_to(src) or src.is_relative_to(out):
        print("--out must be a folder outside the repo", file=sys.stderr)
        return 2

    problems = build(src, out, args.ref, args.require_sniff)
    files = sum(1 for p in out.rglob("*") if p.is_file())
    if problems:
        print(f"Directory edition in {out}: {files} files, {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print(f"Directory edition in {out}: {files} files, all accepted types and content, no forbidden text.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
