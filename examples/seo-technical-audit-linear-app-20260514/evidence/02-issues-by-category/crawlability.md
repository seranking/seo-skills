# Issues — Crawlability

Source: `curl -sI` + `mcp__firecrawl-mcp__firecrawl_scrape` on 8 sample URLs and the parsed XML sitemap (`https://linear.app/sitemap.xml`, 896 URL entries).

## Status code sweep

| URL | Status | Notes |
|---|---:|---|
| https://linear.app/ | 200 | served via Cloudflare + Next.js (`x-nextjs-cache: HIT`) |
| https://linear.app/pricing | 200 | |
| https://linear.app/method | 200 | (308 if `/method/` requested with trailing slash → redirects to `/method`) |
| https://linear.app/customers | 200 | |
| https://linear.app/customers/openai | 200 | rendered by `[slug]` dynamic route |
| https://linear.app/agents | 200 | |
| https://linear.app/features | 200 | |
| https://linear.app/insights | 200 | |
| https://linear.app/blog | 307 | redirect chain; final destination is the blog landing page |
| https://linear.app/api/ | 308 | redirect; correctly disallowed in robots.txt |
| https://linear.app/cdn-cgi/ | 404 | Cloudflare-internal; correctly disallowed |

## robots.txt

```
User-Agent: *
Disallow: /api/
Disallow: /cdn-cgi/
Allow: /api/og/

Sitemap: https://linear.app/sitemap.xml
```

Findings:
- Disallow on `/api/` + carve-out for `/api/og/` (the OG-image route used in `og:image` meta) is correct and intentional.
- No AI-bot directives. `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `CCBot` all fall under `User-Agent: *` → implicit allow. Confirmed by curl with each UA on `/` (all return 200).

## Sitemap structure (896 URLs)

| Bucket | Count | % of sitemap |
|---|---:|---:|
| /integrations/* | 274 | 30.6% |
| /changelog/* | 236 | 26.3% |
| /docs/* | 150 | 16.7% |
| root-level (e.g. /, /pricing, /method) | 99 | 11.0% |
| /blog/* | 51 | 5.7% |
| /customers/* | 39 | 4.4% |
| /developers/* | 25 | 2.8% |
| /method/* | 11 | 1.2% |
| /releases/* | 4 | 0.4% |
| /switch/* | 3 | 0.3% |
| /contact/* | 2 | 0.2% |
| /security/*, /startups/* | 2 | 0.2% |

## lastmod hygiene

- 852/896 URLs (95%) have `<lastmod>` — good baseline.
- 44/896 URLs (4%) have no `<lastmod>` — most are root-level marketing pages (`/`, `/pricing`, `/about`, `/agents`, `/method`, etc).
- 196/852 URLs (23% of those with lastmod) have `lastmod` older than 2024-01-01.
- Oldest lastmod observed: `2020-07-07T19:02:57Z`.
- Most recent: `2026-05-11T21:34:19Z`.

## Caching

- `cache-control: s-maxage=120, stale-while-revalidate=31535880` — 2-minute fresh, 365-day SWR window.
- `x-nextjs-cache: HIT`, `x-nextjs-prerender: 1` — Next.js ISR (Incremental Static Regeneration).
- Combined with a 365-day SWR, lastmod accuracy in the sitemap is what tells Googlebot whether to re-fetch on its own cadence vs trust the cache.
