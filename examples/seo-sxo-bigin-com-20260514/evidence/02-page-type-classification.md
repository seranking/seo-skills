# 02 — Page type classification

> Signals used: URL pattern, title pattern, content structure (from WebFetch markdown), schema (when Firecrawl rawHtml available).
> See `references/page-type-patterns.md` in the skill folder for the canonical heuristics this classifier is grounded in.

## Classification per top-10 result

| # | URL | Page type | URL signal | Title signal | Content signal | Schema signal (where checked) |
|---|---|---|---|---|---|---|
| 1 | forbes.com/advisor/business/software/best-crm-small-business/ | **Listicle** | `/advisor/.../best-` | "10 Best..." | Ranked numbered sections, comparison table, pros/cons per item | Article + ItemList (typical for Forbes Advisor) |
| 2 | pcmag.com/picks/the-best-small-business-crm-software | **Listicle** | `/picks/the-best-` | "The Best..." | "Editor's Choice" callouts, ranked items, pros/cons | Article + ItemList |
| 3 | crm.org/crmland/best-crm-for-small-business | **Listicle** | `/best-crm-for-` | "10 Best CRM..." | Numbered sections, comparison framing | Article (typical) |
| 4 | toolradar.com/blog/best-crm-for-small-business | **Listicle (comparison-heavy)** | `/blog/best-` | "10 Best CRM... Compared" | Heavy comparison-table framing | Article + ItemList |
| 5 | techradar.com/best/best-crm-for-small-business | **Listicle** | `/best/best-crm-` | "Best small business CRM of 2026" | TechRadar's house listicle format | Article + ItemList |
| 6 | capterra.com/small-business-crm-software/ | **Comparison (directory)** | `/{category}-software/` | "Best Small Business CRM Software 2026 | Capterra" | Filterable grid of vendors with ratings | ItemList + AggregateRating per vendor |
| 7 | selecthub.com/c/crm-software/ | **Comparison (directory)** | `/c/crm-software/` | "10 Best CRM... Tested and Rated 2026" | Ranked comparison with rating breakdowns | ItemList + Review |
| 8 | cloudtalk.io/blog/best-crm-software-for-small-businesses/ | **Listicle (vendor blog)** | `/blog/best-` | "12 Best CRM..." | CloudTalk's listicle (CloudTalk is a vendor, blog post is editorial framing) | Article |
| 9 | zdnet.com/article/best-small-business-crm-software/ | **Listicle** | `/article/best-` | "Best small business CRM 2026: Expert tested" | Numbered ranked sections, methodology callout | Article + ItemList |
| 10 | onepagecrm.com/blog/best-crm-for-small-business/ | **Listicle (vendor blog)** | `/blog/best-` | "17 Best CRM..." | OnePageCRM blog post; numbered, includes OnePageCRM | Article |

## Tally

| Page type | Count |
|---|---:|
| Listicle | 8 |
| Comparison (directory) | 2 |
| **Vendor product page** | **0** |
| How-to | 0 |
| Definition | 0 |
| Editorial (non-listicle) | 0 |
| Forum/UGC | 0 |
| Video | 0 |

## Dominant pattern

**Listicle.** 8 of 10 results. Confidence: HIGH.

## Cross-check with SERP features

- AIO present → informational consensus is being aggregated. Confirms listicle dominance.
- PAA present → users have related questions; listicles handle this format natively (a listicle answers "best X for Y" + sub-questions in one page).
- No shopping pack → not pure-transactional. Commercial-investigation, not commercial-transactional.
- No image/video carousel → text content dominates the SERP.

All signals reinforce the listicle classification.

## Bigin.com classification

- **URL signal:** `bigin.com/` — homepage / product hub. NOT `/best-` or `/blog/best-` pattern.
- **Title signal:** "The Easiest Small business CRM - Bigin by Zoho CRM" — single-product positioning, not "best of" framing.
- **Content signal:** Hero + 6 features (Team Pipelines / 360-degree view / Multichannel / Automation / Task Management / Mobile) + customer testimonials carousel + badges. Single-product narrative.
- **Schema signal:** No JSON-LD `ItemList`. (Standard `Organization` + `WebSite` schema typical for this kind of page.)

Bigin.com = **vendor product page**. Confidence: HIGH.

## Conclusion

Page-type mismatch: vendor product page vs SERP-rewarded listicle. This is the case described in `references/page-type-patterns.md` §mismatch — the skill's verdict moves to "ship a different page type" rather than "optimise this one."
