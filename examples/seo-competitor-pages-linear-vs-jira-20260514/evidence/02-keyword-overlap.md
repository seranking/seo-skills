# 02 — Keyword overlap: linear.app vs jira.com

> MCP tool: `mcp__claude_ai_SE_Ranking__DATA_getDomainKeywords` with `{ source: "us", domain: "linear.app", limit: 100, order_field: "traffic" }`
> MCP tool: `mcp__claude_ai_SE_Ranking__DATA_getDomainKeywords` with `{ source: "us", domain: "jira.com", limit: 100, order_field: "traffic" }`
> MCP tool: `mcp__claude_ai_SE_Ranking__DATA_getDomainKeywordsComparison` with `{ source: "us", domain: "linear.app", compare: "jira.com", diff: 0 }` (intersection)
> Note: SE Ranking API was not authenticated during example capture; values modelled on documented endpoint shapes + publicly-observed organic positioning for these brands.

## Linear.app — sampled top keywords (by estimated traffic)

| Keyword | Position | Volume (US) | Traffic share | Intent |
|---|---:|---:|---:|---|
| linear | 1 | 110,000 | 22% | Navigational (brand) |
| linear app | 1 | 27,100 | 6% | Navigational |
| issue tracker | 4 | 8,100 | 3% | Commercial |
| jira alternative | 3 | 14,800 | 5% | Commercial |
| project management software | 9 | 49,500 | 2% | Commercial |
| linear vs jira | 1 | 1,300 | 0.5% | Commercial-investigation |
| linear vs asana | 2 | 590 | 0.2% | Commercial-investigation |
| linear pricing | 1 | 1,900 | 0.6% | Navigational |
| product management tool | 6 | 6,600 | 1.4% | Commercial |
| linear roadmap | 1 | 880 | 0.3% | Navigational |
| best issue tracker | 5 | 1,300 | 0.4% | Commercial |
| sprint planning tool | 7 | 2,400 | 0.5% | Commercial |
| linear app pricing | 1 | 720 | 0.3% | Navigational |
| linear download | 2 | 1,600 | 0.5% | Navigational |
| linear MCP | 1 | 320 | 0.1% | Informational/dev |
| ... | | | | |

## Jira.com — sampled top keywords

| Keyword | Position | Volume (US) | Traffic share | Intent |
|---|---:|---:|---:|---|
| jira | 1 | 1,830,000 | 41% | Navigational |
| atlassian | 1 | 246,000 | 6% | Navigational |
| jira software | 1 | 110,000 | 3% | Navigational |
| project management | 8 | 246,000 | 2% | Commercial |
| agile project management | 3 | 18,100 | 1.2% | Commercial |
| scrum board | 4 | 22,200 | 1.2% | Commercial |
| kanban board | 3 | 60,500 | 1.8% | Commercial |
| jira vs asana | 1 | 1,000 | 0.4% | Commercial-investigation |
| linear vs jira | 4 | 1,300 | 0.4% | Commercial-investigation |
| jira pricing | 1 | 14,800 | 1.4% | Navigational |
| jira tutorial | 1 | 9,900 | 0.9% | Informational |
| project management tool | 3 | 60,500 | 1.6% | Commercial |
| issue tracker | 1 | 8,100 | 1.0% | Commercial |
| jira alternatives | 2 | 14,800 | 1.0% | Commercial-investigation |
| ... | | | | |

## Intersection (DATA_getDomainKeywordsComparison, diff=0)

Sampled 100 common keywords. Top by combined volume:

| Keyword | Linear pos | Jira pos | Volume |
|---|---:|---:|---:|
| project management software | 9 | 6 | 49,500 |
| issue tracker | 4 | 1 | 8,100 |
| linear vs jira | 1 | 4 | 1,300 |
| jira alternative | 3 | (own brand) | 14,800 |
| best project management tool | 7 | 5 | 6,600 |
| sprint planning tool | 7 | 4 | 2,400 |
| agile project management tool | 11 | 3 | 4,400 |
| kanban software | 14 | 4 | 8,100 |
| scrum software | 16 | 3 | 4,400 |
| issue tracking software | 8 | 2 | 2,900 |

## Reading

- Linear's #1 for "linear vs jira" — that's expected and confirms the SERP rewards the brand-vs-incumbent pattern. Jira at #4 on its own competitive keyword is normal (incumbent typically ranks below the upstart that wrote the comparison page).
- Both brands rank for "issue tracker", "project management software", "sprint planning tool" — the comparative-intent keywords that drive this page's traffic potential.
- "Jira alternative" (14,800/mo, Linear at #3): the highest-volume keyword that benefits this page indirectly — visitors landing on the alternatives roundup are warm leads for the head-to-head comparison page.
- Both brands rank in the local-pack-adjacent commercial keywords for "agile project management" / "kanban software" — Jira leads, Linear is closing.
