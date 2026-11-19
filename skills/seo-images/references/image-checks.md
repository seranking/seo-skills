# Image audit rubric

> Updated 2026-05-14 with November-2025 JPEG XL note. Mirrors `AgriciDaniel/claude-seo`'s `seo-images` rubric, adapted to this catalogue's severity ladder.

This is the authoritative rubric for `seo-images`. Every issue code emitted by the skill maps to a row here.

## Severity scale

- **Critical** — major user-experience or major-traffic-loss potential. Fix today.
- **High** — significant ranking, accessibility, or CWV risk. Fix this week.
- **Medium** — quality-signal issue. Fix this month.
- **Low** — best-practice nudge. Fix when convenient.

## Effort scale

- **S** — markup edit on one template, <1 hour.
- **M** — markup edit + asset re-encoding across a section, <1 day.
- **L** — pipeline change (image CDN, build-time conversion, content rewrite at scale), multiple days.

---

## Alt text

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| `alt` attribute missing entirely | `image_alt_missing` | High | Add a descriptive alt (10–125 chars) describing what the image depicts, not the file | S |
| `alt=""` on an image whose filename / context suggests it carries content | `image_alt_decorative_questionable` | Medium | Verify intent. If decorative (separator, hairline, pure background), keep `alt=""` and add `role="presentation"`. Otherwise add a real alt | S |
| `alt` is a bare filename (`image.jpg`, `IMG_1234.png`) | `image_alt_filename` | High | Replace with a descriptive alt | S |
| `alt` is a single generic noun (`photo`, `picture`, `image`, `banner`, `graphic`) | `image_alt_generic` | High | Replace with a descriptive alt | S |
| `alt` is CTA copy (`click here`, `read more`, `learn more`) | `image_alt_cta` | High | Move the CTA to surrounding text; replace alt with a description of the image | S |
| `alt` length < 10 chars (non-empty) | `image_alt_short` | Medium | Expand to describe the image's content meaningfully | S |
| `alt` length > 125 chars | `image_alt_long` | Low | Trim — screen readers truncate around 125 chars | S |
| Same keyword token appears 3+ times in alt, or alt is >50% keyword tokens | `image_alt_stuffed` | Medium | Rewrite naturally; use the keyword at most once | S |
| Identical alt across multiple images on the page | `image_alt_duplicate` | Medium | Templating bug — make each image's alt unique to that image | M |

### Good vs bad alt examples

**Good:**
- "Professional plumber repairing a kitchen sink faucet"
- "Red 2024 Toyota Camry sedan, front three-quarter view"
- "Team of six in a modern office conference room reviewing a roadmap on a wall display"
- "Hand-drawn diagram showing the OAuth 2.0 authorisation-code flow"

**Bad:**
- `image.jpg` (filename, not description)
- `photo` (generic noun)
- `plumber plumbing plumber services` (keyword stuffing)
- `Click here` (CTA, not description)
- `2024_07_15_DSC_4821_edited_v2_final.png` (camera filename masquerading as alt)

---

## File size

Tiered thresholds by image category. Used to flag oversized images and to estimate compression savings when PSI data is unavailable.

| Image category | Target | Warning | Critical |
|---|---|---|---|
| Thumbnails (icons, avatars, list previews) | <50 KB | >100 KB | >200 KB |
| Content images (body images, product photos) | <100 KB | >200 KB | >500 KB |
| Hero / banner images | <200 KB | >300 KB | >700 KB |

When PSI is available (step 10 of the skill), use its `wastedBytes` figures over these thresholds — PSI estimates compression-and-format-conversion savings directly from the served bytes.

---

## Format hierarchy

| Format | Browser support (late-2025) | Use case |
|---|---|---|
| AVIF | 93%+ | Best compression for photos; preferred modern format when available |
| WebP | 97%+ | Default modern format — broader support than AVIF, smaller than JPEG |
| JPEG | 100% | Fallback for photos in `<picture>` chain |
| PNG | 100% | Graphics with transparency (logos, illustrations with hard edges) |
| SVG | 100% | Icons, logos, vector illustrations — never photographs |
| GIF | 100% | Avoid for anything large; convert animated GIFs to `<video>` |

### Recommended `<picture>` pattern

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg"
       alt="Descriptive alt text"
       width="800" height="600"
       loading="lazy"
       decoding="async">
</picture>
```

The browser picks the first supported `<source>`. The `<img>` is the universal fallback and the element to which `alt` / `width` / `height` / `loading` / `decoding` apply.

### JPEG XL note

In November 2025, Google's Chromium team reversed its 2022 decision to drop JPEG XL and announced a Rust-based decoder. Implementation is feature-complete but not yet in Chrome stable. JPEG XL offers lossless JPEG recompression (~20% savings, no quality loss) and competitive lossy compression. **Not yet practical for production deployment.** Monitor for stable-channel rollout through 2026.

### Format issue codes

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| Image served as JPEG/PNG with no `<picture>` modern alternative | `image_legacy_format` | Medium | Wrap in `<picture>` with AVIF + WebP `<source>` entries; keep JPEG/PNG as fallback `<img>` | M |
| Animated GIF >500 KB | `image_animated_gif` | Medium | Convert to `<video autoplay muted loop playsinline>` for far smaller file + same loop behaviour | M |
| SVG used for photographic content | `image_svg_misuse` | Low | Convert to a raster format (WebP/AVIF); SVG file size explodes on photographs | S |
| Image >Critical threshold for its category (see table above) | `image_oversized` | Medium | Compress + convert to WebP/AVIF; cross-check PSI `wastedBytes` for the real savings figure | M |

---

## Responsive sizing

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| Missing `srcset` (non-SVG raster image, served single resolution) | `image_no_srcset` | Medium | Generate 400/800/1200 width variants; add `srcset="img-400.webp 400w, img-800.webp 800w, img-1200.webp 1200w"` | M |
| `srcset` present but `sizes` missing AND not inside `<picture>` | `image_no_sizes` | Medium | Add a `sizes` attribute matching the layout breakpoints, e.g. `sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"` | S |
| `srcset` declared but all candidates within 100 px of each other (or `1x` only) | `image_srcset_useless` | Low | Either expand the width range or remove `srcset` — picking between near-identical sizes wastes the encode | S |

### Recommended `srcset` pattern

```html
<img
  src="image-800.webp"
  srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
  width="1200" height="800">
```

---

## Lazy loading & LCP

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| LCP candidate has `loading="lazy"` | `image_lcp_lazy` | High | Remove `loading="lazy"` from the hero/LCP image. Use `loading="lazy"` only below the fold | S |
| LCP candidate has no `fetchpriority="high"` | `image_lcp_no_fetchpriority` | Medium | Add `fetchpriority="high"` to the LCP image to move it to the front of the browser's network queue | S |
| Below-fold image with no `loading="lazy"` and no JS-loader signal | `image_below_fold_eager` | Medium | Add `loading="lazy"` to below-fold images, OR rely on the page's JS lazy-loader if one is already in use | S |
| Non-LCP image missing `decoding="async"` | `image_no_decoding_async` | Low | Add `decoding="async"` to non-LCP images so decode runs off the main thread | S |

### LCP image markup

```html
<!-- Hero / LCP image: eager-load, high priority, no lazy -->
<img src="hero.webp"
     alt="Hero image description"
     width="1200" height="630"
     fetchpriority="high"
     decoding="sync">
```

Note `decoding="sync"` on the LCP image (or omit the attribute — `sync` is the default). `async` defers decode and can push out the LCP paint.

### Lazy-loader detection

See `lazy-loaders.md` for the full attribute / class taxonomy.

---

## CLS dimensions

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| Missing both `width` and `height` attributes AND no inline `aspect-ratio` style | `image_unsized` | High | Add `width` and `height` attributes set to the image's intrinsic dimensions. CSS handles responsive scaling | S |
| `width` × `height` ratio differs from the actual displayed ratio by >5% | `image_aspect_mismatch` | Low | Match the attribute ratio to the displayed ratio, or set `aspect-ratio` CSS to override | S |

Even if the image is responsive, the `width` and `height` attributes are used by the browser to compute the aspect ratio and reserve space before the image loads. Setting them is what prevents CLS.

```html
<!-- Good — dimensions set, scales responsively via CSS -->
<img src="photo.webp"
     alt="Description"
     width="1200" height="800"
     style="max-width: 100%; height: auto;">

<!-- Also good — aspect-ratio CSS for non-fixed-dimension cases -->
<img src="photo.webp"
     alt="Description"
     style="aspect-ratio: 3/2; width: 100%; height: auto;">
```

---

## File names

| Check | Issue code | Severity | Fix | Effort |
|---|---|---|---|---|
| Camera-default filename (`IMG_xxxx`, `DSC_xxxx`, `DSCN_xxxx`, `P_xxxx`, `Photo_xx`) | `image_camera_filename` | Low | Rename to descriptive lowercase-hyphenated (`blue-running-shoes-side-view.webp`) before upload | S |
| Random-hash filename (hex/base64 with no human tokens) coupled with missing or generic alt | `image_hash_filename` | Low | If the CMS produces hashes for cache-busting, ensure the alt carries the descriptive signal. Otherwise rename | S |
| All-uppercase or all-underscore filename | `image_filename_style` | Low | Convention is lowercase + hyphens (e.g. `kitchen-renovation-after.webp`) | S |

**Don't flag every CDN-served image.** Many image CDNs hash filenames for cache busting; that's the right call for caching and doesn't hurt SEO when the `alt` carries the signal. The flag is meaningful when the alt is also missing / generic.

---

## `ImageObject` JSON-LD

Top-level `ImageObject` blocks can make a page eligible for [licensable-images rich results](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata) on Google Images.

### Required fields

| Field | Type | Notes |
|---|---|---|
| `@context` | URL | Must be `https://schema.org` |
| `@type` | string | Must be `ImageObject` (or a subtype) |
| `contentUrl` | URL | The actual image URL — **use this, not `url`** (Google's spec). `url` is ambiguous |
| `creator` *or* `copyrightHolder` | Person or Organization | At least one is required; both is ideal |

### Recommended for licensable-images rich results

| Field | Type | Notes |
|---|---|---|
| `license` | URL | Page describing the license terms (CC-BY, royalty-free, etc.) |
| `acquireLicensePage` | URL | Page where users can buy / request licensing |
| `creditText` | string | How the image should be credited when used |
| `copyrightNotice` | string | The copyright string (e.g. "© 2026 Brand Name") |
| `caption` | string | Caption describing the image |
| `width` / `height` | Number | Intrinsic dimensions in pixels (Number, not string) |

### Common mistakes

- `url` instead of `contentUrl` — Google's spec prefers `contentUrl` for the image asset and uses `url` for the page the image lives on.
- `author` instead of `creator` — `ImageObject` uses `creator`. `author` is on `Article` / `BlogPosting`.
- `creator` as a bare string instead of a `Person` / `Organization` object. Always nest:
  ```json
  "creator": { "@type": "Organization", "name": "Brand Name" }
  ```
- `width` / `height` as strings instead of numbers. Use `1200`, not `"1200"`.
- Marking up images that aren't visibly on the page. Google penalises hidden-content schema.

See `../templates/image-object.jsonld` for a paste-ready block.

---

## What matters vs what doesn't for Google Images

| Factor | Impact | Where to set it |
|---|---|---|
| Alt text | **Critical** (ranking) | `<img alt="…">` |
| Filename | High (ranking — secondary signal) | File system (descriptive, hyphenated, lowercase) |
| Page context (surrounding text) | High (ranking) | Body copy near the image |
| File size / page speed | Medium (indirect via CWV) | Compression + format conversion |
| `ImageObject` `creator` / `copyrightNotice` | Low (display only — licensable-images rich results) | JSON-LD on the page |
| EXIF camera data (camera model, GPS, etc.) | None | Strip on upload — privacy leak, no SEO value |
| IPTC `Keywords` field | None | Google ignores |

The skill weights signals accordingly when ordering the remediation list.

---

## Optimisation pipeline (out of scope for this skill)

This skill audits markup; converting / re-encoding the actual image files is out of scope. If the user wants a pipeline, the standard recipe is:

```bash
# WebP (preferred default, metadata preserved)
cwebp -q 82 -metadata all input.jpg -o output.webp

# AVIF (better compression, slower encode)
ffmpeg -i input.jpg -c:v libaom-av1 -crf 30 -still-picture 1 output.avif

# Responsive width variants
for w in 400 800 1200; do
  convert input.jpg -resize ${w}x -quality 82 "image-${w}.webp"
done

# Inject IPTC + XMP for licensable-images rich results (Google Images shows these)
exiftool \
  -IPTC:By-line="Brand Name Photography" \
  -IPTC:CopyrightNotice="Copyright 2026 Brand Name" \
  -XMP:Creator="Brand Name Photography" \
  -XMP:Rights="Copyright 2026 Brand Name" \
  image.jpg
```

**WebP supports EXIF and XMP but not IPTC natively** — for WebP files, use XMP fields; `exiftool` converts automatically when writing to `.webp`.

For automated pipelines, an image CDN (Cloudinary, imgix, Cloudflare Images, Vercel Image Optimization, Next.js `<Image>`) handles conversion + responsive variants + `<picture>` markup at request time. Recommend an image CDN over manual conversion for sites with >100 content images.
