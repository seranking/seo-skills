# Claude SEO Skills

**32 free, open-source Claude SEO skills** for Claude (claude.ai, Claude Desktop and Cowork, Claude Code) and any AI agent that supports Agent Skills and MCP. Each SEO skill turns live [SE Ranking](https://seranking.com) data into a finished deliverable: content briefs, technical audits, AI search share of voice, backlink gap lists, keyword clusters and 90-day SEO plans.

Overview and use cases: [Claude SEO Skills by SE Ranking](https://seranking.com/claude-seo-skills.html).

## About this edition

This is the Claude Plugins Directory edition: the same 32 skills, without local scripts. What it doesn't include:

- **Live Google data** (Search Console, GA4, CrUX field data, PageSpeed Insights). `seo-google` points you to the full edition, and the Google steps in `seo-page`, `seo-technical-audit`, `seo-content-audit`, `seo-local`, `seo-hreflang`, `seo-drift`, `seo-images` and `seo-plan` are skipped and marked "not available in this edition" in the report.
- **The Google API setup** for those scripts, and the Cursor and Codex packages. Firecrawl works here through its connector in the Claude directory.

Everything else runs on SE Ranking data. The full edition is on GitHub: https://github.com/seranking/seo-skills

Production-ready [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for SEO, powered by the [SE Ranking MCP](https://seranking.com/mcp.html). Each skill turns raw API data into a finished SEO deliverable — content briefs, AI Search share of voice, page intelligence, structured data, drift monitoring, SXO diagnostics, competitive analysis, and more.

These Claude Skills are designed to work with the SE Ranking MCP server, but they document every API call explicitly so they can also be adapted to other SEO data providers.

## What are Claude SEO skills?

Claude SEO skills are reusable instructions that teach Claude how to run a specific SEO task end to end: which data to pull, in what order, and what file to produce. Instead of writing a long prompt each time, you ask for "a content brief for X" or "a backlink gap vs. these competitors", and Claude picks the matching skill. The skills in this repo get their data from the SE Ranking MCP server, so every brief, audit and report is based on live keyword, backlink, SERP and AI search data rather than the model's memory.

## Install

### Install from the Claude directory

Select **Install** on this plugin's listing in claude.ai, Claude Desktop (Cowork) or Claude Code. The SE Ranking MCP server comes with the plugin; connect it as described below.

Trigger skills by name (`seo-content-brief`, `seo-page`, …), or just describe what you want and Claude picks the right one.

### Prefer the full edition?

The full edition on GitHub adds the `seo-google` Python scripts with their Google API setup, and Cursor and Codex packages. Install it from the `seranking/seo-skills` marketplace *instead of* this listing, not in addition to it, so you don't get two copies of the same skills: https://github.com/seranking/seo-skills#install

### Connect SE Ranking (any install path)

The SE Ranking remote MCP auto-registers when you install the plugin — there's no separate `claude mcp add` step. On your first session, run `/mcp` (or open your connectors) and sign in via OAuth. No API token to manage. If you don't have an SE Ranking account yet, [start a free trial](https://seranking.com/sign-up.html?landing=claude_seo_skills&utm_source=claude_directory&utm_medium=listing&utm_campaign=seo_skills) — it includes 100K API credits and MCP access for 14 days.

<details>
<summary>Manual fallback (older Claude Code, or troubleshooting)</summary>

If `/mcp` doesn't list `se-ranking` after install — typically because you're on a Claude Code build that pre-dates plugin-bundled MCP servers — register it directly:

```bash
claude mcp add --transport http se-ranking https://api.seranking.com/mcp
```

Then run `/mcp` and complete OAuth. (User-scope registrations [outrank plugin-bundled ones](https://code.claude.com/docs/en/mcp#scope-hierarchy-and-precedence), so this safely overrides whatever the plugin shipped with.)

</details>

## What the SE Ranking tools can do

The plugin connects one MCP server, SE Ranking's own. Its tools act only in the SE Ranking and SE Visible account you sign in with. Most of them only read: keyword, domain, backlink, SERP and AI-search data, and the projects, audits and reports in your account. Some tools change things there:

- **Create and edit:** projects and project groups, keywords and keyword groups, tags, competitors, search engines, backlinks and the disavow list, website audits and their settings, marketing-plan tasks, and AI-search prompts, engines, brands, topics and locations.
- **Delete:** the same things, including a whole project, an audit or a brand. A deletion can't be undone from Claude.
- **Change access:** create, edit and delete sub-accounts, and choose which projects a client sub-account can see.
- **Send:** creating a sub-account makes SE Ranking email that person a temporary password. No other tool sends a message.
- **Use credits:** most Data API tools (`DATA_*`), reads included, use your API credits. Audits, position checks and rechecks also count against your plan's limits.

No tool publishes anything outside SE Ranking, pays for anything or changes your subscription. The six social skills also create draft posts in Planable when you've connected it; publishing stays in Planable.

## What you get

25 finished example outputs — covering 25 of the 32 skills — live in [`examples/`](https://github.com/seranking/seo-skills/tree/v2.11.6/examples). Each is a real run against a publicly observable target. Three flagship examples to skim before installing:

- **[`seo-plan` for wix.com (90-day plan)](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-plan-wix-com-20260514/PLAN.md)** — phased SEO roadmap that composes outputs from `seo-ai-search-share-of-voice`, `seo-competitor-gap-analysis`, and `seo-drift` into a 90-day plan with owners, success metrics, and a critical path. Demonstrates skill composition.
- **[`seo-technical-audit` for linear.app](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-technical-audit-linear-app-20260514/TECH-AUDIT.md)** — top-10 priority fix list ranked by `severity × affected_pages / effort`, plus `issues.csv` for the engineering team and a per-key-page issue digest.
- **[`seo-ai-search-share-of-voice` for wix.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md)** — 36.1% combined share of voice across 5 LLM engines (AI Overview / ChatGPT / Perplexity / Gemini / AI Mode), heatmap, topic-cluster ownership grid, and 5 prioritised gap-closing actions.

Full index of all 25 examples: [`examples/README.md`](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/README.md). Every example is dated and snapshot-disclaimed — re-run the skill for fresh numbers.

## All 32 Claude SEO Skills

### Featured SEO skills

The seven to reach for first — each links to a real, dated example run.

| Skill | What it produces | Example run |
|---|---|---|
| [`seo-ai-search-share-of-voice`](skills/seo-ai-search-share-of-voice/SKILL.md) | Share-of-voice heatmap across ChatGPT, Perplexity, Gemini, Google AI Overview, and AI Mode, plus topic-cluster ownership per brand | [wix.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-ai-search-share-of-voice-wix-com-20260427/REPORT.md) |
| [`seo-backlink-gap`](skills/seo-backlink-gap/SKILL.md) | Prospect list of referring domains linking to multiple competitors but not to your site, enriched with authority, anchor samples, and outreach angles | [linear.app](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-backlink-gap-linear-app-20260514/REPORT.md) |
| [`seo-content-brief`](skills/seo-content-brief/SKILL.md) | Writer-ready editor brief from a domain and topic, with keyword research, SERP analysis, competitor content teardown, internal linking plan, and AI Search angle | [vercel.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-content-brief-vercel-rate-limiting-20260514/BRIEF.md) |
| [`seo-keyword-cluster`](skills/seo-keyword-cluster/SKILL.md) | Intent-grouped clusters with pillar plus spokes architecture and H1/H2 suggestions per spoke | [headless CMS](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-keyword-cluster-headless-cms-20260514/PLAN.md) |
| [`seo-ads`](skills/seo-ads/SKILL.md) | Paid-search competitive intelligence. Domain ad footprint, bidding landscape per keyword, ad-copy patterns, SERP shopping/ad-pack visibility, recommended bid-keyword shortlist | [hostinger.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-ads-hostinger-com-20260514/ADS.md) |
| [`seo-content-audit`](skills/seo-content-audit/SKILL.md) | E-E-A-T (60-item) + CITE (30-item) audit for existing content with publish / publish-with-fixes / no-publish verdict and citation-readiness analysis | [stripe.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-content-audit-stripe-rate-limiters-20260514/VERDICT.md) |
| [`seo-sxo`](skills/seo-sxo/SKILL.md) | Read SERPs backwards to find page-type mismatches. Scores the page from 4 personas; produces a wireframe for the SERP-winning page type | [bigin.com](https://github.com/seranking/seo-skills/blob/v2.11.6/examples/seo-sxo-bigin-com-20260514/SXO-REPORT.md) |

### More skills

The rest of the catalogue — every other skill the plugin ships.

| Skill | What it produces | Primary triggers |
|---|---|---|
| [`seo-competitor-gap-analysis`](skills/seo-competitor-gap-analysis/SKILL.md) | Keywords competitors rank for that the target does not, filtered by intent, volume, KD, and scored for priority | "competitor gap", "keyword gap", "organic content gap", "missing keyword opportunities" |
| [`seo-agency-landing-page`](skills/seo-agency-landing-page/SKILL.md) | Demand-gen landing page for an SEO agency with a free-audit lead magnet, grounded in real niche data | "SEO agency landing page", "lead-gen page", "free-audit landing page" |
| [`seo-page`](skills/seo-page/SKILL.md) | URL-level keyword & traffic intelligence with keep / refresh / consolidate / kill verdict for one page | "analyze this page", "page SEO performance", "what does this URL rank for", "should I refresh this page" |
| [`seo-schema`](skills/seo-schema/SKILL.md) | JSON-LD detect, validate, generate. Five bundled templates (Article / Product / LocalBusiness / FAQPage / BreadcrumbList) | "schema markup", "structured data", "JSON-LD", "rich results", "schema validation" |
| [`seo-images`](skills/seo-images/SKILL.md) | Image SEO audit for a URL or sampled domain: alt-text quality, WebP/AVIF coverage, `srcset`/`sizes`, lazy-loading + LCP signals (`loading` / `fetchpriority` / `decoding`), CLS dimensions, file naming, and `ImageObject` JSON-LD. Paste-ready `<picture>` + JSON-LD snippets | "image SEO", "image audit", "alt-text audit", "WebP coverage", "AVIF", "responsive images", "lazy loading", "CLS images", "image schema", "ImageObject" |
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
| [`seo-firecrawl`](skills/seo-firecrawl/SKILL.md) | Ad-hoc web scraping, site mapping, full-site crawling, and within-domain search via Firecrawl. Returns raw HTML, JSON-LD, og:* / twitter:* metadata, JS-rendered DOM, and screenshots that WebFetch can't *(requires the Firecrawl connector, see [Optional extensions](#optional-extensions))* | "scrape this page", "crawl this site", "map this site", "get the OG tags", "render this JS-heavy page" |
| [`seo-plan`](skills/seo-plan/SKILL.md) | Phased SEO roadmap for a domain — quarter-by-quarter, tied to competitive position, content gaps, technical debt, and AI Search readiness. Sequences specialist-skill outputs into one site-level plan with owners, metrics, and a critical path | "SEO plan", "SEO strategy", "SEO roadmap", "90-day plan", "where do we focus next" |
| [`seo-google`](skills/seo-google/SKILL.md) | Points you to the full GitHub edition for Search Console, GA4, CrUX and PageSpeed data, and offers SE Ranking data that can stand in: rankings, traffic estimates, keyword metrics and site-audit issues *(live Google data: full edition on GitHub only)* | "search console", "GSC", "PageSpeed", "CrUX", "URL inspection", "GA4 organic" |
| [`seo-api`](skills/seo-api/SKILL.md) | SE Ranking API integration architect — covers the entire 195-tool surface (Data API + Project API), forecasts credit and plan-limit cost, emits ready-to-paste cURL / Python / TypeScript / MCP-tool-call recipes, and (with explicit confirmation) wires up Project API state (projects, keywords, search engines, audits, AIRT prompts, backlink groups) | "how do I use SE Ranking API to do X", "what endpoint gives me Y", "credit cost of workflow Z", "build a rank tracker", "set up an audit", "Postman / cURL / Python / TypeScript for SE Ranking", "rate limit for X", "integrate SE Ranking with Looker / n8n / Make" |

### Social and agency workflows

These six skills combine SE Ranking data with [Planable](https://planable.io), so they need the Planable connector from the Claude directory connected as well.

| Skill | What it produces | Primary triggers |
|---|---|---|
| [`seo-gaps-to-social-campaign`](skills/seo-gaps-to-social-campaign/SKILL.md) | A ready-to-publish social campaign in Planable built from keyword gaps, competitor wins, ranking losses and question keywords | "what should we post based on our SEO data", "turn these keyword gaps into posts" |
| [`ai-search-gaps-to-social-campaign`](skills/ai-search-gaps-to-social-campaign/SKILL.md) | AI-search prompts and topics where the brand is missing or losing, turned into a Planable campaign with before/after tracking | "what should we post to get cited by AI", "improve our AI search visibility with content" |
| [`site-audit-to-social-distribution`](skills/site-audit-to-social-distribution/SKILL.md) | Weak pages and audit issues from SE Ranking, rewritten page copy for approval in Planable, and scheduled supporting posts | "audit the site and help us fix the weak pages", "fix and promote our content" |
| [`seo-ai-social-report`](skills/seo-ai-social-report/SKILL.md) | One report across SEO rankings, AI-search visibility and social engagement: a chat summary plus an interactive HTML report | "full report across SEO and social", "how did we do this month across search and social" |
| [`client-onboarding-proposal`](skills/client-onboarding-proposal/SKILL.md) | A data-backed onboarding proposal for a new agency client: SEO and AI-search audit plus current social performance | "build an onboarding proposal for [client]", "we're starting with [client]" |
| [`local-gmb-visibility`](skills/local-gmb-visibility/SKILL.md) | City-level rank tracking in SE Ranking paired with local social content and Google Business Profile posts in Planable | "track our rankings in [city]", "set up local rank tracking", "show up in local search" |

## Optional extensions

Firecrawl (raw HTML, JSON-LD, JavaScript rendering, site crawls) makes several skills more precise, and `seo-firecrawl` and `seo-images` need it. Connect the Firecrawl connector from the Claude directory if you use it. Without it, the other skills fall back to `WebFetch` and still produce a deliverable. The Google API scripts ship only with the full edition on GitHub.

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

Data and privacy: the skills send the domains, URLs and keywords you give them to SE Ranking's MCP server (see the [SE Ranking privacy policy](https://seranking.com/legal/privacy-policy.html)). If you've connected Firecrawl, the URLs to scrape go to firecrawl.dev under its own terms, and the social skills send the post drafts and page copy they write to Planable when you've connected it. The skills treat content fetched from web pages as data to analyse, never as instructions.

## Output

Every skill writes its output to a folder named `{skill-slug}-{target-slug}-{YYYYMMDD}/` (e.g., `seo-content-brief-example-com-20260427/`). The date stamp keeps re-runs non-destructive and makes it easy to diff outputs over time. Finished example runs are in the GitHub repository: https://github.com/seranking/seo-skills/tree/main/examples

## Rate limits and costs

The SE Ranking MCP server has two namespaces with different rate limits:

- **Data API** (`DATA_*`): 10 requests per second. Charges API credits per call.
- **Project API** (`PROJECT_*`): 5 requests per second. Retrieval and management calls do not charge; writes consume quota slots.

Every skill in this repo is designed to pace sequentially inside these limits. The largest skills (`seo-competitor-gap-analysis` with full keyword dumps, `seo-keyword-cluster` with 20 seeds) can consume thousands of credits on large domains. Check `DATA_getSubscription` before running on production accounts, and use the `ceiling` parameters the skills document to cap cost.

## Contributing

This repo is the official Skills catalogue for the SE Ranking MCP server. See [`CONTRIBUTING.md`](https://github.com/seranking/seo-skills/blob/v2.11.6/CONTRIBUTING.md) for the skill-authoring template, required structure, MCP tool conventions, and PR checklist.

- **Bug reports** — open an issue with the skill name, the input, and the unexpected output.
- **New skills** — PRs welcome. Use the template in `CONTRIBUTING.md`.
- **Improvements** — PRs welcome. Include a before/after example run in the PR description.

## Links

- SE Ranking: https://seranking.com
- SE Ranking API: https://seranking.com/api.html
- SE Ranking MCP: https://seranking.com/mcp.html
- SE Ranking MCP Docs: https://seranking.com/api/integrations/mcp/
- SE Ranking privacy policy (covers the data the SE Ranking MCP server processes): [seranking.com/legal/privacy-policy.html](https://seranking.com/legal/privacy-policy.html)
- Claude SEO Skills: https://seranking.com/claude-seo-skills.html
- Claude Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code Plugins: https://code.claude.com/docs/en/plugins

## License

MIT. See [LICENSE](LICENSE).
