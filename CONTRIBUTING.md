# Contributing

Thanks for considering a contribution. This repo is the official Skills catalogue for the SE Ranking MCP server. Issues and PRs are welcome.

## What kinds of contributions

- **Bug reports.** Open an issue with: skill name, the input you ran it on, the unexpected output, and the version (`/plugin marketplace info seranking`).
- **New skills.** PRs welcome — see the [skill-authoring template](#skill-authoring-template) below. Open an issue first if the skill is novel; we may already be planning something similar.
- **Improvements to existing skills.** PRs welcome. Include a before/after example run in the PR description.
- **Examples.** Real, end-to-end runs against public targets are gold. Drop them under `examples/{skill-output-folder-pattern}/` and mention them in `examples/README.md`.

## Repo layout

See [`README.md` § Repository layout](README.md#repository-layout). In short:

- `.claude-plugin/marketplace.json` — Claude Code marketplace manifest.
- `.claude-plugin/plugin.json` — plugin manifest. Both live at root.
- `skills/<skill-name>/SKILL.md` — one skill per directory. Some skills include `references/` or `templates/` subfolders.
- `examples/{slug}/` — real run outputs.

## Skill-authoring template

Every `SKILL.md` follows the same shape. Copy from an existing skill (e.g., `skills/seo-page/SKILL.md`) and adapt.

```markdown
---
name: seo-{your-skill}
description: <one-paragraph what-it-does + Use when ... triggers>
---

# {Human-Readable Title}

<one-paragraph framing of the deliverable and who it's for>

## Prerequisites

- SE Ranking MCP server connected.
- (Optional) Claude's `WebFetch` tool available.
- User provides: <inputs>.

## Process

1. **<Step name>** `MCP_tool_used`
   - <what this step does>
2. **<Step name>** `MCP_tool_used`
   - <what this step does>
...

## Output format

Create a folder `seo-{skill}-{target-slug}-{YYYYMMDD}/` with:
\`\`\`
seo-{skill}-{target-slug}-{YYYYMMDD}/
├── 01-<file>.md
├── 02-<file>.md
└── DELIVERABLE.md
\`\`\`

`DELIVERABLE.md` shape:
\`\`\`markdown
# {Title}: {target}
...
\`\`\`

## Tips

- Respect rate limit: 10 req/sec on Data API.
- Call `DATA_getCreditBalance` before running. {credit estimate}.
- {skill-specific tips}
```

## Required frontmatter fields

- **`name`** — the skill slug. Must match the folder name. Always prefixed with `seo-`.
- **`description`** — what the skill does + when it triggers. The description is loaded by Claude at startup; it determines whether the skill auto-invokes for a given user request. Be specific.

## Required body sections

In order:

1. `# Title` — human-readable name.
2. One-paragraph framing.
3. `## Prerequisites` — MCP server status, tool availability, user inputs.
4. `## Process` — numbered steps. Each step that calls MCP names the tool inline (e.g., `` `DATA_getDomainKeywords` ``).
5. `## Output format` — folder structure + the synthesised deliverable's markdown shape.
6. `## Tips` — rate limits, credit estimates, edge cases, recommended chains with other skills.

## Heavy-content rule

Keep `SKILL.md` ≤ 300 lines. If a skill needs a long rubric, schema template, or severity map, put it in a `references/` or `templates/` subfolder under the skill's directory and reference it from `SKILL.md`. This is the [progressive disclosure](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) pattern.

Examples in this repo:
- `skills/seo-content-audit/references/core-eeat.md` — 60-item rubric.
- `skills/seo-schema/templates/article.json` — JSON-LD starter.
- `skills/seo-sxo/references/page-type-patterns.md` — heuristic library.

## MCP tool naming

When you reference an SE Ranking MCP tool in `SKILL.md`, use the documented prefix in code formatting: `` `DATA_getDomainKeywords` ``. The full namespace `mcp__claude_ai_SE_Ranking__DATA_*` is implied — don't bury it in prose.

## Mutating tools

SE Ranking has read-only tools (`DATA_get*`, `DATA_list*`, `PROJECT_get*`, `PROJECT_list*`) and mutating tools (`DATA_createStandardAudit`, `PROJECT_create*`, `PROJECT_add*`, `PROJECT_delete*`, etc.).

- **Read-only tools:** safe to call freely. Document them in the Process section.
- **Mutating tools:** **always confirm with the user before invoking.** The skill body should print a summary (what will change, how many records, credit cost) before the call. Never auto-write to user state.

This plugin is currently DATA-API-only by scope decision; PROJECT_* tools and other mutating tools are out of scope unless a future skill explicitly opts in.

## Output folder convention

Every skill writes its output to `seo-{skill}-{target-slug}-{YYYYMMDD}/`. The date stamp keeps re-runs non-destructive.

## PR checklist

Before opening a PR:

- [ ] `SKILL.md` follows the structure above.
- [ ] Frontmatter has `name` (matching folder) and `description`.
- [ ] All MCP tools referenced are in the [SE Ranking MCP server](https://seranking.com/api/integrations/mcp). Don't reference tools that don't exist.
- [ ] If the skill has supporting files, they're under `references/` or `templates/`.
- [ ] `SKILL.md` ≤ 300 lines.
- [ ] README skills table updated (new row if a new skill).
- [ ] CHANGELOG entry added under the next planned version.
- [ ] Tested end-to-end against a public target. Surface real, redacted-if-needed output in the PR description.

## Versioning rules

Three files must stay in sync at every version bump:

1. `.claude-plugin/plugin.json` — `"version"`.
2. `.claude-plugin/marketplace.json` — `"metadata"."version"`.
3. `.claude-plugin/marketplace.json` — `"plugins"[0]."version"`.

Before each bump commit, verify with: `rg '"version"' .claude-plugin`.

## Coordinating with the SE Ranking MCP server

The MCP server lives at a separate repo. **Don't try to fix MCP-server bugs from this skills repo.** If a skill hits a server-side issue (e.g., the `DATA_getDomainCompetitors` 60KB overflow documented in `seo-content-brief` and `seo-competitor-gap-analysis`), document the workaround in the relevant `SKILL.md` and move on.

## License

MIT. By contributing you agree your contributions are licensed under MIT.
