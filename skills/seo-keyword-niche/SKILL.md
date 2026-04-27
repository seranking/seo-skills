---
name: seo-keyword-niche
description: Mine longtail keywords + question keywords for a topic at scale to surface niche content opportunities. Outputs a content tier plan (template + URL pattern + sample pages + quality gates) suitable for programmatic publishing or steady editorial output. Distinct from `seo-keyword-cluster` (which plans pillar+spoke architecture from broad seeds) — this skill goes deeper into the long tail. Use when the user asks "longtail keywords", "question keywords", "niche content", "content opportunities at scale", "programmatic SEO", "content mining", or "what should I write about for {topic}".
---

# Keyword Niche

Mine the long tail for content opportunities. Pulls longtail variants, question-intent keywords, related keywords, and SERP samples to find under-served niche keywords; clusters them by intent; proposes a content tier (template + URL pattern + sample pages + thin-content quality gates) that can be published programmatically or as a steady editorial cadence.

## Prerequisites

- SE Ranking MCP server connected.
- User provides: a seed topic (e.g. "running shoes", "tax preparation"), or 2–5 seed keywords. Target country (default `us`). Optional: minimum volume threshold (default: 50/mo for niche skill — lower than `seo-keyword-cluster`'s 100), maximum KD (default: 40 for accessibility).

## Process

1. **Validate & preflight**
   - Confirm seeds make sense (not too broad, not branded, not single-letter).
   - `DATA_getCreditBalance` — surface remaining credits. This skill is heavier than most: pulling longtail at depth costs more than pulling head terms.

2. **Longtail expansion** `DATA_getLongTailKeywords`
   - For each seed: pull longtail variants (typically 3+ words, lower individual volume, lower KD).
   - Target: 200–500 longtail candidates per seed.

3. **Question expansion** `DATA_getKeywordQuestions`
   - For each seed: pull question-phrased keywords.
   - These are gold for content mining — explicit user intent in the keyword.

4. **Related expansion** `DATA_getRelatedKeywords` and `DATA_getSimilarKeywords`
   - For each seed: pull related + similar keywords.
   - Catches semantic neighbours that longtail expansion missed.

5. **Filter and clean**
   - Remove keywords below `min_volume` and above `max_kd`.
   - Strip branded keywords the seed-domain doesn't own (unless the user supplied a branded seed).
   - Tag each keyword with detected intent: informational, commercial, transactional, navigational.
   - De-duplicate across seeds.

6. **SERP sample for representative keywords** `DATA_getSerpResults`
   - For 5–10 representative keywords (one per emerging cluster), pull top 10.
   - Identify the dominant page type for each cluster (informs the template proposal in step 8).

7. **Cluster by intent + theme**
   - Group keywords by semantic similarity + intent.
   - Each cluster: name, primary keyword, supporting keywords, total volume, weighted KD, dominant page type.
   - Target 8–20 clusters (more granular than `seo-keyword-cluster`'s 5–12 — this skill is for niche tiers).

8. **Propose a content tier**
   - Template structure: which fields make each page unique. For `{city} apartment rentals`, the template fields are `{city}`, `{neighborhood}`, `{price_range}`, `{property_count}`. For `{tool} alternatives` it's `{tool}`, `{competitor_count}`, `{primary_use_case}`.
   - URL pattern: `/{category}/{slug}/` or `/{topic}/{tool}-alternatives/` etc.
   - Sample pages: 3 fully-spec'd page wireframes for representative cluster keywords.
   - Internal-linking automation: how to link pages within the tier (hub-spoke from a category page, or peer-to-peer for genuinely flat structures).

9. **Quality gates** (anti-thin-content guardrails)
   - **Minimum unique data per page:** template fields must produce ≥ 5 unique attributes (counts, prices, names, dates, etc.). Pages without 5+ unique attributes are duplicates in disguise — skip those keyword variants.
   - **Minimum word count:** 600 words effective content (excludes navigation, footer, boilerplate).
   - **Schema requirement:** every templated page gets `Article` (or relevant type) + `BreadcrumbList`.
   - **Index/noindex split:** if the variant doesn't pass the unique-data threshold, generate the page but `noindex` it.

10. **Synthesise** `KEYWORD-NICHE-PLAN.md`

## Output format

Create a folder `seo-keyword-niche-{target-slug}-{YYYYMMDD}/` with:

```
seo-keyword-niche-{target-slug}-{YYYYMMDD}/
├── 01-seed-expansion.md         (raw expansion per seed)
├── 02-question-keywords.md      (DATA_getKeywordQuestions)
├── 03-filtered-keywords.md      (post min-vol / max-kd filter)
├── 04-cluster-assignment.md     (every keyword and its cluster)
├── 05-serp-samples.md           (top 10 for representative cluster keywords)
├── 06-template-spec.md          (fields, URL pattern, sample pages)
├── 07-quality-gates.md          (thin-content guardrails)
├── keywords.csv                 (all enriched keywords with cluster + intent)
└── KEYWORD-NICHE-PLAN.md        (synthesised plan)
```

`KEYWORD-NICHE-PLAN.md` shape:

```markdown
# Keyword Niche Plan: {topic}

> Generated {YYYY-MM-DD} · Country: {country} · Seeds: {list}

## Inventory
- Longtail keywords mined: {n}
- Question keywords: {n}
- After filter (min-vol {n}, max-kd {n}): {n}
- Clusters formed: {n}
- Estimated combined monthly volume: {n}

## Recommended content tier

### Template
**URL pattern:** `/{category}/{slug}/`

**Required fields per page:**
- `{slug}` — URL-friendly identifier
- `{H1}` — page primary heading
- `{TL;DR}` — first 200 words direct answer
- `{primary_keyword}` — target keyword
- `{related_keywords}` — secondary keywords from cluster
- `{unique_attributes}` — list of ≥ 5 differentiating attributes (numbers, names, dates)
- `{related_pages}` — internal-link list (3–5 sibling pages)
- `{schema_type}` — Article/Product/Other
- `{datestamp}` — last-updated date

**Sample pages:** see `06-template-spec.md` for 3 fully-spec'd wireframes.

## Cluster build order (top 10 by priority)

| Rank | Cluster | Volume (combined) | Weighted KD | Dominant page type | Pages to ship |
|---|---|---|---|---|---|
| 1 | {cluster name} | {n} | {kd} | {type} | {n} |
| ... |

## Quality gates (do not ship pages that fail)

1. **Unique-data threshold:** each page has ≥ 5 unique attributes vs sibling pages in the same cluster.
2. **Minimum word count:** 600 words effective content.
3. **Schema:** `Article` + `BreadcrumbList` (or relevant `@type` for the page).
4. **Internal links:** ≥ 3 outbound to siblings, ≥ 1 inbound from category hub.
5. **Index/noindex:** noindex pages that don't pass the unique-data threshold.

## Scaling estimate
- Clusters: {n}
- Pages per cluster (median): {n}
- Total pages: {n}
- At {pages/week} cadence: {n weeks} to ship the tier.
- Crawl-budget impact (for sites > 10k pages): noindex strategy keeps thin variants out of the index.

## Risks / monitoring
- **Thin-content penalty:** the quality gates above are the guardrail. Audit at scale via `seo-technical-audit` after first 100 pages ship.
- **Index bloat:** monitor in GSC; if newly indexed pages don't accrue impressions in 60 days, candidate for noindex/consolidate.
- **Cannibalization:** monitor with `seo-subdomain` + `seo-page` after first 50 pages.

## Recommended next step
Build a small pilot — 10 pages from the top cluster — before committing to the full tier. Apply quality gates rigorously to the pilot. Re-audit after 60 days; iterate the template based on which pilot pages indexed and ranked.
```

`keywords.csv` columns: `keyword,volume,kd,cpc,intent,cluster,role_in_cluster,dominant_page_type,unique_attributes_estimate`

## Tips

- Respect rate limit: 10 req/sec. Steps 2–4 fan out across all seeds; pace sequentially.
- Cost: ~30–80 credits for 5 seeds, ~150+ for 10–20 seeds. Call `DATA_getCreditBalance` before running and surface the estimate.
- **Programmatic SEO is risky.** Pages that don't pass the unique-data threshold are dead weight at best, penalty bait at worst. The quality gates in step 9 are not optional.
- The pilot recommendation is critical. 10 pages with thoughtful templates outperform 1000 pages of templated mush.
- For e-commerce / inventory-driven content (city pages, product variations), the unique-data threshold is usually easy to hit.
- For "best X for Y" content (where Y has many variants), pick variants that have genuinely distinct content — don't templatise across near-synonyms.
- Pair with `seo-keyword-cluster` for the broader pillar+spoke architecture (this skill complements, not replaces).
- Pair with `seo-content-brief` to expand individual pillar topics into full editor briefs.
- Pair with `seo-technical-audit` after first 100 pages ship to catch any thin-content / canonicalization issues.
- Don't auto-publish. The template, URL pattern, and quality gates ship from this skill; the content authoring + review remains a human responsibility.
