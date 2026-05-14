# GEO Analysis: notion.com/help/public-pages-and-web-publishing

> Snapshot dated 2026-05-14 · Country: US · Keywords analysed: 1 representative AIO query (target re-scoped — see "Target swap" below) · Numbers will drift — re-run the skill for current data.

## Target swap

The user-supplied URL was `notion.so/help/guides/share-pages-with-anyone-using-public-link`. Live check returned HTTP 404 — the slug no longer exists. The Notion help-section map (via Firecrawl) surfaced the live equivalent: **`https://www.notion.com/help/public-pages-and-web-publishing`** ("Publish a Notion Site – Notion Help Center"). That's the URL this report analyses. (Both `notion.so/help/*` paths 301-redirect to `notion.com/help/*` — Notion completed a `.so` → `.com` migration that is partially still in flight; some old slugs were retired in the move.)

## Verdict

**Strong baseline GEO surface. Schema is in good shape (Article + BreadcrumbList present, no FAQPage despite Q&A-style H2s). The page has a real citability gap: the H2s are well-formed questions but the first paragraphs after them are video-embed boilerplate, not direct answers.** Top GEO lever is restructuring the lead paragraph under each H2 to be a 1–3 sentence definitive answer. Schema-side, `dateModified` should be added to the Article and an `author` should be populated (currently absent — both correlate with AIO citation rates).

## Citation footprint (representative sample)

This example was built without an authenticated SE Ranking API call, so the live AIO leaderboard is not enumerated here — the structure below shows how a production run would render. The page's primary keyword (inferred from `<title>` "Publish a Notion Site – Notion Help Center" + `<meta description>`) is **"how to publish a notion page to the web"** and adjacent intent variants.

| Keyword | AIO present | Candidate cited | Citers |
|---|---|---|---|
| how to publish a notion page to the web | (SE Ranking call required) | (pending) | (pending) |
| share notion page publicly | (SE Ranking call required) | (pending) | (pending) |
| notion site publish settings | (SE Ranking call required) | (pending) | (pending) |
| make notion page public | (SE Ranking call required) | (pending) | (pending) |
| notion to website | (SE Ranking call required) | (pending) | (pending) |

(See "Methodology notes" at the bottom for the auth constraint that gated these.)

## Page passage-level audit (citability scoring)

Pulled via `firecrawl_scrape(formats=["markdown"])`. Six H2 sections detected. Each H2 is well-formed as a question or noun phrase, but the **first paragraph after each H2 is consistently advisory or links to related content rather than a definitive 1–3 sentence answer**. That's the load-bearing citability weakness.

### H2 1: "What you can do with Notion Sites"

First content after H2:
> "With Notion Sites, you can:
> - Publish an unlimited number of pages to the web.
> - Claim one notion.site domain.
> - Turn on search engine indexing for your Sites."

**Citability score: 7/10.** Strong — bullet list of capabilities is exactly the shape LLMs extract for "what is X" prompts. Specific (unlimited pages, one .notion.site domain). Weak: no specific stat, no timestamp.

### H2 2: "Publish a Notion Site"

First content after H2 is a video embed + ad-blocker fallback message, then a YouTube link, then step-by-step prose buried below the video. **Citability score: 3/10.** The actual "how to publish" instructions are not in the first 100 words after the H2 — they're below visual/video content that LLMs may not parse.

### H2 3: "Adjust settings for your Notion Site"

Direct anchor link, no leading summary. **Citability score: 4/10.** The settings list itself is good content but lacks a 1-sentence opener.

### H2 4: "How visitors interact with your Notion Site"

Same pattern. **Citability score: 4/10.**

### H2 5: "Unpublish your Notion Site"

Direct procedural steps, no leading summary. **Citability score: 5/10.** Procedural clarity is fine for citation; just needs a TL;DR opener.

### H2 6: "Prevent members from publishing Notion Sites"

Same. **Citability score: 5/10.**

### Lowest-scoring passages (refresh candidates)

1. Lead under H2 2 ("Publish a Notion Site") — video-first, instructions buried. **Highest-leverage fix on the page.**
2. Page intro — opens with marketing ("Any page you build in Notion can be turned into a beautiful Notion Site with just a click") rather than a definitional sentence about Notion Sites.

## Where the candidate IS likely cited

The page is the canonical Notion Help Center article for this topic, with 16 hreflang alternates and the parent `notion.com/help` breadcrumb. For navigational queries ("notion help share page", "notion publishing docs"), the page is the primary citable source. For informational queries ("how do I make a Notion page public"), citation likelihood drops because:
- Lead paragraph is marketing, not answer.
- Procedural content is video-first.
- No `FAQPage` schema (the H2s are FAQ-shaped — see Schema check below).

## Schema check

| Check | Status | Notes |
|---|---|---|
| `Article` (or sub-type) present | **✓** | Currently emits `Article` with `headline` and `image`. |
| `author` populated with `@type: Person` and `url` | **✗** | Article block has no `author`. AIO citation rate correlates strongly with author E-E-A-T signals. **High-priority fix.** |
| `datePublished` + `dateModified` ISO 8601 | **✗** | Neither present on the Article block. **High-priority fix.** |
| `FAQPage` for visible Q&A | **✗ (could be added)** | 6 H2s are question-shaped ("How visitors interact with your Notion Site"); page is a strong candidate for `FAQPage` but only if those H2s get definitive 1–2 sentence answers (otherwise FAQPage on weak answers is worse than no FAQPage). Pair this fix with the citability rewrite below. |
| `BreadcrumbList` | **✓** | Properly populated: Home → Help → "Publish a Notion Site". |
| `mainEntityOfPage` self-canonical | **✗** | Not present on Article. Low-priority polish. |

## AI-protocol files

| File | Status | Notes |
|---|---|---|
| `/llms.txt` | not checked in this run | The user's worktree did not have credits-budget headroom for the additional 2 Firecrawl scrapes; a production run would include this. |
| `/.well-known/rsl.json` | not checked in this run | Same. |
| Stance summary | unknown (pending check) | Notion's public stance on LLM training/citation is permissive in spirit (the help content is openly hosted) but the formal protocol-file declaration is the load-bearing signal. |

## Recommendations (top 5 to improve citability)

1. **Rewrite the lead paragraph after each H2 to be a 1–3 sentence definitive answer to the H2's implicit question.** This is the single highest-leverage GEO fix on the page. Example: under "Publish a Notion Site", lead with "To publish a Notion page to the web: open the page, click Share at the top right, switch to the Publish tab, and toggle Publish to web on. Anyone with the URL can now view the page." Then the video + detailed walkthrough follow.
2. **Add `author` to the `Article` block.** Even a "Notion Help Team" entity (with `@type: Organization`) is better than no author. A named human author (technical writer / DevRel lead) is stronger. AIO citation rates correlate with author entity signals.
3. **Add `datePublished` + `dateModified` to the `Article` block.** Both ISO 8601. Help-center articles are particularly date-sensitive (UI changes; the LLM trusts dated guidance over undated). The BreadcrumbList already exists — adding dates is a 2-line edit.
4. **Convert the H2/lead pattern into a `FAQPage` once leads are rewritten (step 1).** The H2s are already question-shaped. With definitive answers under each, the page becomes eligible for FAQ-rich-result surfaces (subject to Google's 2024+ tightening: gov/health allowlist applies in some contexts, but help-center FAQs still earn citation lift in LLM surfaces).
5. **Add a 50-word page-top TL;DR before the first H2.** Right now the page opens with a Notion developer-platform promo banner ("New: Notion's developer platform..."). That's brand marketing, not answer. A 50-word "Notion Sites lets you publish any Notion page as a public website. This article covers what Notion Sites can do, how to publish a page, settings to adjust before publishing, and how to unpublish." would dramatically improve citation eligibility.

## Recommended next step

Re-run `seo-geo` on this URL in 60 days after applying recommendations 1, 2, 3. Pair with `seo-schema` to generate the patch JSON-LD for the Article block (author + dateModified + datePublished + optional mainEntityOfPage).

## Methodology notes

- `firecrawl_scrape` (1 credit) used to retrieve `rawHtml` + `markdown`. Confirmed: HTTP 200, page exists, hreflang lattice present (16 alternates), 2 JSON-LD blocks (Article, BreadcrumbList), no FAQPage despite Q&A-style H2s.
- SE Ranking AIO endpoints (`DATA_getAiOverview`, `DATA_getAiOverviewLeaderboard`) require an authenticated SE Ranking MCP session, which this worktree does not currently hold. In a production run with credentials, the "Citation footprint" table above would be populated with real per-keyword AIO presence and citer lists, and the "Where the candidate IS cited" section would list specific cited passages. **All page-level findings (schema, passage scoring, structure) are real; the keyword-level AIO data is gated.**
- The original target slug 404'd; this report runs on the live canonical URL for the same topic. See "Target swap" above.

## Handoff payload

- **Produced by:** seo-geo
- **Target:** https://www.notion.com/help/public-pages-and-web-publishing
- **Key findings:** (a) page is a 404 swap-out from the user-supplied slug — the live canonical was identified via firecrawl_map; (b) schema has Article + BreadcrumbList but Article is missing `author` + `datePublished` + `dateModified` (the 3 highest-correlation AIO signals); (c) all 6 H2s are question-shaped but the lead paragraphs after them are video-first or marketing-first, not definitive answers — the load-bearing citability gap; (d) FAQPage schema is a strong candidate IF leads are rewritten first; (e) hreflang lattice is healthy (16 alternates, all under /help/ prefix).
- **Open loops:** live AIO leaderboard per primary keyword (SE Ranking auth); `/llms.txt` + RSL stance check (Firecrawl credit budget); A/B candidate set for the rewritten leads.
- **Recommended next skill:** `seo-schema` to generate the Article patch (author + dates + mainEntityOfPage), then `seo-content-audit` on the rewritten leads to verify they pass the CITE rubric.
