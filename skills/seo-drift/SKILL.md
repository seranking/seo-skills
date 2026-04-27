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
2. **Preflight.** `DATA_getCreditBalance` — typical baseline costs ~10–20 credits depending on whether step 5 is included.
3. **Domain snapshot** (always):
   - `DATA_getDomainOverviewWorldwide` — DA, traffic, organic + paid keyword counts.
   - `DATA_getDomainKeywords` — top 100 organic keywords with positions.
   - `DATA_getBacklinksSummary` — backlinks total, referring domains total.
   - `DATA_getBacklinksRefDomains` — top 20 referring domains with authority.
4. **Page snapshot** (if target is a URL): `WebFetch` the URL.
   - Extract: `<title>`, meta description, all `<h1..h6>`, canonical URL, robots meta, lang attribute, schema types present (parse JSON-LD), word count, internal-link count, image count.
   - Compute a fingerprint hash of the above structure.
   - Also capture page authority: `DATA_getPageAuthority`.
5. **Write snapshot file** `seo-drift-{target-slug}-{YYYYMMDD}/snapshot.json`.
6. **Update index** `seo-drift-{target-slug}/baselines.json` — append `{date, snapshot_path}` entry.

### compare mode

1. **Validate target + locate latest baseline** in `seo-drift-{target-slug}/baselines.json`.
   - If no baseline exists, fall through to baseline mode and tell the user to come back later.
2. **Capture current state** (same data as baseline mode).
3. **Diff** each metric using `references/drift-thresholds.md`:
   - Domain authority: ±5 = yellow, ±10 = red.
   - Estimated organic traffic: ±20% = yellow, ±50% = red.
   - Organic keyword count: ±10% = yellow, ±30% = red.
   - Top-3 keyword count: ±15% = yellow, ±40% = red.
   - Top-100 keyword churn: any high-volume drop = red.
   - Net referring domains: -5 to -20 = yellow, <-20 = red.
   - Page-level (URL mode): any change to canonical / robots / lang / H1 = red; title or meta description change = yellow; schema types added/removed = yellow.
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
├── baseline-snapshot.json   (the prior reference)
├── current-snapshot.json    (today's state)
├── 01-domain-deltas.md      (DA, traffic, keyword count changes)
├── 02-keyword-churn.md      (top-100 entries/exits)
├── 03-backlink-deltas.md    (new + lost backlinks/domains)
├── 04-page-deltas.md        (URL mode only: HTML fingerprint diff)
└── DRIFT-REPORT.md          (synthesised: red/yellow/green changes)
```

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
- Call `DATA_getCreditBalance` before running. Domain baseline ~10–15 credits; URL baseline ~15–20 credits; compare ~20–30 credits.
- Snapshot storage is **local-only** in v0.4.0. If your team needs shared baselines, point everyone at the same `seo-drift-{target-slug}/` directory in a shared filesystem or commit it to a private repo. Baselines are JSON — git-friendly.
- Baseline cadence: monthly is the natural rhythm because SE Ranking's history endpoints have monthly granularity. Weekly is too noisy for backlink data. Document recommended cadence in handoff to your team.
- For deploy-time "did anything break in the last hour" use cases, the URL-mode page-fingerprint half is the workhorse — that doesn't depend on monthly data.
- Don't auto-disavow or auto-fix anything based on drift findings. The skill diagnoses; humans decide.
- Cost of doing nothing: silent regressions. Cost of running monthly: ~15 credits. Run monthly.
