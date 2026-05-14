# 03 — Question-intent variants

Tool: mcp__claude_ai_SE_Ranking__DATA_getKeywordQuestions · Input: keyword=<each head term>, source=us, limit=100

Status: SE Ranking MCP auth unavailable in this session. Re-run with auth to populate.

Live SERP probes (Firecrawl, 2026-05-14) surfaced these recurring question-intent patterns in the SERPs we sampled:
- "Is Hostinger a good web hosting provider?" — Reddit thread surfaces in top 3 for "hostinger web hosting" probe.
- "Hostinger Review 2026 - Is it Actually Good?" — YouTube review surfaces in top 5.

Pattern: question-intent variants in the hosting category tend to cluster around brand-defense ("is X good", "X review"). These are cheap-CPC, high-conversion plays per SKILL.md tip #6 — they catch users mid-evaluation.

Suggested SE Ranking probe queries:
- DATA_getKeywordQuestions on "wordpress hosting" — surface "how to set up wordpress hosting", "best wordpress hosting for beginners", etc.
- DATA_getKeywordQuestions on "vps hosting" — surface "what is vps hosting", "vps vs dedicated", etc.
- DATA_getKeywordQuestions on "hostinger" — surface brand-defense variants.
