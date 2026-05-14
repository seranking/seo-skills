# Domain overview — vercel.com

Source: would normally be `mcp__claude_ai_SE_Ranking__DATA_getDomainOverviewWorldwide` + `DATA_getDomainKeywords`. SE Ranking MCP not authenticated in this run, so this section is reconstructed from publicly-known signals + Firecrawl-scraped index pages. Re-run with SE Ranking authenticated for actual traffic / keyword counts.

## Site overview (positional estimate)

vercel.com is the deployment platform for Next.js. Public signals:
- Deploys ~1M+ teams (Vercel public stats)
- Documentation at vercel.com/docs is the canonical reference for Next.js deployment patterns
- Strong content footprint:
  - `/docs/*` — product documentation
  - `/kb/*` — knowledge-base / troubleshooting
  - `/guides/*` — long-form tutorials (lighter coverage than docs)
  - `/blog/*` — engineering + product announcements
  - `/changelog/*` — frequent product updates
- Organic traffic concentration is heaviest on `/docs/*` (deep-tail technical queries) and `/changelog/*` (release announcements).

## Top organic queries (positional inference — not measured)

Likely owns top-1 for:
- "vercel deploy"
- "vercel next.js"
- "vercel cli"
- "next.js deployment"
- "vercel env vars"

Likely owns top-5 for:
- "vercel functions"
- "vercel edge middleware"
- "next.js api routes"

**Critical gap relevant to this brief:**
- "rate limiting next.js" — Vercel has `/docs/vercel-firewall/vercel-waf/rate-limiting` (commercial-intent, narrow scope) and 3 `/kb/*` articles. **No `/guides/*` entry.** SERP top-8 for the informational query is dominated by third-party publishers (freeCodeCamp, LogRocket, James Perkins, Medium, ByteByteGo).

## Top countries (positional)
US, IN, GB, DE, FR — typical Western developer geography. US is the priority target market.

## Notes on subdomain structure
- `vercel.com` (main)
- `nextjs.org` (sibling site, not subdomain — same parent company but indexed separately)
- `vercel.app` (deployment URLs — generally noindex'd)

For the rate-limiting brief, the new article should live on the main vercel.com domain (likely `/guides/rate-limiting-strategies-nextjs`) — the nextjs.org domain is for framework docs, not editorial.
