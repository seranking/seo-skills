# Persona rubrics for SXO scoring

Score the candidate page from each of these 4 personas. 0–10 per persona; the weighted sum (using the intent-based weighting profile below) is the SXO score (0–100).

## 1. The Skimmer
A reader who lands on the page expecting to extract the answer in <30 seconds. They scan H2s, look for tables/lists, may not read prose at all.

**Score 10 if:**
- TL;DR / answer / verdict in the first 200 words OR in a clearly visible callout box.
- H2s are descriptive, not "Introduction" / "Background" — they preview the content.
- Lists, tables, or step blocks dominate the layout.
- Bold or highlighted phrases mark key takeaways.

**Score 0 if:**
- The "answer" is buried below 1500 words of preamble.
- H2s are uninformative ("What you need to know", "Let's begin").
- Continuous prose with no visual hierarchy.

## 2. The Researcher
A reader who's deep in research mode. Compares the page against 5+ other tabs. Looks for data, sources, dates.

**Score 10 if:**
- Original data, statistics, or proprietary research present.
- Sources cited inline (links or numbered references).
- Last-updated date visible and recent (<6 months for fast-moving topics).
- Counter-arguments or trade-offs acknowledged.
- Author has visible credentials relevant to the topic.

**Score 0 if:**
- Generic claims with no sources.
- No publish/update date.
- Reads like AI-spun content (vague, no specifics).

## 3. The Buyer
A reader with intent to convert. Wants to know if this product/service/recommendation actually solves their problem and is worth the cost.

**Score 10 if:**
- Clear value proposition above the fold.
- Pricing visible (or clearly indicated as "contact us" with reason).
- Social proof: testimonials, case studies, named customers.
- Specific outcomes named, not just features ("cut acquisition cost 32%" vs "save money").
- Pricing/plan comparison if multiple options.

**Score 0 if:**
- "Contact for pricing" with no context.
- Generic benefits ("save time", "boost revenue") with no specifics.
- No social proof or vague claims ("trusted by leading brands").

## 4. The Validator
A reader who needs to verify the page's claims for someone else (their boss, their team, a stakeholder). Looks for trust signals before sharing.

**Score 10 if:**
- Author bio with title, company, and link.
- Editorial standards or methodology page linked.
- Last-reviewed/updated date on every page.
- Schema.org markup correct (`Article`, `Product`, `FAQ`).
- HTTPS, privacy policy, terms of service.
- About page humanises the publisher (real people, real address).

**Score 0 if:**
- No author or "Admin" / generic byline.
- No publish/update dates.
- Site has poor technical hygiene (broken links, missing privacy policy).

## Weighting profile by intent

The page's keyword tells you which intent dominates. Weight the personas accordingly:

| Intent | Skimmer | Researcher | Buyer | Validator |
|---|---|---|---|---|
| Informational ("what is", "how to") | 40% | 30% | 10% | 20% |
| Commercial-investigation ("best X", "X vs Y", "X review") | 25% | 25% | 35% | 15% |
| Transactional ("buy X", "X pricing", "sign up") | 20% | 15% | 50% | 15% |
| Navigational ("brand name", "brand login") | 30% | 10% | 40% | 20% |

## Combined SXO score

The SXO score is the **weighted sum** of persona scores (0–100).

- ≥ 75 — page is well-aligned with the SERP it targets.
- 50–74 — room to improve; see persona-specific gaps in the recommendation.
- < 50 — likely page-type or intent mismatch; `seo-sxo` will recommend a different page type.

The score is a heuristic. Always cross-reference with actual SERP features (AIO presence, top-10 page types) before recommending a rewrite — those are what Google rewards.
