# Lazy-loader detection

> Taxonomy adapted from `AgriciDaniel/claude-seo`'s `seo-images` skill (MIT). Five recognised mechanisms.

Classify each `<img>`'s lazy-loading mechanism by looking at attribute names and class signals. Report the result as `lazy_method` alongside `loading` in `images.csv` so a JS-loader-driven page isn't mis-flagged for missing `loading="lazy"`.

## Detection table

| `lazy_method` | Signal | Common stack |
|---|---|---|
| `native` | `loading="lazy"` HTML attribute | Modern browsers, plain HTML, most CMSes since 2022 |
| `perfmatters` | `data-perfmatters-src` or `data-perfmatters-srcset` attribute, OR `class` contains `perfmatters-lazy` | WordPress + Perfmatters plugin |
| `ewww` | `data-ewww-src` or `data-eio` attribute, OR `class` contains `lazyload-eio` | WordPress + EWWW Image Optimizer |
| `js-generic` | Any of `data-src`, `data-lazy-src`, `data-original`, `data-srcset` attributes, OR `class` contains `lazyload` / `lazyloaded` / `lazy` | Lazysizes, vanilla-lazyload, jQuery LazyLoad, custom rollups |
| `none` | Neither attribute nor class signal | Page is not lazy-loading this image |

## Detection order

Evaluate top-to-bottom — a `native` signal wins over a `js-generic` signal because native lazy-loading is the browser's authoritative behaviour. If a page has both a `loading="lazy"` attribute and a `data-src` attribute, it's almost certainly running both mechanisms in parallel (modern CMSes do this for browser-compat reasons); report `native` and note "JS-loader fallback also present" in the issue evidence.

## What the audit does with each

- `native` — count toward "lazy-loaded" percentage. No remediation needed unless the image is the LCP candidate (in which case → `image_lcp_lazy`).
- `perfmatters` / `ewww` / `js-generic` — count toward "lazy-loaded" percentage **via JS-loader**. Do not flag the image for missing `loading="lazy"`; the JS loader handles it. Audit-relevant findings:
  - If `loading="lazy"` is also present, that's the modern best practice (progressive enhancement) — no flag.
  - If the JS-loader requires JavaScript to display the image at all (e.g., `<noscript>` fallback is missing and `src` is a placeholder), flag `image_js_required` (Low) — search-engine crawlers may not see the real image src.
- `none` — for below-fold images this is `image_below_fold_eager`. For above-fold / LCP, this is correct behaviour.

## Edge cases

- **Cloudinary / Imgix `<img>` with `data-cld-*` or `data-imgix-*` attributes.** These are configuration for the CDN's JS plugin, not lazy-loading. Don't classify as `js-generic`. Treat as `native` if `loading="lazy"` is also set, else `none`.
- **`<picture>` with lazy sources.** The lazy attribute belongs to the inner `<img>`. Detect on the `<img>`, not the `<picture>` or `<source>`.
- **Fragmented WordPress themes.** Some themes lazy-load with one mechanism and ship Perfmatters on top — you may see both `data-perfmatters-src` and `data-src`. Report the more specific one (`perfmatters` over `js-generic`).
- **Intersection-observer-based vanilla rollups** without any `data-*` attribute (some frameworks inject src on intersection from a `<noscript>` tag). Hard to detect without runtime data. If `src` is a placeholder pattern (`data:image/svg+xml...`, `placeholder.png`, transparent 1×1), classify as `js-generic`.

## Why this matters

The `loading="lazy"` HTML attribute is universally supported now, but plenty of production sites still use a JS lazy-loader as primary mechanism — either for control over the offset threshold, for `<picture>` `<source>` lazy-loading (which native doesn't reach into), or for compatibility with older themes. Mis-flagging those as "missing lazy-loading" wastes engineering time chasing a non-bug.
