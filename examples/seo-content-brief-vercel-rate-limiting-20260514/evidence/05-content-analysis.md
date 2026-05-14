# Top-3 winners — content analysis

Source: `mcp__firecrawl-mcp__firecrawl_scrape` on each of the 3 SERP winners. 2026-05-14.

## Winner 1 — freecodecamp.org/news/how-to-build-an-in-memory-rate-limiter-in-nextjs/

| Signal | Value |
|---|---|
| Published | 2026-01-09 |
| Modified | 2026-01-09 (same as published) |
| Word count | ~3,500 |
| Author | Orim Dominic Adah (named, with author archive page) |
| Title | "How to Build an In-Memory Rate Limiter in Next.js" |
| Meta description | 200+ chars (truncated) |
| og:image | 1920×1080 PNG |
| og:type | article |
| JSON-LD | (inferred from `article:*` OpenGraph meta — present) |
| Code blocks | 12+ (TypeScript, YAML for Artillery config) |
| Algorithms covered | 3 (Fixed Window, Sliding Window, Token Bucket) |
| Implementation focus | In-memory only — explicitly states it doesn't address scale-out |
| Load testing | Yes — Artillery setup walked through |

### H-spine
Benefits → How rate limiters work → 3 algorithms (Fixed Window, Sliding Window, Token Bucket) → Build in-memory limiter (TS code) → Front-end test UI → Artillery load test → Conclusion.

### Gaps Vercel's brief should cover
Only 3 algorithms (no Sliding Logs, no Leaky Bucket); in-memory only — no Redis recipe shown; no Edge Middleware vs Route Handler discussion; pages-router based; no comparison table.

## Winner 2 — blog.logrocket.com/rate-limiting-node-js/

| Signal | Value |
|---|---|
| Published | 2024-01-02 |
| Modified | 2024-06-04 (editor's note: "updated on 2 January 2024") |
| Word count | ~4,500 |
| Author | Philip Obosi (named, with bio link) |
| Title | "Understanding and implementing rate limiting in Node.js - LogRocket Blog" (70 chars) |
| Meta description | 137 chars |
| og:image | 895×597 PNG |
| og:type | article |
| JSON-LD | Article schema present |
| Code blocks | 15+ (JavaScript) |
| Algorithms covered | 5 — Fixed Window Counter, Sliding Logs, Sliding Window Counter, Token Bucket, Leaky Bucket |
| Implementation | Express Rate Limit (npm package) + custom Redis/Moment implementation + rate-limiter-flexible |
| Load testing | No |

### H-spine
What is rate limiting (+ throttle vs limit) → 5 algorithms with pros/cons (Fixed Window Counter, Sliding Logs, Sliding Window Counter, Token Bucket, Leaky Bucket) → How to implement in Node.js → Which algorithm is best → Sample project (Express Rate Limit + custom Redis/Moment + rate-limiter-flexible) → Managing global-rate-limit errors → Testing → Conclusion.

### Gaps Vercel's brief should cover
Node.js / Express-only — zero Next.js content; no Edge Middleware mention; no comparison table (pros/cons in prose); state store assumed self-hosted Redis (no Upstash / Vercel KV); X-RateLimit-* headers only (no IETF RateLimit-* draft); 2.3 years old with moment.js patterns now outdated.

## Winner 3 — jamesperkins.dev/post/rate-limiting-nextjs/

| Signal | Value |
|---|---|
| Published | 2025-08-05 |
| Modified | (not declared) |
| Word count | ~800 |
| Author | James Perkins (Unkey CEO — declared at end) |
| Title | "Rate limiting in Next.js in under 10 minutes — James Perkins" |
| Meta description | "Ratelimiting with Unkey is easy" (30 chars — short) |
| og:image | 1200×630 |
| og:type | article |
| Code blocks | 8 (TypeScript, mostly tRPC routes) |
| Algorithms covered | 0 — assumes Unkey handles it |
| Implementation | Unkey + Clerk + tRPC + t3-stack |

### H-spine
What is Unkey → Setting up ENV → Using Clerk for auth → Creating rate limiter → Implementing in protected route → Completed code → Testing → Conclusion.

### Why this ranks (despite being thin) — and why Vercel's brief outclasses it
Recency (Aug-2025), stack-specific (t3 + Clerk + tRPC + Unkey), author personal brand. But: vendor-pitch shape narrows the audience; covers zero algorithms; doesn't address WAF-level rate limiting (Unkey is API-key-level only). Vercel's brief is vendor-neutral on theory + Vercel-native on implementation.

## Synthesis — what Vercel's brief must include

**Parity (must have):** 5 algorithms (Fixed Window, Sliding Logs, Sliding Window Counter, Token Bucket, Leaky Bucket — LogRocket sets this bar); pros/cons per algorithm; named author with bio; Article schema with datePublished + dateModified; 10+ inline code blocks; load-testing section (freeCodeCamp differentiator).

**Differentiators (Vercel-unique):** Next.js Edge Middleware code, Vercel-native state stores (Upstash, Vercel KV), Vercel WAF rate limiting cross-reference (platform-level alternative competitors can't credibly cite), IETF `RateLimit-*` draft headers (recency signal), comparison table (5 × 6 matrix — no SERP winner has one).
