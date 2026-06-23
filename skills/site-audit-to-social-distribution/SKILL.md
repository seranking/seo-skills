---
name: site-audit-to-social-distribution
description: >
  Find weak pages, technical issues, and content gaps in SE Ranking, then coordinate the fix end-to-end
  in Planable — drafting the rewritten page copy in a Universal content page for feedback and approval,
  and scheduling the supporting social distribution. Use this skill whenever the user wants to act on a
  site/SEO audit by getting content fixed and promoted, or says things like "audit the site and help us
  fix the weak pages", "we need to rewrite these pages and approve the new copy", "coordinate a content
  refresh", "turn audit findings into an action plan with social distribution", or "which pages should we
  fix and how do we get the updates reviewed". Always activate when SE Ranking findings need to become
  reviewed, approved content plus a social push.
---

# Site audit → coordinated rewrite + social distribution

Close the loop between *finding* SEO problems (SE Ranking) and *fixing and promoting* them (Planable). Planable's Universal content pages hold the rewritten page copy so it can be reviewed with comments and formally approved before anyone publishes it to the site; the social layer schedules posts that distribute the refreshed page.

## Prerequisites

- **SE Ranking MCP** connected (a project enables repeatable audits + competitive context; one-off audits work without one).
- **Planable MCP** connected, with a **Universal content page** for the page-copy review and **social pages** for distribution. Pages are added inside Planable — they can't be created via the connector.
  - These two may live in **different workspaces** (e.g. a "Universal pages" workspace for page copy and a brand workspace for social). That's fine — run the rewrite in whichever workspace has the Universal page, and the distribution in whichever has the connected social pages. Confirm both up front with `list_pages`; if the Universal page is missing, ask the user to add one.

## Connector health check

Before doing anything else, verify both MCPs are reachable:

- **SE Ranking:** call `DATA_getSubscription`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The SE Ranking connector isn't responding — please reconnect it before we continue. Setup guide: https://seranking.com/api/integrations/mcp/"
- **Planable:** call `list_workspaces`. If it fails or returns an auth error, stop immediately and tell the user:
  > "The Planable connector isn't responding — please reconnect it before we continue. Setup guide: https://help.planable.io/hc/en-us/articles/27538577098780-How-to-connect-Planable-MCP-to-your-AI-tools"

Only continue to the process steps below once both calls return a successful response.

## Process

### 1. Get the audit — reuse before you crawl
A full crawl is slow and consumes plan crawl budget, so **check for an existing audit first**:
- `PROJECT_listAudits` (or `DATA_listAudits`) — if a recent **finished** audit exists for the domain, reuse it; read it with `PROJECT_getAuditReport` / `DATA_getAuditReport(audit_id)`. Note the audit date and tell the user how fresh it is — offer to re-run if it's stale (more than a month or two old).
- Only if none exists (or the user wants fresh data): `PROJECT_createAudit(domain, settings?)` → poll readiness → `getAuditReport`. Without a project, use `DATA_createStandardAudit` (or `createAdvancedAudit`). Scope `max_pages` sensibly for large sites.

Then list the specific pages behind each issue with `DATA_getAuditPagesByIssue` / `getIssuesByUrl`. Focus on issues that move rankings and map to page copy: duplicate/missing titles & descriptions, missing H1s, thin content, plus technical flags (broken links, indexability, redirects).

### 2. Add competitive + demand context
For the pages worth fixing, understand what "good" looks like:
- `DATA_getDomainCompetitors` + `DATA_getDomainKeywordsComparison` — what competitors rank for on these topics that this page doesn't (discard off-brand/junk gap terms — see the seo-gaps skill's note).
- `DATA_getSerpResults` for the page's target query — the dominant content format and SERP features to match.
- `DATA_getRelatedKeywords` + `DATA_getKeywordQuestions` — subtopics and questions the rewrite should cover (query a few seeds; each returns only a handful).

### 3. Prioritise
Build a ranked fix list: **page URL → issue(s) → opportunity (target query, volume, gap) → effort**. Lead with pages that combine a real issue and real demand. Surface this list to the user and confirm which pages to draft.

### 4. Draft the rewritten copy in a Universal content page (the review surface)
For each agreed page, write the improved copy (title, meta description, H1/H2 outline, and body or detailed section guidance grounded in steps 1–2). Create it in Planable on the **Universal content page**:

`create_post(workspaceId, universalPageId, text)` — put the live page URL in the body so reviewers know which page it maps to.

This gives the team a real review object:
- `create_comment(workspaceId, postId, text)` for feedback and questions (`teamOnly: true` for internal notes).
- `update_post(workspaceId, postId, text)` to apply revisions in place.
- `approve_post(workspaceId, postId)` for sign-off.

**Keep the page-copy drafts separate from the social posts** — `create_grouped_post` splits universal and non-universal pages into different sub-groups, so don't try to sync website copy and social captions in one grouped post.

### 5. Schedule the social distribution layer
For each approved page refresh, draft social posts that announce or support it — `create_post` per platform or `create_grouped_post` for synced copy across social pages (remember a grouped post shares one text, so mind the strictest platform's length). Tie them to the same campaign with a label (e.g. "content-refresh"); note labels are per-workspace, so if social lives in a different workspace than the Universal page, create the label there too. 

**Scheduling — ask before creating.** Don't guess dates or leave everything undated by default. Ask how the user wants the batch dated and offer: **spread evenly** across a window (e.g. the next 7 days, one post per slot at a sensible hour), a **fixed cadence/interval** (e.g. every weekday at 10:00, laid out from a start date they give), **manual** dates per post, or **no dates yet** (undated drafts to place on the calendar later). Convert each chosen time to ISO 8601 and pass it as `scheduledAt`. Keep posts as **proposed drafts** — don't set `publishAtScheduledDate` — so nothing auto-publishes; only set it `true` if the user explicitly wants auto-publishing. Scheduled times are treated as **UTC**, so confirm the timezone or state that times are UTC.

### 6. Hand off the publish step
The approved page copy is ready for whoever owns the website/CMS to publish — that step is manual and outside these MCPs. Summarise: which pages were drafted, their review/approval state, and the social posts queued to distribute them. Offer to re-audit after changes ship to confirm the issues cleared.

## Content pointers: writing for keywords & AI visibility gaps

Keep these in mind when writing the page-rewrite copy and the supporting social content meant to target a specific keyword or close an AI-visibility gap:

- **Target one intent per post.** Pick a single keyword or question and answer that one thing clearly. Posts that try to cover everything rank and get cited for nothing.
- **Lead with the answer.** Put the takeaway in the first line, then support it. Skimmers and AI engines both extract the clearest, most self-contained statement — don't bury it.
- **Write the way people actually ask.** Phrase hooks, captions, and headers as real questions and plain-language answers. AI prompts are conversational, so natural phrasing beats keyword-stuffing.
- **Make claims quotable on their own.** AI tools lift snippets out of context, so each key sentence should stand alone — one idea, declarative, no "as mentioned above."
- **Be specific.** Numbers, concrete examples, named steps, clear definitions. Specificity is what gets cited and what sets you apart from generic content competitors already own.
- **Fill the gap, don't echo it.** If a competitor already owns a topic, find the sub-question or angle they're missing instead of repeating what's already ranking.
- **Stay consistent across surfaces.** Use the same terms and claims on social, your site, and your profiles so AI builds one coherent picture of what your brand is the answer for.
- **Keep it human.** It still has to read like a good post — optimizing for keywords or AI shouldn't make the writing robotic.

## Output

1. **Prioritised fix list** — page → issue → opportunity → effort.
2. **Universal content page drafts** — the rewritten copy, in Planable, ready for comments and approval (with links).
3. **Social distribution drafts** — scheduled posts supporting each refreshed page.
4. **Coordination summary** — what's approved, what's awaiting review, what's queued, and what needs to be published to the site.

## Tips

- The Universal content page is the collaboration surface for *page copy*; treat its posts as documents, not social captions. Put the live URL in the body so reviewers have context.
- Reuse audits and don't over-crawl. Crawl budget is limited by plan — read an existing audit when one is fresh enough, and scope `max_pages` when you must crawl.
- Ground every rewrite recommendation in audit + SERP evidence; don't assert "add 800 words" without a reason from the data.

## Edge cases & limits

- **Publishing to the website is out of scope.** These MCPs review and approve the copy and handle social distribution; they do not push to a CMS. Be explicit about the handoff.
- **Universal page and social pages may be in different workspaces.** Don't assume one workspace has both — confirm with `list_pages` and run each layer where its pages live.
- **Pages can't be created via the connector.** If a workspace lacks a Universal content page (or the needed social pages), ask the user to add them in Planable first.
- **Approvals require a configured workflow.** `approve_post` only works if the workspace has an approval workflow; if not, use comments for sign-off and note it.
- Re-auditing to verify fixes only reflects changes once they're actually published to the live site.
