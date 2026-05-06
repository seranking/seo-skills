---
name: seo-google
description: Direct access to Google's own SEO data via Search Console (Search Analytics, URL Inspection, Sitemaps), PageSpeed Insights v5, CrUX field data with 25-week history, Indexing API v3, GA4 organic traffic, YouTube video search, Google NLP entity/sentiment analysis, Knowledge Graph entity verification, Web Risk safety, and Google Ads Keyword Planner. Bridges crawl-based analysis (the rest of this catalogue) with Google's real-time field data — actual Chrome user metrics, real indexation status, real search performance, real organic traffic. Use when the user asks "search console", "GSC", "PageSpeed", "CrUX", "field data", "indexing API", "GA4 organic", "URL inspection", "google api setup", "real CWV data", "impressions", "clicks", "CTR", "position data", "LCP", "INP", "CLS", "FCP", "TTFB", "Lighthouse scores", "youtube SEO", "knowledge graph", "keyword planner", or "real google data".
---

# Google SEO APIs

Direct access to Google's own SEO data. Bridges the gap between crawl-based analysis (the rest of the catalogue) and Google's real-time field data: actual Chrome user metrics, real indexation status, search performance, and organic traffic.

All APIs are free. Setup requires a Google Cloud project with API key and/or service account — run the `setup` command for step-by-step instructions, or read `references/auth-setup.md` directly.

> **Adapted from [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo)'s `seo-google` skill** (MIT). Scripts, references, and command surface mirror the upstream implementation. Config path namespaced to `~/.config/seo-skills/` for clean coexistence with the original.

## Prerequisites

- **Required:** Python 3.10+ and the Google API client libraries. Install via `bash extensions/google/install.sh`.
- **Required:** at minimum a Google API key (Tier 0). For full coverage, also a Google Cloud service account (Tier 1+) and optionally a GA4 property ID (Tier 2) and Google Ads developer token (Tier 3).
- Config file: `~/.config/seo-skills/google-api.json`.

Before executing any command, check credentials:

```bash
python scripts/google_auth.py --check --json
```

Config file shape (`~/.config/seo-skills/google-api.json`):

```json
{
  "service_account_path": "/path/to/service_account.json",
  "api_key": "AIzaSy...",
  "default_property": "sc-domain:example.com",
  "ga4_property_id": "properties/123456789"
}
```

If missing, read `references/auth-setup.md` and walk the user through setup.

### Credential Tiers

| Tier | Detection | Available Commands |
|------|-----------|-------------------|
| **0** (API Key) | `api_key` present | `pagespeed`, `crux`, `crux-history`, `youtube`, `nlp`, `entity`, `safety` |
| **1** (OAuth/SA) | + OAuth token or service account | Tier 0 + `gsc`, `inspect`, `sitemaps`, `index` |
| **2** (Full) | + `ga4_property_id` configured | Tier 1 + `ga4`, `ga4-pages`, `ga4-referrals`, `ga4-channel-mix`, `ga4-properties` |
| **3** (Ads) | + `ads_developer_token` + `ads_customer_id` | Tier 2 + `keywords`, `volume` |

Always communicate the detected tier before running commands.

## Quick Reference

| Command | What it does | Tier |
|---------|-------------|------|
| `setup` | Check/configure API credentials | -- |
| `pagespeed <url>` | PSI Lighthouse + CrUX field data | 0 |
| `crux <url>` | CrUX field data only (p75 metrics) | 0 |
| `crux-history <url>` | 25-week CWV trend analysis | 0 |
| `gsc <property>` | Search Console: clicks, impressions, CTR, position | 1 |
| `inspect <url>` | URL Inspection: index status, canonical, crawl info | 1 |
| `inspect-batch <file>` | Batch URL Inspection from file | 1 |
| `sitemaps <property>` | GSC sitemap status | 1 |
| `index <url>` | Submit URL to Indexing API | 1 |
| `index-batch <file>` | Batch submit up to 200 URLs | 1 |
| `ga4 [property-id]` | GA4 organic traffic report | 2 |
| `ga4-pages [property-id]` | Top organic landing pages | 2 |
| `ga4-referrals [property-id]` | Referral sessions by source — AI assistants by default | 2 |
| `ga4-channel-mix [property-id]` | Sessions split by channel group (Direct / Organic / Referral / Paid …) | 2 |
| `ga4-properties` | List every GA4 account + property the service account can read | 2 |
| `youtube <query>` | YouTube video search (views, likes, duration) | 0 |
| `youtube-video <id>` | YouTube video details + top comments | 0 |
| `nlp <url-or-text>` | NLP entity extraction + sentiment + classification | 0 |
| `entities <url-or-text>` | Entity analysis only (for E-E-A-T) | 0 |
| `keywords <seed>` | Keyword ideas from Google Ads Keyword Planner | 3 |
| `volume <keywords>` | Search volume lookup from Keyword Planner | 3 |
| `entity <query>` | Knowledge Graph entity check | 0 |
| `safety <url>` | Web Risk URL safety check | 0 |
| `quotas` | Show rate limits for all APIs | -- |
| `report <type>` | Generate a PDF/HTML/XLSX report from collected JSON | -- |

---

## PageSpeed + CrUX

### `pagespeed <url>`

Combined Lighthouse lab data + CrUX field data.

**Script:** `python scripts/pagespeed_check.py <url> --json`
**Reference:** `references/pagespeed-crux-api.md`
**Default:** Both mobile + desktop strategies, all Lighthouse categories.

Output merges lab scores (point-in-time Lighthouse) with field data (28-day Chrome user metrics). CrUX tries URL-level first, falls back to origin-level.

### `crux <url>`

CrUX field data only (no Lighthouse run). Faster.

**Script:** `python scripts/pagespeed_check.py <url> --crux-only --json`

### `crux-history <url>`

25-week CrUX History trends. Shows whether CWV metrics are improving, stable, or degrading.

**Script:** `python scripts/crux_history.py <url> --json`
**Reference:** `references/pagespeed-crux-api.md`

Output includes per-metric trend direction, percentage change, and weekly p75 values.

---

## Search Console

### `gsc <property>`

Search Analytics: clicks, impressions, CTR, position for last 28 days.

**Script:** `python scripts/gsc_query.py --property <property> --json`
**Reference:** `references/search-console-api.md`
**Default:** 28 days, dimensions=query,page, type=web, limit=1000.

Includes quick-win detection: queries at position 4-10 with high impressions.

**Filtering:** `--device {desktop,mobile,tablet}`, `--country <ISO3>`, `--page <url-or-substring>` (defaults to `contains` match; pass `--page-match equals` for exact-URL match). Combine for per-URL query analysis: `--page /blog/best-ai-seo-tools/ --dimensions query`.

**AI Overview / AI Mode:** `--ai-overview` (or `--ai-mode`) filters results to queries where Google rendered an AI Overview / AI Mode SERP that included one of your URLs. This is Google's first-party answer to *"are we cited in AI Overview?"* — clicks, impressions, CTR, and avg position straight from GSC. Combine with `--dimensions query,page` to see which queries+pages earned AI Overview presence, or with `--page /post/` to scope to one URL. For other appearance types (`RICH_RESULT`, `REVIEW_SNIPPET`, etc.) use `--search-appearance <value>`.

### `inspect <url>`

URL Inspection: real indexation status from Google.

**Script:** `python scripts/gsc_inspect.py <url> --json`

Returns: verdict (PASS/FAIL), coverage state, robots.txt status, indexing state, page fetch state, canonical selection, mobile usability, rich results.

### `inspect-batch <file>`

Batch inspection from a file (one URL per line). Rate limited to 2,000/day per site.

**Script:** `python scripts/gsc_inspect.py --batch <file> --json`

### `sitemaps <property>`

List submitted sitemaps with status, errors, warnings.

**Script:** `python scripts/gsc_query.py sitemaps --property <property> --json`

---

## Indexing API

### `index <url>`

Notify Google of a URL update.

**Script:** `python scripts/indexing_notify.py <url> --json`
**Reference:** `references/indexing-api.md`

The Indexing API is officially for JobPosting and BroadcastEvent/VideoObject pages. Always inform the user of this restriction. Daily quota: 200 publish requests.

### `index-batch <file>`

Batch submit URLs from a file. Tracks quota usage.

**Script:** `python scripts/indexing_notify.py --batch <file> --json`

---

## GA4 Traffic

All GA4 reports accept an optional `--page <path-or-url>` flag to scope the report to a single landing page (EXACT match against GA4's `landingPage` dimension; full URLs are auto-stripped to path). Use it whenever the question is "how is *this* post performing?" rather than site-wide.

`--report organic` and `--report top-pages` accept `--channel <name|all>`: defaults to `organic` (Organic Search), pass `all` to drop the channel filter (required for whole-page weekly trends across all traffic sources), or any GA4 default channel group verbatim — `Direct`, `Referral`, `Paid Search`, `Organic Social`, etc.

### `ga4 [property-id]`

Daily-time-series traffic report: sessions, users, pageviews, bounce rate, engagement.

**Script:** `python scripts/ga4_report.py --property <id> --json`
**Reference:** `references/ga4-data-api.md`
**Default:** 28 days, filtered to Organic Search channel group. Pass `--channel all` for unfiltered traffic.

The all-channels variant is what answers "how is this post growing week over week?" when most of the traffic is Direct or Referral rather than Organic — the canonical case for AI-cited content. Example: `--report organic --page /blog/best-ai-seo-tools/ --channel all --days 99`.

### `ga4-pages [property-id]`

Top landing pages ranked by sessions for the chosen channel (default Organic Search; use `--channel all` for site-wide top pages across every source).

**Script:** `python scripts/ga4_report.py --property <id> --report top-pages --json`

### `ga4-referrals [property-id]`

Referral sessions broken down by `sessionSource`. Defaults to a curated AI-assistant
hostname list — OpenAI (chatgpt.com, chat.openai.com), Anthropic (claude.ai), Google
(gemini.google.com, bard.google.com), Microsoft (copilot.microsoft.com), Perplexity
(perplexity.ai), Alibaba/Qwen (chat.qwen.ai, qwen.com, tongyi.aliyun.com), Mistral
(chat.mistral.ai), DeepSeek (chat.deepseek.com), xAI/Grok (grok.com, x.ai), plus
you.com / phind.com / poe.com — so the "how much traffic do AI assistants actually
send us?" question is one command. Use this as a reality check against AI-visibility
data from `seo-ai-search-share-of-voice` and `seo-geo` — referral volume measures
users sharing your links in AI chats, not whether the AI proactively cites you.

**Script:** `python scripts/ga4_report.py --property <id> --report referrals --json`

**Source modes (`--sources`):**
- `ai` (default) — curated AI-assistant hostname list
- `all` — every source in the Referral channel group
- `chatgpt.com,perplexity.ai,...` — explicit comma-separated list

Combine with `--page` to answer "how much AI traffic did THIS specific post get?":
`--report referrals --page /blog/best-ai-seo-tools/`.

### `ga4-channel-mix [property-id]`

Sessions broken down by `sessionDefaultChannelGroup` (Direct / Organic Search / Referral / Paid Search / Organic Social / …). No channel filter — this is the diagnostic view for "where does traffic to this page actually come from?". Each row includes a `share_of_sessions` percentage so the mix is visible at a glance.

**Script:** `python scripts/ga4_report.py --property <id> --report channel-mix --json`

This is the report that answers questions like *"is this post mostly winning on organic, or is the traffic coming from somewhere else?"*. AI-assistant traffic frequently lands in `Direct` (uncredited) rather than `Referral`, so a high Direct share on a recent content-heavy page is itself an AI-visibility signal — pair with `ga4-referrals` for a fuller picture.

Per-page diagnosis: `--report channel-mix --page /blog/best-ai-seo-tools/ --days 90`.

### `ga4-properties`

Enumerates every GA4 account and property the service account can read. Use this
*before* running `ga4` / `ga4-pages` / `ga4-referrals` / `ga4-channel-mix` when the
client has multiple GA4 properties (typical: separate marketing-site and app
properties, or per-region properties) and you need to know which property_id to
query. Output groups properties by parent account; the `property_id` field is the
numeric value to pass as `--property`.

**Script:** `python scripts/ga4_admin.py properties --json`

Requires the **Google Analytics Admin API** to be enabled in your Cloud project
(separate from the Data API) and the service account to have Viewer access on at
least one property.

---

## YouTube (Video SEO)

YouTube mentions have the strongest AI visibility correlation (0.737). Free, API key only.

### `youtube <query>`

Search YouTube for videos. Returns title, channel, views, likes, duration.

**Script:** `python scripts/youtube_search.py search "<query>" --json`
**Reference:** `references/youtube-api.md`
**Quota:** 100 units per search (10,000 units/day free).

### `youtube-video <video_id>`

Detailed video info + tags + top 10 comments.

**Script:** `python scripts/youtube_search.py video <video_id> --json`
**Quota:** 2 units (video details + comments).

---

## NLP Content Analysis

Google's own entity/sentiment analysis. Enhances E-E-A-T scoring.

### `nlp <url-or-text>`

Full NLP analysis: entities, sentiment, content classification.

**Script:** `python scripts/nlp_analyze.py --url <url> --json` or `--text "..."`
**Reference:** `references/nlp-api.md`
**Free tier:** 5,000 units/month. Requires billing enabled on GCP project.

### `entities <url-or-text>`

Entity extraction only (faster, less quota).

**Script:** `python scripts/nlp_analyze.py --url <url> --features entities --json`

---

## Keyword Research (Google Ads)

Gold-standard keyword volume data. Requires Google Ads account.

### `keywords <seed>`

Generate keyword ideas from seed terms.

**Script:** `python scripts/keyword_planner.py ideas "<seed>" --json`
**Reference:** `references/keyword-planner-api.md`
**Requires:** Ads developer token + customer ID in config (Tier 3).

### `volume <keywords>`

Search volume for specific keywords (comma-separated).

**Script:** `python scripts/keyword_planner.py volume "<kw1>,<kw2>" --json`

---

## Supplementary

### `entity <query>`

Knowledge Graph entity check. Verifies brand presence.

**Reference:** `references/supplementary-apis.md`
Uses Knowledge Graph Search API with API key.

### `safety <url>`

Web Risk API check for malware/social engineering flags.

**Reference:** `references/supplementary-apis.md`

### `quotas`

Display rate limits table. Read `references/rate-limits-quotas.md`.

---

## Reports

After any analysis command, offer to generate a PDF/HTML/XLSX report.

### `report <type>`

Generate a professional PDF/HTML/XLSX report with charts and analytics.

**Script:** `python scripts/google_report.py --type <type> --data <json> --domain <domain> --format pdf`

| Type | Input | Output |
|------|-------|--------|
| `cwv-audit` | PSI + CrUX + CrUX History data | Core Web Vitals audit with gauges, timelines, distributions |
| `gsc-performance` | GSC query data | Search Console report with query tables, quick wins |
| `indexation` | Batch inspection data | Indexation status with coverage donut chart |
| `full` | All data combined | Comprehensive Google SEO report (all sections) |

**Workflow:**
1. Run data collection commands (`pagespeed`, `gsc`, `inspect-batch`, etc.)
2. Save JSON output to file: `python scripts/pagespeed_check.py <url> --json > data.json`
3. Generate report: `python scripts/google_report.py --type cwv-audit --data data.json --domain <domain>`

**Convention:** After completing analysis, suggest: "Generate a report? Use `report <type>`."

---

## Rate Limits

| API | Per-Minute | Per-Day | Auth |
|-----|-----------|---------|------|
| PSI v5 | 240 QPM | 25,000 QPD | API Key |
| CrUX + History | 150 QPM (shared) | Unlimited | API Key |
| GSC Search Analytics | 1,200 QPM/site | 30M QPD | Service Account |
| GSC URL Inspection | 600 QPM | 2,000 QPD/site | Service Account |
| Indexing API | 380 RPM | 200 publish/day | Service Account |
| GA4 Data API | 10 concurrent | ~25K tokens/day | Service Account |

## Cross-Skill Integration

- **`seo-technical-audit`** — uses `pagespeed_check.py` for real CWV field data; uses `inspect` to confirm indexation status flagged by SE Ranking's audit.
- **`seo-page`** — replaces estimated traffic with real GSC `query,page` data via `gsc`; confirms indexation via `inspect`.
- **`seo-drift`** — adds `crux-history` (25-week trend) and GSC delta tracking to baseline/compare snapshots.
- **`seo-sitemap`** — `sitemaps` command shows which sitemaps Google has actually consumed and their error/warning counts (vs SE Ranking's audit which only crawls).
- **`seo-content-audit`** — `nlp` enhances E-E-A-T entity/sentiment scoring on the page being audited; `gsc` confirms whether the page is earning impressions for its target keywords.
- **`seo-geo`** — `gsc --ai-overview --page <url>` answers "did this URL appear in AI Overview, and what did it earn?" with Google's own data, complementing the SE Ranking AIO citation pull. Pair `gsc --ai-overview --dimensions query,page` with the GEO recommendations to confirm wins/losses URL-by-URL.
- **`seo-ai-search-share-of-voice`** — pair `ga4-referrals` (downstream traffic from chatgpt.com/perplexity.ai/gemini.google.com etc.) with the SoV pull (upstream citation/brand mention presence) for a complete AI-visibility picture: SoV measures whether LLMs cite you, GA4 referrals measure whether their users actually click through.
- **`seo-keyword-cluster`** / **`seo-keyword-niche`** — `volume` (Tier 3) replaces SE Ranking volume with Google Ads gold-standard volumes when available.
- **`seo-plan`** — when GSC + GA4 are configured, the "Where you are" baseline uses real impressions/clicks/conversions instead of SE Ranking estimates.

## Output Format

- CWV metrics: traffic-light rating (Good / Needs Improvement / Poor)
- Performance reports: tables with sortable columns
- Always include data freshness note
- Save reports as `GOOGLE-API-REPORT-{domain}.md`
- Use templates from `assets/templates/` for structured output

## Technical Notes

- INP replaced FID on March 12, 2024. Never reference FID.
- CLS values from CrUX are string-encoded (e.g., "0.05"). Scripts handle parsing.
- CrUX 404 = insufficient traffic, not an auth error.
- Search Analytics data has a 2-3 day lag.
- `round_trip_time` replaced `effectiveConnectionType` in CrUX (Feb 2025).
- Custom Search JSON API is closed to new customers (2025).

## Error Handling

| Scenario | Action |
|----------|--------|
| No credentials configured | Run `setup`. List Tier 0 commands that work with just an API key. |
| Service account lacks GSC access | Report error. Instruct: add `client_email` to GSC > Settings > Users > Add. |
| CrUX data unavailable (404) | Report insufficient Chrome traffic. Suggest PSI lab data as fallback. |
| GA4 property not found | Report error. Show how to find property ID in GA4 Admin > Property Details. |
| Indexing API quota exceeded | Report 200/day limit. Suggest prioritizing most important URLs. |
| Rate limit (429) | Wait and retry with exponential backoff. Report which API hit the limit. |
