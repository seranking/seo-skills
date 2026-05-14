# 02 — Recommended additions

> Three changes total. All are 1-line additions to the existing `@graph` — no new `<script>` blocks needed.

## Priority ranking

| Rank | Change | Why | Effort | Risk |
|---|---|---|---|---|
| 1 | Echo `dateModified` onto Recipe block | Closes the one validation gap; Google's Recipe spec recommends both dates on the Recipe (currently only on Article) | 1 line | None |
| 2 | Add `Speakable` spec on Recipe description | Opens voice-search surfaces (Assistant, Alexa) for recipe summary | 1 line + 1 CSS selector confirmation | None — the selector must match an actual page class |
| 3 | Add `mainEntity` self-reference on WebPage → Recipe | Strengthens graph; helps Google disambiguate primary content type | 1 line | None |

## Why no `HowTo` block

Google retired `HowTo` rich results entirely in September 2023 (mobile and desktop both). The existing `Recipe.recipeInstructions` array uses `HowToStep` types — that's the correct location for step-by-step content inside a Recipe. Adding a separate `HowTo` block would create a redundant entity in the graph and produce zero rich-result uplift.

## Why no `FAQPage`

The page has no visible Q&A section. Google penalises FAQPage schema on pages without actually-visible FAQs. The "Reasons we love this recipe" / "Tips for ..." sections common in food blogs do NOT count as FAQ — they're advisory paragraphs, not question-answer pairs.

## Why no `Product`

This is not a product page. `Recipe` is already the correct primary type. Adding `Product` would muddy the graph and Google would likely ignore both.

## Why no `Course` or `MenuItem`

Recipe is the rich-result-eligible type for this content. `Course` is for educational courses; `MenuItem` is for restaurant menus. Wrong types here.

## Cost-benefit

All three recommended additions are 1-line edits with zero risk and incremental upside. The page is already in excellent shape — these are the kind of refinements you'd ship in a quarterly schema-hygiene sweep, not a critical fix list.
