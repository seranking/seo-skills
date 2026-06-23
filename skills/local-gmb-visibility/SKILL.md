---
name: local-gmb-visibility
description: >
  Build and track local search visibility with SE Ranking city-level rank tracking and turn it into
  local social content in Planable, including Google Business Profile posts. Use this skill whenever the
  user wants to grow a business's presence in a specific city or cities and pair it with local social,
  or says things like "track our rankings in [city]", "set up local rank tracking", "we want to show up
  in local search", "create Google Business Profile posts", "local SEO plus social for our locations", or
  "how are we ranking city by city and what should we post locally". Always activate for local/multi-location
  visibility work that combines SE Ranking rankings with Planable local/GMB content.
---

# Local + Google Business Profile visibility

Pair SE Ranking's city-level rank tracking with Planable's local content — including Google Business Profile posts — so a business can see how it ranks in each target city and publish location-relevant content against it.

> **Scope note.** This skill covers **city-level keyword rank tracking** (SE Ranking projects with geo-targeted search engines) and **local social/GMB content** (Planable). SE Ranking's dedicated **Local Marketing** module — listings management, review monitoring, and the local rank grid/heatmap — is **not** exposed through the MCP, so those aren't part of this workflow. Set expectations accordingly.

## Prerequisites

- **SE Ranking MCP** connected, with permission to create/use a project (rank tracking is project-based).
- **Planable MCP** connected. Before planning GMB posts, confirm a connected **Google Business Profile** page exists: call `list_pages` and look for a page with `type: "googleMyBusiness"`. If there isn't one, tell the user GMB isn't connected and fall back to other local social pages.
- The user provides: business domain, the target city/cities, the core local keywords (e.g. "emergency plumber [city]"), and the Planable workspace.

## Connector health check

Before doing anything else, verify both MCPs are reachable:

- **SE Ranking:** call `DATA_getSubscription`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The SE Ranking connector isn't responding — please reconnect it before we continue. Setup guide: https://seranking.com/api/integrations/mcp/"
- **Planable:** call `list_workspaces`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The Planable connector isn't responding — please reconnect it before we continue. Setup guide: https://help.planable.io/hc/en-us/articles/27538577098780-How-to-connect-Planable-MCP-to-your-AI-tools"

Only continue to the process steps below once both calls return a successful response.

## Process

### 1. Scope the locations and terms
Confirm the cities, the local keywords per city, the business domain, and the Planable workspace + which pages (GMB and/or social). For multi-location, list each location explicitly. **Rank tracking consumes plan quota** (keywords × search engines) and search engines persist in the project — confirm scope before creating many, and offer to remove test engines afterwards.

### 2. Set up city-level rank tracking in SE Ranking
- Create or reuse a project: `PROJECT_createProject(url, title)` → `site_id` (or reuse an existing project's `site_id`).
- For each city, resolve the exact geo-target: `PROJECT_getAvailableRegions(search: "<City, State, Country>")` and take the canonical `name` string verbatim (abbreviated forms are rejected). A specific query returns one clean match.
- Add a geo-targeted search engine per city: `PROJECT_addSearchEngine(site_id, country_code, region_name, lang_code?)` → returns `site_engine_id`. (The catalogue in `PROJECT_getAvailableSearchEngines` is only needed for niche regional engines.)
- Add the local keywords: `PROJECT_addKeywords(site_id, keywords[])`, attaching each to the right city engine via `site_engine_ids`.
- Trigger a check (`PROJECT_runPositionCheck`) or let the project's schedule run. **Results are not instant** — a check is asynchronous and city rankings populate on the next cycle, so don't expect `getPositionHistory` to return data immediately after setup.

### 3. Read local performance
- `PROJECT_getPositionHistory(site_id, type, site_engine_id?, date_from, date_to)` — rankings over time, filterable to a single city engine. Use `avg_pos` and `visibility`.
- `PROJECT_addCompetitor` + `PROJECT_getCompetitorPositions(competitor_id)` — how local competitors rank for the same terms.
- For a live local SERP / local-pack read, `DATA_getSerpLocations` (to find the `location_id`) → `DATA_getSerpResults(location_id=...)`. **Heads-up: `getSerpLocations` can return a very large payload** (hundreds of thousands of characters for a broad query). Pass a specific `q` (e.g. "Brooklyn" or "New York, NY"), and if the result is still huge it's written to a file — extract the one matching `location_id` with `jq` rather than loading the whole thing. For tracking setup you usually only need `getAvailableRegions`, so reserve `getSerpLocations` for when a live SERP read is essential.
- `DATA_getDomainKeywordsComparison` — local keyword gaps vs competitors.

### 4. Build the local content plan
Translate the rankings + gaps into location-relevant content: service-area posts, local proof and reviews-style content (written as posts, since review data isn't pulled here), neighbourhood/landmark references, local offers, and answers to local intent. Tailor copy per city — generic content underperforms locally.

### 5. Create the content in Planable
- **Google Business Profile posts:** if a `googleMyBusiness` page exists, `create_post(workspaceId, gmbPageId, text, scheduledAt?)` on it.
- **Local social posts:** `create_post` per page, or `create_grouped_post` for synced copy. For multi-location, use a label per city (via `list_labels` / `create_label`) so each location's content is easy to filter.
- **Scheduling — ask before creating.** Don't guess dates or leave everything undated by default. Ask how the user wants the batch dated and offer: **spread evenly** across a window (e.g. the next 7 days, one post per slot at a sensible hour), a **fixed cadence/interval** (e.g. every weekday at 10:00, laid out from a start date they give), **manual** dates per post, or **no dates yet** (undated drafts to place on the calendar later). Convert each chosen time to ISO 8601 and pass it as `scheduledAt`. Keep posts as **proposed drafts** — don't set `publishAtScheduledDate` — so nothing auto-publishes; only set it `true` if the user explicitly wants auto-publishing. Scheduled times are treated as **UTC**, so confirm the timezone or state that times are UTC.

### 6. Track and iterate
Re-read `PROJECT_getPositionHistory` per city on the next check cycle to see movement, and adjust the content plan toward the cities/terms with the most headroom.

## Content pointers: writing for keywords & AI visibility gaps

Keep these in mind when creating local social and Google Business Profile content meant to target a specific keyword or close an AI-visibility gap:

- **Target one intent per post.** Pick a single keyword or question and answer that one thing clearly. Posts that try to cover everything rank and get cited for nothing.
- **Lead with the answer.** Put the takeaway in the first line, then support it. Skimmers and AI engines both extract the clearest, most self-contained statement — don't bury it.
- **Write the way people actually ask.** Phrase hooks, captions, and headers as real questions and plain-language answers. AI prompts are conversational, so natural phrasing beats keyword-stuffing.
- **Make claims quotable on their own.** AI tools lift snippets out of context, so each key sentence should stand alone — one idea, declarative, no "as mentioned above."
- **Be specific.** Numbers, concrete examples, named steps, clear definitions. Specificity is what gets cited and what sets you apart from generic content competitors already own.
- **Fill the gap, don't echo it.** If a competitor already owns a topic, find the sub-question or angle they're missing instead of repeating what's already ranking.
- **Stay consistent across surfaces.** Use the same terms and claims on social, your site, and your profiles so AI builds one coherent picture of what your brand is the answer for.
- **Keep it human.** It still has to read like a good post — optimizing for keywords or AI shouldn't make the writing robotic.

## Output

1. **Local rank-tracking setup** — the project, the per-city geo-targets (with `site_engine_id`s), and the keywords being tracked.
2. **City-by-city ranking snapshot** (once checks have run) with competitor context.
3. **Local content drafts** — GMB posts and local social posts in Planable, ideally labelled by city.
4. **Iteration notes** — which cities/terms to prioritise next.

## Tips

- Use the exact region name from `PROJECT_getAvailableRegions` — abbreviations fail.
- City-level rankings populate on the project's **check cycle**, not instantly. If the user needs an immediate read, use `PROJECT_runPositionCheck` and/or a narrow live `DATA_getSerpResults` localized view, and explain the difference.
- Localise copy genuinely (neighbourhoods, local events, real service areas). Recycled national copy is the most common local-content failure.

## Edge cases & limits

- **Local Marketing module not available via MCP:** no listings management, review monitoring, or local rank grid/heatmap. City-level keyword rank tracking is the substitute for "local ranking performance".
- **GMB analytics gap:** Planable's connector does not return performance metrics for Google Business Profile pages, so local social *results* can't be fully reported through these MCPs — note this when setting up tracking.
- **No GMB page connected:** if `list_pages` shows no `googleMyBusiness` page, you can't post to GMB via the connector — say so and use other local pages.
- **Rank tracking is project-based and consumes plan limits** (keywords × search engines). Multi-location setups multiply quickly — confirm scope before creating many city engines, and offer cleanup (`PROJECT_deleteSearchEngine` / `PROJECT_deleteKeywords`) for throwaway test setups.
- Posts are created as drafts; publishing happens in Planable after approval.
