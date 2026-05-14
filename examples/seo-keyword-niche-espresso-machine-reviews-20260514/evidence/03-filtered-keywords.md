# 03 — Filtered keywords (post min-vol / max-kd filter)

> Source: filter step over the longtail + question + related expansion. Pending SE Ranking auth for live volumes.

## Filter applied

- `min_volume = 50/mo`
- `max_kd = 40`
- Strip branded keywords for brands the publisher doesn't own (unless the user supplied a branded seed).
- De-duplicate across seeds.
- Tag with intent (I=Informational, C=Commercial, T=Transactional, N=Navigational).

## Expected post-filter count

- Pre-filter (raw expansion + questions + related): ~2,000–3,000 keywords total.
- Post-filter (volume ≥ 50, KD ≤ 40, intent-tagged, de-duplicated): ~400–700 keywords.

## Intent distribution (qualitative — what to expect)

| Intent | Expected share |
|---|---:|
| Commercial (C) | ~55% |
| Informational (I) | ~30% |
| Transactional (T) | ~10% |
| Navigational (N) | ~5% |

Commercial dominates because "espresso machine reviews" is itself a commercial-intent seed. Informational shows up via the question keywords. Transactional is small because espresso machines aren't typically purchased via direct-search ("buy breville barista express" is lower-volume than "breville barista express review").

## Pending

Live keyword set + tagged intents on next run.
