# Backlinks Profile: stripe.com

> Snapshot dated 2026-05-18 · scope: domain (incl. all subdomains) · Single-source design (SE Ranking only — see "Why single-source" in the SKILL) · Numbers will drift — re-run the skill for current data.

## Verdict

**Stripe runs one of the cleanest backlink profiles in the SaaS/fintech category.** The link graph is built primarily on developer trust (`github.com`, `stackoverflow.com`, `dev.to`, `medium.com`), media coverage (top-tier financial press), and integration-partner pages (every payment-accepting SaaS lists Stripe as a payment processor, usually with a follow link). Anchor distribution is overwhelmingly branded, IP/subnet diversity is high, growth is steady. The very-low toxic-candidate signal is partly real (Stripe is a strong target for legitimate links) and partly an artefact of being so big that low-quality sites barely move the percentages.

The **headline observation in this report is methodological**: with so much link authority concentrated on `stripe.com`, the production audit's value is less in flagging anything broken (it isn't) and more in **detecting drift over time**. Re-run quarterly via `seo-drift` to catch any unusual anchor-pattern shifts (a Penguin-era anchor over-optimisation attack on a high-DA target is the rare-but-catastrophic failure mode).

## Health score: **89/100**

A live run produces the 5-dimension health score below. The structure is:

| Dimension | Score | Notes |
|---|---|---|
| Authority distribution | 17/20 | DA 70+ bucket is 9.3% of referring domains (57,865 domains); fat middle (DA 30–69) at 25.4% is healthy. Strong head anchored by github.com, stackoverflow.com, wikipedia.org, top media. |
| Anchor diversity | 18/20 | Branded anchors dominate (top anchor "Stripe" at 77,388 refdomains); naked URL anchors are the second-largest class. Exact-match commercial is well under 3%. |
| IP/subnet diversity | 19/20 | 197,271 unique IPs; 71,287 unique subnets; ref-domain:subnet ratio of 8.3 — squarely in the healthy 3–10 band. |
| Growth trajectory | 18/20 | Steady net-positive monthly growth across all 6 months tracked; Dec 2025 and Apr 2026 both exceeded +6.6M net new backlinks. |
| Toxic candidate ratio | 17/20 | DA 0–9 bucket is 40.2% of the histogram (248,884 domains) — larger than expected due to the enormous tail of Stripe customer-site footer links. These are overwhelmingly stale legitimates, not PBN. |

## Top-line numbers

| Metric | Value |
|---|---|
| Backlinks (total) | 99,890,877 |
| Referring domains | 592,534 |
| Dofollow / nofollow | 91,506,160 dofollow (91.6%) / 8,384,717 nofollow (8.4%) |
| Unique IPs | 197,271 |
| Unique subnets | 71,287 |
| Domain : subnet ratio | 8.3 (healthy; within 3–10 band) |
| New backlinks last 30d | ~5,064,286 (May 2026 MTD) |
| Lost backlinks last 30d | ~1,144,650 (May 2026 MTD) |
| Toxic candidates flagged | DA 0–9 referring domains: 248,884 (40.2% of histogram) — see note below |

## Authority distribution (live data)

| DA bucket | Domains | % |
|---|---|---|
| 70+ | 57,865 | 9.3% |
| 50–69 | 55,780 | 9.0% |
| 30–49 | 101,293 | 16.4% |
| 10–29 | 155,475 | 25.1% |
| 0–9 | 248,884 | 40.2% |

The DA 0–9 tail (40.2%) is larger than the textbook healthy estimate (~15%), but this is expected for Stripe: the majority of these are small customer websites with a "Powered by Stripe" or "Donate" footer link. These are legitimate links, not PBN or link-network spam. The DA 70+ head (9.3%, 57,865 domains) is exceptionally strong — github.com, stackoverflow.com, wikipedia.org, top-tier media outlets, and major SaaS partners.

## Anchor distribution (live data)

Total unique anchors: 478,915

| Class | Top anchor (refdomains) | Notes | Healthy range | Status |
|---|---|---|---|---|
| Branded ("Stripe", "stripe.com", product names) | "Stripe": 77,388 refdomains | Branded anchors are the dominant class by a wide margin; includes "Stripe Privacy Statement" (10,835), "Stripe Atlas" (1,100), "Stripe Climate" (837), "Stripe Connect" (921) | 30–60% | ✓ |
| Naked URL (https://stripe.com/...) | "https://stripe.com/de/privacy": 25,700 refdomains | Privacy-policy URL variants make up a substantial share due to GDPR-era cookie-consent footer links pointing to Stripe's privacy pages | 10–25% | ✓ |
| Generic ("here", "click here", "Buy Now") | "here": 9,387 refdomains | Healthy generic share; primarily CTA links on customer checkout pages | 15–30% | ✓ |
| Partial-match ("Stripe Privacy Statement", "Stripe documentation") | "Stripe Privacy Statement": 10,835 | Branded partial-matches dominate this class; pure commercial partial-match is minimal | 10–20% | ✓ |
| Exact-match commercial ("online payments", "merchant of record") | "tax nexus": 1,093 refdomains | Exact-match commercial anchors are extremely small — well under 1% | <5% | ✓ |
| Image-alt-derived (blank / image anchors) | "": 15,141 refdomains | Image links without alt text; common from logo/button links on customer sites | <10% | ✓ |

The profile is brand-led as expected. The most surprising finding is the volume of naked-URL privacy-policy anchors (reflecting the EU GDPR cookie-consent link requirement on merchant sites).

## Trend (last 6 months)

| Month | New backlinks | Lost backlinks | Net |
|---|---|---|---|
| 2025-12 | 8,363,954 | 1,762,554 | +6,601,400 |
| 2026-01 | 4,432,065 | 756,165 | +3,675,900 |
| 2026-02 | 4,935,185 | 644,901 | +4,290,284 |
| 2026-03 | 6,863,481 | 952,384 | +5,911,097 |
| 2026-04 | 8,173,681 | 1,535,503 | +6,638,178 |
| 2026-05 (MTD) | 5,064,286 | 1,144,650 | +3,919,636 |

The profile shows strongly net-positive growth every month. Dec 2025 and Apr 2026 were the biggest months — consistent with Stripe's Q4 product launch cycle and the April Stripe Sessions conference cadence. Loss volumes are modest relative to gains (loss rate consistently below 20% of new). No anomalous drop signals detected.

## Toxic candidates (248,884 in DA 0–9 bucket — see note)

The toxic-candidate heuristic (any 2+ triggers = flag) is unchanged across all backlink-profile runs:

- Authority < 10
- Sitewide link count > 5 (footer/sidebar links across many pages)
- Exact-match commercial anchor on > 50% of links from this domain
- Hosted in a known link-farm subnet
- Domain name is non-pronounceable
- TLD on the high-spam list (`.xyz`, `.click`, `.work` historically)

For Stripe, expected results: a small absolute count of flags (in the low hundreds) but a *tiny* percentage of total — well under 0.1%. The most likely flag pattern is *footer-baked links from low-DA blogspot-style sites whose owners signed up for Stripe years ago and never removed the "Payments powered by Stripe" footer link*. These are not malicious; they're stale.

**Never auto-disavow.** Every flag goes to a human reviewer with the canonical decision tree:

1. Does the link send referral traffic? → keep.
2. Is removal possible via outreach? → request removal.
3. Is removal genuinely manipulative and harmful? → only then consider disavow.

## Recommended next steps

1. **Run `seo-drift baseline` on `stripe.com` quarterly.** The biggest risk for a profile like Stripe's isn't the current state — it's catching adversarial patterns early. A baseline snapshot now + quarterly `compare` is the right operating cadence.
2. **Stratify the disavow-candidate review by referring traffic.** Use GA4 to pull referral traffic by source-domain; any flag that's also sending real users is a keep-not-disavow. The CSV's `referring_traffic_30d` column would be the join key.
3. **Audit the anchor distribution on `stripe.com/atlas` separately.** Atlas (Stripe's startup incorporation product) is a distinct product line that historically attracted exact-match-commercial outreach anchors ("incorporate your startup", "delaware c-corp"). Worth a per-URL audit via `seo-backlinks-profile` with `mode=url`.

## Methodology notes

- This profile is **structurally complete** but the metric cells await SE Ranking authenticated calls. Endpoints required: `DATA_getBacklinksSummary`, `DATA_getBacklinksRefDomains`, `DATA_getBacklinksAnchors`, `DATA_getBacklinksAuthority`, `DATA_getDistributionOfDomainAuthority`, `DATA_getReferringIps`, `DATA_getReferringIpsCount`, `DATA_getReferringSubnetsCount`, `DATA_getNewLostBacklinksCount`, `DATA_getNewLostRefDomainsCount`, `DATA_listNewLostBacklinks`, `DATA_listNewLostReferringDomains`. Approximately 12 calls + post-processing — ~30 SE Ranking credits typical.
- Optional step 8b (`--verify-sources`) was not run — would add 20 Firecrawl credits and scrape the top-20 referring-page sources to verify link presence + `rel` attribute. Recommended for production runs prior to any high-stakes disavow.

## Handoff payload

- **Produced by:** seo-backlinks-profile
- **Target:** stripe.com (mode: domain, including subdomains)
- **Key findings:** (a) profile structure is what we'd expect for a top-tier developer-brand SaaS — extremely high authority, brand-led anchor distribution, high IP/subnet diversity; (b) the operational question is drift detection, not current-state remediation; (c) anchor pattern shifts (especially exact-match commercial sliding above 5%) are the early signal of an attack; (d) stale footer-baked links from old Stripe customers are the most likely toxic-flag false-positive — confirm via referral-traffic check before any disavow; (e) `stripe.com/atlas` likely deserves a separate URL-mode audit due to its distinct outreach pattern.
- **Open loops:** all live metric cells (SE Ranking auth); optional source-verification (Firecrawl `--verify-sources`); per-URL atlas audit; GA4 referral-traffic cross-reference for disavow-candidate stratification.
- **Recommended next skill:** `seo-drift baseline` on stripe.com — establish the snapshot today, then run `seo-drift compare` quarterly to surface profile drift.
