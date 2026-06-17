# Claude SEO Skills

Production-ready [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for SEO, powered by the [SE Ranking remote MCP](https://seranking.com/api/integrations/mcp). Each skill turns raw API data into a finished SEO deliverable — content briefs, AI Search share of voice, page intelligence, structured data, drift monitoring, SXO diagnostics, competitive analysis, and more.

These Claude Skills are designed to work with the SE Ranking MCP server, but they document every API call explicitly so they can also be adapted to other SEO data providers.

## Install

Three ways. Pick the first one that fits.

### 1. Claude Desktop (recommended)

The easiest setup — no terminal needed. Cowork in Claude Desktop installs the plugin from a marketplace through a UI flow.

1. Open **Customize** in the sidebar.
2. Click **Personal plugin** → **+ Create plugin**.
3. Click **Add marketplace** and enter `seranking/seo-skills`.
4. Install the plugin once the marketplace loads.

Skills are available in your next Cowork session. Trigger them by name — `seo-content-brief`, `seo-page`, etc. — or just describe what you want and Claude picks the right one.

### 2. Claude Code (slash commands)

If you use Claude Code in the terminal:

```bash
/plugin marketplace add seranking/seo-skills
/plugin install seo-skills@seranking
```

Trigger skills with `/seo-content-brief`, `/seo-page`, etc. — no `seo-skills:` prefix needed. Or just describe what you want and Claude picks the right skill. Update the marketplace later with `/plugin marketplace update seranking`.

### 3. Manual install (only if you want `seo-google` or the optional extensions)

Options 1 and 2 cover **25 of 26 skills**. The 26th — `seo-google` — ships Python scripts that need a local clone. The optional Firecrawl + Google extensions also need this. **If neither matters to you, skip this option.**

```bash
git clone --depth 1 https://github.com/seranking/seo-skills.git
bash seo-skills/install.sh
```

The installer is interactive — it asks which extensions to install. Accept the defaults and you're done. Re-running pulls the latest version and re-runs the chosen extensions. Requires `git`, `python3` 3.10+, and (for Firecrawl) `node` 20+.

<details>
<summary>One-liner (curl)</summary>

```bash
curl -fsSL https://raw.githubusercontent.com/seranking/seo-skills/main/install.sh | bash -s -- --all
```

`--all` enables both extensions. Use `--firecrawl` / `--google` individually, or `--no-extensions` to clone only. Default clone target is `~/.local/share/seo-skills`; override with `--target /path/to/dir`.

</details>

The manual install only wires your *environment* (extensions, Python deps, `~/.config/seo-skills/`). You still need Option 1 or 2 above so Claude can find the skill files.

### 4. Cursor

SE Ranking is also packaged as a [Cursor plugin](.cursor-plugin/plugin.json). Once it is listed on [cursor.com/marketplace](https://cursor.com/marketplace), install it from the marketplace, or add it by name in Cursor:

```
/add-plugin se-ranking
```

The hosted SE Ranking MCP server is declared in [`mcp.json`](mcp.json) and is auto-detected when the plugin is installed — open Cursor's MCP settings and sign in via OAuth (no API token to manage). The same skills ship to the Cursor agent.

### Connect SE Ranking (any install path)

The SE Ranking remote MCP auto-registers when you install the plugin — there's no separate `claude mcp add` step. On your first session, run `/mcp` and sign in via OAuth. No API token to manage. If you don't have an SE Ranking account yet, [sign up](https://seranking.com/api.html) — API access is required.

<details>
<summary>Manual fallback (older Claude Code, or troubleshooting)</summary>

If `/mcp` doesn't list `se-ranking` after install — typically because you're on a Claude Code build that pre-dates plugin-bundled MCP servers — register it directly:

```bash
claude mcp add --transport http se-ranking https://api.seranking.com/mcp
```

Then run `/mcp` and complete OAuth. (User-scope registrations [outrank plugin-bundled ones](https://code.claude.com/docs/en/mcp#scope-hierarchy-and-precedence), so this safely overrides whatever the plugin shipped with.)

</details>

## What you get

25 finished example outputs — covering 25 of the 26 skills — live in [`examples/`](examples/). Each is a real run against a publicly observable target. Three flagship examples to skim before installing:

- **[`seo-plan` for wix.com (90-day plan)](examples/seo-plan-wix-com-20260514/PLAN.md)** — phased SEO roadmap that composes outputs from `seo-ai-search-share-of-voice`, `seo-competitor-gap-analysis`, and `seo-drift` into a 90-day plan with owners, success metrics, and a critical path. Demonstrates skill composition.
- **[`seo-technical-audit` for linear.app](examples/seo-technical-audit-linear-app-20260514/TECH-AUDIT.md)** — top-10 priority fix list ranked by `severity × affected_pages / effort`, plus `issues.csv` for the engineering team and a per-key-page issue digest.
- **[`seo-ai-search-share-of-voice` for wix.com](examples/seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md)** — 36.1% combined share of voice across 5 LLM engines (AI Overview / ChatGPT / Perplexity / Gemini / AI Mode), heatmap, topic-cluster ownership grid, and 5 prioritised gap-closing actions.

Full index of all 25 examples: [`examples/README.md`](examples/README.md). Every example is dated and snapshot-disclaimed — re-run the skill for fresh numbers.

## Skills

### Featured skills

The seven to reach for first — each links to a real, dated example run.

| Skill | What it produces | Example run |
|---|---|---|
| [`seo-ai-search-share-of-voice`](skills/seo-ai-search-share-of-voice/SKILL.md) | Share-of-voice heatmap across ChatGPT, Perplexity, Gemini, Google AI Overview, and AI Mode, plus topic-cluster ownership per brand | [wix.com](examples/seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md) |
| [`seo-backlink-gap`](skills/seo-backlink-gap/SKILL.md) | Prospect list of referring domains linking to multiple competitors but not to your site, enriched with authority, anchor samples, and outreach angles | [linear.app](examples/seo-backlink-gap-linear-app-20260514/REPORT.md) |
| [`seo-content-brief`](skills/seo-content-brief/SKILL.md) | Writer-ready editor brief from a domain and topic, with keyword research, SERP analysis, competitor content teardown, internal linking plan, and AI Search angle | [vercel.com](examples/seo-content-brief-vercel-rate-limiting-20260514/BRIEF.md) |
| [`seo-keyword-cluster`](skills/seo-keyword-cluster/SKILL.md) | Intent-grouped clusters with pillar plus spokes architecture and H1/H2 suggestions per spoke | [headless CMS](examples/seo-keyword-cluster-headless-cms-20260514/PLAN.md) |
| [`seo-ads`](skills/seo-ads/SKILL.md) | Paid-search competitive intelligence. Domain ad footprint, bidding landscape per keyword, ad-copy patterns, SERP shopping/ad-pack visibility, recommended bid-keyword shortlist | [hostinger.com](examples/seo-ads-hostinger-com-20260514/ADS.md) |
| [`seo-content-audit`](skills/seo-content-audit/SKILL.md) | E-E-A-T (60-item) + CITE (30-item) audit for existing content with publish / publish-with-fixes / no-publish verdict and citation-readiness analysis | [stripe.com](examples/seo-content-audit-stripe-rate-limiters-20260514/VERDICT.md) |
| [`seo-sxo`](skills/seo-sxo/SKILL.md) | Read SERPs backwards to find page-type mismatches. Scores the page from 4 personas; produces a wireframe for the SERP-winning page type | [bigin.com](examples/seo-sxo-bigin-com-20260514/SXO-REPORT.md) |

### More skills

The rest of the catalogue — every other skill the plugin ships.

| Skill | What it produces | Primary triggers |
|---|---|---|
| [`seo-competitor-gap-analysis`](skills/seo-competitor-gap-analysis/SKILL.md) | Keywords competitors rank for that the target does not, filtered by intent, volume, KD, and scored for priority | "competitor gap", "keyword gap", "organic content gap", "missing keyword opportunities" |
| [`seo-agency-landing-page`](skills/seo-agency-landing-page/SKILL.md) | Demand-gen landing page for an SEO agency with a free-audit lead magnet, grounded in real niche data | "SEO agency landing page", "lead-gen page", "free-audit landing page" |
| [`seo-page`](skills/seo-page/SKILL.md) | URL-level keyword & traffic intelligence with keep / refresh / consolidate / kill verdict for one page | "analyze this page", "page SEO performance", "what does this URL rank for", "should I refresh this page" |
| [`seo-schema`](skills/seo-schema/SKILL.md) | JSON-LD detect, validate, generate. Five bundled templates (Article / Product / LocalBusiness / FAQPage / BreadcrumbList) | "schema markup", "structured data", "JSON-LD", "rich results", "schema validation" |
| [`seo-images`](skills/seo-images/SKILL.md) | Image SEO audit for a URL or sampled domain: alt-text quality, WebP/AVIF coverage, `srcset`/`sizes`, lazy-loading + LCP signals (`loading` / `fetchpriority` / `decoding`), CLS dimensions, file naming, and `ImageObject` JSON-LD. Optional PSI byte-saving cross-reference. Paste-ready `<picture>` + JSON-LD snippets | "image SEO", "image audit", "alt-text audit", "WebP coverage", "AVIF", "responsive images", "lazy loading", "CLS images", "image schema", "ImageObject" |
| [`seo-drift`](skills/seo-drift/SKILL.md) | Git for SEO — baseline, compare, history. Severity-coded regression report across authority, traffic, keywords, backlinks, page fingerprint | "SEO drift", "did anything break", "deployment check", "baseline this site", "SEO regression" |
| [`seo-technical-audit`](skills/seo-technical-audit/SKILL.md) | One-shot technical audit: crawlability, indexability, security, mobile, structured data, JS rendering. Top-10 fix list ranked by impact × effort | "technical audit", "site audit", "audit my site", "crawl issues", "indexation issues" |
| [`seo-sitemap`](skills/seo-sitemap/SKILL.md) | Compare a domain's XML sitemap to the most recent SE Ranking audit. Surfaces missing-from-sitemap, orphans, broken entries, lastmod issues | "sitemap analysis", "check my sitemap", "missing pages", "orphan pages", "sitemap health" |
| [`seo-competitor-pages`](skills/seo-competitor-pages/SKILL.md) | Generate "X vs Y" / "alternatives to X" / "best X for Y" landing pages with feature matrix, schema, balanced verdict, and CTA flow | "comparison page", "vs page", "alternatives page", "X vs Y", "alternative to X" |
| [`seo-backlinks-profile`](skills/seo-backlinks-profile/SKILL.md) | Full backlink profile audit (vs gap-only `seo-backlink-gap`): authority distribution, anchor diversity, IP/subnet concentration, growth/decay, toxic-candidate flagging | "backlink profile", "link profile audit", "anchor distribution", "toxic links", "disavow candidates" |
| [`seo-subdomain`](skills/seo-subdomain/SKILL.md) | Subdomain ownership map. Lists subdomains, topic ownership, fragmentation/cannibalization flags, consolidate / split recommendations | "subdomain analysis", "subdomain ownership", "blog vs main domain", "should I consolidate subdomains" |
| [`seo-geo`](skills/seo-geo/SKILL.md) | URL-level Generative Engine Optimization analysis. AIO citation footprint per primary keyword + page passage-level audit + recommendations to improve LLM citability | "GEO for this page", "AIO citation analysis", "AI search readiness for URL", "why isn't this page cited" |
| [`seo-keyword-niche`](skills/seo-keyword-niche/SKILL.md) | Mine longtail + question keywords for niche content opportunities. Outputs a content-tier plan with template spec, URL pattern, sample pages, and thin-content quality gates | "longtail keywords", "question keywords", "niche content", "content opportunities at scale", "programmatic SEO" |
| [`seo-hreflang`](skills/seo-hreflang/SKILL.md) | Hreflang and international SEO audit for multi-language / multi-region sites. Validates language-region codes, return tags, `x-default`, and canonical alignment across per-URL HTML, the SE Ranking audit, and the XML sitemap. PASS / NEEDS-FIX / BROKEN verdict with a top-fixes table | "hreflang", "international SEO", "i18n", "language targeting", "x-default", "regional sites", "multi-language SEO" |
| [`seo-local`](skills/seo-local/SKILL.md) | Local SEO audit for brick-and-mortar, service-area, and multi-location businesses. Scores Google Business Profile signals on the page, NAP consistency across page and schema, on-page local intent, Tier-1 citation footprint, review-platform presence, and local-pack rank. Prioritised fix list | "local SEO", "GBP", "Google Business Profile", "NAP", "local pack", "citations", "near me", "service area", "multi-location SEO" |
| [`seo-firecrawl`](skills/seo-firecrawl/SKILL.md) | Ad-hoc web scraping, site mapping, full-site crawling, and within-domain search via Firecrawl. Returns raw HTML, JSON-LD, og:* / twitter:* metadata, JS-rendered DOM, and screenshots that WebFetch can't *(requires the [Firecrawl extension](#firecrawl-raw-html-json-ld-js-rendering-site-crawl))* | "scrape this page", "crawl this site", "map this site", "get the OG tags", "render this JS-heavy page" |
| [`seo-plan`](skills/seo-plan/SKILL.md) | Phased SEO roadmap for a domain — quarter-by-quarter, tied to competitive position, content gaps, technical debt, and AI Search readiness. Sequences specialist-skill outputs into one site-level plan with owners, metrics, and a critical path | "SEO plan", "SEO strategy", "SEO roadmap", "90-day plan", "where do we focus next" |
| [`seo-google`](skills/seo-google/SKILL.md) | Google's own SEO data: GSC Search Analytics + URL Inspection + Sitemaps, PageSpeed Insights, CrUX field data + 25-week history, Indexing API, GA4 organic, YouTube, NLP, Knowledge Graph, Web Risk, Keyword Planner. 4 credential tiers; lower tiers are useful on their own *(requires the [Google APIs extension](#google-apis-real-cwv-gsc-ga4-youtube-keyword-planner))* | "search console", "GSC", "PageSpeed", "CrUX", "URL inspection", "real CWV data", "GA4 organic", "google api setup" |
| [`seo-api`](skills/seo-api/SKILL.md) | SE Ranking API integration architect — covers the entire 195-tool surface (Data API + Project API), forecasts credit and plan-limit cost, emits ready-to-paste cURL / Python / TypeScript / MCP-tool-call recipes, and (with explicit confirmation) wires up Project API state (projects, keywords, search engines, audits, AIRT prompts, backlink groups) | "how do I use SE Ranking API to do X", "what endpoint gives me Y", "credit cost of workflow Z", "build a rank tracker", "set up an audit", "Postman / cURL / Python / TypeScript for SE Ranking", "rate limit for X", "integrate SE Ranking with Looker / n8n / Make" |

## Optional extensions

Some skills work best when paired with optional MCP servers or Python toolchains beyond SE Ranking. Each extension is opt-in — the skills that use it degrade gracefully when it's absent: they fall back to a lower-fidelity method, or note what was unavailable, rather than failing the run.

The fastest way to install both extensions is the top-level `install.sh` ([Install option 3](#3-manual-install-only-if-you-want-seo-google-or-the-optional-extensions)). The per-extension scripts below are equivalent — use them when you only want one of the two, or when you've already cloned the repo and want to install/re-install a single extension without re-running the wrapper.

### Firecrawl (raw HTML, JSON-LD, JS rendering, site crawl)

**Firecrawl is the recommended way to run any skill that inspects raw HTML — but it is not mandatory.** Without it, those skills fall back to `WebFetch` (Claude's built-in page fetch) and still produce a deliverable, just a lower-fidelity one: `WebFetch` returns markdown only, so every `<head>` `<meta>` tag, every `<link rel="canonical">`, and every `<script type="application/ld+json">` block is stripped before the skill sees it. The Firecrawl extension closes that gap and adds full-site crawl, URL discovery, in-site search, and screenshots.

```bash
# From inside a clone of this repo:
bash extensions/firecrawl/install.sh
```

The script verifies Node 20+, prompts for your `FIRECRAWL_API_KEY` (free tier is 500 credits/month at <https://firecrawl.dev>), and idempotently merges the MCP entry into `~/.claude/settings.json` (existing entries preserved). See [`extensions/firecrawl/README.md`](extensions/firecrawl/README.md) for full setup, free-tier credit math, troubleshooting, and tool-prefix details.

**Skills that gain capabilities when Firecrawl is installed:** `seo-page`, `seo-schema`, `seo-geo`, `seo-technical-audit`, `seo-sitemap`, `seo-content-audit`, `seo-drift`, `seo-content-brief`, `seo-competitor-pages`, `seo-sxo`, `seo-backlinks-profile`. Without Firecrawl, each of these falls back to `WebFetch` as described above — lower-fidelity, but still a usable deliverable — and supports a `--no-firecrawl` flag to opt out at runtime even when the extension is installed (saves credits). **Two skills are hard exceptions that need Firecrawl to run at all:** the dedicated `seo-firecrawl` orchestrator, and `seo-images` — `<img>` attributes (`srcset`, `loading`, `fetchpriority`, etc.) are stripped from `WebFetch`'s markdown, so the audit has nothing to analyse without it.

### Google APIs (real CWV, GSC, GA4, YouTube, Keyword Planner)

The `seo-google` skill needs the Google API client libraries plus a free Google Cloud project. All Google APIs used here are free (with quotas). Setup is one-time. Adapted with attribution from [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo)'s upstream `seo-google` skill (MIT) — same Python scripts and reference docs, namespaced to `~/.config/seo-skills/`.

```bash
# From inside a clone of this repo:
bash extensions/google/install.sh
```

The script verifies Python 3.10+, pip-installs the Google API libraries (`google-api-python-client`, `google-auth*`, `google-analytics-data`, plus `matplotlib` + `weasyprint` + `openpyxl` for PDF/HTML/XLSX reports), creates `~/.config/seo-skills/`, writes a stub `google-api.json`, and runs the credential checker.

Fill in the config per [`skills/seo-google/references/auth-setup.md`](skills/seo-google/references/auth-setup.md) (8-step walkthrough). The skill detects which tier is unlocked and only enables the matching commands — Tier 0 (API key) gives PSI + CrUX + YouTube + NLP + Knowledge Graph + Web Risk; Tier 1 (+ service account) adds GSC + Indexing; Tier 2 (+ GA4 property ID) adds GA4; Tier 3 (+ Ads dev token) adds Keyword Planner. See [`extensions/google/README.md`](extensions/google/README.md) for full setup, troubleshooting, and rate-limit reference.

**Skills that gain capabilities when Google APIs are configured:** `seo-google` (the dedicated skill — fully gated on this extension), plus `seo-page`, `seo-drift`, `seo-technical-audit`, `seo-content-audit`, `seo-sitemap`, `seo-geo`, `seo-keyword-cluster`, `seo-keyword-niche`, and `seo-plan` (real impressions/clicks/conversions/CWV instead of estimates when configured).

## How these skills work

Each skill is a single `SKILL.md` file with YAML frontmatter. Claude loads the frontmatter at startup to know when to use the skill, then loads the body only when triggered, then reads any bundled reference files only when needed. This is Anthropic's [progressive disclosure](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) pattern.

A typical skill run produces:

1. A set of numbered raw-data markdown files (`01-domain-overview.md`, `02-competitors.md`, etc.) for auditability.
2. Optionally, a CSV for spreadsheet work.
3. A final synthesised deliverable (`BRIEF.md`, `REPORT.md`, or `PLAN.md`) written in a format a human reviewer or downstream stakeholder can consume directly.

The skills chain naturally. A typical agency workflow:

1. Run `seo-competitor-gap-analysis` to see what opportunities exist.
2. Run `seo-keyword-cluster` on the gap output to plan content.
3. Run `seo-content-brief` on each cluster's pillar topic.
4. Run `seo-backlink-gap` to identify link targets for the new content.
5. Run `seo-ai-search-share-of-voice` quarterly to track LLM visibility.

## Repository layout

```
seo-skills/
├── .claude-plugin/
│   ├── marketplace.json                # Claude Code marketplace manifest
│   └── plugin.json                     # Plugin manifest
├── skills/
│   ├── seo-content-brief/
│   │   └── SKILL.md
│   ├── seo-ai-search-share-of-voice/
│   │   └── SKILL.md
│   ├── seo-backlink-gap/
│   │   └── SKILL.md
│   ├── seo-keyword-cluster/
│   │   └── SKILL.md
│   ├── seo-competitor-gap-analysis/
│   │   └── SKILL.md
│   ├── seo-agency-landing-page/
│   │   └── SKILL.md
│   ├── seo-page/
│   │   └── SKILL.md
│   ├── seo-schema/
│   │   ├── SKILL.md
│   │   ├── templates/                  # 6 JSON-LD starter templates
│   │   └── references/google-rich-results.md
│   ├── seo-drift/
│   │   ├── SKILL.md
│   │   └── references/drift-thresholds.md
│   ├── seo-sxo/
│   │   ├── SKILL.md
│   │   └── references/                 # page-type patterns + persona rubrics
│   ├── seo-technical-audit/
│   │   ├── SKILL.md
│   │   └── references/severity-mapping.md
│   ├── seo-content-audit/
│   │   ├── SKILL.md
│   │   ├── references/                 # core-eeat (60 items) + cite (30 items)
│   │   └── templates/verdict.md
│   ├── seo-sitemap/
│   │   └── SKILL.md
│   ├── seo-competitor-pages/
│   │   └── SKILL.md
│   ├── seo-backlinks-profile/
│   │   └── SKILL.md
│   ├── seo-subdomain/
│   │   └── SKILL.md
│   ├── seo-geo/
│   │   └── SKILL.md
│   ├── seo-ads/
│   │   └── SKILL.md
│   ├── seo-keyword-niche/
│   │   └── SKILL.md
│   ├── seo-firecrawl/                  # Ad-hoc Firecrawl orchestrator (extension required)
│   │   └── SKILL.md
│   ├── seo-plan/
│   │   └── SKILL.md
│   ├── seo-google/                     # Google APIs skill (extension required)
│   │   ├── SKILL.md
│   │   ├── assets/templates/           # 3 report templates (cwv-audit, gsc-performance, indexation)
│   │   └── references/                 # 10 API reference docs (auth, GSC, PSI, CrUX, GA4, etc.)
│   └── seo-api/                        # SE Ranking API integration architect
│       ├── SKILL.md
│       └── references/                 # auth-and-keys, rate-limits-and-credits, api-surface-map, integration-patterns
├── scripts/                            # Python scripts called by seo-google (forked from AgriciDaniel/claude-seo, MIT)
│   ├── google_auth.py
│   ├── pagespeed_check.py
│   ├── crux_history.py
│   ├── gsc_query.py
│   ├── gsc_inspect.py
│   ├── indexing_notify.py
│   ├── ga4_report.py
│   ├── youtube_search.py
│   ├── nlp_analyze.py
│   ├── keyword_planner.py
│   └── google_report.py
├── extensions/
│   ├── firecrawl/                      # Optional Firecrawl MCP wiring
│   │   ├── install.sh
│   │   ├── uninstall.sh
│   │   └── README.md
│   └── google/                         # Optional Google APIs Python toolchain
│       ├── install.sh
│       ├── uninstall.sh
│       ├── README.md
│       └── LICENSE-AgriciDaniel.txt    # MIT attribution for forked content
├── examples/                           # Real, end-to-end runs against public targets
│   └── seo-ai-search-share-of-voice-wix-com-20260427/
├── install.sh                          # Top-level installer (clone + extension installers)
├── CHANGELOG.md
├── LICENSE
└── README.md
```

The repo is a Claude Code marketplace whose single plugin is the repo itself (marketplace `plugins[0].source` is `"./"`). This keeps skill folders visible at the top level rather than buried two layers deep.

Every skill writes its output to a folder named `{skill-slug}-{target-slug}-{YYYYMMDD}/` (e.g., `seo-content-brief-example-com-20260427/`). The date stamp keeps re-runs non-destructive and makes it easy to diff outputs over time. Browse [`examples/`](./examples/) to see what a finished run looks like before installing.

## Rate limits and costs

The SE Ranking MCP server has two namespaces with different rate limits:

- **Data API** (`DATA_*`): 10 requests per second. Charges API credits per call.
- **Project API** (`PROJECT_*`): 5 requests per second. Retrieval and management calls do not charge; writes consume quota slots.

Every skill in this repo is designed to pace sequentially inside these limits. The largest skills (`seo-competitor-gap-analysis` with full keyword dumps, `seo-keyword-cluster` with 20 seeds) can consume thousands of credits on large domains. Check `DATA_getCreditBalance` before running on production accounts, and use the `ceiling` parameters the skills document to cap cost.

## Contributing

This repo is the official Skills catalogue for the SE Ranking MCP server. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the skill-authoring template, required structure, MCP tool conventions, and PR checklist.

- **Bug reports** — open an issue with the skill name, the input, and the unexpected output.
- **New skills** — PRs welcome. Use the template in `CONTRIBUTING.md`.
- **Improvements** — PRs welcome. Include a before/after example run in the PR description.

## Links

- SE Ranking: https://seranking.com
- SE Ranking API: https://seranking.com/api.html
- SE Ranking remote MCP: https://seranking.com/api/integrations/mcp
- Claude Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code Plugins: https://code.claude.com/docs/en/plugins

## License

MIT. See [LICENSE](LICENSE).
