# URLs — stripe.com map (pattern-grouped)

> Source: `mcp__firecrawl-mcp__firecrawl_map` (limit=500, includeSubdomains=false) on 2026-05-14. 399 URLs returned.

## Top-level path patterns

URL paths under stripe.com, grouped by `/<locale>/<top-segment>/`:

| Count | Pattern |
|---:|---|
| 113 | /<locale>/customers/* |
| 33 | /<locale>/guides/* |
| 28 | /<locale>/sessions/* |
| 24 | /<locale>/newsroom/* |
| 21 | /<locale>/payments/* |
| 21 | /jobs/* |
| 15 | /<locale>/use-cases/* |
| 9 | /<locale>/industries/* |
| 8 | /resources/* |
| 8 | /<locale>/connect/* |
| 7 | /<locale>/legal/* |
| 6 | /<locale>/resources/* |
| 6 | /<locale>/jobs/* |
| 5 | /<locale>/terminal/* |
| 5 | /customers/* |
| 5 | /<locale>/capital/* |
| 5 | /<locale>/pricing |
| 5 | /<locale>/payment-method/* |
| 4 | /<locale>/invoicing/* |
| 4 | /<locale>/cookie-settings |
| 4 | /<locale>/contact/* |
| 4 | /<locale>/billing/* |
| 4 | /<locale>/support-plans |
| 3 | /<locale>/privacy |
| 3 | /<locale>/sitemap |
| 3 | /<locale>/sigma |
| 3 | /newsroom/* |
| 3 | /<locale>/partners/* |
| 3 | /<locale>/treasury |
| 3 | /<locale>/enterprise |

Tail (single occurrences): ~30 more pattern buckets including `/billing`, `/atlas`, `/identity`, `/checkout`, `/elements`, `/issuing`, `/radar`, `/payouts`, `/financial-connections`, `/data-pipeline`, `/tax`, `/file`, `/forms`.

## Locale codes detected (73)

```
ae, at, au, br, de, de-be, de-ch, de-li, de-lu, en-at, en-be, en-bg, en-br,
en-ca, en-ch, en-cy, en-cz, en-de, en-dk, en-ee, en-es, en-fr, en-gi, en-gr,
en-hk, en-hr, en-hu, en-it, en-jp, en-li, en-lt, en-lu, en-lv, en-mt, en-mx,
en-my, en-nl, en-no, en-pl, en-pt, en-ro, en-se, en-sg, en-si, en-sk, en-th,
es, es-us, fr, fr-be, fr-ca, fr-ch, fr-lu, gb, ie, in, it, it-ch, it-hr, it-si,
jp, mx, nl, nl-be, nz, pt-pt, se, sv-fi, th, zh-hk, zh-my, zh-sg, zh-us
```

This count matches the 73 unique locales declared in the `/pricing` hreflang lattice — i18n implementation is consistent between declarative metadata (hreflang) and discoverable URL surface (the map).

## Notes on coverage

- `includeSubdomains: false` means `docs.stripe.com`, `support.stripe.com`, `dashboard.stripe.com`, `marketplace.stripe.com`, `status.stripe.com`, `press.stripe.com` are excluded from this run. Confirmed via the scrape mode (those subdomains appeared in body links but not in this map output).
- Firecrawl's map only surfaces URLs reachable from the homepage's link graph — a sitemap pull would include orphaned / sitemap-only URLs. See `seo-sitemap` for that workflow.
- The 399 URL ceiling is Firecrawl's discovery limit on the homepage's reachable set, not a hard site size — Stripe's full marketing surface is larger.
