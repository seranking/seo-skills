# Key pages — per-URL issues

Source: `mcp__firecrawl-mcp__firecrawl_scrape` (page-level head extraction) + `curl -sI` (HTTP response headers) for 5 sample URLs. The skill normally uses `DATA_getIssuesByUrl` on the SE Ranking audit's top-5-traffic pages; here we sample structurally-representative URLs since SE Ranking is unauthenticated.

## `/` (homepage)

| Signal | Value | Issue |
|---|---|---|
| Title | "Linear – The system for product development" (45 chars) | `title_short` (Medium) — target 55-60 |
| Meta description | "Purpose-built for planning and building products with AI agents." (61 chars) | `description_short` (High) — target 140-155 |
| Canonical | `https://linear.app/` (self) | none |
| H1 count | 2 (responsive duplication: visible + hidden variant) | `duplicate_h1` (Medium) |
| og:image | `https://linear.app/static/og/homepage.jpg` | `og_image_dimensions_missing` (no width/height) |
| og:title | "Linear – The system for product development" | none |
| og:type | absent | `og_type_missing` |
| twitter:card | `summary_large_image` | none |
| JSON-LD | **0 blocks** | `jsonld_missing` (Critical) |
| Robots meta | absent (defaults to index, follow) | none |
| Hreflang | absent | site-wide |
| HTML lang | `en` | none |

## `/pricing`

| Signal | Value | Issue |
|---|---|---|
| Title | "Pricing – Linear" (17 chars) | `title_short` (Medium) |
| Meta description | "Use Linear for free with your whole team. Upgrade to enable unlimited issues, enhanced security controls, and additional features." (130 chars) | none — within target |
| Canonical | self | none |
| og:image | `https://linear.app/api/og/generic?title=Pricing&v=3` (dynamically generated) | clever — uses an `/api/og/*` route to generate OG cards; missing width/height |
| JSON-LD | **0 blocks** | should have `Product` + `Offer` for the 4 pricing tiers (Free, Basic $10, Business $16, Enterprise) |
| Robots meta | absent | none |

Comment: pricing is the highest-intent page on the marketing site (top conversion target). Missing `Product`/`Offer` schema means Linear cannot win the Price-Range rich result, and LLMs cannot extract structured pricing from the page reliably.

## `/customers/openai` (sample customer story)

| Signal | Value | Issue |
|---|---|---|
| Title | "Why OpenAI chose Linear and scaled to 3,000 users" (52 chars) | within target |
| Meta description | "OpenAI is at the forefront of artificial intelligence research, developing systems that can understand and generate human-like text, code, and images. Founded in 2015, they've grown from a small research lab to a technology pioneer with over 3,000 employees, shipping products used by hundreds of millions worldwide." (~310 chars) | `description_long` — Google will truncate at ~155 chars |
| Canonical | self | none |
| og:image | `https://linear.app/api/og/customers?slug=openai` | dynamic, no width/height |
| og:type | absent | `og_type_missing` — should be `article` for case studies |
| JSON-LD | **0 blocks** | should have `Article` + `Organization` (OpenAI as `about`) + `Person` (author) |
| Robots meta | absent | none |
| Canonical | `https://linear.app/customers/openai` | matches URL |

Comment: customer-story pages have the strongest E-E-A-T narrative on the site (named customer, named outcome, measured impact). They are also the most likely page type to be cited by LLMs in `"linear vs jira"`, `"is linear good for enterprise"`, `"who uses linear"` prompts. Adding `Article` schema + `about: {Organization: OpenAI}` makes them machine-extractable.

## `/method`

| Signal | Value | Issue |
|---|---|---|
| Title | "Linear Method – Practices for building" (38 chars) | `title_short` (Medium) |
| Meta description | "The quality of a product is driven by both the talent of its creators and how they feel while they're crafting it..." (~250 chars) | `description_long` |
| Canonical | self | none |
| og:image | dynamic via `/api/og/method` | no width/height |
| JSON-LD | **0 blocks** | The Method docs are an opinionated PM methodology — they would be a strong fit for `Article` + `EducationalOccupationalProgram` schema |
| Robots meta | absent | none |

## `/changelog`

| Signal | Value | Issue |
|---|---|---|
| Sub-pages in sitemap | 236 changelog URLs | — |
| Sub-pages with lastmod < 2024-01-01 | 50+ entries | `sitemap_stale_lastmod` (High) |
| JSON-LD per entry | **0 blocks observed** | should be `BlogPosting` schema per changelog entry |
| Robots meta | absent | none |

Comment: the changelog accounts for ~26% of the sitemap (236/896) and is a key crawl-budget drag when ~50 entries are 2-5 years old without refresh. Two options:
1. **Archive:** move pre-2024 changelog entries to a separate area not in the sitemap.
2. **Schema + refresh:** add `BlogPosting` schema with `datePublished` + `dateModified`. Crawlers will weight `dateModified` over sitemap `lastmod` when both are present.
