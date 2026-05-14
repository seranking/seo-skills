# 02 — Keyword churn (top-100)

Tool: mcp__claude_ai_SE_Ranking__DATA_getDomainKeywords · Input: domain=wix.com, source=us, limit=100, order_field=position, order_type=asc — at baseline date AND at current date

Status: SE Ranking MCP auth unavailable in this session. Re-run with auth to populate.

Per SKILL.md compare mode step 3: top-100 keyword churn — any high-volume drop = red.

Computation:
1. Pull top-100 ranking keywords today.
2. Pull top-100 from the baseline snapshot (or DATA_getDomainKeywords with a back-dated equivalent — note: SE Ranking history endpoints have monthly granularity).
3. Set-diff: keywords in baseline-100 but not in current-100 = drops. Keywords in current-100 but not in baseline-100 = gains.
4. For each drop, fetch current position (if 11-50 = soft drop, if 51+ = hard drop, if missing entirely = lost ranking).

The output structure that re-run with auth would produce:

```
DROPPED OUT OF TOP 100:
  - "<keyword>" (was position N at baseline -> position M today)

NEW IN TOP 100:
  - "<keyword>" (no prior rank -> position N today)
```

Wix-specific qualitative expectation (no quantitative substitute for SE Ranking): the share-of-voice example shows Wix dominates "free website builder" + "free portfolio website" + "logo design" + "small business website" clusters. Any churn that drops a keyword from one of those clusters out of the top 100 is RED-tier and warrants immediate investigation.
