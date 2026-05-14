# 06 — Paid-keyword gap (vs competitors, type=adv)

Tool: mcp__claude_ai_SE_Ranking__DATA_getDomainKeywords (with type=adv) and mcp__claude_ai_SE_Ranking__DATA_getDomainKeywordsComparison (with type=adv, diff=1)

Status: SE Ranking MCP auth unavailable in this session. Re-run with auth to populate.

User-supplied competitors for this run: bluehost.com, godaddy.com, siteground.com.

Per SKILL.md step 7, the paid-keyword gap is computed as:
1. DATA_getDomainKeywords(domain=hostinger.com, type=adv) -> Hostinger's paid keyword set
2. DATA_getDomainKeywords(domain=bluehost.com, type=adv) -> Bluehost's paid set
3. DATA_getDomainKeywords(domain=godaddy.com, type=adv) -> GoDaddy's paid set
4. DATA_getDomainKeywords(domain=siteground.com, type=adv) -> SiteGround's paid set
5. Diff each competitor's paid set against Hostinger's -> per-competitor paid-gap lists
6. Intersect the per-competitor gap lists to find keywords ALL competitors bid on but Hostinger doesn't (highest-priority gap)

Qualitative anticipation (re-confirm with SE Ranking):
- "wordpress hosting" — Bluehost owns this paid SERP historically; Hostinger likely under-invests.
- "dedicated server hosting" — GoDaddy + SiteGround compete at premium tier; Hostinger may not bid there.
- "managed wordpress" — SiteGround's strength; gap potential for Hostinger.
- Brand-defense terms ("bluehost vs hostinger", "godaddy vs hostinger", "siteground review") — competitors bid on Hostinger's brand; Hostinger should bid defensively on theirs.

The intersection of per-competitor gaps gives the highest-leverage shortlist; the union surfaces longer-tail experiments. See ADS.md "Recommended bid-keyword shortlist" for the qualitative top 5.
