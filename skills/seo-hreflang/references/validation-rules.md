# Hreflang Validation Rules

Load this reference when applying validation in step 4 (per-URL inventory) or step 5 (sitemap). Each row is one rule: detection logic, severity, suggested fix, and the source the rule fires from.

## Rule table

| Issue code | Severity | Detection (what triggers it) | Suggested fix | Source |
|---|---|---|---|---|
| `hreflang_no_self_reference` | Critical | A page emits hreflang alternates but its own URL is not in the set. | Add `<link rel="alternate" hreflang="{lang}" href="{this-page-url}">` matching the page's own language. | html, sitemap |
| `hreflang_missing_return_tag` | Critical | Page A lists page B as an alternate, but page B does not list page A back. | Add the reciprocal `<link rel="alternate">` on page B pointing to page A. | html, sitemap |
| `hreflang_missing_x_default` | High | The hreflang set has language alternates but no `hreflang="x-default"` entry. | Add one `<link rel="alternate" hreflang="x-default" href="{fallback-url}">` per set. The fallback is typically the language selector page or the English version. | html, sitemap |
| `hreflang_invalid_lang_code` | High | The `hreflang` value is not a valid ISO 639-1 language code (optionally followed by `-` and an ISO 3166-1 Alpha-2 region). | Replace with the correct code. Common errors: `eng` → `en`, `jp` → `ja`, `zh` → `zh-Hans` or `zh-Hant`. | audit, html, sitemap |
| `hreflang_invalid_region_code` | High | The region qualifier is not a valid ISO 3166-1 Alpha-2 code, or is mis-cased. | Replace with the correct region. Common errors: `en-uk` → `en-GB`, `es-LA` → use specific countries (e.g. `es-MX`, `es-AR`). Format is lowercase language, uppercase region. | audit, html, sitemap |
| `hreflang_canonical_mismatch` | High | A page emits hreflang but its `<link rel="canonical">` points at a different URL. | Either move hreflang to the canonical page, or align the canonical to point at this page. Hreflang on a non-canonical page is silently ignored by Google. | audit, html |
| `hreflang_conflict` | High | The same hreflang value (e.g. `de-DE`) is used by multiple distinct URLs in the same set. | Pick one canonical URL per language-region. Google ignores conflicting sets entirely. | audit, html, sitemap |
| `hreflang_protocol_mismatch` | Medium | URLs in the same hreflang set mix HTTP and HTTPS. | Standardise on HTTPS. After an HTTPS migration, update every hreflang `href`. | html, sitemap |
| `hreflang_trailing_slash_mismatch` | Medium | The hreflang `href` differs from the canonical only by trailing-slash. | Match the canonical exactly (including trailing slash). | html, sitemap |
| `hreflang_html_sitemap_mismatch` | Medium | The hreflang set in the sitemap does not match the set in the page HTML for the same URL. | Pick one source of truth (sitemap is preferred for sites with > 50 language variants per page). Remove the other or sync them. | html ↔ sitemap cross-check |
| `hreflang_target_unverified_gsc` | Medium | An `href` target domain in the hreflang set is not verified in Google Search Console. | Verify the domain in GSC. Cross-domain hreflang requires verification on both sides per Google's documentation. | gsc |
| `hreflang_xhtml_namespace_missing` | Medium | The sitemap contains `<xhtml:link>` elements but does not declare `xmlns:xhtml="http://www.w3.org/1999/xhtml"` on the root `<urlset>`. | Add the namespace declaration to the `<urlset>` element. | sitemap |
| `hreflang_language_without_region` | Low | The hreflang value uses only a language code (e.g. `es`) on a page that's clearly geo-targeted (e.g. only mentions Spain). | If geo-targeting is intended, add the region qualifier (`es-ES`). If not, leave as-is — language-only is a valid choice. | html, sitemap |
| `hreflang_dual_implementation` | Low | The site emits hreflang in both HTML and sitemap. Not strictly invalid, but doubles maintenance and creates risk of `hreflang_html_sitemap_mismatch`. | Pick one. Sitemap is preferred for sites with > 50 language variants per page; HTML is fine for smaller sites. | html ↔ sitemap |

## Severity definitions (used by step 7's verdict heuristic)

- **Critical** — entire hreflang set is invalidated; Google ignores it. PASS not possible while any Critical exists.
- **High** — hreflang set works but is wrong in a way that costs traffic in the affected market. NEEDS-FIX threshold.
- **Medium** — hreflang set works but is sloppy. Will likely become a problem after the next deploy that touches URLs.
- **Low** — best-practice nudge. No traffic impact today.

## Detection notes

- **Self-reference check (`hreflang_no_self_reference`):** match by URL string (case-insensitive). If the page is `https://example.com/fr/page` and its hreflang set lists `hreflang="fr" href="https://example.com/fr/page"`, that's a valid self-reference.
- **Return-tag check (`hreflang_missing_return_tag`):** for each (page → alternate) edge in the per-URL inventory or sitemap, verify the inverse edge exists. This is an O(n²) check on small sets; for large sets, build a hash map of URL → set-of-alternates and look up reciprocity per edge.
- **Language-region validation:** ISO 639-1 is two letters (`en`, `fr`, `de`, `ja`, `zh`). ISO 3166-1 Alpha-2 is two letters (`US`, `GB`, `DE`, `BR`). The combined value uses lowercase language + `-` + uppercase region (`en-GB`, `de-AT`, `pt-BR`). `x-default` is the only special value.
- **Canonical alignment (`hreflang_canonical_mismatch`):** strict string match required. Trailing slash, scheme, and case all matter.
- **Conflict detection (`hreflang_conflict`):** two distinct URLs both claiming `hreflang="de-DE"` is the textbook case. Less obvious: a page that lists `de-DE` AND `de-AT` both pointing at the same URL — that's not technically a conflict (different language-region values), but it's a hint that the German strategy is muddled.

## What this skill explicitly does NOT validate

The upstream skill (theirs') extends into cultural adaptation, content parity, locale-format consistency, and word-count ratios. Those are translation-quality concerns. This skill is narrowly scoped to whether the hreflang signal itself is technically correct. If the user wants the broader localization audit, point them at their translation/localization team — Claude can't reliably assess cultural appropriateness without locale-specific expertise that this skill's data doesn't capture.
