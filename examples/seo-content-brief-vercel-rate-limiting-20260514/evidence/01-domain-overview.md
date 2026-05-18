# Domain overview — vercel.com

Source: `DATA_getDomainOverviewWorldwide` (SE Ranking, backfilled 2026-05-18). US figures from zone breakdown; worldwide from aggregate.

## Site overview (SE Ranking data — 2026-05-18)

vercel.com is the deployment platform for Next.js.

**SE Ranking organic metrics (2026-05-18):**
| Scope | Organic keywords | Est. monthly traffic | Est. traffic value |
|---|---:|---:|---:|
| Worldwide | 696,691 | 566,304 | $462,646 |
| US only | 89,351 | 57,325 | $134,136 |

Top traffic countries by SE Ranking zone data: IN (178,465 traffic), US (57,325), FR (21,295), DE (20,120), ID (20,970), BR (25,740). US is 4th by traffic but 1st by traffic value ($134K/mo).

- Strong content footprint:
  - `/docs/*` — product documentation
  - `/kb/*` — knowledge-base / troubleshooting
  - `/guides/*` — long-form tutorials (lighter coverage than docs)
  - `/blog/*` — engineering + product announcements
  - `/changelog/*` — frequent product updates

## Top organic queries (SE Ranking US — top traffic drivers)

SE Ranking US data confirms vercel.com ranks #1 for:
- "vercel" (110,000/mo · KD 95 — branded; drives 30,161 traffic/mo)
- "vercel app" (3,600/mo · KD 80)
- "vercel ai" (2,400/mo · KD 77)
- "vercel pricing" (1,900/mo · KD 67)
- "vercel deployment" (480/mo · KD 61)

**Critical gap relevant to this brief:**
- "rate limiting next.js" — Vercel has `/docs/vercel-firewall/vercel-waf/rate-limiting` (commercial-intent, narrow scope) and 3 `/kb/*` articles. **No `/guides/*` entry.** SERP top-8 for the informational query is dominated by third-party publishers (freeCodeCamp, LogRocket, James Perkins, Medium, ByteByteGo). The domain's US keyword footprint of 89,351 keywords confirms strong authority, yet zero rate-limiting editorial content appears in SE Ranking's US data.

## Top countries (SE Ranking data)
IN, US, BR, FR, DE — top 5 by traffic. US ranks #2 and is highest by traffic value ($134K/mo).

## Notes on subdomain structure
- `vercel.com` (main)
- `nextjs.org` (sibling site, not subdomain — same parent company but indexed separately)
- `vercel.app` (deployment URLs — generally noindex'd)

For the rate-limiting brief, the new article should live on the main vercel.com domain (likely `/guides/rate-limiting-strategies-nextjs`) — the nextjs.org domain is for framework docs, not editorial.
