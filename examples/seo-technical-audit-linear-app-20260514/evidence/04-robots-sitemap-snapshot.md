# robots.txt + sitemap.xml snapshot

Source: `mcp__firecrawl-mcp__firecrawl_scrape` on `https://linear.app/robots.txt` and `https://linear.app/sitemap.xml` (2026-05-14).

## robots.txt (verbatim)

```
User-Agent: *
Disallow: /api/
Disallow: /cdn-cgi/
Allow: /api/og/

Sitemap: https://linear.app/sitemap.xml
```

Findings:
- One `User-Agent: *` block covering all crawlers.
- Disallow on `/api/` is necessary (auth-protected backend). Carve-out for `/api/og/` is correct — the dynamic OG-image route is referenced from `og:image` meta tags across the marketing site (e.g., `https://linear.app/api/og/customers?slug=openai`).
- Disallow on `/cdn-cgi/` is Cloudflare's internal namespace.
- One `Sitemap:` declaration — points to the master sitemap (no sitemap index).
- **No AI-bot directives.** Implicit allow for `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `CCBot`, `Bytespider`, `ChatGPT-User`. Confirmed via curl with each User-Agent — all return HTTP 200 on `/`.

## sitemap.xml summary

- **896 URLs** in a single (non-indexed) sitemap.
- **852 URLs** (95%) have `<lastmod>` timestamps.
- **44 URLs** (5%) have no `<lastmod>` — mostly root-level marketing pages.
- **196 URLs** (22%) have `lastmod` older than 2024-01-01.
- **Oldest `lastmod`:** `2020-07-07T19:02:57Z`.
- **Newest `lastmod`:** `2026-05-11T21:34:19Z` (3 days before this audit).

### Top buckets by URL count

```
integrations: 274 URLs (30.6%)
changelog:    236 URLs (26.3%)
docs:         150 URLs (16.7%)
root-level:    99 URLs (11.0%)
blog:          51 URLs (5.7%)
customers:     39 URLs (4.4%)
developers:    25 URLs (2.8%)
method:        11 URLs (1.2%)
releases:       4 URLs (0.4%)
switch:         3 URLs (0.3%)
contact:        2 URLs (0.2%)
security:       1 URL  (0.1%)
startups:       1 URL  (0.1%)
```

### Stale entries (lastmod < 2024-01-01) — first 10

```
2023-12-14 - https://linear.app/changelog/2023-12-14-github-issues-sync
2023-12-06 - https://linear.app/changelog/2023-12-06-editor-improvements
2023-11-15 - https://linear.app/changelog/2023-11-15-github-workflow-updates
2023-11-08 - https://linear.app/changelog/2023-11-08-resolve-comments
2023-10-25 - https://linear.app/changelog/2023-10-25-linear-asks
2023-10-17 - https://linear.app/changelog/2023-10-12-triage-responsibility
2023-11-07 - https://linear.app/changelog/2023-09-28-resize-images
2023-10-11 - https://linear.app/changelog/2023-09-21-project-templates
2023-09-15 - https://linear.app/changelog/2023-08-30-mentions
2023-08-16 - https://linear.app/changelog/2023-08-16-project-progress-reports
```

The pattern: changelog entries published in 2020-2023 remain in the sitemap. They are reachable, served HTTP 200, and counted toward Linear's indexable surface. They are also exactly the entries with the most stale `lastmod` values — a signal to crawlers that they don't change, but they still consume crawl budget.

## sitemap → audit cross-check

The `seo-sitemap` skill cross-references the sitemap against the SE Ranking audit's discovered URLs to surface:
- (a) sitemap entries the audit's crawler couldn't find (orphan from sitemap),
- (b) audit pages missing from the sitemap (probably oversight),
- (c) sitemap entries that are now 404,
- (d) lastmod inconsistencies.

This skill (technical audit) doesn't run that cross-check directly — handoff to `seo-sitemap` is recommended.
