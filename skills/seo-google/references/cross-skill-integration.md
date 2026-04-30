# Cross-skill integration: enriching other skills with real Google field data

This file is the contract other skills follow to enrich their deliverables with Google-API field data **without** spawning the full `seo-google` skill. Each enrichment is a single Python script call that returns JSON; the calling skill parses it and folds the data into its primary deliverable.

The pattern was adapted from `AgriciDaniel/claude-seo`'s wiring across `seo-audit`, `seo-technical`, and `seo-drift`. Config path is namespaced to `~/.config/seo-skills/` so the two plugins coexist cleanly.

## Trigger pattern (every enrichment-aware skill)

Add this near the top of the skill's Process steps, immediately after the existing preflight (credit balance / Firecrawl detection):

```
**Google data availability check.** Run `python3 scripts/google_auth.py --check --json`
and parse the result. If `tier >= 0` (any creds present), Google enrichment runs in step
N (see below). If `tier == -1` or the file is missing, the skill proceeds without
Google enrichment and notes "Google field data: not configured (run `bash extensions/google/install.sh`)" in the deliverable.
```

The `google_auth.py --check --json` output shape:

```json
{
  "tier": 1,
  "available": ["pagespeed", "crux", "crux-history", "gsc", "inspect", "sitemaps", "index"],
  "missing": ["ga4", "ga4-pages", "keywords", "volume"],
  "config_path": "/Users/.../.config/seo-skills/google-api.json"
}
```

The skill should branch on `available`. Each enrichment lists its required entry below.

## Per-skill enrichment recipes

### `seo-technical-audit` — CrUX field data + per-URL Inspection (Tier 0 + Tier 1)

Replaces the audit's lab-only CWV with actual Chrome user metrics from CrUX, and adds per-URL indexation reality from GSC URL Inspection.

**Step 8b — CrUX (Tier 0):**

```bash
# Domain-level CrUX (origin)
python3 scripts/pagespeed_check.py "https://{domain}" --crux-only --json

# 25-week trend (catches degradation we'd otherwise miss until next month's audit)
python3 scripts/crux_history.py "https://{domain}" --origin --json
```

Surface in `TECH-AUDIT.md` as "## Core Web Vitals (field data)" with p75 LCP / INP / CLS, source label "CrUX 28-day origin", and the 25-week trend direction.

If CrUX has no field data for the origin (low-traffic site), surface "CrUX: insufficient data for {domain}" and continue.

**Step 8c — Per-URL Inspection (Tier 1, mirrors theirs at `seo-technical/SKILL.md:164`):**

For each of the top 5 traffic URLs from step 5 (or homepage + key landing pages):

```bash
python3 scripts/gsc_inspect.py "{url}" --site-url "{config.default_property}" --json
```

Capture `indexStatusVerdict`, `coverageState`, `googleCanonical` vs `userCanonical`, and `lastCrawlTime`.

Cross-check against the audit's noindex / canonical findings:
- GSC says `INDEXED` but audit flagged `noindex` → audit is stale, flag for re-audit.
- GSC says `EXCLUDED` for a "healthy" page → hidden indexability issue invisible to SE Ranking's audit.
- `userCanonical ≠ googleCanonical` on a top-traffic page → elevated to Critical in the Top-10 fix list regardless of `severity-mapping.md` defaults.

Surface in `TECH-AUDIT.md` as "## Indexation reality check (GSC URL Inspection)" with one row per URL.

If property not verified in this account: "GSC: {domain} not verified — add it in Search Console" and skip 8c only (8b still runs).

### `seo-page` — GSC URL performance + URL Inspection (Tier 1 — `gsc`, `inspect` available)

Replaces inferred-from-SE-Ranking traffic with first-party Google data for the target URL.

```bash
# GSC search analytics for the URL (requires default_property in config to be set
# to a verified property that owns this URL — sc-domain:example.com)
python3 scripts/gsc_query.py --property "{config.default_property}" --url "{target_url}" --days 28 --json

# URL Inspection (real indexation status, canonical Google sees, last crawl date)
python3 scripts/gsc_inspect.py "{target_url}" --site-url "{config.default_property}" --json
```

Surface in `PAGE.md` "## Snapshot" as new rows:
- GSC last 28d: `{clicks} clicks / {impressions} impressions / {ctr}% CTR / pos {position}`
- Google sees: `index status: {INDEXED|EXCLUDED|...}`, canonical: `{userCanonical} → {googleCanonical}`, last crawled: `{date}`

Feed into the verdict heuristic:
- `INDEXED` + impressions > 100 + position 4–10 → harden REFRESH (clear quick-win territory).
- `EXCLUDED` (any reason) → harden KILL or CONSOLIDATE.
- googleCanonical ≠ userCanonical → flag in PAGE.md as a critical issue regardless of verdict.

If the URL's domain isn't a verified GSC property, surface "GSC: {target_domain} not verified — add it in Search Console" and continue.

### `seo-content-audit` — GA4 organic traffic on the audited URL (Tier 2 — `ga4-pages` available)

Replaces estimated traffic with measured organic traffic for the audited URL.

```bash
python3 scripts/ga4_report.py --report top-pages --days 28 --json
```

Filter the result client-side for the audited URL's path. Surface in `VERDICT.md` "## Snapshot" alongside the existing AIO citation cross-check:
- GA4 organic last 28d: `{sessions} sessions / {users} users / avg engagement time {n}s`
- If the audited URL doesn't appear in the top-100 organic landing pages: "GA4: not in top-100 organic landing pages last 28d — low or zero traffic."

This is a *signal*, not a veto. Low GA4 traffic on a YMYL page with high E-E-A-T is informative ("we're not earning the visibility our content quality should support") but doesn't change the publish decision.

### `seo-drift` — CrUX-history + indexation drift + SSRF protection (Tier 0+1)

Three additions versus the bare-MCP drift run.

**SSRF protection (always, mirrors theirs at `seo-drift/SKILL.md:97`):**

Before any URL fetch (Firecrawl, WebFetch, Google APIs), validate via:

```python
from scripts.google_auth import validate_url
if not validate_url(target_url):
    abort("URL rejected: loopback, private IP, link-local, or metadata endpoint")
```

Or invoke as a one-liner:

```bash
python3 -c "from scripts.google_auth import validate_url; import sys; sys.exit(0 if validate_url('{url}') else 1)"
```

`validate_url()` (defined at `scripts/google_auth.py:366`) rejects: loopback (127.0.0.1, ::1, localhost), RFC1918 private ranges (10/8, 172.16/12, 192.168/16), link-local (169.254/16), and Google metadata endpoints. Refuses non-http(s) schemes.

**`--skip-cwv` flag** (mirrors theirs at `seo-drift/SKILL.md:107, 131`): skips the entire Google field-data snapshot (step 4b) even when `google-api.json` is configured. Useful when you only care about content/structural drift, or when CrUX rate-limit concerns outweigh CWV coverage.

**Field-data drift** (the actual enrichment):

```bash
# CWV drift over 25 weeks (origin or per-URL based on baseline scope)
python3 scripts/crux_history.py "{baseline_url_or_origin}" --json

# Indexation drift: re-run Inspection on each baselined URL and diff
python3 scripts/gsc_inspect.py "{url}" --site-url "{config.default_property}" --json
```

Compare against the previous baseline's stored CrUX + Inspection JSON. New drift triggers:
- LCP p75 increased ≥20% → red.
- INP p75 increased ≥20% → red.
- CLS p75 increased ≥0.05 absolute → yellow.
- FCP / TTFB p75 increased ≥30% → yellow.
- Inspection status changed from `INDEXED` to anything else → red.
- googleCanonical changed → yellow.
- last crawl date >60 days old → yellow.

Append to `DRIFT-REPORT.md` "## Field-data drift" section.

**Skip note when `--skip-cwv` was passed:** "Field-data drift: skipped — `--skip-cwv` flag passed at baseline (or this compare)."

### `seo-plan` — Phase-0 auto-spawn (any tier)

Plan composes other skills' outputs. If creds are present and the user hasn't already run `seo-google` in this session, Phase-0 should print:

```
> Google APIs detected (tier {n}). For real CWV / GSC / GA4 enrichment in
> downstream phases, run `seo-google {pagespeed,gsc,ga4-pages} <domain>`
> before re-running this plan. Continue without Google enrichment? (y/n)
```

If user continues, plan proceeds with SE Ranking data only and notes the limitation in PLAN.md. If user opts to run `seo-google` first, plan exits and re-runs after.

This is the lightest possible auto-spawn — plan doesn't dispatch the skill itself (transferring friction is theirs' anti-pattern we critiqued in EVAL_RESULT_v2.md), it just tells the user there's a richer path available.

## Failure modes (handle gracefully across all skills)

| Failure | Detection | Skill response |
|---|---|---|
| Config file missing | `google_auth.py --check` exits non-zero | Note "Google field data: not configured" and skip enrichment |
| API key invalid | Script returns `{"error": "API_KEY_INVALID"}` | Note "Google API key rejected — re-check `~/.config/seo-skills/google-api.json`" and skip |
| Property not verified (GSC) | `gsc_query.py` returns `{"error": "PROPERTY_NOT_VERIFIED"}` | Note "GSC property `{x}` not verified for this account" and skip GSC enrichment only |
| GA4 property not configured | `ga4_property_id` empty in config | Note "GA4: property ID not configured (Tier 2 setup required)" and skip GA4 only |
| Insufficient CrUX data | `pagespeed_check.py --crux-only` returns `{"crux": null}` | Note "CrUX: insufficient field data for `{url}` (low traffic)" and skip CrUX only |
| Rate-limit hit | Script returns HTTP 429 | Note "Google API rate-limit reached — try again in 1h" and skip the affected enrichment |

A skill **never** fails the run because Google enrichment failed. Enrichment is optional uplift; the SE Ranking-based deliverable always ships.

## Why this pattern (vs spawning `seo-google` as a sub-skill)

- One Python call per enrichment, returns JSON, parsed in-line — no extra agent context, no extra latency.
- Each skill stays self-contained; no orchestration logic in the calling skill.
- Failure-isolated: a failed Google call doesn't pollute the SE Ranking-based primary deliverable.
- Mirrors the upstream wiring (`AgriciDaniel/claude-seo`'s `seo-technical/SKILL.md:164` invokes the same scripts directly).
