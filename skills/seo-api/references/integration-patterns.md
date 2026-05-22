# Integration Patterns

Five canonical recipes the `seo-api` skill draws from. Each one is ready to paste — the skill adapts variable names, target domains, and credentials but doesn't need to re-derive the shape.

## Pattern 1 — Rank tracker setup (Project API)

**Goal:** stand up a new project, add a search engine, add 50 keywords, run the first position check.

**Surfaces used:** Project API.
**Plan cost:** 1 Site + 50 Keywords from the user's subscription.
**Credits:** 0 (Project API).

### MCP-tool-call sequence

```text
1. PROJECT_listProjects             // confirm the project doesn't already exist
2. PROJECT_createProject            // domain="acme.com", name="ACME Rank Tracker"
3. PROJECT_addSearchEngine          // project_id=<from #2>, country_code="us"
4. PROJECT_addKeywords              // project_id=<from #2>, keywords=[...50 strings]
5. PROJECT_runPositionCheck         // project_id=<from #2>
6. PROJECT_getPositionHistory       // project_id=<from #2>  (poll until ready)
```

### Python equivalent

```python
import os, time, requests

API_KEY = os.environ["SERANKING_API_KEY"]
HEADERS = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}
BASE = "https://api.seranking.com/v1"

DOMAIN = "acme.com"
NAME = "ACME Rank Tracker"
COUNTRY = "us"
KEYWORDS = ["seo software", "rank tracker", ...]  # 50 total

project = requests.post(f"{BASE}/projects", json={"domain": DOMAIN, "name": NAME}, headers=HEADERS).json()
project_id = project["id"]

requests.post(f"{BASE}/projects/{project_id}/search-engines", json={"country_code": COUNTRY}, headers=HEADERS)

requests.post(
    f"{BASE}/projects/{project_id}/keywords",
    json={"keywords": KEYWORDS},
    headers=HEADERS,
)

requests.post(f"{BASE}/projects/{project_id}/positions/check", headers=HEADERS)

# Position checks are async — poll
for _ in range(20):
    r = requests.get(f"{BASE}/projects/{project_id}/positions/history", headers=HEADERS)
    if r.json().get("ready"):
        positions = r.json()
        break
    time.sleep(15)
```

### When to use

User says: "set up rank tracking for X", "create a new project for client Y", "I want to monitor positions for these keywords".

### Variants

- **Local rank tracking.** Add a region: call `PROJECT_getAvailableRegions` first, then pass `region_name` (verbatim from the response, no abbreviations) to `PROJECT_addSearchEngine`.
- **Multiple search engines.** Loop `PROJECT_addSearchEngine` per `country_code`. Each one is independent — rank checks run in parallel.
- **Tagged keyword groups.** After `PROJECT_addKeywords`, use `PROJECT_createKeywordGroup` + `PROJECT_moveKeywordsToGroup` to organise.

## Pattern 2 — Bulk backlink export to BigQuery / S3 (Data API)

**Goal:** pull every backlink for a list of 250 domains and ship the rows to BigQuery for analysis.

**Surfaces used:** Data API only.
**Credits:** ~75,000 (25,000 for 250 summaries + 50,000 for one full domain export; multi-domain exports scale linearly).
**Plan cost:** 0.

### Sequence

```text
1. DATA_getCreditBalance                    // confirm budget
2. for each domain:
     DATA_getBacklinksSummary               // 100 credits / domain
3. DATA_exportBacklinksData                 // 1 credit per backlink record returned (per domain)
4. DATA_getBacklinksExportStatus            // 0 credits / call; poll
5. (when ready) fetch the result URL        // 0 credits
```

### Python skeleton

```python
import requests, time, json
from google.cloud import bigquery

DOMAINS = [...]  # 250 entries

bq = bigquery.Client()
table = bq.dataset("seo").table("backlinks")

for domain in DOMAINS:
    summary = client.get("/backlinks/summary", params={"target": domain}).json()
    bq.insert_rows_json(table, [summary])

    task = client.post("/backlinks/export", json={"target": domain}).json()
    task_id = task["task_id"]

    while True:
        status = client.get(f"/backlinks/export/status", params={"task_id": task_id}).json()
        if status["status"] == "done":
            rows = requests.get(status["result_url"]).json()
            bq.insert_rows_json(table, rows)
            break
        time.sleep(15)
```

(See `references/rate-limits-and-credits.md` for the `client` wrapper — it handles 429 + 403 + throttling.)

### When to use

User says: "export all backlinks for X", "ship backlinks to {warehouse}", "I need a daily/weekly backlink delta job".

### Variants

- **Incremental (delta) export.** Use `DATA_listNewLostBacklinks` instead of full export — much cheaper for daily jobs.
- **Filter at request time.** Pass `min_authority`, `dofollow_only`, `anchor_contains` to reduce both data volume and credit cost.
- **For ref domains instead of links.** Same shape with `DATA_getBacklinksRefDomains` → `DATA_listNewLostReferringDomains`.

## Pattern 3 — Audit pipeline (Project API + Data API hybrid)

**Goal:** stand up an ongoing audit for a project, then pull the latest report into a Slack alert.

**Surfaces used:** both.
**Credits:** 0 (audit lives on Project API).
**Plan cost:** Audit Pages quota (depends on crawl scope).

### Sequence

```text
1. PROJECT_listProjects                    // resolve project_id
2. PROJECT_getAuditSettings                // confirm current crawl scope
3. PROJECT_updateAuditSettings             // optional — tune scope
4. PROJECT_createAudit                     // kicks off crawl
5. PROJECT_getAuditStatus                  // poll until "completed"
6. PROJECT_getAuditReport                  // top-level summary
7. PROJECT_getIssuesByUrl                  // per-URL issue list
8. (optional) DATA_getDomainAuthority      // contextual signal for severity ranking
9. Slack webhook                            // emit alert
```

### Slack-alert TS skeleton

```typescript
const project = (await client.get(`/projects/list`)).find(p => p.domain === DOMAIN);

await client.post(`/projects/${project.id}/audits/create`);

let status = "pending";
while (status !== "completed") {
  await sleep(60_000);
  status = (await client.get(`/projects/${project.id}/audits/status`)).status;
}

const report = await client.get(`/projects/${project.id}/audits/report`);
const critical = report.issues.filter(i => i.severity === "critical");

if (critical.length > 0) {
  await fetch(SLACK_WEBHOOK, {
    method: "POST",
    body: JSON.stringify({
      text: `⚠️ ${critical.length} critical SEO issues on ${DOMAIN}:\n${critical.map(i => `- ${i.title}`).join("\n")}`,
    }),
  });
}
```

### When to use

User says: "set up site auditing for X", "alert me when audit issues appear", "build an audit pipeline".

### Variants

- **One-off audit (no project).** Use `DATA_createStandardAudit` / `DATA_createAdvancedAudit` instead — fits when there's no Project API access or no need for ongoing tracking.
- **Compare against last week.** Hold the previous `audit_id`; diff `PROJECT_getAuditReport` summaries to detect new/resolved issues.

## Pattern 4 — AIRT visibility tracker (Project API)

**Goal:** track how often a brand appears in answers across ChatGPT / Gemini / Perplexity for a curated prompt set.

**Surfaces used:** Project API (with optional `DATA_getAiSearch*` for cross-domain comparison).
**Credits:** 0 (AIRT is plan-billed).
**Plan cost:** N AIRT Prompts from subscription.

### Sequence

```text
1. PROJECT_listProjects                  // resolve project_id
2. PROJECT_listLlmEngines                // confirm engines available
3. (optional) PROJECT_createLlmEngine    // if a custom engine is needed
4. PROJECT_createPromptGroup             // group the prompts logically
5. PROJECT_addPrompts                    // attach 20–50 prompts
6. PROJECT_getLlmStatus                  // poll — answers refresh on a schedule
7. PROJECT_getPromptAnswer (per prompt)   // current top-N answers
8. PROJECT_getPromptsRankings             // brand mention positions across the group
```

### When to use

User says: "track brand mentions in LLMs", "AIRT setup", "AI Result Tracker prompts for X", "build LLM visibility dashboard".

### Variants

- **Cross-domain competitive view.** Pair with `DATA_getAiSearchLeaderboard` + `DATA_getAiSearchOverview` for a benchmark against domains you don't own.
- **Per-engine breakdown.** Call `PROJECT_getLlmStatistics` filtered by engine_id for an engine-by-engine heatmap.

## Pattern 5 — Keyword research bulk job (Data API)

**Goal:** for a list of seed keywords, expand each into related / similar / longtail / question keywords, write the merged result to a CSV.

**Surfaces used:** Data API only.
**Credits:** ~1–5 per keyword expanded (varies by tool).
**Plan cost:** 0.

### Sequence

```text
for each seed:
  DATA_getRelatedKeywords
  DATA_getSimilarKeywords
  DATA_getLongTailKeywords
  DATA_getKeywordQuestions
merge + dedupe
write to CSV
```

### Python skeleton

```python
import csv, itertools

SEEDS = [...]  # e.g., 20 seed keywords
COUNTRY = "us"

rows = []
for seed in SEEDS:
    rel = client.get("/keywords/related", params={"keyword": seed, "source": COUNTRY}).json()
    sim = client.get("/keywords/similar", params={"keyword": seed, "source": COUNTRY}).json()
    long = client.get("/keywords/longtail", params={"keyword": seed, "source": COUNTRY}).json()
    qst = client.get("/keywords/questions", params={"keyword": seed, "source": COUNTRY}).json()

    for kw in itertools.chain(rel, sim, long, qst):
        rows.append({**kw, "source_seed": seed})

# Dedupe by keyword
unique = {row["keyword"]: row for row in rows}.values()

with open("keywords.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["keyword", "volume", "kd", "intent", "source_seed"])
    writer.writeheader()
    writer.writerows(unique)
```

### When to use

User says: "expand these seeds", "bulk keyword research", "build a keyword list for X", "I have 20 seeds, give me 2000 keywords".

### Variants

- **By intent.** Filter on `intent` in the response: keep only `informational` + `commercial` for content briefs.
- **By KD ceiling.** Filter `kd <= 30` for new domains to skip the impossible-to-rank keywords.
- **Cluster after expansion.** Pipe the merged CSV into `seo-keyword-cluster` for pillar-and-spoke structure.

## Composing patterns

Real integrations chain these. Common compositions:

| Goal | Patterns chained |
|---|---|
| "Weekly client SEO report" | Pattern 1 (one-time setup) → Pattern 3 (recurring audit) + `PROJECT_getPositionHistory` + Pattern 2 trim (delta backlinks) |
| "Find the highest-value new content opportunities" | Pattern 5 → `seo-keyword-cluster` → `seo-content-brief` |
| "AI Search competitive intelligence" | Pattern 4 → `seo-ai-search-share-of-voice` |
| "Outreach prospecting" | Pattern 2 (variant: ref domains) → competitor diff → outreach CSV |

When the user's goal spans more than one pattern, the `seo-api` skill writes them all as numbered sections inside `RECIPE.md` and emits separate `code/` files per language for the combined flow.
