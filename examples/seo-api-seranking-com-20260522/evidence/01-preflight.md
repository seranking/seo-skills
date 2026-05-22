# Preflight — 2026-05-22

## MCP connectivity

- SE Ranking MCP reachable at `https://api.seranking.com/mcp`. ✓
- Data API tools respond. ✓
- Project API tools respond — `PROJECT_listProjects` returned 22 projects, so this account has Business/Enterprise (Project API) access. ✓ (not needed for this read-only run, but confirms the full surface is live)

## Credit balance

`DATA_getSubscription`:

| Field | Value |
|-------|-------|
| status | active |
| units_limit | 101,323,444 |
| units_left | 90,055,398 |
| expiration | 2027-04-17 |

`DATA_getCreditBalance`:

| Field | Value |
|-------|-------|
| limit | 101,323,444 |
| used | 19,916,982 |

> **⚠️ Discrepancy.** `getCreditBalance` implies `101,323,444 − 19,916,982 = 81,406,462` credits left. `getSubscription` reports `90,055,398`. The two counters do **not** reconcile — an ~8.6M gap — and are not aliases for one another. This run forecasts against `getSubscription.units_left`, which is the figure the official credit-system docs document.

## Verdict

Preflight **PASS**. ~90M credits available; run costs 300. Proceed.
