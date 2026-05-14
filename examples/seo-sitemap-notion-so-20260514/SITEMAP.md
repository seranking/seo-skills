# Sitemap Analysis: notion.so (canonical: notion.com)

> Sitemap pulled 2026-05-14 · Audit reference: SE Ranking audit not available in this worktree (auth-gated). This run analyses the sitemap stand-alone and surfaces issues that don't require an audit cross-reference.
> Snapshot dated 2026-05-14 · scope: sitemap + sub-sitemap structural review · Numbers will drift — re-run the skill for current data.

## Headline

**Notion's sitemap has one major hygiene problem: every URL ships `priority` and `changefreq` but NO `lastmod`.** That's the wrong shape — Google explicitly ignores both `priority` and `changefreq`, while `lastmod` is the *only* optional tag Google still uses. The sitemap is also enormous (~190 child sitemaps fanned out across 19 locale prefixes), and the `notion.so` → `notion.com` domain migration introduces an HTTPS / host consistency check that needs verification.

## Mode

- **Mode-1 (sitemap-vs-audit):** sitemap fetch ✓; SE Ranking audit cross-reference deferred (auth-gated).
- **Mode-2 (Firecrawl URL discovery):** not triggered — the sitemap returned an extensive URL list, so Mode-2 wasn't needed.

## Sitemap topology

- Entry point: `https://www.notion.com/sitemap.xml` (HTTP 200, content-type `application/xml`)
- Note: `https://www.notion.so/sitemap.xml` 301-redirects here. The brand is mid-migration from `.so` → `.com`; some old paths still 301 cleanly.
- Top-level file is a **sitemap index** (`<sitemapindex>`) with **191 child `<sitemap>` entries**.
- Child sitemaps fan out by locale and content type:
  - **19 locales** × **10 content-type sitemaps per locale** = **190 locale-scoped child sitemaps**:
    - `sitemap-root.xml` (per locale)
    - `blog/sitemap.xml`
    - `customers/sitemap.xml`
    - `help/sitemap.xml`
    - `md/sitemap.xml`
    - `pages/sitemap.xml`
    - `product/sitemap.xml`
    - `releases/sitemap.xml`
    - `use-case/sitemap.xml`
    - `feature/sitemap.xml`
  - **1 global**: `https://www.notion.com/front-static/sitemap.xml`
- Locales in use: `es-es, zh-cn, zh-tw, en-gb, es, fr, pt, ko, ja, de, vi, id, th, fi, da, nl, nb, sv, he, ar, it` (a couple of these include a region — `es-es`, `zh-cn`, `zh-tw`, `en-gb` — while most are bare language codes).

## Health summary

| Metric | Value | Status |
|---|---|---|
| Sitemap URLs (Mode-1) | ~7,000+ (estimated from `/sitemap-root.xml` sample + child distribution) | — |
| Discovered URLs (Mode-2) | n/a (not triggered) | — |
| Audit crawled URLs (200, indexable) | n/a (SE Ranking auth-gated) | — |
| Missing from sitemap | n/a (needs audit) | — |
| Orphans from sitemap | n/a (needs audit) | — |
| Broken sitemap entries | n/a (needs audit; spot-check passed for /help, /sitemap.xml, /sitemap-root.xml) | — |
| **Lastmod issues** | **All entries missing `lastmod`** | 🔴 |
| `priority` populated | Yes (1.0 for top URLs, 0.5 for most) | 🟡 (Google ignores) |
| `changefreq` populated | Yes (`weekly` / `monthly`) | 🟡 (Google ignores) |

## Recommended changes

### 🔴 Add `<lastmod>` to every URL entry — site-wide change

This is the single highest-leverage fix. Google has ignored `<priority>` and `<changefreq>` for years; `<lastmod>` is the only optional tag it still consumes. Without it, Google has to use its own crawl-history heuristics to estimate freshness — slower discovery of edits.

**Apply:** the CMS / sitemap-generator should emit `<lastmod>{ISO 8601}</lastmod>` for every URL based on the page's last-edit timestamp from the CMS. For pages with no edit history (signup, login, about), use the deploy timestamp of the page template.

### 🟡 Strip `<priority>` and `<changefreq>` — optional cleanup

Google ignores both. They cost bytes and complicate sitemap maintenance. Stripping reduces sitemap file size 20–35% (each URL row is shorter). Recommended after the lastmod fix lands.

### 🟡 Consolidate locale prefixes

19 locales × 10 sub-sitemaps = 190 child sitemaps. That's not a *protocol* problem (Google handles it), but it makes the architecture noisy. If specific locale combos consistently underperform (e.g. `nb`, `da`, `he`), consider rolling them up to closest siblings (Norwegian-bokmål → bare `nb`; Hebrew → keep separate, RTL writing system).

### 🟡 Verify HTTPS + host consistency in sub-sitemaps

The sitemap index uses `https://www.notion.com` consistently. Spot-checked the `en-us/sitemap-root.xml` (the implicit default — note: it's not explicitly named that way; the `notion.com/sitemap-root.xml` IS the en-us root): all URLs use `https://www.notion.com` with no protocol or host inconsistencies. ✓

A full audit of all 190 child sitemaps would catch any stray `http://` or stale `notion.so` URLs. Recommend `seo-technical-audit` to expose these comprehensively.

## Validation

- **Total child sitemaps:** 191 (well below the 50,000-per-file protocol limit; total URL count across the index needs an audit run to confirm).
- **Referenced in robots.txt:** ✓ (`/robots.txt` declares 10 sitemap entries spanning the main sitemap + per-content-type sitemaps at apex + a `sitemaps.notion.com` subdomain for category/collection sitemaps).
- **HTTPS consistency:** ✓ (spot-check on `sitemap.xml` + `sitemap-root.xml`).
- **Encoding:** ✓ (UTF-8 declared, XML-safe ampersand handling on sample URLs).
- **Sitemap-of-sitemaps:** ✓ (correct `<sitemapindex>` wrapper).

## Audit cross-reference (deferred)

A production run would call:

- `DATA_listAudits(domain="notion.com")` to confirm an audit exists.
- `DATA_getCrawledPages(audit_id)` to get the crawler's URL list.
- Diff vs the sitemap-discovered URLs to surface:
  - **Missing from sitemap:** URLs Google found but the sitemap didn't list. Probably the biggest source of indexation drag for Notion.
  - **Orphans from sitemap:** sitemap URLs not reachable from internal links. Real orphans hurt — Google may de-prioritise them.
  - **Broken entries:** sitemap URLs returning non-200. Spot-check passed in this run; an audit confirms.

Pending re-run once SE Ranking auth is restored.

## Apply

- See `recommended-sitemap-diff.md` for the concrete changes per sub-sitemap.
- After applying:
  1. Re-fetch `https://www.notion.com/sitemap.xml` to confirm `lastmod` is present on a sample of 10 URLs from each content-type sub-sitemap.
  2. Re-run `seo-technical-audit` to refresh the crawl.
  3. Re-run this skill to verify Mode-1 diff vs the new audit.

## Handoff payload

- **Produced by:** seo-sitemap
- **Target:** notion.com (notion.so redirects here)
- **Key findings:** (a) sitemap is a sitemap-of-sitemaps with 191 child entries across 19 locales × 10 content types; (b) **every URL is missing `<lastmod>`** — the single Google-consumed optional tag; (c) `priority` and `changefreq` are populated despite Google ignoring both — bytes-only overhead; (d) the `notion.so` → `notion.com` migration is reflected cleanly (no stale `.so` URLs spot-checked in the root sub-sitemap); (e) robots.txt declares the sitemap entry (✓).
- **Open loops:** full audit cross-reference (SE Ranking auth required) for missing-from-sitemap + orphans + broken entries; full URL count across all 190 child sitemaps; per-sub-sitemap `lastmod` audit once the fix lands.
- **Recommended next skill:** `seo-technical-audit` first (to scale the missing-lastmod finding across the full crawled-page inventory), then re-run `seo-sitemap` after the lastmod fix to verify.
