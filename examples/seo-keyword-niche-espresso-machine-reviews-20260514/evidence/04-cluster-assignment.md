# 04 — Cluster assignment

> Source: production clustering over the filtered keyword set. Pending SE Ranking auth for live keyword data.

## Clustering approach

For this skill, keywords are clustered by:

1. **Token-shared head term** (e.g. all keywords containing "best espresso machine under" map to one cluster).
2. **Intent + dominant page-type signal** (commercial-listicle keywords vs commercial-review keywords go to different clusters even when the head term overlaps).
3. **SERP overlap** (for borderline cases — keywords whose top-10 SERPs share ≥ 4 URLs join the same cluster; this is the `seo-keyword-cluster` skill's deeper signal).

The combination of token-grouping + intent-typing produces the 12 clusters in `KEYWORD-NICHE-PLAN.md`.

## Expected per-cluster keyword counts (qualitative)

| Cluster | Approximate keyword count | Notes |
|---|---:|---|
| 1. Price band | 35–50 | Many price thresholds × persona modifiers |
| 2. Use case | 40–60 | Wide persona surface |
| 3. Single-product reviews | 80–120 | Highest count — each machine name + variants |
| 4. By feature | 30–45 | Bounded by feature vocabulary |
| 5. Comparison | 40–70 | N choose 2 across popular machines |
| 6. Espresso style | 20–35 | Drink-specific |
| 7. Buyer guides | 15–25 | Lower count, head-term-heavy |
| 8. Maintenance & troubleshooting | 60–90 | Long-tail dominant |
| 9. Accessories | 25–40 | Tampers, scales, grinders, knock boxes |
| 10. Skill level | 15–25 | "Best for pro-am users" niche |
| 11. By manufacturer | 30–50 | Best Breville / Gaggia / Rocket / etc. |
| 12. Coffee shop / commercial | 10–20 | Smaller, higher-CPC niche |

Total: ~400–700 keywords across 12 clusters — matches the post-filter expected count.

## Cluster role assignment

Within each cluster, keywords are assigned a "role":

- **head** — primary keyword for the page (1–3 per page).
- **supporting** — secondary keywords the page targets via H2 / body copy.
- **filler** — third-tier keywords mentioned once for breadth (high-tail variants).

This drives the keyword-deployment shape on each page. The page's `<title>` and H1 use the head term; H2s use supporting terms; body uses fillers.

## Pending

Live cluster assignment on next run with the real keyword set.
