---
name: ai-search-gaps-to-social-campaign
description: >
  Find the AI-search prompts and topics where a brand is invisible (or losing to competitors) in
  SE Ranking, then turn those gaps into a social campaign in Planable and set up before/after tracking.
  Use this skill whenever the user wants to improve how their brand shows up in AI answers (ChatGPT,
  Perplexity, Gemini, Google AI Overview, AI Mode) through content, or says things like "what should we
  post to get cited by AI", "where are competitors winning in AI answers and we're not", "create content
  for the prompts we're missing", "improve our AI visibility with social", "AEO/GEO content plan", or
  "turn our AI search gaps into posts". Always activate when AI-search visibility is the goal and Planable
  is where the content will be made.
---

# AI-search gaps → social campaign

Use SE Ranking's AI Search data to see which prompts and narratives a brand owns, which competitors own, and which are wide open — then build social content in Planable that stakes a claim in the missing narratives, and instrument it so impact is measurable.

> **Scope note (read this).** SE Ranking's AI Search MCP tools expose brand presence, link presence, share of voice, and the prompts behind them. They do **not** expose sentiment scoring. Do not report or imply sentiment from these tools. Social content is one lever on AI visibility — LLM citation is also driven by website content and authority, which is outside what these two MCPs publish.

## Prerequisites

- **SE Ranking MCP** connected (AI Search Data API; optionally a project for the AI Result Tracker, which enables ongoing prompt tracking).
- **Planable MCP** connected, with the destination workspace and pages.
- The user provides: target domain + brand name, country (default `us`), competitor domains + brand names (up to 10), and optionally which engines to focus on (default: all of `ai-overview`, `ai-mode`, `chatgpt`, `perplexity`, `gemini`).

## Connector health check

Before doing anything else, verify both MCPs are reachable:

- **SE Ranking:** call `DATA_getSubscription`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The SE Ranking connector isn't responding — please reconnect it before we continue. Setup guide: https://seranking.com/api/integrations/mcp/"
- **Planable:** call `list_workspaces`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The Planable connector isn't responding — please reconnect it before we continue. Setup guide: https://help.planable.io/hc/en-us/articles/27538577098780-How-to-connect-Planable-MCP-to-your-AI-tools"

Only continue to the process steps below once both calls return a successful response.

## Process

### 1. Resolve the brand and scope
If the user gives a domain but not the exact brand string, call `DATA_getAiSearchBrand(target, source)` to get the name SE Ranking attributes to it. Do the same for each competitor. Confirm the Planable workspace and target platforms.

### 2. Baseline AI visibility
- `DATA_getAiSearchOverview(target, source, brand?)` — capture brand_presence, link_presence, ai_opportunity_traffic, and average_position. **Read `previous` before quoting change:** if it's `null`, this is the first snapshot — report the current values as a baseline and do **not** present the `change_percent` of 100 as real growth.
- `DATA_getAiSearchLeaderboard(primary{target,brand}, competitors[{target,brand}], source, engines[])` — share of voice for the brand vs competitors, per engine. Build a quick heatmap (rows = brands, columns = engines).
  - **This endpoint is heavy and can return a 504 timeout** when you pass many competitors × many engines at once. Query **one engine at a time** (or keep it to ≤3 competitors per call), and retry once on timeout. If it still fails, fall back to calling `DATA_getAiSearchOverview` for each competitor and compare brand_presence / link_presence yourself.

### 3. Find the prompt gaps
For the target and each competitor, pull the prompts behind the presence:

- `DATA_getAiSearchPromptsByBrand(brand, engine, source)` — prompts mentioning the brand by name.
- `DATA_getAiSearchPromptsByTarget(target, engine, source)` — prompts where the domain is cited as a source.

Compare: cluster prompts by topic, then mark each cluster as **owned** (target appears), **contested** (target + competitors), or **missing** (competitors appear, target doesn't). The missing and contested clusters are the campaign targets.

- **AI prompts almost always have `volume: 0`** — they're conversational queries, not search keywords. That is expected and is **not** a signal of low value. Judge a cluster by topical relevance and by *which brands the LLM cites*, never by search volume.
- **Validate brand-name matches.** A brand can surface in loosely related answers ("best year planner", a person's name, etc.). Read the answer text and flag ambiguous matches rather than counting them as real presence.
- Note *where* the target sits when it does appear (e.g. cited 4th of 6 in "best X" answers) — moving up within contested prompts is as valuable as entering missing ones.

### 4. Turn gaps into content hypotheses
For each target cluster, write a hypothesis: *"If we publish clear, citable content asserting [brand] in [narrative], we should start appearing for prompts like [examples]."* Translate each into social angles that make the brand's position explicit and quotable — definitions, head-to-head comparisons, "X vs Y", myth-busting, FAQ-style answers. LLMs favour clear, structured, attributable claims, so write social copy that states the position plainly rather than burying it.

Present the clusters and hypotheses to the user before drafting.

### 5. Draft and create in Planable
Write platform-appropriate copy, then create drafts: `create_post` per page (per-platform copy) or `create_grouped_post` for synced content. Tag the batch with a label (via `list_labels` / `create_label`, e.g. "AI-visibility") so the campaign is easy to isolate when measuring. 

**Scheduling — ask before creating.** Don't guess dates or leave everything undated by default. Ask how the user wants the batch dated and offer: **spread evenly** across a window (e.g. the next 7 days, one post per slot at a sensible hour), a **fixed cadence/interval** (e.g. every weekday at 10:00, laid out from a start date they give), **manual** dates per post, or **no dates yet** (undated drafts to place on the calendar later). Convert each chosen time to ISO 8601 and pass it as `scheduledAt`. Keep posts as **proposed drafts** — don't set `publishAtScheduledDate` — so nothing auto-publishes; only set it `true` if the user explicitly wants auto-publishing. Scheduled times are treated as **UTC**, so confirm the timezone or state that times are UTC.

### 6. Instrument before/after measurement
This is what makes the loop real:

- **Ongoing AI tracking (if a project exists):** create an AI Result Tracker engine with `PROJECT_createLlmEngine`, add the target prompts with `PROJECT_addPrompts(site_id, llm_id, prompts[])`, then read movement later with `PROJECT_getPromptsRankings` and `PROJECT_getLlmStatistics`. Because this writes to the user's live project (and consumes plan limits), confirm before creating engines/prompts.
- **Periodic re-checks:** re-run `DATA_getAiSearchOverview` and `DATA_getAiSearchLeaderboard` after the campaign has run and diff against the baseline from step 2.
- **Social side:** `get_post_metrics_summary(workspaceId, pageIds, startDate, endDate)` on the labelled campaign posts shows the engagement the content earned.

## Content pointers: writing for keywords & AI visibility gaps

Keep these in mind when creating social content meant to target a specific keyword or close an AI-visibility gap:

- **Target one intent per post.** Pick a single keyword or question and answer that one thing clearly. Posts that try to cover everything rank and get cited for nothing.
- **Lead with the answer.** Put the takeaway in the first line, then support it. Skimmers and AI engines both extract the clearest, most self-contained statement — don't bury it.
- **Write the way people actually ask.** Phrase hooks, captions, and headers as real questions and plain-language answers. AI prompts are conversational, so natural phrasing beats keyword-stuffing.
- **Make claims quotable on their own.** AI tools lift snippets out of context, so each key sentence should stand alone — one idea, declarative, no "as mentioned above."
- **Be specific.** Numbers, concrete examples, named steps, clear definitions. Specificity is what gets cited and what sets you apart from generic content competitors already own.
- **Fill the gap, don't echo it.** If a competitor already owns a topic, find the sub-question or angle they're missing instead of repeating what's already ranking.
- **Stay consistent across surfaces.** Use the same terms and claims on social, your site, and your profiles so AI builds one coherent picture of what your brand is the answer for.
- **Keep it human.** It still has to read like a good post — optimizing for keywords or AI shouldn't make the writing robotic.

## Output

1. **AI visibility snapshot** — overview metrics + the share-of-voice heatmap.
2. **Prompt-gap clusters** — owned / contested / missing, with example prompts and the competitor(s) winning each.
3. **Content plan** — cluster → hypothesis → platform → angle.
4. **Created drafts** in Planable, labelled.
5. **Tracking plan** — the prompts added to the AI Result Tracker (if set up) and the metrics to re-pull later.

## Tips

- Respect the Data API rate limit (~10 req/s); with several brands × engines × prompt queries, pace the loop — and prefer narrow leaderboard calls over one giant one (see step 2).
- Report zero as zero. If an engine returns no prompts for a brand, say so — don't estimate.
- Recommend re-running monthly and diffing — AI visibility moves slowly, so a single snapshot isn't a verdict.

## Edge cases & limits

- **No sentiment.** These tools don't measure how a brand is *talked about*, only whether/where it appears. If the user wants sentiment, say it's not available through the connected MCPs.
- **Social is indirect.** Appearing in AI answers is heavily influenced by citable web content. This skill drives the social lever and tracks the result; it cannot publish or score website pages.
- **Ongoing tracking needs a project.** The one-off `DATA_` AI Search calls work without a project; the AI Result Tracker (prompts over time) requires an SE Ranking project.
- Posts are created as drafts — publishing happens in Planable after approval.
