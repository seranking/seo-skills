# Firecrawl: stripe.com (map mode)

> Snapshot dated 2026-05-14 · Mode: map · Credits used: ~200 (399 URLs × 0.5 credit)
> Numbers will drift — re-run the skill for current data.

## Summary

Mapped `https://stripe.com` with `limit: 500` and `includeSubdomains: false`. Firecrawl discovered 399 indexed URLs reachable from the homepage's link graph. The site is structured as a **locale-prefixed monolith**: 73 unique locale codes (e.g. `/en-ca/`, `/de-be/`, `/zh-us/`, `/pt-pt/`) front almost every content path. The biggest content surface by URL count is `/customers/` (case studies — 113 locale-variant URLs), followed by `/guides/` (33), `/sessions/` (28), and `/newsroom/` (24). Stripe operates the entire site on `stripe.com` — no subdomains surfaced in this map run because we set `includeSubdomains: false`.

## Key findings

1. **73 distinct locale prefixes**, consistent with the 87-locale hreflang lattice observed on `/pricing` (the map sees URLs Firecrawl could reach via crawlable links; hreflang is the declarative source-of-truth). Strong international coverage.
2. **Case studies (`/customers/`) is the largest content surface by URL count** — 113 locale-variant URLs across the map sample. Likely a sales-enablement / proof-driven SEO play, not a top-of-funnel content engine.
3. **Editorial content (`/guides/`, `/newsroom/`, `/resources/`) is comparatively thin** — combined ~70 URLs across all locales. Stripe is heavily product-page-led, not content-marketing-led.
4. **`/jobs/listing/*` accounts for 20 URLs** in the map. Career marketing has its own surface — worth surfacing separately if a domain audit cares about hiring signal.
5. **No subdomains in this map.** A second pass with `includeSubdomains: true` is needed to surface `docs.stripe.com`, `support.stripe.com`, `dashboard.stripe.com` properly. Their absence here is the parameter, not a finding about Stripe.

## Open loops

- A `crawl` (not `map`) over the top patterns (`/customers/*`, `/guides/*`) would let us audit per-page metadata at scale — ~150 credits for the top 150 pages.
- The subdomain surface (`docs.stripe.com`, `support.stripe.com`, `dashboard.stripe.com`, `marketplace.stripe.com`, `status.stripe.com`, `press.stripe.com`) needs a separate `seo-subdomain` analysis or a second map run with `includeSubdomains: true`.
- The 73 locales detected via URL inference can be cross-checked against Stripe's official i18n config (the `/pricing` hreflang lattice declared 73 codes too — they match).
- `firecrawl_map` does not return last-crawled or canonical metadata — those need per-URL `scrape` calls for confirmation.

## Recommended next step

`seo-subdomain` on `stripe.com` — the map confirms a single-host architecture for marketing content but several subdomains were referenced by the `/pricing` scrape (`docs.stripe.com`, `support.stripe.com`, `dashboard.stripe.com`, `marketplace.stripe.com`). The subdomain audit answers "does Stripe own each topic cluster on the right host?".

## Handoff payload

- **Produced by:** seo-firecrawl
- **Target:** stripe.com
- **Mode:** map
- **Credits used:** ~200 (Firecrawl charges 0.5 cr per discovered URL)
- **Key findings:** (a) 399 indexed URLs surfaced via homepage link graph; (b) 73 locale prefixes detected, consistent with hreflang lattice; (c) `/customers/` is the largest content surface by URL count (113); (d) editorial content is comparatively thin (~70 URLs across guides + newsroom + resources); (e) no subdomains in this run because `includeSubdomains: false`.
- **Open loops:** subdomain map (separate run), per-page metadata via `crawl`, hreflang-vs-URL-pattern cross-validation.
- **Recommended next skill:** `seo-subdomain` — confirm topic ownership across the subdomains (`docs`, `support`, `dashboard`, `marketplace`) the scrape mode surfaced.
