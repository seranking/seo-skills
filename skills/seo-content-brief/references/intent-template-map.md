# Intent → template map (8 templates)

> Adapted from `AgriciDaniel/claude-seo`'s `seo-cluster/references/hub-spoke-architecture.md` (MIT).

Use this map at brief time to classify the article being briefed against one of 8 canonical templates. Selection is driven by the SERP top-10 (page-type majority) and the keyword's intent classification from `DATA_getRelatedKeywords` / `DATA_getKeywordQuestions`. Cross-reference word-count floors against the page-type rubric the auditor uses in `skills/seo-content-audit/` — the brief's "Word count target" must clear the floor for the chosen template.

## How to use

1. Pull SERP top-10 + PAA + AIO presence (already collected in step 5 of `SKILL.md`).
2. Classify each top-10 URL by page type (use the heuristics in `skills/seo-sxo/references/page-type-patterns.md`).
3. Take the dominant type (≥ 6 of 10) → that's your template. If split (e.g. 4-4-2), see the MIXED rule in `SKILL.md` Tips.
4. Sanity-check against the keyword's intent classification (informational broad / informational how / commercial compare / etc.).
5. Record the chosen template + a one-sentence justification in `BRIEF.md`'s "Template type" + "Why this template" lines.

---

## 1. ultimate-guide
**Pick when:** the SERP top-10 has ≥ 6 pages with `<title>` length > 60 chars and the keyword is a broad noun phrase (e.g. "content marketing", "supply chain management").

- **SERP signals:** PAA cluster of 6+ "what is / how does / types of" questions; top-10 dominated by long-form editorial on .com/blog or .com/guide; AIO almost always present; titles often "The Ultimate Guide to X" / "X: A Complete Guide".
- **Intent classification:** informational (broad).
- **Outline shape:** H1 = "{Topic}: The Complete Guide" → H2s: What is X · Why X matters · Core components of X (3-6 sub-H2s) · How to get started with X · Common pitfalls · X vs adjacent concepts · FAQ.
- **Word count floor:** 2,500 words. Use 3,000-4,000 for high-volume head terms. (See `seo-content-audit` for E-E-A-T thresholds at this length — anonymous bylines fail the YMYL veto regardless.)
- **Example brief patterns** (paraphrased from real published winners):
  - "Marketing Attribution: The Complete Guide" — 3,800 words, 9 H2s, 1 model-comparison table, 2 case-study callouts, FAQ block of 8 PAA-derived questions.
  - "What Is Vendor Risk Management" — 3,200 words, opens with a 180-word definition for AIO citability, then framework / lifecycle / tooling / metrics / FAQ.

## 2. how-to
**Pick when:** the keyword starts with "how to" or "how do I", AND ≥ 5 of the top-10 carry numbered-step content with `HowTo` schema or numbered H2s.

- **SERP signals:** PAA dominated by "how do I / how long does / what do I need" questions; titles start with "How to"; AIO often shows numbered steps; video carousel common.
- **Intent classification:** informational (procedural).
- **Outline shape:** H1 = "How to {verb} {object}" → H2s: What you'll need · Step 1 · Step 2 · ... · Troubleshooting · FAQ.
- **Word count floor:** 1,200 words. Steps with screenshots can run shorter; pure-prose tutorials need more.
- **Example brief patterns:**
  - "How to migrate a WordPress site to a new host" — 1,800 words, 8 numbered steps each with a screenshot and a "what could go wrong" callout, troubleshooting H2 with 5 known errors.
  - "How to set up GA4 ecommerce tracking" — 1,400 words, 6 steps, embedded code block per step, "verify it worked" final step.

## 3. listicle
**Pick when:** ≥ 6 of the top-10 titles start with a number (e.g. "10 X", "7 ways to Y") OR the keyword contains "tips", "ways", "examples", "reasons".

- **SERP signals:** Titles "{Number} {plural noun}"; URLs with `/n-things/`, `/n-tips/`; PAA mostly "what are some / what is the best".
- **Intent classification:** informational (list).
- **Outline shape:** H1 = "{N} {items}" → H2s: one per list item (uniform length, ~150-250 words each), Intro before list, optional "How we picked" methodology block, FAQ.
- **Word count floor:** 1,500 words. Floor scales with N — `N × 200` is a useful lower bound for each entry to be substantive.
- **Example brief patterns:**
  - "12 examples of brand storytelling" — 2,400 words, 12 entries × ~180 words each, brand logo per entry, "what we learn" one-liner per entry.
  - "8 ways to reduce SaaS churn" — 1,700 words, 8 H2s with a 1-paragraph rationale + 1 stat citation each, conclusion summary table.

## 4. explainer
**Pick when:** the keyword is "what is X", "X meaning", "X explained", AND the top-10 is dominated by definition-led editorial pages (no products, no listicles).

- **SERP signals:** Featured snippet often present (definition pulled from page); PAA dominated by "what does X mean / why is X important / what are types of X"; AIO definition lifted from one of the top-3.
- **Intent classification:** informational (concept).
- **Outline shape:** H1 = "What is {X}?" → H2s: Definition (60-100 words, citable) · Why X matters · How X works · Types / variants of X · X vs related concepts · Examples · FAQ.
- **Word count floor:** 1,200 words. The opening 200 words must contain a tight, atomic definition (passage-citability for AIO).
- **Example brief patterns:**
  - "What is zero-trust security" — 1,600 words, 80-word lead definition, 5 H2s, 1 architecture diagram, FAQ of 6 PAA questions.
  - "What is product-led growth" — 1,400 words, definition + 3 hallmarks + 4 examples + FAQ; closes with "PLG vs sales-led" comparison block.

## 5. comparison
**Pick when:** the keyword is "X vs Y" / "X compared to Y" / "X or Y", AND ≥ 5 of the top-10 are head-to-head pages with both names in H1.

- **SERP signals:** Titles contain "vs", "vs.", "or", "compared"; URLs match `/x-vs-y/`; schema typically `Product` ×2 + `BreadcrumbList`; commercial intent.
- **Intent classification:** commercial (compare).
- **Outline shape:** H1 = "X vs Y: {differentiator}" → H2s: TL;DR verdict · Feature-by-feature comparison (table-heavy) · Pricing · Best for {persona A} · Best for {persona B} · How to choose · FAQ.
- **Word count floor:** 1,500 words. Comparison tables count toward depth but not toward word count — 1,500 is prose only.
- **Example brief patterns:**
  - "Notion vs Coda" — 2,000 words, 12-row feature table, 3 use-case scenarios with verdicts, "switch from one to the other" migration sidebar.
  - "Stripe vs Adyen for SaaS" — 1,800 words, balanced verdict in lead, pricing breakdown table, FAQ of 7 buyer-decision questions.

## 6. review
**Pick when:** the keyword is "X review" / "is X worth it" / "X pros and cons", AND ≥ 5 of the top-10 are single-product editorial reviews (not listicles, not vendor pages).

- **SERP signals:** Titles "{Product} Review {YYYY}"; PAA "is X good / does X work / X complaints"; rich-result stars often visible; freshness signals strong (date in title or first paragraph).
- **Intent classification:** commercial (evaluate).
- **Outline shape:** H1 = "{Product} Review: {verdict phrase}" → H2s: TL;DR rating · Who it's for · Features tested · What we liked · What we didn't · Pricing · Alternatives · Final verdict.
- **Word count floor:** 1,500 words. Hands-on testing detail (screenshots, original data) carries more weight than length.
- **Example brief patterns:**
  - "Ahrefs review (2026)" — 2,200 words, dated lead, scorecard at top, 6 feature deep-dives with screenshots, 4 alternatives at the bottom each linked to a comparison page.
  - "Fellow coffee grinder review" — 1,600 words, original tasting notes from 8 brews, particle-distribution chart, "buy / skip" verdict in first 100 words.

## 7. best-of
**Pick when:** the keyword is "best X" / "top X" / "X alternatives", AND ≥ 5 of the top-10 are ranked lists of 5-15 products with `ItemList` schema or numbered product cards.

- **SERP signals:** Titles "Best {N} X for Y"; URLs `/best-x/`, `/x-alternatives/`; commercial; shopping pack often above organic; PAA "what is the best / which X should I buy".
- **Intent classification:** commercial (rank).
- **Outline shape:** H1 = "The {N} Best {category} in {YYYY}" → H2s: How we picked (methodology) · #1 {Product} · #2 {Product} · ... · Honourable mentions · How to choose · FAQ.
- **Word count floor:** 1,800 words. Each ranked entry needs ~150-250 words of justification (use case, pros, cons, who it's for) to outscore thin list affiliate competitors.
- **Example brief patterns:**
  - "Best CRM for small business 2026" — 2,500 words, 8 entries × ~200 words, methodology block (12 criteria scored), 1 summary table, "how to choose" decision tree.
  - "10 best Zapier alternatives" — 2,200 words, 10 entries each with use-case fit, pricing snapshot, link to a dedicated "vs Zapier" comparison page.

## 8. landing-page
**Pick when:** the keyword is the brand name, a high-commercial product term, or a "{tool} for {persona}" head term, AND ≥ 5 of the top-10 are product/SaaS landing pages (not editorial, not blog).

- **SERP signals:** Titles "{Product} – {benefit}"; URL is root or `/products/x`; schema `Product` / `SoftwareApplication` / `Organization`; transactional intent.
- **Intent classification:** transactional.
- **Outline shape:** H1 = brand or category benefit promise → Hero CTA · Social proof · Problem framing · Feature blocks · Use cases · Pricing · FAQ · Footer CTA. (Brief is structural, not editorial — prose volume is intentionally lower.)
- **Word count floor:** 600 words. Landing pages prioritise CRO over depth; the floor exists only to satisfy crawlable text minimums and clear thin-content thresholds.
- **Example brief patterns:**
  - "Project management for engineering teams" — 800 words across hero / 3 feature blocks / 2 customer logos / pricing table / FAQ; H2s designed for snippet capture.
  - "AI-native CRM" — 700 words, hero with demo video, 4 feature blocks each with a screenshot, integrations grid, single pricing CTA.
