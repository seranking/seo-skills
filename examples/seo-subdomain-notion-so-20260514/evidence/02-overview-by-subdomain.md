# 02 — Per-subdomain overview (live data 2026-05-18)

> Source: `DATA_getDomainSubdomains` (notion.com + notion.so, base_domain scope, US) + `DATA_getDomainOverviewWorldwide` + `DATA_getDomainAuthority` + `DATA_getBacklinksSummary` — retrieved 2026-05-18.

## Live data

| Subdomain | Org. KWs (US) | Traffic est./mo (US) | Backlinks ref-domains | DA | Notes |
|---|---|---|---|---|---|
| www.notion.com | 534,477 | 325,324 | 31,085 | 90 | Post-migration marketing apex; dominates by 2 orders of magnitude |
| www.notion.so | 7,714 | 17,211 | 184,877 | 96 | Legacy apex; 301 → www.notion.com; traffic declining but DA 96 reflects pre-migration link equity |
| developers.notion.com | 6,320 | 2,383 | 2,706 | 90 | API/SDK docs; technical audience; strong developer-link profile |
| academy.notion.com | 175 | 367 | — | — | New subdomain (not in original audit scope) |
| faces.notion.com | 336 | 284 | — | — | New subdomain (not in original audit scope) |
| sitemaps.notion.com | ≈ 0 | ≈ 0 | n/a | n/a | Operational; no SEO surface |
| app.notion.com | ≈ 0 | ≈ 0 | n/a | n/a | Operational; workspace runtime |

## notion.so subdomain detail (base_domain)

From `DATA_getDomainSubdomains(notion.so, base_domain)`:

| Host | Traffic (US) | Keywords (US) | Notes |
|---|---|---|---|
| www.notion.so | 17,211 | 7,714 | Legacy apex — 301 to www.notion.com |
| affiliate.notion.so | 354 | 25 | Affiliate programme subdomain |
| privacycenter.notion.so | 26 | 26 | Privacy centre |
| info.notion.so | 6 | 49 | — |
| status.notion.so | 2 | 305 | Status page |
| calendar.notion.so | 1 | 15 | — |

## Migration signal confirmed

`www.notion.so` has 184,877 referring domains (DA 96) versus `www.notion.com`'s 31,085 (DA 90). This gap is the clearest quantitative signal of the migration in progress: link equity is still disproportionately concentrated on the old domain. Google is consolidating signals via the sitewide 301, but the process is not complete. The DA delta (96 vs 90) will narrow over the next 6–12 months as the 301 transfers fully propagate.

**Key implication:** the `www.notion.so` legacy domain still holds the bulk of Notion's accumulated link equity. Any interruption to the 301 chain would be high-impact.
