# 01 — Seed expansion (longtail)

> Source: `DATA_getLongTailKeywords(keyword="espresso machine reviews", source="us", limit=500)` — pending SE Ranking auth.

## What a full run captures

The longtail expansion endpoint returns variants of the seed keyword that include the seed as a substring or close semantic neighbour, sorted by descending volume. Typical output for a seed like "espresso machine reviews" includes:

- All variants with brand names (breville espresso machine reviews, gaggia espresso machine reviews, ...)
- Price-band variants ("espresso machine reviews under 500", "best espresso machine reviews 2026", ...)
- Use-case variants ("best espresso machine reviews for home", "espresso machine reviews for beginners", ...)
- Question-shaped variants ("which espresso machine has the best reviews", "are breville espresso machines good", ...)
- Comparison variants ("espresso machine reviews breville vs delonghi")

Approximately 800–1,500 longtail variants are typical for a seed of this scope.

## What gets filtered

The default filter:

- Minimum volume: 50/month
- Maximum KD: 40

This drops ~30–50% of the raw expansion to focus on accessible niche keywords. For "espresso machine reviews", the surviving ~400–700 keywords feed step 5 (filter + clean) and downstream clustering.

## Pending

Live keywords on next run.
