# Content snapshot — stripe.com/blog/rate-limiters

Source: `mcp__firecrawl-mcp__firecrawl_scrape` (markdown + metadata) + `curl -s` (rawHtml for JSON-LD inspection). 2026-05-14.

## URL + canonical
- URL audited: https://stripe.com/blog/rate-limiters
- Canonical: `https://stripe.com/blog/rate-limiters` (self-referencing)
- HTTP status: 200
- Content type: `text/html; charset=utf-8`

## Page metadata

| Field | Value |
|---|---|
| `<title>` | "Scaling your API with rate limiters" |
| `<meta name="description">` | "Online payment processing for internet businesses. Stripe is a suite of payment APIs..." (generic site-wide description, NOT article-specific) |
| `<meta name="robots">` | absent (defaults to index, follow) |
| Language | en-US |
| `og:url` | https://stripe.com/blog/rate-limiters |
| `og:title` | "Scaling your API with rate limiters" |
| `og:description` | (generic site-wide; not article-specific) |
| `og:image` | `?q=80` (truncated/broken — missing source URL) |
| `twitter:card` | `summary_large_image` |
| `twitter:site` | `@stripe` |
| `twitter:title` | "Scaling your API with rate limiters" |
| `twitter:image` | `?q=80` (truncated/broken) |

Issues: meta description is the site-wide payments description, not article-specific. og:image and twitter:image are broken (truncated `?q=80` with no base URL). These are content-blocking issues for social previews and rich-result eligibility.

## JSON-LD blocks

1 block detected:

```json
{
  "@context": "https://schema.org",
  "@type": ["Article", "BlogPosting"],
  "headline": "Scaling your API with rate limiters",
  "image": [],
  "datePublished": "2017-03-30T00:00-08:00",
  "author": [{
    "@type": "Person",
    "name": "Paul Tarjan",
    "url": "https://twitter.com/ptarjan"
  }]
}
```

Issues:
- `image: []` — empty array; should be a populated image URL.
- `dateModified` — absent. Article is 9 years old; lack of modification timestamp signals "static" to crawlers.
- `publisher` — absent. Should be:
  ```json
  "publisher": {"@type": "Organization", "name": "Stripe", "logo": {"@type": "ImageObject", "url": "..."}}
  ```
- `author.url` — points to Twitter only. No `sameAs` array. No `jobTitle` field. Weak entity disambiguation.
- No `about` field. The article topic ("rate limiting", "API scaling") should be declared as `about: {"@type": "Thing", "name": "Rate limiting"}`.
- No `wordCount` field.

## Page-type detection

Cross-references:
- URL pattern: `/blog/{slug}` — blog post.
- H1: "Scaling your API with rate limiters" — explainer/how-to phrasing.
- JSON-LD `@type`: `[Article, BlogPosting]` — confirms blog post.
- Structure: intro + 4 named rate-limiter types (each as H3) + "Building rate limiters in practice" + Conclusion.

**Classified as: hybrid explainer + how-to listicle.** The 4-strategy enumeration is the listicle backbone; the surrounding intro + Building-in-practice section is explainer-shaped.

Word-count floor (from `references/core-eeat.md` → "Word-count floors by page type"):
- explainer: 1,500
- listicle: 1,200

Applied floor: **1,500** (explainer baseline, conservative).

## Word count

Estimated article body: **~1,500-1,800 words**. Meets the explainer floor.

(Method: the rendered markdown was ~3,150 words total, but ~1,300-1,500 of those are nav/footer/country-list boilerplate. The actual prose article — intro through conclusion, excluding internal-link nav — is ~1,500-1,800 words.)

## Structural elements

| Element | Count | Notes |
|---|---:|---|
| H1 | 1 | "Scaling your API with rate limiters" |
| H2 | 3 | "Rate limiters and load shedders", "Using different kinds of rate limiters in concert", "Building rate limiters in practice", "Conclusion" (4 if counting conclusion) |
| H3 | 4 | one per rate-limiter type |
| Images | 4 | all production-traffic graphs — labelled "Graph 1-4" |
| Code blocks | 0 inline | code linked via GitHub gist |
| Tables | 0 | no comparison table |
| Internal links | 1 | `/blog/idempotency` |
| External links | ≥6 | Wikipedia ×2, IETF RFC ×2, AWS ElastiCache, GitHub gist, Twitter |
| Internal author page link | 0 | author URL is twitter.com |

## Byline / author signals

- **DOM byline:** `[Paul Tarjan](https://twitter.com/ptarjan)` — link to Twitter, not to an internal author page.
- **`<a rel="author">`:** not present (count: 0).
- **`<meta name="author">`:** not present.
- **JSON-LD `author`:** present (one Person object with name + Twitter url).
- **"Engineering" tag** appears next to the byline — implies Stripe Engineering attribution.

## Date signals

- **Visible date:** "March 30, 2017" rendered at the top.
- **`datePublished` schema:** "2017-03-30T00:00-08:00".
- **`dateModified` schema:** absent.
- **"Last reviewed" / "Updated" notice:** absent.

## Country / locale variants

Sitemap exposes 40+ locale variants:
```
en (default): https://stripe.com/blog/rate-limiters
au:           https://stripe.com/au/blog/rate-limiters
de:           https://stripe.com/de/blog/rate-limiters
fr:           https://stripe.com/fr/blog/rate-limiters
... (40+ more)
```

Translation/localisation tier is mature. Not relevant to this audit since the target keyword is US-English.
