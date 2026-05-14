# CITE scoring: stripe.com/blog/rate-limiters

> 30-item rubric (Clear answer / Include stats / Timestamp / Entity authority — ~7-8 items each). Per-item: ✓ yes / ✗ no / ~ partial.

## Clear answer (6/7 = 86%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Direct answer in first 200 words | ✓ | "Rate limiting can help make your API more reliable in the following scenarios:" appears within first ~150 words, with 4 bulleted use-cases |
| 2 | Definition before exposition | ✓ | "A *rate limiter* is used to control the rate of traffic sent or received on the network" |
| 3 | Tl;dr / summary box | ✗ | no executive summary box |
| 4 | Question framed before answer | ✓ | "When should you use a rate limiter?" → answer |
| 5 | Distinction surfaced (X vs Y) | ✓ | rate limiter vs load shedder distinction — explicitly defined |
| 6 | Quick-reference / cheat-sheet | ✓ | the conclusion lists "Follow the following steps" as a clear ordered recipe |
| 7 | Skimmable structure | ✓ | 4 named strategies as H3, plus H2 sections; bold inline highlights |

## Include primary stats (5/7 = 71%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | At least one specific number cited | ✓ | "12,000 requests this month", "rejected millions of requests" |
| 2 | Numbers attributed to source | ✓ | implied first-party (Stripe production); explicit "in our case" |
| 3 | Numbers contextualised (per X) | ~ | per-month volume is shown, but no per-second / per-customer breakdown |
| 4 | Comparison points provided | ~ | "more important than the others" stated, but no quantitative comparison |
| 5 | Numbers visualised | ✓ | 4 inline graphs |
| 6 | Recent / dated statistics | ✗ | the "this month" framing refers to 2017 traffic — no refresh |
| 7 | Avoids unsourced "studies show..." | ✓ | no vague third-party claims |

## Timestamp freshness (1/8 = 13%) — CRITICAL

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Publication date visible | ✓ | "March 30, 2017" |
| 2 | Publication date in machine-readable schema | ✓ | `datePublished: 2017-03-30T00:00-08:00` |
| 3 | Last-updated date visible | ✗ | absent |
| 4 | Last-updated date in `dateModified` | ✗ | absent |
| 5 | "Reviewed YYYY-MM" disclosure | ✗ | absent |
| 6 | Datestamp on volatile claims | ✗ | "12,000 requests this month" refers to Mar-2017 month, undated in body |
| 7 | Versioning / revision history | ✗ | absent |
| 8 | Datestamp matches schema | n/a | only one date exists, but **9 years old without refresh** is the actual problem |

This is the dimension that drags the composite below the publish threshold. A 9-year-old article with no `dateModified` and no visible review date sends "stale" signals to both classical SERP ranking and to LLM citation models.

## Entity authority (6/8 = 75%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Author named with affiliation | ✓ | Paul Tarjan / Stripe Engineering |
| 2 | Author entity disambiguated | ~ | twitter URL gives one signal; no `sameAs` array |
| 3 | Publisher entity declared in schema | ✗ | JSON-LD has no `publisher` field |
| 4 | `Organization` schema for publisher | ✗ | absent |
| 5 | Topic entity declared (`about: { ... }`) | ✗ | no `about` field in Article schema |
| 6 | Internal-link breadcrumbs reflect taxonomy | ✓ | Blog > Engineering > article |
| 7 | External citations resolve to authoritative entities | ✓ | IETF RFCs, Wikipedia, AWS — all canonical sources |
| 8 | Entity types used consistently across schema | ✓ | `@type: [Article, BlogPosting]` is appropriate; `author.@type: Person` matches |

## Composite

| Dimension | Score | Threshold | Status |
|---|---:|---:|:---:|
| Clear answer | 86% | 70% | OK |
| Include stats | 71% | 70% | OK (barely) |
| Timestamp | 13% | 70% | **FAIL** |
| Entity authority | 75% | 70% | OK |
| **CITE composite** | **66%** | 70% | **FAIL** |

## Veto checks

- **No answer in first 300 words:** not triggered (answer + use-case enumeration within first 150 words)
- **No datestamp on time-sensitive content:** *partially triggered* — the article makes time-sensitive claims ("this month" traffic numbers) without per-section datestamps, but does carry a publication date. Not a hard veto.
- **No entity disambiguation for proper-noun queries:** not triggered (author has identifiable Person schema + twitter URL)
