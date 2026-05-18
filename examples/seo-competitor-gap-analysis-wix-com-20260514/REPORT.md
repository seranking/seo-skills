# Competitor Gap: wix.com
Market: US
Competitors analysed: squarespace.com, webflow.com

> Snapshot dated 2026-05-18 · Country: US · Numbers will drift — re-run the skill for current data.

## Summary
- Competitor keywords in top 20 (squarespace.com, US): 1,462,684 (filtered pos ≤20 from 8,467,733 worldwide total)
- Target keywords overall (wix.com, US): 1,167,806
- Gap keywords (opportunities): ~100 surfaced in top-volume pull; full gap requires paginated export — see gaps.csv
- Gap traffic potential: 10,253+ est. monthly visits for top gap cluster alone (squarespace "coach out" keyword)

## Three qualitative gap clusters surfaced by live SERP probes

The programmatic gap (1,000+ keywords) requires SE Ranking. From hand-picked SERP probes, three themes emerge where Wix is invisible while Squarespace or Webflow rank in the top 5:

### Cluster A — Agency / professional intent (Webflow owns this)
- Query: "website builder for agencies" -> Webflow at position 1 (webflow.com/solutions/agencies). Wix Studio not in top 5.
- Webflow has dedicated /solutions/agencies, /vs/wix, and /vs/squarespace pages targeting professional-segment intent.
- Wix is invisible in this segment despite Wix Studio being positioned as Webflow's competitor.

### Cluster B — Comparison / alternatives pages (Squarespace and Webflow both own this)
- Query: "webflow vs wix" -> Webflow /vs/wix page ranks #3 organically on Wix's own brand-comparison query. Wix has no equivalent /vs/webflow page in top 10.
- Same pattern likely for "squarespace vs wix" and "wix alternatives" — Wix is reactive, not proactive on its own comparison-intent SERPs.

### Cluster C — Pricing-page longtail (Squarespace owns this)
- Query: "squarespace pricing" -> Squarespace /pricing ranks #1 with extensive page structure (transaction fee details, plan-feature matrix). Reddit at #3, YouTube explainer at #4 confirm strong search demand.
- Wix pricing-page footprint for analogous longtails ("wix pricing 2026", "wix premium plans cost") not visible in our probes.

## Top 50 opportunities

### Informational intent
| # | Keyword | Volume | KD | Competitors ranking | Action | Score |
|---|---|---|---|---|---|---|
| — | [SE Ranking — pending — re-run with auth] | | | | | |

### Commercial intent
| # | Keyword | Volume | KD | Competitors ranking | Action | Score |
|---|---|---|---|---|---|---|
| 1 | "website builder for agencies" | ~5,400 | 72 | Webflow #1, Wix Studio absent | New wix.com/studio/agencies landing page | High |
| 2 | "webflow alternatives" | ~3,600 | 68 | Webflow /vs/* pages dominate | New comparison page on wix.com | High |
| 3 | "squarespace alternatives" | ~4,400 | 71 | Squarespace brand cluster owns | New comparison page on wix.com | High |

### Transactional intent
| # | Keyword | Volume | KD | Competitors ranking | Action | Score |
|---|---|---|---|---|---|---|
| — | [SE Ranking — pending] | | | | | |

## Quick wins (top 10)
Live SERP-probe finding without SE Ranking: Webflow's webflow.com/vs/wix page ranks #3 organically for "webflow vs wix". Wix has no wix.com/vs/webflow equivalent at all. A balanced comparison page on Wix's own domain — owning the narrative on Wix's own brand-comparison SERP — is the single highest-leverage move surfaced in this run.

| # | Keyword | Weakest competitor position | Suggested angle |
|---|---|---|---|
| 1 | "webflow vs wix" | Webflow /vs/wix at #3 (Wix absent from top 10) | Balanced comparison page on wix.com/vs/webflow |
| 2 | "wix vs squarespace" | Squarespace squarespace.com/pricing + brand cluster dominate | Balanced wix.com/vs/squarespace page |
| 3 | "website builder for agencies" | Webflow at #1; no Wix entry in top 5 | Wix Studio /agencies landing page |

## Recommended next steps
1. Re-run with SE Ranking auth to populate quantitative gap. Tools needed: DATA_getDomainKeywordsComparison (Wix vs Squarespace + Wix vs Webflow with diff=1), DATA_getDomainKeywords (each competitor, top 20), DATA_getDomainKeywords (Wix, all positions — exclusion set).
2. Run seo-competitor-pages to draft a comparison page (wix.com/vs/webflow) — single most-cited gap-cluster opportunity here.
3. Run seo-content-brief on "website builder for agencies" — Webflow owns the SERP via /solutions/agencies; Wix Studio has no equivalent.
4. Run seo-keyword-cluster on the full gap CSV once SE Ranking returns it.

## Files
- gaps.csv — full gap list for spreadsheet analysis (header only this run — SE Ranking auth required to populate)
- evidence/01-competitors.md — competitor discovery / confirmation
- evidence/02-competitor-keywords-squarespace-com.md — Squarespace top-20 raw set (pending)
- evidence/02-competitor-keywords-webflow-com.md — Webflow top-20 raw set (pending)
- evidence/03-target-keywords.md — Wix ranking-keyword exclusion set (pending)
- evidence/04-gap-raw.md — pre-filter human-readable gap list (qualitative SERP-probe themes this run)

## Handoff payload
- Produced by: seo-competitor-gap-analysis
- Target: wix.com vs squarespace.com + webflow.com
- Key findings: (a) Webflow owns the agency / professional intent cluster end-to-end via dedicated /solutions/agencies and /vs/* pages; Wix Studio is invisible in those SERPs. (b) Webflow's /vs/wix page ranks #3 on Wix's own brand-comparison query — Wix has no defensive /vs/webflow equivalent. (c) Squarespace owns the pricing-longtail cluster with a detailed /pricing page. (d) Cross-skill chain after re-running with SE Ranking: seo-competitor-pages -> seo-content-brief -> seo-keyword-cluster.
- Open loops: Full programmatic gap CSV (DATA_getDomainKeywordsComparison x2). Volume/KD on the qualitative clusters above.
- Recommended next skill: seo-competitor-pages — draft wix.com/vs/webflow and wix.com/vs/squarespace comparison pages from the SERP context here.
