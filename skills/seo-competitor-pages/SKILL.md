---
name: seo-competitor-pages
description: Generate SEO-optimized "X vs Y" comparison and "alternatives to X" landing pages targeting comparative-intent keywords. Pulls competitor data, comparative-intent SERPs, and existing comparison pages to produce a balanced, structured page draft with feature matrix, schema, and conversion blocks. Distinct from `seo-agency-landing-page` (top-of-funnel demand-gen). Use when the user asks for "comparison page", "vs page", "alternatives page", "X vs Y", "alternative to X", or "competitor comparison page".
---

# Competitor Comparison & Alternatives Pages

Produce conversion-tuned landing pages targeting comparative-intent keywords ("X vs Y", "alternatives to X", "best X for Y"). The deliverable is a paste-ready page draft with feature matrix, balanced verdict, schema markup, and a CTA flow that converts comparison-stage traffic.

## Page types this skill produces

1. **"X vs Y" head-to-head** — direct comparison between two products/services. Target keyword: `[Product A] vs [Product B]`.
2. **"Alternatives to X"** — listicle-format page positioning the user's product as one of N alternatives to a category leader. Target keyword: `[Competitor] alternatives` or `alternatives to [Competitor]`.
3. **"Best X for Y"** — segmented best-of page targeting a use case or audience. Target keyword: `best [category] for [use case]`.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available.
- User provides: (a) the user's brand/product (the page's hero), (b) target competitor(s) — at least one, optionally up to 5 for an alternatives page, (c) page type (auto-detected from the keyword if user doesn't specify), (d) target country (default `us`).

## Process

1. **Validate & determine page type**
   - From the user's input, detect: vs / alternatives / best-of.
   - If page type unclear, ask the user. Don't guess silently.

2. **Pull competitor context** `DATA_getDomainCompetitors`
   - For the user's domain, list top organic competitors by `common_keywords` overlap.
   - Validate that the user's named competitor is in the list (or close).

3. **Pull keyword data per brand** `DATA_getDomainKeywords`
   - For the user's domain and each named competitor, pull top 100 organic keywords.
   - Identify: keywords each brand owns exclusively, keywords both rank for, gaps.

4. **Pull comparative SERPs** `DATA_getSerpResults` and `DATA_getKeywordQuestions`
   - For "X vs Y" / "alternatives to X" / "best X for Y" target keyword(s):
     - Top 10 organic results — who else ranks for this comparative keyword?
     - PAA questions (these become FAQ section content).
     - Featured snippet (if present, capture the answer pattern).

5. **Fetch existing comparison pages** `WebFetch`
   - Pull the top 3 SERP winners for the target keyword.
   - Extract their structure: H2 outline, feature-matrix dimensions, verdict pattern, CTA placement, schema types.
   - This anchors the draft in observed-rewarded-pattern.

6. **Pull keyword comparison data** `DATA_getDomainKeywordsComparison` (if available for the brands)
   - Side-by-side keyword overlap.

7. **Build feature matrix**
   - Dimensions inferred from the top SERP winners (e.g., "Pricing", "Free tier", "Integrations", "Support tiers", "Best for").
   - Cells: ✓ / ✗ / partial / "TBD — confirm with PM" placeholders for fields you can't auto-infer.
   - Where SE Ranking data informs a cell (e.g., "ranks for X enterprise keywords"), pull the number.

8. **Synthesise** `COMPARISON.md`
   - Hero (target keyword in H1, balanced positioning).
   - TL;DR / verdict box in first 200 words.
   - Feature matrix.
   - Section per major dimension (each H2 = one dimension).
   - PAA-derived FAQ (top 3–5 questions from step 4).
   - Verdict / recommendation.
   - CTA flow.
   - Schema-ready JSON-LD: `Product` (×N) + `BreadcrumbList` + `FAQPage` (if real Q&A).

## Output format

Create a folder `seo-competitor-pages-{target-slug}-{YYYYMMDD}/` with:

```
seo-competitor-pages-{target-slug}-{YYYYMMDD}/
├── 01-competitor-context.md      (DATA_getDomainCompetitors)
├── 02-keyword-overlap.md         (DATA_getDomainKeywords for each brand)
├── 03-comparative-serp.md        (top 10 + PAA for the target keyword)
├── 04-existing-pages-teardown.md (top-3 SERP winners' structure)
├── 05-feature-matrix.md          (inferred dimensions × brands)
├── schema.jsonld                 (paste-ready Product + Breadcrumb + FAQ)
└── COMPARISON.md                 (the page draft)
```

`COMPARISON.md` for an "X vs Y" page follows this shape:

```markdown
# {User's Brand} vs {Competitor}: 2026 Comparison

> Updated {YYYY-MM-DD}. Compare {Brand A} and {Brand B} on pricing, features, integrations, and best-fit use case.

## TL;DR
{One paragraph balanced verdict — when to choose A, when to choose B}

## At a glance

| Dimension | {Brand A} | {Brand B} |
|---|---|---|
| Starting price | {$X/mo} | {$Y/mo} |
| Free tier | {✓/✗} | {✓/✗} |
| Best for | {use case} | {use case} |
| Integrations | {n} | {n} |
| Support | {tier} | {tier} |
| ... | | |

## {Dimension 1 header — e.g., Pricing}
{Side-by-side detail, balanced. Avoid hyperbole.}

## {Dimension 2 header — e.g., Features}
{...}

## {Dimension 3 header — e.g., Integrations}
{...}

## {Dimension 4 header — e.g., Support}
{...}

## When to choose {Brand A}
- {scenario 1}
- {scenario 2}
- {scenario 3}

## When to choose {Brand B}
- {scenario 1}
- {scenario 2}
- {scenario 3}

## FAQ
**{PAA question 1}**
{Answer}

**{PAA question 2}**
{Answer}

**{PAA question 3}**
{Answer}

## Get started
{Brand A} CTA — {link}
{Brand B} CTA — {link if balanced; otherwise drop}

## Schema
See `schema.jsonld` — paste into `<head>`.
```

## Tips

- **Balance is conversion.** Pages that pretend the user's product is always better lose trust and rankings. Honest assessments outperform partisan ones.
- Respect rate limit. Step 5 (fetching top 3 SERP winners) takes 3 WebFetch calls + earlier MCP queries.
- Cost: ~15–25 credits typical.
- **Schema:** use `Product` for both products in a vs page, plus `BreadcrumbList`, plus `FAQPage` if the FAQ section is real Q&A (not a manufactured one).
- For "alternatives to X" pages, position the user's product as one of N (typically 5–10), not as #1. Numbered listicles convert better than self-promotional alternatives pages.
- For "best X for Y" pages, segment by use case explicitly — "best for solo developers" vs "best for enterprise teams" — this lets you win multiple long-tail variants.
- Run `seo-page` on the published page after 30 days to track ranking trajectory.
- Pair with `seo-content-audit` to E-E-A-T-check the draft before publishing.
- The PAA-derived FAQ in step 4 is gold — those are the questions users are actually searching, and answering them in-page raises citation-readiness for AIO.
- Don't auto-publish. Hand the draft to a writer/PM for fact-checking and brand-voice tuning.
