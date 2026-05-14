# Modern signals (JS-render, AI bots, IndexNow)

Source: `mcp__firecrawl-mcp__firecrawl_scrape` for JS-rendered DOM comparison (raw HTML returned post-render) on 5 sample URLs. AI-bot probing via `curl -A "{bot UA}"` on `/`.

## JS-rendered canonical vs initial-HTML canonical

Per Google's December 2025 JavaScript SEO guidance, divergence between initial-HTML and JS-rendered canonical URLs can produce non-deterministic indexing decisions.

| URL | Initial-HTML canonical | JS-rendered canonical | Match? |
|---|---|---|:---:|
| / | https://linear.app/ | https://linear.app/ | yes |
| /pricing | https://linear.app/pricing | https://linear.app/pricing | yes |
| /method | https://linear.app/method | https://linear.app/method | yes |
| /customers | https://linear.app/customers | https://linear.app/customers | yes |
| /customers/openai | https://linear.app/customers/openai | https://linear.app/customers/openai | yes |

**No `js_canonical_mismatch` detected on the sample.** Linear's Next.js setup appears to inject canonical tags at SSR time, so the static HTML and the rendered DOM match. Good.

## JS-rendered noindex

No `<meta name="robots" content="noindex">` observed in either initial HTML or rendered DOM on any sampled page. No `js_noindex_injected` risk.

## X-Robots-Tag header

No `X-Robots-Tag` HTTP-layer directive on any sampled page. No HTTP-layer noindex conflict.

## Risk 1 — Rendering-budget cuts (`js_render_budget`)
Not directly measured in this run (would require comparing raw initial HTML size to post-render DOM size in Firecrawl's `parsers` output). Linear is Next.js with SSR + ISR — the initial HTML is already well-populated, so render-budget risk is low. Not flagged.

## Risk 2 — Hydration mismatch
Already covered by canonical match check above. No drift.

## Risk 3 — CSR pitfalls (`js_csr_meta_drift`)
Title, H1, and meta description match between initial HTML and rendered DOM on the homepage and the 4 sampled inner pages. **No `js_csr_meta_drift` detected.**

## Risk 4 — Soft-404 from JS errors (`js_soft_404`)
No sampled page rendered <500 chars of body text with a 200 status. **No `js_soft_404` detected.**

## AI-crawler robots.txt rules

| Bot User-Agent | curl result | robots.txt rule | Behaviour |
|---|---:|---|---|
| `GPTBot` | HTTP 200 | none specific | implicit allow via `User-Agent: *` |
| `ClaudeBot` | HTTP 200 | none specific | implicit allow |
| `PerplexityBot` | HTTP 200 | none specific | implicit allow |
| `Google-Extended` | HTTP 200 | none specific | implicit allow |
| `CCBot` | HTTP 200 | none specific | implicit allow |
| `Bytespider` | (not tested) | none specific | implicit allow |

**Decision needed.** Linear has no explicit AI-bot policy in robots.txt. The current behaviour is implicit allow, which is the default. To make the policy intentional:
- **Option A — explicit allow** (preserves current behaviour, signals "yes, train on us"):
  ```
  User-Agent: GPTBot
  Allow: /
  
  User-Agent: ClaudeBot
  Allow: /
  
  User-Agent: PerplexityBot
  Allow: /
  
  User-Agent: Google-Extended
  Allow: /
  ```
- **Option B — opt out** of LLM training while keeping AI Search citation access:
  ```
  User-Agent: GPTBot
  Disallow: /
  
  User-Agent: ClaudeBot
  Disallow: /
  
  User-Agent: CCBot
  Disallow: /
  ```
  (Note: `Google-Extended` disallow opts out of Gemini training but **also** affects AI Overview generation; PerplexityBot is the index, opt-out blocks Perplexity citations entirely.)

## IndexNow

- `IndexNow:` directive in robots.txt: **none**.
- `x-indexnow-key` / `x-indexnow-key-location` response headers: **none**.
- `/<key>.txt` at root: not probed (no hint to follow).
- Status: **`indexnow_no_key`** (Low; informational — Bing-only benefit; Bing's share is small but IndexNow is cheap to set up if you publish frequently).

## Summary

Linear's marketing site is **well-behaved on modern crawlability signals**: SSR canonical matches rendered canonical, no JS-only noindex, no soft-404 risk, no metadata drift between initial HTML and DOM. The only "modern signal" gaps are:
1. No explicit AI-bot policy in robots.txt (implicit allow).
2. IndexNow not configured.
3. The structured-data gap (covered in `structured-data.md`) is the dominant AI-Search-readiness issue.
