# E-E-A-T scoring: stripe.com/blog/rate-limiters

> 60-item rubric (15 per dimension). Per-item: ✓ yes / ✗ no / ~ partial. Each scored 1 / 0 / 0.5; dimension % = sum / 15.

## Experience (14/15 = 93%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | First-person production usage stated | ✓ | "Our rate limits for requests is constantly triggered. It has rejected millions of requests this month alone" |
| 2 | Concrete numbers from production | ✓ | "12,000 requests this month", "100 requests rejected this month", "millions of requests" |
| 3 | Time-in-role / experience window signalled | ~ | implied by Stripe employment + content date, but no explicit "we have been doing this since X" |
| 4 | Tools / stack named explicitly | ✓ | Redis, AWS ElastiCache, Lua (via gist), HTTP 429, HTTP 503 |
| 5 | Failure modes / edge cases described | ✓ | "flapping" example, "kill switches", "feature flags", "fail open" |
| 6 | Production telemetry visible | ✓ | 4 inline graphs labelled "Graph 1-4" with traffic data |
| 7 | Decisions explained, not just choices listed | ✓ | "tune this limiter up so it rejects more often", trade-offs surfaced |
| 8 | Trade-offs acknowledged | ✓ | "two patterns so feel free to use which one is most suitable for the users of your API" |
| 9 | Reader's likely first attempt addressed | ✓ | "The first few times this happens, it's reasonable to just add more capacity" |
| 10 | War stories / "we tried X, it didn't work" | ✓ | "regularly dealt with resource contention on our most expensive endpoints" before concurrent limiter |
| 11 | Code / config examples present | ~ | Code linked via GitHub gist; not inline |
| 12 | Diagrams / visualisations original | ✓ | 4 production-traffic graphs (Stripe's own, not stock illustrations) |
| 13 | Avoids stock-photo style imagery | ✓ | only Stripe-generated traffic graphs |
| 14 | Author present in content (not just byline) | ✓ | "we", "our" used throughout; identifiable single perspective |
| 15 | Voice consistent end-to-end | ✓ | clearly one author throughout |

## Expertise (13/15 = 87%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Author named | ✓ | Paul Tarjan |
| 2 | Author affiliation declared | ✓ | "Engineering" tag, Stripe |
| 3 | Author has verifiable credentials | ✓ | twitter.com/ptarjan link present in JSON-LD `author.url` |
| 4 | Author has track record on topic | ✓ | senior engineer at a payments company that operates at scale |
| 5 | Technical correctness | ✓ | RFC 6585 (HTTP 429), RFC 7231 (HTTP 503), token bucket algorithm — all correct |
| 6 | Terminology used precisely | ✓ | "rate limiter" vs "load shedder" — clear, non-conflated distinction (this is rare and valuable) |
| 7 | Domain jargon defined where used | ✓ | "load shedding" italic + defined, "token bucket" + Wikipedia link |
| 8 | Citations point to primary sources | ✓ | RFCs are primary; Wikipedia is secondary but accepted |
| 9 | Author bio / page present | ✗ | no `/blog/authors/paul-tarjan` page; only twitter link |
| 10 | `Person` schema present | ~ | embedded inside `Article.author`, not standalone — partial credit |
| 11 | Authors `sameAs` to LinkedIn/GitHub | ✗ | only twitter URL — should include LinkedIn + GitHub |
| 12 | Editor / reviewer credited | ✗ | no "reviewed by" or editor byline |
| 13 | Last-reviewed date | ✗ | none — and the article is 9 years old |
| 14 | Author has multiple related posts | ~ | Paul Tarjan has at least one other Stripe blog post; not surfaced on this page |
| 15 | Topic depth proportional to claim | ✓ | 4-strategy enumeration with separate sub-sections is appropriately deep |

## Authoritativeness (12/15 = 80%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Publisher domain has topical authority | ✓ | stripe.com is THE canonical source for payments-scale API engineering |
| 2 | Publisher schema declared | ✗ | JSON-LD has no `publisher` field |
| 3 | About page / company info findable | ✓ | stripe.com is well-known; nav surfaces "About" |
| 4 | Contact info present | ✓ | "Contact sales", footer email |
| 5 | Editorial standards / fact-checking process disclosed | ✗ | no editorial process page |
| 6 | Site has consistent author archive | ~ | individual posts have authors but no `/blog/authors/{slug}` |
| 7 | External backlinks to this URL from authority sites | ~ | not measured (would need SE Ranking backlinks endpoint) — known anecdotally to be high (popular engineering blog post) |
| 8 | Cited by competitors / peer publications | ~ | not measured |
| 9 | Listed in industry reading lists | ~ | not measured; presumed yes given page's reputation |
| 10 | About-this-article transparency | ✗ | no "Why we wrote this" or methodology disclosure |
| 11 | First-party data (proprietary) cited | ✓ | Stripe's own production metrics ("12,000 requests this month") |
| 12 | Third-party references credible | ✓ | RFCs, Wikipedia, AWS docs |
| 13 | Article positioned in editorial taxonomy | ✓ | breadcrumb: Blog > Engineering > this article |
| 14 | Related-articles surfaced | ✓ | one internal link to `/blog/idempotency` |
| 15 | Trust badges / certifications surfaced where relevant | ✓ | global footer covers compliance / privacy / licensing |

## Trustworthiness (11/15 = 73%)

| # | Item | Result | Note |
|---|---|:---:|---|
| 1 | Publication date visible | ✓ | "March 30, 2017" rendered |
| 2 | Last-updated date visible | ✗ | absent — **critical issue for a 9-year-old article** |
| 3 | `datePublished` in JSON-LD | ✓ | "2017-03-30T00:00-08:00" |
| 4 | `dateModified` in JSON-LD | ✗ | **missing** |
| 5 | Author identity verifiable | ✓ | twitter URL + Stripe Engineering tag |
| 6 | Author has staff / disclosure status | ✓ | "Engineering" badge implies Stripe employee |
| 7 | Affiliate / sponsored content disclosed | n/a | no commercial relationships in the article |
| 8 | Conflict of interest disclosed | n/a | none present |
| 9 | Privacy policy linked | ✓ | footer |
| 10 | Terms of service linked | ✓ | footer |
| 11 | HTTPS + valid certificate | ✓ | Stripe site-wide |
| 12 | Comments / interaction surface (with moderation) | ✗ | no comments / discussion |
| 13 | Errata / correction policy | ✗ | not disclosed |
| 14 | Reader feedback mechanism | ~ | "Contact us" CTA at the bottom; not topic-specific |
| 15 | Trust-tier byline (e.g., "Reviewed by [editor]") | ✗ | absent |

## AI-content markers (0 / 8 fired)

The article is from 2017, well before generative-AI authorship became a concern. None of the 8 AI-content markers fire:
- ✗ "Delve" / "tapestry" / "leverage" / "synergy" overload — clear, technical voice
- ✗ Excessive lists/bullets per section — appropriate enumeration only
- ✗ Generic / non-specific examples — real production numbers cited
- ✗ Repetition of phrases across sections — none
- ✗ Hedging language ("It's important to note that...") — none
- ✗ Empty calorie phrases — none
- ✗ Awkward transition phrases — none
- ✗ Wikipedia-style impartiality — strong first-person voice

## Composite

| Dimension | Score | Threshold | Status |
|---|---:|---:|:---:|
| Experience | 93% | 75% | OK |
| Expertise | 87% | 75% | OK |
| Authoritativeness | 80% | 75% | OK |
| Trustworthiness | 73% | 75% | **FAIL** (driven entirely by absent `dateModified` + visible review date) |
| **E-E-A-T composite** | **83%** | 75% | OK |
