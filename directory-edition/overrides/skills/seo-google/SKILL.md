---
name: seo-google
description: Google's own SEO data (Search Console clicks, impressions and URL Inspection, PageSpeed Insights, CrUX field data, Indexing API, GA4 organic traffic, YouTube, NLP, Keyword Planner) comes from local Python scripts that are not part of the Claude Plugins Directory edition of these skills. This skill tells the user how to get them and what SE Ranking data can stand in. Use when the user asks for "search console", "GSC", "PageSpeed", "CrUX", "field data", "indexing API", "GA4 organic", "URL inspection", "real CWV data", "impressions", "clicks", "CTR", "position data", "keyword planner", or "real google data".
---

# Google SEO APIs (not in this edition)

The full `seo-google` skill pulls first-party Google data: Search Console performance and URL Inspection, CrUX field data with 25-week history, PageSpeed Insights, the Indexing API, GA4 organic traffic, YouTube search, Google NLP and Keyword Planner. It runs local Python scripts with the user's own Google Cloud credentials. The Claude Plugins Directory edition ships skills only, so those scripts are not here.

## What to do

1. Tell the user plainly that real Google data needs the full edition of these skills from GitHub: https://github.com/seranking/seo-skills (its README, install option 3, sets up the scripts and the Google credentials).
2. Offer what this edition can answer with SE Ranking data instead:
   - Rankings, traffic estimates and SERP features for a page or domain: `seo-page`, `seo-keyword-niche`, or `DATA_getDomainKeywords`.
   - Search volume, keyword difficulty and CPC: `DATA_getKeywordsMetrics`.
   - Lab performance, crawl and indexability issues from a site audit: `seo-technical-audit`.
3. Don't ask for Google API keys, service-account files or OAuth tokens, and don't try to reach Google APIs another way.
