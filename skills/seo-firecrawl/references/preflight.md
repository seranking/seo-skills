# Shared preflight contract for analysis skills

> Shared preflight contract for analysis skills. v2.7.1+. Mirror this pattern; don't reimplement.

Every analysis skill in this catalogue runs the same 3-stage preflight at the start of its Process section. This file is the single source of truth — skills should reference it from their step 1 (or Prerequisites) rather than inlining the full prose.

The pattern was duplicated 6+ times across SKILL.md files until v2.7.0; centralised in v2.7.1 so a doc fix lands in one place.

## The 3-stage preflight

### Stage A — SE Ranking credit balance (`DATA_getCreditBalance`)

Call `DATA_getCreditBalance` before running anything that costs SE Ranking credits. Surface the result and the per-skill estimate to the user before continuing, in this canonical shape:

```
Remaining: {n} credits. Estimated cost: ~{n} credits. Continue? (y/N)
```

The estimate is skill-specific — each skill cites its own figure in its step 1 reference (see "How to reference this from a skill" below).

If the remaining balance is below the estimate, surface the shortfall and stop — don't run a partial pass.

### Stage B — Firecrawl availability (`mcp__firecrawl-mcp__firecrawl_scrape`)

Check whether `mcp__firecrawl-mcp__firecrawl_scrape` is connected. The branch is the same in every skill that uses Firecrawl:

- **If available → enriched path.** Run the Firecrawl-using steps as documented in the skill. Surface the projected Firecrawl cost (typically 1 credit per URL scraped, varies by mode — see `seo-firecrawl/SKILL.md` § "Cost estimation").
- **If unavailable → degraded path.** The skill still runs on WebFetch + SE Ranking data. The Firecrawl-only deliverable lines emit `(skipped — Firecrawl not installed)` notes; skill-specific caveats (lower-confidence schema detection, missing canonical/robots/og:* recovery, etc.) are documented in the skill's own step descriptions.
- **`--no-firecrawl` flag.** User may pass `--no-firecrawl` to force the degraded path even when Firecrawl is available — useful for credit conservation.

When unavailable, also surface the install hint: `bash extensions/firecrawl/install.sh` (free tier 500 credits/month — see `seo-firecrawl/SKILL.md`).

### Stage C — Google APIs (`python3 scripts/google_auth.py --check --json`)

Run `python3 scripts/google_auth.py --check --json` and parse the result.

- **If `tier >= 0`** (any creds present): the skill branches into the per-tier enrichment recipes documented in `skills/seo-google/references/cross-skill-integration.md`. Each enrichment-aware skill has its own section there listing which tier unlocks which step.
- **If `tier == -1`** or the file is missing: the skill proceeds without Google enrichment and notes `Google enrichment: not configured (run `bash extensions/google/install.sh`)` in the deliverable.

This stage **defers entirely** to `skills/seo-google/references/cross-skill-integration.md` for per-tier branches, failure handling, and the per-skill enrichment recipes — don't duplicate that contract here.

## Failure-mode table

Mirror the cross-skill-integration table for the Google stage; the Firecrawl + credit-balance rows are this skill's own additions.

| Failure | Detection | Skill response |
|---|---|---|
| Credit balance call fails | `DATA_getCreditBalance` returns error or non-200 | Note "SE Ranking credit balance unavailable — proceeding without preflight cost estimate; surface actual cost in deliverable" and continue. **Never** fail the run on this — credit data is a courtesy, not a gate. |
| Credit balance below estimate | `remaining < estimated_cost` | Surface the shortfall; ask the user whether to proceed with a reduced scope (e.g. lower URL cap, lite mode) or top up credits before re-running. |
| Firecrawl MCP not installed | `mcp__firecrawl-mcp__firecrawl_scrape` not in available tools | Note "Firecrawl not installed — degraded path active; install via `bash extensions/firecrawl/install.sh`" and run the WebFetch-only path. |
| Firecrawl rate-limit hit | Firecrawl response 429 | Note "Firecrawl rate-limit reached — falling back to WebFetch for remaining URLs" and continue degraded for the rest of the run. Do not retry in a tight loop. |
| Firecrawl Cloudflare/anti-bot block | Firecrawl response 403 / "blocked by WAF" | Note the affected URL and the block reason in the deliverable, then continue. Defeating WAFs is out of scope. |
| Google config file missing | `google_auth.py --check` exits non-zero | Note "Google field data: not configured" and skip enrichment. |
| Google API key invalid | Script returns `{"error": "API_KEY_INVALID"}` | Note "Google API key rejected — re-check `~/.config/seo-skills/google-api.json`" and skip. |
| GSC property not verified | `gsc_query.py` returns `{"error": "PROPERTY_NOT_VERIFIED"}` | Note "GSC property `{x}` not verified for this account" and skip GSC enrichment only. |
| GA4 property not configured | `ga4_property_id` empty in config | Note "GA4: property ID not configured (Tier 2 setup required)" and skip GA4 only. |
| Insufficient CrUX data | `pagespeed_check.py --crux-only` returns `{"crux": null}` | Note "CrUX: insufficient field data for `{url}` (low traffic)" and skip CrUX only. |
| Google API rate-limit hit | Script returns HTTP 429 | Note "Google API rate-limit reached — try again in 1h" and skip the affected enrichment. |

A skill **never** fails the run because preflight enrichment failed. Enrichment is optional uplift; the SE Ranking-based deliverable always ships.

## How to reference this from a skill

In the skill's Prerequisites or Process step 1, replace the verbose 3-block preflight prose with this canonical reference:

```
1. **Validate target & preflight.** See `skills/seo-firecrawl/references/preflight.md` for the canonical 3-stage preflight (credit balance, Firecrawl availability, Google APIs). Skill-specific notes:
   - Estimated SE Ranking cost for this skill: ~{N} credits ({describe scope}).
   - Firecrawl: {required | optional with WebFetch fallback | not used}, ~{N} credits if available.
   - Google APIs: {tier required for which enrichment step, or "not used"}.
```

Skill-specific notes preserve the bits that vary per skill (cost figures, Firecrawl scope, Google API tier) — the verbose preflight prose is centralised here.
