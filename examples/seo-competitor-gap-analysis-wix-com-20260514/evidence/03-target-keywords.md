# 03 — Target keywords: wix.com (exclusion set)

Source: `mcp__plugin_seo-skills_se-ranking__DATA_getDomainKeywords`
Inputs: `source=us, domain=wix.com, limit=30, order_field=traffic, filter_position_to=10`
Pulled: 2026-05-18

Returns: keywords for which wix.com already ranks in positions 1–10 in US organic, sorted by traffic descending. This is the "exclusion set" — territory Wix already owns. The gap analysis filter chain subtracts this set from competitor-ranking pools to leave only true gaps.

## Top 30 Wix ranking keywords (positions 1–10, US, by traffic)

| # | Keyword | Volume | KD | Position | Traffic | URL | Intent |
|---|---|---:|---:|---:|---:|---|---|
| 1 | wix | 673,000 | 99 | 1 | 231,840 | wix.com/ | I/N |
| 2 | wix login | 135,000 | 98 | 1 | 40,335 | users.wix.com/signin | I/N |
| 3 | wix website builder | 165,000 | 89 | 1 | 23,701 | wix.com/ | I/N |
| 4 | wix (variant url) | 673,000 | 99 | 1 | 11,208 | users.wix.com/signin | I/N |
| 5 | wix website | 33,100 | 99 | 1 | 9,820 | wix.com/ | I/N |
| 6 | com | 450,000 | 96 | 1 | 6,043 | wix.com/blog/what-is-com-domain | I |
| 7 | website | 301,000 | 99 | 4 | 5,621 | wix.com/ | I |
| 8 | wix (templates) | 673,000 | 99 | 1 | 5,518 | wix.com/website/templates | I/N |
| 9 | small business ideas for | 201,000 | 96 | 1 | 5,163 | wix.com/blog/business-ideas | I |
| 10 | website maker | 27,100 | 100 | 1 | 4,975 | wix.com/ | I |
| 11 | website design | 40,500 | 92 | 1 | 4,772 | wix.com/website/design | L/C |
| 12 | wix login (signup variant) | 135,000 | 98 | 1 | 4,067 | users.wix.com/signin/signup | I/N |
| 13 | wix login (homepage) | 135,000 | 98 | 2 | 3,994 | wix.com/ | I/N |
| 14 | wix web | 12,100 | 99 | 1 | 3,593 | wix.com/ | I/N |
| 15 | com | 450,000 | 96 | 5 | 3,402 | wix.com/blog/what-is-com-domain | I |
| 16 | wix website builder (signin) | 165,000 | 89 | 1 | 3,392 | users.wix.com/signin | I/N |
| 17 | com (org-vs-com variant) | 450,000 | 96 | 1 | 3,311 | wix.com/blog/org-vs-com-vs-net-domain-extensions | I |
| 18 | website maker free | 40,500 | 98 | 2 | 3,208 | wix.com/ | I |
| 19 | wix (AI variant) | 673,000 | 99 | 1 | 3,130 | wix.com/ai-website-builder | I/N |
| 20 | wix.com login | 14,800 | 96 | 1 | 2,970 | users.wix.com/signin | I/N |
| 21 | website (build guide) | 301,000 | 99 | 3 | 2,682 | wix.com/blog/how-to-build-website-from-scratch-guide | I |
| 22 | site free | 14,800 | 100 | 1 | 2,667 | wix.com/ | I |
| 23 | wix studio | 12,100 | 97 | 1 | 2,530 | wix.com/studio | L/N |
| 24 | website builder ai | 12,100 | 94 | 1 | 2,431 | wix.com/ai-website-builder | I |
| 25 | wix customer service | 10,800 | 86 | 1 | 2,424 | support.wix.com | I |
| 26 | wix (plans variant) | 673,000 | 99 | 1 | 2,397 | wix.com/plans | I/N |
| 27 | wix pricing | 8,000 | 74 | 1 | 2,374 | wix.com/plans | I/N |
| 28 | wix templates | 9,900 | 73 | 1 | 2,307 | wix.com/website/templates | I/N |
| 29 | wix login (support) | 135,000 | 98 | 3 | 2,165 | support.wix.com | I/N |
| 30 | com (head variant) | 450,000 | 96 | 4 | 2,114 | wix.com/blog/what-is-com-domain | I |

## Patterns visible in Wix's owned territory

- **Brand dominates** — "wix" + variants drive ~313K of the top-30 traffic alone. Branded SEO is the bedrock.
- **Generic head terms** — Wix ranks #1 for "website maker", "site free", "website maker free", "website design", "website" #4. This is the moat the competitor-gap analysis is trying to extend.
- **AI cluster** — "website builder ai" #1, AI variants of "wix" #1. Wix Studio + AI builder pages are pulling weight.
- **"com" cluster** — 4 variants of "com" / "what is com" rank #1–5 from Wix Blog. Webflow has none of this.

## Composition

The top-30 cap is intentional. The full ranking set is 1,167,806 US keywords (per the worldwide overview) — too large to dump as an exclusion file. Position-≤10 caps to the highest-confidence owned territory; the gap-analysis filter chain expands this dynamically when assessing borderline keywords.

A keyword appearing in BOTH this file AND `02-competitor-keywords-{squarespace,webflow}.md` is filtered OUT of `gaps.csv` — Wix already ranks for it. Keywords that appear in the competitor files but NOT here flow into the gap.
