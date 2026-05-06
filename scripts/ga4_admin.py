#!/usr/bin/env python3
"""
GA4 Admin API v1beta - account/property discovery.

Lists the GA4 accounts and properties the configured service account can read,
so users don't have to hunt for property IDs in the GA4 Admin UI.

Usage:
    python ga4_admin.py properties
    python ga4_admin.py properties --json
"""

import argparse
import json
import sys
from typing import Optional

try:
    from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
except ImportError:
    print(
        "Error: google-analytics-admin required. "
        "Install with: pip install google-analytics-admin",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    from google_auth import get_oauth_credentials
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from google_auth import get_oauth_credentials

GA4_ADMIN_SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


def _build_admin_client():
    credentials = get_oauth_credentials(GA4_ADMIN_SCOPES)
    if not credentials:
        return None
    try:
        return AnalyticsAdminServiceClient(credentials=credentials)
    except Exception as e:
        print(f"Error building GA4 Admin client: {e}", file=sys.stderr)
        return None


def list_properties() -> dict:
    """
    Enumerate every GA4 account and property the credentials can see.

    Mirrors the GA4 UI's "All accounts > Property" picker. Each property entry
    includes the numeric property_id (the value to pass as `--property` to
    ga4_report.py) and its display name and timezone.
    """
    result = {
        "accounts": [],
        "property_count": 0,
        "error": None,
    }

    client = _build_admin_client()
    if not client:
        result["error"] = (
            "Could not build GA4 Admin client. Ensure the service account has "
            "Viewer access on the relevant GA4 properties (Admin > Property "
            "Access Management) and that the Google Analytics Admin API is "
            "enabled in your Cloud project."
        )
        return result

    try:
        page = client.list_account_summaries()
        for acct in page:
            account_entry = {
                "account": acct.account,
                "display_name": acct.display_name,
                "properties": [],
            }
            for prop in acct.property_summaries:
                # `prop.property` is "properties/123456789" — split for the
                # numeric ID since that's what users paste into the data API.
                numeric_id = prop.property.split("/", 1)[-1] if prop.property else None
                account_entry["properties"].append({
                    "property": prop.property,
                    "property_id": numeric_id,
                    "display_name": prop.display_name,
                    "property_type": getattr(prop, "property_type", None) and str(prop.property_type),
                    "parent": getattr(prop, "parent", None),
                })
                result["property_count"] += 1
            result["accounts"].append(account_entry)
    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            result["error"] = (
                "Permission denied. Either the Google Analytics Admin API is "
                "not enabled in your Cloud project, or the service account "
                "isn't a Viewer on any GA4 property."
            )
        else:
            result["error"] = f"GA4 Admin API error: {e}"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="GA4 Admin API - account/property discovery"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="properties",
        choices=["properties"],
        help="Command (default: properties)",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = list_properties()

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        if not args.json:
            sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return

    print(f"=== GA4 Properties Visible to Service Account ===")
    print(f"Accounts: {len(result.get('accounts', []))} | Properties: {result.get('property_count', 0)}\n")
    for acct in result.get("accounts", []):
        print(f"{acct['display_name']}  ({acct['account']})")
        for prop in acct["properties"]:
            print(f"  - {prop['display_name']}  →  property_id={prop['property_id']}")
        print()


if __name__ == "__main__":
    main()
