# Rate Limits & Credits

Everything the `seo-api` skill needs to forecast cost and pace requests against the Data API and Project API.

## Rate limits

**Per API key, not per IP.** All threads, workers, and servers sharing one key contribute to the same RPS budget. For production fan-outs, mint multiple keys via the API Dashboard.

| API | Standard limit | Trial accounts |
|---|---|---|
| Data API | **10 requests per second** | 1 RPS (can be raised on request — email api@seranking.com) |
| Project API | **5 requests per second** | 1 RPS (same path to raise) |

**Async operations.** Endpoints like `/backlinks/export` create a task; subsequent polls of `*ExportStatus` count against the same RPS budget (but cost 0 credits).

**Custom limits.** Production workloads needing higher throughput: contact `api@seranking.com`. Custom plans are available.

## Handling 429 — exponential backoff with jitter

```python
import random, time, requests

def call(url, headers, max_attempts=5):
    delay = 1.0
    for attempt in range(max_attempts):
        r = requests.get(url, headers=headers)
        if r.status_code != 429:
            return r
        jitter = random.uniform(-0.2, 0.2) * delay
        time.sleep(delay + jitter)
        delay *= 2
    r.raise_for_status()
```

```typescript
async function call(url: string, headers: HeadersInit, maxAttempts = 5): Promise<Response> {
  let delay = 1000;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const r = await fetch(url, { headers });
    if (r.status !== 429) return r;
    const jitter = (Math.random() * 0.4 - 0.2) * delay;
    await new Promise((resolve) => setTimeout(resolve, delay + jitter));
    delay *= 2;
  }
  throw new Error(`Rate-limited after ${maxAttempts} attempts`);
}
```

**Why jitter matters.** Without it, multiple clients hitting the limit simultaneously synchronise their retries and re-hit the limit at the next interval — the thundering-herd problem. A ±20% randomisation spreads them out.

**Simple delays (use with caution).** Because the API uses a rolling 1s window, a brief pause (200–500ms) is enough for occasional, isolated overages. But it doesn't survive bursty traffic — use exponential backoff for anything production.

## Client-side throttling

Better than reactive 429 handling: proactively pace requests to stay under the limit.

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, rps: int):
        self.rps = rps
        self.calls = deque()

    def acquire(self):
        now = time.monotonic()
        while self.calls and self.calls[0] < now - 1.0:
            self.calls.popleft()
        if len(self.calls) >= self.rps:
            time.sleep(1.0 - (now - self.calls[0]))
        self.calls.append(time.monotonic())

limiter = RateLimiter(rps=10)
for url in urls:
    limiter.acquire()
    call(url, headers)
```

## Credit system (Data API)

Pay-as-you-go. Plans start at 1 million credits.

### Two billing models

1. **Cost per record** — credits charged per row returned. Example: `/backlinks/summary` at 100 credits/record, request 250 domains → 25,000 credits.
2. **Cost per request** — flat fee per successful call regardless of payload size. Example: `/keywords/research` at 5 credits/request, 1000 keywords returned → still 5 credits.

**Failed requests are free.** 4xx and 5xx never consume credits. Don't over-engineer error retries to "save credits".

### Reading current balance

```bash
curl -X GET 'https://api.seranking.com/v1/account/subscription' \
  -H 'Authorization: Token YOUR_API_KEY'
```

Or via MCP: `DATA_getCreditBalance` (0 credits, returns `units_left`).

Response shape:
```json
{
  "subscription_info": {
    "status": "active",
    "start_date": "2026-01-18 14:20:02",
    "expiration_date": "2027-01-18 14:20:02",
    "units_limit": 5000000,
    "units_left": 4975033
  }
}
```

### Forecasting

Before running a large workflow:

1. List every API call.
2. Multiply by per-call cost (see canonical table at <https://seranking.com/api/data/getting-started/#unit-costs>, or check each MCP tool's own description for the per-tool figure).
3. Sum.
4. Compare against `units_left`.

**Worked example.** Pull backlink summaries for 250 domains + full export for one:

| Call | Records | Per-record cost | Total |
|---|---|---|---|
| `/backlinks/summary` | 250 | 100 credits | 25,000 |
| `/backlinks/export` (task creation) | 50,000 (links in target domain) | 1 credit | 50,000 |
| `/backlinks/export/status` (poll 2×) | 2 | 0 credits/request | 0 |
| **Total** | | | **75,000 credits** |

### Insufficient credits — 403

```json
{
  "error": {
    "code": 403,
    "message": "Insufficient funds",
    "description": "Your current credit balance is too low to process this request."
  }
}
```

No partial billing — the entire request is rejected. Top up at the API Dashboard or contact `api@seranking.com` for overage billing.

## Plan limits (Project API)

The Project API doesn't use credits. It consumes the same limits as the SE Ranking web platform.

| Action | Limit consumed | When |
|---|---|---|
| `PROJECT_createProject` | 1 Site | On creation |
| `PROJECT_addKeywords` | N Keywords | Each new keyword tracked |
| `PROJECT_runPositionCheck` | (free — uses tracking schedule) | — |
| `PROJECT_addAuditSourcePages` + audit run | N Audit Pages | Per page crawled |
| `PROJECT_createAudit` (advanced) | Audit Pages × pages | Per crawl |
| `PROJECT_addPrompts` | N AIRT Prompts | Per prompt added to AIRT |
| `PROJECT_addCompetitor` | (free) | — |
| `PROJECT_addProjectBacklink` | (free — uses Backlinks tier) | — |

**Read the user's plan limits before mutating.** `PROJECT_getUserProfile` returns the current plan tier and remaining quota. If the integration would push a limit over, surface upfront and ask whether to proceed or downsize.

### Insufficient plan limits

```json
{
  "error": {
    "code": 403,
    "message": "Limit reached",
    "description": "Cannot add 50 keywords — you have 32 keywords remaining on the Pro plan."
  }
}
```

Fix paths:
- Upgrade plan: <https://seranking.com/subscription.html>.
- Free up quota: delete unused projects, keywords, AIRT prompts via the matching `PROJECT_delete*` tool.

## Per-endpoint cost cheat-sheet

The skill should never hardcode these — they're authoritative on the live MCP tool descriptions and the canonical table at <https://seranking.com/api/data/getting-started/#unit-costs>. Common ones for quick recall:

| Endpoint | MCP tool | Cost |
|---|---|---|
| Account subscription | `DATA_getSubscription` | 0 |
| Credit balance | `DATA_getCreditBalance` | 0 |
| Backlinks summary | `GetBacklinksSummary` | 100/record |
| Backlinks export (task) | `ExportBacklinksData` | 1/record |
| Backlinks export status | `GetBacklinksExportStatus` | 0/request |
| Domain overview | `GetDomainOverviewWorldwide` / `GetDomainOverviewDatabases` | 100/record |
| Domain keywords | `GetDomainKeywords` | 1/keyword |
| Domain competitors | `GetDomainCompetitors` | 1/competitor |
| Keyword research | `DATA_getRelatedKeywords` / `DATA_getSimilarKeywords` | varies (often 1/keyword) |
| Keyword overview | `DATA_getKeywordOverview` | 100/keyword |
| SERP task creation | `DATA_createSerpTask` | 1/keyword |
| SERP task results | `DATA_getSerpTaskResults` | 0 (already paid at task creation) |
| Website audit creation | `DATA_createStandardAudit` | varies by site size |
| Website audit report | `DATA_getAuditReport` | 0 |
| AI Search overview | `DATA_getAiSearchOverview` | varies |

**Always defer to the live tool description for the canonical figure.** SE Ranking updates costs periodically; the in-tool figure is the source of truth.

## Combined rate-limit + credit safety pattern

The end-to-end shape for any production integration:

```python
import time, random, requests

API_KEY = os.environ["SERANKING_API_KEY"]
HEADERS = {"Authorization": f"Token {API_KEY}"}
BASE = "https://api.seranking.com/v1"

class SERankingClient:
    def __init__(self, rps=10):
        self.rps = rps
        self.calls = deque()

    def _throttle(self):
        now = time.monotonic()
        while self.calls and self.calls[0] < now - 1.0:
            self.calls.popleft()
        if len(self.calls) >= self.rps:
            time.sleep(1.0 - (now - self.calls[0]))
        self.calls.append(time.monotonic())

    def get(self, path, params=None, max_attempts=5):
        delay = 1.0
        for attempt in range(max_attempts):
            self._throttle()
            r = requests.get(f"{BASE}{path}", headers=HEADERS, params=params)
            if r.status_code == 429:
                time.sleep(delay + random.uniform(-0.2, 0.2) * delay)
                delay *= 2
                continue
            if r.status_code == 403 and "Insufficient funds" in r.text:
                raise RuntimeError("Out of credits — top up before retrying.")
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"Rate-limited after {max_attempts} attempts on {path}")
```

This handles the common cases: rate-limit pacing, exponential backoff with jitter, terminal 403, transient 5xx. Tune `rps` to match the API (5 for Project, 10 for Data).
