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

0. **Google data availability check (advisory, not blocking)**
   - Run `python3 scripts/google_auth.py --check --json`. If `tier >= 0`, the downstream specialist skills (technical-audit, page, content-audit, drift) will enrich their outputs with real Google field data — and `seo-plan` ingests those richer outputs in step 4. The plan itself doesn't dispatch `seo-google` directly; it prints a one-line notice so the user knows the option is on the table:
   ```
   > Google APIs detected (tier {n}, available: {comma-list}). Downstream specialist
   > skills (seo-technical-audit, seo-page, seo-content-audit, seo-drift) will enrich
   > their outputs with real CrUX / GSC / GA4 / URL Inspection data automatically.
   ```
   - If creds are missing, the plan continues with SE Ranking-only data and prints:
   ```
   > Google APIs not configured. To enrich downstream phases with real CWV / GSC /
   > GA4 / indexation data, run `bash extensions/google/install.sh`. Plan continues
   > with SE Ranking data only.
   ```
   - This is the **lightest possible auto-spawn** — `seo-plan` doesn't run `seo-google` itself (transferring friction to a single command is theirs' anti-pattern we critiqued in `EVAL_RESULT_v2.md`); it surfaces the option so the user can opt in or out before specialist skills run. See `skills/seo-google/references/cross-skill-integration.md` § "seo-plan" for the full rationale.

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

4. **Pull specialist inputs — confirm-then-dispatch pattern**
   - **4a. Detect existing outputs.** In the current working directory, look for any folder matching the patterns below dated within the last 30 days (treat folders older than 30 days as stale and re-list them as missing):
     - `seo-technical-audit-*`
     - `seo-content-audit-*`
     - `seo-competitor-gap-analysis-*`
     - `seo-ai-search-share-of-voice-*`
     - `seo-backlinks-profile-*`
   - For each present folder, ingest its primary deliverable (`TECH-AUDIT.md`, `VERDICT.md` rollup, `GAPS.md`, `REPORT.md`, `PROFILE.md` respectively).
   - **4b. Build the missing list.** For each prerequisite that did not have a fresh output, look up its credit-cost figure from the specialist's own SKILL.md (read those when forming the prompt — figures may drift):
     - `seo-technical-audit` → varies by page count for a fresh audit; ~6 Firecrawl credits for the modern-signals step. Cite "varies; check page count" if no recent audit cached.
     - `seo-content-audit` → ~10–15 SE Ranking credits + 1 Firecrawl credit per audited URL (default cap 50; for the seo-plan top-10-pages scope, expect ~10–15 SE Ranking + ~10 Firecrawl).
     - `seo-competitor-gap-analysis` → ~30–80 credits for 10 seeds.
     - `seo-ai-search-share-of-voice` → ~10–20 credits (leaderboard + ~20 prompts × N domains).
     - `seo-backlinks-profile` → ~25–40 SE Ranking credits.
   - **4c. Print the confirmation prompt** (single block, exactly this shape, with the missing-list filtered to only what is actually missing):
   ```
   To produce a defensible plan, seo-plan needs outputs from N specialists not yet
   run for {domain}:
   - seo-technical-audit (~{N} credits)
   - seo-content-audit (~{N} credits)
   - seo-competitor-gap-analysis (~{N} credits)
   - seo-ai-search-share-of-voice (~{N} credits)
   - seo-backlinks-profile (~{N} credits)
   Total estimated cost: ~{N} credits.
   Run them now in this session? (y/N — default N preserves the existing v2.6 behavior of asking the user to run them manually first)
   ```
   - **4d. If user answers `y`:** dispatch each missing specialist in this order, ingesting each primary deliverable as it completes:
     - **Parallel batch (independent):** `seo-technical-audit`, `seo-competitor-gap-analysis`, `seo-ai-search-share-of-voice`, `seo-backlinks-profile`.
     - **Sequential after the batch:** `seo-content-audit` — its top-10-pages scope depends on knowing the top traffic pages from `seo-competitor-gap-analysis` / `DATA_getDomainKeywords`, so it must run after the gap-analysis batch completes.
     - Each specialist runs its own `DATA_getCreditBalance` preflight and surfaces cost before proceeding (their existing behaviour — `seo-plan` does not bypass it). If any specialist aborts on a credit-balance check, surface that abort to the user and let them decide whether to top up or skip.
     - After every dispatch, ingest the new folder the same way step 4a does.
   - **4e. If user answers `N` (or anything else — default `N`):** fall through to the existing v2.6 behaviour — the plan opens with **Phase 0: Discovery**, and running each missing specialist becomes the first sprint's work. This preserves the user's control over credit spend in environments where the specialists should be scheduled or batched separately.

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
├── PLAN.md                              (synthesis — primary deliverable; inlines 01-baseline, 02-competitive-frame, 07-dependencies, 08-metrics as sections)
├── 04-phase-1-foundations.md            (load-bearing — owners share single phase files in standups)
├── 05-phase-2-build.md                  (load-bearing — owners share single phase files)
├── 06-phase-3-compound.md               (load-bearing — owners share single phase files)
└── evidence/
    ├── 01-baseline.md                   (where you are now — raw data inlined into PLAN.md)
    ├── 02-competitive-frame.md          (who you're actually competing with — raw data inlined into PLAN.md)
    ├── 03-pillar-scores.md              (technical / content / topical / AI Search — scoring math)
    ├── 07-dependencies-and-critical-path.md  (dependency map — inlined as PLAN.md section)
    └── 08-metrics.md                    (metric tables — inlined as PLAN.md section)
```

Top-level: `PLAN.md` + the three phase files (`04`/`05`/`06`). Owners share single phase files in standups, so phase files stay top-level rather than collapsing into PLAN.md. The verbatim-duplicate sections (baseline, competitive frame, dependencies, metrics) are inlined into PLAN.md but the raw step files are preserved in `evidence/` along with the pillar-scoring math.

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

- **Default is "no auto-dispatch."** The confirm prompt in step 4c defaults to `N`. If the user just hits Enter (or answers anything other than an explicit `y`), `seo-plan` falls through to the v2.6 Phase-0 behaviour and lists the missing specialists as the first sprint's work. This preserves user control over credit spend — important when the user is on a tight SE Ranking budget or wants to schedule specialists separately.
- **Auto-dispatch (the `y` path) is the convenience option.** When the user wants a finished plan in one session and is comfortable with the displayed credit estimate, the `y` path runs the missing specialists in the optimal parallel-then-sequential order described in step 4d, ingests their outputs, and proceeds straight into pillar scoring (step 5). No silent re-execution: every dispatch is gated by the single confirmation in step 4c.
- **Auto-dispatch respects each specialist's own credit-balance preflight.** Each specialist already calls `DATA_getCreditBalance` at its first step and surfaces cost before consuming credits — `seo-plan` does not bypass that gate. If a specialist aborts on its preflight (insufficient credits, user declines its inner cost prompt), `seo-plan` surfaces the abort and lets the user choose to top up, skip that specialist (and let it remain a Phase-0 work item), or cancel the rest of the dispatch.
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
