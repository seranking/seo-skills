# 05 — Feature matrix: Linear vs Jira

> Inferred from the top 3 SERP winners for "linear vs jira" plus the live pricing/feature pages for each product. Use this as the load-bearing reference for the PM/writer. Cells marked "TBD — confirm with PM" should not be published until verified.

## Reading

The feature matrix in `COMPARISON.md` is a curated subset for conversion. This file is the full grid — useful for the writer to (a) pull additional rows into the comparison if commercial says so, (b) tighten or correct cells before publishing, and (c) maintain the comparison as both products evolve.

## Full feature matrix

| Dimension | Linear | Jira | Source / confidence |
|---|---|---|---|
| **Pricing** | | | |
| Free tier | Yes — 2 teams, 250 issues, unlimited members | Yes — up to 10 users | High (both pricing pages) |
| Paid entry tier | $10/user/mo (Basic, annual) | $7.53/user/mo (Standard, typical) | High for Linear; Jira regional pricing varies — confirm |
| Mid tier | $16/user/mo (Business) | $13.53/user/mo (Premium) | High for Linear; Jira regional varies |
| Enterprise tier | Custom | Custom | High |
| Annual billing required for paid | Yes (Basic/Business/Enterprise) | No (monthly available on most plans) | High |
| **Issue tracking** | | | |
| Issues with state machine | Yes (Backlog → Todo → In Progress → Done) | Yes (fully customisable workflow) | High |
| Custom issue types | Limited (Story / Bug / Feature / Improvement) | Yes (unlimited) | High |
| Custom fields | Limited | Yes (unlimited) | High |
| Bulk edit | Yes | Yes | High |
| **Workflows** | | | |
| Cycles / sprints | Cycles (native) | Sprints (native) | High |
| Custom workflow states | Limited (per-team config) | Yes (no-code workflow editor) | High |
| Multi-step approvals | Limited | Yes (via custom workflow) | High |
| Automation rules | Yes (Business+) | Yes (built into Standard+) | High |
| **Planning** | | | |
| Roadmaps | Native (Linear Plan) | Native (Advanced Roadmaps in Premium) | High |
| Initiatives | Yes | Yes (via Premium Advanced Roadmaps) | Medium — verify Premium tier |
| Goals | Yes | Yes | High |
| Cross-team dependencies | Yes | Yes | High |
| **AI** | | | |
| AI agent (in-product) | Linear Agent (beta), included | Rovo (separate add-on, per-seat fee) | High |
| AI ticket auto-routing | Triage Intelligence (Business+) | Rovo Triage | High |
| AI-drafted PRDs | Linear Agent | Rovo + Confluence integration | High |
| MCP / external AI tool access | Native MCP server | Native MCP server | High |
| **Integrations** | | | |
| Slack | Yes | Yes | High |
| GitHub | Yes (deep — branch/PR sync, auto-status) | Yes (via Smart Commits + integration) | High |
| GitLab | Yes | Yes | High |
| Figma | Yes | Yes | High |
| Confluence | Via export/embed | Native (Atlassian) | High |
| Bitbucket | No native (third-party only) | Native (Atlassian) | High |
| Zendesk | Yes (Business+) | Yes | High |
| Intercom | Yes (Business+) | Yes | High |
| Salesforce | Yes | Yes | High |
| Total directory size | ~100 | 3,000+ | High |
| **Reporting** | | | |
| Built-in dashboards | Yes (Linear Insights, Business+) | Yes (Standard+) | High |
| Custom query language | None published (UI filters) | JQL | High |
| Burndown / velocity | Yes | Yes (with sprint setup) | High |
| Cycle reports | Yes | Yes (sprint reports) | High |
| **Admin / security** | | | |
| SAML SSO | Yes (Enterprise) | Yes (Premium+) | High |
| SCIM | Yes (Enterprise) | Yes (Premium+) | High |
| Audit logs | Yes (Business+ for basic, Enterprise for full) | Yes (Premium+) | High |
| Granular role-based access | Yes (Business+ for guests/private teams, Enterprise for advanced) | Yes (granular permissions, all paid tiers) | High |
| Data residency options | Yes (Enterprise) | Yes (Premium+) | Medium — confirm |
| **Support** | | | |
| Email support | All paid | All paid | High |
| Priority support | Enterprise | Premium (24/7) + Enterprise | High |
| Dedicated account team | Enterprise | Enterprise | High |
| **Best for (positioning)** | | | |
| Engineering teams | Strong fit (designed for) | Good fit (Scrum/Kanban templates) | High |
| Product teams | Strong fit | Good fit | High |
| Design teams | Strong fit (Linear Insights, Asks) | Average | Medium |
| Cross-functional / marketing | Average | Strong (Jira Work Management for non-software) | High |
| Large enterprise (1k+ employees) | Emerging | Strong (10+ years of enterprise) | High |
| ITSM / IT support tickets | Not designed for | Yes (Jira Service Management — separate product) | High |

## Conflicts / cells to verify before publishing

1. **Jira Standard / Premium per-seat:** Atlassian Cloud pricing varies by region and seat-count tier. The $7.53 / $13.53 figures are widely-cited mid-2025 values for a small-team configuration — confirm against current pricing for the target audience's region.
2. **Linear integration count:** "~100" is a rough estimate from Linear's published integration directory. Count is approximate — confirm with Linear's actual directory at time of publishing.
3. **Jira free-tier seat cap:** Atlassian has experimented with raising the free seat cap; cell currently says 10 users (long-standing default). Verify if cap has been raised since 2024.
4. **Rovo pricing:** Cell says "separate add-on, per-seat fee" — confirm the current add-on model and pricing before publishing. Atlassian's AI pricing has evolved through 2024–2026.

## Cells the writer should NOT change without source

- Free-tier seat policies (load-bearing for the FAQ + verdict)
- "Built for / Best for" positioning (this is the narrative spine)
- AI agent rows (the AI differentiation is the strongest current differentiator)
