# 04 — SERP ad / shopping pack inventory

Tool: mcp__claude_ai_SE_Ranking__DATA_getSerpResults · Input: keyword=<each top term>, source=us, filter_serp_features=tads,bads,sads,mads,paa,image_pack

Status: SE Ranking MCP auth unavailable in this session. Re-run with auth to populate.

Per SKILL.md step 5, SERP-feature filters to apply:
- tads = top ads above organic (positions 1-4)
- bads = bottom ads below organic (positions 1-3)
- sads = shopping ads / Google Shopping pack
- mads = mobile/map-pack ads

For web hosting keywords, expected pattern (qualitative, awaiting confirmation):
- Shopping pack: typically absent (service, not retail product).
- Map pack: typically absent (national service, not local).
- Top ads (tads): typically dense — 3-4 advertisers compete for above-organic positions.
- Bottom ads (bads): typically present — Hostinger, GoDaddy, Bluehost often appear here too.
- PAA: typically present for "what is web hosting", "how to choose web hosting".
- Image pack: typically absent.

The tads/bads split matters because top-ad CPC is 2-3x the bottom-ad CPC for the same keyword. The recommended bid-keyword shortlist in ADS.md should target positions 1-3 (tads) for head terms and positions 5-7 (bads, organic-influenced visibility) for longtails.
