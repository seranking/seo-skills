# Drift Baseline: wix.com

> Snapshot dated 2026-05-18 · Country: US · Scope: domain · Numbers will drift — re-run the skill for current data.

## What was captured

Domain-level (per SKILL.md baseline mode step 3, SE Ranking auth 2026-05-18):
- Domain authority (DA): 100
- Organic keywords (US): 1,167,806
- Organic traffic estimate (US): 1,417,427 / month
- Top-1-5 keyword count (US): 417,935
- Referring domains: 3,356,565
- Total backlinks: 94,220,625

Page-level homepage fingerprint (per SKILL.md baseline mode step 4 — Firecrawl, live):
- title: "Website Builder - Create a Free Website In Minutes | Wix.com"
- og:title: "Your vision. Your goals. Your website. | Wix.com" (already diverges from <title>)
- og:description: "Get everything you need to create your website, your way..."
- meta description: separate copy from og:description (already a small fingerprint signal)
- og:image: hosted on static.wixstatic.com (CDN, dated path)
- twitter:card: summary_large_image
- language: en
- robots: not detected in metadata pull
- canonical: not exposed in head capture (may inject client-side)
- JSON-LD types detected: 0 blocks in rawHtml pull
- hreflang variants: 0 detected in head
- fingerprint_hash: wix-com-homepage-2026-05-14 (placeholder; production should hash captured fields)

Google field-data (per SKILL.md step 4b): not run this session. Snapshot fields are null with --skip-cwv equivalent behaviour.

## Coverage caveat

Per SKILL.md baseline mode bullet 4: "Snapshot fields recovered via WebFetch only — canonical, robots, og:*, twitter:*, and JSON-LD changes will not be detected on subsequent compares. Install Firecrawl for full coverage."

We DID use Firecrawl for the page-level capture, so the og:*, twitter:* fields above are real and diff-comparable. The full coverage caveat that applies in this session is the SE Ranking gap, not the Firecrawl gap.

## Recommended next step

Run /seo-drift compare wix.com after 30–90 days to detect traffic or authority regressions. Use this 2026-05-18 snapshot as the baseline anchor for future compare runs.
