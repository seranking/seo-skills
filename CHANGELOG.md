# Changelog

All notable changes to this project will be documented in this file. Format based on Keep a Changelog.

## [0.3.1] — 2026-04-27

### Removed
- `seo-website-audit-change-report` skill removed from the catalogue. A focused one-shot `seo-technical-audit` (planned for v0.4.0) will cover the audit-deliverable use case.

### Changed
- Renamed `seo-keyword-cluster-planner` → `seo-keyword-cluster`. Folder, frontmatter `name:`, output-folder slug pattern, and all README references updated. Description tightened to call out how the skill differs from `seo-content-brief` (single article) and the planned `seo-page` (existing URL) — this skill plans a content tier across many articles.

## [0.3.0] — 2026-04-27

### Changed
- Renamed all 7 skills with an `seo-` prefix so slash-command tab-completion groups them visually: `content-brief` → `seo-content-brief`, `agency-landing-page` → `seo-agency-landing-page`, and so on. Skills are now invoked as `/seranking-mcp-skills:seo-content-brief`. Folder names, frontmatter `name:` fields, and output-folder slug patterns (`seo-{skill}-{target-slug}-{YYYYMMDD}/`) all updated to match.
- Renamed the bundled example run from `examples/ai-search-share-of-voice-wix-com-20260427/` to `examples/seo-ai-search-share-of-voice-wix-com-20260427/` for parity with the new slug convention.

## [0.2.0] — 2026-04-27

### Changed
- Flattened the repo layout: skill folders are now at `skills/<name>/SKILL.md` (was `plugins/seranking-mcp-skills/skills/<name>/SKILL.md`). The marketplace's `plugins[0].source` is `"./"`, and `plugin.json` lives alongside `marketplace.json` under `.claude-plugin/`. Matches the single-plugin convention used by other community plugins (e.g. `AgriciDaniel/claude-seo`).
- Updated README install Options 2–4 to use the new flat paths. Users installing via `/plugin marketplace add seranking/seranking-mcp-skills` are unaffected; users using `--plugin-dir` or `cp -r` need to update their paths.

## [0.1.1] — 2026-04-27

### Changed
- Standardized output folder slugs to `{skill-slug}-{target-slug}-{YYYYMMDD}/` across all skills.
- Pointed README at the SE Ranking remote MCP (`https://seranking.com/api/integrations/mcp`). Install is now `claude mcp add --transport http se-ranking https://api.seranking.com/mcp` + OAuth sign-in. Removed the `DATA_API_TOKEN` env-var requirement and the `PROJECT_API_TOKEN` mention — OAuth covers auth, and one connection covers every skill.

### Added
- Rate-limit tip in `agency-landing-page` for parity with other skills.
- WebFetch declared in Prerequisites of `content-brief` and `backlink-gap`.
- Credit-budget notes in `competitor-gap-analysis` and `keyword-cluster-planner`.
- Form-endpoint note in `agency-landing-page` output.

### Fixed
- `content-brief` and `competitor-gap-analysis` now document the `DATA_getDomainCompetitors` overflow: that endpoint has no upstream `limit`/`offset` and returns ~60KB, so the MCP harness writes it to a file. Skills now instruct: read the file, parse `{data: [...]}`, sort by `common_keywords` desc, take top 5.

### Removed
- Empty `examples/` directory placeholder (replaced with a real example run, see Added).

### Examples
- Added [`examples/ai-search-share-of-voice-wix-com-20260427/`](examples/ai-search-share-of-voice-wix-com-20260427/) — an end-to-end run of `ai-search-share-of-voice` against Wix vs Weebly / Hostinger / Squarespace / Webflow. Includes leaderboard, heatmap, prompt samples, topic cluster ownership analysis, and a finished `REPORT.md`. Snapshot dated 2026-04-27.

## [0.1.0] — 2026-04-24

- Initial release: 7 skills covering content briefs, AI-search reports, audit diffs, backlink gaps, keyword clusters, competitor gaps, and agency landing pages.
