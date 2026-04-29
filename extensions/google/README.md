# Google APIs extension for `seo-skills`

Optional Google APIs integration that powers the `seo-google` skill — Search Console, PageSpeed Insights, CrUX field data, Indexing API, GA4, YouTube, NLP, Knowledge Graph, Web Risk, and Google Ads Keyword Planner. Without it, `seo-google` cannot run; the rest of the catalogue is unaffected.

> **Adapted from [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo)** (MIT). Scripts under `scripts/` are forks of the upstream `seo-google` skill, namespaced to `~/.config/seo-skills/` for clean coexistence with the original.

## What this enables

| Skill | What `seo-google` unlocks |
|---|---|
| `seo-google` | All 21 commands across PSI / CrUX / GSC / Indexing / GA4 / YouTube / NLP / Knowledge Graph / Web Risk / Keyword Planner / report generation. |
| `seo-technical-audit` | Real CWV field data from CrUX + Lighthouse lab via PSI; real indexation status via URL Inspection. |
| `seo-page` | Replaces SE Ranking traffic *estimates* with real GSC impressions/clicks/CTR/position; confirms indexation via URL Inspection. |
| `seo-drift` | Adds 25-week CrUX history trend + GSC delta tracking to baseline/compare snapshots. |
| `seo-sitemap` | Adds GSC-sitemap status (which sitemaps Google has actually consumed and their error/warning counts). |
| `seo-content-audit` | NLP entity/sentiment analysis enhances E-E-A-T scoring. |
| `seo-geo` | GSC Search Analytics with `dimensions=searchAppearance` includes AI Overview impressions. |
| `seo-keyword-cluster` / `seo-keyword-niche` | Tier-3 Keyword Planner volumes (gold-standard) replace SE Ranking estimates when configured. |
| `seo-plan` | Real impressions/clicks/conversions in the "Where you are" baseline when Tier 1+ is configured. |

## Requirements

- **Python 3.10+** (`python3 --version`).
- `pip` for python3 (`python3 -m pip --version`).
- A free Google Cloud project with the relevant APIs enabled. See `skills/seo-google/references/auth-setup.md` for the 8-step walkthrough.
- All Google APIs used here are **free** (with quotas — see "Rate limits" below).

## Install

```bash
bash extensions/google/install.sh
```

The script:

1. Verifies Python 3.10+ and pip.
2. `pip install --user --upgrade` of:
   - **Core**: `google-api-python-client`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-analytics-data`, `requests`.
   - **Reports** (matplotlib + weasyprint + openpyxl): optional. If system deps are missing (cairo/pango on Linux, Xcode CLT on macOS), the install warns and continues — only the `report` command becomes unavailable.
3. Creates `~/.config/seo-skills/` (700 mode) and writes a stub `google-api.json` (600 mode) the user fills in.
4. Runs the credential checker to report the unlocked tier.

After install, fill in `~/.config/seo-skills/google-api.json` per the [auth-setup walkthrough](../../skills/seo-google/references/auth-setup.md). Re-run the credential checker:

```bash
python3 scripts/google_auth.py --check
```

## Uninstall

```bash
bash extensions/google/uninstall.sh
```

Removes `~/.config/seo-skills/google-api.json` and `~/.config/seo-skills/oauth-token.json`. Does **not** uninstall pip libraries (they may be in use by other tools — uninstall manually if needed). Does **not** delete service-account JSON files referenced by `service_account_path`.

## Credential tiers

| Tier | What's configured | What's unlocked |
|------|-------------------|------------------|
| **0** | API key only | PSI, CrUX, CrUX History, YouTube, NLP, Knowledge Graph, Web Risk |
| **1** | + service account (added to GSC as "Full" user) | + GSC Search Analytics, URL Inspection, Sitemaps, Indexing API |
| **2** | + GA4 property ID + service account added as Viewer | + GA4 organic traffic and landing pages |
| **3** | + Google Ads developer token + customer ID | + Keyword Planner ideas + volumes |

Each tier is independently useful — Tier 0 alone gives you real CWV field data, which already justifies the install. Higher tiers unlock more.

## Rate limits

| API | Per-Minute | Per-Day | Auth |
|-----|-----------|---------|------|
| PageSpeed Insights v5 | 240 QPM | 25,000 QPD | API Key |
| CrUX + History | 150 QPM (shared) | Unlimited | API Key |
| GSC Search Analytics | 1,200 QPM/site | 30M QPD | Service Account |
| GSC URL Inspection | 600 QPM | **2,000 QPD/site** | Service Account |
| Indexing API | 380 RPM | **200 publish/day** | Service Account |
| GA4 Data API | 10 concurrent | ~25K tokens/day | Service Account |
| YouTube Data API v3 | — | 10,000 units/day | API Key |
| Cloud Natural Language | — | 5,000 units/month free | API Key (billing required) |

The two real budgets to watch are **GSC URL Inspection (2,000/day per site)** and **Indexing API (200 publish/day)** — both have hard daily caps that the scripts surface.

## Troubleshooting

- **`No credentials found`** after install: the stub config exists but fields are empty. Open `~/.config/seo-skills/google-api.json` and follow `skills/seo-google/references/auth-setup.md`.
- **`403 Forbidden` on GSC**: the service account email isn't added to the GSC property as a Full user. GSC > Settings > Users and permissions > Add user, paste `client_email`, set Full.
- **`403 Forbidden` on GA4**: the service account email isn't added to the GA4 property as Viewer. GA Admin > Property Access Management > Add users.
- **`404 Not Found` on CrUX**: the URL/origin has insufficient Chrome traffic for CrUX. Not an auth issue — fall back to PSI lab data.
- **`429 Rate Limit`**: wait and retry; check `references/rate-limits-quotas.md` for which API hit the cap.
- **`weasyprint` install fails on Linux**: install system deps first — `apt install libpango-1.0-0 libpangoft2-1.0-0`. On macOS, install Xcode Command Line Tools.
- **`API not enabled`**: enable the specific API in [Google Cloud Console > APIs & Services > Library](https://console.cloud.google.com/apis/library).

## License

MIT, same as the parent plugin. The forked Python scripts and reference docs preserve [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)'s MIT copyright (Copyright © 2026 AgriciDaniel) — see `LICENSE-AgriciDaniel.txt` in this directory.
