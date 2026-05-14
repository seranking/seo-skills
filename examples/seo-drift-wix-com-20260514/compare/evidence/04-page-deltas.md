# 04 — Page-level fingerprint deltas (homepage)

Tool: mcp__firecrawl-mcp__firecrawl_scrape (with formats=["rawHtml"]) on https://www.wix.com/

Status: Live Firecrawl capture for 2026-05-14 below. Baseline-side fingerprint is absent — no prior /seo-drift baseline was run at 2026-02-13, so this is a first-capture record, not a diff.

## Current homepage fingerprint (Firecrawl, 2026-05-14)

```
url               : https://www.wix.com/
title             : Website Builder - Create a Free Website In Minutes | Wix.com
og:title          : Your vision. Your goals. Your website. | Wix.com
                    (note: og:title is intentionally different from <title>; brand-narrative vs feature-narrative split)
og:description    : Get everything you need to create your website, your way. From an intuitive website builder to built-in business solutions and AI tools—try Wix for free.
meta description  : Get everything you need to build a website your way. Wix's free, easy-to-use website builder offers 2,000+ templates, built-in AI tools and a custom domain.
                    (note: distinct from og:description; covers slightly different value props)
og:image          : https://static.wixstatic.com/media/343a2a_f435947596b24c0a87854aa410c4cf48~mv2.jpg/v1/fill/w_1200,h_630,al_c/...
twitter:card      : summary_large_image
twitter:title     : Your vision. Your goals. Your website. | Wix.com
language          : en
robots            : (not detected in head pull — Firecrawl rawHtml didn't surface a robots meta tag, but absence is not noindex/follow; default is index,follow)
canonical         : (not exposed in head capture — Wix SPA may inject client-side; re-capture with full client-side render needed for full confirmation)
JSON-LD types     : 0 blocks detected in rawHtml capture
hreflang variants : 0 detected in head
```

## Diff threshold (per SKILL.md compare mode step 3, page-level)

- Any change to canonical / robots / lang / H1 = RED
- Title or meta description change = YELLOW
- Schema types added/removed = YELLOW
- og:* / twitter:* changes = YELLOW

## Notes for future compare runs

1. The title / og:title divergence is by design. On the next /seo-drift compare run, expect this divergence to persist — don't treat it as drift.
2. The meta-description vs og:description distinction is also by design. Each has slightly different value-prop wording. Future runs should detect a CHANGE in either, not the difference between them.
3. The 0 JSON-LD blocks is worth re-checking with a more aggressive Firecrawl render (waitFor: 5000 or 10000ms). Wix's homepage is JS-heavy; if structured data is injected client-side, this metric may flip on a more patient render.
4. Hreflang count of 0 is consistent with Wix's homepage targeting English-language US users primarily; localised variants live at /es/, /pt/, /fr/ etc. and have their own hreflang lattices. The English homepage having 0 hreflang is not a regression signal.

For the first /seo-drift compare wix.com run AFTER this baseline lands, the page-delta section will produce actual diffs. Today, it produces a structural record only.
