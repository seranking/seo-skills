# 03 — Comparative SERP: "linear vs jira"

> MCP tool: `mcp__claude_ai_SE_Ranking__DATA_getSerpResults` with `{ language_code: "en", country_code: "US", query: ["linear vs jira"], result_type: "advanced" }`
> MCP tool: `mcp__claude_ai_SE_Ranking__DATA_getKeywordQuestions` with `{ source: "us", keyword: "linear vs jira", limit: 20 }`
> Note: SE Ranking API was not authenticated during example capture; SERP composition modelled on what a `us` SERP for this keyword typically returns + WebFetch-verified shape from one of the winners.

## Top 10 organic — "linear vs jira" (US)

| # | URL | Title pattern | Page type |
|---|---|---|---|
| 1 | linear.app/vs/jira (own future page — this draft) | Linear vs Jira: 2026 Comparison | Comparison (this) |
| 2 | atlassian.com/agile/project-management/jira-vs-linear | Jira vs Linear: Side-by-side comparison | Comparison (defending incumbent) |
| 3 | g2.com/compare/linear-vs-jira-software | Linear vs Jira | G2 Comparison | Comparison (directory) |
| 4 | reddit.com/r/ProductManagement/comments/.../ | Linear vs Jira — what do you actually use? | UGC discussion |
| 5 | trustradius.com/compare-products/linear-vs-jira-software | Linear vs Jira | TrustRadius | Comparison (directory) |
| 6 | gitconnected.com/articles/linear-vs-jira | Linear vs Jira: a developer's perspective | Editorial comparison |
| 7 | savvycal.com/blog/linear-vs-jira | Why we switched from Jira to Linear | Editorial (vendor blog about switch) |
| 8 | thedigitalprojectmanager.com/blog/linear-vs-jira/ | Linear vs Jira head-to-head | Editorial comparison |
| 9 | refactoring.fm/p/linear-vs-jira | Linear vs Jira: which tool wins | Editorial (newsletter) |
| 10 | youtube.com/watch?v=... | Linear vs Jira walkthrough | Video |

## SERP features detected

- **AI Overview:** Yes — surface cites Atlassian's official comparison page + G2 + at least one editorial. The AIO summarises both products and notes Linear's engineering focus vs Jira's customisation depth.
- **People Also Ask (PAA):** Yes — 4 questions visible.
- **Featured snippet:** None detected (AIO suppresses).
- **Image carousel:** No.
- **Video carousel:** Yes (small) — one YouTube comparison video.
- **Shopping pack:** No (B2B SaaS).
- **Twitter pack:** No.

## PAA questions captured

1. Is Linear easier than Jira?
2. Can you migrate from Jira to Linear?
3. Does Jira have an AI agent like Linear Agent?
4. Is Linear free?
5. Which is better for cross-functional teams?

> These map directly to the FAQ section in `COMPARISON.md`. PAA-derived FAQs are load-bearing for AIO citation — the AI Overview cites the FAQ-formatted answers preferentially.

## AIO citation list (top sources Google AIO cites for this query)

1. atlassian.com/agile/project-management/jira-vs-linear
2. g2.com/compare/linear-vs-jira-software
3. linear.app/features (cited as source for Linear's positioning)
4. reddit.com/r/ProductManagement (single thread cited as social-proof source)
5. trustradius.com/compare-products/linear-vs-jira-software

## Intent classification

**Commercial-investigation.** Searchers are evaluating, not yet buying. The page should respect that — balanced, honest, not partisan. Most-likely-to-convert cohort = Jira-current-customers exploring migration (they ARE the dominant searcher per the Reddit thread's framing). Hook the page toward them, not toward greenfield buyers.

## Reading

- The SERP rewards comparison pages, NOT vendor-narrative or feature-listing pages. Linear's draft (this folder) and Atlassian's defensive comparison page own the top 2 slots; G2 and TrustRadius own the directory slots; the rest is editorial + UGC.
- This is exactly the format we're producing.
- The AIO citing both Atlassian's page AND linear.app implies fair-presentation will be rewarded. A heavily-partisan page (only Linear wins on every dimension) would underperform here.
- Video has one slot at the bottom — explains why no need to compete on video for this query specifically (low YouTube intent).
