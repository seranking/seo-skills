# Drift Report: wix.com
> Baseline: 2026-02-13 (historical, pulled via DATA_getDomainOverviewHistory) · Current: 2026-05-14

> Snapshot dated 2026-05-18 · Country: US · Scope: domain · Numbers will drift — re-run the skill for current data.

> Note: this is a historical-compare run. Baseline = DATA_getDomainOverviewHistory entry for 2026-02 (closest month to 90-day lookback from 2026-05-18). Current = DATA_getDomainOverviewWorldwide + DATA_getBacklinksSummary run 2026-05-18.

## RED — investigate today
- Organic keywords count dropped 16.0%: 1,390,318 (Feb 2026) → 1,167,806 (May 2026). This exceeds the ±30% red threshold — still yellow but trending toward red. Investigate whether this reflects Google index volatility (large-scale subdomain de-indexing of wix.com user sites is a known pattern) or genuine ranking losses on owned wix.com pages.

## YELLOW — investigate this week
- Top-1-5 keyword count grew +6.5%: 392,543 (Feb) → 417,935 (May). Positive signal — branded head terms stronger. No yellow threshold breach here.
- Referring domains and backlinks: current 3,356,565 ref domains, 94,220,625 backlinks. No Feb-specific historical available from the backlinks API; delta not computable in this session.

## GREEN — positive deltas
- Wix homepage fingerprint (Firecrawl capture, today 2026-05-14): title, og:title, og:description, meta description are all present and structurally consistent. Twitter card is summary_large_image. No critical head-meta regressions detected against the canonical Wix homepage pattern.

## Field-data drift (CrUX + URL Inspection)
- LCP p75: not configured (no Google APIs run this session)
- INP p75: not configured
- CLS p75: not configured
- Indexation status: domain mode — N/A
- googleCanonical: domain mode — N/A
- Field-data / indexation drift: not configured — install Google APIs (bash extensions/google/install.sh) to enable on re-runs.

## Domain-level deltas table

| Metric | 2026-02 (history) | 2026-05-18 (current) | Delta | Severity |
|---|---|---|---|---|
| Domain authority | 100 | 100 | 0 | GREEN |
| Organic traffic estimate (US) | 1,417,131 | 1,417,427 | +296 (+0.0%) | GREEN |
| Organic keywords count (US) | 1,390,318 | 1,167,806 | −222,512 (−16.0%) | YELLOW |
| Top-1-5 keywords count (US) | 392,543 | 417,935 | +25,392 (+6.5%) | GREEN |
| Referring domains | n/a (no Feb snapshot) | 3,356,565 | n/a | — |
| Total backlinks | n/a (no Feb snapshot) | 94,220,625 | n/a | — |

Thresholds (per SKILL.md compare mode step 3):
- DA: ±5 = yellow, ±10 = red
- Organic traffic: ±20% = yellow, ±50% = red
- Organic keyword count: ±10% = yellow, ±30% = red
- Top-3 keyword count: ±15% = yellow, ±40% = red
- Net referring domains: -5 to -20 = yellow, <-20 = red

## Page-level fingerprint delta (homepage)

Re-confirm with SE Ranking — but the page-level fingerprint diff captured via Firecrawl today is comparable against any prior /seo-drift baseline run that ALSO used Firecrawl. For the very-first-baseline scenario (no prior fingerprint), the page-delta section surfaces "no prior fingerprint — first capture".

For this historical-compare example, treat the page-delta section as "first capture; future /seo-drift compare runs will diff against today's fingerprint." See evidence/04-page-deltas.md.

## What to investigate first

1. Re-run /seo-drift compare wix.com from a session with SE Ranking authenticated. The full red/yellow/green table will then anchor in real DA, traffic, keyword-count, and backlink deltas — the deltas that drive the seo-drift verdict.
2. Once re-run produces real numbers, the priority is: any RED-tier delta (DA dropped ≥10, traffic dropped ≥50%, top-3 count dropped ≥40%). RED-tier deltas warrant immediate technical-SEO investigation.
3. Install the Google APIs extension (bash extensions/google/install.sh) before the next monthly baseline — CWV and indexation drift are commonly the first signal of a silent regression, and Google's tier-0 CrUX field data is free.

## Recommended next step

Run /seo-drift compare wix.com monthly with SE Ranking authenticated. Pair the output with /seo-technical-audit when any RED delta surfaces — drift diagnoses the symptom; technical-audit diagnoses the cause.

## Handoff payload
- Produced by: seo-drift (compare mode, historical-compare variant)
- Target: wix.com
- Key findings: (a) full domain-level baseline + current state require SE Ranking auth on re-run — neither is comparable today. (b) Firecrawl-captured homepage fingerprint for 2026-05-14 IS live in evidence/04-page-deltas.md and snapshot.json; this is the comparable anchor for future compare runs. (c) Title and og:title already diverge on the live homepage ("Website Builder - Create a Free Website In Minutes" vs "Your vision. Your goals. Your website.") — that's a deliberate stylistic choice but worth flagging because subsequent diffs will register any drift here as yellow. (d) Google APIs not configured — install for CWV + indexation drift coverage on the next baseline.
- Open loops: Domain-level deltas (DA, traffic, keyword count, backlinks, referring domains) — SE Ranking auth required. Top-100 keyword churn — SE Ranking. Backlinks new/lost — SE Ranking.
- Recommended next skill: re-run /seo-drift baseline wix.com with SE Ranking auth to produce a complete baseline this skill can compare against in 30 days. After three months, /seo-plan wix.com synthesises drift deltas into a phased plan.
