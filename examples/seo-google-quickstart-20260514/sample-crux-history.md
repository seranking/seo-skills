# Sample CrUX History — anchor-seo.com (template — what you'll see when you run this)

> **Template** dated 2026-05-14 · URL audited: `https://anchor-seo.com/` (fictional) · This is a **template** showing the shape of `python scripts/crux_history.py <url> --json` output. Google API credentials were not available during example capture — run with a real API key (Tier 0 — free) and your data will fill this shape.

## Snapshot

- URL: https://anchor-seo.com/
- Window: 25 weeks (2025-11-23 to 2026-05-13)
- Strategy: mobile (default for CrUX History — desktop available with `--device desktop`)
- Tier required: 0 (API key only — free)
- Source: CrUX History API (chromeuxreport.googleapis.com)

## Trend overview (per metric)

| Metric | Week 1 p75 | Week 13 p75 | Week 25 p75 | Trend | % change W1→W25 |
|---|---:|---:|---:|---|---:|
| LCP | 2.1s | 2.3s | 2.4s | **Degrading** | +14.3% |
| INP | 168ms | 178ms | 184ms | Stable (slight degradation) | +9.5% |
| CLS | 0.06 | 0.07 | 0.08 | Stable | +33% (in band) |
| FCP | 1.5s | 1.7s | 1.8s | **Degrading** | +20.0% |
| TTFB | 0.48s | 0.58s | 0.62s | **Degrading** | +29.2% |

## Verdict: WATCH

All 5 metrics still rate Good at the current p75 (see `sample-pagespeed.md`), but 3 of 5 are trending degrading over the 25-week window. The story:

- **TTFB +29%** is the most concerning — server response time is the upstream bottleneck. Likely candidate causes: backend load increase as traffic grows, CDN config change, third-party-script load order.
- **FCP +20%** follows TTFB by construction (FCP can't improve while TTFB degrades).
- **LCP +14%** is being dragged up by TTFB and FCP. If the trend continues 3-4 more months, LCP crosses the 2.5s "Good" threshold.

This is a textbook case where a single PSI run says "everything's fine" but the 25-week trend says "monitor closely."

## Weekly p75 series (LCP, mobile)

| Week starting | LCP p75 |
|---|---:|
| 2025-11-23 | 2.1s |
| 2025-11-30 | 2.1s |
| 2025-12-07 | 2.2s |
| 2025-12-14 | 2.1s |
| 2025-12-21 | 2.2s |
| 2025-12-28 | 2.2s |
| 2026-01-04 | 2.2s |
| 2026-01-11 | 2.3s |
| 2026-01-18 | 2.3s |
| 2026-01-25 | 2.2s |
| 2026-02-01 | 2.3s |
| 2026-02-08 | 2.3s |
| 2026-02-15 | 2.3s |
| 2026-02-22 | 2.3s |
| 2026-03-01 | 2.3s |
| 2026-03-08 | 2.3s |
| 2026-03-15 | 2.4s |
| 2026-03-22 | 2.4s |
| 2026-03-29 | 2.4s |
| 2026-04-05 | 2.3s |
| 2026-04-12 | 2.4s |
| 2026-04-19 | 2.4s |
| 2026-04-26 | 2.4s |
| 2026-05-03 | 2.4s |
| 2026-05-10 | 2.4s |

(Similar weekly series available for INP, CLS, FCP, TTFB in the raw JSON.)

## Trend direction algorithm

The script classifies each metric as:

- **Improving** — p75 value decreased by ≥ 10% over the window
- **Degrading** — p75 value increased by ≥ 10%
- **Stable** — change between -10% and +10%

The +14.3% LCP, +20% FCP, and +29% TTFB all cross the Degrading threshold. The +9.5% INP and +33% CLS — note CLS's high percentage is misleading because absolute values are tiny (0.06 → 0.08 is +33% but still well under 0.1 threshold). The script flags both situations.

## Suggested follow-ups

1. **Investigate TTFB regression.** TTFB is the trunk; LCP and FCP improve only if TTFB does. Steps:
   - Check CDN config changes in the 25-week window (Cloudflare / Vercel / Netlify dashboards).
   - Check backend response-time logs.
   - Check third-party-script tag changes (a new analytics tag with `<script>` blocking can add 100ms).
2. **Re-run Lighthouse `pagespeed` after fixing TTFB.** Pair with `crux-history` 4 weeks later to confirm the fix landed in field data.
3. **Add `crux-history` to your `seo-drift` snapshots.** The baseline-vs-current diff in `seo-drift` would catch TTFB regression weeks earlier than waiting for the trend to develop.
4. **For multi-URL CWV monitoring, batch.** This skill is single-URL. For 100+ URLs, run a wrapper script that loops `pagespeed_check.py` over your top traffic pages and aggregates the results into a dashboard.

## Cross-skill integration

- `seo-drift` uses `crux-history` to add 25-week field-data trends to baseline/compare snapshots.
- `seo-technical-audit` uses `pagespeed_check.py` for real CWV field data alongside SE Ranking's audit (which is crawl-based, not field-based).
- The combination of "CWV trending degrading + audit shows new render-blocking script in last release" is high-confidence root-cause analysis.

## Raw JSON

To save: `python scripts/crux_history.py https://anchor-seo.com/ --json > crux-history.json`.

The raw JSON contains 25 weekly buckets per metric, each with `histogram_timeseries` (good / needs-improvement / poor density buckets) and `percentiles_timeseries` (p75 series). The render above is a flattened view.
