# Page-type patterns for SXO classification

These heuristics help classify each top-10 SERP result by page type. Combine signals — no single signal is definitive. Score-of-evidence approach: if 2+ signals point at the same type, classify as that type.

## Page types

### Comparison (head-to-head)
Targets keywords like "X vs Y", "X compared to Y", "X versus Y".
- **URL pattern:** `/x-vs-y/`, `/compare/x-y/`, `/x-or-y/`
- **Title pattern:** contains "vs", "vs.", "or", "compared", "comparison"
- **Schema:** often `Product` (×2) + `BreadcrumbList`
- **Content signals:** side-by-side feature table dominant, balanced verdict, both names in H1, ~70/30 prose-to-table ratio.

### Alternatives / "best X"
Targets keywords like "alternatives to X", "best X for Y", "top 10 X".
- **URL pattern:** `/best-x/`, `/x-alternatives/`, `/top-y/`
- **Title pattern:** starts with a number ("10 best…", "Top 5…") or contains "alternative", "alternatives", "best"
- **Schema:** `ItemList` with embedded `Product`s
- **Content signals:** numbered list 5–15 entries; each entry has a mini-verdict and pros/cons.

### Listicle (informational top-N)
Targets keywords like "things to know about X", "ways to do Y", "tips for Z".
- **URL pattern:** `/n-things/`, `/n-tips/`, `/n-ways/`
- **Title pattern:** starts with number, contains "things", "tips", "ways", "reasons", "examples"
- **Schema:** `Article` or `BlogPosting`
- **Content signals:** numbered or bulleted entries, each with H2, similar length per entry.

### How-to / tutorial
Targets keywords like "how to X", "X tutorial", "guide to X".
- **URL pattern:** `/how-to-x/`, `/tutorial/x/`, `/guide/x/`
- **Title pattern:** starts with "How to", "How do I", contains "tutorial", "guide", "step by step"
- **Schema:** `HowTo` or `Article`
- **Content signals:** numbered steps each with image, optional time-to-complete, prerequisites section.

### Definition / "what is X"
Targets keywords like "what is X", "X meaning", "X definition".
- **URL pattern:** `/what-is-x/`, `/x-definition/`, `/glossary/x/`
- **Title pattern:** starts with "What is", contains "definition", "meaning", "explained"
- **Schema:** `DefinedTerm`, `Article`
- **Content signals:** short definition in first paragraph (passage-citability optimised), then expanded explanation, FAQs, related concepts.

### Product / SaaS landing
Targets the brand name + commercial-intent variations.
- **URL pattern:** `/`, `/products/x/`, `/x/`
- **Title pattern:** brand name + benefit promise
- **Schema:** `Product`, `SoftwareApplication`, `Organization`
- **Content signals:** hero with CTA, social proof, feature blocks, pricing, FAQ, footer CTA.

### Editorial / blog
Targets informational queries with topical depth.
- **URL pattern:** `/blog/x/`, `/articles/x/`, `/insights/x/`, dated `/2026/04/x/`
- **Title pattern:** editorial headline (no template); often ends with "explained" or asks a question
- **Schema:** `Article`, `BlogPosting`, `NewsArticle`
- **Content signals:** byline, publish date, longer-form (1500+ words typical), related articles.

### Forum / community
Targets queries that real users ask in their own words ("X not working", "anyone tried Y").
- **URL pattern:** `reddit.com/r/x/`, `forum.x.com/`, `community.x.com/`, `stackoverflow.com/`
- **Title pattern:** question-form, often grammatically informal
- **Schema:** `QAPage`, `DiscussionForumPosting`
- **Content signals:** original post + comment thread, vote counts, user avatars.

### Video / video-pack
SERPs heavy on video carousels.
- **URL pattern:** `youtube.com/watch?v=`, `vimeo.com/`, `tiktok.com/@/video/`
- **Indicators in SERP:** "Videos" feature card, top results from video platforms.

## Detecting the dominant pattern

A SERP usually has 1–2 dominant patterns. Heuristic:

1. Classify each top-10 result.
2. Count types. If one type is ≥ 6 of 10 → **dominant**.
3. If two types tie at 4–4 → **split intent**; both work; user's choice depends on commercial vs informational angle.
4. Cross-reference with SERP features:
    - **Video carousel present** → expect 2+ Video results.
    - **PAA present** → expect at least 1 informational result.
    - **Shopping pack present** → commercial intent dominant.
    - **AIO present** → informational consensus; passage-citability matters more.

## Edge cases

- **Brand-name SERPs:** the top result is the brand's homepage; rest is press/reviews. Page type for the user's brand: Product/SaaS landing.
- **Local SERPs (with map pack):** treat as a separate pattern — `seo-local-rank-tracking` (planned future skill) is the better diagnostic.
- **News-fresh SERPs:** dominated by editorial/news with date-stamps in titles; treat as Editorial; freshness is the dominant signal.

## Outputs the SXO skill produces from this

For each top-10 result, the page-type label and the signals that triggered it. The user's page is classified the same way and compared. If the dominant pattern is X but the user's page is type Y, the verdict explains the mismatch and proposes a wireframe for type X.
