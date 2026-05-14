# AIO context — "api rate limiting strategies"

Source: `mcp__firecrawl-mcp__firecrawl_search` for the target keyword + manual SERP analysis. The skill normally pulls AIO directly via `DATA_getAiOverview` / `DATA_getAiOverviewLeaderboard` — those endpoints are unavailable in this run (SE Ranking MCP not authenticated). Re-run with auth for actual AIO citation graph.

## AIO presence (inferred from SERP shape)

The target keyword "api rate limiting strategies" returns:
- 7 educational publishers in organic top-8 (Medium, Kong, ByteByteGo, Gravitee, API7, OneUptime, Moesif).
- 1 community result (Reddit).
- All entries are explainer / strategies-enumeration format.
- **All entries published 2024-01 or later** (most 2025+).

This is a strong AIO-trigger shape: high-volume educational query, multiple competing authoritative sources, recent content, vendor-agnostic phrasing. **AIO likely fires for this query.** Re-run with SE Ranking auth to confirm via `DATA_getAiOverview`.

## Likely AIO citation patterns (from SERP shape)

Based on what LLMs typically cite for this shape:

1. **Recency-weighted.** Sources published 2024+ are heavily favoured. Stripe's 2017-dated article fails this filter.
2. **Coverage-breadth-weighted.** Sources covering 4+ algorithms outrank sources covering 1-2 algorithms. Stripe covers 1 algorithm (token bucket) in depth + 2 strategies (concurrent, load shedder).
3. **Vendor-neutrality bonus.** API7 / Moesif / ByteByteGo are independent or near-independent voices. Stripe is more vendor-shaped (uses Stripe's product context) but doesn't sell rate limiting as a product, so the bias risk is low.

## Candidate URL citation status

Cannot be measured without SE Ranking auth. Known facts:
- The Stripe article is **not in the organic top 8** for "api rate limiting strategies guide" — meaning it's not the visible default source for this query.
- The article **is** in the organic top 1 for "stripe rate limiters" (brand+topic query) — its brand-prefixed traffic is intact.
- Likely citation status in AIO: **low**. LLMs that scrape SERP-by-keyword would likely cite the 2024+ educational sources first.
- Likely citation status when the prompt is **"how does Stripe handle rate limiting?"**: high — the article is canonical for that prompt because it's first-party Stripe content.

## Topic clusters this URL plausibly captures

- "rate limiter vs load shedder" — niche distinction; Stripe is one of the strongest sources.
- "concurrent request limiter" — most explainer articles don't cover this; Stripe is one of the strongest sources.
- "rate limiter production tuning" — Stripe's "Hook into middleware safely" / "Build in safeguards" / "Dark launch" guidance is unique.
- "API rate limiting at scale" — the body word "at scale" is in the article but Stripe loses to competitors on raw breadth.

## Recommendations grounded in the AIO context

- **Refresh the article (do not retire it).** The unique-distinction content (load shedder, war stories, production telemetry) is genuinely valuable and not replicated elsewhere. Pure retirement would lose value.
- **Expand to match SERP-winner coverage.** Sliding window + leaky bucket + fixed window + comparison table — 4 specific additions identified in `05-aio-winner-comparison.md`.
- **Surface the freshness signal.** Add `dateModified` + visible review date; this alone may move the article back into the organic top 10 within 4-6 weeks of refresh.
- **Earn the long-tail.** Even if the article doesn't rank #1 for "api rate limiting strategies", it can rank #1 for "rate limiter vs load shedder", "stripe rate limiting", "concurrent request rate limiter" — all higher-intent prompts where Stripe's distinction wins.
