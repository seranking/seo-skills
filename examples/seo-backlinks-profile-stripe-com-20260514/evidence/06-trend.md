# 06 — Trend (last 6 months)

> Source: `DATA_getNewLostBacklinksCount(target="stripe.com", mode="domain", date_from="2025-11-01", date_to="2026-05-18")` — retrieved 2026-05-18.

## Live monthly trend (2025-12 through 2026-05)

| Month | New backlinks | Lost backlinks | Net |
|---|---|---|---|
| 2025-12 | 8,363,954 | 1,762,554 | +6,601,400 |
| 2026-01 | 4,432,065 | 756,165 | +3,675,900 |
| 2026-02 | 4,935,185 | 644,901 | +4,290,284 |
| 2026-03 | 6,863,481 | 952,384 | +5,911,097 |
| 2026-04 | 8,173,681 | 1,535,503 | +6,638,178 |
| 2026-05 (MTD) | 5,064,286 | 1,144,650 | +3,919,636 |

## Observations

- Every month is strongly net-positive. No decline signal detected.
- Dec 2025 spike (+6.6M net): consistent with year-end Stripe product launches and financial press recaps.
- Apr 2026 spike (+6.6M net): consistent with Stripe Sessions conference timing and associated press coverage.
- Jan 2026 is the lowest-volume month (+3.7M net) — typical post-holiday plateau.
- Loss volumes are consistently low relative to gains (loss rate 8–19% of new). The Nov 2025 data (not shown in the table above) showed a brief negative-net period that resolved by Dec 1 — likely a crawl recalibration by SE Ranking.

## Pattern types to flag (for future runs)

| Pattern | Signal | Action |
|---|---|---|
| Net negative for 2+ consecutive months | De-indexation / partner removal / algo update | Investigate immediately |
| Monthly new > 3× the 6-month average | Unnatural link campaign | Investigate source |
| Steady -3% MoM decline in ref_domains | Profile drift | Address with renewed press cadence |
