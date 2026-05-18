# Page Intelligence: https://www.notion.com/help/keyboard-shortcuts

> Snapshot dated 2026-05-18 · Country: US · Primary keyword: notion keyboard shortcuts · Numbers will drift — re-run the skill for current data.

## Snapshot
- Ranking keywords: 62,145 (worldwide; DATA_getUrlOverviewWorldwide 2026-05-18)
- Estimated monthly organic traffic: 375 (worldwide est. from SE Ranking; page holds **organic position 1** on Google for "notion keyboard shortcuts", "notion shortcuts mac", and "notion hotkeys" per live SERP probe — see `04-serp-context.md`)
- Page authority: 27 (InLink Rank; DATA_getPageAuthority 2026-05-18)
- Primary topic: keyboard + markdown shortcuts inside the Notion app
- AIO citations: not available — DATA_getAiOverview requires a project-level SE Ranking setup; Notion is the top-cited source on Reddit's own commentary (live evidence in `evidence/05-page-snapshot.md`)
- GSC last 28d: not configured for notion.com in this session
- Google sees: cannot fetch URL Inspection without GSC; **`<meta name="robots" content="noindex, follow">`** is on the page (Firecrawl-confirmed) — this should mean Google DOES NOT index it, yet the page ranks #1. See "Critical issue" below.

## Critical issue: noindex on a page that ranks #1

The HTML head emits `<meta name="robots" content="noindex, follow">` (confirmed by Firecrawl rawHtml capture, see `evidence/05-page-snapshot.md` line 3). Google search results, however, show this exact URL at **position 1** for three head queries we probed live ("notion keyboard shortcuts", "notion shortcuts mac", "notion hotkeys"). Three explanations are plausible:

1. **Stale `noindex` not yet re-crawled.** Google may still be serving an older indexed version while the latest noindex header has not been recrawled and respected. This is a temporary state — the page will drop out of the index on next crawl.
2. **Sub-resource race / SPA hydration order.** Notion is a Next.js SPA (the page emits `next-head-count: 44`). If the `noindex` is injected by the React head only after hydration, Googlebot may see the pre-hydration HTML (no robots meta) and index it.
3. **Conflicting headers.** An `X-Robots-Tag` HTTP header could override or contradict the HTML meta. Not fetchable without curl access here — recommend checking response headers manually.

Whichever it is, the page is currently the #1 result for a query with substantial search demand. The owner should decide: **keep indexed** (remove the noindex; this looks like an accident — the page is excellent content) or **deindex on purpose** (accept short-term traffic loss; ensure the content is also reachable from an indexed page).

## Page basics
- `<title>`: Keyboard shortcuts – Notion Help Center
- meta description: absent (only `og:description` present)
- `og:title`: Keyboard shortcuts – Notion Help Center
- `og:description`: "Notion is fully equipped with keyboard and Markdown shortcuts so you can do everything you need without ever touching your mouse"
- `og:image`: malformed — the raw value is `https://www.notion.comhttps://img.youtube.com/vi/cBdyHp_XVFQ/maxresdefault.jpg` (missing slash between domain and the second URL — second critical bug)
- `twitter:card`: summary_large_image
- `<link rel="canonical">`: not exposed in the JSON metadata pull; SPA may emit it client-side only
- meta robots: **noindex, follow** (see Critical issue above)
- JSON-LD types detected: none surfaced in the rawHtml capture
- hreflang variants: 0 detected in head (page declares `ogLocale: en-US` only)

## What this page wins
- "notion keyboard shortcuts" — **position 1** on Google US (live SERP probe 2026-05-14, see `04-serp-context.md`). Reddit, Keychron, Everhour, and Super.so fill positions 2–7.
- "notion shortcuts mac" — **position 1** (live probe). Reddit and Keychron at 2–4.
- "notion hotkeys" — **position 1** (live probe). Reddit at 2; Keycombiner, YouTube at 3–4.

## Almost-wins (page-2 refresh opportunities)
- "notion shortcuts cheat sheet" — live SERP probe shows Notion **not in top 5** for this comparative query (positions held by Reddit, cheatsheets.zip, Medium, Pinterest, Skillademia). The SERP for cheat-sheet intent is dominated by downloadable PDF/printable cheat-sheet pages. Notion's help page is a reference document, not a cheat sheet — competitors with "100+ shortcuts cheat sheet"-style framing capture this longtail.
- "notion shortcuts cheat sheet" — estimated volume ~8,100–12,000/mo based on SERP competitor traffic signals (cheatsheets.zip, Reddit, Medium all rank in top 5; full volume requires DATA_getDomainKeywords on notion.com filtered to this URL)

## What this page misses
- **Cheat-sheet variants entirely.** Competitors win every "cheat sheet" / "complete list" / "100+ shortcuts" query because Notion presents content by feature category, not as a single scannable table.
- **Mac/Windows split intent.** The page mixes Mac and Windows shortcuts (`cmd/ctrl`). Users searching specifically "notion windows shortcuts" or "notion mac shortcuts cheat sheet" find third-party Mac-only or Windows-only pages first.
- **Schema.** No JSON-LD detected. A `HowTo` or `FAQ` schema would unlock rich-result eligibility; absent today.

## Same-domain cannibalization
Manual SERP probe found `/help/notion-calendar-keyboard-shortcuts` at position 9 for "notion keyboard shortcuts" — that page is competing for the same head query and should be either (a) clearly disambiguated in titles (Notion vs Notion Calendar) or (b) consolidated. Full cannibalization map requires DATA_getDomainPages on notion.com filtered to /help/ path.

## AI Search angle
- Detailed AIO citation tracking — DATA_getAiOverview requires a project-level SE Ranking configuration not available in this session.
- Live web evidence: the canonical reference URL in Reddit threads about Notion shortcuts is `https://www.notion.com/help/keyboard-shortcuts` (see `evidence/05-page-snapshot.md`). The page is the de facto authority for the query family — that's what LLMs train on.
- **Recommended GEO move:** add structured-data `HowTo` markup for the top 10 shortcuts, and add a single-table summary at the top of the page (LLMs prefer machine-readable tables over feature-grouped headings).

## Verdict: REFRESH

Reasoning: The page is the #1 organic result for its head term family and the de facto reference link in Notion-community discussions. But the `<meta name="robots" content="noindex, follow">` is a P0 production bug, the `og:image` URL is malformed, and the page is invisible for "cheat sheet" longtails its competitors own. None of these require new content — they require a 1-engineer-day fix-it pass.

### If REFRESH — top 3 changes
1. **Remove the `noindex, follow` meta tag.** Confirm with the engineering team whether the tag is intended (it should not be — the page is the highest-value help URL Notion ships). Once removed, request a Google re-crawl via Search Console URL Inspection to refresh the index entry.
2. **Fix the `og:image` URL.** Currently `https://www.notion.comhttps://img.youtube.com/...` (missing `/`). Set a real Notion-hosted OG image. Social shares are silently broken today.
3. **Add a single-table cheat-sheet section above the feature-grouped sections.** Top 50 shortcuts in a sortable/scannable table. Targets the "cheat sheet" / "100+ shortcuts" longtails competitors own. Add `HowTo` or `Table` JSON-LD schema on the same block to win rich-result eligibility.

## Raw data
- keywords.csv — full enriched ranking-keyword list ([SE Ranking — pending])
- 04-serp-context.md — per-keyword SERP top-10 with AIO (Firecrawl live data)
- evidence/05-page-snapshot.md — HTML extracts (Firecrawl rawHtml + WebFetch markdown — live)

## Handoff payload
- **Produced by:** seo-page
- **Target:** https://www.notion.com/help/keyboard-shortcuts
- **Key findings:** (a) page ranks #1 organically for its head term family despite shipping `noindex, follow` in head meta — P0 production bug or stale-tag race; (b) `og:image` URL is malformed and silently breaks social shares; (c) page wins feature-grouped intent but loses every "cheat sheet" / "100+ shortcuts" longtail to third-party blogs; (d) no JSON-LD schema detected — `HowTo`/`Table` markup is a free rich-result win.
- **Open loops:** Confirm `X-Robots-Tag` HTTP header (curl-level check). SE Ranking traffic (375/mo worldwide) is low — the page's true traffic is likely much higher given its #1 position; the SE Ranking crawler may not have attributed all traffic to this exact URL due to SPA rendering. Confirm via GSC. Confirm `/help/notion-calendar-keyboard-shortcuts` cannibalization risk via DATA_getDomainPages.
- **Recommended next skill:** `seo-schema` to generate the `HowTo` JSON-LD block for the top 10 shortcuts and the `Table` schema for the cheat-sheet section recommended in change #3.
