# 07 — Recent lost backlinks (sample)

> Source: `DATA_listNewLostBacklinks(target="stripe.com", mode="domain", new_lost_type="lost", order_by="domain_inlink_rank", limit=20, date_from="2026-04-01", date_to="2026-05-18")` — retrieved 2026-05-18.

## Why we sample lost links

A profile audit isn't just about the new-link surface — losses tell a story too:

- **High-authority losses** are immediate red flags. Did a major partner stop linking? Did a press piece de-index? Did a popular GitHub repo migrate to a competitor?
- **Many low-authority losses** are usually noise (small blogs going stale, sites going dark) — track in aggregate, don't act on individuals.
- **Patterns in losses** matter: 50 losses from the same subnet on the same day is interesting.

## Top losses by domain authority (Apr–May 2026)

| Domain | DA | Lost date | Anchor | Reason | Notes |
|---|---|---|---|---|---|
| github.com | 100 | 2026-05-09 | "stripe" | link_removed | assimon/dujiaoka repo removed Stripe link (nofollow) |
| wordpress.com | 100 | 2026-04-25 | "Stripe" + 4 others | other | WordPress.com ToS page removed multiple Stripe legal links — likely a ToS page restructure |
| aws.amazon.com | 100 | 2026-05-12 | Logo (image) | crawl_error | AWS startups page — crawl error, not confirmed removal |
| github.com | 100 | 2026-05-01 | "Stripe API documentation" | link_removed | phpgt/Json wiki removed a Stripe API docs link (nofollow) |
| forbes.com | 98 | 2026-04-22 | "Stripe" | link_removed | 2015 Forbes article had Stripe link removed |
| linktr.ee | 98 | multiple | various | crawl_error | Multiple Linktree user pages with buy.stripe.com links — crawl errors, not confirmed removals |

## What the loss data tells us

1. **DA 100 losses are not alarming here.** The github.com and wordpress.com losses are content-driven (a repo removed a payment-processor link; a ToS page was restructured). Neither signals a competitor threat or Stripe's loss of ecosystem standing.
2. **The AWS crawl error** should be re-checked; crawl_error losses often resolve on the next SE Ranking crawl.
3. **Linktree bulk losses** are from user-generated commerce links (`buy.stripe.com`) that turn over naturally as promotions end. These are noise.
4. **The Forbes 2015 article loss** is a stale-link cleanup — not actionable.

## What to do with this list

1. **Sort by authority descending.** Top 10–20 losses are the actionable ones.
2. **Recheck crawl_error losses first** — most resolve automatically.
3. **For genuine link_removed losses at DA 80+** — reach out to understand if the removal was intentional (content refresh) or accidental (site migration dropped the link).
4. **Cross-reference with `seo-drift`** to confirm whether any loss correlates with a ranking impact.
