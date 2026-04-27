# E-E-A-T scoring rubric (60 items)

15 items per dimension × 4 dimensions = 60 total. Score each: ✓ (full credit), ~ (partial), ✗ (fail). Dimension score = ✓ ÷ 15 × 100%. E-E-A-T composite = average of dimension scores.

## Veto items (any one triggers automatic NO PUBLISH)

1. **Anonymous authorship on a YMYL topic** (Your Money or Your Life: medical, financial, legal, safety). Author bylines required for these.
2. **Factual claims with no sources cited.** A piece that asserts statistics, study findings, or expert positions without inline citations.
3. **Undisclosed affiliate / sponsored relationships.** Required by FTC and Google's Helpful Content guidelines.
4. **AI-generated YMYL content with no human-review markers.** Trips when ≥4 of the 8 AI-content markers below are present *and* the topic is YMYL *and* the page lacks all of: a named human editor byline, a "reviewed by" credit, a "last reviewed" or "fact-checked on" date. AI assistance is fine; AI assistance on health/finance/legal/safety with no human accountability surface is not.

---

## 1. Experience (15 items)

First-hand engagement with the topic. Did the author actually do this?

1. The author has personally used / tested / experienced the product / service / process being discussed.
2. The piece includes original photos, screenshots, or video the author captured.
3. Original data the author collected (survey, A/B test, log analysis) is presented.
4. Specific, verifiable details only an experienced practitioner would know (numbers, edge cases, quirks).
5. Process documentation (step-by-step accounts) reflects real execution, not hypothetical steps.
6. Comparative observations across multiple instances (e.g., "across 12 client engagements, 8 saw…").
7. The piece acknowledges trade-offs and failure modes the author encountered.
8. Specific dates, locations, or contexts ground the experience claims.
9. Hands-on demonstrations (live code, working artifacts, before/after evidence).
10. Customer / user / patient quotes attributed to a real source (with permission).
11. Time-based observations (e.g., "after 6 months of using X, the result was…").
12. Process improvements or tweaks the author made along the way.
13. Tools / specific configurations / version numbers mentioned (signals real use).
14. Pricing / cost specifics from real engagements (not a price list).
15. Failures or rejected approaches described, not just successes.

## 2. Expertise (15 items)

Author's qualifications and depth on the topic.

1. Author byline visible with full name, not "Admin" or pseudonym.
2. Author bio includes credentials relevant to the topic (degree, certification, professional title).
3. Author bio includes years of experience in the topic domain.
4. Author has a linkable profile (LinkedIn, professional homepage, ORCID for academic).
5. Author publishes consistently in this topic area (link to other articles).
6. Citations to authoritative primary sources (peer-reviewed papers, government data, original research).
7. Industry-specific terminology used correctly and consistently.
8. Counter-arguments addressed and engaged, not strawmanned.
9. Methodology section if the piece presents data or analysis.
10. Disclosure of limitations of the analysis or recommendations.
11. Up-to-date with current developments in the field (recent references, current best practices).
12. Distinguishes correlation from causation when discussing data.
13. Avoids absolute claims where the field is genuinely contested.
14. Editorial review credit (e.g., "reviewed by Dr. X").
15. Author responds to comments / corrections (signals ongoing engagement).

## 3. Authoritativeness (15 items)

Reputation of the author and publishing entity in the topic domain.

1. The publisher has an "About" page describing its mission, history, team.
2. Editorial guidelines / standards page is publicly available.
3. The publisher is referenced or cited by other authoritative sources in the same field.
4. Wikipedia or industry-association mentions of the publisher (a strong signal).
5. The author has spoken at industry events, been quoted in trade press, or published in authoritative venues.
6. Awards or recognitions from peer institutions (with verifiable links).
7. The publisher's contact information is real and discoverable (physical address, named team).
8. Domain age and consistency (publishing in this topic for years, not weeks).
9. Other articles by this author cluster around the same topic (topical authority).
10. Internal links from cornerstone content on this site point to this piece (it's part of a hub).
11. External backlinks to this piece from authoritative sites (assess via `seo-backlink-gap` or `seo-backlinks-profile`).
12. The publisher is a recognised authority for its topic per industry consensus (not just self-description).
13. Press release / news coverage of the publisher's research or position on this topic.
14. Citations from peer publications to the publisher's previous work.
15. Inclusion in expert lists, "best of" roundups, awards lists by external bodies.

## 4. Trustworthiness (15 items)

Signals that the page and publisher are honest, accurate, and accountable.

1. HTTPS, valid certificate, no mixed-content issues.
2. Privacy policy and terms of service accessible from the page footer.
3. The publisher's name, registered business address, and contact route published.
4. Last-updated date visible and recent (within freshness window for the topic).
5. Original publish date visible.
6. Editorial standards / fact-check policy linked.
7. Corrections / updates log (visible if substantive corrections were made).
8. Comment moderation visible (no spam, signs of engagement).
9. Affiliate / sponsored / paid-content disclosures clear and prominent (if applicable).
10. Author bio prevents impersonation (recognisable photo, social proof links).
11. Schema.org `Article` (or sub-type) with `author` (Person), `publisher` (Organization), `datePublished` valid.
12. Site-wide trust signals: customer reviews, testimonials linked to real names/orgs.
13. The piece doesn't contain known misinformation about the topic (cross-check with authoritative sources).
14. Sources cited are themselves trustworthy (not Wikipedia → Wikipedia → Wikipedia chains).
15. Pricing, claims, and guarantees are clearly stated and not buried.

---

## AI-content markers (8 items — feeds veto #4)

A 2025-09 Search Quality Rater Guidelines update made "low-effort AI-generated content" an explicit demotion signal. These markers don't ban AI use — they identify pieces where AI was clearly the *only* hand on the page. Count how many fire and combine with the YMYL + human-review-credit check in veto #4.

1. **Generic LLM phrasing.** Multiple instances of "in today's world", "it's important to note that", "let's dive in", "navigating the landscape of", "in conclusion". Three or more on a single page = signal.
2. **Repetitive structural template across the site.** Five+ recently published pieces on the same domain share the identical H2 → H2 → H2 → H2 → FAQ structure with similar word counts. Smells like a single prompt template.
3. **No original insight or first-hand evidence.** Every claim paraphrases something already on the SERP top-10. Score 0/15 on Experience dimension is a strong corroborator.
4. **Em-dash density + bolded-phrase peppering.** Heavy use of em-dashes mid-sentence + every 2–3 paragraphs has a bolded summary phrase. Common output of GPT-4-class models.
5. **Hallucinated or unverifiable citations.** Inline citations exist but the linked source doesn't contain the cited claim, or the URL 404s, or the cited "study" can't be located. Spot-check 3 random citations.
6. **AI-shaped author byline.** Byline reads "Editorial Team", "Staff Writer", "{SiteName} Team" with no linked profile, OR the byline links to a profile with no other articles, no LinkedIn, no real-world footprint.
7. **No "reviewed by" or "fact-checked on" credit.** Especially for YMYL topics, absence of any human-accountability surface is itself a signal — combined with markers 1–6, suggests AI-only authorship.
8. **Suspiciously round publishing cadence.** Same site shipped 20+ pieces on different topics in a week with no obvious editorial arc. (Use site `:` site search or `seo-content-brief`-style topic clustering on the domain to corroborate.)

**Counting rule:** mark each as fired/not-fired. ≥4 fired = AI-content suspected. Combine with veto #4's YMYL + missing-human-review check before triggering the veto.

---

## How to score

For each item, mark ✓ (1), ~ (0.5), or ✗ (0). Dimension score = sum / 15 × 100%. E-E-A-T composite = average of 4 dimensions.

## Threshold

- E-E-A-T composite ≥ 75% AND no veto = pass.
- 60–74% = "publish with fixes" (top 5 fixes from lowest-scoring items).
- < 60% OR any veto = no publish.

## Calibration tips

- For YMYL topics, raise the bar: composite ≥ 85%, individual dimensions ≥ 75%.
- For purely informational content (e.g., a how-to on a hobby), Authoritativeness can be slightly lower if Experience and Expertise are strong.
- For brand / product content, Buyer-relevant Trust items dominate (transparent pricing, clear claims, social proof).
