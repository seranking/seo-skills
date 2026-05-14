# Content Audit: stripe.com/blog/rate-limiters

> Snapshot dated 2026-05-14 · Target keyword: "api rate limiting strategies" · Country: US · Numbers will drift — re-run the skill for current data.

## Verdict: PUBLISH WITH FIXES

The article is a developer-canonical reference with strong technical authority (named senior engineer at Stripe, production telemetry cited inline, 4-strategy framework). E-E-A-T scores high but **freshness is a critical weakness** — published March 30, 2017, never updated, no `dateModified` in schema, no "Last reviewed" date in body. CITE scores drag mainly on the timestamp dimension and on AIO-winner gaps (token bucket alternatives like sliding-window/leaky-bucket are not covered; SERP winners all cover at least 3-4 algorithms).

## Scores

| Dimension | Score | Threshold | Status |
|---|---:|---:|:---:|
| Experience | 92% | 75% | OK |
| Expertise | 87% | 75% | OK |
| Authoritativeness | 80% | 75% | OK |
| Trustworthiness | 73% | 75% | FAIL |
| **E-E-A-T composite** | **83%** | **75%** | **OK** |
| Clear answer | 80% | 70% | OK |
| Include stats | 72% | 70% | OK |
| Timestamp | 33% | 70% | **FAIL** |
| Entity authority | 78% | 70% | OK |
| **CITE composite** | **66%** | **70%** | **FAIL** |

## Veto checks

- Anonymous author on YMYL: **not triggered** (named author Paul Tarjan, with twitter URL in JSON-LD)
- Unsourced factual claims: **not triggered** (Wikipedia + RFC 6585 + RFC 7231 + AWS ElastiCache + GitHub gist all linked inline)
- Undisclosed affiliate / sponsored: **not triggered** (no commercial third-party recommendations; AWS link is contextual not promotional)
- AI-generated YMYL with no human review: **not triggered** (article predates LLM-content era by years; clear human voice + production telemetry)

## AI Search readiness
- AIO present for "api rate limiting strategies": **likely yes** (SERP for the phrase is dominated by educational/learning-center content — high AIO probability)
- Top citation patterns from comparable SERP winners: (a) cover 3-5 algorithms (Stripe covers only token bucket, mentions others by category); (b) include implementation code snippets (Stripe links to GitHub gist but doesn't inline); (c) recent timestamp or "Updated YYYY" (Stripe has neither).
- Candidate URL cited in any sampled AIO: **not measured** (SE Ranking unauthenticated this run — see methodology notes). Manual SERP check shows the article is **not in the top 8 organic** for "api rate limiting strategies guide" today; Medium, Kong, ByteByteGo, Gravitee, API7 own that SERP. Stripe is **outranked by its own technical content** by 6 educational publishers despite higher domain authority.
- Gap vs cited sources: (a) freshness — every competitor has a 2023-2026 date; (b) algorithm coverage — competitors cover token bucket + leaky bucket + sliding window + fixed window; Stripe covers only token bucket; (c) code samples — competitors inline ; Stripe defers to gist.

## Snapshot (measured)
- Article body word count: ~1,500-1,800 words (excluding nav/footer/country list)
- Published: 2017-03-30 · Modified: (none in schema) · Age: 9 years 1 month
- Author: Paul Tarjan (twitter.com/ptarjan, no internal author page on stripe.com)
- External citations: 5 (Wikipedia ×2, IETF RFC ×2, AWS ElastiCache, GitHub gist)
- JSON-LD blocks: 1 (`@type: [Article, BlogPosting]`)
- Internal cross-link: 1 (`/blog/idempotency`)
- Page type detected: explainer / how-to hybrid — 4-strategy enumeration is structurally a listicle
- Word-count floor applied (explainer): 1,500 — article meets floor
- GA4 organic last 28d: not configured (Tier 2 required — SE Ranking + Google APIs unauthenticated this run)

## Top 5 fixes

1. **Add `dateModified` and "Last updated" notice.** This is the single biggest fix. The article is canonical in spirit but is invisibly aging — `dateModified` in JSON-LD plus a visible "Reviewed YYYY-MM" in the body would restore freshness signals without rewriting. If the content needs updates (it does — see fix 2), bump both.
2. **Expand algorithm coverage to match SERP winners.** Add sections for **sliding window**, **leaky bucket**, and **fixed window counters**. Competitor articles all cover 3-5 algorithms; Stripe covers only token bucket. This is a 400-700 word addition that closes the AIO-winner gap on the same page.
3. **Inline code samples for the Request Rate Limiter.** The "GitHub gist" link at the end is friction. Promote the Lua/Redis script directly into the body (Stripe's own production-grade code). Code blocks are highly extractable by LLMs and SERP rich-result parsers.
4. **Fix `og:image` and add `image` to JSON-LD `Article`.** Current `og:image` is `?q=80` (truncated/broken). JSON-LD `image: []` is empty. This blocks rich-result eligibility and weakens social preview.
5. **Add internal author page for Paul Tarjan.** Current author link points to Twitter — weak entity signal. A `/blog/authors/paul-tarjan` page with bio + post list, plus `Person` schema (`@type: Person, sameAs: [twitter, linkedin, github]`), strengthens both E-E-A-T author signals and AIO citability (LLMs reward named expert authority).

## Detailed scoring

See:
- 03-eeat-scoring.md (item-by-item E-E-A-T)
- 04-cite-scoring.md (item-by-item CITE)
- 05-aio-winner-comparison.md (gap vs cited sources)

## Methodology notes

- **SE Ranking MCP not authenticated in this run.** The skill's AIO context steps (`DATA_getAiOverview`, `DATA_getAiOverviewLeaderboard`, `DATA_getAiPromptsByTarget`) were unavailable. The AIO competitive set was reconstructed from `mcp__firecrawl-mcp__firecrawl_search` on the target keyword; the cross-check in `05-aio-winner-comparison.md` is built from that SERP — re-run with SE Ranking authenticated to get the actual AIO citation graph + brand-mention counts.
- **Firecrawl + curl used for the page extract** (1 Firecrawl credit + 1 curl fetch for rawHtml inspection). JSON-LD, canonical, author, datePublished, dateModified, og:image, twitter:card all measured directly.
- **GA4 organic traffic** (step 3b) not available — Google APIs not configured.
- **Page-type detection** classified the article as a hybrid explainer/how-to listicle. The 4-strategy enumeration is the listicle backbone; the surrounding intro + Building-in-practice section is explainer-shaped. Applied word-count floor: 1,500 (explainer baseline).

## Handoff payload
- **Produced by:** seo-content-audit
- **Target:** https://stripe.com/blog/rate-limiters
- **Key findings:** (a) Strong E-E-A-T (83% composite) — named senior engineer, production telemetry, external authoritative citations; (b) CITE fails on freshness (33% timestamp score) — published 2017, no dateModified, no visible review date; (c) algorithm coverage is narrower than every SERP competitor; (d) JSON-LD `image: []` empty + og:image broken — rich-result eligibility blocked.
- **Open loops:** AIO citation graph (which prompts cite this URL today), GA4 organic traffic (is this still earning visits or just sitting?), `DATA_getAiPromptsByTarget` to see if `stripe.com` as a domain is mentioned for rate-limiting prompts at all.
- **Recommended next skill:** `seo-page` to confirm current traffic + keyword footprint for this URL (verdict: refresh, not consolidate). Then `seo-schema` for the JSON-LD `image` field + author Person schema; then writer-led refresh adding sliding-window / leaky-bucket / fixed-window sections.
