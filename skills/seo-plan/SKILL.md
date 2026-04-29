---
name: seo-plan
description: Build a phased SEO roadmap for a domain — quarter-by-quarter, tied to the site's competitive position, content gaps, technical debt, and AI Search readiness. Synthesises the outputs of multiple skills (`seo-technical-audit`, `seo-content-audit`, `seo-keyword-cluster`, `seo-competitor-gap-analysis`, `seo-ai-search-share-of-voice`) into one site-level plan with sequencing, owners, and success metrics. Distinct from `seo-keyword-cluster` (keyword architecture for one topic), `seo-content-brief` (one article), and `seo-keyword-niche` (longtail content tier). Use when the user asks for an "SEO plan", "SEO strategy", "SEO roadmap", "90-day plan", "quarterly SEO plan", "site SEO strategy", or "where do we focus next".
---

# SEO Plan

Produce a phased SEO roadmap for a domain. Output is a single `PLAN.md` plus per-phase deliverable folders, each phase scoped to a quarter (or a 90-day sprint), each with explicit goals, work items, owners, and metrics. The plan is grounded in the site's actual competitive position — not a generic checklist.

This is the "what should we work on next quarter" skill. It does not replace specialist skills — it composes them, then sequences their outputs.

## Prerequisites

- SE Ranking MCP server connected.
- `seo-firecrawl` available for site mapping and head metadata (optional but recommended).
- User provides:
  - Target domain.
  - Optionally: target country (default `us`), business type (saas / ecommerce / local / publisher / agency / b2b — auto-detected from the domain if not supplied), planning horizon (default 90 days, options: 30 / 90 / 180 / 365).
  - Optionally: known constraints (engineering capacity, content budget, no JS-render changes allowed, etc.).

## Process

1. **Detect business type** `DATA_getDomainOverviewWorldwide`, plus a Firecrawl `scrape` of the homepage if available
   - Inspect title, H1, JSON-LD types, primary nav patterns.
   - Classify as one of: `saas`, `ecommerce`, `local`, `publisher`, `agency`, `b2b-services`, `marketplace`. If ambiguous, ask the user once.
   - Business type drives template selection (see step 6).

2. **Domain baseline** `DATA_getDomainOverviewWorldwide`, `DATA_getDomainOverviewHistory`, `DATA_getDomainAuthority`, `DATA_getBacklinksSummary`
   - Capture: organic keywords, organic traffic estimate, DA, backlink profile health, top countries, traffic trend over the last 12 months.
   - This sets the "where you are now" anchor.

3. **Competitive frame** `DATA_getDomainCompetitors`
   - Pull top 5–10 organic competitors.
   - For each: organic keywords, traffic share, DA, top topical clusters they own.
   - Identifies who the user is *actually* competing with on the SERP (often different from who they think).

4. **Pull specialist inputs in parallel** (do NOT re-run these inside `seo-plan` — invoke the specialist skills separately and ingest their outputs if already produced; if not produced, queue them as Phase 0)
   - `seo-technical-audit` → site-wide technical debt list with severity.
   - `seo-content-audit` (sampled across top 10 traffic pages) → E-E-A-T + CITE quality baseline.
   - `seo-competitor-gap-analysis` → keyword gap buckets by intent + difficulty.
   - `seo-ai-search-share-of-voice` → AI Search visibility vs competitors.
   - `seo-backlinks-profile` → link health + toxic candidates.
   - If any of these are missing, the plan opens with **Phase 0: Discovery** — running them is the first sprint's work.

5. **Score the four pillars**
   - **Technical health** (0–100): from `seo-technical-audit` severity-weighted issue count.
   - **Content quality** (0–100): average E-E-A-T+CITE score across audited pages.
   - **Topical authority** (0–100): cluster coverage relative to top 3 competitors.
   - **AI Search readiness** (0–100): citation share vs SoV competitors.
   - The lowest pillar becomes the **lead theme** for the first phase.

6. **Apply business-type template** (templates differ — pick one and parameterise)
   - **saas** → product-led pillars + integration pages + comparison/alternatives + JTBD content.
   - **ecommerce** → category page hygiene + product schema + faceted-nav indexation rules + review aggregation.
   - **local** → GBP optimisation + location pages + citation cleanup (note: we don't have a `seo-local` skill yet — flag this as a manual sub-step or external).
   - **publisher** → topical clusters + author E-E-A-T + freshness cadence + AI-Search citations.
   - **agency** → service pages + case studies + comparison content + lead-gen LP (use `seo-agency-landing-page`).
   - **b2b-services** → industry-specific landing pages + thought-leadership clusters + decision-stage content.
   - Template provides default work-item categories; the lowest-pillar score from step 5 weights them.

7. **Phase the plan** — three phases over the planning horizon, each with goals, work items, owners, metrics
   - **Phase 1 (weeks 1–4 of horizon): Foundations.** Technical fixes that unblock everything else, baseline drift snapshot, 1–2 quick-win content refreshes from `seo-page` verdicts.
   - **Phase 2 (weeks 5–8): Build.** Content tier from `seo-keyword-cluster` (1 pillar + 3–7 spokes), schema fixes from `seo-schema`, comparison page from `seo-competitor-pages` if competitive frame supports it.
   - **Phase 3 (weeks 9–12): Compound + measure.** AI Search readiness pass via `seo-geo` on top pages, backlink-gap outreach starter from `seo-backlink-gap`, second drift comparison via `seo-drift compare`, retro + adjust.
   - For longer horizons (180/365 days), repeat phases 2+3 with refreshed inputs and a quarterly retro.
   - Each work item is tagged with the skill that produces it: `seo-content-brief`, `seo-schema`, `seo-page`, etc.

8. **Pick metrics**
   - **Lagging (quarterly):** organic traffic, organic keywords ranking top-10, organic conversions.
   - **Leading (weekly/monthly):** technical-issue count, pages with E-E-A-T verdict ≥ 70, AI Search citation count, referring-domain count.
   - One leading + one lagging per phase. Tie each metric to a current value (from step 2) and a phase-end target. Targets must be defensible — call out base rates.

9. **Sequencing + dependencies**
   - Build a dependency map: e.g., "rewrite cluster A pillar" depends on "fix `noindex` on /blog templates" depends on "run `seo-technical-audit`."
   - Surface the critical path. Anything off the critical path is moveable; anything on it blocks the phase.

10. **Synthesise** `PLAN.md`

## Output format

Folder `seo-plan-{domain-slug}-{YYYYMMDD}/`:

```
seo-plan-{domain-slug}-{YYYYMMDD}/
├── 01-baseline.md                  (where you are now)
├── 02-competitive-frame.md         (who you're actually competing with)
├── 03-pillar-scores.md             (technical / content / topical / AI Search)
├── 04-phase-1-foundations.md
├── 05-phase-2-build.md
├── 06-phase-3-compound.md
├── 07-dependencies-and-critical-path.md
├── 08-metrics.md
└── PLAN.md                         (synthesis)
```

`PLAN.md` follows this shape:

```markdown
# SEO Plan: {domain}

> Plan dated {YYYY-MM-DD} · Horizon: {n} days · Business type: {type} · Country: {country}

## Where you are
- Organic keywords: {n} (trend: {↑↓→ over 12mo})
- Organic traffic estimate: {n}/mo
- Domain authority: {n}
- Referring domains: {n}
- Pillar scores: Technical {n}/100 · Content {n}/100 · Topical {n}/100 · AI Search {n}/100

## Lead theme
{The lowest pillar from step 5, plus a one-line "why this is the constraint."}

## Top 5 competitors
| Domain | DA | Organic kw | Top cluster they own |
|---|---|---|---|
| {comp} | {n} | {n} | {cluster} |

## Phase 1 — Foundations (weeks 1–4)

**Goal:** {1-line outcome, e.g. "remove technical debt blocking content investment"}

| # | Work item | Skill / source | Owner | Effort | Phase-end metric |
|---|---|---|---|---|---|
| 1.1 | {item} | `seo-technical-audit` follow-up | {role} | {S/M/L} | {metric} |
| 1.2 | ... | | | | |

**Phase exit criteria:** {what must be true to declare Phase 1 done}

## Phase 2 — Build (weeks 5–8)
{same shape}

## Phase 3 — Compound + measure (weeks 9–12)
{same shape}

## Critical path
{Ordered list of work items that block subsequent phases. Anything not on this list is moveable.}

## Metrics

| Metric | Type | Current | Phase 1 target | Phase 2 target | Phase 3 target |
|---|---|---|---|---|---|
| Organic traffic | Lagging | {n} | {n} | {n} | {n} |
| Pages with E-E-A-T ≥ 70 | Leading | {n} | {n} | {n} | {n} |
| Technical issue count | Leading | {n} | {n} | {n} | {n} |
| AI Search citation count | Leading | {n} | {n} | {n} | {n} |
| Referring domains | Leading | {n} | {n} | {n} | {n} |

## Constraints / caveats
{User-supplied constraints, plus anything the data flags — e.g., "DA gap to top competitor is 25 points; expect 6+ months for keyword parity."}

## Recommended next step
Run Phase 1 work items. After week 4, run `seo-drift compare` against the baseline captured today, then adjust Phase 2 scope.
```

## Tips

- **`seo-plan` does not run other skills' work** — it sequences them. If `seo-technical-audit` hasn't been run, Phase 0 of the plan is "run it." Don't silently re-execute specialist skills inside this one; you'll burn credits and produce stale duplicates.
- **Auto-detect business type cheaply.** Homepage `<title>`, schema `@type`, and top-nav anchors are usually enough. Ask the user only when truly ambiguous.
- **The lead theme is the lowest pillar score.** Don't pick the pillar the user is most excited about — pick the one the data says is the constraint. Surface this gap explicitly if they conflict.
- **Three phases, even for 30-day horizons.** Compress, don't drop. A 30-day plan is foundations (weeks 1–2), build (weeks 2–3), measure (week 4). The structure forces sequencing discipline.
- **Targets must be defensible.** Don't write "double organic traffic in Q1." Tie each target to a base rate from competitor data or category benchmarks. If the math doesn't support a target, say so and lower it.
- **Critical path is the deliverable.** Most teams can do *something*; few know what's blocking what. Surface the dependency chain — that's where this skill earns its keep.
- **Local SEO is a known gap.** If business type is `local`, flag that we don't have a `seo-local` skill yet and recommend manual GBP audit as a Phase 0 item. Don't pretend coverage we don't have.
- **Don't generate work items the team can't execute.** If the user said "no JS-render changes allowed," drop those items even if they're high-leverage. A plan that won't ship is worse than a smaller plan that does.
- **Update cadence.** A 90-day plan should be re-run at the 90-day mark with `seo-drift compare` against the original baseline as input. Drift output rewrites the "Where you are" section; everything downstream updates from there.

## Works well with

- **Predecessors:**
  - `seo-technical-audit`, `seo-content-audit`, `seo-competitor-gap-analysis`, `seo-ai-search-share-of-voice`, `seo-backlinks-profile` — produce inputs.
  - `seo-drift baseline` — captures the snapshot the plan measures progress against.
- **Successors:**
  - `seo-keyword-cluster` — when Phase 2 calls for a content tier.
  - `seo-content-brief` — for each spoke article in Phase 2.
  - `seo-schema` — for structured-data work items.
  - `seo-competitor-pages` — when comparison content is on the plan.
  - `seo-drift compare` — at end of phase to measure progress.
  - `seo-page` — for individual URL keep/refresh/consolidate/kill calls in Phase 1.
