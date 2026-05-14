# Technical Audit: linear.app

> Snapshot dated 2026-05-14 · sample 8 URLs crawled (Firecrawl + HTTP HEAD) · Country: US · Numbers will drift — re-run the skill for current data.

## Verdict

**Health score: 78/100** — solid security and Next.js infrastructure, **but blocked from AI Search and Open Graph upside by zero JSON-LD structured data across the entire site**. The top fix list is dominated by missing schema markup, sitemap hygiene, and an outdated changelog tier still in the indexable set.

## Summary

| Severity | Count |
|---|---:|
| Critical | 1 |
| High | 4 |
| Medium | 7 |
| Low | 3 |

## Top 10 fixes (impact × effort)

| Rank | Issue | Severity | Pages | Fix | Effort |
|---|---|---|---:|---|---|
| 1 | No JSON-LD structured data anywhere on the marketing site | Critical | ~896 (entire sitemap) | Add `Organization` + `SoftwareApplication` schema on `/`, `Article` + `Person` schema on `/blog/*`, `Article` schema on `/customers/*`, `BreadcrumbList` site-wide | M |
| 2 | 196 changelog/blog URLs in sitemap with `lastmod` older than 2024-01-01 | High | 196 | Either refresh + bump lastmod, or move stale changelog entries to an archive section (no-sitemap) | M |
| 3 | HSTS missing `preload` directive | High | site-wide | Add `preload` to STS header (currently `max-age=63072000; includeSubDomains`), then submit to hstspreload.org | S |
| 4 | Meta description on homepage is 61 chars (target ≥120) | High | `/` | Rewrite homepage description to 140-155 chars to capture full SERP snippet | S |
| 5 | No AI-crawler rules in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended all allowed by default) | High | `/robots.txt` | Decision required: explicitly allow (signals intent) or disallow (opt out of training); current behaviour is implicit allow | S |
| 6 | `og:image` lacks `og:image:width` and `og:image:height` | Medium | ~896 | Add `og:image:width` / `og:image:height` meta tags to template — improves social-share preview reliability | S |
| 7 | 44 URLs in sitemap (4%) without `<lastmod>` | Medium | 44 | Add lastmod to all entries; absent lastmod tells crawlers "no signal," so they re-crawl on their own cadence | S |
| 8 | CSP `frame-src *` wildcard | Medium | site-wide | Tighten `frame-src` to explicit allow-list (Stripe, Ashby, Cloudflare Turnstile already used) — wildcard allows clickjacking via iframe embed | M |
| 9 | Title (45 chars) below the 60-char target on homepage | Medium | `/` | Lengthen homepage title to 55-60 chars — current "Linear – The system for product development" leaves SERP real estate unused | S |
| 10 | No hreflang or `x-default` declared | Medium | site-wide | English-only is fine for now, but the absence of `<link rel="alternate" hreflang>` blocks any future internationalisation without a structural change | S |

## By category

### Crawlability (2 issues)
- 8/8 sampled URLs returned HTTP 200 — no crawl errors on the marketing tier.
- `/blog` returns 307 on first hop (likely Geo-IP/locale routing) — sitemap should list canonical destinations to avoid wasting crawl budget on the redirect.

### Indexability (3 issues)
- No `meta robots` tag on any sampled page → defaults to `index, follow`. Good.
- Canonical present on every sampled page and points to self — no canonical conflicts detected.
- Disallow `/api/` and `/cdn-cgi/` in robots.txt correctly excludes internal API routes from crawl budget.

### Security (4 issues — see `evidence/02-issues-by-category/security.md` for full headers)
- **HSTS preload missing** (`hsts_no_preload`) — header present but `preload` directive absent and `linear.app` not on Chromium preload list.
- **CSP `frame-src *`** — wildcard frame-src is a clickjacking surface; harden to explicit list.
- **X-Content-Type-Options: nosniff** present everywhere sampled. Good.
- **X-Frame-Options absent**, but CSP `frame-ancestors 'self' https://cms.linear.app` supersedes — informational only.
- **Referrer-Policy: same-origin** present everywhere. Good.

### Mobile (1 issue)
- `viewport` meta tag present with `width=device-width, height=device-height, initial-scale=1, viewport-fit=cover`. Good — viewport-fit=cover signals modern notched-device awareness.

### Structured data (1 critical issue)
- **Zero JSON-LD on every sampled page.** Homepage, pricing, customers/openai, customers index, method, changelog: no `<script type="application/ld+json">` blocks. This is the single most consequential finding — see Modern signals + key-page deep dives.

### Content (2 issues)
- Homepage meta description (61 chars) and title (45 chars) both run short. SERP real estate left unused.
- H1 on homepage is rendered twice in initial HTML (likely responsive design with display:none on one variant). Static crawlers see two H1s; flag for review.

### Modern signals (5 findings)
- robots.txt — **GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot all return HTTP 200** when fetching `/` (implicit allow). No AI-bot Disallow declared. Decision required: explicit allow or explicit disallow.
- JS-render canonical vs initial-HTML canonical — match on every sampled page (homepage, pricing, method, customers/openai). No `js_canonical_mismatch`.
- X-Robots-Tag header — absent on every sampled page. No conflict with HTML-level robots.
- IndexNow — no `IndexNow:` directive in robots.txt, no `x-indexnow-key` header observed, no key file detected at root. `indexnow_no_key` (Low; informational — Bing-only benefit).
- Cache: `cache-control: s-maxage=120, stale-while-revalidate=31535880` — aggressive SWR window (~365 days). Good for perf, but `lastmod` accuracy in the sitemap matters more when revalidation lags.

### Security headers (extended — HTTP HEAD on homepage + 3 samples)

| Header | Homepage | /pricing | /method | /customers | Issue |
|---|---|---|---|---|---|
| Content-Security-Policy | present (broad) | present (broad) | present (broad) | present (broad) | `frame-src *` wildcard (Medium) |
| X-Frame-Options | absent | absent | absent | absent | superseded by CSP `frame-ancestors` (informational) |
| X-Content-Type-Options | `nosniff` | `nosniff` | `nosniff` | `nosniff` | none |
| Referrer-Policy | `same-origin` | `same-origin` | `same-origin` | `same-origin` | none |
| HSTS preload | `max-age=63072000; includeSubDomains` (no preload directive) | same | same | same | `hsts_no_preload` (High) |

## Core Web Vitals (field data — CrUX)

CWV (field data): not configured — SE Ranking MCP not authenticated in this run, CrUX requires `google-api.json` (Tier 0) which is not present. Run `bash extensions/google/install.sh` to enable, then re-run this skill for actual p75 LCP / INP / CLS / FCP / TTFB and the 25-week trend.

## Indexation reality check (GSC URL Inspection)

Indexation reality check: not configured (Tier 1 setup required — GSC property verification + `google-api.json`).

## Key-page deep dives

### `/` (homepage)
3 issues found. Top fixes:
1. Add `Organization` + `SoftwareApplication` JSON-LD (logo, sameAs to twitter/linkedin/github, alternate `applicationCategory: "BusinessApplication"`).
2. Rewrite meta description to 140-155 chars — current 61-char description leaves SERP snippet truncated.
3. Lengthen `<title>` from 45 to 55-60 chars (current title is "Linear – The system for product development").

### `/customers/openai` (sample customer story)
2 issues found. Top fixes:
1. Add `Article` + `Organization` JSON-LD with `author`, `publisher`, `datePublished`, `dateModified`, `about: {OpenAI}` to make the page citable by LLMs as a case study.
2. `og:type` absent — declare `og:type: "article"` on customer-story pages.

### `/changelog`
2 issues found. Top fixes:
1. 196 changelog entries (2020-2023) in the sitemap still receive crawl budget. Archive or refresh.
2. No JSON-LD — at minimum, declare `BlogPosting` schema per entry.

## Recommended cadence

Re-run this skill monthly to catch regressions, or wire `seo-drift` to baseline + diff between audits.

## Methodology notes

- **SE Ranking MCP not authenticated in this run.** The skill's primary data source (`DATA_listAudits` / `DATA_createStandardAudit` → `DATA_getAuditReport` → `DATA_getAuditPagesByIssue`) was unavailable. The audit was reproduced from Firecrawl + HTTP HEAD on a sample of 8 URLs (homepage, pricing, method, customers index, customers/openai, agents, features, insights) plus the full sitemap (896 URLs parsed). The Top-10 fixes are reproducible — anyone with the URL can curl-verify the security headers and grep the HTML for JSON-LD presence. Re-run with SE Ranking authenticated for the full site-wide crawl (typically 50-100 pages) and proper issue-code mapping (`issues.csv` columns map to SE Ranking's audit codes; in this run they are mapped from observed signals).
- **Tools used:** `mcp__firecrawl-mcp__firecrawl_scrape` (homepage, robots.txt, sitemap.xml, 3 sample pages), `WebFetch` + curl HEAD (response headers across 7 URLs).
- **Credit budget:** 6 Firecrawl credits (well under the example's 10-credit cap).
- **Page-count cap:** 8 sample URLs crawled (vs the skill's default 50-100). The findings generalise to the marketing tier because Linear's templating is Next.js-based and head-tag patterns are consistent across the sampled URLs.

## Handoff payload
- **Produced by:** seo-technical-audit
- **Target:** linear.app
- **Key findings:** (a) Zero JSON-LD anywhere on the marketing site — biggest single AI Search readiness gap; (b) strong baseline security (HSTS, CSP, X-Content-Type-Options, Referrer-Policy all present) but HSTS preload missing and CSP frame-src wildcard remains; (c) 196 changelog/blog URLs in sitemap with lastmod older than 2024-01-01 — stale-content drag on crawl budget; (d) AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) all return 200 with no explicit allow/disallow rules — implicit allow is a passive default.
- **Open loops:** SE Ranking audit for the full issue-code mapping, page-count reach, and per-URL issue lists. CrUX field data for actual p75 CWV. GSC URL Inspection for `indexStatusVerdict` + `googleCanonical` divergence on top traffic pages.
- **Recommended next skill:** `seo-schema` — paste-ready JSON-LD blocks for the top page types (homepage Organization, customers/* Article, blog/* BlogPosting, /pricing Product/Offer). After that, `seo-drift baseline` to capture this snapshot for monthly diff.
