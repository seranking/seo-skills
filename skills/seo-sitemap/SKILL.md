---
name: seo-sitemap
description: Pull a domain's XML sitemap (and sitemap-of-sitemaps), then compare against the most recent SE Ranking website audit. Surfaces (a) sitemap entries the crawler couldn't find (orphans from the sitemap), (b) audit pages missing from the sitemap (probably an oversight), (c) sitemap entries that are now 404, (d) lastmod inconsistencies. Use when the user asks for "sitemap analysis", "check my sitemap", "sitemap vs audit", "missing pages", "orphan pages", or "sitemap health".
---

# Sitemap Analysis

Compare a domain's XML sitemap against the most recent SE Ranking website audit. Surface what the sitemap claims vs what the crawler actually found, in both directions.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available.
- User provides: a target domain. Optional: the sitemap URL if not at `/sitemap.xml` (auto-discovery from `robots.txt` is attempted first).
- **Predecessor:** `seo-technical-audit` (or any prior SE Ranking audit) on this domain. Without an existing audit, this skill has nothing to compare against — chain `seo-technical-audit` first.

## Process

1. **Validate target & confirm audit**
   - Normalise the domain.
   - `DATA_listAudits` → confirm an audit exists for this domain. If none, surface a clear message: "Run `seo-technical-audit` first; this skill compares the sitemap to that audit's crawl."
   - Use the most recent `done` audit by default.
   - **Firecrawl availability check.** If `mcp__firecrawl-mcp__firecrawl_map` is available, Mode-2 (URL discovery via crawl) is offered when the sitemap is missing or suspect. Cost: ~0.5 Firecrawl credits per URL discovered, hard cap 500 URLs (~250 credits). Without Firecrawl, the skill runs Mode-1 only and notes the gap if Mode-2 was needed. User may pass `--no-firecrawl` to force Mode-1 even when Firecrawl is available (saves credits at the cost of orphan/missing analysis when sitemap is broken).

2. **Build URL lists** `WebFetch` (sitemap) + `mcp__firecrawl-mcp__firecrawl_map` (optional Mode-2)
   - **Mode-1 (default).** Try `https://{domain}/sitemap.xml`. If 404, fetch `/robots.txt` and look for `Sitemap:` directives. For sitemap-of-sitemaps, recursively fetch each child sitemap. Build the canonical URL list from the sitemap.
   - **Mode-2 trigger.** Switch on Mode-2 when (a) no sitemap is reachable, (b) the sitemap returns < 10% of the audit's `DATA_getCrawledPages` count, or (c) the user explicitly requests `--discover`. Always surface the trigger and the cost estimate to the user before running Mode-2.
   - **Mode-2 execution** (requires Firecrawl): call `firecrawl_map(url=domain, limit=500)`. The response is the URL list Firecrawl could discover from the homepage and internal linking. Use this list as the "sitemap-equivalent" in step 6 — the diffs run identically, just with discovered URLs in place of declared sitemap URLs.
   - **If Mode-2 is needed but Firecrawl is unavailable:** continue with whatever sitemap data Mode-1 returned (possibly empty). Surface clearly in `SITEMAP.md`: `Mode-2 (Firecrawl URL discovery) needed but Firecrawl not installed — sitemap-vs-audit diffs run on partial data only.`

3. **Pull the audit's crawled pages** `DATA_getCrawledPages`
   - All URLs the crawler found, with status codes, indexability flags, depth.

4. **Pull domain pages** `DATA_getDomainPages`
   - Domain-level page inventory (broader than the audit's crawl scope in some cases).

5. **Pull orphan-page issues** `DATA_getAuditPagesByIssue`
   - Filter for orphan-page and depth-related issues. These intersect with sitemap analysis.

6. **Compute the four diffs**
   - **Missing from sitemap:** URLs in `DATA_getCrawledPages` (status 200, indexable) that don't appear in the sitemap. Probably should be added.
   - **Orphans from sitemap:** URLs in the sitemap that the crawler didn't find via internal links (cross-ref `DATA_getAuditPagesByIssue` orphan flags). The sitemap is the only thing pointing at them — investigate whether they should be linked internally.
   - **Broken sitemap entries:** sitemap URLs that returned non-200 in the audit's crawl. Remove from sitemap or fix the URL.
   - **Lastmod issues:** sitemap entries where (a) all `<lastmod>` dates are identical (lazy generation) or (b) `<lastmod>` is older than the audit's crawl date for the page even though the page changed (stale).

7. **Validation**
   - URL count <50,000 per file (sitemap protocol limit). Flag if exceeded.
   - Sitemap referenced in `robots.txt`.
   - Encoding: each URL is XML-safe (ampersands escaped, etc.).
   - HTTPS consistency: sitemap URLs match the canonical protocol.
   - **`<lastmod>` is the only optional tag Google still consumes.** Validate it (step 6). `<priority>` and `<changefreq>` have been **explicitly ignored by Google for years** (per [Google's sitemap docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) — "Google ignores `priority` and `changefreq` values"). Don't validate them; if present, flag as low-signal noise the user can strip to shrink the sitemap.

8. **Synthesise** `SITEMAP.md`

## Output format

Create a folder `seo-sitemap-{target-slug}-{YYYYMMDD}/` with:

```
seo-sitemap-{target-slug}-{YYYYMMDD}/
├── SITEMAP.md                       (synthesised report — primary deliverable)
├── recommended-sitemap-diff.md      (proposed changes: add X, remove Y — load-bearing artefact engineering applies to sitemap.xml)
└── evidence/
    └── source-data.md               (consolidated raw step output: fetched sitemap content, Firecrawl-discovered URLs if Mode-2 ran, audit's crawled-pages list, the four diffs (missing/orphans/broken/lastmod-issues) — preserved for reproducibility)
```

Top-level: `SITEMAP.md` + `recommended-sitemap-diff.md`. The seven raw step files (`01-sitemap-raw`, `01b-firecrawl-discovered`, `02-audit-pages`, `03-missing-from-sitemap`, `04-orphans-from-sitemap`, `05-broken-entries`, `06-lastmod-issues`) are consolidated into a single `evidence/source-data.md` document with the same per-step section headers — a reader who needs to replay the diff has all raw inputs in one file rather than seven.

`SITEMAP.md` follows this shape:

```markdown
# Sitemap Analysis: {domain}

> Sitemap pulled {YYYY-MM-DD} · Audit reference {audit-date}

## Mode

- **Mode-1 (sitemap-vs-audit):** {ran / skipped — no sitemap reachable}
- **Mode-2 (Firecrawl URL discovery):** {ran with {n} URLs / not triggered / triggered but Firecrawl not installed}

## Health summary

| Metric | Value | Status |
|---|---|---|
| Sitemap URLs (Mode-1) | {n} | — |
| Discovered URLs (Mode-2, if ran) | {n} | — |
| Audit crawled URLs (200, indexable) | {n} | — |
| Missing from sitemap (probable adds) | {n} | {🔴 if >5%} |
| Orphans from sitemap (probable cuts or link-ins) | {n} | {🟡 if >5} |
| Broken sitemap entries (non-200) | {n} | {🔴 if >0} |
| Lastmod issues | {n} | {🟡 if uniform; 🔴 if stale} |

## Recommended changes

### Add to sitemap ({n} URLs)
- {URL} — found by crawler at depth {n}, status 200, indexable.
- ...

### Remove from sitemap ({n} URLs)
- {URL} — returns {status code}.
- ...

### Investigate (orphan from sitemap, {n} URLs)
- {URL} — in sitemap but not reachable via internal links. Either link from {suggested parent} or remove from sitemap.
- ...

### Fix lastmod ({n} URLs)
- {URL} — lastmod is {date} but the audit crawled the page on {date} and detected changes since.
- ...

## Validation

- Total URL count: {n} ({✓ under 50k limit | ✗ exceeds — split into sitemap-of-sitemaps})
- Referenced in robots.txt: {✓/✗}
- HTTPS consistency: {✓/✗}
- Encoding: {✓/✗}

## Apply
- See `recommended-sitemap-diff.md` for the proposed sitemap.xml changes.
- After applying, re-run `seo-technical-audit` to refresh the crawl, then re-run this skill to verify.
```

## Tips

- Run `seo-technical-audit` first. Without an audit, this skill has nothing to compare.
- Re-run after deploys that change page inventory (new content, removed pages, URL restructures).
- Sitemap-of-sitemaps fan-out can be large for big sites — the skill recursively fetches all child sitemaps. For sites with 50+ child sitemaps, fetching dominates runtime; not credit cost.
- `<priority>` and `<changefreq>` are dead signals — Google explicitly ignores both. Don't waste time tuning them; if your sitemap generator emits them, the bytes are pure overhead. `<lastmod>` is still consumed, so keep that one accurate.
- The "investigate orphans" list is often the highest-leverage finding — pages that exist but aren't linked are usually accidentally orphaned, and adding a couple of internal links can revive them.
- Pair with `seo-drift` to track sitemap composition over time (URL count, lastmod patterns).
- Cost: ~5–10 SE Ranking credits typical (mostly the `getCrawledPages` and `getDomainPages` calls). Mode-2 adds Firecrawl credits at ~0.5 per discovered URL — surface the estimate before triggering.
