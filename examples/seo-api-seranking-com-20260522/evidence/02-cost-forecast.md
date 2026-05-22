# Cost forecast — 2026-05-22

| Step | Tool | Endpoint | Billing model | Cost |
|------|------|----------|---------------|------|
| 1 | `DATA_getSubscription` | `GET /v1/account/subscription` | free | 0 |
| 2 | `DATA_getDomainOverviewWorldwide` | `GET /v1/domain/overview/worldwide` | per request | 100 |
| 3 | `DATA_getDomainCompetitors` | `GET /v1/domain/competitors` | per request | 100 |
| 4 | `DATA_getBacklinksSummary` | `POST /v1/backlinks/summary` | per target | 100 |

**Total: 300 credits per run.**

Costs verified against `seranking.com/api/data/domain-analysis` (overview/worldwide and competitors both state "Cost: 100 credits per request") and `…/backlinks` (summary states "Cost: 100 credits per target"). All three are **flat per-request / per-target — not per-record** — so the 300-credit figure is fixed regardless of how many competitor rows or backlinks come back.

Plan-limit consumption: none — read-only Data API only.

## Why the live counter cannot confirm this number

A before/after diff of the credit counter did **not** confirm the 300-credit spend. Between two reads of `DATA_getCreditBalance` during this run, `used` moved **−1,300** (it went *down*) and `getSubscription.units_left` moved **+1,300** (it went *up*) — credits were refunded/reconciled by something other than this workflow.

The SE Ranking API key is **account-global**. Any concurrent consumer — other scripts, the SE Ranking platform UI, other team members on the same key — moves the same counter. On a shared key you cannot isolate one workflow's spend by diffing.

**Forecast from documented per-endpoint costs** (as above); do not rely on counter diffs. If precise per-job accounting matters, mint a **dedicated API key per workload** from the API Dashboard.
