# Drift severity thresholds

These thresholds drive the red / yellow / green coding in `DRIFT-REPORT.md`. Tune for your project — what's a regression for an enterprise site is noise for a startup.

## Domain-level

| Metric | Yellow | Red |
|---|---|---|
| Domain authority | ±5 points | ±10 points |
| Estimated organic traffic | ±20% | ±50% |
| Organic keyword count | ±10% | ±30% |
| Top-3 keyword count | ±15% | ±40% |
| Top-10 keyword count | ±10% | ±30% |
| Net referring domains | -5 to -20 | <-20 |
| Net backlinks | -50 to -200 | <-200 |
| Loss of any DA-50+ referring domain | red regardless of count | — |

## Page-level (when target is a single URL)

| Metric | Yellow | Red |
|---|---|---|
| Page authority | ±5 points | ±10 points |
| Title tag changed | yellow | — |
| Meta description changed | yellow | — |
| H1 changed | red | — |
| Canonical URL changed | red | — |
| Robots meta changed | red | — |
| Lang attribute changed | red | — |
| JSON-LD types added or removed | yellow | — |
| Internal-link count ±25% | yellow | — |
| Word count ±50% | yellow | — |

## Keyword churn (top-100)

| Change | Severity |
|---|---|
| Any top-3 keyword fell out of top-3 | red |
| Any top-10 keyword fell out of top-10 | yellow |
| New top-3 entry | green (positive) |
| Net top-100 churn > 30% | red (significant content shift, intentional or not) |
| Loss of a keyword with >5,000 monthly searches | red |

## Backlink churn

| Change | Severity |
|---|---|
| Loss of >5 referring domains | yellow |
| Loss of >20 referring domains | red |
| Loss of any DA-50+ referring domain | red regardless of count |
| Net new backlinks > +20% | green |

## What to investigate first

When `DRIFT-REPORT.md` shows multiple red findings, the recommended order:

1. **Page-level reds** (canonical, robots, lang, H1) — usually deploy-time mistakes, fast to fix.
2. **Top-3 keyword drops** — direct visibility/revenue impact.
3. **DA-50+ referring domain loss** — link equity loss compounds; investigate whether the linking page was removed or just moved.
4. **Net keyword churn > 30%** — points at content changes that affected ranking; cross-reference with a `seo-page` deep-dive on the most-affected URLs.
5. **Domain authority drop > 10** — usually a lagging signal of the above; treat as confirmation, not primary diagnosis.

## How to interpret "yellow"

Yellow means: notable change, worth a one-line note in the team standup, not a fire drill. If a single yellow finding appears in isolation, often it's seasonal/normal variance. If multiple yellows appear together, treat as an emerging red.

## How to interpret "green"

Green deltas are still worth noting — they tell you which changes in your content/SEO program are working. Build muscle around capturing the why behind each green finding so it can be replicated.
