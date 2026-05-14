# Internal linking plan — vercel.com (rate-limiting cluster)

Source: `mcp__firecrawl-mcp__firecrawl_search` on `site:vercel.com "rate limit"` (2026-05-14). The skill normally also pulls `DATA_getDomainKeywords` filtered to the target domain — SE Ranking unauthenticated, so the existing-page inventory below is sourced from Firecrawl search only.

## Existing Vercel pages on rate limiting

| URL | Title | Type | Authority on topic |
|---|---|---|---|
| vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting | WAF Rate Limiting | Product docs | High — canonical for WAF-level config |
| vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting-sdk | Rate Limiting SDK | Product docs | High — canonical for the SDK |
| vercel.com/kb/guide/add-rate-limiting-vercel | Add Rate Limiting with Vercel | KB tutorial | Medium |
| vercel.com/kb/guide/securing-ai-app-rate-limiting | Securing your AI applications with Rate Limiting | KB tutorial | Medium |
| vercel.com/kb/guide/limit-abuse-with-rate-limiting | Limit Abuse with Rate Limiting | KB tutorial | Medium |

**5 existing pages.** All are commercial-intent (product docs / how-to tutorials). **Zero informational/editorial coverage** of the algorithms, theory, or framework-native patterns. This is the gap the brief fills.

## Cross-link plan

### Into the new pillar (link FROM existing pages)

| From | Anchor (suggested) | Where it lands in the new brief |
|---|---|---|
| /docs/vercel-firewall/vercel-waf/rate-limiting | "code-level rate limiting strategies" | H2: Implementing rate limiting in Next.js → H3: Vercel WAF rate limiting (subsection) |
| /docs/vercel-firewall/vercel-waf/rate-limiting-sdk | "rate limiting algorithms comparison" | H2: The 5 algorithms |
| /kb/guide/add-rate-limiting-vercel | "deep-dive on rate limiting strategies" | top of guide |
| /kb/guide/securing-ai-app-rate-limiting | "general rate limiting strategies" | H2: Identifier strategy (relevant because AI APIs are token-budget-shaped) |
| /kb/guide/limit-abuse-with-rate-limiting | "algorithm comparison" | H2: The 5 algorithms |

Pattern: each existing page gets one "deep dive" link with semantically meaningful anchor text. The existing pages remain commercial-intent (their job is to convert); the new pillar absorbs informational intent and hands warm leads back to the docs.

### Out of the new pillar (link TO existing pages)

| To | Anchor (suggested) | Where it sits in the brief |
|---|---|---|
| /docs/vercel-firewall/vercel-waf/rate-limiting | "Vercel WAF rate limiting" | H2: Implementing in Next.js → H3: Vercel WAF |
| /docs/vercel-firewall/vercel-waf/rate-limiting-sdk | "Rate Limiting SDK" | H2: Implementing in Next.js → H3: Vercel WAF |
| /docs/edge-middleware | "Edge Middleware" | H2: Implementing in Next.js → H3: Middleware pattern |
| /docs/functions | "Functions (serverless)" | H2: Choosing a state store (cold start discussion) |
| /docs/storage/vercel-kv | "Vercel KV" | H2: Choosing a state store |
| /docs/observability | "Vercel observability" | H2: Testing your rate limiter |

### Anchor-text concentration check

Per `seo-keyword-cluster` step 7's anchor-diversity rule (no single anchor used >40% of internal links), the suggested anchors above are deliberately varied. No anchor is repeated within or across the inbound/outbound link sets.

## Topical adjacency

Pages that DON'T currently mention rate limiting but should — for natural cross-link opportunities once the pillar is live:

| URL | Why it should link to the new pillar |
|---|---|
| /docs/functions | Functions cold-start handling is rate-limit-adjacent (cold starts make in-memory rate limiters wrong) |
| /docs/edge-middleware | Middleware is the recommended insertion point for rate limiting |
| /docs/observability/runtime-logs | Rate-limit hit observability lives here |
| /docs/storage/vercel-kv | KV is a state-store option for rate limiting |
| /blog/*next.js-15-api-routes* (any post about API routes) | Cross-link the rate-limit guide for "before you ship to prod" guidance |
| /blog/edge-middleware (any post about Edge Middleware) | Same |

These are post-publish opportunities — once the pillar exists, file PRs or doc-update tickets to add cross-links from the topical-adjacency set.

## Summary

The internal-link plan is healthy:
- 5 existing pages can flow link equity inward.
- 6+ existing pages can receive outbound links from the new pillar.
- No anchor text concentration risk.
- The pillar earns its keep by absorbing the entire informational-intent layer of the rate-limiting topic and feeding warm leads back into the commercial-intent pages.
