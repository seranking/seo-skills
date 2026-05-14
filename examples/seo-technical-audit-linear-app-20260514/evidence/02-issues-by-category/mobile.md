# Issues — Mobile

Source: `mcp__firecrawl-mcp__firecrawl_scrape` (reads `<meta name="viewport">` and mobile-related meta tags) on 8 sample URLs.

## Viewport

Every sampled URL has:
```
<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, viewport-fit=cover">
```

- `width=device-width` — pass.
- `initial-scale=1` — pass.
- `viewport-fit=cover` — modern (handles notched devices like iPhone X+ correctly).
- `height=device-height` — unusual addition; not standard but harmless.

## Apple-specific

Present everywhere sampled:
- `<meta name="mobile-web-app-capable" content="yes">`
- `<meta name="apple-mobile-web-app-status-bar-style" content="black">`
- `<meta name="theme-color" content="#08090a">`

## PWA / app manifest

- `<link rel="manifest" href="https://linear.app/static/pwa.webmanifest?v=4">` — present on all sampled pages.
- PWA is supported. The Linear marketing site doubles as a PWA install target.

## Touch targets / responsive layout

Not measurable from headers/markup alone — would require headed Lighthouse run (Tier 0 via CrUX or full PageSpeed Insights).

## Verdict
No mobile blockers detected. Linear's mobile baseline is strong (modern viewport, PWA-ready, dark theme matched). The CWV-on-mobile field data lives in CrUX and is not configured in this run.
