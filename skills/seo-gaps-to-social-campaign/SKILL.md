---
name: seo-gaps-to-social-campaign
description: >
  Turn SE Ranking search-opportunity insights into a ready-to-publish social campaign in Planable.
  Use this skill whenever the user wants to convert SEO research into social content — keyword gaps,
  competitor wins, ranking losses, question keywords, or new topic opportunities — and have the posts
  drafted and scheduled in Planable. Trigger on things like "what should we post based on our SEO data",
  "turn these keyword gaps into posts", "our competitor is ranking for X, make social content about it",
  "repurpose our ranking opportunities into a campaign", "build a social campaign from search demand", or
  "fill the calendar based on what people are searching". Always activate when SE Ranking research is the
  starting point and Planable is the destination.
---

# SEO gaps → social campaign

Connect SE Ranking (where the demand and the gaps live) to Planable (where content gets made, approved, and published). The goal is a focused social campaign whose every post is grounded in real search demand — not a generic brainstorm.

## Prerequisites

- **SE Ranking MCP** connected (Data API for research; a project is optional but unlocks ranking-loss detection).
- **Planable MCP** connected, with the destination workspace and at least one connected page.
- The user provides: target domain, market/country (default `us`), the Planable workspace, and ideally 1–3 competitor domains. Number of posts defaults to 6 if unspecified.

## Connector health check

Before doing anything else, verify both MCPs are reachable:

- **SE Ranking:** call `DATA_getSubscription`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The SE Ranking connector isn't responding — please reconnect it before we continue. Setup guide: https://seranking.com/api/integrations/mcp/"
- **Planable:** call `list_workspaces`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The Planable connector isn't responding — please reconnect it before we continue. Setup guide: https://help.planable.io/hc/en-us/articles/27538577098780-How-to-connect-Planable-MCP-to-your-AI-tools"

Only continue to the process steps below once both calls return a successful response.

## Process

### 1. Scope the campaign
Confirm: target domain, country, competitors (optional), the Planable workspace + which platforms, how many posts, and any campaign window. If the workspace is ambiguous, call `list_workspaces` and let the user pick — do not guess.

### 2. Discover opportunities in SE Ranking
Work sequentially (respect the Data API limit of ~10 requests/second). Save raw results as you go.

- `DATA_getDomainOverviewWorldwide` + `DATA_getDomainKeywords` — the target's current footprint and best existing keywords. The target's own strong/striking-distance keywords are often the most on-brand campaign fuel, so mine these first.
- `DATA_getDomainCompetitors` — confirm the real organic competitors (sort by shared keywords; take the top 3–5). Note: this call returns the full set and may be written to a file — read and parse it.
- `DATA_getDomainKeywordsComparison` — the core gap list: keywords competitors rank for that the target does not. Filter to keep it useful (e.g. informational/commercial intent, volume > a sensible floor, difficulty the domain can realistically win). **Then judge relevance, not just the numbers** — competitor gap lists are noisy and surface off-brand junk (glossary entries, follower-farming terms like "free followers", unrelated blog tangents). Discard anything that isn't a topic the target could credibly post about; a high-volume term the brand has no business addressing is not an opportunity. If a strict filter returns almost nothing, loosen one threshold or try another competitor rather than forcing a campaign out of junk.
- `DATA_getRelatedKeywords` + `DATA_getKeywordQuestions` — expansion terms and real questions people ask. **Question keywords are gold for social hooks** — they map directly to post openers. These endpoints often return only a handful of rows per seed, so query **several seeds (3–5 core topics) and aggregate** rather than trusting one; a seed returning 1–2 questions is normal, not a sign there's no demand.
- `DATA_getSerpResults` for the 2–4 strongest themes — read the intent and the SERP features so the social angle matches what searchers actually want.
- **Ranking losses (if a project exists):** call `PROJECT_getPositionHistory` (type `avg_pos` or `visibility`) to find terms that slipped. A recovering or slipping keyword is a strong "we have something to say" social trigger. If there is no project, skip this and rely on the gap analysis above.

### 3. Cluster into themes, then into angles
Group the keywords/questions into 3–6 content themes. For each theme, write a one-line rationale tied to the data (volume, gap size, intent, or a ranking move). Then translate each theme into concrete social angles — a question keyword becomes a hook, a comparison term becomes a carousel, a how-to becomes a tips post.

Surface the themes to the user **before** drafting, so they can steer.

### 4. Draft the posts
Write platform-appropriate copy for each post (see length/format norms below). Vary hooks and formats across the batch — don't repeat one structure. Keep each post traceable to its source keyword/question so the user understands the "why".

| Platform | Length | Notes |
|---|---|---|
| LinkedIn | ~3,000 chars | Professional, can be long-form, line breaks |
| Instagram | ~2,200 chars | Visual-first; hashtags at end or first comment; requires media |
| Facebook | shorter performs better | Conversational |
| X/Twitter | 280 chars | Punchy |
| TikTok | ~2,200 chars | Casual, trend-aware |

Show all drafts in a preview before creating anything, unless the user said "just create them".

### 5. Create the drafts in Planable
`list_pages(workspaceId)` to get page IDs for the requested platforms. Then:

- Same content across platforms → `create_grouped_post(workspaceId, pageIds[], text, scheduledAt?, labels?)`. **Caveat:** a grouped post shares one text across every page, so grouping platforms with very different limits (e.g. Facebook + X) forces the shared copy under the strictest one (X's 280 chars). When copy should differ in length or tone per platform, use separate `create_post` calls instead.
- Per-platform copy → `create_post(workspaceId, pageId, text, scheduledAt?, labels?, firstComment?)` once per page.
- **Scheduling — ask before creating.** Don't guess dates or leave everything undated by default. Ask how the user wants the batch dated and offer: **spread evenly** across a window (e.g. the next 7 days, one post per slot at a sensible hour), a **fixed cadence/interval** (e.g. every weekday at 10:00, laid out from a start date they give), **manual** dates per post, or **no dates yet** (undated drafts to place on the calendar later). Convert each chosen time to ISO 8601 and pass it as `scheduledAt`. Keep posts as **proposed drafts** — don't set `publishAtScheduledDate` — so nothing auto-publishes; only set it `true` if the user explicitly wants auto-publishing. Scheduled times are treated as **UTC**, so confirm the timezone or state that times are UTC.
- If the user wants the batch tagged, call `list_labels` (or `create_label`) and pass the label UUIDs. A campaign label (e.g. "SEO-driven") makes later reporting easy.

### 6. Confirm and hand off
Report how many drafts were created, in which workspace/pages, the proposed schedule, and any `validationErrors` (e.g. Instagram needs media — flag it). Offer to set up rank/AI tracking for the targeted terms, or to report on the campaign later (the `seo-ai-social-report` skill).

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

1. A short **content plan** the user can scan: theme → source keyword/question (with volume/difficulty) → platform → angle.
2. The **created drafts** summary with Planable links.
3. Optional: save a `campaign-brief.md` to the outputs folder if the user wants something to circulate.

## Tips

- Never invent search volume or difficulty. If SE Ranking returns null, mark it unknown rather than guessing — the credibility of the plan depends on it.
- Relevance beats volume. A 320-volume question your brand can answer brilliantly will outperform a 50k-volume term that has nothing to do with the product.
- Match intent to platform: informational questions → educational posts; commercial/comparison terms → proof, demos, comparisons.
- Posts are created as drafts. They will not publish until approved/scheduled in Planable. Say this explicitly so nothing goes live unexpectedly.

## Edge cases & limits

- **Ranking-loss detection needs an SE Ranking project** with position history. Without one, the campaign is built from competitor gap analysis (still strong, just not loss-driven).
- **No SE Ranking Content Editor via MCP.** This skill drafts the social copy directly; it does not produce a Content-Editor optimization score. If the user needs website/blog copy scored, that step stays in the SE Ranking UI.
- **Instagram/visual platforms require media.** Text-only drafts will flag a validation error; offer to attach a public image URL via `mediaUrls`, or note that media must be added in Planable before publishing.
- This skill creates social drafts only — publishing happens in Planable after approval.
