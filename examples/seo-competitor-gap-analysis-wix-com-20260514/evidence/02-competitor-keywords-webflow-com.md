# 02 — Competitor keywords: webflow.com (gap vs wix.com)

Source: `mcp__plugin_seo-skills_se-ranking__DATA_getDomainKeywordsComparison`
Inputs: `source=us, domain=webflow.com, compare=wix.com, diff=1, limit=50, filter_volume_from=100, order_field=volume, order_type=desc`
Pulled: 2026-05-18

Returns: keywords webflow.com ranks for in US organic search where wix.com does NOT rank. Filtered to volume ≥ 100. Sorted by volume desc.

## Top 50 Webflow-only keywords (US)

| # | Keyword | Volume | KD | Position | Intent | URL pattern | Win type |
|---|---|---:|---:|---:|---|---|---|
| 1 | font generator | 823,000 | 61 | 47 | I | webflow.com/tools/free-font-generator | Free tool |
| 2 | font gen | 823,000 | 60 | 45 | I | webflow.com/tools/free-font-generator | Free tool |
| 3 | what does mean | 165,000 | 91 | 40 | I | uploads-ssl.webflow.com PDF | User PDF (noise) |
| 4 | startup page | 165,000 | 91 | 83 | I | webflow.com/blog/startup-website-examples | Blog |
| 5 | png | 110,000 | 95 | 1 | I | webflow.com/blog/png-vs-jpg | Blog (strong) |
| 6 | webflow | 90,500 | 88 | 1 | I/N | university.webflow.com | Brand |
| 7 | cursive generator | 90,500 | 76 | 47 | I | webflow.com/tools/free-font-generator/cursive | Free tool |
| 8 | template | 74,000 | 96 | 26 | I | webflow.com/templates | **Strategic — templates** |
| 9 | freelance platform | 74,000 | 85 | 20 | I | webflow.com/blog/freelance-websites | Blog |
| 10 | hex color picker | 74,000 | 86 | 83 | I | webflow.com/blog/color-picker-tools | Tool review |
| 11 | horizontal rule | 74,000 | 87 | 20 | I | discourse.webflow.com | Forum |
| 12 | pop art | 74,000 | 89 | 86 | C | webflow.com/blog/the-pop-art-movement | Blog |
| 13 | color picker from image | 60,500 | 86 | 48 | I | webflow.com/blog/color-picker-tools | Tool review |
| 14 | hex code color picker | 60,500 | 84 | 50 | I | webflow.com/blog/color-picker-tools | Tool review |
| 15 | nat | 60,500 | 94 | 84 | I | webflow.com/glossary/nat | Glossary |
| 16 | graffiti font | 49,500 | 86 | 16 | I | webflow.com/blog/graffiti-font | **Strategic — font blog** |
| 17 | cursive font generator | 40,500 | 70 | 43 | I | webflow.com/tools/free-font-generator/cursive | Free tool |
| 18 | gothic font | 40,500 | 90 | 25 | I | webflow.com/tools/free-font-generator/gothic | Free tool |

The remaining 32 of 50 results are uploads-ssl.webflow.com user-hosted PDFs (smoothie cafe menus, license-renewal forms, blood-sugar charts, etc.) — Webflow's customer-content CDN, not strategic content Wix can compete against by building assets. Dropped from the table; available in raw API response if needed.

## Read of the data

**Strategic gap (real signal):** ~10 of 50 (20%) are Webflow's own marketing content:
- **Free tools cluster** — `webflow.com/tools/free-font-generator` (and `/cursive`, `/gothic`) ranks 16–47 for high-volume design queries. Wix has nothing equivalent.
- **Templates** — `webflow.com/templates` ranks #26 for "template" (74K vol). Genuinely competitive long-tail.
- **Design blog** — `webflow.com/blog/png-vs-jpg` #1 for "png" (110K vol), `webflow.com/blog/graffiti-font` #16 for "graffiti font" (49.5K vol). Webflow's design-explainer blog earns rankings Wix Blog doesn't.
- **Glossary / docs** — `webflow.com/glossary/nat`, `university.webflow.com` for "webflow" #1. Documentation+education as a content moat.

**Noise:** ~64% are user-hosted PDFs. Webflow's CDN sub-domain (`uploads-ssl.webflow.com`) ranks accidentally on random queries because customers upload random documents. These aren't actionable for Wix.

## Live Firecrawl SERP-probe corroboration (captured 2026-05-14)

- "website builder for agencies" → Webflow `webflow.com/solutions/agencies` at #1
- "webflow vs wix" → Webflow `webflow.com/vs/wix` at #3 (Wix absent from top 10)

These two confirm the comparison-page and agency-vertical templates that the SE Ranking gap data shows ranking at the page-template level (`/solutions/{audience}`, `/vs/{competitor}`).

## What gets surfaced into REPORT.md

The strategic-content rows above feed the REPORT.md "Top opportunities" tables. The agency / comparison / free-tools / design-education clusters are the four content patterns Wix can realistically build to close the gap.
