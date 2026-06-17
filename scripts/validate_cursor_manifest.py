#!/usr/bin/env python3
"""Validate .cursor-plugin/plugin.json against the vendored Cursor plugin schema.

The Claude Code CLI (`claude plugin validate`) only understands Claude manifests,
so the Cursor manifest needs its own guard. This validates it against
schemas/cursor-plugin.schema.json (Cursor's published draft-07 schema, which is
additionalProperties:false — unknown fields fail, not just warn) and confirms the
assets it declares (logo, skills) and the auto-detected mcp.json actually exist.

Exits non-zero on any failure so CI goes red. Requires: jsonschema.
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas" / "cursor-plugin.schema.json"
MANIFEST = ROOT / ".cursor-plugin" / "plugin.json"

PNG_SIG = bytes.fromhex("89504e470d0a1a0a")


def main() -> int:
    from jsonschema import Draft7Validator

    problems = 0

    def ok(msg: str) -> None:
        print(f"  [PASS] {msg}")

    def fail(msg: str) -> None:
        nonlocal problems
        problems += 1
        print(f"  [FAIL] {msg}")

    print("Cursor plugin manifest validation")

    if not MANIFEST.is_file():
        print(f"  [FAIL] {MANIFEST.relative_to(ROOT)} not found")
        return 1
    if not SCHEMA.is_file():
        print(f"  [FAIL] {SCHEMA.relative_to(ROOT)} not found")
        return 1

    manifest = json.loads(MANIFEST.read_text())
    schema = json.loads(SCHEMA.read_text())

    # 1) Schema conformance (catches the icon/author.url class of errors).
    errs = sorted(Draft7Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
    if errs:
        fail(f"schema: {len(errs)} violation(s)")
        for e in errs:
            loc = "/".join(map(str, e.path)) or "(root)"
            print(f"         - at {loc}: {e.message}")
    else:
        ok("schema: valid against schemas/cursor-plugin.schema.json")

    # 2) Declared logo exists, is relative, and is a square PNG.
    logo = manifest.get("logo")
    if not logo:
        fail("logo: not declared")
    elif logo.startswith(("/", "http://", "https://")):
        ok(f"logo: external/absolute ({logo}) — file check skipped")
    else:
        p = ROOT / logo
        if not p.is_file():
            fail(f"logo: {logo} does not exist")
        else:
            b = p.read_bytes()
            if b[:8] != PNG_SIG:
                fail(f"logo: {logo} is not a valid PNG")
            else:
                w, h = struct.unpack(">II", b[16:24])
                if w == h:
                    ok(f"logo: {logo} is a {w}x{h} square PNG")
                else:
                    fail(f"logo: {logo} is {w}x{h}, not square")

    # 3) Declared skills path resolves to a directory.
    skills = manifest.get("skills")
    if skills:
        sp = ROOT / str(skills).lstrip("./")
        if sp.is_dir():
            ok(f"skills: {skills} exists")
        else:
            fail(f"skills: {skills} is missing")

    # 4) Auto-detected mcp.json at plugin root (optional, but if present must be sane).
    mcp = ROOT / "mcp.json"
    if mcp.is_file():
        try:
            servers = json.loads(mcp.read_text()).get("mcpServers", {})
        except json.JSONDecodeError as ex:
            fail(f"mcp.json: invalid JSON ({ex})")
        else:
            if isinstance(servers, dict) and servers:
                ok(f"mcp.json: present with {len(servers)} server(s)")
            else:
                fail("mcp.json: no mcpServers entries")
    else:
        ok("mcp.json: not present (no bundled MCP server)")

    print("OK" if problems == 0 else f"{problems} problem(s) — see above")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
