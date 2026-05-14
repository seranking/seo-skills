# Competitors — vercel.com (rate-limiting topic)

Source: would normally be `mcp__claude_ai_SE_Ranking__DATA_getDomainCompetitors`. SE Ranking MCP not authenticated; this section is reconstructed from the SERP top-8 for "rate limiting strategies node.js next.js" + "api rate limiting strategies" — the topical competitor set for this brief, not the full domain-competitor set.

## SERP-set competitors (rate-limiting topic)

| Rank | Domain | Topical role | Authority on rate limiting |
|---:|---|---|---|
| 1 | freecodecamp.org | Free-curriculum publisher | Strong — long-form tutorial, runnable code, load testing |
| 2 | reddit.com | Community Q&A | Strong (long-tail community discussion); not a direct content competitor |
| 3 | blog.logrocket.com | Vendor blog (monitoring) | **Dominant** — 5-algorithm guide, ~4,500 words, regularly updated (last update 2024-06) |
| 4 | youtube.com | Video | Different format; complementary |
| 5 | medium.com | Independent publisher | Variable quality; some posts compete |
| 6 | stackoverflow.com | Community Q&A | Long-tail capture; not a direct content competitor |
| 7 | youtube.com | Video | Different format |
| 8 | jamesperkins.dev | Independent (Unkey CEO) | Strong on lightweight implementation; weak on theory |

## Closest editorial competitors

1. **LogRocket** — biggest single competitor. Their guide is comprehensive (5 algorithms), well-maintained, and earns natural backlinks from "rate limiting node.js" queries. Vercel's new brief must match its breadth AND outclass it on framework-specific code.

2. **freeCodeCamp** — strong long-form competitor with runnable code (GitHub repo + load testing). Recent (2026-01). Vercel can outclass by being Next.js-native (freeCodeCamp uses pages router, generic Node patterns).

3. **API gateway vendors** (Kong, Gravitee, API7) — own the "what is API rate limiting" educational tier. Different angle (gateway-centric) but worth being aware of since they overlap on informational queries.

## Adjacent vendors (state-store / rate-limiting infrastructure)

- **Upstash** — partners with Vercel on the @upstash/ratelimit package. Friendly; cross-link encouraged.
- **Unkey** — competitor; SERP winner #8 is their CEO. Don't link to Unkey from the new guide; instead, point to Upstash + Vercel KV.
- **Cloudflare** — competitor at infrastructure layer (Cloudflare WAF rate limiting). Adjacent, not a content competitor for "next.js rate limiting" specifically.
- **AWS** — Lambda function rate limiting is platform-specific; not the same query intent.

## Positioning angle

Vercel's brief should be:
- **Next.js-native** (not framework-agnostic — that's LogRocket's spot)
- **Edge-first** (not Node.js-server-first — that's LogRocket / freeCodeCamp's spot)
- **Algorithm-comprehensive** (cover all 5 — match LogRocket's breadth)
- **State-store-opinionated** (Upstash > self-hosted Redis on Vercel; Vercel KV when stable enough)
- **WAF-aware** (cross-link to Vercel WAF docs — own the platform-vs-framework distinction)

This positioning maps to a guide that is 3,500-4,500 words, code-heavy, and editorially branded as "the Next.js rate limiting reference" — exactly what is missing from the SERP today.
