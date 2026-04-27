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
   - **Firecrawl availability check.** If `mcp__firecrawl-mcp__firecrawl_scrape` is available, the JSON-LD parse in step 7 and the new AI-protocol-files step 8 use it (~3 Firecrawl credits). If unavailable, those steps emit `(skipped — Firecrawl not installed; install via extensions/firecrawl/install.sh)` notes in `GEO.md` rather than failing the run. User may pass `--no-firecrawl` to skip Firecrawl even when available (saves credits).

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

7. **Schema check** `mcp__firecrawl-mcp__firecrawl_scrape`
   - WebFetch in step 5 returned markdown — JSON-LD blocks were stripped before parsing. The schema check requires Firecrawl to recover them.
   - **If Firecrawl available:** scrape the target URL once (1 Firecrawl credit), parse the returned `html` for every `<script type="application/ld+json">` block. Specifically check for: `Article`/`BlogPosting` with valid `author` + `datePublished` + `dateModified`; `FAQPage` if Q&A blocks present; `BreadcrumbList`; `mainEntityOfPage` self-canonical.
   - **If Firecrawl unavailable:** write `Schema check: skipped — Firecrawl required to parse JSON-LD blocks (WebFetch returns markdown only).` into `06-schema-check.md`, mirror the same line in the GEO.md "Schema check" section. Don't infer from markdown — that's the bug this section closes.
   - Schema isn't a direct citation signal but it correlates strongly with citation rates in Google's AIO.

8. **AI-protocol files** `mcp__firecrawl-mcp__firecrawl_scrape`
   - **If Firecrawl available:** scrape `https://{domain}/llms.txt` and `https://{domain}/.well-known/rsl.json` (and the legacy `/RSL.txt` location as a fallback). Cost: 2 Firecrawl credits (one per file).
   - For each file: capture HTTP status (200 / 404 / other), full body if present, and a parsed summary (declared content categories, allow/deny scope, attribution requirements).
   - Surface in `07-ai-protocol-files.md` and in GEO.md as a new "AI-protocol files" section. These signal the domain's stance on LLM training and citation — present-and-permissive correlates with higher AIO citation rates.
   - **If Firecrawl unavailable:** write `AI-protocol files: skipped — Firecrawl not installed.` Don't fall back to WebFetch (it would work for plain text but the integration stays uniform; runtime savings are negligible).

9. **Synthesise** `GEO.md`

## Output format

Create a folder `seo-geo-{target-slug}-{YYYYMMDD}/` with:

```
seo-geo-{target-slug}-{YYYYMMDD}/
├── 01-url-keyword-footprint.md  (URL overview + top keywords)
├── 02-aio-by-keyword.md         (AIO presence + citation per keyword)
├── 03-leaderboards.md           (full leaderboards per keyword)
├── 04-page-passages.md          (extracted passages + citability scores)
├── 05-cited-source-comparison.md (gap vs cited sources)
├── 06-schema-check.md           (JSON-LD audit for GEO-relevant types — requires Firecrawl)
├── 07-ai-protocol-files.md      (llms.txt + RSL status and content — requires Firecrawl)
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
- `Article` (or sub-type) present and valid: {✓/✗ | skipped — Firecrawl required}
- `author` populated with `@type: Person` and `url`: {✓/✗}
- `datePublished` + `dateModified` ISO 8601: {✓/✗}
- `FAQPage` for visible Q&A: {✓/✗/N-A}
- `BreadcrumbList`: {✓/✗}

## AI-protocol files
- `/llms.txt` present: {✓ status 200 / ✗ status {n} / skipped — Firecrawl required}
- `/.well-known/rsl.json` (or `/RSL.txt`) present: {✓ / ✗ / skipped}
- Stance summary: {permissive / restrictive / mixed / unknown — based on declared categories and allow/deny scope}

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
- Cost: ~10–20 SE Ranking credits typical, plus ~3 Firecrawl credits when the extension is installed (1 for target-URL JSON-LD, 2 for AI-protocol files). The skill degrades gracefully without Firecrawl — the schema and AI-protocol sections emit explicit "skipped" notes rather than silently dropping.
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
