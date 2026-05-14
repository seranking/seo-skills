# 01 — Detected schema

> Source: `mcp__firecrawl-mcp__firecrawl_scrape(url="https://www.budgetbytes.com/slow-cooker-chicken-noodle-soup", formats=["rawHtml"], onlyMainContent=false)` on 2026-05-14.

## Inventory

- `<script type="application/ld+json">` blocks: **1**
- That block contains an `@graph` with **8 interlinked entities**.
- Microdata (`itemscope` / `itemprop`): not detected on this page (the WPRM plugin emits JSON-LD exclusively).
- RDFa (`typeof` / `property`): not detected.

## The single `@graph` block, item-by-item

### 1. Article

```jsonc
{
  "@type": "Article",
  "headline": "Slow Cooker Chicken Noodle Soup",
  "author": {"name": "Beth Moncel", "@id": "https://www.budgetbytes.com/#/schema/person/de533a4dad507aefcf8ea04e131701f9"},
  "publisher": {"@id": "https://www.budgetbytes.com/#organization"},
  "datePublished": "2020-01-16T15:43:21+00:00",
  "dateModified": "2025-09-06T00:44:55+00:00",
  "image": "...", "articleSection": "...", "keywords": "...",
  "commentCount": "...", "wordCount": "..."
}
```

Status: valid. All required + recommended fields populated.

### 2. WebPage

Fields: breadcrumb, datePublished, dateModified, description, image, inLanguage, isPartOf, name, potentialAction, primaryImageOfPage, thumbnailUrl, url.

Status: valid.

### 3. ImageObject

Fields: caption, contentUrl, height, width, inLanguage, url. Pulled out as a separate entity in the graph (referenced by the Recipe).

### 4. BreadcrumbList

Fields: itemListElement (an array of position-aware ListItems). The breadcrumb chain links Home → Slow Cooker Recipes → Slow Cooker Chicken Noodle Soup.

### 5. WebSite

Fields: description, inLanguage, name, potentialAction (SearchAction for site search), publisher, url. The SearchAction allows `sitelinks searchbox` rich-result eligibility.

### 6. Organization

```jsonc
{
  "@type": "Organization",
  "name": "Budget Bytes",
  "url": "https://www.budgetbytes.com/",
  "logo": {"@type": "ImageObject", "url": "...", "width": 300, "height": 300, "caption": "Budget Bytes"},
  "sameAs": [
    "https://www.facebook.com/budgetbytes1/?ref=hl",
    "https://x.com/Budget_Bytes",
    "https://instagram.com/budgetbytes/",
    "https://www.pinterest.com/budgetbytes/",
    "https://www.youtube.com/channel/UC17vdVOZBVxTSDcldUBBlRg"
  ]
}
```

Status: valid. 5 social `sameAs` entries — strong entity-disambiguation signal.

### 7. Person

```jsonc
{
  "@type": "Person",
  "name": "Beth Moncel",
  "description": "I'm a food lover, number cruncher, and meticulous budgeter. I love science and art, and the way they come together when I cook. ...",
  "url": "https://www.budgetbytes.com/author/beth/",
  "sameAs": [
    "https://www.budgetbytes.com/about/",
    "https://www.facebook.com/budgetbytes1",
    "https://x.com/Budget_Bytes"
  ]
}
```

Status: valid. 160+ char bio, dedicated author page, 3 sameAs entries — strong E-E-A-T anchor.

### 8. Recipe

```jsonc
{
  "@type": "Recipe",
  "name": "Slow Cooker Chicken Noodle Soup",
  "author": {"@id": "https://www.budgetbytes.com/#/schema/person/de533a4dad507aefcf8ea04e131701f9"},
  "description": "Slow cooker chicken noodle soup is an incredibly easy and soothing winter recipe ...",
  "datePublished": "2020-01-16T10:43:21+00:00",
  // dateModified: MISSING
  "image": ["...x4 sizes..."],
  "video": {"@type": "VideoObject", "uploadDate": "2025-08-30T03:00:45+00:00", "duration": "PT59S", "contentUrl": "https://www.youtube.com/watch?v=cNh2FbIUV44", "...": "..."},
  "recipeYield": ["8", "8 1.5 cups each"],
  "prepTime": "PT30M", "cookTime": "PT240M", "totalTime": "PT270M",
  "recipeIngredient": ["1 yellow onion ($0.32)", "..."],   // 14 entries
  "recipeInstructions": [{"@type": "HowToStep", "text": "Dice the onion...", "...": "..."}, ...],   // 6 steps
  "nutrition": {"@type": "NutritionInformation", "servingSize": "1.5 cups", "calories": "235.2 kcal", "carbohydrateContent": "20.9 g", "proteinContent": "27.6 g", "fatContent": "4.1 g", "sodiumContent": "1349.6 mg", "fiberContent": "2.5 g"},
  "recipeCategory": ["Dinner", "Lunch", "Main Course", "Soup"],
  "recipeCuisine": ["American"],
  "keywords": "Chicken Soup, Easy Recipe, Slow Cooker Soup",
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.23", "ratingCount": "45", "reviewCount": "13"},
  "review": [
    {"@type": "Review", "reviewRating": {"@type": "Rating", "ratingValue": "4"}, "reviewBody": "I made it twice now...", "author": {"@type": "Person", "name": "Brian Tinker"}, "datePublished": "2026-03-29"},
    // ...12 more reviews
  ]
}
```

Status: valid (one soft warning — Recipe-level `dateModified` not echoed from Article).

## Graph-quality observations

- All cross-references use `@id` — minimal duplication.
- Single `<script>` block — most Recipe sites emit 3–5 separate blocks (one per type); the @graph approach is cleaner.
- `Person` and `Organization` are *first-class entities* in the graph, not nested in `Article.author` / `Article.publisher`. That's the modern best practice.
- WPRM (WP Recipe Maker plugin) is the likely generator — explains the consistent quality.
