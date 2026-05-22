#!/usr/bin/env bash
# Domain intelligence snapshot — seranking.com — SE Ranking Data API.
# Read-only. 300 credits/run. Designed to run weekly (cron).
set -euo pipefail

: "${SERANKING_API_KEY:?Set SERANKING_API_KEY to your SE Ranking API key}"
BASE="https://api.seranking.com/v1"
AUTH="Authorization: Token ${SERANKING_API_KEY}"
DOMAIN="seranking.com"
SOURCE="us"
STAMP="$(date +%Y%m%d)"

# 1 — Preflight: subscription + remaining credits (0 credits).
curl -fsS -X GET "${BASE}/account/subscription" \
  -H "${AUTH}" -o "subscription-${STAMP}.json"

# 2 — Worldwide overview: organic + paid footprint (100 credits).
curl -fsS -X GET "${BASE}/domain/overview/worldwide?domain=${DOMAIN}&currency=USD" \
  -H "${AUTH}" -o "overview-${STAMP}.json"

# 3 — Organic competitors, US database (100 credits; up to 500 rows).
curl -fsS -X GET "${BASE}/domain/competitors?source=${SOURCE}&domain=${DOMAIN}&type=organic" \
  -H "${AUTH}" -o "competitors-${STAMP}.json"

# 4 — Backlink profile summary, domain mode (100 credits).
curl -fsS -X POST "${BASE}/backlinks/summary" \
  -H "${AUTH}" -H "Content-Type: application/json" \
  -d "{\"target\":\"${DOMAIN}\",\"mode\":\"domain\"}" \
  -o "backlinks-${STAMP}.json"

echo "Snapshot written for ${STAMP}: subscription / overview / competitors / backlinks JSON."
