# 06 — Template spec

Three template variants serve the 12 clusters. Each variant has its own field set, URL pattern, schema requirement, and quality bar.

## Variant A: Single-product review

**Use for:** Cluster 3 (single-product reviews) — e.g. "breville barista express review".

**URL pattern:** `/espresso-machines/{slug}-review/` (e.g. `/espresso-machines/breville-barista-express-review/`)

**Fields (in render order):**

| Field | Required | Source | Quality bar |
|---|---|---|---|
| `H1` | Yes | "{Product Name} Review" | Match the primary keyword closely without being a slug. |
| `Author byline + expertise statement` | Yes | Editor / writer profile | Must establish coffee-domain credibility (years in the niche, certifications, café experience). |
| `Last-updated date` | Yes | CMS | Refresh quarterly; surface the date prominently. |
| `Hero photo` | Yes | First-hand photo, not manufacturer-supplied | This is the single highest-leverage E-E-A-T signal. No stock images. |
| `TL;DR verdict (≤ 200 words)` | Yes | Reviewer | Direct answer to "should I buy this?" tied to a specific persona. |
| `Specs table` | Yes | Manufacturer + reviewer-measured | Include MSRP, street price, type, boiler, pressure, grinder built-in, weight, dimensions, watts. |
| `Pros (≥ 4)` | Yes | Reviewer | Each pro tied to a measurable feature, not vague ("looks nice" disqualifies). |
| `Cons (≥ 3)` | Yes | Reviewer | Each con tied to a measurable trade-off ("65-ounce reservoir is small for households >2 people"). |
| `In-use observations` | Yes | Reviewer | A paragraph or two demonstrating the reviewer used the machine. Steam-wand behaviour, shot-pull consistency, descale frequency, etc. |
| `Comparison block` | Yes | Editorial | 2–3 sibling machines this one competes with, each with a link to the sibling's review or to the relevant comparison page. |
| `Verdict by persona` | Yes | Reviewer | "Best for beginner / home / pro-am" call, with reasoning. |
| `Internal links` | Yes | Linking automation | ≥ 3 to siblings (related reviews, comparison pages, buyer guide), ≥ 1 to category hub. |
| `Schema` | Yes | CMS template | `Product` + `Review` + `BreadcrumbList` + `Person` (for author) + `Organization` (for publisher). |

**Schema example (paste-ready when integrated with real product data):**

```jsonc
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{Product Name}",
  "image": "{first-hand photo URL}",
  "brand": {"@type": "Brand", "name": "{Brand}"},
  "review": {
    "@type": "Review",
    "reviewRating": {"@type": "Rating", "ratingValue": "{0-5}", "bestRating": "5"},
    "author": {"@type": "Person", "name": "{Author}", "url": "{author bio URL}"},
    "datePublished": "{ISO 8601}",
    "reviewBody": "{TL;DR + key in-use observation, 200-400 chars}"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "{MSRP}",
    "availability": "https://schema.org/InStock"
  }
}
```

## Variant B: Multi-product listicle

**Use for:** Clusters 1, 2, 4, 6, 9, 10, 11, 12 (price-band, use-case, by-feature, style, accessories, skill-level, by-manufacturer, commercial).

**URL pattern:** `/espresso-machines/best-{category}/` (e.g. `/espresso-machines/best-under-500/`, `/espresso-machines/best-for-beginners/`)

**Fields:**

| Field | Required | Notes |
|---|---|---|
| `H1` | Yes | "Best {category} of {current year}" |
| `Author + updated date` | Yes | Same as Variant A |
| `TL;DR + methodology` | Yes | 200 words on how the picks were chosen (criteria, machines tested, qualitative rubric). This block IS the differentiator vs affiliate-spam listicles. |
| `Comparison table` | Yes | Sortable / responsive. Columns: Machine, Type, Price, Best for, Rating, "Read full review →". |
| `Per-pick deep-dive` (5–10 picks) | Yes | Each pick: photo + 200-word summary + pros/cons + link to dedicated review. |
| `Honourable mentions` (3) | Recommended | Machines that didn't make the cut and why. |
| `Buyer's guide` | Recommended | Inline mini-guide tying into the relevant Variant C standalone guide. |
| `Schema` | Yes | `ItemList` (each item = `Product` with embedded `Review`) + `BreadcrumbList`. |

## Variant C: Buyer guide / informational

**Use for:** Cluster 7 (buyer guides) and Cluster 8 (maintenance & troubleshooting).

**URL pattern:** `/espresso-machines/guide/{slug}/` (e.g. `/espresso-machines/guide/how-to-choose/`) or `/espresso-machines/maintenance/{slug}/`

**Fields:**

| Field | Required | Notes |
|---|---|---|
| `H1` | Yes | Direct question or topic |
| `TL;DR` | Yes | 50–100-word direct answer in the first paragraph (high citability for AI Overviews). |
| `H2-shaped questions` | Yes | Each H2 is the question shape ("What does PID do?"); first paragraph after each H2 is the definitive answer. |
| `Internal links to relevant reviews + listicles` | Yes | This is the funnel-deepening surface. |
| `Schema` | Yes | `Article` (for guides) or `FAQPage` if the guide has 5+ visible Q&A pairs with definitive answers. (No `HowTo` — Google retired the rich result in 2023.) |

## Sample wireframes

Three fully-spec'd wireframes (would be ~200 lines each) live in `evidence/wireframe-{a,b,c}.md` in a production run. For this example, the field tables above are sufficient — they map 1:1 to the wireframes.
