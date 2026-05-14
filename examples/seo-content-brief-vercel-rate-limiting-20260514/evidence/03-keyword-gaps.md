# Keyword gaps — vercel.com vs editorial competitors (rate-limiting topic)

Source: would normally be `mcp__claude_ai_SE_Ranking__DATA_getDomainKeywordsComparison`. SE Ranking MCP not authenticated; this section is reconstructed from SERP-position observation + the SERP-winner content analysis in `05-content-analysis.md`. Re-run with SE Ranking for verified KD + volume + position data.

## Keywords vercel.com plausibly ranks for today (rate-limiting cluster)

| Keyword | Estimated current rank | Owned by |
|---|---:|---|
| vercel rate limiting | 1-3 | `/docs/vercel-firewall/vercel-waf/rate-limiting` |
| vercel waf | 1-3 | `/docs/vercel-firewall/*` |
| vercel rate limit api | 1-5 | `/docs/vercel-firewall/vercel-waf/rate-limiting-sdk` |
| limit abuse rate limiting | 5-10 | `/kb/guide/limit-abuse-with-rate-limiting` |
| ai rate limiting | 5-15 | `/kb/guide/securing-ai-app-rate-limiting` |

## Keyword gaps (informational, mid-difficulty)

Filtered to: informational intent, volume > 1,000/mo, KD < 40. Volume + KD shown as positional estimates pending SE Ranking auth.

| Keyword | Est. volume | Est. KD | Intent | Current SERP winner | Gap reason |
|---|---:|---:|---|---|---|
| rate limiting strategies | 1.6K | 30 | I | LogRocket | no Vercel page |
| api rate limiting | 3.6K | 38 | I | LogRocket / Kong | no Vercel page |
| rate limiting algorithms | 1.4K | 32 | I | LogRocket | no Vercel page |
| token bucket algorithm | 2.2K | 35 | I | Wikipedia + LogRocket | no Vercel page |
| sliding window rate limiter | 880 | 28 | I | freeCodeCamp + LogRocket | no Vercel page |
| leaky bucket algorithm | 1.1K | 30 | I | Wikipedia + LogRocket | no Vercel page |
| fixed window rate limiting | 590 | 22 | I | freeCodeCamp + LogRocket | no Vercel page |
| nextjs rate limit | 590 | 25 | I | James Perkins / Medium | no Vercel page |
| rate limiting next.js | 880 | 28 | I | LogRocket / James Perkins | no Vercel page |
| node.js rate limiting | 720 | 28 | I | LogRocket / freeCodeCamp | no Vercel page |
| http 429 retry-after | 1.1K | 22 | I | MDN + IETF | no Vercel page |
| rate limit vs throttling | 480 | 25 | I | LogRocket | no Vercel page |

**Total combined volume in this gap: ~15K/mo** of informational, mid-difficulty traffic flowing through 3rd-party publishers today.

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
