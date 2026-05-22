# MCP tool-call sequence — domain intelligence snapshot for seranking.com

Agent-native variant. Run inside any MCP client connected to the SE Ranking
server (`https://api.seranking.com/mcp`). These are the exact calls executed
in this run on 2026-05-22 — every one verified live.

## 1. Preflight (0 credits)

`DATA_getSubscription` — no args.
→ `{ subscription_info: { status, units_limit, units_left, start_date, expiraton_date } }`
Abort if `units_left` < 300.

`DATA_getCreditBalance` — no args. Optional second view.
→ `{ limit, used }`

> **NOTE:** `getCreditBalance` and `getSubscription` are **not** interchangeable.
> They return different shapes, and their numbers do not reconcile — in this run
> `getCreditBalance` (`limit − used`) implied 81.4M credits left while
> `getSubscription.units_left` reported 90.1M, an ~8.6M gap. For cost
> forecasting use `getSubscription.units_left` (the figure the official credit
> docs document).

## 2. Worldwide overview (100 credits)

`DATA_getDomainOverviewWorldwide`
- `domain`: `"seranking.com"`

→ `{ organic: [{ source, keywords_count, traffic_sum, price_sum }], adv: [{ ... }] }`

## 3. Organic competitors, US database (100 credits)

`DATA_getDomainCompetitors`
- `domain`: `"seranking.com"`
- `source`: `"us"`
- `type`: `"organic"`

→ `{ data: [{ domain, common_keywords, total_keywords, missing_keywords, traffic_sum, price_sum, domain_relevance }] }`

> **⚠️ 60KB overflow:** for popular domains this response exceeds the MCP
> client's token limit and is auto-saved to a file rather than returned inline
> (in this run: 371 rows, ~60KB). Recover the data with `jq` on the saved file:
>
> ```bash
> jq -r '.data[:15][] | "\(.domain)\t\(.common_keywords)"' <saved-file.txt>
> ```
>
> This is an MCP-transport limit only — the raw REST endpoint
> `GET /v1/domain/competitors` returns the full JSON with no size cap.

## 4. Backlink profile summary (100 credits)

`DATA_getBacklinksSummary`
- `target`: `"seranking.com"`
- `mode`: `"domain"`  (covers `*.seranking.com` incl. subdomains)

→ `{ summary: [{ backlinks, refdomains, subnets, ips, dofollow_backlinks, nofollow_backlinks, domain_inlink_rank, top_anchors_by_backlinks, top_pages_by_refdomains, top_countries, ... }] }`

## Total

~300 credits — 100 each for steps 2, 3, 4. Steps 1 are free.
Four sequential calls, well inside the 10 RPS Data API limit.
