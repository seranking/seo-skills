# Sample PageSpeed Insights — anchor-seo.com (template — what you'll see when you run this)

> **Template** dated 2026-05-14 · URL audited: `https://anchor-seo.com/` (fictional) · This is a **template** showing the shape of `python scripts/pagespeed_check.py <url> --json` output. Google API credentials were not available during example capture — run with a real API key (Tier 0 — free) and your data will fill this shape.

## Snapshot

- URL: https://anchor-seo.com/
- Tested: 2026-05-14
- Strategy: mobile + desktop (default — both run)
- Tier required: 0 (API key only — free, 25,000 queries/day)
- CrUX coverage: URL-level (sufficient Chrome traffic for first-party field data)

## Core Web Vitals (CrUX field data — last 28 days)

### Mobile

| Metric | p75 value | Rating | vs threshold |
|---|---|---|---|
| LCP | 2.4s | **Good** | < 2.5s ✓ |
| INP | 184ms | **Good** | < 200ms ✓ |
| CLS | 0.08 | **Good** | < 0.1 ✓ |
| FCP | 1.8s | **Good** | < 1.8s ✓ |
| TTFB | 0.62s | **Good** | < 0.8s ✓ |

### Desktop

| Metric | p75 value | Rating | vs threshold |
|---|---|---|---|
| LCP | 1.2s | **Good** | < 2.5s ✓ |
| INP | 92ms | **Good** | < 200ms ✓ |
| CLS | 0.04 | **Good** | < 0.1 ✓ |
| FCP | 0.9s | **Good** | < 1.8s ✓ |
| TTFB | 0.34s | **Good** | < 0.8s ✓ |

## Verdict: PASS

All 5 CWV metrics are rated **Good** at p75 on both mobile and desktop. No CWV-blocked indexation risk.

## Lighthouse lab scores

### Mobile (real-world device throttling, 4G)

| Category | Score |
|---|---:|
| Performance | 87/100 |
| Accessibility | 96/100 |
| Best Practices | 92/100 |
| SEO | 100/100 |

### Desktop (faster simulated network)

| Category | Score |
|---|---:|
| Performance | 98/100 |
| Accessibility | 96/100 |
| Best Practices | 92/100 |
| SEO | 100/100 |

## Lighthouse Opportunities (mobile)

> Each Opportunity is an estimated speed saving if implemented. Sorted by potential savings.

| # | Opportunity | Estimated savings | Category |
|---|---|---:|---|
| 1 | Properly size images | 0.42s | LCP / FCP |
| 2 | Eliminate render-blocking resources | 0.28s | LCP / FCP |
| 3 | Defer offscreen images | 0.18s | LCP |
| 4 | Reduce unused JavaScript | 0.14s | LCP |
| 5 | Use efficient image formats (AVIF / WebP) | 0.10s | LCP |
| 6 | Reduce unused CSS | 0.06s | LCP |
| 7 | Preconnect to required origins | 0.04s | TTFB / FCP |

**Total estimated savings if all implemented:** ~1.22s on mobile (LCP could drop from 2.4s to ~1.2s, putting more headroom against the 2.5s threshold and reducing degradation risk over time).

## Lighthouse Diagnostics (mobile)

> Diagnostics are observations, not direct speed savings.

- DOM size: 1,840 elements (acceptable; warning threshold is 1,500)
- Main-thread work: 1.6s total, 412ms scripting (acceptable)
- JavaScript execution time: 1.1s (acceptable for B2B SaaS marketing page)
- Largest Contentful Paint element: hero `<img>` (correctly identified, optimisable)
- Avoid an excessive DOM size: yes (1,840 > 1,500 warning)
- Image elements have explicit width and height: yes (no CLS contribution from images)

## Accessibility findings

- Form elements have associated labels: yes
- Color contrast ratios: yes (1 warning on slate-400 text against slate-50 background — minor)
- Images have alt text: 14 of 16 present (2 decorative images correctly use empty alt; check)
- Heading order: warning (one H2 follows H4 — flag for content team)

## Best Practices findings

- HTTPS: yes
- Images aspect ratios are correct: yes
- Browser errors logged to console: 0
- Uses HTTP/2: yes
- Avoids `unload` event listeners: yes

## SEO findings

- Page has meta description: yes
- Page has `<title>`: yes
- Document has a viewport meta tag: yes
- robots.txt is valid: yes
- Image elements have alt: see Accessibility
- Document uses legible font sizes: yes
- Tap targets are sized appropriately: yes
- Document has a valid `hreflang`: N/A (single-language site)
- Document avoids plugins: yes
- Score: 100/100

## CrUX URL-level vs origin-level

CrUX returned URL-level field data for this URL. If the URL had insufficient Chrome traffic for URL-level reporting (404 from the CrUX API), the script would fall back to origin-level data (averaged across `anchor-seo.com`).

## Suggested follow-ups

1. **Implement the top 3 Lighthouse Opportunities** (image sizing, render-blocking, offscreen images). Estimated ~0.88s LCP saving. Re-run `pagespeed` after the deploy to confirm.
2. **Track CWV trend with `crux-history`.** A single PSI run is a point-in-time check. The 25-week CrUX History trend (see `sample-crux-history.md`) reveals whether performance is degrading over time.
3. **Pair with `seo-technical-audit`.** Lighthouse covers performance + a11y + a-thin-SEO-pass. The `seo-technical-audit` skill goes deeper on crawlability, indexability, structured data, JS rendering, etc.

## Raw JSON

To save the full PSI response: `python scripts/pagespeed_check.py https://anchor-seo.com/ --json > psi.json`.
To render as a report: `python scripts/google_report.py --type cwv-audit --data psi.json --domain anchor-seo.com --format md`.
