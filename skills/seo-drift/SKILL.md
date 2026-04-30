---
name: seo-drift
description: Capture an SEO baseline snapshot for a domain or URL, then on later runs compare the current state and surface regressions. Tracks authority, traffic, keywords, backlinks, and on-page content. Three subcommands — `baseline`, `compare`, `history`. Use when the user asks for "SEO drift", "baseline this site", "did anything break", "SEO regression check", "compare before and after", "deployment check", or "monthly SEO snapshot".
---

# SEO Drift

Git for SEO. Capture a snapshot of a domain or URL's SEO state ("baseline"), then on later runs diff the current state against the baseline and surface regressions. Catches the things that get worse silently after a deploy, redesign, or content cull.

> **Acknowledgements:** drift-as-an-SEO-skill framework originated in `claude-seo` by AgriciDaniel (with the original concept credited to Dan Colta, Pro Hub Challenge). MIT-licensed both directions; this implementation is independent but the framing is theirs.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available (for URL-mode page fingerprinting).
- User provides: target domain or URL, plus a subcommand (`baseline`, `compare`, `history`).

## Optional flags

| Flag | Mode | Effect |
|---|---|---|
| `--no-firecrawl` | baseline, compare | Skip Firecrawl-based `<head>` + JSON-LD capture even when Firecrawl is installed (saves credits at the cost of canonical / robots / og:* / JSON-LD diff coverage). |
| `--skip-cwv` | baseline, compare | Skip the Google CrUX capture (step 4b) even when `google-api.json` is configured. Useful when you only care about content/structural drift, or when CrUX rate-limit concerns outweigh CWV coverage. Mirrors theirs at `seo-drift/SKILL.md:107, 131`. |
| `--baseline-id <n>` | compare | Compare against a specific baseline by ID rather than the most recent. |
| `--limit <n>` | history | Cap the number of historical entries shown. |

## Subcommands

### `baseline <target>`
Capture the current SEO state and write it to a snapshot file. No diff produced.

### `compare <target>`
Load the most recent baseline for the target. Capture the current state. Diff. Produce `DRIFT-REPORT.md`.

### `history <target>`
List all stored baselines for the target with their dates and key metrics (DA, traffic, keyword count). No diff produced.

## Process

### baseline mode

1. **Validate target.** Determine if domain or URL. Domain = `example.com`; URL = anything starting with `http(s)://`.
   - **SSRF protection (URL mode).** If target is a URL, validate via `python3 -c "from scripts.google_auth import validate_url; import sys; sys.exit(0 if validate_url('{target}') else 1)"` (or import `validate_url` directly in any helper script). Reject loopback (127.0.0.1, ::1, localhost), private IP ranges (10/8, 172.16/12, 192.168/16), link-local (169.254/16), and Google metadata endpoints. If validation fails, abort with a clear error and don't proceed to fetch — feeding an unvalidated URL into Firecrawl / WebFetch / Google APIs would risk SSRF against internal services. Mirrors theirs at `seo-drift/SKILL.md:97`.
2. **Preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (credit balance, Firecrawl availability, Google APIs). Skill-specific notes:
   - Estimated SE Ranking cost for this skill: typical baseline costs ~10–20 SE Ranking credits depending on whether step 4 (URL-mode page snapshot) is included.
   - Firecrawl: optional with WebFetch fallback, +1 Firecrawl credit per URL if available (URL mode). When available, the snapshot also captures `<head>` + JSON-LD content so canonical / robots / og:* / JSON-LD changes are detectable on diff. Without it the snapshot is partial. Pass `--no-firecrawl` to skip Firecrawl even when available (saves credits at the cost of diff coverage).
   - Google APIs: tier 0 unlocks CrUX p75 LCP/INP/CLS capture (origin in domain mode, URL in URL mode); tier 1 (URL mode only) additionally captures URL Inspection state (`indexStatusVerdict`, `googleCanonical`, `lastCrawlTime`) so subsequent compares can flag field-data and indexation drift. See `skills/seo-google/references/cross-skill-integration.md` § "seo-drift" for the full recipe.
3. **Domain snapshot** (always):
   - `DATA_getDomainOverviewWorldwide` — DA, traffic, organic + paid keyword counts.
   - `DATA_getDomainKeywords` — top 100 organic keywords with positions.
   - `DATA_getBacklinksSummary` — backlinks total, referring domains total.
   - `DATA_getBacklinksRefDomains` — top 20 referring domains with authority.
4. **Page snapshot** (if target is a URL): `WebFetch` (always) + `mcp__firecrawl-mcp__firecrawl_scrape` (when available)
   - **WebFetch** (free): extract `<title>`, all `<h1..h6>`, lang, word count, internal-link count, image count, body markdown for prose-level diff.
   - **Firecrawl** (1 Firecrawl credit per URL) — recovers `<head>` and `<script>` content WebFetch strips:
     - From `metadata`: canonical URL, robots meta, og:title, og:description, og:image, twitter:card.
     - From returned `html`: every `<script type="application/ld+json">` block. Capture both detected `@type`s and a hash of the full block content (so any schema-content change is detected on diff, not just type-list changes).
   - **If Firecrawl unavailable (or `--no-firecrawl` passed):** only WebFetch fields enter the fingerprint. `BASELINE.md` notes: `Snapshot fields recovered via WebFetch only — canonical, robots, og:*, twitter:*, and JSON-LD changes will not be detected on subsequent compares. Install Firecrawl for full coverage.`
   - Compute a fingerprint hash of the captured fields.
   - Also capture page authority: `DATA_getPageAuthority`.
4b. **Google field-data snapshot** *(only if google-api.json is present AND `--skip-cwv` not set)*
   - Tier 0 (always when configured): `python3 scripts/pagespeed_check.py "{target}" --crux-only --json` (URL mode) or `python3 scripts/pagespeed_check.py "https://{domain}" --crux-only --json` (domain mode, origin-level CrUX). Store the resulting p75 LCP / INP / CLS / FCP / TTFB and the source label ("URL" or "origin").
   - Tier 0 (always when configured): `python3 scripts/crux_history.py "{target_or_origin}" --json` for the 25-week trend window snapshot — store as `crux_history_baseline`. Subsequent compares can detect drift against the most recent week.
   - Tier 1 (URL mode only): `python3 scripts/gsc_inspect.py "{target_url}" --site-url "{config.default_property}" --json`. Store `indexStatusVerdict`, `coverageState`, `googleCanonical`, `userCanonical`, `lastCrawlTime`.
   - If `--skip-cwv` was passed, skip this step entirely and store `null` for `cwv` / `crux_history` fields. The compare-mode rules then surface "Field-data drift: skipped — `--skip-cwv` flag passed at baseline."
   - If CrUX returns insufficient data, store `null` for the affected metrics and continue.
5. **Write snapshot file** `seo-drift-{target-slug}-{YYYYMMDD}/snapshot.json`.
6. **Update index** `seo-drift-{target-slug}/baselines.json` — append `{date, snapshot_path}` entry.

### compare mode

1. **Validate target + locate latest baseline** in `seo-drift-{target-slug}/baselines.json`.
   - **SSRF protection (URL mode).** Same `validate_url()` check as baseline mode. Refuses to fetch private/loopback/metadata addresses.
   - If no baseline exists, fall through to baseline mode and tell the user to come back later.
2. **Capture current state** (same data as baseline mode).
3. **Diff** each metric using `references/drift-thresholds.md`:
   - Domain authority: ±5 = yellow, ±10 = red.
   - Estimated organic traffic: ±20% = yellow, ±50% = red.
   - Organic keyword count: ±10% = yellow, ±30% = red.
   - Top-3 keyword count: ±15% = yellow, ±40% = red.
   - Top-100 keyword churn: any high-volume drop = red.
   - Net referring domains: -5 to -20 = yellow, <-20 = red.
   - Page-level (URL mode): any change to canonical / robots / lang / H1 = red; title or meta description change = yellow; schema types added/removed = yellow; og:* / twitter:* changes = yellow.
   - **Firecrawl-dependent diff caveat:** canonical / robots / og:* / twitter:* / JSON-LD diffs require both baseline and current snapshots to have been captured with Firecrawl. If either snapshot was WebFetch-only, those fields surface as `not comparable — Firecrawl-only fields missing from {baseline | current} snapshot` rather than as a green pass.
   - **Google-data drift** *(only if both snapshots have Google fields)*:
     - LCP p75 increased ≥20% → red.
     - INP p75 increased ≥20% → red.
     - CLS p75 increased ≥0.05 absolute → yellow.
     - FCP / TTFB p75 increased ≥30% → yellow.
     - Inspection status changed from `INDEXED` to anything else → red.
     - `googleCanonical` changed → yellow.
     - `lastCrawlTime` >60 days old → yellow.
     - **Caveat:** if either snapshot lacks Google fields (creds were missing at one capture), surface `Field-data / indexation drift: not comparable — Google fields missing from {baseline | current} snapshot.`
4. **Synthesise** `DRIFT-REPORT.md` — red findings first, then yellow, then green/positive deltas. End with a "what to investigate first" recommendation.

### history mode

1. Load `baselines.json`.
2. For each entry, render a one-row summary: date, DA, traffic, keyword count, top-3 count.
3. Write `HISTORY.md` with the table.

## Output format

### baseline mode
`seo-drift-{target-slug}-{YYYYMMDD}/`:
```
seo-drift-{target-slug}-{YYYYMMDD}/
├── snapshot.json            (the captured state)
└── BASELINE.md              (one-page human summary of what was captured)
```

### compare mode
`seo-drift-{target-slug}-{YYYYMMDD}/`:
```
seo-drift-{target-slug}-{YYYYMMDD}/
├── DRIFT-REPORT.md              (synthesised: red/yellow/green changes — primary deliverable; inlines 01-domain-deltas, 02-keyword-churn, 03-backlink-deltas, 04-page-deltas as sections)
└── evidence/
    ├── baseline-snapshot.json   (the prior reference — kept for replay)
    ├── current-snapshot.json    (today's state — kept for replay)
    ├── 01-domain-deltas.md      (DA, traffic, keyword count changes — raw step output)
    ├── 02-keyword-churn.md      (top-100 entries/exits)
    ├── 03-backlink-deltas.md    (new + lost backlinks/domains)
    └── 04-page-deltas.md        (URL mode only: HTML fingerprint diff)
```

Top-level: `DRIFT-REPORT.md` only. The four delta step files are inlined into named sections in DRIFT-REPORT.md; `evidence/` keeps the raw delta dumps and both snapshot JSONs so a future re-diff or audit can replay against them.

`DRIFT-REPORT.md` shape:

```markdown
# Drift Report: {target}
> Baseline: {baseline date} · Current: {today's date}

## RED — investigate today
- {finding} ({severity rationale})
- ...

## YELLOW — investigate this week
- {finding}
- ...

## GREEN — positive deltas
- {finding}
- ...

## Field-data drift (CrUX + URL Inspection)
- LCP p75: {baseline} → {current} ms ({Δ%}) {↑ red / ↑ yellow / stable / ↓ green}
- INP p75: {baseline} → {current} ms ({Δ%}) {…}
- CLS p75: {baseline} → {current} ({Δ absolute}) {…}
- Indexation status: {baseline INDEXED → current EXCLUDED} (URL mode)
- googleCanonical: {baseline → current} (if changed)
- (Or: `Field-data / indexation drift: not configured` / `not comparable — missing from {snapshot}`)

## What to investigate first
1. {prioritised action with reasoning}
2. ...
```

### history mode
`seo-drift-{target-slug}-{YYYYMMDD}/HISTORY.md`:

```markdown
# History: {target}

| Date | DA | Traffic | Keywords | Top-3 |
|---|---|---|---|---|
| 2026-04-27 | 42 | 18,500/mo | 1,247 | 89 |
| 2026-03-15 | 41 | 17,200/mo | 1,213 | 85 |
| ...
```

## Tips

- Respect rate limit: 10 req/sec. Baseline runs 4–6 sequential calls; pace easily.
- Call `DATA_getCreditBalance` before running. Domain baseline ~10–15 SE Ranking credits; URL baseline ~15–20 SE Ranking credits + 1 Firecrawl credit; compare ~20–30 SE Ranking credits + 1 Firecrawl credit (current-state capture).
- Snapshot storage is **local-only** in v0.4.0. If your team needs shared baselines, point everyone at the same `seo-drift-{target-slug}/` directory in a shared filesystem or commit it to a private repo. Baselines are JSON — git-friendly.
- Baseline cadence: monthly is the natural rhythm because SE Ranking's history endpoints have monthly granularity. Weekly is too noisy for backlink data. Document recommended cadence in handoff to your team.
- For deploy-time "did anything break in the last hour" use cases, the URL-mode page-fingerprint half is the workhorse — that doesn't depend on monthly data.
- Don't auto-disavow or auto-fix anything based on drift findings. The skill diagnoses; humans decide.
- **Authority-history all-zeros caveat:** if `DATA_getPageAuthorityHistory` (URL mode) or `DATA_getDomainAuthorityHistory` returns flat-zero values across the window, treat as "insufficient history" — don't compute a delta or surface a regression based on missing data. Cross-check the current-value endpoint (`DATA_getPageAuthority` / `DATA_getDomainOverviewWorldwide`) — if the current value is meaningful but history is flat, surface that as a data-quality flag in `DRIFT-REPORT.md` rather than fabricating a trend.
- Cost of doing nothing: silent regressions. Cost of running monthly: ~15 credits. Run monthly.
