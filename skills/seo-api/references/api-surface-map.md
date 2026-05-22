# API Surface Map

The decision tree for "which API and which tool do I need". Pulled from the live MCP server's tool catalogue plus the canonical docs at `seranking.com/api/*`.

## Top-level split

| API | Owns | Billed against | Required plan |
|---|---|---|---|
| **Data API** | Research-shaped data on any domain. No prior account setup. | Credits. | Any with API credits. |
| **Project API** | Operations on the user's own SE Ranking projects. | Plan limits (Sites / Keywords / Audit Pages / AIRT Prompts). | Business or Enterprise. |

**Both APIs share a single API key.** A request lands on Data API or Project API based on its endpoint path (`/v1/backlinks/*` vs `/v1/projects/*`), not based on which key you sent.

## Data API surfaces

### Backlinks (~30 tools, prefix `DATA_*Backlinks*` / `DATA_*RefDomains*` / `DATA_*Ips*`)

Read backlink profile of any domain.

- **Summary & metrics:** `DATA_getBacklinksSummary`, `DATA_getBacklinksMetrics`, `DATA_getBacklinksCount`.
- **Lists:** `DATA_getAllBacklinks`, `DATA_getBacklinksRaw`, `DATA_listNewLostBacklinks`.
- **Anchors:** `DATA_getBacklinksAnchors`.
- **Referring domains:** `DATA_getBacklinksRefDomains`, `DATA_getTotalRefDomainsCount`, `DATA_getNewLostRefDomainsCount`, `DATA_listNewLostReferringDomains`.
- **Referring IPs / subnets:** `DATA_getReferringIps`, `DATA_getReferringIpsCount`, `DATA_getReferringSubnetsCount`.
- **Authority:** `DATA_getDomainAuthority`, `DATA_getDomainAuthorityHistory`, `DATA_getDistributionOfDomainAuthority`, `DATA_getPageAuthority`, `DATA_getPageAuthorityHistory`, `DATA_getBacklinksAuthority`.
- **History:** `DATA_getCumulativeBacklinksHistory`, `DATA_getNewLostBacklinksCount`.
- **Indexed pages:** `DATA_getBacklinksIndexedPages`.
- **Export (async):** `DATA_exportBacklinksData` → `DATA_getBacklinksExportStatus`.

### Domain analysis (~12 tools)

Read keyword / traffic / competitor / ad profile of any domain.

- **Overview:** `DATA_getDomainOverviewWorldwide` (global), `DATA_getDomainOverviewDatabases` (per-region), `DATA_getDomainOverviewHistory` (12-month).
- **Keywords:** `DATA_getDomainKeywords` (full list; supports `url` param for per-URL).
- **Pages:** `DATA_getDomainPages` (top pages by traffic).
- **Subdomains:** `DATA_getDomainSubdomains`.
- **Competitors:** `DATA_getDomainCompetitors`, `DATA_getDomainKeywordsComparison`.
- **Ads:** `DATA_getDomainAdsByDomain`, `DATA_getDomainAdsByKeyword`.
- **URL-level overview:** `DATA_getUrlOverviewWorldwide`.

### Keyword research (~7 tools)

- `DATA_getRelatedKeywords`, `DATA_getSimilarKeywords`, `DATA_getLongTailKeywords`, `DATA_getKeywordQuestions`.
- `DATA_exportKeywords` (bulk export).

### SERP (~6 tools)

Real-time top-100 SERP results.

- **Task-based (recommended for batches):** `DATA_getSerpTasks` (list), `DATA_getSerpTaskResults`, `DATA_getSerpTaskAdvancedResults`.
- **Synchronous:** `DATA_getSerpResults`.
- **Locations:** `DATA_getSerpLocations`.
- **HTML dump:** `DATA_getSerpHtmlDump` (raw SERP HTML for diagnostic).

### Website audit — on-demand (~6 tools, lives under DATA)

For one-off audits of any site (vs. Project-attached audits below).

- **Create:** `DATA_createStandardAudit`, `DATA_createAdvancedAudit`.
- **Status:** `DATA_getAuditStatus`, `DATA_listAudits`.
- **Report:** `DATA_getAuditReport`, `DATA_getCrawledPages`, `DATA_getIssuesByUrl`, `DATA_getAuditPagesByIssue`.
- **Manage:** `DATA_updateAuditTitle`, `DATA_recheckAudit`, `DATA_deleteAudit`, `DATA_getAuditHistory`.

### AI Search (~10 tools, prefix `DATA_getAiSearch*`)

LLM-engine visibility data.

- **Overview:** `DATA_getAiSearchOverview`, `DATA_getAiSearchLeaderboard`.
- **Per-brand / per-target:** `DATA_getAiSearchBrand`, `DATA_getAiSearchPromptsByBrand`, `DATA_getAiSearchPromptsByTarget`.
- **Page-level:** `DATA_getAiVisibilityPages`, `DATA_getAiVisibilityPrompts`, `DATA_getAiVisibilityResponses`.
- **Sources / topics / sentiment / models / aliases / scores:** the `DATA_getAiVisibility*` family.
- **Reports:** `DATA_getAiVisibilityReports`.

### Account & system (~4 tools)

- `DATA_getSubscription` — plan info + `units_left`.
- `DATA_getCreditBalance` — alias.
- `DATA_getUserProfile` — user identity + workspace.

## Project API surfaces

Project API mutates the user's account. Confirm all `create / add / delete / update` calls before invoking.

### Project management (~15 tools)

- **List:** `PROJECT_listProjects`, `PROJECT_listOwnedProjects`, `PROJECT_listSharedProjects`.
- **CRUD:** `PROJECT_createProject`, `PROJECT_updateProject`, `PROJECT_deleteProject`.
- **Groups:** `PROJECT_listProjectGroups`, `PROJECT_createProjectGroup`, `PROJECT_updateProjectGroup`, `PROJECT_deleteProjectGroup`, `PROJECT_moveProjectsToGroup`.
- **Sharing:** `PROJECT_shareProject`.
- **Summary:** `PROJECT_getSummary`, `PROJECT_getSeoPotential`.
- **Brand:** `PROJECT_getSiteBrand`, `PROJECT_saveSiteBrand`.

### Rank tracking — keywords & search engines (~25 tools)

- **Keywords CRUD:** `PROJECT_listKeywords`, `PROJECT_addKeywords`, `PROJECT_updateKeyword`, `PROJECT_deleteKeywords`.
- **Keyword groups:** `PROJECT_listKeywordGroups`, `PROJECT_createKeywordGroup`, `PROJECT_updateKeywordGroup`, `PROJECT_deleteKeywordGroup`, `PROJECT_moveKeywordsToGroup`.
- **Tags:** `PROJECT_listTags`, `PROJECT_addTag`, `PROJECT_updateTag`, `PROJECT_deleteTag`.
- **Search engines:** `PROJECT_getSearchEngines`, `PROJECT_addSearchEngine`, `PROJECT_updateSearchEngine`, `PROJECT_deleteSearchEngine`, `PROJECT_getAvailableSearchEngines`, `PROJECT_getAvailableRegions`, `PROJECT_getGoogleLanguages`.
- **Positions:** `PROJECT_getPositionHistory`, `PROJECT_runPositionCheck`, `PROJECT_setKeywordPosition`, `PROJECT_getKeywordStats`, `PROJECT_getCheckDates`, `PROJECT_getHistoricalDates`.
- **GSC integration:** `PROJECT_getGoogleSearchConsole`.
- **Stats:** `PROJECT_getAdsStats`.

### Competitors (~7 tools)

- `PROJECT_listCompetitors`, `PROJECT_addCompetitor`, `PROJECT_deleteCompetitor`.
- `PROJECT_getCompetitorPositions`, `PROJECT_getCompetitorSerp10`, `PROJECT_getCompetitorSerp100`, `PROJECT_getAllCompetitorsMetrics`.

### Website audit (Project-attached, ~15 tools)

For ongoing audits tied to a project. Distinct from on-demand audits via `DATA_*` above.

- **Create & manage:** `PROJECT_createAudit`, `PROJECT_recheckAudit`, `PROJECT_deleteAudit`, `PROJECT_updateAuditTitle`, `PROJECT_listAudits`.
- **Settings:** `PROJECT_getAuditSettings`, `PROJECT_updateAuditSettings`, `PROJECT_resetAuditSettings`.
- **Sitemaps & source pages:** `PROJECT_listAuditSitemaps`, `PROJECT_addAuditSitemap`, `PROJECT_deleteAuditSitemap`, `PROJECT_listAuditSourcePages`, `PROJECT_addAuditSourcePages`, `PROJECT_deleteAuditSourcePages`.
- **Reports:** `PROJECT_getAuditReport`, `PROJECT_getAuditHistory`, `PROJECT_getAuditStatus`, `PROJECT_getCrawledPages`, `PROJECT_getIssuesByUrl`, `PROJECT_getAuditPagesByIssue`.

### Backlinks (Project-attached, ~10 tools)

For monitoring user-owned backlinks (vs. crawling any domain via Data API).

- **CRUD:** `PROJECT_listProjectBacklinks`, `PROJECT_addProjectBacklink`, `PROJECT_deleteProjectBacklinks`, `PROJECT_recheckProjectBacklinks`.
- **Groups:** `PROJECT_listBacklinkGroups`, `PROJECT_createBacklinkGroup`, `PROJECT_renameBacklinkGroup`, `PROJECT_deleteBacklinkGroup`, `PROJECT_moveBacklinksToGroup`.
- **GSC import:** `PROJECT_runBacklinkGscImport`, `PROJECT_getBacklinkGscImportStatus`, `PROJECT_updateBacklinkImportSettings`.
- **Stats:** `PROJECT_getBacklinkStats`, `PROJECT_getFoundLinks`.
- **Disavow:** `PROJECT_listDisavowedBacklinks`, `PROJECT_addDisavowedBacklinks`, `PROJECT_deleteDisavowedBacklink`.

### AIRT — AI Result Tracker (~10 tools)

- **Prompts:** `PROJECT_listPrompts`, `PROJECT_addPrompts`, `PROJECT_deletePrompts`, `PROJECT_transferPrompts`.
- **Prompt groups:** `PROJECT_listPromptGroups`, `PROJECT_createPromptGroup`, `PROJECT_updatePromptGroup`, `PROJECT_deletePromptGroup`, `PROJECT_deleteAllPromptsInGroup`, `PROJECT_movePromptsToGroup`, `PROJECT_changePromptGroupOrder`.
- **LLM engines:** `PROJECT_listLlmEngines`, `PROJECT_getLlmEngine`, `PROJECT_createLlmEngine`, `PROJECT_updateLlmEngine`, `PROJECT_deleteLlmEngine`.
- **Status & results:** `PROJECT_getLlmStatus`, `PROJECT_getLlmStatistics`, `PROJECT_getPromptAnswer`, `PROJECT_getPromptsRankings`.

### Marketing plan (~3 tools)

- `PROJECT_getMarketingPlan`, `PROJECT_addPlanTask`, `PROJECT_updatePlanTask`, `PROJECT_setPlanTaskStatus`, `PROJECT_deletePlanTask`.

### Sub-accounts (~5 tools)

- `PROJECT_listSubAccounts`, `PROJECT_createSubAccount`, `PROJECT_updateSubAccount`, `PROJECT_deleteSubAccount`, `PROJECT_getSubAccountDetails`.

### Account & profile (~3 tools)

- `PROJECT_getUserProfile`, `PROJECT_getAdsStats`.

## ID resolution — the lookup-first pattern

Most Project API operations need an ID. The skill should call the appropriate `*list*` or `*available*` tool first when the user didn't supply it.

| User said… | Lookup tool | Returns | Pass to |
|---|---|---|---|
| "for my project on acme.com" | `PROJECT_listProjects` | List of projects + `project_id` | `project_id` to any per-project tool |
| "track in the US" | (none — pass `country_code: "us"` directly) | — | `PROJECT_addSearchEngine` resolves automatically |
| "track in Catalonia" | `PROJECT_getAvailableSearchEngines` | `id` for regional engine | `search_engine_id` to `PROJECT_addSearchEngine` |
| "in Spanish" | `PROJECT_getGoogleLanguages` | Language code list | `language_code` to rank-tracking tools |
| "in Barcelona" | `PROJECT_getAvailableRegions` | Region records with verbatim `name` | `region_name` to rank-tracking tools (use exact name — abbreviations rejected) |
| "for keyword group X" | `PROJECT_listKeywordGroups` | Group IDs + names | `group_id` to `PROJECT_moveKeywordsToGroup` etc. |
| "for our backlink group X" | `PROJECT_listBacklinkGroups` | Group IDs + names | `group_id` to backlink group tools |
| "for AIRT prompt group X" | `PROJECT_listPromptGroups` | Group IDs + names | `group_id` to prompt group tools |
| "for SERP in {city}" | `DATA_getSerpLocations` | Locations + codes | `location` to SERP tools |
| "audit X" | `DATA_listAudits` / `PROJECT_listAudits` | Audit IDs | `audit_id` to report/recheck/delete |

## Quick decision tree

```
"I want to research a domain I don't own"
  → Data API
    backlinks → DATA_getBacklinks*
    keywords → DATA_getDomainKeywords / getDomainOverviewWorldwide
    competitors → DATA_getDomainCompetitors
    SERP for a keyword → DATA_getSerpResults / SerpTask
    one-off audit → DATA_createStandardAudit
    LLM visibility → DATA_getAiSearch*

"I want to track/manage state on my own SE Ranking projects"
  → Project API (needs Business/Enterprise plan)
    create project → PROJECT_createProject
    add keywords to track → PROJECT_addKeywords (after PROJECT_addSearchEngine)
    daily ranks → PROJECT_runPositionCheck / PROJECT_getPositionHistory
    project audit → PROJECT_createAudit
    backlink monitoring → PROJECT_addProjectBacklink (with PROJECT_runBacklinkGscImport for bulk)
    AIRT prompts → PROJECT_addPrompts (with PROJECT_createLlmEngine if a custom engine)
    competitors → PROJECT_addCompetitor + PROJECT_getCompetitorPositions

"I want to integrate SE Ranking into another tool"
  → Both, usually
    e.g., "weekly client report"
      use PROJECT_getPositionHistory + DATA_getDomainCompetitors + DATA_getBacklinksSummary
      pipe into Looker / Sheets / your dashboard
```

## Built-in MCP prompts (server-shipped recipes)

The MCP server ships 5 built-in prompts (via the `prompts/list` capability) — encoded recommended tool sequences for common workflows. **Prefer these when the user's ask matches**:

| Prompt | What it does | Args |
|---|---|---|
| `serp-analysis` | Compare SERPs across two locations for a keyword | `keyword`, `location1`, `location2`, optional `language`, optional `device` |
| `backlink-gap` | Find backlink opportunities vs. competitors | `my_domain`, `competitors` (comma-separated), optional `min_domain_trust` |
| `domain-traffic-competitors` | Traffic + top competitors for a domain | `domain` |
| `keyword-clusters` | Build intent-grouped keyword clusters | `market`, `seed_keywords` |
| `ai-share-of-voice` | LLM-engine visibility vs. competitors | `domain`, `competitors`, optional `country`, `llm_engines` |

These prompts are accessible via any spec-compliant MCP client. In Claude Code: `/mcp` shows them; calling `mcp__claude_ai_SE_Ranking__<prompt-name>` (varies by client) executes.
