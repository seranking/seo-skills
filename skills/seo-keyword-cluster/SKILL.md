---
name: seo-keyword-cluster
description: Build a content cluster plan from seed keywords: intent-grouped clusters, pillar+spokes architecture with H1/H2 suggestions per spoke, prioritised build order, and an internal-linking map. Plans a content tier across many articles (vs `seo-content-brief` which produces a single article from a topic; vs `seo-page` which audits one existing URL). Use when the user asks for keyword clustering, topical map, pillar content strategy, content cluster plan, or content calendar from a keyword list.
---

# Keyword Cluster

Transform seed keywords into a prioritised cluster plan: each cluster grouped by search intent and theme, with volume totals, a pillar concept, spoke articles, and suggested H1/H2 for each spoke.

## Prerequisites

- SE Ranking MCP server connected.
- User provides: (a) 3 to 20 seed keywords, (b) target market country (default: `us`), and optionally (c) minimum volume threshold (default: 100/mo), (d) maximum KD (default: 60).

## Process

1. **Expand seeds** `DATA_getRelatedKeywords`, `DATA_getSimilarKeywords`, `DATA_getLongTailKeywords`
   - For each seed, pull related + similar + long-tail variants in the target country.
   - Target at least 100 candidate keywords per seed; de-duplicate across seeds.

2. **Question-based expansion** `DATA_getKeywordQuestions`
   - Pull question-intent keywords for the top 5 seeds.
   - These usually become spoke articles with PAA/featured-snippet potential.

3. **Clean and filter**
   - Remove keywords below min volume and above max KD.
   - Strip branded terms the target does not own.
   - Tag each keyword with detected intent: informational, commercial, transactional, navigational.

4. **Cluster by SERP overlap** `DATA_getSerpResults` (or `DATA_getSerpTaskAdvancedResults`)
   - Group keywords by how Google actually ranks them — shared top-10 organic URLs — not by text similarity. Token-overlap clustering manufactures cannibalisation; see `references/serp-overlap-methodology.md` for the full algorithm and anti-pattern callouts.
   - **Budget guard before running.** Compute `estimated_credits = num_candidate_keywords × per_keyword_cost` where `per_keyword_cost = 3` (SERP-standard, default) or `10` (SERP-advanced, only if downstream needs AIO/PAA). Standard is sufficient for clustering. If `estimated_credits > 500`, surface the figure to the user and offer two paths: (a) proceed with SERP-standard, (b) trim the candidate set by raising the min-volume / lowering the max-KD thresholds in step 3 and re-running. If the user already requested SERP-advanced and the estimate exceeds 500, additionally offer SERP-standard as a cheaper fallback.
   - **Fetch SERPs** (one call per unique candidate keyword, cached for the session) — see `references/serp-overlap-methodology.md` § "Caching". Total SERP fetches = number of keywords, not number of pairs.
   - **Pairwise overlap scoring.** For each pair within an intent pre-group (see `references/serp-overlap-methodology.md` § "Pre-Grouping" for the optimisation that avoids full O(N²)), count shared URLs in the top 10 organic. Apply thresholds: 7-10 shared = same post (merge keywords), 4-6 = same cluster, 2-3 = interlink across clusters, 0-1 = separate clusters or exclude.
   - **Form clusters** from the connected components in the 4-6+ overlap graph. Target 5 to 12 clusters. Each cluster gets a name, primary keyword, secondary keywords, total volume, weighted KD.
   - Classify each cluster as pillar-worthy (broad, high volume, informational) or spoke-only (narrow, specific).

5. **Pillar plus spokes architecture**
   - For each pillar cluster, nominate 3 to 7 spoke articles (each one from a sub-cluster or question).
   - For each spoke, draft an H1 and 3 to 5 H2s.
   - Map internal-link structure: pillar links to all spokes, spokes link back to pillar, spokes cross-link where topically adjacent.

6. **Prioritise**
   - Applied **after** clusters are formed via SERP-overlap in step 4 — the formula scores already-grouped clusters, it does not influence which keywords cluster together.
   - Score each cluster: volume (40%) + inverse KD (30%) + commercial intent weighting (30%).
   - Output a prioritised build order.

7. **Quality scorecard** (post-synthesis validation)
   - After `PLAN.md` is written, run a 4-metric quality scorecard against the produced plan and warn the user if any metric fails. Inspired by theirs' post-execution scorecard model — adapted to our cluster-plan output (we score the *plan*, not generated content, since `seo-keyword-cluster` stops at the architecture).
   - **Cannibalisation (zero tolerance).** No two clusters in the plan should share ≥ 40% SERP overlap with each other (computed from the cached SERP matrix in step 4). If two clusters trip this gate, re-merge them and re-run from step 5 onward.
   - **Orphan (zero tolerance).** Every spoke article in the plan must be linked from its pillar in the internal-link map produced in step 5. Any spoke without an inbound link from its pillar is an orphan.
   - **Coverage.** The pillar page in each cluster must cover ≥ 70% of the cluster's high-volume keywords (top half of the cluster by volume) in its primary keyword + secondary keyword set, or via the H2s drafted in step 5. Below 70% means the pillar is too narrow for the cluster it heads.
   - **Anchor diversity.** Across all internal links inside a cluster (pillar↔spoke + spoke↔spoke), no single anchor text should be used > 40% of the time. Concentration above 40% is an over-optimisation signal.
   - **Output.** If all four metrics pass, append a single line to `PLAN.md` under "## Quality scorecard": `All gates passed (cannibalisation/orphan/coverage/anchor-diversity).` If **any** metric fails, append a "## Quality scorecard" section to `PLAN.md` with red/yellow/green rows for each metric (red = fail, yellow = within 10% of threshold, green = pass), and annotate the verdict header at the top of `PLAN.md` with `(needs review — N quality-gate failures)`. Also write the same scorecard verbatim to `06-quality-scorecard.md` in the output folder so it's auditable independently.

## Output format

Create a folder `seo-keyword-cluster-{target-slug}-{YYYYMMDD}/` with:

```
seo-keyword-cluster-{target-slug}-{YYYYMMDD}/
├── 01-seed-expansion.md
├── 02-filtered-keywords.md
├── 03-cluster-assignment.md      (SERP overlap matrix + cluster groupings)
├── 06-quality-scorecard.md       (evidence) — 4-metric gate result; written every run
├── keywords.csv
└── PLAN.md
```

`PLAN.md` follows this shape:

```markdown
# Cluster Plan: {topic} {(needs review — N quality-gate failures) if step 7 flagged any}
Market: {country}
Seeds: {seed list}

## Summary
- Keywords analysed: {n}
- Clusters formed: {n}
- Estimated combined monthly volume: {n}
- Pillars: {n}, spokes: {n}
- Clustering method: SERP-overlap top-10 (mode: {standard | advanced}, ~{credits} credits)

## Build order

### Cluster 1: {cluster name} [PILLAR]
- Primary keyword: {kw} ({volume}/mo, KD {kd})
- Secondary: {list}
- Total volume: {n}/mo
- Priority score: {n}

#### Pillar page
- H1: {H1}
- H2s: {list}

#### Spoke articles
1. **{spoke title}**
   - H1: {H1}
   - H2s: {list}
   - Target keyword: {kw} ({volume})
2. **{spoke title}** ...

### Cluster 2: {cluster name} [SPOKE-ONLY]
...

## Internal linking map
- Pillar A links to: spokes A1, A2, A3
- Spoke A1 links back to: pillar A, and cross-links to spoke B2 (topical overlap)
...

## Quality scorecard
{If all four gates pass:}
All gates passed (cannibalisation/orphan/coverage/anchor-diversity).

{If any fail, render this table instead:}
| Gate | Status | Detail |
|---|---|---|
| Cannibalisation (no two clusters ≥40% SERP overlap) | RED / YELLOW / GREEN | {detail} |
| Orphan (every spoke linked from its pillar) | RED / YELLOW / GREEN | {detail} |
| Coverage (pillar covers ≥70% of cluster's high-volume keywords) | RED / YELLOW / GREEN | {detail} |
| Anchor diversity (no anchor used >40% of internal links per cluster) | RED / YELLOW / GREEN | {detail} |

## Raw data
- keywords.csv: full enriched keyword list
- 03-cluster-assignment.md: every keyword and its cluster (incl. SERP overlap matrix)
- 06-quality-scorecard.md: standalone copy of the scorecard above (evidence)
```

`keywords.csv` columns:
`keyword,volume,kd,cpc,intent,cluster,role_in_cluster`

## Tips

- Respect Data API rate limit: 10 requests per second. With 20 seeds and 3 expansion endpoints, this is ~60 calls; pace sequentially.
- Call `DATA_getCreditBalance` before running. The dominant cost driver is now the SERP-overlap pass in step 4: ≈ 3 credits per candidate keyword in SERP-standard mode (default), ≈ 10 credits in SERP-advanced. A typical 40-keyword candidate set is ≈ 120 credits standard / ≈ 400 credits advanced. Step 4's budget guard surfaces this estimate to the user before fetching any SERPs and offers a cheaper-fallback path if the estimate exceeds 500 credits.
- Do not lump different intents into the same cluster even if the keywords are semantically similar. "Best X" (commercial) and "What is X" (informational) deserve separate content.
- Pillar pages fail when they try to rank for too narrow a query. The primary keyword of a pillar cluster should have volume > 1,000/mo and be broad enough to justify a 3,000+ word article.
- The priority score is a starting point, not a mandate. Ask the user to review the top 3 clusters before committing a quarter of content.
- **Cluster merging is now SERP-driven, not text-driven.** If two clusters share ≥ 40% SERP overlap with each other, the step-7 cannibalisation gate flags them — re-merge those clusters and re-run from step 5.
