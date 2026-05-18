# 01 — Seed expansion (longtail)

> Source: `DATA_getLongTailKeywords(keyword="espresso machine reviews", source="us", limit=500)` — retrieved 2026-05-18.

## Live data (2026-05-18)

Total longtail keywords returned: **439**

The expansion returned brand-specific review variants (breville, gaggia, saeco, delonghi, krups, rancilio, la pavoni, sunbeam, russell hobbs, etc.), year-dated variants (2010–2015 vintage terms, still indexable), and type variants (automatic, semi-automatic, super-automatic, capsule, lever, steam). The endpoint returns keyword strings only — volume and KD are not included in this response.

Sample keywords returned:
- breville barista express reviews, gaggia classic reviews, saeco odea go reviews
- best home espresso machine reviews, home espresso machine reviews 2015
- automatic espresso machine reviews 2012/2013/2014
- delonghi ec155 reviews, krups xp3200 reviews, sunbeam cafe series reviews
- commercial espresso machine reviews, double boiler espresso machines reviews
- espresso capsule machine reviews, lever espresso machine reviews

## What gets filtered (downstream step)

The default filter applied in step 5:

- Minimum volume: 50/month
- Maximum KD: 40

The longtail endpoint does not return volume/KD directly — these are obtained via `DATA_getRelatedKeywords` or `DATA_getSimilarKeywords` in the next step. Note that many of the 439 returned terms are year-dated (2011–2015) and will have zero or near-zero current search volume — the active universe after filtering is estimated at 120–200 terms.

## Cluster coverage confirmed

The 439 raw terms confirm all 12 planned clusters have representation: brand-specific reviews (cluster 3, 11), automatic/type (cluster 4), price-band (cluster 1), comparison (cluster 5), capsule/lever (cluster 4). No unexpected cluster gaps found.
