# SEO Plan: wix.com

> Plan dated 2026-05-18 · Horizon: 90 days · Business type: saas (website-builder PLG) · Country: US · Numbers will drift — re-run the skill for current data.

## Inputs ingested

This plan composes three sibling examples in /examples/:
- AI Search share-of-voice (committed prior, real SE Ranking numbers): [../seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md](../seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md)
- Competitor gap analysis vs squarespace + webflow: [../seo-competitor-gap-analysis-wix-com-20260514/REPORT.md](../seo-competitor-gap-analysis-wix-com-20260514/REPORT.md)
- Drift baseline + historical compare: [../seo-drift-wix-com-20260514/compare/DRIFT-REPORT.md](../seo-drift-wix-com-20260514/compare/DRIFT-REPORT.md)

What is NOT yet ingested (per SKILL.md step 4a, would normally be ingested if present): seo-technical-audit, seo-content-audit, seo-backlinks-profile for wix.com. These three become Phase 0 work items below.

## Where you are

(Anchored in the share-of-voice example's competitive frame plus today's Firecrawl capture of wix.com)

- Organic keywords (US): 1,167,806
- Organic traffic estimate (US): 1,417,427 / month
- Domain authority: 100
- Referring domains: 3,356,565
- AI Search share of voice: 36.1% combined across 5 engines, #1 of 5 competitors [SoV-2026-04-27]
- Pillar scores: Technical [pending audit] / Content [pending audit] / Topical 90/100 [SoV-derived, qualitative — Wix dominates 6 of 9 clusters] / AI Search 95/100 [SoV-derived]

## Lead theme

**Defend the AI-Search and topical-authority moats; close the agency / designer gap before Wix Studio's growth window narrows.**

Why this is the constraint (per SKILL.md step 5): Wix's two highest pillar scores are Topical (90) and AI Search (95). Those are the moats that compound. The lowest pillar is the unmeasured one — Technical and Content health are pending audits. So Phase 1 is "measure the unmeasured pillars"; Phase 2 builds the missing competitive surface area (Wix Studio agency cluster); Phase 3 hardens AI Search citation moats while measuring drift.

The Wix gap analysis (sibling example) surfaces the single highest-leverage missing surface: Webflow's webflow.com/vs/wix page ranks #3 organically on Wix's own brand-comparison query, and Wix has no defensive /vs/webflow equivalent at all. This is the load-bearing build for Phase 2.

## Top 5 competitors

| Domain | DA | Organic kw | Top cluster they own |
|---|---|---|---|
| weebly.com | 88 | 28,783,430 (WW, incl. user subdomains) | Free-builder secondary brand (acquired by Square, declining) [SoV] |
| squarespace.com | 97 | 8,467,733 (WW) | Design-led / portfolio / professional templates [SoV] |
| hostinger.com | 96 | 4,179,209 (WW) | Hosting-first; bundled builder is secondary [SoV] |
| webflow.com | 95 | 2,971,221 (WW) | Designer / agency / Wix Studio's direct competition [SoV + gap analysis] |
| (5th slot variable; auto-discover with DATA_getDomainCompetitors) | | | |

## Phase 1 — Foundations (weeks 1–4)

**Goal:** measure the unmeasured pillars. Capture a fresh /seo-drift baseline. Run /seo-technical-audit, /seo-content-audit, /seo-backlinks-profile to populate the Technical / Content / Backlink pillars that are pending today.

| # | Work item | Skill / source | Owner | Effort | Phase-end metric |
|---|---|---|---|---|---|
| 1.1 | Run /seo-technical-audit wix.com | seo-technical-audit | SEO Lead | M | Technical pillar score populated |
| 1.2 | Run /seo-content-audit on top 10 traffic pages | seo-content-audit | Content Lead | L | Content pillar score populated; E-E-A-T verdicts on top 10 |
| 1.3 | Run /seo-backlinks-profile wix.com | seo-backlinks-profile | SEO Lead | M | Backlink profile score; disavow candidate list reviewed |
| 1.4 | Run /seo-drift baseline wix.com (with SE Ranking auth + Google APIs configured) | seo-drift | SEO Lead | S | snapshot.json saved; baselines.json entry created |
| 1.5 | Fix the og:image / twitter:image malformation if confirmed on other Wix subdomains | seo-page (any URL audit) | Eng | S | Social-share preview health green |
| 1.6 | Run /seo-page on the top 3 traffic pages (auto-discover via Phase 1.2 top-10 list) | seo-page | Content Lead | M | KEEP/REFRESH/CONSOLIDATE/KILL verdicts on top 3 |

**Phase exit criteria:** all four pillar scores have a real number. Drift baseline captured. Top-3 page verdicts produced.

## Phase 2 — Build (weeks 5–8)

**Goal:** close the highest-leverage competitive gap surfaced by the sibling gap-analysis example — Wix has no defensive /vs/webflow page. Build it.

| # | Work item | Skill / source | Owner | Effort | Phase-end metric |
|---|---|---|---|---|---|
| 2.1 | Run /seo-competitor-pages wix-vs-webflow | seo-competitor-pages | Content Lead | M | Comparison page draft + feature matrix produced |
| 2.2 | Ship wix.com/vs/webflow (and wix.com/vs/squarespace) | Content + Eng | M | Indexable pages live; structured-data validated |
| 2.3 | Run /seo-content-brief on "website builder for agencies" | seo-content-brief | Content Lead | M | Writer-ready brief for Wix Studio /agencies landing page |
| 2.4 | Ship Wix Studio /agencies landing page | Content + Eng | M | Page live; ranks present in top 50 for "website builder for agencies" |
| 2.5 | Run /seo-keyword-cluster on the qualitative gap themes from sibling gap example | seo-keyword-cluster | Content Lead | M | Cluster plan + sequencing for the agency / comparison / pricing-longtail themes |
| 2.6 | Run /seo-schema on the new /vs/* and /agencies pages | seo-schema | Eng | S | Comparison / Product / WebPage schema added; rich-result eligible |

**Phase exit criteria:** /vs/webflow, /vs/squarespace, /studio/agencies live and indexable. Cluster plan covers the agency segment end-to-end.

## Phase 3 — Compound + measure (weeks 9–12)

**Goal:** harden AI Search citation moats on the new pages; measure drift; retro + adjust.

| # | Work item | Skill / source | Owner | Effort | Phase-end metric |
|---|---|---|---|---|---|
| 3.1 | Run /seo-geo on /vs/webflow, /vs/squarespace, /studio/agencies | seo-geo | SEO Lead | M | GEO improvement recommendations per URL; AIO citation status documented |
| 3.2 | Run /seo-backlink-gap vs webflow.com + squarespace.com | seo-backlink-gap | Outreach | L | Prospect list for the outreach team |
| 3.3 | Run /seo-drift compare wix.com against Phase 1 baseline | seo-drift | SEO Lead | S | RED/YELLOW/GREEN deltas; what to investigate first |
| 3.4 | Quarterly retro: review pillar-score deltas, AI Search SoV delta vs 2026-04-27 baseline, adjust Q3 plan | (manual) | SEO Lead | M | Q3 plan signed off |

**Phase exit criteria:** drift compare shows no RED-tier regressions. AI Search SoV held or grew on the cluster covered by the new pages.

## Critical path

In order (anything off this list is moveable):

1. **Phase 1.1 (technical audit)** — blocks every page-level deploy in Phase 2.
2. **Phase 1.4 (drift baseline)** — must run BEFORE Phase 2 pages ship so Phase 3.3 has a comparable anchor.
3. **Phase 2.1 (competitor-pages draft)** — blocks Phase 2.2 (ship pages) and Phase 2.6 (schema on new pages).
4. **Phase 2.6 (schema)** — blocks Phase 3.1 (GEO analysis needs the pages indexed AND structured-data-rich to evaluate AIO citation potential).
5. **Phase 3.3 (drift compare)** — closes the loop on Phase 1.4.

## Metrics

| Metric | Type | Current | Phase 1 target | Phase 2 target | Phase 3 target |
|---|---|---|---|---|---|
| Organic traffic | Lagging | 1,417,427/mo (US) | hold at baseline | +5% from Phase 1 | +10% from Phase 1 |
| Pages with E-E-A-T ≥ 70 | Leading | [pending audit] | populate audit | maintain or grow | maintain or grow |
| Technical issue count | Leading | [pending audit] | reduce ≥25% | reduce ≥40% | reduce ≥50% |
| AI Search SoV (combined) | Lagging | 36.1% [SoV-2026-04-27] | hold ≥34% | hold ≥34% | hold ≥34% + grow on agency cluster |
| Referring domains | Leading | 3,356,565 | hold at baseline | grow with /vs/* outreach | +50 from outreach |

Targets are defensible because: (a) "hold at baseline" is the lowest credible bar for a category leader of Wix's size; (b) +5% traffic in 60 days is conservative for a site shipping 3 new high-leverage pages; (c) AI Search SoV holds because we don't ship enough new pages to swing the share materially — we just don't lose it.

## Constraints / caveats

- SE Ranking domain-level metrics are now populated (DA, traffic, referring domains, organic keyword count). Pillar scores for Technical and Content still require the Phase 1 specialist runs (seo-technical-audit, seo-content-audit) before the plan can be fully defended to a stakeholder.
- The /vs/* comparison-page strategy depends on Wix being willing to publish balanced comparison content that mentions competitors by name. If brand wants only Wix-only marketing pages, drop Phase 2.1, 2.2, 2.6 and pivot to a Wix-Studio-only narrative.
- "Hold AI Search SoV at 34%" is a no-loss target. If the team wants to grow SoV, that requires sustained content investment beyond the 90-day horizon — flag as a Q3+ initiative.

## Recommended next step

Run Phase 1 work items. After week 4, run /seo-drift compare wix.com against the Phase 1.4 baseline, then adjust Phase 2 scope. After Phase 3, re-run /seo-plan wix.com using the Phase 3.3 drift compare as the new "Where you are" anchor.

## Handoff payload
- Produced by: seo-plan
- Target: wix.com (90-day horizon, US, saas business type)
- Key findings: (a) Wix's two strongest pillars (Topical, AI Search) are already moats — defend, don't rebuild. (b) The unmeasured pillars (Technical, Content) are the Phase 1 priority — measure before you optimise. (c) The single highest-leverage build is wix.com/vs/webflow — Webflow's /vs/wix ranks #3 on Wix's own brand-comparison query and Wix has nothing defensive there (gap analysis sibling example). (d) The agency / designer cluster (Webflow + Framer) is the biggest competitive gap Wix can close with content, and Wix Studio is the product positioned to win it.
- Open loops: Full Phase 1 specialist runs (technical-audit, content-audit, backlinks-profile) all need SE Ranking auth. Phase 3.3 drift compare needs the Phase 1.4 baseline with SE Ranking auth.
- Recommended next skill: /seo-technical-audit wix.com (Phase 1.1 — the gating dependency for everything in Phase 2).
