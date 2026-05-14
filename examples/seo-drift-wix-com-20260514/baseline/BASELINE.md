# Drift Baseline: wix.com

> Snapshot dated 2026-05-14 · Country: US · Scope: domain · Numbers will drift — re-run the skill for current data.

> Session note: SE Ranking MCP auth unavailable in this session. Domain authority, organic-traffic estimate, organic-keywords count, top-100 keywords, backlinks, referring-domains, and page authority are stored as null in snapshot.json with a [SE Ranking — pending] marker on each field. Re-run /seo-drift baseline wix.com from a session with SE Ranking auth to produce a complete snapshot. Firecrawl head-metadata capture for the homepage IS live in snapshot.json.

## What was captured

Domain-level (per SKILL.md baseline mode step 3): all fields pending SE Ranking auth.

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

Re-run /seo-drift baseline wix.com from a session with SE Ranking auth. The resulting snapshot.json will have DA, organic-traffic, organic-keywords count, top-100 keywords, backlinks, and referring-domains fields populated — and subsequent /seo-drift compare wix.com calls will produce meaningful red/yellow/green diffs against that fuller baseline.

Estimated SE Ranking cost on a re-run: ~10–15 credits for the domain-only baseline (per SKILL.md).
