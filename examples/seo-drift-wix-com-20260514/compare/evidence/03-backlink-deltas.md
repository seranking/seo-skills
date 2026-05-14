# 03 — Backlink deltas

Tools: mcp__claude_ai_SE_Ranking__DATA_getNewLostBacklinksCount + DATA_listNewLostBacklinks + DATA_getNewLostRefDomainsCount + DATA_listNewLostReferringDomains

Status: SE Ranking MCP auth unavailable in this session. Re-run with auth to populate.

Per SKILL.md compare mode step 3: net referring domains -5 to -20 = yellow, <-20 = red.

The four endpoints listed return:
- Total counts of new vs lost backlinks in the window
- Per-link details for both lists
- Same for referring domains

For a category leader like Wix.com (qualitative — see SoV example), the expected absolute volume of new+lost backlinks across a 90-day window is large (~1000s of links). What matters is the NET: net referring-domains delta normalised to baseline-domain-count.

Wix-specific qualitative caveat: many of Wix's "backlinks" are user-built sites on wix.com subdomains and the wixsite.com infrastructure. A drop in referring-domain count tied to a template change or a deprecated subdomain pattern is a known false-positive signal that doesn't warrant action.

Re-run with auth, then qualitatively filter the lost-link list for that pattern before treating the YELLOW/RED severity as actionable.
