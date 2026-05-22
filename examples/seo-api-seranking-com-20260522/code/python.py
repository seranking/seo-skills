#!/usr/bin/env python3
"""Domain intelligence snapshot — seranking.com — SE Ranking Data API.

Read-only. 300 credits/run. Designed for a weekly cron job.
Pulls worldwide overview + organic competitors + backlink summary and
merges them into one JSON document for a dashboard / warehouse.
"""
import json
import os
import random
import sys
import time
from datetime import date

import requests

API_KEY = os.environ.get("SERANKING_API_KEY")
if not API_KEY:
    sys.exit("Set SERANKING_API_KEY")

BASE = "https://api.seranking.com/v1"
HEADERS = {"Authorization": f"Token {API_KEY}"}
DOMAIN = "seranking.com"
SOURCE = "us"
RUN_COST = 300  # 100 each: overview + competitors + backlinks


def call(method, path, *, params=None, json_body=None, max_attempts=5):
    """One Data API call with 429 backoff + terminal-403 handling."""
    delay = 1.0
    for _ in range(max_attempts):
        r = requests.request(
            method, f"{BASE}{path}",
            headers=HEADERS, params=params, json=json_body, timeout=30,
        )
        if r.status_code == 429:
            time.sleep(delay + random.uniform(-0.2, 0.2) * delay)
            delay *= 2
            continue
        if r.status_code == 403 and "Insufficient funds" in r.text:
            sys.exit("Out of credits — top up before retrying.")
        r.raise_for_status()
        return r.json()
    sys.exit(f"Rate-limited after {max_attempts} attempts on {path}")


def main():
    # 1 — Preflight (0 credits). units_left is the figure to forecast against.
    sub = call("GET", "/account/subscription")["subscription_info"]
    if sub["units_left"] < RUN_COST:
        sys.exit(f"Only {sub['units_left']} credits left; run needs {RUN_COST}.")

    # 2 — Worldwide overview (100 credits).
    overview = call("GET", "/domain/overview/worldwide",
                    params={"domain": DOMAIN, "currency": "USD"})

    # 3 — Organic competitors, US (100 credits; up to 500 rows).
    competitors = call("GET", "/domain/competitors",
                       params={"source": SOURCE, "domain": DOMAIN, "type": "organic"})

    # 4 — Backlink summary, domain mode (100 credits).
    backlinks = call("POST", "/backlinks/summary",
                     json_body={"target": DOMAIN, "mode": "domain"})

    rows = competitors.get("data", competitors) if isinstance(competitors, dict) else competitors
    snapshot = {
        "domain": DOMAIN,
        "captured": date.today().isoformat(),
        "credits_left": sub["units_left"],
        "overview": overview,
        "top_competitors": rows[:15],
        "backlinks": backlinks["summary"][0],
    }
    out = f"snapshot-{DOMAIN}-{date.today():%Y%m%d}.json"
    with open(out, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
