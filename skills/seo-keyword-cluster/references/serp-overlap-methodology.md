# SERP Overlap Methodology

> Adapted from `AgriciDaniel/claude-seo`'s `seo-cluster/references/serp-overlap-methodology.md` (MIT). Input source swapped from theirs' WebSearch top-10 scrape to our SE Ranking `DATA_getSerpResults` MCP call so the SERP we cluster on is the same dataset every other skill in this catalogue uses.

## Core Principle

Two keywords that return the same Google results should be targeted by the same page.
Two keywords that return completely different results need separate pages. This is the
foundation of SERP-based clustering — using Google's own ranking decisions to determine
content architecture rather than relying on keyword text similarity or stemming.

## Scoring Algorithm

### Step 1: Collect SERP Data

For each keyword in the candidate set, retrieve the top 10 organic results via
`DATA_getSerpResults` (SE Ranking MCP):

- Pass the keyword + target country (`source` param maps to the SE Ranking SERP database, e.g. `us`, `uk`, `de`).
- Default to **SERP-standard mode** (`result_type=standard`) — organic top-10 only, ≈ 3 credits per keyword.
- Use **SERP-advanced mode** (`result_type=advanced` via `DATA_getSerpTaskAdvancedResults`, ≈ 10 credits per keyword) only if the cluster plan also needs SERP features (AIO presence, PAA, video carousels). For pure clustering, standard is sufficient.
- Extract only organic result URLs (ignore ads, featured snippets, PAA, knowledge panels).
- Normalize URLs: strip protocol, trailing slash, and query parameters (except meaningful ones like `?id=` for product pages).
- Store as a set of 10 URLs per keyword.

### Step 2: Pairwise Comparison

For each pair of keywords (A, B):
1. Retrieve the URL sets: `urls_A` and `urls_B`.
2. Compute overlap: `shared = urls_A intersection urls_B`.
3. Score: `overlap_score = len(shared)`.

### Step 3: Apply Thresholds

| Overlap Score | Relationship | Action |
|--------------|-------------|--------|
| 7-10 | **Same post** | Merge keywords into one target page. Use higher-volume keyword as primary. |
| 4-6 | **Same cluster** | Place in same spoke cluster. May be separate posts or same post depending on volume difference. |
| 2-3 | **Interlink** | Place in adjacent clusters. Create cross-cluster internal links. |
| 0-1 | **Separate** | Different clusters entirely or exclude from current pillar topic. |

### Step 4: Handle Ambiguous Scores (3-4 Range)

Scores in the 3-4 range require tiebreaking:
1. Check domain overlap (same domains but different pages = closer relationship).
2. Check intent alignment (same intent category = lean toward same cluster).
3. Check volume ratio (if one keyword has 10x+ more volume, it likely deserves its own post).
4. When in doubt, keep in same cluster with separate posts (err toward cohesion).

## Optimization Strategy

Full pairwise comparison of N keywords requires N*(N-1)/2 SERP fetches. For 40
keywords, that is 780 comparisons — at ≈ 3 credits per fetch (standard mode) and
40 unique fetches (each keyword's SERP only fetched once and cached, see § Caching),
the actual budget is **≈ 120 credits for the SERP pulls**, plus the in-memory pairwise
overlap math (free). Optimize further by reducing unnecessary checks:

### Pre-Grouping

1. Classify all keywords by intent (Informational, Commercial, Transactional).
2. Group keywords that share the same head term (e.g., "CRM software" variants).
3. Only run pairwise SERP comparison within pre-groups.
4. Cross-check boundary keywords (highest volume in each group) across groups.

### Skip Rules

- If keywords A and B are both long-tail variants of the same head term AND share
  the same intent, assume overlap 4-6 (same cluster) without checking SERP.
- If keywords are in different intent categories, assume overlap 0-2 unless they
  share a head term.
- Verify assumptions with spot-check SERP comparisons (sample 20% of skipped pairs).

## Scoring Matrix Format

Store the overlap data as a symmetric matrix in `03-cluster-assignment.md` (or as
JSON in an evidence dump if more than ~30 keywords):

```json
{
  "serp_matrix": {
    "keywords": ["keyword-a", "keyword-b", "keyword-c"],
    "scores": [
      [10, 5, 1],
      [5, 10, 3],
      [1, 3, 10]
    ]
  }
}
```

Diagonal is always 10 (a keyword overlaps perfectly with itself).

## Anti-Patterns

1. **Never cluster by text similarity alone.** "Dog training tips" and "dog training
   classes" may have completely different SERPs despite similar text. This is the
   2019-era methodology and it manufactures cannibalisation when shipped today.
2. **Never use stemming-only grouping.** "Run" and "running" may target different
   intents entirely.
3. **Never assume related searches belong in the same cluster.** Verify with SERP data.
4. **Never ignore SERP feature differences.** If keyword A triggers a local pack and
   keyword B triggers a featured snippet, they likely need different content types
   even with moderate URL overlap. (SERP-advanced mode is required to see this — the
   standard `DATA_getSerpResults` call returns organic only.)
5. **Never treat all domains equally.** Wikipedia and Reddit appear in many SERPs.
   Consider filtering out ubiquitous domains (top 5 most common) before scoring, or
   weighting domain-specific results higher.

## Data Source Priority

1. **`DATA_getSerpResults` (standard mode, default)** — organic top-10 only, ≈ 3 credits
   per keyword. Sufficient for clustering. Pass the target country as `source`.
2. **`DATA_getSerpTaskAdvancedResults` (advanced mode)** — organic + SERP features,
   ≈ 10 credits per keyword. Use only if the cluster plan downstream wants AIO/PAA
   data per keyword (e.g. you intend to also feed the keyword set into `seo-geo` or
   `seo-sxo`). Otherwise the extra cost is wasted on a clustering pass.

## Caching

Within a single clustering session, cache all SERP results. If keyword A's results
are fetched for the A-B comparison, reuse them for the A-C, A-D, ..., A-N comparisons.
This means each keyword's SERP is fetched **exactly once** regardless of how many
pairs it participates in — total SERP fetches = N (number of keywords), not
N*(N-1)/2 (number of pairs). Persist the cache to the skill's evidence folder for the run
so a re-run on the same keyword set within the same day reuses the result.
