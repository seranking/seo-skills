---
name: seo-technical-audit
description: Focused one-shot technical SEO audit for a domain. Crawlability, indexability, security, mobile, structured data, JS rendering — single-pass deliverable, not a diff. Distinct from `seo-drift` (which tracks changes over time) and from `seo-page` (which audits keywords/traffic for one URL, not technical health). Use when the user asks "technical audit", "site audit", "audit my site", "crawl issues", "indexation issues", or "technical SEO check".
---

# Technical Audit

A one-shot technical SEO audit for a domain. Pulls SE Ranking's audit data, categorizes findings by area (crawlability, indexability, security, mobile, structured data, etc.), severity-sorts within each, and produces a top-10 fix list ranked by impact × effort.

## Prerequisites

- SE Ranking MCP server connected.
- Claude's `WebFetch` tool available (used for sense-checking robots.txt and sitemap presence).
- User provides: a target domain (e.g. `example.com`). Optional: target country (default `us`), audit-page-limit override (default: rely on the existing audit's limit).

## Process

1. **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (credit balance, Firecrawl availability, Google APIs). Skill-specific notes:
   - Normalise domain (strip protocol, trailing slash) before continuing.
   - Estimated SE Ranking cost for this skill: a re-check of an existing audit is cheap; creating a new audit is significantly more expensive and varies by page count. Surface the cost before deciding.
   - Firecrawl: optional. When available, step 8 (Modern signals checklist) runs on 5 sample URLs and `/robots.txt`, ~6 Firecrawl credits (hard cap). Without it, step 8 is skipped — JS-render canonical/noindex divergence, X-Robots-Tag headers, and AI-crawler robots-rule analysis are unavailable but the full technical-audit deliverable still ships. Pass `--no-firecrawl` to skip step 8 even when Firecrawl is available (saves credits).
   - Google APIs: tier 0 unlocks step 8b (CrUX field data); tier 1 also unlocks step 8c (per-URL GSC Inspection on top 5 traffic pages). See `skills/seo-google/references/cross-skill-integration.md` § "seo-technical-audit" for the full recipe and per-tier branches.

2. **Find or create the audit** `DATA_listAudits`
   - List audits for the domain.
   - If a recent audit exists (<30 days old), use it.
   - If older than 30 days, run `DATA_recheckAudit` to refresh.
   - If none exists, ask the user before creating a new one with `DATA_createStandardAudit` (it consumes credits).
   - Wait for `DATA_getAuditStatus` to report `done` before pulling the report.

3. **Pull the audit report** `DATA_getAuditReport`
   - Top-line metrics: pages crawled, health score, total issues by severity.
   - Issues grouped by category (crawlability, indexability, mobile, security, structured data, etc.).

4. **Pull per-issue page lists** `DATA_getAuditPagesByIssue`
   - For each significant issue (severity ≥ medium, count ≥ 5), pull the affected URLs.
   - This produces the actionable fix list.

5. **Cross-reference key URLs** `DATA_getIssuesByUrl`
   - For the top 5 pages by traffic (from `DATA_getDomainKeywords`'s page aggregation, or homepage + key landing pages if no keyword data), pull all issues for those specific URLs.
   - This catches cases where one important page concentrates many issues.

6. **Sense-check** `WebFetch`
   - Fetch `/robots.txt` and `/sitemap.xml` directly.
   - Confirm the audit's findings match reality on these critical files (audits sometimes lag behind same-day deploys).
   - **Extended security headers.** WebFetch the homepage and 3 sample URLs (top-traffic landing pages from step 5, fall back to homepage + key landing pages if no keyword data); read response headers and flag any of:
     - `csp_missing` — `Content-Security-Policy` absent.
     - `xframe_missing` — `X-Frame-Options` absent (informational; CSP `frame-ancestors` supersedes).
     - `xcontent_missing` — `X-Content-Type-Options` not set to `nosniff`.
     - `referrer_policy_missing` — `Referrer-Policy` absent.
     - `hsts_no_preload` — `Strict-Transport-Security` present but `preload` directive missing AND domain not on the Chromium HSTS preload list.
   - Map findings via `references/severity-mapping.md` § Security and surface in `evidence/02-issues-by-category/security.md` (and inline into TECH-AUDIT.md's "By category → Security" section).

7. **Categorize and prioritize** using `references/severity-mapping.md`
   - Map each issue code to severity, fix, and effort estimate.
   - Score each finding: severity × affected-page-count / effort.
   - Build the top-10 fix list.

8. **Modern signals checklist** `mcp__firecrawl-mcp__firecrawl_scrape`
   - SE Ranking's audit crawler doesn't execute JS and doesn't expose response headers per page. This step surfaces what's invisible to it.
   - **If Firecrawl available** (~6 Firecrawl credits, hard cap): pick 5 sample URLs from the audit — bias toward high-traffic landing pages and pages already flagged with noindex / canonical issues. For each:
     - **JS-rendered canonical vs initial-HTML canonical (`js_canonical_mismatch`).** Compare `metadata.canonical` (after JS render) against the canonical the audit recorded. Flag any divergence — per Google's Dec-2025 JavaScript SEO guidance, when a canonical in raw HTML differs from one injected by JS, Google MAY use either one, making canonical decisions non-deterministic. JS-injected canonical changes silently break indexing on JS-heavy sites.
     - **JS-rendered noindex.** Check `metadata.robots` for `noindex` after render. Catches client-side-only `noindex` injection that the audit can't see.
     - **X-Robots-Tag header.** Read response headers from `metadata`. Flag any `noindex` / `nofollow` / `none` directives at the HTTP layer.
     - **Dec-2025 JS-SEO risk detection** (Google's December 2025 JavaScript SEO guidance — four risks the static crawler cannot detect):
       - **Risk 1 — Rendering-budget cuts (`js_render_budget`).** Compare initial-HTML body size to rendered-HTML body size. Flag pages where rendered HTML is <50% of initial HTML size after JS execution — indicates Google may exhaust its render budget before the page's actual content loads.
       - **Risk 2 — Hydration mismatch.** Already detected above via `js_canonical_mismatch`; rationale: per the Dec-2025 guidance Google may pick *either* canonical, so any drift is a real-world ranking risk, not just a tidiness issue.
       - **Risk 3 — CSR pitfalls (`js_csr_meta_drift`).** Diff initial-HTML `<title>`, `<h1>`, and `<meta name="description">` against the same fields in the JS-rendered DOM. Flag any divergence — Google does not reliably index content that only appears post-render, so the empty/wrong initial values may be what gets indexed.
       - **Risk 4 — Soft-404 from JS errors (`js_soft_404`).** Flag rendered pages where body text content is <500 chars but the HTTP response status is 200. This pattern indicates a JS render failure that Google treats as a soft-404 — the page returns 200 (so it's "live") but contains no real content (so it's "empty").
     - Then make one additional call: `firecrawl_scrape` on `/robots.txt` (1 credit). Parse for AI-crawler User-Agent rules — `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `ChatGPT-User`, `Bytespider`, `CCBot`. Surface allow/disallow scope per agent.
   - **If Firecrawl unavailable:** skip this step. Note in `TECH-AUDIT.md`: `Modern signals (JS canonical/noindex divergence, X-Robots-Tag, AI-crawler robots.txt rules, Dec-2025 JS-SEO risks): skipped — Firecrawl not installed.`

8b. **CWV field data via CrUX** *(only if google-api.json is present, tier ≥ 0)*
   - SE Ranking's audit reports lab-only CWV (Lighthouse-flavoured estimates). CrUX returns actual Chrome user p75 metrics — the data Google ranks against.
   - Run `python3 scripts/pagespeed_check.py "https://{domain}" --crux-only --json` for current p75 LCP / INP / CLS / FCP / TTFB.
   - Run `python3 scripts/crux_history.py "https://{domain}" --origin --json` for the 25-week trend per metric (improving / stable / degrading).
   - If CrUX has no field data ("insufficient data"), surface that and continue — low-traffic origins are common.
   - Surface in `TECH-AUDIT.md` as a new section "## Core Web Vitals (field data)" with current p75 + trend per metric, source labelled "CrUX 28-day origin".

8c. **Per-URL indexation status via GSC URL Inspection** *(only if google-api.json is present, tier ≥ 1)*
   - For each of the top 5 traffic pages identified in step 5 (or homepage + key landing pages if no keyword data), run:
     `python3 scripts/gsc_inspect.py "{url}" --site-url "{config.default_property}" --json`
   - Capture `indexStatusVerdict`, `coverageState`, `googleCanonical` (vs `userCanonical`), and `lastCrawlTime` per URL.
   - **Cross-check against the audit's noindex / canonical findings.** If GSC reports `INDEXED` but the audit flagged `noindex`, the audit is stale or the directive was added recently — flag for re-audit. If GSC reports `EXCLUDED` for a page the audit treats as healthy, that's a hidden indexability issue the SE Ranking audit can't see.
   - **Critical-issue elevation:** any `userCanonical ≠ googleCanonical` divergence on a top-traffic page is added to the Top-10 fix list at Critical severity regardless of `severity-mapping.md`'s default — Google having decided on a different canonical is a real-world ranking problem.
   - If the property isn't verified in GSC for this account, surface "GSC: {domain} not verified — add it in Search Console" and skip 8c only.
   - Surface in `TECH-AUDIT.md` as a new section "## Indexation reality check (GSC URL Inspection)" with one row per top-5-traffic URL: status / canonical-divergence / last-crawled.
   - See `skills/seo-google/references/cross-skill-integration.md` § "seo-technical-audit" for the full recipe and failure modes.

8d. **IndexNow detection** `WebFetch`
   - Detection logic — IndexNow advertises its key one of three ways. Check in this order:
     1. **robots.txt hint:** look in the already-fetched `/robots.txt` (step 6) for an `IndexNow:` directive or a comment referencing the key file path.
     2. **Response header hint:** scan response headers from the homepage WebFetch (step 6) for `x-indexnow-key`, `x-indexnow`, or `x-indexnow-key-location`.
     3. **Conventional path probe:** WebFetch `/<key>.txt` if a key was hinted in (1) or (2). If neither hint exists, additionally probe a small set of conventional locations only when the user's domain has signalled IndexNow elsewhere (e.g. Bing Webmaster integration disclosed in robots.txt).
   - Map findings via `references/severity-mapping.md` § IndexNow:
     - No key advertised anywhere → `indexnow_no_key` (Low; informational — Bing-only benefit).
     - Key advertised but `/<key>.txt` content ≠ advertised key → `indexnow_key_mismatch` (Medium).
     - Key file present and matches but no recent submissions detected → `indexnow_not_submitted_recently` (Low; informational).
   - Detect last-key-rotation date when possible: WebFetch the key file and read the `Last-Modified` response header (or fall back to the file's `Date` header).
   - Surface in `evidence/02-issues-by-category/security.md` (or a new `evidence/02-issues-by-category/indexnow.md` if findings are non-trivial; either way, fold into TECH-AUDIT.md's "By category" section) and add a row to the `TECH-AUDIT.md` Modern signals section showing IndexNow status: configured (Y/N) and last-key-rotation date if detectable.

9. **Synthesise** `TECH-AUDIT.md`

## Output format

Create a folder `seo-technical-audit-{target-slug}-{YYYYMMDD}/` with:

```
seo-technical-audit-{target-slug}-{YYYYMMDD}/
├── TECH-AUDIT.md                       (synthesised top-10 fix list + category summary — primary deliverable; inlines 01-audit-summary header + the six 02-issues-by-category/* tables under "By category")
├── issues.csv                          (every issue: code, severity, count, fix, effort — load-bearing CSV engineering pastes into Jira)
├── 03-key-pages-issues.md              (top 5 traffic pages, all their issues — load-bearing reference engineering / on-call consult per-URL)
└── evidence/
    ├── 02-issues-by-category/          (raw per-category tables — preserved in case a reader wants the unmerged view)
    │   ├── crawlability.md
    │   ├── indexability.md
    │   ├── security.md
    │   ├── mobile.md
    │   ├── structured-data.md
    │   └── content.md
    ├── 04-robots-sitemap-snapshot.md   (raw fetched files — preserved for reproducibility)
    └── 05-modern-signals.md            (JS-render canonical/noindex divergence, X-Robots-Tag, AI-crawler rules — requires Firecrawl)
```

Top-level: `TECH-AUDIT.md` + `issues.csv` + `03-key-pages-issues.md`. The audit summary header (`01-audit-summary`) is already in TECH-AUDIT.md's header; the six per-category tables (`02-issues-by-category/*.md`) are inlined under TECH-AUDIT.md's "By category" section. The raw category files, robots/sitemap snapshot, and modern-signals dump live under `evidence/` for reproducibility.

`TECH-AUDIT.md` follows this shape:

```markdown
# Technical Audit: {domain}

> Audit date {YYYY-MM-DD} · Pages crawled: {n} · Health score: {n}/100

## Summary

| Severity | Count |
|---|---|
| Critical | {n} |
| High | {n} |
| Medium | {n} |
| Low | {n} |

## Top 10 fixes (impact × effort)

| Rank | Issue | Severity | Pages | Fix | Effort |
|---|---|---|---|---|---|
| 1 | {issue name} | {severity} | {n} | {one-line fix} | {S/M/L} |
| ... |

## By category

### Crawlability ({n} issues)
- {issue name} ({n} pages) — {fix}
- ...

### Indexability ({n} issues)
- ...

### Security ({n} issues)
- ...

### Mobile ({n} issues)
- ...

### Structured data ({n} issues)
- ...

### Content ({n} issues)
- ...

### Modern signals ({n} findings — Firecrawl)
- {URL} — initial-HTML canonical `{X}` differs from JS-rendered canonical `{Y}` (`js_canonical_mismatch`)
- {URL} — JS-rendered `noindex` not visible to static crawler
- {URL} — `X-Robots-Tag: noindex` at HTTP layer
- {URL} — rendered HTML <50% of initial HTML size (`js_render_budget` — Google may stop rendering before content loads)
- {URL} — title / H1 / meta description differ between initial HTML and post-render DOM (`js_csr_meta_drift`)
- {URL} — rendered body <500 chars but HTTP 200 (`js_soft_404` — likely JS render failure, treated as soft-404 by Google)
- robots.txt — `GPTBot`: {allow / disallow `/path`}, `ClaudeBot`: {…}, `Google-Extended`: {…}, ...
- IndexNow — configured: {Y/N} · key-file: `/<key>.txt` {found / missing / mismatch} · last-key-rotation: {YYYY-MM-DD or "unknown"}
- (Or: `Modern signals: skipped — Firecrawl not installed`)

### Security headers (extended — WebFetch)

| Header | Homepage | Sample 1 | Sample 2 | Sample 3 | Issue |
|---|---|---|---|---|---|
| Content-Security-Policy | {present/absent} | … | … | … | `csp_missing` if absent |
| X-Frame-Options | {present/absent} | … | … | … | `xframe_missing` if absent (informational; CSP frame-ancestors supersedes) |
| X-Content-Type-Options | {`nosniff`/absent/other} | … | … | … | `xcontent_missing` if not `nosniff` |
| Referrer-Policy | {present/absent} | … | … | … | `referrer_policy_missing` if absent |
| HSTS preload | {preload directive Y/N · on Chromium preload list Y/N} | … | … | … | `hsts_no_preload` if not on list |

## Core Web Vitals (field data — CrUX)

| Metric | p75 (current) | 25-week trend | Threshold | Status |
|---|---|---|---|---|
| LCP | {n} ms | {improving/stable/degrading} | ≤2500 ms good · ≤4000 ms needs improvement | {pass/warn/fail} |
| INP | {n} ms | … | ≤200 ms good · ≤500 ms needs improvement | … |
| CLS | {n} | … | ≤0.1 good · ≤0.25 needs improvement | … |
| FCP | {n} ms | … | ≤1800 ms good · ≤3000 ms needs improvement | … |
| TTFB | {n} ms | … | ≤800 ms good · ≤1800 ms needs improvement | … |

Source: CrUX 28-day origin. If insufficient field data: "CrUX: insufficient data for {domain} (low-traffic origin)."
(Or: `CWV (field data): not configured — run `bash extensions/google/install.sh` for setup.`)

## Indexation reality check (GSC URL Inspection)

| URL | Status | userCanonical → googleCanonical | Last crawled |
|---|---|---|---|
| {top-traffic URL 1} | {INDEXED|EXCLUDED|...} | {URL} {→ different URL if divergent} | {YYYY-MM-DD} |
| {top-traffic URL 2} | … | … | … |
| ... |

Source: GSC URL Inspection (Tier 1). If property not verified: "GSC: {domain} not verified — add it in Search Console."
(Or: `Indexation reality check: not configured (Tier 1 setup required).`)

## Key-page deep dives

### {URL with most issues}
{n} issues found. Top fixes:
1. ...
2. ...

## Recommended cadence
Re-run this skill monthly to catch regressions, or wire `seo-drift` to baseline + diff between audits.
```

`issues.csv` columns: `category,issue_code,issue_name,severity,affected_pages,suggested_fix,effort,priority_score`

## Tips

- Respect rate limit: 10 req/sec.
- Reuse existing audits when possible — creating a new audit is the most expensive operation.
- A fresh audit on a 1k-page site can take 10–30 minutes to complete. The skill polls `DATA_getAuditStatus` until `done` — be patient.
- The severity scale comes from SE Ranking's audit (not arbitrary). Map them via `references/severity-mapping.md` so impact × effort scoring is consistent run-to-run.
- For sites with >10k pages, consider auditing critical sections separately (set audit URL filters in SE Ranking) rather than crawling the whole site every time.
- Pair with `seo-drift` for regression tracking: this skill is the snapshot, drift is the diff.
- Pair with `seo-sitemap` for orphan/missing-page analysis (it consumes this skill's audit data).
- Don't auto-apply fixes. The skill diagnoses; humans decide which fixes to ship and in what order.
