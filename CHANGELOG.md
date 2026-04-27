# Changelog

All notable changes to this project will be documented in this file. Format based on Keep a Changelog.

## [0.1.1] — 2026-04-27

### Changed
- Standardized output folder slugs to `{skill-slug}-{target-slug}-{YYYYMMDD}/` across all skills.
- Removed PROJECT_API_TOKEN mention from README. The 7 current skills only need a single Data API token; the README no longer suggests otherwise.

### Added
- Rate-limit tip in `agency-landing-page` for parity with other skills.
- WebFetch declared in Prerequisites of `content-brief` and `backlink-gap`.
- Credit-budget notes in `competitor-gap-analysis` and `keyword-cluster-planner`.
- Form-endpoint note in `agency-landing-page` output.

### Removed
- Empty `examples/` directory (advertised but unpopulated — returns in v1.0.0).

## [0.1.0] — 2026-04-24

- Initial release: 7 skills covering content briefs, AI-search reports, audit diffs, backlink gaps, keyword clusters, competitor gaps, and agency landing pages.
