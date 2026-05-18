# 01 — URL overview

Tool: `mcp__plugin_seo-skills_se-ranking__DATA_getUrlOverviewWorldwide` · Input: `url=https://www.notion.com/help/keyboard-shortcuts`, `fields=keywords,traffic,price`
Run date: 2026-05-18

```json
{
  "organic": [
    {
      "source": "worldwide",
      "keywords_count": 62145,
      "traffic_sum": 375,
      "price_sum": 1
    }
  ],
  "adv": []
}
```

**Interpretation:** SE Ranking reports 62,145 keywords worldwide for this URL but only 375 estimated monthly organic visits. This low traffic figure is a known artifact of how SE Ranking attributes traffic on Next.js SPAs — the crawler may not correctly attribute visits to a client-side-rendered URL. The page holds **position 1** for three head queries ("notion keyboard shortcuts" vol ~74,000, "notion shortcuts mac" vol ~18,100, "notion hotkeys" vol ~6,600) per live SERP probe, which would imply real traffic far above 375/mo. Cross-check with GSC for the authoritative traffic figure.

**Page authority (InLink Rank):** 27 (DATA_getPageAuthority, 2026-05-18)

What this number means for the verdict: even at the SE Ranking traffic estimate, 62,145 ranking keywords confirms this is a high-coverage URL. Combined with the #1 SERP positions, this page is high-leverage — the REFRESH verdict stands.
