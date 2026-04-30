---
name: seo-local
description: Local SEO audit for brick-and-mortar, service-area, and multi-location businesses. Covers Google Business Profile signals on the website, NAP consistency across page and schema, local-pack rank tracking, citation samples on Tier-1 directories, and reviews on Google / Yelp / Trustpilot. Distinct from `seo-page` (URL-level keywords, no local layer) and from `seo-schema` (which generates LocalBusiness markup — this skill defers to it). Use when the user asks "local SEO", "GBP", "Google Business Profile", "NAP", "local pack", "citations", "near me", "service area", or "multi-location SEO".
---

# Local SEO

Score a local business's website against the signals that drive local-pack and "near me" visibility — GBP integration on the page, NAP consistency, on-page local intent, citation footprint on Tier-1 directories, review-platform presence, and local-pack rank for the business's primary keywords. Deliverable is one prioritised fix list, anchored in observable signals.

> Adapted from [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo)'s `seo-local` skill (MIT). Concept and dimension structure mirror the upstream; backend rewired to SE Ranking + Firecrawl + Google APIs. DataForSEO Maps geo-grid and Business Listings checks from the upstream are dropped (no equivalent backend) — see "Limitations" in the deliverable.

## Prerequisites

- SE Ranking MCP server connected (used for local-pack rank, on-page audit data, domain context).
- Claude's `WebFetch` tool available (used for sense-check fallback when Firecrawl is unavailable).
- User provides: (a) a target domain or homepage URL, (b) at least one primary local keyword (e.g. `"dentist Brooklyn"`, `"plumber near me"`), (c) target country and ideally city/region for local-pack scoping. Optional: GBP listing URL, Yelp/Trustpilot URLs for review scraping.

## Process

1. **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (credit balance, Firecrawl availability, Google APIs). Skill-specific notes:
   - Normalise the target (strip protocol from domain; confirm homepage is fetchable). Confirm at least one local keyword was provided — if none, infer from `<title>` + `<h1>` of the homepage; if still ambiguous, ask the user before continuing.
   - Estimated SE Ranking cost for this skill: ~15–25 credits (1 audit re-check + 3–5 SERP queries + 1 domain overview).
   - Firecrawl: optional with WebFetch fallback, ~6–9 Firecrawl credits if available (hard cap 12). When available, steps 4 (GBP-on-page audit), 5 (NAP extraction), and 7 (review scraping) run on the homepage + 5 sample pages + provided review URLs. Without Firecrawl those steps degrade to WebFetch-only — schema/JSON-LD detection and `tel:` / address element extraction become best-effort prose inspection. Pass `--no-firecrawl` to force WebFetch-only.
   - Google APIs: tier 1 (GSC) unlocks step 8b (GSC local query performance) after the local-pack rank step; tier 2 (GA4) additionally unlocks step 8c (GA4 organic-by-landing-page enrichment). See `skills/seo-google/references/cross-skill-integration.md` for the full enrichment contract.

2. **Business-type detection**
   - Read homepage + `/contact` + footer prose (WebFetch markdown is enough for this).
   - Classify as one of:
     - **Brick-and-Mortar** — visible street address, "Visit us at", embedded Maps iframe.
     - **Service Area Business (SAB)** — no street address, "serving {region}", "we come to you", `areaServed` in schema without `address.streetAddress`.
     - **Hybrid** — both signals present (e.g. showroom + service area).
   - This determines which checks apply downstream. SAB skips embedded-map and physical-address consistency. Record in `LOCAL-SEO-REPORT.md` "Snapshot".

3. **Industry-vertical detection**
   - From URL patterns (`/menu`, `/practice-areas`, `/listings`, `/inventory`), `<title>`, page prose, infer one of: Restaurant / Healthcare / Legal / Home Services / Real Estate / Automotive / Generic.
   - This routes citation-source recommendations and schema-subtype recommendations later — load `references/local-citation-sources.md` for the vertical's Tier-1 directories.

4. **GBP signals on the page** `mcp__firecrawl-mcp__firecrawl_scrape` (with `formats: ["rawHtml"]`)
   - Scrape homepage + `/contact` (or whichever page has the most local intent).
   - From `rawHtml` extract:
     - Embedded Google Maps iframe (`<iframe src="https://www.google.com/maps/embed?...">`) — record place ID if present.
     - Reviews widget / GBP rich snippet markup.
     - `aggregateRating` JSON-LD block (presence is the strongest signal that the site wants stars in SERPs).
     - Business hours visibility on page (open-at-search-time correlates with rank — Whitespark's #5 factor).
     - Click-to-call: count of `<a href="tel:...">` elements.
     - GBP profile link: any `<a href>` to `https://g.page/...` or `https://maps.app.goo.gl/...` or `https://www.google.com/maps/place/...`.
   - **If Firecrawl unavailable:** WebFetch markdown can detect a `tel:` link in some renderings but loses iframes and JSON-LD. Mark Maps embed / aggregateRating / GBP profile-link detection as `(skipped — Firecrawl required)`.

5. **NAP consistency** `mcp__firecrawl-mcp__firecrawl_scrape` on homepage + 5 sample pages
   - Sample pages: homepage, `/contact`, `/about`, plus 2 service or location pages (pick from sitemap or top traffic pages).
   - For each, extract:
     - **Visible NAP from rendered prose.** Address pattern (street + city + region + postal), phone (`tel:` href + display format), business name (logo alt, footer, schema `name`).
     - **NAP from JSON-LD.** Parse every `<script type="application/ld+json">` block. Pull `name`, `address.streetAddress`, `address.addressLocality`, `address.addressRegion`, `address.postalCode`, `telephone`.
   - **Compare across the 6 page samples + schema.** Any divergence (different phone format on the contact page vs homepage; "Suite 200" missing from one footer; schema phone in international format while page shows local format) → record in `nap-inconsistencies.csv`.
   - **Brick-and-mortar only:** if a Maps iframe is present, attempt to read the embedded address from the iframe URL (the place ID and address are URL-encoded). Compare to page/schema NAP. SAB skips this.
   - If `nap-inconsistencies.csv` is empty after the scan, write `nap-inconsistencies.csv` as a one-line file with header only and note "NAP consistent across {n} pages and schema" in `LOCAL-SEO-REPORT.md`.

6. **Local-pack rank tracking** `DATA_getSerpResults` with country/region filters
   - For each user-provided local keyword (or the 1–3 inferred from homepage):
     - Call `DATA_getSerpResults` with the user's country and the most specific region/city the API supports (use `DATA_getSerpLocations` first to confirm a valid location code if the user supplied a city).
     - Capture: top 10 organic, local-pack presence (yes/no), the 3 businesses in the local pack if shown (name, rating, review count), AIO presence.
     - Cross-check: is the target domain in the top 10 organic? Is the target business name in the local pack?
   - **Save the parsed result per keyword to `local-keywords.csv`** (columns: `keyword,country,location,local_pack_present,target_in_pack,target_pack_position,target_organic_position,top_pack_competitor_1,top_pack_competitor_2,top_pack_competitor_3`).
   - Note the local-pack-ads caveat: the SE Ranking SERP returns the AI/ads-modified pack as Google serves it. If the local pack shows ads, record that — local-pack ad density jumped from 1% to 22% of mobile US local searches in 2025–2026 per Sterling Sky.

7. **Reviews scraping** `mcp__firecrawl-mcp__firecrawl_scrape` on user-provided review URLs
   - **Inputs (user-provided, optional).** GBP listing URL (`https://www.google.com/maps/place/...`), Yelp business URL, Trustpilot business URL, BBB profile URL.
   - **For each provided URL:** scrape with `formats: ["rawHtml"]`. From the parsed DOM, extract: total review count, average rating, date of most recent review (review velocity proxy), count of owner responses on the most recent 10 reviews.
   - **Aggregate signals:**
     - Velocity: ≥1 new review in last 18 days = healthy (Sterling Sky 18-day rule). >21 days since last = "review cliff" risk.
     - Volume: <10 Google reviews flags below the magic threshold.
     - Star rating: 4.5+ matches consumer filtering thresholds (BrightLocal: 31% only consider 4.5+).
     - Owner-response rate on Google: <50% on recent 10 = engagement gap.
   - **If user provides no review URLs:** skip step 7 entirely. Note in `LOCAL-SEO-REPORT.md`: "Review platforms: not provided. To audit review health, re-run with `--reviews 'gbp_url,yelp_url,trustpilot_url'`." Don't try to discover them — review-URL discovery is a different problem (and the Maps API path is the one we don't have).

8. **On-page local-SEO audit** `DATA_getAuditReport` (existing audit) + `DATA_getIssuesByUrl` on the homepage
   - **Reuse the existing site audit if one is recent (<30 days, see `seo-technical-audit`).** Don't create a new audit just for local — the audit data already covers title-tag issues, missing schema, mobile usability, etc.
   - From the audit, surface the issues that bear on local SEO specifically:
     - Title / H1 missing primary city or service term.
     - Missing or invalid `LocalBusiness` JSON-LD.
     - Mobile usability issues (mobile = where "near me" happens).
     - Schema validation errors (broken `aggregateRating`, malformed `address`).
   - **Defer schema fixes to `seo-schema`.** This skill does NOT generate JSON-LD. If LocalBusiness schema is missing or broken, the deliverable says "Run `seo-schema` for paste-ready LocalBusiness markup with the correct industry subtype" — that's `seo-schema`'s job and reimplementing it here would duplicate work.

8b. **GSC local query performance** *(only if google-api.json is present, tier ≥ 1)*
   - Pull GSC search analytics for the target property, last 28 days, dimension=query, filtered to local-intent patterns:
     `python3 scripts/gsc_query.py --property "{config.default_property}" --days 28 --json`
   - Client-side filter the queries for: contains `near me`, contains a city/region known for the business, or ends in a place-name. Surface top 10 by impressions.
   - If a city-bearing query has impressions >100 and average position >10, that's a local-pack reach gap — flag in `LOCAL-SEO-REPORT.md` "Top fixes" with the GSC numbers as supporting evidence.
   - If property not verified for this account: surface "GSC: {target_domain} not verified — add it in Search Console" and continue.
   - See `skills/seo-google/references/cross-skill-integration.md` for failure modes.

8c. **GA4 organic by landing page** *(only if google-api.json is present, tier ≥ 2)*
   - Pull GA4 top organic landing pages, last 28 days:
     `python3 scripts/ga4_report.py --report top-pages --days 28 --json`
   - For multi-location sites, surface per-location-page sessions. If one location page captures 80%+ of organic traffic while peer location pages capture <5%, that's location-page quality variance worth flagging (probable doorway-page or thin-content risk on the underperformers).
   - Single-location sites: just record the homepage's organic sessions as one row in the snapshot.

9. **Citation-presence sample (best-effort)** `WebSearch` (no API key cost)
   - For each Tier-1 directory in the vertical's list (load `references/local-citation-sources.md`), check whether the business has a listing using `site:{directory} "{business_name}"` queries via WebSearch.
   - **Cap at 8 directories** (Google, Yelp, Facebook, BBB, Apple Maps, Bing Places, plus 2 vertical-specific). Anything beyond is diminishing returns and the user can run their own audit.
   - Record in `LOCAL-SEO-REPORT.md` "Citations" section: detected / not detected per directory, plus the URL of the listing if found.
   - **Caveat to surface:** WebSearch hits are a *sample*, not a comprehensive audit. A "not detected" doesn't prove absence — it proves the listing didn't surface for that specific query. Recommend a paid citation-audit tool (Whitespark, BrightLocal, Yext) for definitive coverage.

10. **Synthesise** `LOCAL-SEO-REPORT.md`
   - Score the 5 local dimensions on the rubric below, list top fixes (Critical / High / Medium / Low), record limitations.
   - Apply the verdict heuristic — see Tips.

## Output format

Create a folder `seo-local-{domain-slug}-{YYYYMMDD}/` with:

```
seo-local-{domain-slug}-{YYYYMMDD}/
├── LOCAL-SEO-REPORT.md         (PRIMARY: verdict, scores, top fixes, limitations)
├── local-keywords.csv          (load-bearing: per-keyword local-pack + organic positions)
├── nap-inconsistencies.csv     (load-bearing: only emitted if discrepancies found)
└── evidence/
    ├── 01-homepage-snapshot.md     (Firecrawl raw HTML extracts: NAP, schema, GBP signals)
    ├── 02-nap-page-samples.md      (per-page NAP extracts across 5 sample URLs)
    ├── 03-serp-context.md          (raw DATA_getSerpResults per keyword)
    ├── 04-reviews.md               (per-platform review-page snapshots, only if user provided URLs)
    └── 05-citation-sample.md       (raw WebSearch results per directory check)
```

`LOCAL-SEO-REPORT.md` follows this shape:

```markdown
# Local SEO Report: {domain}

> Snapshot dated {YYYY-MM-DD} · Country: {country} · Region: {region} · Primary keyword: "{keyword}"

## Snapshot
- Business type: {Brick-and-Mortar | SAB | Hybrid}
- Industry vertical: {Restaurant | Healthcare | Legal | Home Services | Real Estate | Automotive | Generic}
- Pages sampled for NAP: {n}
- Local keywords tracked: {n}
- Local pack present on {n}/{m} keywords; target in pack on {p}/{m}
- Review platforms audited: {Google, Yelp, ... | not provided}
- GSC last 28d local-intent queries: {n} queries / {clicks} clicks / {impressions} impressions  *(or `not configured`)*

## Verdict: {STRONG | NEEDS WORK | WEAK}

{One-sentence summary anchored in dimension scores below}

## Dimension scores (0–10)

| Dimension | Score | Top finding |
|---|---|---|
| GBP integration on page | {n}/10 | {one-line} |
| NAP consistency | {n}/10 | {one-line} |
| Local on-page (title/H1/contact/service pages) | {n}/10 | {one-line} |
| Local-pack rank | {n}/10 | {one-line} |
| Reviews & citations | {n}/10 | {one-line} |
| **Composite** | {n}/10 | — |

## Top fixes

### Critical
1. {Specific fix anchored in a finding above. Example: "NAP discrepancy: footer shows '(212) 555-1234' but JSON-LD shows '+1-212-555-9999'. Pick one canonical phone, fix the wrong one." Cite the page/schema source.}

### High
- {fix}

### Medium
- {fix}

### Low
- {fix}

## Local-pack rank summary
- "{keyword 1}": local pack {present/absent}, target {in pack at #n / not in pack}, organic position {n}.
- "{keyword 2}": …
- (Full data: `local-keywords.csv`)

## Reviews health (if audited)
- Google: {n} reviews, {rating} avg, last review {n} days ago, owner response rate {p}%.
- Yelp: …
- Trustpilot: …

## Citation sample
- Google Business: {detected / not detected via site:google.com "..." search}
- Yelp: …
- Facebook: …
- BBB: …
- Apple Business Connect: …
- Bing Places: …
- {vertical-specific 1}: …
- {vertical-specific 2}: …

(Caveat: this is a sample, not a comprehensive citation audit. For definitive coverage, use Whitespark / BrightLocal / Yext.)

## Schema status
- LocalBusiness JSON-LD: {present and valid / present but missing recommended properties / invalid / absent}
- Recommended next step: run `seo-schema {homepage_url}` for paste-ready LocalBusiness markup with the correct industry subtype.

## Limitations
This skill could NOT assess:
- **Geo-grid local-pack rank by lat/long.** Requires a Maps API (e.g. DataForSEO Maps geo-grid endpoint) we don't have. Workaround: pay for Local Falcon, GMB Crush, or BrightLocal Local Search Grid.
- **Comprehensive citation audit.** WebSearch sampling covers ~8 directories; full audits cover 50+. Use Whitespark, BrightLocal, or Yext.
- **GBP Insights data.** Requires GBP API access scoped to the listing owner. Ask the listing owner to export Insights and share.
- **Real-time local-pack rank tracking over time.** This skill is a snapshot. Use SE Ranking's project-level rank tracker (`PROJECT_runPositionCheck`) or pair with `seo-drift` for diff snapshots.
- **DataForSEO Business Listings.** Not in our backend; if the user needs it, they'd need to subscribe to DataForSEO directly.
```

`local-keywords.csv` columns: `keyword,country,location,local_pack_present,target_in_pack,target_pack_position,target_organic_position,top_pack_competitor_1,top_pack_competitor_2,top_pack_competitor_3,aio_present`

`nap-inconsistencies.csv` columns: `source,name,address,phone,page_or_schema_path,canonical_value,divergence_note`

## Tips

- Respect SE Ranking Data API rate limit: 10 requests per second. Pace the per-keyword `DATA_getSerpResults` calls sequentially.
- Call `DATA_getCreditBalance` before running. ~15–25 SE Ranking credits typical, plus 6–12 Firecrawl credits when Firecrawl is installed.
- Verdict heuristic:
  - **STRONG**: composite ≥7/10, NAP consistent across all sampled pages, target in local pack on majority of keywords, valid LocalBusiness schema with industry-correct subtype, ≥10 Google reviews with healthy velocity.
  - **NEEDS WORK**: composite 4–6.9/10, OR 1+ NAP discrepancy, OR target out of local pack on majority of keywords. The "Top fixes" section is the deliverable here — most local-SEO audits land in this bucket.
  - **WEAK**: composite <4/10, OR no LocalBusiness schema and no NAP visible on page, OR target absent from local pack on every tracked keyword. Substantial work required across multiple dimensions.
- Don't generate LocalBusiness schema in this skill. **Always** defer to `seo-schema` for that — it has the rich-results validation and industry-subtype routing this skill doesn't replicate.
- Don't generate review URLs from search results. If the user didn't provide a Yelp/Trustpilot/BBB URL, skip review scraping and tell the user to provide URLs in a re-run. Discovering review URLs from a domain is unreliable.
- For multi-location sites with >5 locations, audit one location page per region rather than one per location — the local audit pattern repeats per location, so a sample establishes the baseline. If location-page quality variance is the suspected issue, pair with `seo-content-audit` on a sample of location pages.
- AI-search local context (ChatGPT, Perplexity, AI Overviews) is **not** this skill's job — pair with `seo-geo` (URL-level GEO) or `seo-ai-search-share-of-voice` (domain-level brand visibility) for AI-search local visibility.
- The 18-day review velocity rule (Sterling Sky) is the most actionable single number from review-platform analysis. If the most recent review is >21 days old, that's a leading indicator of upcoming local-pack rank drop — flag as Critical regardless of star rating.
- Citation directories per vertical: load `references/local-citation-sources.md`. The list is curated to the directories that move the needle (Tier 1 + vertical-specific), not the long tail.
- Pair with `seo-technical-audit` if site-wide technical-SEO issues surface in step 8 — this skill scopes to local-relevant findings, not the full audit.
