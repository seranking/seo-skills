# 05 — SERP samples for representative cluster keywords

> Source: `DATA_getSerpResults` for 5–10 representative keywords (one per emerging cluster). Pending SE Ranking auth.

## What a full run captures per cluster

For each representative keyword:

- Top 10 organic results (URL, title, meta description).
- SERP features present (featured snippet, AIO, people-also-ask, image pack, video carousel).
- Dominant page type (listicle vs single-product review vs guide vs comparison vs forum).

## Expected dominant page types per cluster (qualitative)

| Cluster | Representative keyword | Expected dominant SERP shape |
|---|---|---|
| 1. Price band | "best espresso machine under 500" | 7–8 listicles, 1–2 forum threads, 1 video |
| 2. Use case | "best espresso machine for beginners" | 7–9 listicles, 1 forum thread |
| 3. Single-product | "breville barista express review" | 5–6 single-product reviews, 2–3 videos, 1–2 forum threads |
| 4. By feature | "best espresso machine with grinder" | 8 listicles, 2 manufacturer landing pages |
| 5. Comparison | "breville barista express vs touch" | 5–7 comparison articles, 2–3 videos, 1–2 forum threads |
| 6. Espresso style | "best espresso machine for latte art" | 7 listicles, 3 specialty-coffee guides |
| 7. Buyer guide | "how to choose an espresso machine" | 4–5 guides, 2 manufacturer pages, 3 listicles |
| 8. Maintenance | "how to descale breville espresso machine" | 4 manufacturer pages, 3–4 third-party guides, 2–3 videos |
| 9. Accessories | "best tamper for breville" | 7–8 listicles, 1–2 niche reviews |
| 10. Skill level | "best espresso machine for pro-am users" | 5–6 listicles, 2 specialty forums (CoffeeGeek, Home-Barista) |
| 11. By manufacturer | "best breville espresso machine" | 8 listicles, 1–2 manufacturer pages |
| 12. Commercial | "best commercial espresso machine for small café" | 5–6 B2B listicles, 2 manufacturer pages, 2 industry-blog guides |

## Why this matters for the tier design

The dominant SERP shape per cluster directly determines the template variant for that cluster (A/B/C in `06-template-spec.md`). If the SERP for cluster X is dominated by listicles, ship Variant B; if by single-product reviews, ship Variant A.

The brand-comparison clusters (3, 5, 11) skew toward video — embedding a first-hand video on those pages is a meaningful SERP feature opportunity (video carousel inclusion).

## Pending

Real SERP samples on next run.
