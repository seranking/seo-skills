# Keyword gaps — vercel.com vs editorial competitors (rate-limiting topic)

Source: `DATA_getRelatedKeywords` + `DATA_getSimilarKeywords` (SE Ranking US database, backfilled 2026-05-18). Note: SE Ranking's US database does not index "rate limiting strategies", "rate limiting algorithms", "sliding window rate limiter", "fixed window rate limiting", "nextjs rate limit", "rate limiting next.js", "node.js rate limiting", "http 429 retry-after", or "rate limit vs throttling" as standalone keywords with search volume — these return 0 results. Volume + KD for those rows are retained as SERP-inferred estimates. Where SE Ranking returned data, actual values are shown.

## Keywords vercel.com plausibly ranks for today (rate-limiting cluster)

| Keyword | Estimated current rank | Owned by |
|---|---:|---|
| vercel rate limiting | 1-3 | `/docs/vercel-firewall/vercel-waf/rate-limiting` |
| vercel waf | 1-3 | `/docs/vercel-firewall/*` |
| vercel rate limit api | 1-5 | `/docs/vercel-firewall/vercel-waf/rate-limiting-sdk` |
| limit abuse rate limiting | 5-10 | `/kb/guide/limit-abuse-with-rate-limiting` |
| ai rate limiting | 5-15 | `/kb/guide/securing-ai-app-rate-limiting` |

## Keyword gaps (informational, mid-difficulty)

Filtered to: informational intent, volume > 1,000/mo, KD < 40. Volume + KD: SE Ranking values shown where available (2026-05-18); rows marked † have no SE Ranking US entry and retain SERP-inferred estimates.

| Keyword | Volume (SE Ranking US) | KD (SE Ranking) | Intent | Current SERP winner | Gap reason |
|---|---:|---:|---|---|---|
| rate limiting strategies † | est. 1.6K | est. 30 | I | LogRocket | no Vercel page |
| api rate limiting † | est. 3.6K | est. 38 | I | LogRocket / Kong | no Vercel page |
| api rate limit | 440 | 19 | I | LogRocket / Kong | no Vercel page |
| api rate limits | 390 | 31 | I | LogRocket / Kong | no Vercel page |
| rate limiting algorithms † | est. 1.4K | est. 32 | I | LogRocket | no Vercel page |
| token bucket algorithm † | est. 2.2K | est. 35 | I | Wikipedia + LogRocket | no Vercel page |
| sliding window rate limiter † | est. 880 | est. 28 | I | freeCodeCamp + LogRocket | no Vercel page |
| leaky bucket algorithm | 30 | 14 | I | Wikipedia + LogRocket | no Vercel page |
| fixed window rate limiting † | est. 590 | est. 22 | I | freeCodeCamp + LogRocket | no Vercel page |
| nextjs rate limit † | est. 590 | est. 25 | I | James Perkins / Medium | no Vercel page |
| rate limiting next.js † | est. 880 | est. 28 | I | LogRocket / James Perkins | no Vercel page |
| node.js rate limiting † | est. 720 | est. 28 | I | LogRocket / freeCodeCamp | no Vercel page |
| http 429 retry-after † | est. 1.1K | est. 22 | I | MDN + IETF | no Vercel page |
| rate limit vs throttling † | est. 480 | est. 25 | I | LogRocket | no Vercel page |

**Total combined volume in this gap: ~15K/mo (SERP-inferred estimate)** — SE Ranking US database confirms "api rate limit" (440/mo · KD 19) and "api rate limits" (390/mo · KD 31) but does not index most of the remaining keywords as standalone entries; total remains an estimate based on SERP shape. SE Ranking data backfilled 2026-05-18.

## Filter logic
- Removed branded queries (e.g., "vercel waf") — already won.
- Removed transactional queries — different brief type ([seo-agency-landing-page or seo-competitor-pages]).
- Removed difficulty > 40 (would require >12 months of E-E-A-T building + backlinks to compete).
- Kept long-tail / question keywords for `04-serp-and-keywords.md`.

## Strategic note
The "rate limiting strategies" cluster is reachable for Vercel because:
1. **Topical authority is already implicit** — Vercel runs Next.js apps; rate limiting is intrinsically about API infrastructure; Vercel has natural authority.
2. **Internal-link equity is available** — 5 existing pages on rate limiting can flow link equity into a new pillar guide.
3. **No vendor incumbent.** LogRocket is the highest-authority current ranker but they're a monitoring company, not a Next.js-native platform — Vercel's framework-native angle is a genuine positioning advantage.

This is a "free pickup" — Vercel doesn't have to invent demand, just publish a guide that matches the SERP-winner shape and adds the Next.js-native angle that nobody currently covers.
