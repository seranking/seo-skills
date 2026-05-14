# Sample GSC Search Analytics — anchor-seo.com (template — what you'll see when you run this)

> **Template** dated 2026-05-14 · Property: `sc-domain:anchor-seo.com` (fictional) · 28-day window · This is a **template** showing the shape of `python scripts/gsc_query.py --property <p> --days 28 --json` output rendered into the `--report gsc-performance` format. Google API credentials were not available during example capture — run with real credentials and your data will fill this shape.

## Snapshot

- Property: sc-domain:anchor-seo.com
- Window: 2026-04-16 to 2026-05-13 (28 days, US/Pacific)
- Data lag: 2-3 days (GSC standard)
- Dimensions queried: query, page
- Row limit: 1,000
- Tier required: 1 (service account with GSC access)

## Top-level metrics

| Metric | Value | vs prior 28d |
|---|---:|---:|
| Total clicks | 8,742 | +18% |
| Total impressions | 412,508 | +9% |
| Average CTR | 2.12% | +0.18pp |
| Average position | 12.4 | -0.6 (improved) |

## Top 10 queries by clicks

| # | Query | Clicks | Impressions | CTR | Avg Position |
|---|---|---:|---:|---:|---:|
| 1 | anchor seo | 1,824 | 4,212 | 43.31% | 1.1 |
| 2 | b2b saas seo agency | 478 | 9,840 | 4.86% | 8.4 |
| 3 | seo audit free saas | 322 | 11,402 | 2.82% | 11.7 |
| 4 | saas seo audit | 296 | 14,808 | 2.00% | 14.2 |
| 5 | ai overview saas | 248 | 22,142 | 1.12% | 18.4 |
| 6 | saas seo benchmark | 188 | 7,408 | 2.54% | 13.1 |
| 7 | seo for b2b saas | 167 | 13,902 | 1.20% | 15.7 |
| 8 | best saas seo agency | 148 | 6,108 | 2.42% | 12.4 |
| 9 | ai search seo | 124 | 18,402 | 0.67% | 22.8 |
| 10 | seo agency saas founders | 118 | 4,824 | 2.45% | 10.7 |

## Top 10 pages by clicks

| # | Page | Clicks | Impressions | CTR | Avg Position |
|---|---|---:|---:|---:|---:|
| 1 | / | 2,108 | 12,408 | 16.99% | 4.8 |
| 2 | /audit | 1,840 | 22,408 | 8.21% | 8.4 |
| 3 | /blog/ai-overviews-b2b-saas | 824 | 38,408 | 2.15% | 14.7 |
| 4 | /blog/saas-comparison-pages | 542 | 22,108 | 2.45% | 12.4 |
| 5 | /case-studies/posthog | 388 | 12,408 | 3.13% | 9.7 |
| 6 | /services/technical-audit | 322 | 18,408 | 1.75% | 16.4 |
| 7 | /pricing | 248 | 4,808 | 5.16% | 5.4 |
| 8 | /blog/seo-benchmarks-saas | 224 | 32,408 | 0.69% | 22.4 |
| 9 | /about | 188 | 2,408 | 7.81% | 6.4 |
| 10 | /blog/gsc-vs-ga4-organic | 148 | 18,408 | 0.80% | 28.4 |

## Quick-win opportunities (queries at position 4-10 with high impressions)

| Query | Impressions | Position | Estimated incremental clicks at top-3 |
|---|---:|---:|---:|
| b2b saas seo agency | 9,840 | 8.4 | +~390 |
| best saas seo agency | 6,108 | 12.4 | +~210 (needs more lift) |
| seo agency saas founders | 4,824 | 10.7 | +~165 |
| saas seo benchmark | 7,408 | 13.1 | +~240 (needs more lift) |

> Quick-win detection rule: queries at position 4-10 with impressions ≥ 5,000. Moving to position 1-3 typically lifts CTR from 2-5% to 8-15% in B2B SaaS — that's ~3-4× click volume on the same impression count.

## CTR outliers (clicks higher or lower than expected for position)

**High CTR for position (good — title/meta are working):**
- `anchor seo` at position 1.1 with 43.31% CTR (brand query, expected).
- `/` at position 4.8 with 16.99% CTR (likely strong brand recall + sitelinks).

**Low CTR for position (bad — title/meta need optimisation):**
- `ai search seo` at position 22.8 with 0.67% CTR — page is `/blog/ai-overviews-b2b-saas` but the meta description doesn't match this query intent. Rewrite meta to include "ai search seo" specifically.
- `/blog/seo-benchmarks-saas` at position 22.4 with 0.69% CTR — same pattern. Audit the title tag.

## Suggested follow-ups

1. **Refine title + meta** on the two low-CTR-for-position pages identified above. Re-pull GSC after 2 weeks.
2. **Pull AIO-specific data**: `gsc --ai-overview --dimensions query,page` to see which queries are surfacing AIOs and whether you're cited. This data overlaps with `seo-ai-search-share-of-voice` and `seo-geo` outputs.
3. **Pair with GA4 organic** (`ga4-pages --page /audit`) to see conversion rate per top page — GSC tells you traffic, GA4 tells you outcome.
4. **Run `inspect <url>`** on any page where average position is below 50 — indexation issues may be the explanation.

## Filter examples (re-run with these for narrower analysis)

- Mobile only: `gsc --property sc-domain:anchor-seo.com --device mobile`
- Single URL: `gsc --property sc-domain:anchor-seo.com --page /audit --dimensions query`
- AI Overview-only: `gsc --property sc-domain:anchor-seo.com --ai-overview --dimensions query,page`
- US only: `gsc --property sc-domain:anchor-seo.com --country USA`

## Raw output

When run with `--json`, the underlying CLI returns the GSC Search Analytics API response wrapped in a normalised JSON envelope with the dimensions you queried. This `.md` is the rendered version.

To save raw JSON: `python scripts/gsc_query.py --property sc-domain:anchor-seo.com --days 28 --json > gsc-output.json`. Then feed to `python scripts/google_report.py --type gsc-performance --data gsc-output.json --domain anchor-seo.com --format md` to produce this report.
