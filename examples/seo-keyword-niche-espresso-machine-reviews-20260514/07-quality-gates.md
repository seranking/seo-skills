# 07 — Quality gates

These gates are **non-negotiable** for the espresso-machine-reviews tier. The biggest risk is shipping thin content into a category that Google explicitly polices via the reviews-update.

## Universal gates (all variants)

### Gate 1 — Unique-data threshold (≥ 5 unique attributes vs sibling pages)

Each page must have ≥ 5 attributes that differ from its sibling pages in the same cluster.

For single-product reviews, the unique attributes are usually a slam-dunk: MSRP, type, boiler, pressure, grinder, in-use observation, photo. **The exception is when two machines from the same brand are nearly identical** (e.g. Breville Barista Express vs Express Impress — they share 80% of their spec sheet). In that case, the differentiator MUST be the in-use observation, not the spec table.

**Audit before publishing:** can a competitor's article on the same machine be substituted for this one with zero loss to the reader? If yes — fail. Do not publish.

### Gate 2 — Minimum word count: 800 words effective content

(Above the default 600. This is a high-CPC commercial niche where readers expect depth.)

Effective content = body prose + table rows + caption text. Nav, footer, sidebar, recommended-articles widget DO NOT count.

### Gate 3 — Schema requirements

Per template variant (see `06-template-spec.md` for the field tables):

- Variant A (single-product review): `Product` + `Review` (with `aggregateRating` if internal aggregation exists) + `BreadcrumbList` + `Person` (author) + `Organization` (publisher).
- Variant B (listicle): `ItemList` (each item = `Product` with embedded `Review`) + `BreadcrumbList`.
- Variant C (guide): `Article` or `FAQPage` (if 5+ visible Q&A) + `BreadcrumbList`. **Never `HowTo`** — Google retired that rich result in 2023.

Validate every published page in Google's Rich Results Test before submission.

### Gate 4 — Internal links

- ≥ 3 outbound to siblings in the same cluster (related reviews / comparisons / sub-guides).
- ≥ 1 inbound from the category hub or a nearby pillar.

### Gate 5 — **First-hand evidence (load-bearing)**

**Every single-product review page must demonstrate the reviewer actually used the machine.**

Acceptable evidence:

- A first-hand photo of the machine in the reviewer's space (not the studio shot from the manufacturer).
- A first-hand video (even a 15-second steam-wand demo).
- A specific observation that no manufacturer marketing would publish ("the steam wand purges enough water to chill the milk by 4°F before the build-up clears", "the descale notification fires every 23 days at our hard-water level").
- A measurement the reviewer took ("shots pulled in 28 seconds at 9.3 bar at 200°F").

NOT acceptable:

- Paraphrased manufacturer marketing.
- Stock photos.
- Generic "we like this machine" without measurement.

**Pages that fail gate 5 are not published.** This gate is the single highest-leverage E-E-A-T signal in the category, and Google's reviews-update has been ratcheting up scrutiny on exactly this point since 2022.

### Gate 6 — Index/noindex split

If a page can't pass gate 5 — generate it, store it, but `<meta name="robots" content="noindex,follow">` it. The follow attribute preserves internal link equity within the site without putting the thin page in the index.

## Programmatic-only gates (apply when tier ships 50+ pages)

### Gate 7 — Per-row uniqueness ≥ 30%

Of the template's content-producing fields, ≥ 30% must differ from the cluster median.

For espresso machine reviews this is usually easy — every machine has unique specs and price. The risk pages are the in-use observation fields where templates can devolve into "we like this machine" boilerplate.

### Gate 8 — Min unique facts vs parent + sibling (≥ 5)

Each row carries ≥ 5 facts that don't appear on the parent hub or any sibling page. Synonym shuffles don't count. **Sample 10 rows manually before greenlighting the tier.**

### Gate 9 — Data-source independence (≥ 2 sources)

Don't auto-publish from a single source. Mix:

- Manufacturer spec sheet
- Reviewer's first-hand observation
- Third-party measurement (e.g. independent thermometer / pressure-gauge data)
- User reviews aggregated across multiple platforms (Reddit /r/espresso, Coffee Geek forum, Amazon — synthesised, not scraped)

Auto-publishing from a single CSV scrape is the #1 trigger for spam-classifier blowback in this niche.

### Gate 10 — Index-bloat circuit-breaker

After the first 50 pages ship, monitor GSC. If the index-coverage rate drops below 60% (Google indexed < 60% of submitted), **pause the tier and re-audit**. Continuing past this signal compounds bloat across the rest of the tier.

## Refresh cadence

Espresso machine pricing and availability turn over fast. Recommended refresh:

- **Single-product reviews:** quarterly check of price, availability, model status (discontinued / replaced).
- **Listicles:** quarterly re-rank, every list refreshed with current models.
- **Buyer guides:** annual unless a major shift (new tech, regulatory change).
- **Maintenance guides:** annual.

Refresh = update content + bump `dateModified` in schema + cross-link to any new sibling pages.

## Anti-pattern checklist (what NOT to do)

- ❌ Spinning the same review across "best for beginners" / "best under $500" / "best Italian-made" listicles. Each listicle's pick must come from a genuine round-up, not a generic recommendation pasted everywhere.
- ❌ Embedding affiliate links in the H1 or first 100 words. Google's reviews-update specifically flags this pattern.
- ❌ Hiding the methodology block behind an accordion. Spam classifiers and AIO both extract methodology — if it's collapsed by default, it gets less signal weight.
- ❌ Using `<table>` for layout instead of for actual specifications. The Product/Review schema relies on a real specs table.
- ❌ Publishing without an author byline and an "About the author" link to a bio page. Author E-E-A-T is the second-highest leverage signal after first-hand evidence.
