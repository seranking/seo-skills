# Recommended sitemap diff

## Change 1 — Add `<lastmod>` to every URL (REQUIRED)

### Before (current)

```xml
<url>
  <loc>https://www.notion.com/blog</loc>
  <priority>0.5</priority>
  <changefreq>weekly</changefreq>
</url>
```

### After

```xml
<url>
  <loc>https://www.notion.com/blog</loc>
  <lastmod>2026-05-12T00:00:00+00:00</lastmod>
</url>
```

The `<lastmod>` value should come from the CMS — the page's last-edit timestamp in ISO 8601 format with offset. Use the deploy timestamp of the page template for static pages with no edit history (signup, login).

### Why drop `<priority>` and `<changefreq>` simultaneously

Both are explicitly ignored by Google ([source: developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)). Keeping them inflates file size with zero signal. Removing alongside the lastmod fix is one CMS / sitemap-generator commit.

## Change 2 — Consolidate (optional)

Combine very-low-traffic locale-prefixed sub-sitemaps where the localised content is < 50 URLs. A 19-locale × 10-content-type fan-out is fine; pruning empty leaves keeps the file index lean.

This is a sitemap-generator config change, not an XML edit per file.

## Change 3 — Validate post-deploy (REQUIRED)

After the lastmod fix lands, re-fetch:

```
https://www.notion.com/sitemap.xml
https://www.notion.com/sitemap-root.xml
https://www.notion.com/blog/sitemap.xml
https://www.notion.com/help/sitemap.xml
https://www.notion.com/customers/sitemap.xml
```

Spot-check 10 URL entries from each to confirm `<lastmod>` is populated, ISO 8601, and matches the CMS edit timestamp.

## Out of scope (defer to `seo-technical-audit`)

- Missing-from-sitemap URLs — requires a full audit crawl.
- Orphans-from-sitemap URLs — requires internal-link analysis.
- Broken sitemap entries (status 404 / 410) — requires per-URL HEAD check across ~7,000+ entries.
