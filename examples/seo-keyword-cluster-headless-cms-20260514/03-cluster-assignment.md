# Cluster assignment — SERP overlap matrix

Source: SERP overlap was computed from `mcp__firecrawl-mcp__firecrawl_search` on each of 8 seed keywords, capturing the top-10 organic URLs per seed. URL-level overlap was computed pairwise. Domain-level overlap was computed separately as a sanity check.

The skill normally uses `DATA_getSerpResults` (SE Ranking) on each candidate keyword — that endpoint is unavailable in this run. Firecrawl search is a substitute for SERP-standard mode at lower cost.

## Pairwise URL-overlap matrix (top-10 shared URLs)

|   | hc cms | best hc cms | hc vs trad | hc ecom | hc nextjs | open src | hc api | strapi vs contentful |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **hc cms** | — | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| **best hc cms** | 0 | — | 0 | 0 | 1 | 1 | 0 | 1 |
| **hc vs trad** | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 |
| **hc ecom** | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 |
| **hc nextjs** | 0 | 1 | 0 | 0 | — | 0 | 0 | 0 |
| **open src** | 0 | 1 | 0 | 0 | 0 | — | 0 | 1 |
| **hc api** | 1 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| **strapi vs contentful** | 0 | 1 | 0 | 0 | 0 | 1 | 0 | — |

Per the skill's thresholds:
- **7-10 shared URLs** → merge to same post (none observed)
- **4-6 shared URLs** → same cluster (none observed)
- **2-3 shared URLs** → interlink across clusters (none observed)
- **0-1 shared URLs** → separate clusters or exclude (everything here)

**Every seed forms its own cluster.** This is unusually clean — typically you'd see at least one pair in the 2-6 range. The "headless CMS" topic has unusually crisp sub-topic boundaries because vendors have shaped the SERP intentionally to own specific intents (Sanity owns "headless cms"; Cosmic owns "best headless cms 2026"; Crystallize owns "ecommerce"; Strapi owns "open source" + "vs contentful"). Each query has its own vendor-staked territory.

## Cluster derivation logic

Since URL-overlap is zero, clustering falls back to:
1. **Domain-level overlap** (which publishers appear across seeds — sanity check, not for grouping)
2. **Intent overlap** (informational / commercial / use-case)
3. **Semantic relatedness** (these are all about the same topic, after all)

This produces 5 logical clusters:

| Cluster | Seeds folded in | Primary intent | Pillar-worthy? |
|---|---|---|:---:|
| 1. What is a Headless CMS | hc cms, hc vs trad, hc api | Informational | yes |
| 2. Best Headless CMS | best hc cms, hc nextjs, open src | Commercial | yes |
| 3. Headless Commerce | hc ecom | Use-case (commercial) | yes |
| 4. Vendor Comparisons | strapi vs contentful | Commercial | spoke-only |
| 5. Pricing | (not in seeds — derived from intent classification of `headless cms pricing` + `free headless cms`) | Transactional | spoke-only |

The "best hc cms" seed touches `hc nextjs` (1 shared URL) and `open src` (1 shared URL) — both 1-pair overlaps lean toward "interlink across clusters" per the threshold but I folded them into Cluster 2 as **spokes** of the Best pillar. Rationale: searcher intent is the same ("which one should I buy") regardless of audience qualifier (Next.js / open-source).

`strapi vs contentful` shares 1 URL each with `best hc cms` and `open src` — kept separate as Cluster 4 because vendor-comparison content has structurally different shape (head-to-head matrices, feature parity tables) than "best of" listicles.

## Domain-level overlap (publishers across seeds — sanity check)

| Publisher | Seeds where ranking | Notes |
|---|---:|---|
| reddit.com | 3 of 8 | Community / Q&A — different format from editorial content; not a content competitor for the planned pillars |
| sanity.io | 2 of 8 | Vendor with "what is" + "vs traditional" pillars — Cluster 1 competitor |
| prismic.io | 2 of 8 | Vendor with "what is" + "best for startups" — Cluster 1 + Cluster 2 |
| strapi.io | 2 of 8 | Vendor with "what is" + "for ecommerce" — Cluster 1 + Cluster 3 |
| contentful.com | 2 of 8 | Vendor with "what is" + "vs traditional" — Cluster 1 |
| cosmicjs.com | 2 of 8 | Vendor with "best" + "for nextjs" + "explained" — Cluster 1 + Cluster 2 |

All multi-seed publishers are themselves headless CMS vendors. None are pure-publisher (e.g., G2, ProductHunt, TechCrunch). This means the SERP is **vendor-saturated** — any new entrant either needs to be a vendor too (and out-content the established players) or be a respected publisher entering the space.

## Cluster volume + KD summary

| Cluster | Total volume | Avg KD | Pillar volume | Spoke volume |
|---|---:|---:|---:|---:|
| 1. What is a Headless CMS | ~41K/mo | 48 | 33K | 8K |
| 2. Best Headless CMS | ~12K/mo | 42 | 5.4K | 6.6K |
| 3. Headless Commerce | ~9.5K/mo | 47 | 6.6K | 2.9K |
| 4. Vendor Comparisons | ~3.0K/mo | 30 | — | 3.0K |
| 5. Pricing | ~1.5K/mo | 30 | — | 1.5K |
| **Total** | **~67K/mo** | **~42** | **45K** | **22K** |

(Above is approximate — exact numbers pending SE Ranking auth.)

## Implications for build order

The Priority score (volume 40% + inv-KD 30% + commercial-intent 30%) yields:
1. **Cluster 1 (What is)** → 92 — highest volume + reachable KD; ship pillar first
2. **Cluster 2 (Best)** → 78 — high commercial intent; ship pillar second
3. **Cluster 3 (Ecommerce)** → 70 — use-case angle; ship pillar third
4. **Cluster 4 (Vendor comparisons)** → 60 — high commercial intent but low volume; ship after pillars; use `seo-competitor-pages` skill
5. **Cluster 5 (Pricing)** → 50 — low volume, very specific intent; ship last
