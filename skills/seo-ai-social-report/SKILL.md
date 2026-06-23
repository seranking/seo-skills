---
name: seo-ai-social-report
description: >
  Generate one unified performance report that brings together SEO rankings, AI-search visibility
  (SE Ranking) and social engagement (Planable) — delivered as a short text summary in chat plus a
  self-contained interactive HTML report. Use this skill whenever the user wants a combined cross-channel
  report, or says things like "give me a full report across SEO and social", "how did we do this month
  across search and social", "combined SEO + AI + social report for [client]", "build a cross-channel
  dashboard", or "one report that covers rankings, AI visibility and social". Always activate when the
  request spans both search (SE Ranking) and social (Planable) in a single report.
---

# Unified SEO + AI + social report

Most reporting forces clients to read three tools separately. This produces one view: search rankings and AI-search visibility from SE Ranking, social engagement from Planable, with quick text conclusions for the inbox and an interactive HTML report for the detail.

## Prerequisites

- **SE Ranking MCP** connected (a project gives the cleanest ranking trend; Data API history works without one).
- **Planable MCP** connected, with the workspace and connected pages.
- The user provides: domain + brand, market/country (default `us`), the Planable workspace, the reporting period (default: previous calendar month), and optionally competitors for share-of-voice.

## Connector health check

Before doing anything else, verify both MCPs are reachable:

- **SE Ranking:** call `DATA_getSubscription`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The SE Ranking connector isn't responding — please reconnect it before we continue. Setup guide: https://seranking.com/api/integrations/mcp/"
- **Planable:** call `list_workspaces`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The Planable connector isn't responding — please reconnect it before we continue. Setup guide: https://help.planable.io/hc/en-us/articles/27538577098780-How-to-connect-Planable-MCP-to-your-AI-tools"

Only continue to the process steps below once both calls return a successful response.

## Process

### 1. Scope
Confirm domain, Planable workspace, period, and competitors. Resolve the period to explicit start/end dates.

### 2. Pull SEO (SE Ranking)
- **With a project:** `PROJECT_getSummary` and `PROJECT_getPositionHistory(site_id, type: avg_pos | visibility, date_from, date_to)` for the ranking trend; optionally reuse a finished audit (`PROJECT_listAudits` → `getAuditReport`) for a site-health number.
- **Without a project:** `DATA_getDomainOverviewWorldwide` for the snapshot.
- **Shortcut:** the AI overview call in step 3 (time-series view) already returns monthly `organic_traffic` / `overall_traffic` streams for the chosen country — you can reuse those for the organic-trend chart instead of a separate history call.

### 3. Pull AI search (SE Ranking)
- `DATA_getAiSearchOverview(target, source, brand?)` with the default time-series view — brand presence, link presence, AI opportunity traffic, average position, plus monthly trend streams (including organic/overall traffic). If `previous` is `null`, treat it as a baseline — don't render the `change_percent` of 100 as growth.
- `DATA_getAiSearchLeaderboard(primary, competitors[], source, engines[])` — share of voice vs competitors (only if competitors were provided). Query it narrowly (few engines/competitors per call) — it can time out on large requests.

### 4. Pull social (Planable)
- `list_pages(workspaceId)` → page IDs.
- `get_page_metrics_summary(workspaceId, pageIds, startDate, endDate)` — **account-level** audience/impressions/engagement-rate.
- `get_post_metrics_summary(workspaceId, pageIds, startDate, endDate)` — **published-post** totals in the window. (Different scope from page impressions — keep them separate.)
- `get_post_metrics(workspaceId, pageIds, ..., limit: 5)` — top posts.
- `list_posts(...)` — posts published in the period (volume/cadence).
- For a monthly social trend, call `get_page_metrics_summary` once per month bucket.

### 5. Write the quick conclusions (chat)
A ~10–15 line plain-text summary: the headline move in each of the three areas (SEO, AI search, social), then 2–3 specific callouts ("what moved", "what to watch"). This is the part most people actually read — make it sharp and number-led, no filler.

### 6. Build the interactive HTML report
Use the bundled template at `assets/report-template.html` as the starting point — it has the Planable colour palette, the card/section layout, and Chart.js (CDN) wired up, including a **dual-axis** trend chart. Populate it with the **real data** you pulled:

- **KPI cards:** organic traffic, AI presence / share of voice, social impressions, engagement rate, posts — each with a real period-over-period change where you have one (leave the delta blank otherwise; never invent it).
- **Trend charts (interactive):** ranking/organic trend, AI presence trend, social impressions & engagement. **When two series have very different scales** (e.g. organic traffic in the thousands vs AI opportunity traffic in the hundreds, or impressions vs engagement), plot them on a **dual axis** or in separate charts — don't squash them onto one axis or the smaller line flatlines.
- **Share of voice:** a bar chart of brand vs competitors (omit if no competitors).
- **Top posts** and **What moved / What to watch** — same callouts as the text summary.

Inline the data as JavaScript arrays in the file (no external data files, no `localStorage`). Save to the outputs folder as `{client}-{period}-cross-channel-report.html`, then share it with `present_files`. Validate the inline script parses (a quick `node --check`-style pass) before presenting.

## Output

1. **Quick conclusions** — short text summary in chat (the numbers + 2–3 callouts).
2. **Interactive HTML report** — self-contained file, presented via `present_files`, with KPI cards, hoverable trend charts, share-of-voice, and top posts.

## Tips

- Keep the chat summary tight; the HTML is the detailed artefact. Don't duplicate the full report in chat.
- Label data sources in the report footer (SE Ranking for search/AI, Planable for social) and stamp the generation date and exact date range.
- Round for readability (48K, 4.2%); never fabricate a trend. If a series has one data point, show the point and skip the trend line.
- Mark partial periods (e.g. a month-to-date bucket) clearly so a short bar isn't read as a drop.

## Edge cases & limits

- **No GA4 / no Looker Studio.** This report covers what the two MCPs return — search/AI visibility and social engagement, not cross-channel conversion attribution. State this in the footer.
- **Limited page-level social analytics:** Twitter/X, Pinterest, Threads and Google Business Profile typically don't return page-level metrics via the connector — they appear in `unsupportedPages`; base totals on supported channels and note the rest as "data not available".
- **Thin periods:** if little was published or rankings barely moved, say so plainly rather than dramatising noise.
- **No competitors provided:** skip the share-of-voice section instead of leaving an empty chart.
