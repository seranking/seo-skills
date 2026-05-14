# Firecrawl: stripe.com/pricing

> Snapshot dated 2026-05-14 · Mode: scrape · Credits used: 1
> Numbers will drift — re-run the skill for current data.

## Summary

Scraped `https://stripe.com/pricing` with `formats: ["markdown", "html", "rawHtml", "links"]` and `onlyMainContent: false`. Page returns HTTP 200, server-rendered (no JS divergence detected), canonical self-referencing. Robust internationalisation signal: **87 `hreflang` alternates** declared in `<head>`, covering 73 distinct locale codes. **Zero JSON-LD blocks** — that is the headline finding, surprising for a flagship pricing page. Twitter card present (`summary_large_image`), Open Graph complete, Facebook domain verified. 271 outbound links from page body, heavily concentrated on `stripe.com` (203) with `docs.stripe.com` (29), `dashboard.stripe.com` (19), `support.stripe.com` (12) as the next biggest subdomains.

## Key findings

1. **No JSON-LD on the pricing page.** Zero `<script type="application/ld+json">` blocks. For a high-intent pricing page that drives commercial queries, missing `Product`/`Offer`/`Organization` schema leaves rich-result eligibility on the table. Highest-leverage fix.
2. **Massive hreflang surface (87 alternates).** `x-default` present and points to `/pricing`. Self-reference (`en-US` → `https://stripe.com/pricing`) is correct. Coverage spans 73 locales — well above industry median. Worth a dedicated `seo-hreflang` audit to verify return tags on each variant.
3. **Canonical is self-referencing and clean.** `<link rel="canonical" href="https://stripe.com/pricing">`. No conflict with the hreflang `en-US` self-entry.
4. **Robots meta absent from head** — Stripe relies on `/robots.txt` and HTTP headers. Reasonable for a high-trust domain but worth confirming via header inspection if indexation issues ever appear.
5. **Markdown body extracts cleanly with `onlyMainContent: false`** (65 KB markdown, 271 links). For purely-prose use cases (LLM training, content audits) the default `onlyMainContent: true` would have been preferable — this run used full-page to preserve nav for link-graph analysis.

## Open loops

- JSON-LD generation — fix that in a follow-up `seo-schema` run on this URL.
- Return-tag verification across the 87 hreflang alternates — `seo-hreflang` is the right successor; this scrape only confirms the source-page surface.
- AIO citation status for "stripe pricing" / "credit card processing fees" — `seo-geo` on this URL would answer that.
- WAF/anti-bot interactions — `proxyUsed: basic`, `cacheState: hit`, no blocks. Worth re-running with `proxy: "stealth"` only if a fresh (uncached) scrape behaves differently.

## Recommended next step

`seo-schema` — the JSON-LD gap is the highest-leverage finding from this scrape. Generate `Product`/`Offer`/`Organization` schema blocks paste-ready for the pricing page. Pair with `seo-hreflang` on the same domain to validate the 87-locale lattice.

## Handoff payload

- **Produced by:** seo-firecrawl
- **Target:** https://stripe.com/pricing
- **Mode:** scrape
- **Credits used:** 1
- **Key findings:** (a) zero JSON-LD blocks present; (b) 87 hreflang alternates covering 73 locales; (c) canonical self-referencing and clean; (d) twitter:card summary_large_image + Open Graph complete; (e) 271 outbound links, mostly internal stripe.com.
- **Open loops:** schema generation; hreflang return-tag verification; AIO citation status.
- **Recommended next skill:** `seo-schema` — close the JSON-LD gap on the pricing page. Then `seo-hreflang` to validate the 73-locale lattice.
