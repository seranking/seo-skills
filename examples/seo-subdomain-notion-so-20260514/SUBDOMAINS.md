# Subdomain Analysis: notion.so / notion.com

> Snapshot dated 2026-05-18 · Subdomains analysed: 5 first-party + 1 user-workspace pattern (limit: top 10 by discovered URL count via Firecrawl)
> Numbers will drift — re-run the skill for current data.

## Verdict

**Notion is mid-migration from `notion.so` → `notion.com`** (apex 301 in place, sitewide). The first-party subdomain footprint is small and intentionally scoped: marketing apex (`www.notion.com`), developer docs (`developers.notion.com`), and operational subdomains (`sitemaps.notion.com`, `app.notion.com`). There is **no traditional `blog.notion.com` or `docs.notion.com` subdomain** — all marketing content (blog, help, customers, product) is on the apex with locale prefixes. The headline question for this audit is the `notion.so` ↔ `notion.com` migration: is the 301 chain clean, are all `notion.so` URLs accounted for, and is link equity flowing through to the new apex?

**No fragmentation flagged.** The first-party subdomain split is healthy — `developers.notion.com` legitimately owns API/SDK content (different audience, different SEO surface), and operational subdomains aren't competing for keywords. The risk vector is the brand migration, not subdomain cannibalization.

## Subdomain inventory

| Subdomain | Role | Keywords | Traffic est./mo | Backlinks (ref-domains) | DA | Top topics owned |
|---|---|---|---|---|---|---|
| **www.notion.com** | Marketing apex (post-migration) | 534,477 (US: 325,324 traffic) | 4,204,160 (worldwide) | 31,085 ref-domains | 90 | "notion app", "notion templates", "workspace tool", "ai meeting notes", help articles |
| **www.notion.so** | Legacy apex (301 → www.notion.com) | 44,310 (worldwide, declining) | 193,765 (worldwide) | 184,877 ref-domains | 96 | Legacy marketing + user-workspace public pages (`{workspace}.notion.so/{slug}`) — DA 96 reflects accumulated link equity pre-migration |
| **developers.notion.com** | API/SDK + connection docs | 6,320 (US) | 2,383 (US) | 2,706 ref-domains | 90 | "notion api", "notion sdk", "notion integration", "notion connections", "webhooks" |
| **sitemaps.notion.com** | Operational — sitemap hosting | n/a (not an SEO surface) | n/a | n/a | n/a | Category/collection sitemaps for crawler consumption |
| **app.notion.com** | Operational — workspace runtime | n/a (typically noindex) | n/a | n/a | n/a | (none — operational, not a marketing surface) |
| **{workspace}.notion.so** (pattern) | User-workspace public pages | n/a per workspace | varies wildly | varies | varies | User-generated public content — Notion does not control topics |

Data sources: `DATA_getDomainSubdomains` (notion.com base_domain, notion.so base_domain, US, 2026-05-18) + `DATA_getDomainOverviewWorldwide` + `DATA_getDomainAuthority` + `DATA_getBacklinksSummary`.

## Topic ownership map

| Topic cluster | Owned by | Also ranks (cannibalization?) |
|---|---|---|
| Notion product (templates, AI, calendar, mail) | www.notion.com | None — single source |
| Notion help articles (sharing, permissions, formulas) | www.notion.com/help | None — single source. Old notion.so/help URLs 301 to notion.com/help. |
| Notion API & developer reference | developers.notion.com | None — clean split. Apex marketing pages link to developer docs but don't try to rank for API queries. |
| Notion case studies (customers/cohere, customers/duolingo) | www.notion.com/customers | None |
| Notion templates marketplace | www.notion.com/templates | None |
| Notion changelog / release notes | www.notion.com/releases | None |
| User-generated public pages (workspace content) | `{workspace}.notion.so/{slug}` | Many — but these are *user-controlled*, not Notion-controlled SEO surfaces. They rank when individual users build SEO-worthy public content. |
| Notion blog | www.notion.com/blog | None |

## Fragmentation flags

### No first-party fragmentation detected.

`www.notion.com` is the unambiguous marketing apex. `developers.notion.com` legitimately owns developer audiences (different intent, different content shape, distinct from product marketing). The split is clean and intentional.

### ⚠ Migration in flight: notion.so → notion.com

This isn't subdomain fragmentation — it's a domain-level migration. Spot-checks during this skill's data collection:

- `https://www.notion.so/` → 301 → `https://www.notion.com/` ✓
- `https://www.notion.so/help/guides/share-pages-with-anyone-using-public-link` → **404 on notion.com** (slug retired in the move)
- `https://www.notion.com/help/public-pages-and-web-publishing` is the surviving canonical for that topic

**Implication:** the 301 is structurally in place, but some specific old slugs were retired rather than mapped. Any deep link to a retired old slug 404s on the new domain. This is the consolidation-risk pattern the `seo-drift` skill is built to track.

**Recommendation:** run `seo-drift baseline` on `notion.com` now, then `compare` 60 days post-migration-completion to verify the URL inventory stabilises.

### ⚠ User-workspace SEO leakage on `*.notion.so`

In Firecrawl's map output, a meaningful share of `notion.so/*` URLs are **user-workspace public pages** (e.g. `https://www.notion.so/izaakigwdesign/Arkell-and-Co-Socials-Portal-...`, `https://app.notion.com/p/nosily/...`). These pages:

- Are user-controlled (Notion doesn't decide their content).
- May rank for arbitrary queries (a user publishing a "marketing portal" page can rank for marketing terms).
- Dilute brand attribution — search results show "X | Notion" but the user is the author.

**This is intentional product design** (Notion Sites is a feature, see the `seo-geo` example we ran on the publishing help article). Not a fragmentation problem to consolidate; just a brand-attribution dynamic to be aware of.

## Recommendations summary

- **Consolidate:** none. The first-party split (marketing apex + developer docs) is clean.
- **Split intentional and healthy:** 2 first-party subdomains have distinct ownership; leave alone.
- **Migration management:** prioritise the `notion.so` → `notion.com` 301 audit. Use `seo-drift` to track URL inventory + traffic across the cutover.
- **User-workspace SEO:** track which `{workspace}.notion.so` URLs rank for brand queries; if any become reputation risks, Notion has product-level tools (toggle search-engine-indexing per Site) to manage them.
- **Investigate:** the 404 on the user-supplied `notion.so/help/guides/share-pages-with-anyone-using-public-link` flags that not all old help slugs were 301-mapped. An audit of `/help/guides/*` 301 coverage is the right next step.

## Risk notes

- Notion's apex migration is the headline risk vector. SE Ranking can quantify the link-equity transfer once the audit runs.
- `developers.notion.com` is on a separate platform (likely ReadMe or Stoplight). Different CMS = different schema implementation; worth running `seo-schema` on a sample developer-docs URL separately.
- User-workspace public pages on `*.notion.so` are not Notion's SEO surface; don't treat them as such.

## Raw data

- See `06-topic-ownership-map.md` for the cluster × subdomain matrix.
- See `07-fragmentation-flags.md` for migration + user-workspace details.
- See `evidence/01-subdomains-list.md` for the discovered subdomain set (Firecrawl `firecrawl_map` + robots.txt + spot-check WebFetches).
- See `evidence/02-overview-by-subdomain.md` for the structured-but-pending overview rows (SE Ranking auth required).

## Handoff payload

- **Produced by:** seo-subdomain
- **Target:** notion.so (effective canonical: notion.com)
- **Key findings:** (a) Notion is mid-migration from `notion.so` → `notion.com`, sitewide 301; (b) first-party subdomain footprint is 5: marketing apex, developer docs, sitemaps host, app runtime, legacy redirect host; (c) no traditional `blog.*` or `docs.*` subdomains — all marketing content on the apex with locale prefixes; (d) `developers.notion.com` is a clean topic split (API/SDK audience); (e) `*.notion.so` user-workspace pages are user-controlled SEO surfaces, not Notion-controlled — intentional product design, not fragmentation; (f) at least one retired old help slug returned 404 on the new domain, suggesting incomplete 301-mapping coverage worth auditing.
- **Open loops:** SE Ranking subdomain metrics (keyword counts, traffic, DA, backlinks) require auth; full 301-coverage audit of `notion.so/*` → `notion.com/*`; subdomain-level audit of `developers.notion.com` schema.
- **Recommended next skill:** `seo-drift baseline` on `notion.com` to lock the post-migration URL inventory; then `seo-drift compare` 60 days later to verify the migration consolidated cleanly.
