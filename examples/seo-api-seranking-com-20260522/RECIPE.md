# Domain Intelligence Snapshot: seranking.com

> Run dated 2026-05-22 · Mode: code (read-only Data API calls executed live to populate real figures) · Target market: US · Total cost: 300 credits/run

## Goal

Stand up a recurring (weekly) domain-intelligence snapshot for `seranking.com`: the worldwide organic + paid search footprint, the top organic competitors, and the backlink-profile summary — merged into one JSON document a dashboard or warehouse can ingest. Read-only Data API only; no account state is created or modified.

## API surface map

| Step | MCP tool | REST endpoint | Verb | Cost |
|------|----------|---------------|------|------|
| 1 | `DATA_getSubscription` | `/v1/account/subscription` | GET | 0 credits |
| 2 | `DATA_getDomainOverviewWorldwide` | `/v1/domain/overview/worldwide` | GET | 100 credits |
| 3 | `DATA_getDomainCompetitors` | `/v1/domain/competitors` | GET | 100 credits |
| 4 | `DATA_getBacklinksSummary` | `/v1/backlinks/summary` | POST | 100 credits |

All four are Data API, read-only. No Project API, no plan-limit consumption. A single SE Ranking API key authorises every call.

## Auth & setup

```bash
export SERANKING_API_KEY="<your-uuid-key>"   # from https://online.seranking.com/admin.api.dashboard.html
```

REST auth is the `Authorization` header with the `Token` scheme (not `Bearer`):

```
Authorization: Token <SERANKING_API_KEY>
```

See `../../skills/seo-api/references/auth-and-keys.md` for OAuth vs. header tradeoffs and headless/CI patterns.

## Cost forecast

- Credit cost: **300 credits/run** — 100 each for overview, competitors, backlinks summary. All three are flat per-request/per-target, verified against `seranking.com/api/data/domain-analysis` and `…/backlinks`.
- Plan-limit consumption: none (read-only Data API).
- Balance at run time: 90,055,398 credits left — ~300k runs of headroom.
- A full weekly cadence costs ~15,600 credits/year. Negligible against any paid plan.

See `evidence/02-cost-forecast.md` for the note on why a before/after counter diff cannot confirm the 300-credit figure on a shared API key.

## Recipe

Four equivalent implementations of the same workflow. Pick the one that fits your stack.

- **`code/curl.sh`** — bash + curl, writes one JSON file per endpoint. Smallest dependency footprint; good for cron.
- **`code/python.py`** — `requests`-based, with 429 backoff + terminal-403 handling, merges everything into one snapshot JSON.
- **`code/typescript.ts`** — Node 20+ native `fetch`, same merge logic, typed.
- **`code/mcp-calls.md`** — the agent-native MCP tool-call sequence, for when this snapshot runs inside a Claude / Cursor / Codex workflow rather than as standalone code.

All four pace sequentially — four calls, well inside the 10 RPS Data API limit.

## What this returns (observed 2026-05-22)

**Worldwide overview** — `seranking.com`:

| Channel | Keywords | Est. monthly traffic | Est. traffic value |
|---------|----------|----------------------|--------------------|
| Organic | 946,465 | 625,206 | $621,762 |
| Paid    | 3,717   | 2,616   | $2,182 |

**Top organic competitors** (US database, 371 returned, by shared keywords):

| Competitor | Common keywords | Their total keywords | Est. traffic |
|------------|-----------------|----------------------|--------------|
| seoreviewtools.com | 26,727 | 41,468 | 64,299 |
| seomator.com | 23,266 | 38,451 | 14,751 |
| seobility.net | 22,605 | 46,090 | 96,285 |
| thehoth.com | 22,097 | 39,488 | 34,145 |
| mangools.com | 20,665 | 40,401 | 33,887 |
| serpstat.com | 19,614 | 42,023 | 15,886 |
| spyfu.com | 17,418 | 35,445 | 45,069 |

**Backlink profile summary** — `seranking.com` (domain mode):

| Metric | Value |
|--------|-------|
| Total backlinks | 508,045 |
| Referring domains | 21,735 |
| Referring subnets / IPs | 7,734 / 15,506 |
| Dofollow / nofollow | 445,894 / 62,151 |
| .edu / .gov backlinks | 682 / 102 |
| Domain Trust (`domain_inlink_rank`) | 90 |

## Rate limit & retry strategy

- Data API: 10 RPS per key. This workflow is 4 sequential calls — no pacing needed.
- 429: exponential backoff with jitter (1s → 2s → 4s → 8s, ±20%). Implemented in `code/python.py` and `code/typescript.ts`.
- 403 `Insufficient funds`: terminal — do not retry; top up credits.
- See `../../skills/seo-api/references/rate-limits-and-credits.md` for the reusable client wrapper.

## What you still need to do

- Schedule `code/python.py` (or `curl.sh`) weekly — e.g. cron `0 6 * * 1` (Mondays 06:00).
- Point the snapshot output at your warehouse / dashboard sink (BigQuery insert, S3 put, etc. — left as a one-line swap in `main()`).
- The competitors call returns up to 500 rows; the recipe keeps the top 15. Widen the slice if you want the full set.

## Linked docs

- Domain Analysis API — <https://seranking.com/api/data/domain-analysis/>
- Backlinks API — <https://seranking.com/api/data/backlinks/>
- Credit system — <https://seranking.com/api/data/getting-started/#unit-costs>

## When to escalate to another skill

- `seo-competitor-gap-analysis` — the competitor list above is the input for a full keyword-gap analysis.
- `seo-backlinks-profile` — turns the backlink summary into a full profile audit (anchor distribution, toxic-candidate flagging — note the spammy Telegram anchors already visible in the raw data).
- `seo-drift baseline` — to track this snapshot over time and detect regressions, baseline the domain instead of just snapshotting it.
