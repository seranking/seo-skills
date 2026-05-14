# seo-google — Quickstart bundle (NOT a full example output)

> Snapshot dated 2026-05-14 · This is a **quickstart**, not a canonical example output, because `seo-google` is a heterogeneous CLI surface over multiple Google APIs (GSC, PSI, CrUX, Indexing, GA4, YouTube, NLP, Knowledge Graph, Web Risk, Google Ads Keyword Planner). Each command has its own output shape — there's no single canonical deliverable to ship as an example.

## Why this folder is different from every other example

The other 23 skills in this catalogue each have a single canonical output contract (`REPORT.md`, `BRIEF.md`, `LOCAL-SEO-REPORT.md`, etc.). `seo-google` is a CLI surface — `pagespeed`, `gsc`, `crux-history`, `ga4`, `inspect`, `youtube`, `keywords`, etc. — each returns a different JSON or rendered report. Producing "one example" would mis-frame the skill.

This folder ships **three sample reports** representing the most common command paths:

1. `sample-gsc-search-analytics.md` — Search Console Search Analytics (impressions, clicks, CTR, position).
2. `sample-pagespeed.md` — PageSpeed Insights v5 with Lighthouse lab + CrUX field data.
3. `sample-crux-history.md` — 25-week CrUX field-data trend.

Each is labelled as a **template** ("what you'll see when you run this") because the API credentials weren't available during example capture. Run the scripts with real credentials and you'll get the same shape with your data.

## How to actually use seo-google

1. **Set up credentials.** Run the `setup` command (or read `references/auth-setup.md` in the skill). Minimum: a Google Cloud project + API key gets you Tier 0 (`pagespeed`, `crux`, `crux-history`, `youtube`, `nlp`, `entity`, `safety`). Add a service account JSON for Tier 1 (`gsc`, `inspect`, `sitemaps`, `index`). Add GA4 property ID for Tier 2. Add Google Ads developer token for Tier 3 (keyword research).

2. **Check current tier.** `python scripts/google_auth.py --check --json` — confirms which commands are available.

3. **Pick the command for the question.** See the Quick Reference table in `skills/seo-google/SKILL.md`. Common starting points:
   - "Real Core Web Vitals on this URL" → `pagespeed <url>` or `crux <url>` for field-only.
   - "Real GSC clicks / impressions for last 28 days" → `gsc <property>`.
   - "Is Google actually indexing this URL?" → `inspect <url>`.
   - "AI Overview citation share via GSC" → `gsc <property> --ai-overview`.
   - "GA4 organic traffic for this landing page" → `ga4-pages <property-id> --page <url>`.

4. **Combine with other skills.** `seo-google` bridges crawl-based analysis (the rest of this catalogue) with Google's real field data. See `skills/seo-google/references/cross-skill-integration.md` (and the SKILL.md "Cross-Skill Integration" section) for how to weave Google's data into `seo-technical-audit`, `seo-drift`, `seo-page`, etc.

## When NOT to use seo-google

- For the SE Ranking-driven analysis flows (`seo-keyword-cluster`, `seo-content-brief`, `seo-page`, etc.), the SE Ranking MCP path is the primary one. `seo-google` is the supplement, not the replacement.
- For brand-vs-brand AI Search visibility (`seo-ai-search-share-of-voice`), SE Ranking's AIO leaderboard is the primary source. `seo-google`'s `gsc --ai-overview` gives YOU your own first-party AIO data — the brand-vs-brand visibility comparison still requires SE Ranking's prompt-database tooling.

## What's in each sample report

### `sample-gsc-search-analytics.md`
Last 28 days of GSC Search Analytics for a fictional B2B SaaS domain. Shape mirrors what `scripts/gsc_query.py --property <p> --days 28 --json` produces, post-aggregation into the `--report gsc-performance` format. Demonstrates: query/page table, quick-win detection (positions 4-10 with impression volume), CTR outliers.

### `sample-pagespeed.md`
PageSpeed Insights output for a homepage. Mobile + desktop strategies, all Lighthouse categories. Demonstrates: CrUX field data (LCP / INP / CLS / FCP / TTFB), Lighthouse lab scores, Opportunities + Diagnostics list, the trafficked-light rating per metric.

### `sample-crux-history.md`
25-week CrUX History for the same URL. Demonstrates: weekly p75 series per metric, trend direction (improving/stable/degrading), percentage change vs first week of window. The narrative that the CWV trend analysis surfaces — "your LCP has been degrading for 8 weeks" — is the actionable takeaway.

## Cost note

All `seo-google` commands are **free** (under standard Google API rate limits). PSI v5 = 25,000 queries/day on a single API key, more than enough for individual analysis. The cost in this skill is your Google Cloud setup time (Tier 0 = ~5 minutes with API key; Tier 1 = ~15 minutes with service account; Tier 2 = ~20 minutes with GA4 property).

## What's NOT in this quickstart bundle

- The `youtube` / `nlp` / `entity` / `keywords` / `safety` commands aren't sampled here — they're documented in `skills/seo-google/SKILL.md` and the underlying `references/` files. If you need a sample of those, run them once with the real API and use that output as your reference.
- The Indexing API (`index <url>`) isn't sampled — its output is just a 200 confirmation. Read the SKILL.md note on the JobPosting / VideoObject restriction before using it for general URLs.

## Files

- `sample-gsc-search-analytics.md` — template GSC output
- `sample-pagespeed.md` — template PSI + CrUX output
- `sample-crux-history.md` — template CrUX 25-week history
