# Local citation sources by vertical

Reference list for step 9 of `seo-local` (citation-presence sample via WebSearch). Use this to pick the 8 directories to sample for the detected vertical: 6 Tier-1 universal + 2 vertical-specific.

The list is curated to directories that meaningfully drive local-pack visibility, GBP verification trust, or AI-search source coverage (ChatGPT pulls from Yelp / TripAdvisor / BBB / Reddit; Bing Places powers ChatGPT, Copilot, Alexa). Long-tail directories below the surface here have low-to-zero ranking impact and contribute to the diminishing-returns curve.

## Tier 1 universal (always sample these 6)

| Directory | site: pattern | Why it matters |
|---|---|---|
| Google Business Profile | `site:google.com/maps "{business name}"` | The primary local-pack signal; verifies legitimacy. |
| Yelp | `site:yelp.com "{business name}"` | High Domain Authority; ChatGPT sources from it. |
| Facebook | `site:facebook.com "{business name}"` | Brand presence + reviews; Apple Maps may pull from FB. |
| BBB | `site:bbb.org "{business name}"` | Google uses BBB for verification signals; consumer-trust marker. |
| Apple Business Connect | `site:maps.apple.com "{business name}"` | Apple Maps data; usage doubled to 27% of consumers (BrightLocal 2026). |
| Bing Places | `site:bing.com/maps "{business name}"` | Powers ChatGPT, Copilot, Alexa local recommendations. |

## Vertical-specific (pick the top 2 for the detected vertical)

### Restaurant
- TripAdvisor — `site:tripadvisor.com "{name}"` — primary travel/dining citation, ChatGPT source.
- OpenTable — `site:opentable.com "{name}"` — reservation signal + listing.
- Zomato — `site:zomato.com "{name}"` — international restaurant directory.
- Grubhub / DoorDash / Uber Eats — service-platform listings (one of these is usually fine).

### Healthcare
- Healthgrades — `site:healthgrades.com "{name}"` — primary healthcare directory.
- Vitals — `site:vitals.com "{name}"` — physician reviews.
- WebMD — `site:doctor.webmd.com "{name}"` — practitioner profile.
- Zocdoc — `site:zocdoc.com "{name}"` — appointment booking platform.
- (HIPAA caveat: do NOT confirm/deny a reviewer is a patient in any owner response. Surface this in the deliverable if the user audits responses.)

### Legal
- Avvo — `site:avvo.com "{name}"` — primary legal directory.
- FindLaw — `site:findlaw.com "{name}"` — Thomson Reuters legal directory.
- Justia — `site:justia.com "{name}"` — free legal directory; high DA.
- Martindale-Hubbell — `site:martindale.com "{name}"` — peer-rated, attorney trust signal.
- (Bar admissions: cross-check with the state bar's lawyer-search portal.)

### Home Services
- Angi (formerly Angie's List) — `site:angi.com "{name}"` — primary home-services directory.
- HomeAdvisor — `site:homeadvisor.com "{name}"` — quote-request platform.
- Houzz — `site:houzz.com "{name}"` — design + home pros.
- Thumbtack — `site:thumbtack.com "{name}"` — local-services marketplace.
- Nextdoor — `site:nextdoor.com "{name}"` — hyperlocal recommendation engine.

### Real Estate
- Zillow — `site:zillow.com "{agent or brokerage}"` — primary RE platform.
- Realtor.com — `site:realtor.com "{name}"` — NAR official directory.
- Redfin — `site:redfin.com "{name}"` — agent profiles.
- Trulia — `site:trulia.com "{name}"` — Zillow-owned, separate listing.

### Automotive
- Cars.com — `site:cars.com "{dealership}"` — primary auto-dealer directory.
- AutoTrader — `site:autotrader.com "{dealership}"` — inventory + dealer pages.
- DealerRater — `site:dealerrater.com "{dealership}"` — auto-dealer-specific reviews.
- Edmunds — `site:edmunds.com "{dealership}"` — reviews + dealer profiles.
- Kelley Blue Book — `site:kbb.com "{dealership}"` — dealer search.

### Generic (no vertical detected)
- Yellow Pages — `site:yellowpages.com "{name}"` — long-running general directory.
- Foursquare — `site:foursquare.com "{name}"` — location data aggregator.
- Better Business Bureau — already in Tier 1.
- Manta — `site:manta.com "{name}"` — small-business directory.
- Mapquest — `site:mapquest.com "{name}"` — Apple Maps & Bing data partner.

## Data aggregators (recommendation, not WebSearch sample)

These power downstream distribution to dozens of smaller directories. Recommend submission rather than sampling — a "not detected" result on these via WebSearch isn't meaningful since they don't expose listings via search.

- **Data Axle** (formerly Infogroup) — feeds Apple Maps, Yelp, Yahoo, others.
- **Foursquare / Factual** — powers Snap Maps, Apple Maps, Square, Tripadvisor.
- **Neustar / TransUnion (Localeze)** — feeds Bing, Apple Maps, Yelp, Yahoo.

Surface in `LOCAL-SEO-REPORT.md` "Top fixes" → Medium: "Submit to Data Axle, Foursquare, Neustar/Localeze for distribution to downstream directories."

## What NOT to sample

- **Long-tail "free directory" lists** (e.g. Yellowbook, Hotfrog, Cylex). Low DA, near-zero local-pack impact, citation submission services optimise for these because they're cheap, not because they work.
- **Industry directories with no consumer traffic.** A directory with 100 visits/month moves nothing. Vet by searching the directory's name in Google Trends — if the directory isn't searched, the listing isn't discovered.
- **Paid-only directories at the discovery phase.** If the user needs to pay to even check whether they're listed, defer that to a paid citation tool (Whitespark, BrightLocal, Yext).

## Caveat on "site:" sampling

`site:directory.com "Business Name"` returns a hit when the listing's page is in Google's index AND the exact business name string appears on the page. False negatives:
- Business name has variations (e.g. "Joe's Plumbing" vs "Joe's Plumbing & Heating LLC") — try both formats.
- Listing exists but page is `noindex` (rare on big directories, common on smaller ones).
- Listing exists but the directory's index hasn't been crawled recently.

False positives:
- Another business with the same name is on the directory. Verify the city/region in the snippet.

The `LOCAL-SEO-REPORT.md` "Citation sample" section should always end with the line: *"Caveat: this is a sample, not a comprehensive citation audit. For definitive coverage, use Whitespark / BrightLocal / Yext."*
