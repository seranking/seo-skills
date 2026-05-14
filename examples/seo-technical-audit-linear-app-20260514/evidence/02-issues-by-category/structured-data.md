# Issues — Structured data

Source: `mcp__firecrawl-mcp__firecrawl_scrape` (returns full rendered HTML; greps `<script type="application/ld+json">` blocks) on 5 sample URLs.

## Findings

**JSON-LD blocks observed on the marketing site: zero.**

| URL | JSON-LD blocks | OpenGraph type | twitter:card |
|---|---:|---|---|
| https://linear.app/ | 0 | (absent) | summary_large_image |
| https://linear.app/pricing | 0 | (absent) | summary_large_image |
| https://linear.app/method | 0 | (absent) | summary_large_image |
| https://linear.app/customers | 0 | (absent) | summary_large_image |
| https://linear.app/customers/openai | 0 | (absent) | summary_large_image |

This is the single most consequential finding in the audit. The marketing site has zero machine-readable structured data, which means:
1. **No rich SERP results** — no Sitelinks Search Box, no Product/Offer rich result on /pricing, no Article rich result on case studies.
2. **AI Search citation gap** — LLMs that crawl with structured-data parsing (Bing/ChatGPT, Perplexity, Google AI Overview) cannot extract entities deterministically. Linear is mentioned in LLM outputs (it's a well-known brand), but the cited *page* is less likely to be Linear's own page when no schema markup signals "this is the canonical answer."
3. **No `og:type` declared** — even basic OpenGraph type signals are missing on case-study pages, which weakens social-share preview quality.

## Recommended schema additions (by page type)

### Homepage (`/`)
```jsonld
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Linear",
  "url": "https://linear.app",
  "logo": "https://linear.app/static/og/homepage.jpg",
  "sameAs": [
    "https://twitter.com/linear",
    "https://www.linkedin.com/company/linear",
    "https://github.com/linear"
  ],
  "description": "Purpose-built for planning and building products with AI agents."
}
```

Plus `SoftwareApplication`:
```jsonld
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Linear",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web, iOS, Android, macOS",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
}
```

### Pricing (`/pricing`)
4× `Product` + `Offer` (Free, Basic $10, Business $16, Enterprise — see `/pricing` rendered tier table). Currently the dynamic pricing is purely visual; no machine-readable price.

### Customer stories (`/customers/{slug}`)
```jsonld
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{customer story title}",
  "author": {"@type": "Organization", "name": "Linear"},
  "publisher": {"@type": "Organization", "name": "Linear", "logo": {"@type": "ImageObject", "url": "https://linear.app/static/og/homepage.jpg"}},
  "datePublished": "{ISO 8601}",
  "dateModified": "{ISO 8601}",
  "about": {"@type": "Organization", "name": "{customer name}"},
  "image": "{og:image URL}"
}
```

### Blog (`/blog/{slug}`) and Changelog (`/changelog/{slug}`)
`BlogPosting` with `author` (a real Person), `datePublished`, `dateModified`.

### Site-wide
`BreadcrumbList` on every leaf page (current navigation has implicit breadcrumb pattern: Home › Customers › OpenAI; surface it in markup).

## Next step
Hand to `seo-schema` skill to generate paste-ready blocks per page type, then validate via Google Rich Results Test.
