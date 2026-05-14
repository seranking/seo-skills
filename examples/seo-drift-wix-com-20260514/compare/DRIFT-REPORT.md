# Drift Report: wix.com
> Baseline: 2026-02-13 (historical, pulled via DATA_getDomainOverviewHistory) · Current: 2026-05-14

> Snapshot dated 2026-05-14 · Country: US · Scope: domain · Numbers will drift — re-run the skill for current data.

> Session note: this is a historical-compare run. The seo-drift skill normally compares two real time-separated snapshots (one stored from a prior /seo-drift baseline run, one from today's capture). In this example we substitute the prior snapshot with the historical entry from DATA_getDomainOverviewHistory ~90 days ago. SE Ranking MCP auth was unavailable in this session, so both the historical pull and today's domain-level capture are marked [SE Ranking — pending] in the evidence files below. Page-level Firecrawl capture for today IS live (see evidence/04-page-deltas.md).

## RED — investigate today
- [SE Ranking — pending] — DA, traffic, top-3 keyword count changes can only be computed once DATA_getDomainOverviewHistory (baseline) and DATA_getDomainOverviewWorldwide (current) both run with auth. Re-run with SE Ranking authenticated.

## YELLOW — investigate this week
- [SE Ranking — pending] — net-referring-domains delta needs DATA_getBacklinksSummary at both timepoints.

## GREEN — positive deltas
- Wix homepage fingerprint (Firecrawl capture, today 2026-05-14): title, og:title, og:description, meta description are all present and structurally consistent. Twitter card is summary_large_image. No critical head-meta regressions detected against the canonical Wix homepage pattern.

## Field-data drift (CrUX + URL Inspection)
- LCP p75: not configured (no Google APIs run this session)
- INP p75: not configured
- CLS p75: not configured
- Indexation status: domain mode — N/A
- googleCanonical: domain mode — N/A
- Field-data / indexation drift: not configured — install Google APIs (bash extensions/google/install.sh) to enable on re-runs.

## Domain-level deltas table (historical-compare placeholder)

| Metric | 2026-02-13 (history) | 2026-05-14 (current) | Delta | Severity |
|---|---|---|---|---|
| Domain authority | [SE Ranking — pending] | [SE Ranking — pending] | [pending] | [pending] |
| Organic traffic estimate | [pending] | [pending] | [pending] | [pending] |
| Organic keywords count | [pending] | [pending] | [pending] | [pending] |
| Top-3 keywords count | [pending] | [pending] | [pending] | [pending] |
| Referring domains | [pending] | [pending] | [pending] | [pending] |
| Total backlinks | [pending] | [pending] | [pending] | [pending] |

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
