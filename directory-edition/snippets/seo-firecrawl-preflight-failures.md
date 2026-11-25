| Failure | Detection | Skill response |
|---|---|---|
| Credit balance call fails | `DATA_getSubscription` returns error or non-200 | Note "SE Ranking credit balance unavailable — proceeding without preflight cost estimate; surface actual cost in deliverable" and continue. **Never** fail the run on this — credit data is a courtesy, not a gate. |
| Credit balance below estimate | `remaining < estimated_cost` | Surface the shortfall; ask the user whether to proceed with a reduced scope (e.g. lower URL cap, lite mode) or top up credits before re-running. |
| Firecrawl connector not connected | Firecrawl's `firecrawl_scrape` tool not in available tools | Note "Firecrawl not connected — degraded path active; connect the Firecrawl connector from the Claude directory" and run the WebFetch-only path. |
| Firecrawl rate-limit hit | Firecrawl response 429 | Note "Firecrawl rate-limit reached — falling back to WebFetch for remaining URLs" and continue degraded for the rest of the run. Do not retry in a tight loop. |
| Firecrawl Cloudflare/anti-bot block | Firecrawl response 403 / "blocked by WAF" | Note the affected URL and the block reason in the deliverable, then continue. Defeating WAFs is out of scope. |
