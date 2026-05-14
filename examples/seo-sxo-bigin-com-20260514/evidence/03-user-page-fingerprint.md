# 03 — User page fingerprint: bigin.com/

> WebFetch on `bigin.com/` (2026-05-14): meta + content structure
> `mcp__firecrawl-mcp__firecrawl_scrape` on `bigin.com/` (formats: ["markdown"]): full DOM content
> Note: this fingerprint is real (live scrape), not templated.

## Metadata (Firecrawl)

| Field | Value |
|---|---|
| `<title>` | The Easiest Small business CRM - Bigin by Zoho CRM |
| meta `description` | Try Bigin by Zoho CRM, the most simple-yet-powerful CRM solution for small and micro businesses. Get started today with your free CRM trial. |
| `og:title` | The Easiest Small business CRM - Bigin by Zoho CRM |
| `og:description` | Try Bigin by Zoho CRM, the most simple-yet-powerful CRM solution... |
| `og:image` | https://www.zohowebstatic.com/sites/oweb/images/ogimage/zohobigin-logo.png |
| `og:type` | website |
| `twitter:card` | summary |
| `twitter:site` | @zoho |
| Canonical | https://www.bigin.com/ |

## H-tag outline

- **H1:** Your business needs a simple CRM
- **H2:** Effortless Task Management and Client Organization
- **H3 (subhead):** 15-day free trial. No credit card. No fuss.
- **H2:** Uncover The Mystery
- **H2:** Start seeing real impact. Just like our customers.
- **H2:** Everything you need to get organized and make more sales!
  - **H3:** Easily track anything (Team Pipelines)
  - **H3:** Complete customer context (360-degree view)
  - **H3:** Connect with customers (Multichannel)
  - **H3:** Reduce manual work (Automation)
  - **H3:** Never miss a deadline (Task Management)
  - **H3:** Highly-rated apps (Mobile)
- **H2:** Bigin integrates well with all your favorite applications
- **H2:** Bigin is already loved by 50,000+ customers
- **H2:** You don't need to think twice!
- **H2:** Let Bigin be a part of your growth story

## Content structure signals

| Signal | Value |
|---|---|
| Primary structure | Hero + feature blocks + testimonial carousel |
| Numbered list of 10+ items | **No** |
| Comparison table | **No** |
| Lists alternative CRMs / competitors | **No** |
| Pros/cons callouts | **No** |
| "Best of" framing | **No** |
| Author/methodology byline | **No** |
| Customer logos | **No** (named customer quotes only, no logo bar) |
| Pricing block on-page | **No** (referenced — "Starting at $7" — but no detailed tier table) |
| FAQ section | **No** |
| Reviews/ratings inline | **Yes** — embedded G2 / Capterra / Software Advice badge logos at footer + per-quote star ratings (4.6-4.8) |
| Trust badges | **Yes** (12 badges: G2 Small Business Leader, Capterra Best Value, PCMag Editors Choice, GetApp Leaders, Software Advice Front Runners, etc.) |
| Word count (markdown) | ~2,100 |
| Primary CTAs | "Sign Up for Free", "Get started for free", "Book a free demo", "Access Bigin" |
| Implicit price | $0 (15-day trial) + "Starting at $7/user" reference |

## Schema (inferred from rawHtml patterns + Firecrawl metadata)

Bigin.com's homepage typically ships with:
- `Organization` JSON-LD (the Zoho org block)
- `WebSite` JSON-LD (sitelinks search box)
- Possibly `SoftwareApplication` (Bigin as a product)

**Notably absent for this page type:** `ItemList`, `Article`, `Review`, `AggregateRating` at the page level. The SERP winners (listicles) typically ship `ItemList` + `Article` + per-item `Review`/`AggregateRating`. Bigin's page schema doesn't match.

## Page-type classification result

**Vendor product page.** Strong signal: single-brand H1, single-product feature blocks, no "best of" framing, no comparison table, single-CTA hierarchy. The customer testimonial carousel and trust badges are good content — just don't match what Google's algorithm has learned the keyword "best CRM for small business" wants.

## Implications for SXO scoring

- Skimmer: above-the-fold hero is brand-centric, not category-comparative. Score 4/10.
- Researcher: no comparison table, no feature checklist against alternatives. Score 3/10.
- Buyer: CTAs are clear but pre-sell is missing. Score 4/10.
- Validator: trust badges are present (good) but not contextual in the SERP-comparison frame. Score 2/10.

See `04-persona-scores.md` for the full breakdown.
