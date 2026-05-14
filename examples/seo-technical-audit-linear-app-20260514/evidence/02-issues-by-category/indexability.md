# Issues — Indexability

Source: `mcp__firecrawl-mcp__firecrawl_scrape` (extracts `<link rel="canonical">`, `<meta name="robots">`, `<html lang>` from rendered HTML) on 8 sample URLs.

## Canonical URLs

| URL | Canonical | Self-referencing? |
|---|---|:---:|
| https://linear.app/ | `https://linear.app/` | yes |
| https://linear.app/pricing | `https://linear.app/pricing` | yes |
| https://linear.app/method | `https://linear.app/method` | yes |
| https://linear.app/customers | `https://linear.app/customers` | yes |
| https://linear.app/customers/openai | `https://linear.app/customers/openai` | yes |

No `canonical_conflict`, no `canonical_external`, no `js_canonical_mismatch` detected on the sample. Canonical injection appears to be server-rendered (Next.js SSR) — no JS-only canonical risk.

## Robots meta

Every sampled URL has **no `<meta name="robots">` tag**. Default: `index, follow`.

## X-Robots-Tag header

No URL in the sample returned `X-Robots-Tag` in HTTP response headers. No HTTP-layer noindex conflict.

## Hreflang

No `<link rel="alternate" hreflang>` tags on any sampled page. `<html lang="en">` consistently. English-only is OK since Linear targets EN markets, but the structural absence means any future internationalisation requires a template change, not a content addition.

## Disallowed paths

robots.txt:
```
Disallow: /api/
Disallow: /cdn-cgi/
Allow: /api/og/
```

- `/api/` → 308 redirect (then Cloudflare returns auth-protected — fine, never indexable).
- `/api/og/` → public OG-image generator. Correctly allowed (used in `og:image` meta).
- `/cdn-cgi/` → 404 at root; Cloudflare-internal. Correctly disallowed.

## Summary

No indexability blockers. The site is fully crawlable on the marketing tier with consistent self-referencing canonicals and no rogue noindex directives. The single indexability-adjacent risk is **hreflang absent**, which doesn't matter today but constrains future i18n.
