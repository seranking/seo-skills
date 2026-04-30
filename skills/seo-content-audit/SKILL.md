---
name: seo-content-audit
description: E-E-A-T + CITE quality audit for an EXISTING piece of content. Scores Experience, Expertise, Authoritativeness, Trustworthiness, and citation-readiness for AI search; surfaces veto items that block publication; produces a publish / publish-with-fixes / no-publish verdict. Distinct from `seo-content-brief` (produces a NEW article from a topic) and from `seo-page` (URL-level keyword/traffic intelligence). Use when the user asks "content quality audit", "E-E-A-T check", "is this content good", "review this article", "content audit", "citation readiness", or "AI search readiness".
---

# Content Quality Audit

Score an existing piece of content against modern E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) and CITE (Clear answer, Include primary stats, Timestamp, Entity authority) rubrics. Surface veto items that block publication regardless of overall score. Produce a clear publish / publish-with-fixes / no-publish verdict with the top 5 fixes.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available.
- User provides: (a) the URL of an existing piece of content (or pasted content + intended URL), (b) target keyword the content is meant to rank for. Optional: target country (default `us`).

## Process

1. **Fetch content** `WebFetch` (always) + `mcp__firecrawl-mcp__firecrawl_scrape` (when available)
   - **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (credit balance, Firecrawl availability, Google APIs). Skill-specific notes:
     - Estimated SE Ranking cost for this skill: ~10–15 credits typical (AIO context + AIO prompt sampling for the target keyword + audited URL).
     - Firecrawl: optional with WebFetch fallback, 1 Firecrawl credit per URL audited (default cap 50 URLs, hard cap 200). Surface the projected Firecrawl credit count before continuing. Pass `--no-firecrawl` to force WebFetch-only inspection (lower-confidence veto checks; see step 4 caveat).
     - Google APIs: tier 2 (GA4 available) unlocks step 3b (GA4 organic traffic on the audited URL) after the AIO context step. See `skills/seo-google/references/cross-skill-integration.md` § "seo-content-audit" for the full recipe.
   - **WebFetch first** (free, instant): pull the markdown for word count, H-tag hierarchy, source citations (links to authorities, numbered references), images, tables, code blocks, comment thread.
   - **Page-type detection.** From the URL pattern, H1 phrasing, and JSON-LD `@type`, classify the page as one of: ultimate guide / pillar, how-to, listicle / best-of, comparison (X vs Y), explainer, review (single product), landing page (commercial). Look up the corresponding word-count floor from `references/core-eeat.md` → "Word-count floors by page type". Surface the detected type, the applied floor, and the actual word count in `evidence/01-content-snapshot.md`. If the actual word count is materially below the floor, flag it for the depth E-E-A-T items (auto ✗ unless the auditor justifies the exception).
   - **Firecrawl second** — recovers what WebFetch's markdown loses:
     - From `metadata`: canonical URL, robots, lang, `og:title`.
     - From the returned `html`: every `<script type="application/ld+json">` block. Parse for `Article` / `BlogPosting` schema and extract `author` (name, `@type: Person`, optional `url` + `sameAs`), `datePublished` / `dateModified` (ISO 8601), `publisher`, `mainEntityOfPage`. Detect `Person` schema standalone if present.
     - DOM-level byline detection: locate the structural byline (`<a rel="author">`, `<meta name="author">`, `<span class="byline">`, `[itemprop="author"]`). Distinguish a real byline element from prose mentions ("Written by Jane in collaboration..." in body text is not a byline; `<a rel="author">Jane Doe</a>` is).
   - **If Firecrawl unavailable:** WebFetch portion runs unchanged. Mark schema-type detection and structural byline detection as `(skipped — Firecrawl required)` in `evidence/01-content-snapshot.md`. Step 4's veto checks #1 and #4 fall back to prose-level inspection (less reliable) — surface that caveat in `VERDICT.md`.

2. **AIO context** `DATA_getAiOverview` and `DATA_getAiOverviewLeaderboard`
   - For the target keyword: is there an AIO?
   - Who is cited in the AIO?
   - Is the candidate URL cited?
   - What patterns characterise the cited sources (publication tier, freshness, structure)?

3. **AIO prompt sampling** `DATA_getAiPromptsByTarget`
   - Sample LLM prompts where the target URL's domain appears as a source.
   - Cross-reference with the candidate URL — does it show up in any sampled prompts?

3b. **GA4 organic traffic on the audited URL** *(only if google-api.json is present, tier ≥ 2)*
   - Replaces the implicit traffic estimation with actual measured organic sessions for the audited URL.
   - Pull the top organic landing pages (last 28 days):
     `python3 scripts/ga4_report.py --report top-pages --days 28 --json`
   - Filter the result client-side for the audited URL's path. Surface in `VERDICT.md` "## Snapshot" alongside the existing AIO citation cross-check:
     - GA4 organic last 28d: `{sessions} sessions / {users} users / avg engagement {n}s`
     - If the URL doesn't appear in the top-100 organic landing pages: "GA4: not in top-100 organic landing pages last 28d — low or zero traffic."
   - **This is a signal, not a veto.** Low GA4 traffic on a YMYL page with high E-E-A-T is informative ("we're not earning the visibility our content quality should support") but doesn't change the publish decision.
   - See `skills/seo-google/references/cross-skill-integration.md` § "seo-content-audit" for the full recipe.

4. **Score E-E-A-T** using `references/core-eeat.md`
   - 60-item rubric across 4 dimensions (15 items each).
   - Per-item: yes/no/partial. Compute dimension scores (0–100% each).
   - Score the 8-item **AI-content markers** subsection (see references/core-eeat.md → "AI-content markers"). Mark each fired/not-fired.
   - Apply 4 veto checks. Any veto = no-publish.
     1. Anonymous author on YMYL topic. (High-confidence with Firecrawl-recovered author schema + DOM byline; medium-confidence with prose-only inspection.)
     2. Factual claims with no sources cited.
     3. Undisclosed affiliate / sponsored relationships.
     4. AI-generated YMYL content with no human-review markers (≥4 AI-content markers fired AND YMYL topic AND no editor byline / "reviewed by" credit / "last reviewed" or "fact-checked on" date). The "editor byline / reviewed by" check uses Firecrawl-recovered DOM byline + Article-schema `author` when available; falls back to prose-level pattern match if Firecrawl is absent (lower confidence — note in `VERDICT.md`).

5. **Score CITE** using `references/cite.md`
   - 30-item CITE rubric (Clear answer in 1st 200 words, Include primary stats, Timestamp freshness, Entity authority).
   - Per-item: yes/no/partial. Compute dimension scores.
   - Apply 3 veto checks (no answer in first 300 words / no datestamp on time-sensitive content / no entity disambiguation for proper-noun queries).

6. **Cross-check against AIO winners**
   - For the patterns characteristic of cited sources (from step 2), evaluate the candidate against each: does it have what the cited sources have?
   - Surface specific gaps.

7. **Synthesise verdict** using `templates/verdict.md`
   - **Publish:** E-E-A-T ≥ 75%, CITE ≥ 70%, no vetoes triggered.
   - **Publish with fixes:** E-E-A-T 60–74% OR CITE 55–69%, no vetoes. Top 5 fixes specified.
   - **No publish:** any veto triggered, OR E-E-A-T < 60%, OR CITE < 55%. Substantial rewrite needed.

## Output format

Create a folder `seo-content-audit-{target-slug}-{YYYYMMDD}/` with:

```
seo-content-audit-{target-slug}-{YYYYMMDD}/
├── VERDICT.md                       (publish / publish-with-fixes / no-publish — primary deliverable; inlines content snapshot + AIO context)
├── 03-eeat-scoring.md               (60-item rubric scored — load-bearing reference an editor consults item-by-item)
├── 04-cite-scoring.md               (30-item rubric scored — load-bearing reference)
├── 05-aio-winner-comparison.md      (gap vs cited sources — must remain top-level; live AIO competitive evidence per EVAL_RESULT_v2.md §9)
└── evidence/
    ├── 01-content-snapshot.md       (HTML extracts + page metadata — raw step output)
    └── 02-aio-context.md            (AIO presence, citations, patterns — raw step output)
```

Step files 01 + 02 are inlined as a "Snapshot" / "AIO context" section in `VERDICT.md`; the copies in `evidence/` preserve raw step output. `03-eeat-scoring.md`, `04-cite-scoring.md`, and `05-aio-winner-comparison.md` stay at top level — editors consult the rubric scoring detail directly, and the AIO winner comparison is the live competitive evidence the rubric verdict rests on.

`VERDICT.md` follows this shape (also see `templates/verdict.md`):

```markdown
# Content Audit: {URL or title}

> Audited {YYYY-MM-DD} · Target keyword: "{keyword}" · Country: {country}

## Verdict: {PUBLISH | PUBLISH WITH FIXES | NO PUBLISH}

{One sentence summary of why}

## Scores

| Dimension | Score | Threshold | Status |
|---|---|---|---|
| Experience | {n}% | 75% | {✓/✗} |
| Expertise | {n}% | 75% | {✓/✗} |
| Authoritativeness | {n}% | 75% | {✓/✗} |
| Trustworthiness | {n}% | 75% | {✓/✗} |
| **E-E-A-T composite** | {n}% | 75% | {✓/✗} |
| Clear answer | {n}% | 70% | {✓/✗} |
| Include stats | {n}% | 70% | {✓/✗} |
| Timestamp | {n}% | 70% | {✓/✗} |
| Entity authority | {n}% | 70% | {✓/✗} |
| **CITE composite** | {n}% | 70% | {✓/✗} |

## Veto checks

- Anonymous author on YMYL: {triggered / not triggered}
- Unsourced factual claims: {triggered / not triggered}
- Undisclosed affiliate / sponsored: {triggered / not triggered}
- AI-generated YMYL with no human review: {triggered / not triggered} ({n}/8 AI-content markers fired)
- ...

## AI Search readiness
- AIO present for "{keyword}": {yes/no}
- Top citation patterns: {list}
- Candidate URL cited in any sampled AIO: {yes/no}
- Gap vs cited sources: {bulleted gaps}

## Snapshot (measured)
- GA4 organic last 28d: {sessions} sessions / {users} users / avg engagement {n}s  *(or `not in top-100` / `not configured (Tier 2 required)`)*

## Top 5 fixes

1. {Specific fix linked to a low-scored item or veto}
2. ...
5. ...

## Detailed scoring

See:
- 03-eeat-scoring.md (item-by-item E-E-A-T)
- 04-cite-scoring.md (item-by-item CITE)
- 05-aio-winner-comparison.md (gap analysis)
```

## Tips

- Respect rate limit. AIO + AIO-prompts queries are ~5–10 calls; plenty of headroom.
- Call `DATA_getCreditBalance` before running. ~10–15 SE Ranking credits typical, plus 1 Firecrawl credit per URL audited when Firecrawl is installed (default cap 50 URLs).
- The thresholds (75% E-E-A-T, 70% CITE) are starting points. Tune per domain — a YMYL site (medical, financial) should require higher (85%/80%); a general-interest blog can run lower (65%/60%).
- The veto checks are not negotiable. A piece with anonymous authorship on a YMYL topic doesn't pass regardless of score.
- For pieces that score "publish with fixes," the top-5 list is the deliverable. Hand it to the writer; re-audit after fixes.
- Pair with `seo-content-brief` for the new-article counterpart: this skill audits existing content, content-brief produces new content.
- Pair with `seo-sxo` if the page has technical/page-type issues — that's a different diagnosis.
- The 60-item E-E-A-T rubric and 30-item CITE rubric are in `references/`. They are opinionated — adjust for your domain's editorial standards.
