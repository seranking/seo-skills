# Execution log — 2026-05-22

Read-only smoke-test run. No mutating calls. No account state created or modified.

| # | Tool | Args | Result |
|---|------|------|--------|
| 1 | `DATA_getCreditBalance` | — | 200 · `{limit: 101,323,444, used: 19,916,982}` |
| 2 | `DATA_getSubscription` | — | 200 · status active, units_left 90,055,398 |
| 3 | `PROJECT_listProjects` | — | 200 · 22 projects (Project API access confirmed) |
| 4 | `DATA_getDomainOverviewWorldwide` | `domain=seranking.com` | 200 · organic + adv blocks |
| 5 | `DATA_getDomainCompetitors` | `domain=seranking.com, source=us` | 200 · 371 rows — **exceeded MCP 60KB token limit**, auto-saved to file, read via `jq` |
| 6 | `DATA_getBacklinksSummary` | `target=seranking.com, mode=domain` | 200 · full summary |
| 7 | `DATA_getCreditBalance` | — | 200 · `{used: 19,915,682}` (moved −1,300 vs #1 — concurrent activity on the shared key) |
| 8 | `DATA_getSubscription` | — | 200 · units_left 90,056,698 (moved +1,300 vs #2) |

All calls returned HTTP 200. One transport-level caveat: step 5 overflowed the MCP client's inline token limit and was auto-saved to disk — recovered with a `jq` slice (see `../code/mcp-calls.md`). The raw REST endpoint has no such limit.
