# Schema Markup: budgetbytes.com/slow-cooker-chicken-noodle-soup

> Snapshot dated 2026-05-14 · Page snapshot pulled via Firecrawl `formats: ["rawHtml"]`
> Numbers will drift — re-run the skill for current data.

## Verdict

**Schema is in excellent shape. Only one paste-ready addition recommended (`HowTo` is intentionally skipped).** This is a textbook example of how a food publisher should structure JSON-LD: a single `<script type="application/ld+json">` block emitting an `@graph` with **8 interlinked entities** (`Article`, `WebPage`, `ImageObject`, `BreadcrumbList`, `WebSite`, `Organization`, `Person`, `Recipe`), all using `@id` references so the graph compresses cleanly. Required Recipe fields are all populated, including `aggregateRating` (4.23 / 45 ratings) and 13 user reviews — both strong rich-result signals.

The recipe markup is so complete that the validation pass below has only one soft warning (Recipe missing `dateModified` — present on the parent `Article` but not echoed onto `Recipe`). The recommended addition is `Speakable` schema for the recipe summary paragraph — a forward-looking, low-effort add that opens voice-search surfaces.

## Currently present

| @type | Status | Notes |
|---|---|---|
| `Article` | valid | full set: author, publisher, datePublished 2020-01-16, dateModified 2025-09-06, headline, image, articleSection, keywords, commentCount, wordCount |
| `WebPage` | valid | breadcrumb-linked, has primaryImageOfPage, datePublished + dateModified |
| `ImageObject` | valid | contentUrl, height, width, caption, inLanguage |
| `BreadcrumbList` | valid | itemListElement with position-aware ListItems |
| `WebSite` | valid | name, url, description, potentialAction (SearchAction) |
| `Organization` | valid | name "Budget Bytes", logo (ImageObject 300×300), 5 sameAs social links (Facebook, X, Instagram, Pinterest, YouTube) |
| `Person` | valid | name "Beth Moncel", description (160+ chars), url, 3 sameAs links — strong E-E-A-T author signal |
| `Recipe` | valid (soft warn) | name, author @id-ref, datePublished, image (4 sizes), video (YouTube VideoObject with uploadDate, duration PT59S, contentUrl), recipeYield, prepTime PT30M, cookTime PT240M, totalTime PT270M, 14 ingredients, 6 HowToStep instructions, nutrition (NutritionInformation, 7 fields), recipeCategory ['Dinner', 'Lunch', 'Main Course', 'Soup'], recipeCuisine ['American'], keywords, aggregateRating (4.23 of 45 ratings, 13 reviewCount), 13 Review items with reviewBody + author + datePublished |

## Validation against Google Rich Results spec

### Recipe (the most rich-result-eligible block)

| Field | Required? | Present | Notes |
|---|---|---|---|
| `@type` | required | Recipe | |
| `name` | required | "Slow Cooker Chicken Noodle Soup" | |
| `image` | required | 4 image variants (1200×?, 500×500, 500×375, 480×270) | Google asks for one image ≥ 1200×1200; the first appears to satisfy. Worth confirming dimensions in CMS. |
| `author` | recommended | @id-ref to Person "Beth Moncel" | E-E-A-T anchor — Person entity in same graph has description + url + sameAs |
| `datePublished` | recommended | 2020-01-16T10:43:21+00:00 | ISO 8601 ✓ |
| `dateModified` | recommended | **MISSING on Recipe** | Present on parent Article (2025-09-06); echo onto Recipe for completeness |
| `description` | recommended | present | |
| `recipeIngredient` | recommended | 14 entries | |
| `recipeInstructions` | recommended | 6 HowToStep with text + url anchors | |
| `prepTime` / `cookTime` / `totalTime` | recommended | PT30M / PT240M / PT270M | All ISO 8601 duration ✓ |
| `recipeYield` | recommended | ["8", "8 1.5 cups each"] | |
| `recipeCategory` / `recipeCuisine` | recommended | ['Dinner', 'Lunch', 'Main Course', 'Soup'] / ['American'] | |
| `nutrition` | recommended | NutritionInformation: 235.2 kcal, carb/protein/fat/sodium/fiber | |
| `aggregateRating` | recommended | 4.23 (45 ratings, 13 reviewCount) | Strong rich-result signal |
| `review` | recommended | 13 Review items | |
| `video` | recommended | VideoObject (YouTube, 59s, dated 2025-08-30) | |
| `suitableForDiet` | recommended | MISSING | Optional, only add if accurate |

**Verdict:** Recipe block is rich-result-eligible *today*. The only soft fix is echoing `dateModified` onto `Recipe` (currently only on `Article`).

### Article

All required + recommended fields populated. No fixes needed.

### Organization

Logo `ImageObject` properly nested. `sameAs` covers 5 social profiles. No fixes.

## Recommended additions

### 1. `Speakable` specification on the recipe description (low-effort, forward-looking)

Voice-search surfaces (Google Assistant, Alexa) preferentially read passages marked with `speakable`. The recipe's intro paragraph is a natural fit — a 1–2 sentence what-this-is-and-why-it's-good summary.

**Effort:** 1 line of JSON-LD added to the existing graph. No new `<script>` tag needed.

### 2. (Optional) `MainEntity` self-reference on `WebPage`

Currently `WebPage` has `primaryImageOfPage` but no `mainEntity` pointer to the `Recipe`. Adding `"mainEntity": {"@id": "https://www.budgetbytes.com/slow-cooker-chicken-noodle-soup/#recipe"}` strengthens the graph and helps Google identify the primary content type unambiguously.

**Effort:** 1 line. Low priority — Google generally infers correctly already.

### 3. (Skipped) `HowTo`

Google retired `HowTo` rich results in September 2023. The `recipeInstructions` array already uses `HowToStep` types — that's the correct surface for instructions within Recipe. No standalone `HowTo` block recommended.

## Paste-ready additions

### Echo `dateModified` onto Recipe

Update the existing Recipe block by adding one line:

```json
{
  "@type": "Recipe",
  "name": "Slow Cooker Chicken Noodle Soup",
  "datePublished": "2020-01-16T10:43:21+00:00",
  "dateModified": "2025-09-06T00:44:55+00:00",
  // ... rest of existing Recipe ...
}
```

### Add Speakable spec on Recipe description

```json
{
  "@type": "Recipe",
  // ... existing Recipe fields ...
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".wprm-recipe-summary"]
  }
}
```

(Update the CSS selector to match the actual class in the recipe template.)

### Add MainEntity pointer on WebPage

```json
{
  "@type": "WebPage",
  // ... existing fields ...
  "mainEntity": {"@id": "https://www.budgetbytes.com/slow-cooker-chicken-noodle-soup/#recipe"}
}
```

(Confirm the `@id` value matches the Recipe's `@id` in the existing graph.)

## Validation pass

- All currently-present JSON-LD parses cleanly ✓
- 0 `{REPLACE: ...}` placeholders in recommended additions (additions are 1-line edits to existing graph)
- Server-rendered ✓ (Firecrawl `rawHtml` captures the schema without needing `waitFor`)
- Schema is in a single `<script type="application/ld+json">` block with `@graph` — the canonical pattern

## Install

1. Locate the existing Yoast/WPRM-generated `<script type="application/ld+json">` block in the page template.
2. Add the three recommended edits above to the existing `@graph` items (don't add a second `<script>` block).
3. Test the updated page in [Google's Rich Results Test](https://search.google.com/test/rich-results).
4. Re-run this skill to confirm the additions persisted.

## Methodology notes

- 1 Firecrawl credit used (`firecrawl_scrape` on the target URL).
- SE Ranking step 7 (competitor benchmark via `DATA_getSerpResults` + scrape top 10) was NOT run for this example — would have added ~5 SE Ranking credits and ~10 Firecrawl credits to verify what the top-ranked "slow cooker chicken noodle soup" pages emit.

## Handoff payload

- **Produced by:** seo-schema
- **Target:** https://www.budgetbytes.com/slow-cooker-chicken-noodle-soup
- **Key findings:** (a) full `@graph` with 8 interlinked schema entities — among the cleanest implementations we've seen; (b) Recipe is rich-result-eligible today with `aggregateRating` 4.23 of 45 ratings and 13 inline Reviews; (c) only soft warning is missing `dateModified` on the Recipe block (present on parent Article); (d) HowTo retirement (2023) handled correctly — instructions use `HowToStep` within Recipe; (e) Person + Organization entities strong E-E-A-T anchors.
- **Open loops:** competitor benchmark for the SERP cluster (which schema types do the top 10 recipe results emit?); image dimension audit for the primary image (≥ 1200×1200 confirmation).
- **Recommended next skill:** `seo-content-audit` — schema is so clean that the meaningful audit is whether the page text itself (and the linked Person bio) demonstrates the E-E-A-T signals the schema claims.
