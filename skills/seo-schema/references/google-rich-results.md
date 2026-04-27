# Google Rich Results — supported types and requirements

> **Last reviewed: 2026-04-27.** Google updates supported types and requirements regularly. This file is a guide, not authoritative. Verify in [Google's Rich Results Test](https://search.google.com/test/rich-results) and the [Search Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery).

## Supported types (April 2026)

| Schema.org type | When to use | Template |
|---|---|---|
| `Article` / `NewsArticle` / `BlogPosting` | Editorial content with an author | `templates/article.json` |
| `Product` (with `Offer`) | E-commerce product page | `templates/product.json` |
| `LocalBusiness` (and subtypes like `Restaurant`, `Dentist`) | Brick-and-mortar landing page | `templates/local-business.json` |
| `FAQPage` | Page with explicit Q&A blocks (not inline questions) | `templates/faq-page.json` |
| `HowTo` | Step-by-step instructions | `templates/how-to.json` |
| `BreadcrumbList` | Most pages with breadcrumb navigation | `templates/breadcrumb-list.json` |
| `VideoObject` | Pages embedding video content | (template not bundled — see Google docs) |
| `Recipe` | Cooking recipes | (template not bundled) |
| `Event` | Time-bound events | (template not bundled) |

## Required vs recommended (highlights)

### Article / NewsArticle / BlogPosting
- **Required:** `headline`, `image`, `datePublished`
- **Recommended:** `author` (with `@type: Person` and `url`), `dateModified`, `publisher` (with logo `ImageObject`), `mainEntityOfPage`
- **Common errors:** `headline` over 110 chars; missing `image` or image too small (min 1200×800 for max coverage); `author` as plain string instead of `@type: Person`.

### Product
- **Required:** `name`, `image`, `offers` (with `price`, `priceCurrency`, `availability`)
- **Recommended:** `aggregateRating`, `review`, `sku`, `brand`, `gtin`/`mpn`
- **Common errors:** `price` as a number instead of string; `availability` as plain text instead of schema.org URL (`https://schema.org/InStock`).

### LocalBusiness
- **Required:** `name`, `address` (full `PostalAddress`), `telephone` OR `url`
- **Recommended:** `geo`, `openingHoursSpecification`, `priceRange`, `image`, `aggregateRating`
- **Common errors:** `telephone` not in international format (must include country code, no spaces in JSON-LD); `address` as plain string instead of `@type: PostalAddress`.

### FAQPage
- **Required:** `mainEntity` array of `Question` objects, each with `name` and `acceptedAnswer.text`
- **Common errors:** marking up FAQs that aren't visibly Q&A on the page; using `Question` for content that is just an H2 + paragraph.
- ⚠ **Note (2024–2026):** Google has significantly reduced FAQ rich-result eligibility — most sites no longer get FAQ rich results in SERPs. Apply this schema only to pages that are unambiguously Q&A (e.g., dedicated FAQ pages).

### HowTo
- **Required:** `name`, `step` array (each with `name` and `text`)
- **Recommended:** `totalTime`, `image` per step, `supply`, `tool`, `estimatedCost`
- ⚠ **Note (2024–2026):** Google has removed HowTo rich results for non-cooking content on desktop. Currently effective only on mobile and primarily for recipe/cooking content.

### BreadcrumbList
- **Required:** `itemListElement` array (each with `position`, `name`, `item`)
- **Recommended:** include the canonical absolute URL in each `item`.
- **Note:** highly reliable rich result; most pages with breadcrumbs benefit.

## Validation checklist (apply after generating)

1. `@context` is exactly `https://schema.org` (lowercase, no trailing slash).
2. `@type` matches one of the supported types above (case-sensitive).
3. All URLs are **absolute**, not relative.
4. Dates are ISO 8601 (`2026-04-27` or `2026-04-27T10:30:00+00:00`).
5. The JSON parses cleanly (no trailing commas, balanced braces).
6. The `<script type="application/ld+json">` block is in `<head>` or top of `<body>`.
7. The structured data describes content **actually visible on the page**. Google penalises hidden-content schema.

## When to skip generating

- The page is a generic "kitchen sink" page that doesn't fit a single intent — generating speculative schema usually hurts.
- The content is JS-rendered and the team doesn't server-side render — schema in client-only JS is often missed by crawlers.
- The site is a low-trust domain Google has already penalised — schema doesn't unlock rich results until the trust signals improve.
