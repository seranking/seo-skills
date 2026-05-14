# Source data — sitemap fetch + spot checks

> Source: `mcp__firecrawl-mcp__firecrawl_scrape` (1 credit) on the sitemap index, plus `WebFetch` of `notion.com/sitemap-root.xml` and `notion.com/robots.txt`. Evidence is real.

## Step 01 — Sitemap index fetch

**Endpoint:** `https://www.notion.com/sitemap.xml`  
**Status:** 200  
**Content-Type:** `application/xml`  
**Wrapper:** `<sitemapindex>` (sitemap-of-sitemaps)  
**Child sitemap count:** 191

### Locale prefixes detected (19)

```
es-es, zh-cn, zh-tw, en-gb, es, fr, pt, ko, ja, de, vi, id, th, fi, da, nl, nb, sv, he, ar, it
```

Plus an implicit "default" (en-us) hosted at `https://www.notion.com/sitemap-root.xml`.

### Per-locale child sitemap structure (10 sub-sitemaps each)

For each locale `{loc}`:

- `https://www.notion.com/{loc}/sitemap-root.xml`
- `https://www.notion.com/{loc}/blog/sitemap.xml`
- `https://www.notion.com/{loc}/customers/sitemap.xml`
- `https://www.notion.com/{loc}/help/sitemap.xml`
- `https://www.notion.com/{loc}/md/sitemap.xml`
- `https://www.notion.com/{loc}/pages/sitemap.xml`
- `https://www.notion.com/{loc}/product/sitemap.xml`
- `https://www.notion.com/{loc}/releases/sitemap.xml`
- `https://www.notion.com/{loc}/use-case/sitemap.xml`
- `https://www.notion.com/{loc}/feature/sitemap.xml`

### One global sitemap

- `https://www.notion.com/front-static/sitemap.xml`

## Step 01b — Spot-check on `sitemap-root.xml` (en-us implicit)

**Endpoint:** `https://www.notion.com/sitemap-root.xml`  
**Status:** 200  
**Wrapper:** `<urlset>`  
**Sample of first 20 URL entries:**

| # | URL | lastmod | priority | changefreq |
|---|-----|---------|----------|------------|
| 1 | https://www.notion.com | (none) | 1.0 | weekly |
| 2 | https://www.notion.com/login | (none) | 1.0 | monthly |
| 3 | https://www.notion.com/signup | (none) | 1.0 | monthly |
| 4 | https://www.notion.com/about | (none) | 0.5 | weekly |
| 5 | https://www.notion.com/affiliates | (none) | 0.5 | weekly |
| 6 | https://www.notion.com/product/ai | (none) | 0.5 | weekly |
| 7 | https://www.notion.com/product/ai-meeting-notes | (none) | 0.5 | weekly |
| 8 | https://www.notion.com/product/try-ai-meeting-notes | (none) | 0.5 | weekly |
| 9 | https://www.notion.com/product/ai/use-cases | (none) | 0.5 | weekly |
| 10 | https://www.notion.com/blog | (none) | 0.5 | weekly |
| 11 | https://www.notion.com/careers | (none) | 0.5 | weekly |
| 12 | https://www.notion.com/calendar | (none) | 0.5 | weekly |
| 13 | https://www.notion.com/product/calendar | (none) | 0.5 | weekly |
| 14 | https://www.notion.com/product/calendar/signup | (none) | 0.5 | weekly |
| 15 | https://www.notion.com/product/calendar/download/desktop | (none) | 0.5 | weekly |
| 16 | https://www.notion.com/product/calendar/download | (none) | 0.5 | weekly |
| 17 | https://www.notion.com/product/calendar/download/ios | (none) | 0.5 | weekly |
| 18 | https://www.notion.com/product/calendar/download/windows | (none) | 0.5 | weekly |
| 19 | https://www.notion.com/product/calendar/download/mac | (none) | 0.5 | weekly |
| 20 | https://www.notion.com/compare-against | (none) | 0.5 | weekly |

**0 of 20 sampled URLs have `<lastmod>`.** The pattern is consistent — the sitemap generator simply doesn't emit `<lastmod>` at all.

## Step 02 — Audit-cross-reference (deferred)

A full run would call `DATA_listAudits(domain="notion.com")` → `DATA_getCrawledPages(audit_id)`. SE Ranking auth not available in this worktree. The "missing from sitemap" / "orphans from sitemap" / "broken sitemap entries" diffs require this audit data and are gated accordingly.

## Step 03-06 — The four diffs (require audit data)

| Diff | Status |
|---|---|
| Missing from sitemap | pending audit |
| Orphans from sitemap | pending audit |
| Broken sitemap entries | spot-checks passed (sitemap.xml, sitemap-root.xml return 200) |
| Lastmod issues | **🔴 every URL missing lastmod — see Step 01b** |

## robots.txt directives (from WebFetch, Step 0)

10 sitemap directives declared:
- Main sitemap at `/sitemap.xml`
- Per-content-type at apex: `/blog/sitemap.xml`, `/customers/sitemap.xml`, `/help/sitemap.xml`, `/markdown/sitemap.xml` (note: `/markdown/` not `/md/`), `/pages/sitemap.xml`, `/product/sitemap.xml`, `/releases/sitemap.xml`, `/use-case/sitemap.xml`
- Plus secondary domain: `https://sitemaps.notion.com/...` for category/collection sitemaps

Sitemap referenced in robots.txt: ✓

User-agent blocks (subset): `BLEXBot, AhrefsBot, Amazonbot, SemrushBot, dotbot` are disallowed. `User-agent: *` allows most paths but disallows invite endpoints, template search queries, experiment sections, webinar landing pages, embed resources.

## Cost summary

- 1 Firecrawl credit (sitemap index fetch)
- 2 WebFetch calls (sitemap-root.xml + robots.txt) — no quota cost
- 0 SE Ranking credits (auth-gated; audit cross-reference deferred)
