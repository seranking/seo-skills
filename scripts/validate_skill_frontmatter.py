#!/usr/bin/env python3
"""Validate every skill's SKILL.md frontmatter against the Anthropic Agent Skills
API rules that the claude.ai / Cowork marketplace sync enforces.

`claude plugin validate` (run by validate.yml) does NOT enforce these — it only
truncates over-long descriptions for its listing budget — so a skill that the CLI
and `/plugin marketplace add` accept can still hard-fail the web "Add marketplace"
sync with the generic "Marketplace sync failed. Check the repository URL and try
again." Because the web sync uploads every bundled skill to the Skills API and
replaces all plugins atomically, ONE invalid skill fails the WHOLE sync. This
linter closes that gap. See DAT-563 / anthropics/claude-code#63081.

Rules (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
  name        required; <= 64 chars; ^[a-z0-9]+(-[a-z0-9]+)*$; no XML tags;
              must not contain the reserved words "anthropic" / "claude".
  description  required; non-empty; <= 1024 chars AND <= 1024 UTF-8 bytes;
              no XML tags (angle-bracket tags break the web upload).

Exit non-zero if any skill violates a rule, printing every problem (and a
GitHub Actions ::error annotation per file).
"""
from __future__ import annotations

import glob
import re
import sys

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
XML_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
RESERVED_WORDS = ("anthropic", "claude")
MAX_NAME_CHARS = 64
MAX_DESC_CHARS = 1024
MAX_DESC_BYTES = 1024

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.S)


def load_frontmatter(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter (--- ... ---)")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return data


def check_skill(path: str) -> list[str]:
    try:
        fm = load_frontmatter(path)
    except Exception as exc:  # noqa: BLE001 — surface any parse error as a finding
        return [str(exc)]

    errors: list[str] = []

    name = fm.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("name: missing or empty")
    else:
        if len(name) > MAX_NAME_CHARS:
            errors.append(f"name: {len(name)} chars > {MAX_NAME_CHARS}")
        if not NAME_RE.match(name):
            errors.append(f"name: {name!r} must match ^[a-z0-9]+(-[a-z0-9]+)*$")
        if XML_TAG_RE.search(name):
            errors.append("name: must not contain XML tags")
        lowered = name.lower()
        for word in RESERVED_WORDS:
            if word in lowered:
                errors.append(f"name: must not contain reserved word {word!r}")

    description = fm.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("description: missing or empty")
    else:
        n_chars = len(description)
        n_bytes = len(description.encode("utf-8"))
        if n_chars > MAX_DESC_CHARS:
            errors.append(f"description: {n_chars} chars > {MAX_DESC_CHARS}")
        if n_bytes > MAX_DESC_BYTES:
            errors.append(f"description: {n_bytes} bytes > {MAX_DESC_BYTES}")
        tag = XML_TAG_RE.search(description)
        if tag:
            errors.append(f"description: must not contain XML tags (found {tag.group(0)!r})")

    return errors


def main() -> int:
    paths = sorted(glob.glob("skills/*/SKILL.md"))
    if not paths:
        print("error: no skills/*/SKILL.md found (run from the repo root)", file=sys.stderr)
        return 1

    failed = 0
    for path in paths:
        errors = check_skill(path)
        if errors:
            failed += 1
            print(f"::error file={path}::{'; '.join(errors)}")
            print(f"✘ {path}")
            for err in errors:
                print(f"    - {err}")
        else:
            print(f"✔ {path}")

    print()
    print(f"{len(paths)} skills checked, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
