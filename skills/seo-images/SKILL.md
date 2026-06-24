---
name: seo-images
description: Image SEO audit for a URL or domain. Pulls raw image inventory via Firecrawl, then audits alt-text quality, modern-format coverage (WebP / AVIF), responsive sizing (`srcset` / `sizes`), lazy-loading and LCP signals (`loading`, `fetchpriority`, `decoding`), CLS-safe dimensions, descriptive file names, and `ImageObject` JSON-LD. Optional PageSpeed Insights cross-reference for real byte-saving estimates. Produces a prioritised remediation list plus paste-ready picture-element markup and `ImageObject` schema. Distinct from `seo-technical-audit` (which surfaces audit-flagged image issues at the site level) and from `seo-schema` (which generates page-level JSON-LD but not image-specific markup). Use when the user asks for "image SEO", "image audit", "alt-text audit", "WebP coverage", "AVIF", "responsive images", "lazy loading", "CLS images", "image schema", "ImageObject", "image rich results", "licensable images", or "optimise images".
---

# Image SEO Audit

A focused, page-level (or domain-sample) audit of every `<img>` and `<picture>` on the target. Surfaces alt-text issues, format gaps (WebP/AVIF coverage), responsive-image gaps (`srcset` / `sizes`), LCP and CLS risk, and missing `ImageObject` markup. Output is a prioritised remediation list plus paste-ready `<picture>` and JSON-LD snippets.

> **Adapted from [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo)'s `seo-images` skill** (MIT). Rubric, lazy-loader taxonomy, and severity ladder track the upstream implementation; data sources are wired to this catalogue's SE Ranking / Firecrawl / Google APIs stack.

## Prerequisites

- **Required for inventory:** `mcp__firecrawl-mcp__firecrawl_scrape` (raw HTML access). `WebFetch` returns markdown only — every `<img>` attribute (`srcset`, `sizes`, `loading`, `fetchpriority`, `width`, `height`, `data-src*` lazy variants) is stripped before the skill ever sees it. Without Firecrawl the audit cannot run. Install via `bash extensions/firecrawl/install.sh`.
- **Optional (PSI byte-saving estimates):** `google-api.json` configured (Tier 0 — API key only). When present, step 9 runs and adds real Lighthouse `wastedBytes` per image to the remediation list.
- **Optional (SE Ranking audit cross-reference):** SE Ranking MCP server connected and a recent audit for the domain. When present, step 10 elevates image-related audit issues onto the same remediation list.
- User provides: a target URL (single-page audit) or a domain (sampled audit). For domains, the skill confirms how many pages to sample before spending Firecrawl credits.

## Process

1. **Validate target & preflight.** Normalise the URL (strip trailing slash, decode IDN). Resolve mode:
   - **URL mode** (default for inputs that look like a single page): the target is one URL. Cost: 1 Firecrawl credit + optional PSI calls.
   - **Domain mode** (input is a bare domain or the user explicitly asks for a domain-wide audit): map first, then scrape a sample.
   - **Preflight checks** (mirror `skills/seo-firecrawl/references/preflight.md` where it applies):
     - Confirm Firecrawl is connected. If not, abort with the install command and stop.
     - If Google APIs are wired up (`~/.config/seo-skills/google-api.json` present), record the detected tier; step 9 will use it. If not, mark step 9 as skipped.
     - If SE Ranking MCP is connected and a recent audit exists for the domain, record the audit ID; step 10 will use it. If not, mark step 10 as skipped.

2. **Gather image inventory** `mcp__firecrawl-mcp__firecrawl_scrape` (URL mode) or `firecrawl_map` + `firecrawl_scrape` (domain mode)
   - **URL mode:** scrape the target with `formats: ["html", "markdown"]` and `onlyMainContent: false` (we want nav/footer images too — hero logo, footer trust badges, decorative imagery all matter for the audit). For SPAs, pass `waitFor: 2000` so lazy-injected images appear in the rendered DOM. Parse every `<img>` and every `<picture>` from the returned `html`. Capture per image:
     - `src`, `srcset`, `sizes`, `alt`, `loading`, `fetchpriority`, `decoding`, `width`, `height`, `role`, `aria-hidden`
     - Lazy-loader attributes: `data-src`, `data-srcset`, `data-lazy-src`, `data-original`, `data-perfmatters-src`, `data-perfmatters-srcset`, `data-ewww-src`, `data-eio`
     - Class signals: `lazyload`, `lazyloaded`, `lazy`, `perfmatters-lazy`, `lazyload-eio`
     - Parent `<picture>` `<source>` entries: `type`, `srcset`, `media`
     - Resolved absolute URL (for cross-origin / CDN detection)
   - **Domain mode:** run `firecrawl_map` (default `limit: 500`, hard cap; cost: ~0.5 credit per discovered URL — surface the estimate before running). From the URL list, select a sample of up to 10 pages: homepage, plus the top traffic landing pages (from `DATA_getDomainKeywords`'s page aggregation if SE Ranking is connected, otherwise the deepest-nested URLs found in the sitemap — these are usually the content pages, not category indexes). Confirm the sample list and credit cost before scraping. Then scrape each (1 credit per page). Inventory is the union of every image on the sampled pages.
   - **CSS background-images:** flag as a known blind spot. We don't audit `background-image: url(...)` in stylesheets — those are not crawlable as content images by Google and don't get image-search visibility. Surface "{n} likely background-images detected (computed style references) — out of scope for this audit; review separately if hero/feature images are CSS-based" in the synthesis.

3. **Alt-text audit**
   - Load `references/image-checks.md` § Alt text. For each image:
     - **Presence:** missing `alt` (not `alt=""` — the empty-string form is valid for purely decorative images). Severity High.
     - **Decorative-but-not-marked:** `alt=""` is fine only if the image is genuinely decorative. Flag images with `alt=""` that also have a non-decorative `src` (e.g. product photo path, hero image path) as "verify decorative intent" (Medium).
     - **Generic text:** `alt` value matches a generic pattern — bare filename (`image.jpg`, `IMG_1234.png`), single generic noun (`photo`, `picture`, `image`, `banner`), CTA copy (`click here`, `read more`, `learn more`). Severity High.
     - **Length:** `alt` outside the 10–125 character window. Below 10 → Medium (probably not descriptive). Above 125 → Low (likely too verbose; screen readers truncate around there).
     - **Keyword stuffing:** the same keyword token appears 3+ times in the alt, or the alt is >50% keyword tokens. Severity Medium.
     - **Identical alt across multiple images on the page:** flag as a templating bug (Medium) — every product photo on a PDP should not share the same alt.

4. **Format coverage (WebP / AVIF)**
   - For each image, classify its served format from `src` extension (`.webp`, `.avif`, `.jpg`/`.jpeg`, `.png`, `.gif`, `.svg`) and `<picture>` `<source>` `type` attributes (`image/avif`, `image/webp`).
   - Compute three coverage metrics for the page (or domain sample):
     - **% images served as WebP or AVIF directly** (via the chosen `<img src>` or chosen `<picture>` `<source>`).
     - **% images wrapped in `<picture>` with at least one modern-format `<source>`** (progressive enhancement — fallback chain).
     - **% images stuck on legacy formats** (JPEG / PNG / GIF) with no modern alternative.
   - Per-image flags:
     - Legacy format with no `<picture>` modern alternative → `image_legacy_format` (Medium).
     - Animated GIF over 500 KB → recommend video (`<video autoplay muted loop playsinline>`) instead (Medium — performance + LCP impact). Source: Google PSI `efficient-animated-content` audit.
     - SVG used for photographic content → `image_svg_misuse` (Low — file size will be enormous; SVG is for icons/illustrations).
   - **JPEG XL note.** Chromium announced restoration of JPEG XL decoding (Rust-based) in November 2025 but it's not yet in Chrome stable. Surface as a Tips note: not actionable today, monitor for 2026.

5. **Responsive coverage (`srcset` / `sizes`)**
   - For each non-SVG raster image:
     - Missing `srcset` → `image_no_srcset` (Medium). Browser cannot pick a size-appropriate file; mobile users download desktop-sized images.
     - `srcset` present but no `sizes` and not inside `<picture>` → `image_no_sizes` (Medium). Browser falls back to viewport width assumptions and can pick the wrong candidate.
     - `srcset` declared but all candidates are the same width descriptor (`1x` only, or all `w` values within 100 px of each other) → `image_srcset_useless` (Low).

6. **Lazy loading & LCP signals**
   - For each image, classify the lazy-loading mechanism using `references/lazy-loaders.md`'s taxonomy: `native` / `perfmatters` / `ewww` / `js-generic` / `none`. Report `lazy_method` alongside `loading` so a JS-loader-driven page isn't mis-flagged for missing `loading="lazy"` (the native attribute is intentionally absent there — the loader handles it).
   - **LCP-candidate heuristic.** The LCP image is typically the first `<img>` that:
     - Appears above the fold on a typical mobile viewport (no exact viewport without rendering; heuristic = first `<img>` in the rendered DOM that is not inside a `<header>` / `<nav>` / `<aside>` and has no `loading="lazy"` ancestor),
     - Has a large rendered area (width × height attributes both ≥ 300, or `<picture>` `<source>` with viewport-spanning `sizes`).
   - For the LCP candidate:
     - `loading="lazy"` set → `image_lcp_lazy` (High). Lazy-loading the LCP image directly harms LCP.
     - No `fetchpriority="high"` → `image_lcp_no_fetchpriority` (Medium). Lighthouse's `prioritize-lcp-image` audit; setting `fetchpriority="high"` moves the LCP image to the front of the browser's network queue.
   - For below-fold images (not the LCP candidate, not inside the first viewport):
     - Neither native `loading="lazy"` nor any JS-loader signal → `image_below_fold_eager` (Medium). Below-fold images should defer.
     - Missing `decoding="async"` → `image_no_decoding_async` (Low). Async decode prevents image decoding from blocking the main thread for non-LCP images.

7. **CLS dimensions**
   - For each image:
     - Missing both `width` and `height` attributes AND no inline `aspect-ratio` style → `image_unsized` (High). The browser cannot reserve space; the image will shift content when it loads. Matches Lighthouse `unsized-images`.
     - `width` and `height` present but the ratio mismatches the actual displayed ratio by >5% → `image_aspect_mismatch` (Low). Layout will shift on load.
   - The fix for both is the same: set `width` and `height` attributes to the image's intrinsic dimensions, and let CSS handle responsive scaling.

8. **File-name quality**
   - For each image's resolved URL, extract the filename. Flag:
     - Camera-default names (`IMG_xxxx`, `DSC_xxxx`, `DSCN_xxxx`, `P_xxxx`, `Photo_xx`) → `image_camera_filename` (Low).
     - Random-hash names (`a3f9b2c.jpg`, `0e8d1f7.webp` — hex/base64 patterns with no human-readable tokens) → `image_hash_filename` (Low). Common with image CDNs; verify there's no SEO-friendly version available.
     - All-uppercase or all-underscore filenames → `image_filename_style` (Low). Convention is lowercase + hyphens.
   - Don't flag every CDN-served image as a problem — many CMSes hash filenames for cache busting and that's fine. The signal is meaningful when paired with a missing or generic `alt` on the same image (the page has no signal at all about what the image depicts).

9. **`ImageObject` JSON-LD: detect, validate, generate**
   - **Detect:** parse every `<script type="application/ld+json">` block returned by Firecrawl. Find existing `ImageObject` blocks — either top-level (for image-search rich results) or nested under `Article.image`, `Product.image`, `Recipe.image`, etc.
   - **Validate** against Google Images' guidelines (see `references/image-checks.md` § ImageObject for the field list). For a top-level `ImageObject`:
     - Required: `@context`, `@type: ImageObject`, `contentUrl` (the image URL), `creator` or `copyrightHolder`.
     - Recommended for licensable-images rich results: `license` (URL to the license terms), `acquireLicensePage` (URL where users can buy/license the image), `creditText` (how the creator should be credited).
     - Common mistakes: `url` instead of `contentUrl`, `author` as a bare string instead of a `Person` / `Organization` object, dimensions as strings instead of `Number`.
   - **Generate:** for each image that doesn't already have an `ImageObject` block AND that meets the "worth marking up" threshold (the image is the page's hero / first-fold and the page has a clear creator/owner), produce a paste-ready block from `templates/image-object.json`, filling in fields from the live HTML. Mark unresolved fields as `{REPLACE: ...}`. The generated file is emitted as `02-remediation/image-object.jsonld` (the `.jsonld` extension marks it as a deliverable for `<script type="application/ld+json">`).
   - **Don't generate `ImageObject` for every `<img>`.** It's noise. Limit to the hero image and any image that should be eligible for licensable-images rich results.

10. **Optional: PageSpeed Insights byte savings** *(only if `~/.config/seo-skills/google-api.json` is present, Tier ≥ 0)*
    - Run `python3 scripts/pagespeed_check.py "{url}" --strategy=mobile --json` and `--strategy=desktop --json` (2 API calls per target URL — within PSI's 25k/day free quota).
    - Pull the following audits from the JSON response and merge per-image `wastedBytes` into the remediation list:
      - `modern-image-formats` — bytes savable by serving WebP/AVIF (overlaps with step 4; PSI's number is authoritative).
      - `uses-optimized-images` — bytes savable by re-compressing.
      - `uses-responsive-images` — bytes savable by serving size-appropriate files (overlaps with step 5).
      - `offscreen-images` — bytes deferrable by lazy-loading below-fold images (overlaps with step 6).
      - `unsized-images` — page elements missing dimensions (cross-checks step 7).
      - `prioritize-lcp-image` — confirms or contradicts the step-6 LCP-candidate heuristic and gives PSI's authoritative LCP element.
      - `efficient-animated-content` — confirms animated-GIF flagging from step 4.
    - Each PSI audit returns `details.items[]` with `url` and `wastedBytes`. Join on image URL (resolved absolute) and tag each remediation row with `psi_wasted_bytes` so the prioritised list orders by real savings, not heuristic severity alone.
    - **If PSI is configured but returns no audits** (likely a 4xx — usually a private/protected URL Lighthouse can't load): note "PSI: could not analyse {url} ({reason})" and continue with non-PSI signals.

11. **Optional: SE Ranking audit cross-reference** *(only if SE Ranking MCP is connected and a recent audit exists)*
    - `DATA_listAudits` → find the most recent audit for the domain. If none exists or it's >30 days old, skip this step (don't trigger a new audit from the image skill — that's `seo-technical-audit`'s call to make).
    - For each image-related audit code, `DATA_getAuditPagesByIssue`:
      - `images_oversized` (or whatever SE Ranking's current code is for "uncompressed images")
      - `images_no_alt`
      - `images_broken` (404 / 5xx image URLs)
      - `images_no_dimensions` (CLS)
    - Merge findings: for any image flagged by both the audit and this skill, elevate severity by one step. For any audit-flagged URL that the Firecrawl sample didn't include, list it under "Audit-flagged pages not in this sample" with a recommendation to re-run on those URLs specifically.

12. **Synthesise** `IMAGES.md`. Build the remediation table sorted by:
    1. Severity (Critical → High → Medium → Low),
    2. Within severity: PSI `wastedBytes` descending (when PSI ran), else affected-image count descending,
    3. Then alphabetical by issue code.

## Output format

Create a folder `seo-images-{target-slug}-{YYYYMMDD}/` with:

```
seo-images-{target-slug}-{YYYYMMDD}/
├── IMAGES.md                       (synthesised audit + remediation list — primary deliverable)
├── images.csv                      (every image with all audit columns — engineering pastes into Jira)
├── 01-inventory.md                 (per-page image list with raw attributes)
├── 02-remediation/
│   ├── picture-snippets.md         (paste-ready <picture> blocks for the top N legacy-format images)
│   ├── alt-text-rewrites.md        (suggested alts for missing / generic-text cases)
│   └── image-object.jsonld         (generated ImageObject for the hero image, if applicable)
├── 03-psi-report.md                (PSI image-audit breakdown — only if Google APIs configured)
└── 04-audit-cross-ref.md           (image-related SE Ranking audit issues — only if step 11 ran)
```

`IMAGES.md` follows this shape:

```markdown
# Image SEO Audit: {URL or domain}

> Snapshot dated {YYYY-MM-DD} · Mode: {URL | domain-sample (n pages)} · Images analysed: {n}

## Coverage at a glance

| Metric | Result |
|---|---|
| Total images | {n} |
| Missing alt text | {n} ({pct}%) |
| Generic / templated alt text | {n} ({pct}%) |
| Modern format (WebP/AVIF) coverage | {pct}% direct, {pct}% via `<picture>` fallback |
| `srcset` present (responsive) | {pct}% |
| `loading` strategy detected | native: {pct}% · JS-loader: {pct}% · none: {pct}% |
| LCP image flagged | {yes/no — element + risk} |
| Unsized (CLS risk) | {n} ({pct}%) |
| `ImageObject` JSON-LD | {present / partial / missing} |

## Top 10 remediations (severity × byte savings)

| Rank | Issue code | Severity | Images | PSI wastedBytes | Fix | Effort |
|---|---|---|---|---|---|---|
| 1 | image_lcp_lazy | High | 1 | 480 KB | Remove `loading="lazy"`; add `fetchpriority="high"` | S |
| 2 | image_legacy_format | Medium | 14 | 2.1 MB | Convert to WebP, wrap in `<picture>` with fallback | M |
| ... |

## By category

### Alt text ({n} issues)
- {n} images missing `alt` entirely. See `02-remediation/alt-text-rewrites.md` for suggested rewrites.
- {n} images with generic alt (`image.jpg`, `photo`, "click here").
- {n} images with identical alt across multiple images (templating bug).

### Format coverage ({pct}% modern)
- {n} images stuck on legacy JPEG/PNG. See `02-remediation/picture-snippets.md`.
- {n} animated GIFs >500 KB — recommend video.

### Responsive sizing ({pct}% have `srcset`)
- {n} images without `srcset`.
- {n} images with `srcset` but no `sizes`.

### Lazy loading & LCP
- LCP candidate: `{img src or selector}` — {risk summary}.
- {n} below-fold images loading eagerly.
- {n} images missing `decoding="async"`.

### CLS dimensions ({n} unsized)
- {n} images without `width`/`height` attributes.
- {n} images with aspect-ratio mismatches.

### File names ({n} flagged)
- {n} camera-default names (IMG_xxxx).
- {n} hash-only filenames coupled with a missing/generic alt.

### ImageObject JSON-LD
- Currently present: {none | block-level on hero | partial}.
- Recommended additions: {none | hero-image ImageObject for licensable-images rich result}.

## Paste-ready remediations

See `02-remediation/`:
- `picture-snippets.md` — `<picture>` blocks for the top N legacy-format images.
- `alt-text-rewrites.md` — alt-text rewrites for missing / generic cases.
- `image-object.jsonld` — `ImageObject` block for the hero image.

## Out of scope for this skill

- **File-level optimisation** (running `cwebp` / `exiftool` / ImageMagick / `ffmpeg` against the actual binary). This skill audits markup and references; converting and re-uploading the files is engineering work — see the pipeline note in `references/image-checks.md` § Optimisation pipeline if you want a starting recipe.
- **CSS background-images.** {n} likely background-image references detected via computed style, but not audited. They don't appear in Google Images and aren't subject to the `<img>`-tag rubric.
- **Site-wide audit at >10 pages.** This is a sampled audit. For domain-level "every image on every page", run `seo-technical-audit` first to surface the audit-grade signals, then come back here for sample-level deep audit.

## Recommended next steps

- {`seo-technical-audit` if domain-wide image issues need to be quantified — uncompressed-images counts, etc.}
- {`seo-schema` if `ImageObject` was generated and the page also needs `Article` / `Product` / etc. markup.}
- {`seo-google pagespeed` for the full Lighthouse breakdown (this skill only pulls image-specific audits).}
```

`images.csv` columns: `page_url,image_url,alt,alt_length,alt_issue,format,in_picture,modern_source,srcset,sizes,loading,lazy_method,fetchpriority,decoding,width,height,unsized,lcp_candidate,filename_issue,psi_wasted_bytes,severity,fix,effort`.

## Tips

- **Default to URL mode.** Single-page audits are 1 Firecrawl credit and produce a complete deliverable for the most common ask ("audit the images on /this/page"). Domain mode is for "give me a representative read on the whole site" — it surfaces patterns (templating bugs, CMS-wide missing alts) that single-page mode misses.
- **`<picture>` is the right answer.** When recommending modern formats, always recommend the `<picture>` element with AVIF + WebP `<source>` and a JPEG fallback `<img>` — not raw `<img src=".avif">`. AVIF is at 93%+ support and WebP at 97%+, but the fallback is what makes the markup safe for older clients and crawlers.
- **Don't lazy-load the LCP image.** This is the single most common image-SEO mistake on modern CMSes. Themes ship with site-wide `loading="lazy"` defaults that apply to the hero. The skill's LCP heuristic catches the most likely culprit; PSI (step 10) confirms it authoritatively.
- **Empty `alt=""` is correct for purely decorative images** (a hairline-rule SVG, a pure background-spacer image). It tells screen readers to skip the image. Don't auto-flag every empty alt — flag only those where the image filename and context suggest the image carries content.
- **Reverse the inventory if it's small.** For pages with <10 images, list every image with its full audit row in `IMAGES.md`'s "By category" section, not just the aggregate counts. Aggregate-only output is useful when there are 100+ images; below that it hides the specifics.
- **PSI is rate-limited at 25k/day on the free tier** but counts requests, not images. Calling PSI twice per target URL (mobile + desktop) is the default; skip desktop if you only care about Google's mobile-first ranking signal.
- **CSS background-images are a real blind spot** — flag the count, but don't audit them. They're not crawled as content images by Google.
- **JPEG XL is not yet shippable** (Nov 2025 Chromium announcement restoring decoder support, not yet in stable Chrome). Don't recommend JPEG XL until it lands in stable. WebP and AVIF are the current safe modern formats.
- **Don't auto-apply fixes.** The skill diagnoses and produces paste-ready snippets; humans decide which fixes to ship and in what order.
- **Verify after deploy.** Re-run this skill on the same URL after the fixes ship — the new run's "Coverage at a glance" reflects the live state and confirms the markup actually changed (vs sitting in the CMS but not pushed).

## Works well with

- **Predecessors:**
  - `seo-firecrawl` — when the user already scraped a page and now wants the image-specific cut.
  - `seo-technical-audit` — when a site-wide audit flagged image issues and the user wants the deep per-image rubric.
  - `seo-page` — when a URL-level keyword/traffic verdict is "refresh" and images are part of the refresh.
- **Successors:**
  - `seo-schema` — when the page also needs `Article` / `Product` / `LocalBusiness` schema beyond `ImageObject`.
  - `seo-google pagespeed` — for the full Lighthouse report (this skill cherry-picks the image audits; PSI has 100+ more).
  - `seo-drift` — to baseline image markup and detect regressions after a CMS or theme upgrade.
