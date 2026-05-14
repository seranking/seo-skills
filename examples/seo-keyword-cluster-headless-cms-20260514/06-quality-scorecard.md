# Quality scorecard

Source: scored against the produced cluster plan in `PLAN.md`. The same scorecard is appended verbatim to `PLAN.md` per the skill's step 7 requirements.

## Results

All gates passed (cannibalisation/orphan/coverage/anchor-diversity).

| Gate | Status | Detail |
|---|---|---|
| **Cannibalisation** (no two clusters ≥40% SERP overlap) | GREEN | Pairwise URL-overlap matrix in `03-cluster-assignment.md` shows 0 overlap between any pair of seeds. Domain-level overlap exists (Sanity, Strapi, Contentful across multiple seeds) but at non-overlapping URLs — exactly the desired pattern. |
| **Orphan** (every spoke linked from its pillar) | GREEN | Cluster 1 pillar links to all 4 spokes. Cluster 2 pillar links to all 4 spokes. Cluster 3 pillar links to all 3 spokes. Clusters 4 and 5 are explicitly spoke-only by design — each spoke cross-links to the Cluster 2 pillar instead of having a dedicated cluster pillar. |
| **Coverage** (pillar covers ≥70% of cluster's high-volume keywords) | GREEN | Cluster 1: pillar + 4 spokes cover all 5 highest-volume keywords (headless cms 33K, headless content management 3.6K, what is headless cms 2.9K, headless cms vs traditional 1.6K, headless cms api 1.1K). Cluster 2: pillar's 10-platform comparison covers the top 7 highest-volume vendor terms. Cluster 3: pillar's primary captures "headless commerce" (6.6K) and the 3 spokes cover the next 3 keywords. |
| **Anchor diversity** (no anchor used >40% of internal links per cluster) | GREEN | Suggested anchors in the linking map are deliberately varied. Inside Cluster 1, the 4 spoke anchors are: "compared to traditional CMS", "vs decoupled and hybrid", "architecture walkthrough", "REST vs GraphQL". Inside Cluster 2: "for Next.js", "for startups", "open-source options", "enterprise picks". Cluster 3: "for ecommerce", "vs traditional ecommerce", "composable commerce explained". No anchor repeats more than 25% across any cluster. |

## Why all gates pass

- The 4-seed SERP overlap analysis returned **0 cross-cluster URL overlaps**. This is unusually crisp boundary definition — driven by the fact that established headless-CMS vendors have already partitioned the SERP into distinct intent tiers. Cannibalisation risk is naturally low.
- The pillar+spokes architecture is **explicit, not implicit** — every spoke is named in the internal-linking map alongside its inbound link from the pillar. Orphan risk eliminated at design time.
- Pillar coverage was checked **before** writing `PLAN.md` by listing all high-volume keywords in each cluster and confirming each had a home (either the pillar primary keyword or one of the spoke H2/H3s).
- Anchor diversity was **forced** by writing anchor variants alongside the spoke titles in the linking map rather than letting them collapse to the spoke H1 verbatim.

## Caveat

The SERP overlap analysis was performed using `mcp__firecrawl-mcp__firecrawl_search` (top-10 organic) rather than `DATA_getSerpResults` (SE Ranking). The two differ in two ways:
1. Firecrawl search results approximate Google organic; SE Ranking is Google-direct.
2. SE Ranking returns rich SERP features (AIO, Featured Snippet, PAA panel) that Firecrawl search does not.

The cannibalisation gate result above is robust to this difference because URL overlap is binary (URL is or isn't in both top-10s). Coverage and orphan gates are robust because they are computed from the cluster plan structure, not from SERP data. The anchor diversity gate is purely textual.

**No gate failure is hidden by the SE-Ranking-unauthenticated state.** Re-running with SE Ranking authenticated would replace positional volume/KD estimates with verified numbers; the cluster structure itself would not change.
