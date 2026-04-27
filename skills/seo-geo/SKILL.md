---
name: seo-geo
description: URL-level Generative Engine Optimization (GEO) analysis. For a specific URL, pulls AI Overview citation data scoped to the URL's primary keywords, identifies which AIO queries cite the URL vs which don't but should, and recommends page-level changes that improve LLM citability. Distinct from `seo-ai-search-share-of-voice` (domain-level, brand vs brand) — this is one URL, deeper. Use when the user asks "GEO for this page", "AIO citation analysis", "AI search readiness for URL", "why isn't this page cited", or "improve LLM citations".
---

# Page-Level GEO (Generative Engine Optimization)

For one URL, surface its AI-search citation footprint and recommend the page-level changes that would improve citability across AI Overview, Perplexity, ChatGPT, and other LLM-powered search engines. Different from the domain-level brand-vs-brand share-of-voice — this is page-level diagnosis.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available.
- User provides: a target URL. Optional: target country (default `us`), specific keywords to focus on (defaults: the URL's top-5 traffic-weighted keywords from SE Ranking).

## Process

1. **Validate & preflight**
   - Confirm URL is fetchable.
   - `DATA_getCreditBalance` — surface remaining credits. ~10–20 credits typical.

2. **URL keyword footprint** `DATA_getUrlOverviewWorldwide` and `DATA_getDomainKeywords` (URL-filtered)
   - Pull URL's overview (keywords, traffic).
   - Pull all keywords the URL ranks for. Sort by traffic-weighted score.
   - Take the top 5 as the GEO investigation set (or use user-supplied keywords).

3. **AIO presence per keyword** `DATA_getAiOverview`
   - For each keyword, query AIO presence + citation list.
   - Flag: AIO present? Is the candidate URL cited?
   - Capture the AIO answer text — it tells you what passage shape Google's models prefer.

4. **AIO leaderboard per keyword** `DATA_getAiOverviewLeaderboard`
   - Full ranked list of cited sources per AIO query.
   - Identify patterns: domain-level (which sites consistently cited?), passage-level (what structure?).

5. **Page passage-level audit** `WebFetch`
   - Pull the page HTML.
   - Identify "passages" — paragraphs that could be extracted standalone (TL;DR boxes, definition paragraphs, summary sentences after H2s).
   - For each passage, score citability:
     - Has it a complete thought in 1–3 sentences?
     - Does it answer a specific question (i.e., the question its parent H2 implies)?
     - Has it a stat / number / named entity?
     - Has it a clear timestamp or freshness signal?
   - This is the citability layer.

6. **Compare candidate to cited sources**
   - For each AIO query where candidate is NOT cited, identify the cited sources.
   - WebFetch 2–3 of them.
   - Extract the cited passage (often a snippet from the AIO answer).
   - Compare passage shape: candidate vs cited. Surface specific structural / content / freshness gaps.

7. **Schema check**
   - Re-parse the page's JSON-LD. Specifically check for: `Article`/`BlogPosting` with valid `author` + `datePublished` + `dateModified`; `FAQPage` if Q&A blocks present; `BreadcrumbList`; `mainEntityOfPage` self-canonical.
   - Schema isn't a direct citation signal but it correlates strongly with citation rates in Google's AIO.

8. **Synthesise** `GEO.md`

## Output format

Create a folder `seo-geo-{target-slug}-{YYYYMMDD}/` with:

```
seo-geo-{target-slug}-{YYYYMMDD}/
├── 01-url-keyword-footprint.md  (URL overview + top keywords)
├── 02-aio-by-keyword.md         (AIO presence + citation per keyword)
├── 03-leaderboards.md           (full leaderboards per keyword)
├── 04-page-passages.md          (extracted passages + citability scores)
├── 05-cited-source-comparison.md (gap vs cited sources)
├── 06-schema-check.md           (JSON-LD audit for GEO-relevant types)
└── GEO.md                       (synthesised report + recommendations)
```

`GEO.md` follows this shape:

```markdown
# GEO Analysis: {URL}

> Snapshot dated {YYYY-MM-DD} · Country: {country} · Keywords analysed: {n}

## Citation footprint

| Keyword | AIO present | Candidate cited | Citers |
|---|---|---|---|
| {keyword 1} | ✓ | ✗ | {3 cited sources} |
| {keyword 2} | ✓ | ✓ | {includes candidate + 2 others} |
| ... |

**Citation rate: {n}/{checked} ({%}) of AIOs where candidate could appear actually cite it.**

## Where the candidate IS cited
- {keyword X} — passage cited: "{passage text}"
- ...

## Where the candidate is NOT cited (and AIO is present)
- {keyword Y} — cited sources tend to share these patterns:
  - {pattern 1: short definitive answer in first 100 words}
  - {pattern 2: numbered stat with date}
  - {pattern 3: schema-marked Article with author bio}
- The candidate is missing: {specific gap}.

## Page passage-level audit

Top-scoring passages on the candidate (by citability score):
1. {passage at H2 "X" — score 8/10. Strong: definitive sentence, named stat. Weak: no date.}
2. ...

Lowest-scoring passages (refresh candidates):
1. {passage at H2 "Y" — score 3/10. Weak: vague generalities, no specific data.}
2. ...

## Schema check
- `Article` (or sub-type) present and valid: {✓/✗}
- `author` populated with `@type: Person` and `url`: {✓/✗}
- `datePublished` + `dateModified` ISO 8601: {✓/✗}
- `FAQPage` for visible Q&A: {✓/✗/N-A}
- `BreadcrumbList`: {✓/✗}

## Recommendations (top 5 to improve citability)

1. {Specific change — e.g., "Add a 60-word TL;DR after the H1 that directly answers '{primary keyword}' — current page buries the answer below 800 words of preamble"}
2. {Specific change}
3. {Specific change}
4. {Specific change}
5. {Specific change}

## Recommended next step
Re-run `seo-geo` on this URL in 30 days after applying the recommendations. AIO indexes update on a monthly cadence — citation changes show up there first.
```

## Tips

- Respect rate limit. ~5 keywords × 2 AIO calls = ~10 calls; plus 2–3 WebFetch on cited sources. Easy.
- Cost: ~10–20 credits typical.
- **Citation isn't ranking.** A page can rank well organically and still not be cited in AIO. The opposite happens too — cited pages often rank below their citation rate.
- The biggest GEO levers are usually:
  1. Definitive answer in the first 200 words.
  2. Specific stats with dates and sources.
  3. Schema with author + dates.
  4. Passage-level structure (each H2 is a question; first paragraph after H2 is the answer).
- Pair with `seo-ai-search-share-of-voice` for domain-level brand-vs-brand visibility (this skill is page-level).
- Pair with `seo-content-audit` to apply the CITE rubric to the page (which has more citation-readiness items).
- Pair with `seo-schema` to fix schema issues identified in step 7.
- Don't optimize for AIO at the expense of human readability. The two reinforce each other when done right.
