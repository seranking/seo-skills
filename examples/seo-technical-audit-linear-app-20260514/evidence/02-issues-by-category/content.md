# Issues — Content

Source: `mcp__firecrawl-mcp__firecrawl_scrape` extracts (title, meta description, H1, H2) on 8 sample URLs.

## Title and description audit

| URL | Title chars | Meta description chars | Verdict |
|---|---:|---:|---|
| / | 45 | 61 | both short — leaves SERP real estate unused |
| /pricing | 17 | 130 | title very short; description in range |
| /method | 38 | ~250 | title short; description too long (Google truncates at ~155) |
| /customers | 17 | 78 | both short — esp. weak for a competitive query like "linear customers" |
| /customers/openai | 52 | ~310 | title in range; description heavily truncated |
| /agents | sampled, similar pattern | — | — |
| /features | sampled, similar pattern | — | — |
| /insights | sampled, similar pattern | — | — |

## H-tag hierarchy

| URL | H1 count | Sample H1 | Issue |
|---|---:|---|---|
| / | 2 | "The productdevelopmentsystem for teamsand agents" (rendered twice with display:none variant for responsive) | `duplicate_h1` |
| /pricing | 1 | "Pricing" | none |
| /method | 1 | "Practices for building" | none |
| /customers | 1 | "Customers" | none |
| /customers/openai | 1 | (from page narrative) | none |

The duplicate-H1 on the homepage is a responsive-design artefact. Static crawlers and screen readers see both H1s. Recommend `aria-hidden` + `tabindex="-1"` on the duplicate, or consolidate into a single H1 with CSS-driven line-breaks.

## Word-count signals

Not directly measured, but observation from rendered markdown:
- `/` is heavily visual; word count likely <500 in indexable text — typical for a homepage.
- `/pricing` is feature-comparison-heavy; word count ~800 with all tiers rendered.
- `/method` is essay-shaped with internal-link spine (Introduction → Direction → Building → Product → Company → Communication → Inspiration); word count likely 3-5K across the index plus per-chapter pages.
- `/customers/openai` (and other customer stories) are case-study-shaped; word count typically 1.5-3K — strong E-E-A-T baseline if `Article` + `Person` schema were added.

## Recommendations

1. Rewrite homepage `<title>` and `<meta description>` to use full SERP real estate (title 55-60, description 140-155).
2. Trim `/method` and `/customers/*` meta descriptions to ≤155 chars.
3. Resolve homepage duplicate-H1.
4. Consider `Article` body markup (with `<article>`, `<header>`, `<time datetime="...">`) on `/method/{chapter}` and `/blog/{slug}` and `/customers/{slug}` to give schema parsers a structural anchor.
