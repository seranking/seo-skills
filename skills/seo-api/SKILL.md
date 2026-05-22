---
name: seo-api
description: SE Ranking API integration architect for developers. Covers the entire SE Ranking surface — Data API (keyword research, backlinks, domain & competitor analysis, SERP, website audit, AI Search, account) AND Project API (rank tracking, project management, keyword/competitor/backlink/group operations, marketing plan, sub-accounts, AIRT prompts). For any "how do I…" question about endpoints, parameters, JSON schemas, credit cost, rate limits, or authentication. Produces ready-to-paste cURL / Python / TypeScript / MCP-tool-call recipes, and (with explicit confirmation) wires up Project API state — create projects, add keywords, configure audits, set up AIRT prompt groups, manage backlink groups. Pulls live tool schemas from the connected SE Ranking MCP so reference data is never stale. Distinct from the other 24 SEO skills which produce analysis deliverables (briefs, audits, reports); `seo-api` produces integration recipes and wired-up state. Use when the user asks "how do I use SE Ranking API to do X", "what endpoint gives me Y", "credit cost of workflow Z", "build a rank tracker", "set up an audit for client X", "Postman / cURL / Python / TypeScript for SE Ranking", "what's the rate limit", "integrate SE Ranking with Looker / n8n / Make", "create a project", "add keywords", or any direct question about endpoints, parameters, schemas, or wiring up Project API resources.
---
> Live with the SE Ranking MCP at `https://api.seranking.com/mcp`. Tool schemas are introspected live; this skill never relies on a frozen snapshot of the API surface.

# SE Ranking API Integration Architect

Help developers ship real integrations against the SE Ranking SEO Data API and Project API. The deliverable is either a **code recipe** (ready-to-paste cURL / Python / TypeScript / MCP-tool-call sequence) or **live wiring** of Project API state (create projects, add keywords, configure audits, set up AIRT prompts), or both. The skill knows the entire 195-tool surface, the credit and rate-limit cost of every call, and the canonical setup story for every major MCP client.

## Prerequisites

- **SE Ranking MCP connected** at `https://api.seranking.com/mcp`. Single API key authenticates both `DATA_*` and `PROJECT_*` tools through the unified gateway. If `/mcp` doesn't show `se-ranking`, the skill emits the install command and stops — see `references/auth-and-keys.md`.
- **(Optional) `WebFetch`** for fetching deep guides at `seranking.com/api/data/*` and `seranking.com/api/project/*` when the request needs prose beyond JSON Schema.
- User provides: an integration goal in plain language (e.g., "build a rank tracker for client X", "pull all backlinks for these 50 domains into BigQuery weekly", "configure an audit + AIRT prompts for a new project"). The skill interviews only when the goal is ambiguous.

## Process

1. **Preflight.**
   - Confirm the SE Ranking MCP is reachable. If not, emit:
     ```bash
     claude mcp add --transport http se-ranking https://api.seranking.com/mcp
     ```
     and stop. See `references/auth-and-keys.md` for OAuth vs. `X-Api-Key` header tradeoffs and headless / CI patterns.
   - Call `DATA_getSubscription` (0 credits). Record `units_left`, plan status, expiration — `units_left` is the figure to forecast against, and it gets printed in the cost forecast in step 5. Optionally also call `DATA_getCreditBalance` for its `{ limit, used }` view — but the two are **not** aliases: they report different remaining-credit numbers that do not reconcile (an ~8.6M gap is normal), so treat `getSubscription.units_left` as the source of truth.

2. **Clarify the goal.** Ask 1–3 questions only if the goal is ambiguous. Skip when the user already spelled it out. Useful follow-ups:
   - "Is this a one-off run, a recurring job (daily/weekly), or a long-lived integration in your product?"
   - "Target country / language / device — or worldwide?"
   - "Are we operating on a project you already own in SE Ranking, or just researching domains?"

3. **Identify the API surface(s).** Map the goal to one or both of:
   - **Data API** — research-shaped data on any domain, no prior account setup. Credit-billed. See `references/api-surface-map.md` § "Data API surfaces".
   - **Project API** — operations on the user's own SE Ranking projects (rank tracking, audits, AIRT, backlink groups, marketing plan, sub-accounts). Subscription-limit-billed, not credit-billed. Requires Business or Enterprise plan. See `references/api-surface-map.md` § "Project API surfaces".
   - Many real integrations span both — e.g., a rank-tracker setup uses `PROJECT_createProject` + `PROJECT_addKeywords` + `PROJECT_runPositionCheck`, then reports use `DATA_getDomainKeywords` for the same domain.

4. **Map to tools / endpoints.** For every step in the integration, name:
   - The MCP tool: `` `DATA_getDomainKeywords` `` or `` `PROJECT_addKeywords` ``.
   - The underlying REST endpoint + HTTP verb (e.g., `GET /v1/domain/keywords`).
   - The credit cost (Data API) or limit consumed (Project API). Source costs from `references/rate-limits-and-credits.md` and the per-endpoint pages at `seranking.com/api/data/*` — MCP tool `description` fields carry input schemas and usage notes but **not** credit costs.
   - If a tool needs an ID the user didn't supply (project ID, search engine ID, geo region name, language code), insert the prerequisite `*list*` or `*available*` call before it. See `references/api-surface-map.md` § "ID resolution".

5. **Forecast cost.** Sum credit cost across all Data API calls. For Project API calls, surface plan-limit impact (e.g., "this consumes 1 Site + 50 Keywords + ~500 Audit Pages from your plan"). Compare against:
   - `units_left` from step 1 — if insufficient, surface and stop with the upgrade link.
   - Plan limits if Project API tools are involved — `PROJECT_getUserProfile` returns current usage; flag if the integration would push a limit over.

6. **Pick execution mode.** Confirm with the user explicitly:
   - **Code mode** — emit ready-to-paste cURL, Python (`requests`), TypeScript (`fetch`), and MCP-tool-call variants. The developer runs them. Default for read-only research, recurring jobs the user wants to own, and anything they want to deploy outside their Claude session.
   - **Live mode** — execute the integration step by step via MCP. Confirm every mutating call. Default for one-off Project API setup (new project, add keywords, configure audit, set up AIRT prompt group, etc.) where the user wants the state to exist by the end of this conversation.
   - **Hybrid** — wire up the one-time setup live, emit code for the recurring workload (e.g., "I created the project and added the 50 keywords for you; here's the daily-run Python script to pull positions and write them to BigQuery").

7. **Execute or emit.**
   - **Code mode** — write `code/curl.sh`, `code/python.py`, `code/typescript.ts`, `code/mcp-calls.md`. Each file is a complete runnable example, not a fragment. Include error handling for `429` (rate limit) and `403` (insufficient credits). See `references/integration-patterns.md` for canonical pattern snippets.
   - **Live mode** — for each *mutating* call (`PROJECT_create*`, `PROJECT_add*`, `PROJECT_delete*`, `PROJECT_update*`, `DATA_createStandardAudit`, `DATA_createAdvancedAudit`, etc.), print a single-line confirmation:
     ```
     About to call PROJECT_createProject(domain="acme.com", name="ACME Inc — Rank Tracker", country="us").
     Consumes: 1 "Site" from your subscription. Proceed? [y/N]
     ```
     Wait for explicit `y` / `yes`. On anything else, fall back to code mode and emit the equivalent code instead of executing. Read-only calls (`DATA_get*`, `DATA_list*`, `PROJECT_get*`, `PROJECT_list*`) run without confirmation. Log every call to `evidence/03-execution-log.md` with timestamp, args, response status.

8. **Synthesise `RECIPE.md`.** Always written, regardless of mode. The deliverable a developer reads to understand what was built or how to build it. See output format below.

## Output format

Folder `seo-api-{slug}-{YYYYMMDD}/` where `{slug}` is a kebab-case summary of the goal (e.g., `acme-rank-tracker`, `bulk-backlinks-bigquery`).

```
seo-api-{slug}-{YYYYMMDD}/
├── RECIPE.md                       (primary deliverable — what was built or how to build it)
├── code/
│   ├── curl.sh                     (cURL one-liners + multi-step bash)
│   ├── python.py                   (idiomatic requests-based script)
│   ├── typescript.ts               (fetch + zod-validated responses)
│   └── mcp-calls.md                (MCP-tool-call sequence — same workflow, agent-native)
└── evidence/
    ├── 01-preflight.md             (credit balance, subscription status, MCP connectivity check)
    ├── 02-cost-forecast.md         (per-call cost breakdown, plan-limit deltas, total)
    ├── 03-ids-resolved.md          (Project API / search-engine IDs, geo codes resolved upfront — omit if none needed)
    └── 04-execution-log.md         (every MCP call executed, with args + status — omit in pure code mode where nothing ran)
```

Top-level: `RECIPE.md` + `code/`. The `evidence/` folder preserves the reasoning trail; auditors lean on `02-cost-forecast.md` and the execution log. `03` and `04` are conditional — a run with no ID lookups and no executed calls (pure code-mode advice) ships just `01` + `02`.

`RECIPE.md` follows this shape:

```markdown
# {Integration Title}: {target}

> Run dated {YYYY-MM-DD} · Mode: {code | live | hybrid} · Total cost: {n} credits + {plan-limits consumed}

## Goal

{1–2 sentences. What was asked, what's being shipped.}

## API surface map

| Step | MCP tool | REST endpoint | Verb | Cost |
|------|----------|---------------|------|------|
| 1    | `DATA_getCreditBalance` | `/v1/account/subscription` | GET | 0 credits |
| 2    | `PROJECT_listProjects` | `/v1/account/projects` | GET | 0 (plan limit: read) |
| 3    | `PROJECT_createProject` | `/v1/projects` | POST | 1 Site from plan |
| ...  | ... | ... | ... | ... |

## Auth & setup

{cURL header / Python session / TypeScript fetch wrapper showing exactly how to authenticate. Reference `references/auth-and-keys.md` for OAuth vs. header tradeoffs.}

## Cost forecast

- Credit cost (Data API): {n} credits ({explanation per call})
- Plan-limit consumption (Project API): {Sites: n, Keywords: n, Audit Pages: n, AIRT Prompts: n}
- Your balance at run time: {units_left} credits, {plan limits available}
- {OK / WARNING: this integration would push X over plan limit}

## Recipe

### Option A — cURL

(complete bash script in `code/curl.sh`)

### Option B — Python

(complete script in `code/python.py`)

### Option C — TypeScript

(complete script in `code/typescript.ts`)

### Option D — MCP tool calls

(agent-native sequence in `code/mcp-calls.md` — for when this integration lives inside another Claude/Cursor/Codex workflow)

## Rate limit & retry strategy

- Data API: 10 RPS, Project API: 5 RPS. Pace sequentially for batched workflows; small-batch parallelism (≤3 concurrent) is safe.
- 429 handling: exponential backoff with jitter (1s → 2s → 4s → 8s, ±20% jitter). 5xx: same. Treat 403 "Insufficient funds" as terminal — no retry.

## What's running now (live mode only)

{Bullet list of MCP calls that were executed, with their outcomes. Pulled from `evidence/04-execution-log.md`.}

## What you still need to do

{Concrete next steps for the developer. E.g., "Run `python.py` daily via cron at 06:00 UTC", "Open the project at https://online.seranking.com/...", "Add a webhook for rank changes via Settings → Notifications".}

## Linked docs

- {Direct links to the relevant pages on `seranking.com/api/data/*` and `seranking.com/api/project/*`.}

## When to escalate to another skill

- `seo-content-brief` — once your integration is pulling keyword data, this skill turns it into editor briefs.
- `seo-technical-audit` — if the integration involves website audits, this skill interprets the audit output.
- `seo-drift baseline` — if the integration's job is to track a domain over time, snapshot it first.
```

## Tips

- **Single API key authenticates everything.** `API_TOKEN` (or `X-Api-Key` header for headless) covers both `DATA_*` and `PROJECT_*`. The legacy split into separate Data and Project keys is gone — passing both still works as headers for backwards compatibility, but you can use just `X-Api-Key` now. See `references/auth-and-keys.md`.
- **Rate limits are per-API-key, not per-IP.** All threads / workers / servers sharing one key contribute to the same 10-RPS (Data) or 5-RPS (Project) budget. For production fan-outs, mint multiple keys via the API Dashboard.
- **Failed requests are free.** 4xx and 5xx never consume credits. Don't over-engineer cost protection for normal error retries.
- **Project API limits are not credits.** They consume your subscription's "Sites", "Keywords", "Audit Pages", "AIRT Prompts" quotas. Surface plan-limit impact upfront for any mutating call — these limits are stickier than credits because the user has to upgrade their plan to lift them, not just buy a credit pack.
- **Confirm before mutating.** `PROJECT_create*`, `PROJECT_add*`, `PROJECT_delete*`, `PROJECT_update*`, `DATA_create*Audit`, `DATA_deleteAudit` all permanently modify account state. Always print a one-line summary (tool, args, what gets consumed) and wait for `y`/`yes` before calling.
- **Use the right ID resolution tool.** Most "I want to operate on project X / keyword Y" requests need an ID lookup first. See `references/api-surface-map.md` § "ID resolution" for the full table. Common cases:
  - Project IDs → `PROJECT_listProjects` (or `PROJECT_listOwnedProjects` / `PROJECT_listSharedProjects` for sub-account setups).
  - Search engine for rank tracking → pass `country_code` directly to `PROJECT_addSearchEngine` (ISO 3166-1 alpha-2). Only fall back to `PROJECT_getAvailableSearchEngines` for regional engines (Catalonia, Turkish-Cypriot Cyprus).
  - SERP locations → `DATA_getSerpLocations`.
  - Languages → `PROJECT_getGoogleLanguages`.
  - Regions for local rank tracking → `PROJECT_getAvailableRegions` (use the verbatim `name` field; abbreviations are rejected).
- **For exports, poll the status endpoint.** Async endpoints (`/backlinks/export`, `/keywords/export`) return a task ID; subsequent polls of `*ExportStatus` count against the rate limit but cost 0 credits. Start with a 5s poll interval; exponential backoff if the task is large.
- **Check the MCP tool description before WebFetching docs.** Every MCP tool exposes its full input schema, defaults, and usage notes via the protocol — e.g. `DATA_getDomainCompetitors` documents its own ~60KB response cap. One thing the descriptions do *not* carry: credit costs — for those, use `references/rate-limits-and-credits.md` and the public per-endpoint pages.
- **Large list endpoints can overflow the MCP transport.** `DATA_getDomainCompetitors` on a popular domain — and `DATA_getDomainKeywords` / `DATA_getAllBacklinks` on big domains — return responses past the MCP client's inline token limit; the result is auto-saved to a file instead. Recover it with a `jq` slice on the saved file, or call the REST endpoint directly (raw REST has no size cap). See `references/api-surface-map.md`.
- **For "show me Swagger / OpenAPI for the MCP"** — point the developer at MCP Inspector (`npx @modelcontextprotocol/inspector https://api.seranking.com/mcp`) or `mcp-scan`. Both walk the live tool/prompt/resource catalogue. A canonical MCP→OpenAPI converter is on the roadmap; for now the inspector output is the source of truth.

## Works well with

- **Predecessors:** none — entry point for any API integration question.
- **Successors (when the integration starts producing data):**
  - `seo-content-brief` — when the integration pulls keyword research that should become editor briefs.
  - `seo-page` — when one URL from the integration needs a keep/refresh/consolidate/kill verdict.
  - `seo-drift baseline` — to snapshot a domain or URL before the integration starts running, so regressions are detectable.
  - `seo-technical-audit` — when the integration involves audit runs and the output needs prioritisation.
  - `seo-ai-search-share-of-voice` — when the integration tracks AIRT visibility and needs a competitive read.

## References

- `references/auth-and-keys.md` — API key formats, OAuth vs. header, headless / CI patterns, key rotation.
- `references/rate-limits-and-credits.md` — 10 RPS / 5 RPS, credit billing models, plan-limit consumption, error codes (429, 403), exponential-backoff template.
- `references/api-surface-map.md` — full routing table (which API owns what) + ID resolution table + decision tree for "which tool do I need".
- `references/integration-patterns.md` — five canonical recipes copy-paste-ready: rank tracker setup, bulk backlink export, audit pipeline, AIRT visibility tracker, keyword research bulk job.
