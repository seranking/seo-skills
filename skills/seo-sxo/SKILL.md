---
name: seo-sxo
description: Diagnose why a page is not ranking by reading the SERP backwards. Identifies the page type Google rewards for the target keyword, scores the candidate page against that pattern from multiple persona perspectives, and recommends the page format that would win the SERP. Use when the user asks "why isn't this page ranking", "page type mismatch", "SXO", "search experience optimization", "intent mismatch", or wants a wireframe.
---

# SEO SXO — Search Experience Optimization

Diagnose why a "well-optimized" page doesn't rank. Reads the actual SERP for the target keyword, infers the page type Google is rewarding, scores the candidate page against that pattern from multiple persona perspectives, and recommends the page format that would win the SERP.

> **Acknowledgements:** SXO-as-a-skill framework originated in `claude-seo` by AgriciDaniel (with the original concept credited to Florian Schmitz, Pro Hub Challenge). MIT-licensed both directions; this implementation is independent but the framing is theirs.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available.
- User provides: (a) target page URL, (b) target keyword the page is meant to rank for, optionally (c) target country (default `us`).

## Process

1. **Validate inputs.** Both URL and keyword are required. If keyword missing, ask the user — don't infer.

2. **Pull the SERP** `DATA_getSerpResults` and `DATA_getSerpTaskAdvancedResults`
   - Top 10 organic results with URL, title, snippet.
   - SERP features: AI Overview presence, People Also Ask, image carousel, video carousel, shopping pack, Twitter pack, Featured Snippet, etc.

3. **Pull AIO context** `DATA_getAiOverview`
   - If AIO is present for the keyword, capture the answer text and citation list.
   - Note which top-10 organic results are also cited in the AIO.

4. **WebFetch top winners**
   - Fetch the user's page + the top 3 SERP winners.
   - Extract: `<title>`, all H-tags, schema types, primary content structure (numbered list? table? prose? Q&A?), word count, image-pack indicators, presence of comparison/feature tables, CTA presence and prominence.

5. **Classify each top-10 result by page type**
   - Use the heuristics in `references/page-type-patterns.md`.
   - For each: assign one of {comparison, alternatives, listicle, how-to, definition, product, editorial, forum, video}.
   - Note signals that informed the classification (URL pattern, title pattern, schema, content structure).

6. **Detect the dominant pattern**
   - Count types in top 10. If one type ≥ 6, that's dominant.
   - If two tie at 4–4, the SERP is "split intent" — both work; commercial vs informational angle determines which to choose.
   - Cross-reference with SERP features: video carousel → expect ≥ 2 video results; PAA → expect informational results; shopping pack → commercial intent dominant; AIO → informational consensus.

7. **Score the user's page** against the dominant pattern × 4 personas
   - Use the rubrics in `references/persona-rubrics.md`.
   - 4 personas: Skimmer, Researcher, Buyer, Validator.
   - 0–10 per persona. Apply the intent-weighting profile (also in persona-rubrics.md) to get a single 0–100 SXO score.

8. **Synthesise verdict and wireframe**
   - If user's page type matches dominant: SXO score reflects how well it executes the pattern. Recommend specific persona-targeted improvements.
   - If user's page type does NOT match dominant: this is the "page-type mismatch" case. Output a wireframe for the dominant page type, anchored in observed patterns from the top 3 winners.
   - Write `SXO-REPORT.md`.

## Output format

Create a folder `seo-sxo-{target-slug}-{YYYYMMDD}/` with:

```
seo-sxo-{target-slug}-{YYYYMMDD}/
├── 01-serp-snapshot.md            (top 10 + features + AIO)
├── 02-page-type-classification.md (each top-10 result classified)
├── 03-user-page-fingerprint.md    (the candidate page's structure)
├── 04-persona-scores.md           (4 personas × current page)
├── 05-recommendation.md           (verdict + page-type-winning wireframe)
└── SXO-REPORT.md                  (executive summary deliverable)
```

`SXO-REPORT.md` shape:

```markdown
# SXO Report: {URL} for keyword "{keyword}"

> Snapshot dated {YYYY-MM-DD} · Country: {country}

## SERP profile
- Top 10 page types: {comparison: 4, listicle: 3, editorial: 2, video: 1}
- Dominant pattern: **{pattern}** ({n} of 10)
- SERP features: AIO ✓ ({n} citations), PAA ✓ ({n} questions), Image carousel ✗, Video carousel ✗, Shopping pack ✗
- Intent: {informational | commercial-investigation | transactional | navigational}

## Your page
- Page type: **{detected type}**
- Page-type match with dominant: **{✓ match | ✗ MISMATCH — see Verdict}**
- Word count: {n}
- Primary content structure: {prose | numbered-list | table | step-blocks | Q&A | mixed}

## SXO score: **{score}/100**

| Persona | Weight | Score | Notes |
|---|---|---|---|
| Skimmer | {%} | {n}/10 | {1-line note} |
| Researcher | {%} | {n}/10 | {1-line note} |
| Buyer | {%} | {n}/10 | {1-line note} |
| Validator | {%} | {n}/10 | {1-line note} |

## Verdict

{One paragraph. If page type matches: "Your page is the right type for this SERP. The score gap is {X} points — see persona-specific gaps below." If MISMATCH: "Your page is a {your type} but the SERP rewards {dominant type}. No amount of on-page optimization will close the gap; ship a {dominant type} page instead. Wireframe below."}

## If MISMATCH — wireframe for the winning page type

\`\`\`
{Page title pattern — e.g., "{Brand A} vs {Brand B}: 2026 Comparison"}

[Hero / TL;DR — first 200 words answer the comparative question]
[Comparison table — must be visually dominant]
[Section per dimension — each with H2 named after the dimension]
[Verdict / recommendation — explicit, justified]
[FAQ — top 3–5 PAA questions]
[Schema — Product (×2) + BreadcrumbList + FAQPage]
\`\`\`

## If MATCH — top 3 changes by persona

1. {Skimmer}: {specific change}
2. {Researcher}: {specific change}
3. {Buyer or Validator}: {specific change}

## Raw data
- 02-page-type-classification.md — every top-10 result, classified
- 03-user-page-fingerprint.md — your page's signals
- 04-persona-scores.md — full persona-by-persona breakdown
```

## Tips

- Respect rate limit: 10 req/sec. The SERP calls in step 2/3 are fast; WebFetch calls in step 4 dominate latency, not API.
- Call `DATA_getCreditBalance` before running. ~10–20 credits typical.
- Page-type classification is a heuristic — `references/page-type-patterns.md` documents the signals so users can override. If the heuristic gets a result wrong, edit that file with the correction.
- The 4 personas are opinionated. They come from the framework's original source — don't invent more without good reason.
- The SXO score is directional. An 85/100 doesn't guarantee ranking; a 35/100 strongly suggests the page won't break through. Treat as a diagnostic, not a forecast.
- When the dominant pattern is split-intent (4-4), ship two pages — one per intent — rather than trying to make one page serve both. Google's SERPs reflect this split for a reason.
- The wireframe in MISMATCH mode is a starting point. The user still needs to write the content. This skill diagnoses; `seo-content-brief` produces the writer-ready brief.
