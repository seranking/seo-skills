#!/usr/bin/env python3
"""
GA4 Data API v1beta - organic traffic reporting.

Queries the Google Analytics Data API for organic search traffic,
top landing pages, and session metrics with channel filtering.

Usage:
    python ga4_report.py --property 123456789
    python ga4_report.py --property 123456789 --days 90 --report top-pages
    python ga4_report.py --property 123456789 --report organic --json
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Optional

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Filter,
        FilterExpression,
        FilterExpressionList,
        Metric,
        OrderBy,
        RunReportRequest,
    )
except ImportError:
    print(
        "Error: google-analytics-data required. "
        "Install with: pip install google-analytics-data",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    from google_auth import get_oauth_credentials, load_config
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from google_auth import get_oauth_credentials, load_config

GA4_SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

# Hostnames GA4 stores in `sessionSource` for AI assistants. Grouped by vendor;
# legacy hostnames (chat.openai.com, bard.google.com) included since historical
# sessions still carry those values.
AI_REFERRAL_SOURCES = [
    # OpenAI
    "chatgpt.com",
    "chat.openai.com",
    # Anthropic
    "claude.ai",
    # Google
    "gemini.google.com",
    "bard.google.com",
    # Microsoft
    "copilot.microsoft.com",
    # Perplexity
    "perplexity.ai",
    # Alibaba (Qwen / Tongyi)
    "chat.qwen.ai",
    "qwen.com",
    "tongyi.aliyun.com",
    # Mistral (Le Chat)
    "chat.mistral.ai",
    # DeepSeek
    "chat.deepseek.com",
    # xAI (Grok)
    "grok.com",
    "x.ai",
    # Smaller / aggregators
    "you.com",
    "phind.com",
    "poe.com",
]


def _build_ga4_client():
    """Build the GA4 BetaAnalyticsDataClient."""
    credentials = get_oauth_credentials(GA4_SCOPES)
    if not credentials:
        return None
    try:
        return BetaAnalyticsDataClient(credentials=credentials)
    except Exception as e:
        print(f"Error building GA4 client: {e}", file=sys.stderr)
        return None


def _resolve_property(property_id: str) -> str:
    """Ensure property ID is in the correct format."""
    if not property_id:
        return ""
    if property_id.startswith("properties/"):
        return property_id
    return f"properties/{property_id}"


def _normalize_page(page: Optional[str]) -> Optional[str]:
    """Strip protocol+host from a full URL, leaving the path GA4 stores in `landingPage`."""
    if not page:
        return None
    if "://" in page:
        from urllib.parse import urlparse
        parsed = urlparse(page)
        return parsed.path or "/"
    return page


def _page_filter(page: Optional[str]) -> Optional[FilterExpression]:
    """Build a `landingPage` EXACT filter, or None if page is empty."""
    if not page:
        return None
    return FilterExpression(
        filter=Filter(
            field_name="landingPage",
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.EXACT,
                value=page,
            ),
        )
    )


def _combine_and(*expressions: Optional[FilterExpression]) -> Optional[FilterExpression]:
    """AND-combine FilterExpressions, dropping None values. Returns None if all None."""
    valid = [e for e in expressions if e is not None]
    if not valid:
        return None
    if len(valid) == 1:
        return valid[0]
    return FilterExpression(and_group=FilterExpressionList(expressions=valid))


def organic_traffic_report(
    property_id: str,
    days: int = 28,
    limit: int = 100,
    page: Optional[str] = None,
    channel: Optional[str] = "Organic Search",
) -> dict:
    """
    Generate a daily-time-series traffic report from GA4.

    Defaults to organic-only for backward compatibility, but pass `channel=None`
    to drop the channel filter (all-channels view — required to reproduce the
    "weekly trend across the whole post" use case where most traffic is Direct
    or Referral, not Organic Search).

    Args:
        property_id: GA4 property ID (numeric or 'properties/123456789').
        days: Number of days to query (default: 28).
        limit: Max rows for the top-pages query (default: 100).
        page: Optional landing page path (or full URL — host stripped) to scope
              the report to a single entry page.
        channel: sessionDefaultChannelGroup value to filter on (default
                 "Organic Search"). Pass None for all channels.

    Returns:
        Dictionary with daily_data, top_pages, totals, and quota usage.
    """
    page_norm = _normalize_page(page)
    result = {
        "property": property_id,
        "report": "organic_traffic",
        "page_filter": page_norm,
        "channel_filter": channel,
        "date_range": None,
        "totals": {},
        "daily_data": [],
        "top_pages": [],
        "quota_tokens_used": None,
        "error": None,
    }

    client = _build_ga4_client()
    if not client:
        result["error"] = (
            "Could not build GA4 client. Ensure the service account has "
            "Viewer access in GA4 Admin > Property Access Management."
        )
        return result

    prop = _resolve_property(property_id)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result["date_range"] = {"start": start_date, "end": end_date}

    channel_filter_expr = (
        FilterExpression(
            filter=Filter(
                field_name="sessionDefaultChannelGroup",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.EXACT,
                    value=channel,
                ),
            )
        )
        if channel
        else None
    )
    dim_filter = _combine_and(channel_filter_expr, _page_filter(page_norm))

    # Daily organic sessions
    try:
        daily_request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="bounceRate"),
                Metric(name="averageSessionDuration"),
                Metric(name="engagementRate"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
            limit=days + 5,
            return_property_quota=True,
        )

        daily_response = client.run_report(daily_request)

        for row in daily_response.rows:
            result["daily_data"].append({
                "date": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "pageviews": int(row.metric_values[2].value),
                "bounce_rate": round(float(row.metric_values[3].value) * 100, 1),
                "avg_session_duration": round(float(row.metric_values[4].value), 1),
                "engagement_rate": round(float(row.metric_values[5].value) * 100, 1),
            })

        # Quota info
        if daily_response.property_quota:
            pq = daily_response.property_quota
            result["quota_tokens_used"] = {
                "daily_consumed": pq.tokens_per_day.consumed if pq.tokens_per_day else None,
                "daily_remaining": pq.tokens_per_day.remaining if pq.tokens_per_day else None,
                "hourly_consumed": pq.tokens_per_hour.consumed if pq.tokens_per_hour else None,
                "hourly_remaining": pq.tokens_per_hour.remaining if pq.tokens_per_hour else None,
            }

    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            result["error"] = (
                f"Permission denied for property '{property_id}'. "
                "Add the service account email as Viewer in "
                "GA4 Admin > Property Access Management."
            )
        elif "404" in error_str or "NOT_FOUND" in error_str:
            result["error"] = (
                f"Property '{property_id}' not found. "
                "Verify the numeric property ID in GA4 Admin > Property Details."
            )
        else:
            result["error"] = f"GA4 API error: {e}"
        return result

    # Top landing pages by organic sessions
    try:
        pages_request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="landingPage")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="bounceRate"),
                Metric(name="engagementRate"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[
                OrderBy(
                    metric=OrderBy.MetricOrderBy(metric_name="sessions"),
                    desc=True,
                )
            ],
            limit=limit,
        )

        pages_response = client.run_report(pages_request)

        for row in pages_response.rows:
            result["top_pages"].append({
                "landing_page": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "pageviews": int(row.metric_values[2].value),
                "bounce_rate": round(float(row.metric_values[3].value) * 100, 1),
                "engagement_rate": round(float(row.metric_values[4].value) * 100, 1),
            })

    except Exception as e:
        # Non-fatal: daily data succeeded, pages failed
        result["pages_error"] = f"Error fetching top pages: {e}"

    # Calculate totals
    if result["daily_data"]:
        total_sessions = sum(d["sessions"] for d in result["daily_data"])
        total_users = sum(d["users"] for d in result["daily_data"])
        total_pageviews = sum(d["pageviews"] for d in result["daily_data"])
        result["totals"] = {
            "sessions": total_sessions,
            "users": total_users,
            "pageviews": total_pageviews,
            "avg_daily_sessions": round(total_sessions / len(result["daily_data"]), 1),
        }

    return result


def top_pages_report(
    property_id: str,
    days: int = 28,
    limit: int = 50,
    page: Optional[str] = None,
    channel: Optional[str] = "Organic Search",
) -> dict:
    """
    Get top landing pages from GA4 for a given channel (default Organic Search).

    Args:
        property_id: GA4 property ID.
        days: Number of days.
        limit: Max pages to return.
        page: Optional landing-page filter (degenerate — collapses to one row).
        channel: sessionDefaultChannelGroup value (default "Organic Search").
                 Pass None for all channels.

    Returns:
        Dictionary with top pages ranked by sessions for the chosen channel.
    """
    report = organic_traffic_report(
        property_id, days, limit, page=page, channel=channel
    )
    return {
        "property": property_id,
        "report": "top_pages",
        "page_filter": report.get("page_filter"),
        "channel_filter": report.get("channel_filter"),
        "date_range": report.get("date_range"),
        "pages": report.get("top_pages", []),
        "total_sessions": report.get("totals", {}).get("sessions", 0),
        "quota_tokens_used": report.get("quota_tokens_used"),
        "error": report.get("error"),
    }


def device_breakdown(
    property_id: str,
    days: int = 28,
    page: Optional[str] = None,
) -> dict:
    """
    Organic sessions broken down by device category.

    Args:
        property_id: GA4 property ID.
        days: Number of days.
        page: Optional landing-page filter.

    Returns:
        Dictionary with device breakdown data.
    """
    page_norm = _normalize_page(page)
    result = {
        "property": property_id,
        "report": "device_breakdown",
        "page_filter": page_norm,
        "devices": [],
        "error": None,
    }

    client = _build_ga4_client()
    if not client:
        result["error"] = "Could not build GA4 client."
        return result

    prop = _resolve_property(property_id)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result["date_range"] = {"start": start_date, "end": end_date}

    organic_filter = FilterExpression(
        filter=Filter(
            field_name="sessionDefaultChannelGroup",
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.EXACT,
                value="Organic Search",
            ),
        )
    )
    dim_filter = _combine_and(organic_filter, _page_filter(page_norm))

    try:
        request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="deviceCategory")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="bounceRate"),
                Metric(name="engagementRate"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        )
        response = client.run_report(request)
        for row in response.rows:
            result["devices"].append({
                "category": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "bounce_rate": round(float(row.metric_values[2].value) * 100, 1),
                "engagement_rate": round(float(row.metric_values[3].value) * 100, 1),
            })
    except Exception as e:
        result["error"] = f"GA4 device breakdown error: {e}"

    return result


def country_breakdown(
    property_id: str,
    days: int = 28,
    limit: int = 20,
    page: Optional[str] = None,
) -> dict:
    """
    Organic sessions broken down by country.

    Args:
        property_id: GA4 property ID.
        days: Number of days.
        limit: Max countries to return.
        page: Optional landing-page filter.

    Returns:
        Dictionary with country breakdown data.
    """
    page_norm = _normalize_page(page)
    result = {
        "property": property_id,
        "report": "country_breakdown",
        "page_filter": page_norm,
        "countries": [],
        "error": None,
    }

    client = _build_ga4_client()
    if not client:
        result["error"] = "Could not build GA4 client."
        return result

    prop = _resolve_property(property_id)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result["date_range"] = {"start": start_date, "end": end_date}

    organic_filter = FilterExpression(
        filter=Filter(
            field_name="sessionDefaultChannelGroup",
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.EXACT,
                value="Organic Search",
            ),
        )
    )
    dim_filter = _combine_and(organic_filter, _page_filter(page_norm))

    try:
        request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="country")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=limit,
        )
        response = client.run_report(request)
        for row in response.rows:
            result["countries"].append({
                "country": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
            })
    except Exception as e:
        result["error"] = f"GA4 country breakdown error: {e}"

    return result


def referrals_report(
    property_id: str,
    days: int = 28,
    limit: int = 100,
    sources: Optional[list] = None,
    page: Optional[str] = None,
) -> dict:
    """
    Referral sessions report from GA4, optionally filtered to specific source hostnames.

    Captures third-party referrer traffic — useful for measuring AI-assistant referral
    traffic (chatgpt.com, perplexity.ai, gemini.google.com, etc.) as a reality check
    against AI Search visibility data from SE Ranking / GSC.

    Args:
        property_id: GA4 property ID.
        days: Number of days to query.
        limit: Max rows.
        sources: Explicit list of source hostnames. If None, no source filter is
                 applied and the result is scoped to the Referral channel group.
        page: Optional landing-page filter — answers "how much AI traffic did THIS
              specific page get?" rather than domain-wide.

    Returns:
        Dictionary with per-source breakdown, totals, and quota usage.
    """
    page_norm = _normalize_page(page)
    result = {
        "property": property_id,
        "report": "referrals",
        "sources_filter": sources,
        "page_filter": page_norm,
        "date_range": None,
        "totals": {},
        "sources": [],
        "quota_tokens_used": None,
        "error": None,
    }

    client = _build_ga4_client()
    if not client:
        result["error"] = (
            "Could not build GA4 client. Ensure the service account has "
            "Viewer access in GA4 Admin > Property Access Management."
        )
        return result

    prop = _resolve_property(property_id)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result["date_range"] = {"start": start_date, "end": end_date}

    if sources:
        # Explicit hostname list — filter by sessionSource directly. Don't AND with
        # the Referral channel group: a configured source may be classified as
        # Organic Search or Direct depending on UTM tagging, and the user wants
        # all sessions from those hostnames.
        source_filter = FilterExpression(
            filter=Filter(
                field_name="sessionSource",
                in_list_filter=Filter.InListFilter(values=sources),
            )
        )
    else:
        source_filter = FilterExpression(
            filter=Filter(
                field_name="sessionDefaultChannelGroup",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.EXACT,
                    value="Referral",
                ),
            )
        )
    dim_filter = _combine_and(source_filter, _page_filter(page_norm))

    try:
        request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="sessionSource")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="bounceRate"),
                Metric(name="engagementRate"),
                Metric(name="averageSessionDuration"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[
                OrderBy(
                    metric=OrderBy.MetricOrderBy(metric_name="sessions"),
                    desc=True,
                )
            ],
            limit=limit,
            return_property_quota=True,
        )
        response = client.run_report(request)

        for row in response.rows:
            result["sources"].append({
                "source": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "pageviews": int(row.metric_values[2].value),
                "bounce_rate": round(float(row.metric_values[3].value) * 100, 1),
                "engagement_rate": round(float(row.metric_values[4].value) * 100, 1),
                "avg_session_duration": round(float(row.metric_values[5].value), 1),
            })

        if response.property_quota:
            pq = response.property_quota
            result["quota_tokens_used"] = {
                "daily_consumed": pq.tokens_per_day.consumed if pq.tokens_per_day else None,
                "daily_remaining": pq.tokens_per_day.remaining if pq.tokens_per_day else None,
                "hourly_consumed": pq.tokens_per_hour.consumed if pq.tokens_per_hour else None,
                "hourly_remaining": pq.tokens_per_hour.remaining if pq.tokens_per_hour else None,
            }

    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            result["error"] = (
                f"Permission denied for property '{property_id}'. "
                "Add the service account email as Viewer in "
                "GA4 Admin > Property Access Management."
            )
        elif "404" in error_str or "NOT_FOUND" in error_str:
            result["error"] = (
                f"Property '{property_id}' not found. "
                "Verify the numeric property ID in GA4 Admin > Property Details."
            )
        else:
            result["error"] = f"GA4 API error: {e}"
        return result

    if result["sources"]:
        total_sessions = sum(s["sessions"] for s in result["sources"])
        total_users = sum(s["users"] for s in result["sources"])
        total_pageviews = sum(s["pageviews"] for s in result["sources"])
        result["totals"] = {
            "sessions": total_sessions,
            "users": total_users,
            "pageviews": total_pageviews,
            "source_count": len(result["sources"]),
        }

    return result


def channel_mix_report(
    property_id: str,
    days: int = 28,
    limit: int = 20,
    page: Optional[str] = None,
) -> dict:
    """
    Sessions broken down by `sessionDefaultChannelGroup` — Direct, Organic Search,
    Referral, Paid Search, Organic Social, etc.

    No channel filter is applied: this is the diagnostic view for "where does
    traffic to this page actually come from?". AI-assistant traffic frequently
    lands in `Direct` (uncredited) rather than `Referral`, so a high Direct share
    on a page that's recent and content-heavy is itself a signal.

    Args:
        property_id: GA4 property ID.
        days: Number of days.
        limit: Max channel groups (typically <10 distinct values exist).
        page: Optional landing-page filter to scope to a single entry page.

    Returns:
        Dictionary with per-channel sessions/users/engagement metrics, totals,
        and per-channel share-of-sessions percentages.
    """
    page_norm = _normalize_page(page)
    result = {
        "property": property_id,
        "report": "channel_mix",
        "page_filter": page_norm,
        "date_range": None,
        "totals": {},
        "channels": [],
        "quota_tokens_used": None,
        "error": None,
    }

    client = _build_ga4_client()
    if not client:
        result["error"] = (
            "Could not build GA4 client. Ensure the service account has "
            "Viewer access in GA4 Admin > Property Access Management."
        )
        return result

    prop = _resolve_property(property_id)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    result["date_range"] = {"start": start_date, "end": end_date}

    dim_filter = _page_filter(page_norm)

    try:
        request = RunReportRequest(
            property=prop,
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="engagementRate"),
                Metric(name="averageSessionDuration"),
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=dim_filter,
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=limit,
            return_property_quota=True,
        )
        response = client.run_report(request)

        for row in response.rows:
            result["channels"].append({
                "channel": row.dimension_values[0].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
                "pageviews": int(row.metric_values[2].value),
                "engagement_rate": round(float(row.metric_values[3].value) * 100, 1),
                "avg_session_duration": round(float(row.metric_values[4].value), 1),
            })

        if response.property_quota:
            pq = response.property_quota
            result["quota_tokens_used"] = {
                "daily_consumed": pq.tokens_per_day.consumed if pq.tokens_per_day else None,
                "daily_remaining": pq.tokens_per_day.remaining if pq.tokens_per_day else None,
                "hourly_consumed": pq.tokens_per_hour.consumed if pq.tokens_per_hour else None,
                "hourly_remaining": pq.tokens_per_hour.remaining if pq.tokens_per_hour else None,
            }

    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            result["error"] = (
                f"Permission denied for property '{property_id}'. "
                "Add the service account email as Viewer in "
                "GA4 Admin > Property Access Management."
            )
        elif "404" in error_str or "NOT_FOUND" in error_str:
            result["error"] = (
                f"Property '{property_id}' not found. "
                "Verify the numeric property ID in GA4 Admin > Property Details."
            )
        else:
            result["error"] = f"GA4 API error: {e}"
        return result

    if result["channels"]:
        total_sessions = sum(c["sessions"] for c in result["channels"])
        total_users = sum(c["users"] for c in result["channels"])
        total_pageviews = sum(c["pageviews"] for c in result["channels"])
        result["totals"] = {
            "sessions": total_sessions,
            "users": total_users,
            "pageviews": total_pageviews,
            "channel_count": len(result["channels"]),
        }
        # Per-channel share of total sessions
        if total_sessions > 0:
            for c in result["channels"]:
                c["share_of_sessions"] = round(c["sessions"] / total_sessions * 100, 1)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="GA4 Data API - organic traffic reporting"
    )
    parser.add_argument(
        "--property", "-p",
        help="GA4 property ID (numeric, e.g., 123456789). Uses config default if not specified.",
    )
    parser.add_argument("--days", "-d", type=int, default=28, help="Number of days (default: 28)")
    parser.add_argument(
        "--report", "-r",
        choices=["organic", "top-pages", "device", "country", "referrals", "channel-mix"],
        default="organic",
        help="Report type (default: organic)",
    )
    parser.add_argument("--limit", type=int, default=50, help="Max rows (default: 50)")
    parser.add_argument(
        "--page",
        help=(
            "Optional landing-page filter — scope any report to a single entry page. "
            "Accepts a path ('/blog/post/') or full URL (host stripped). EXACT match "
            "against GA4's `landingPage` dimension."
        ),
    )
    parser.add_argument(
        "--channel",
        default="organic",
        help=(
            "Channel filter for --report organic / top-pages. Use 'organic' "
            "(default, == 'Organic Search'), 'all' for no filter (required to "
            "reproduce all-channels weekly trends), or any GA4 default channel "
            "group name verbatim ('Direct', 'Referral', 'Paid Search', "
            "'Organic Social', etc.)."
        ),
    )
    parser.add_argument(
        "--sources",
        default="ai",
        help=(
            "For --report referrals only: 'ai' for AI-assistant default list, "
            "'all' for every Referral-channel source, or a comma-separated list "
            "of source hostnames (e.g. 'chatgpt.com,perplexity.ai'). Default: ai."
        ),
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Resolve property
    prop = args.property
    if not prop:
        config = load_config()
        prop = config.get("ga4_property_id") or ""
        # Strip 'properties/' prefix if present for consistency
        if prop and prop.startswith("properties/"):
            prop = prop[len("properties/"):]
    if not prop:
        print(
            "Error: No GA4 property specified. Use --property or set ga4_property_id in config.",
            file=sys.stderr,
        )
        sys.exit(1)

    # --channel for organic / top-pages: translate aliases to GA4 channel-group values
    if args.channel == "all":
        channel_value: Optional[str] = None
    elif args.channel == "organic":
        channel_value = "Organic Search"
    else:
        channel_value = args.channel

    if args.report == "top-pages":
        result = top_pages_report(prop, args.days, args.limit, page=args.page, channel=channel_value)
    elif args.report == "device":
        result = device_breakdown(prop, args.days, page=args.page)
    elif args.report == "country":
        result = country_breakdown(prop, args.days, args.limit, page=args.page)
    elif args.report == "channel-mix":
        result = channel_mix_report(prop, args.days, args.limit, page=args.page)
    elif args.report == "referrals":
        if args.sources == "all":
            sources_list = None
        elif args.sources == "ai":
            sources_list = AI_REFERRAL_SOURCES
        else:
            sources_list = [s.strip() for s in args.sources.split(",") if s.strip()]
        result = referrals_report(prop, args.days, args.limit, sources_list, page=args.page)
    else:
        result = organic_traffic_report(prop, args.days, args.limit, page=args.page, channel=channel_value)

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        if not args.json:
            sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        page_filter = result.get("page_filter")
        channel_filter = result.get("channel_filter")
        if args.report == "top-pages":
            ch_label = channel_filter or "all channels"
            print(f"=== Top Landing Pages ({ch_label}) ===")
            print(f"Property: {prop} | Period: {result.get('date_range', {}).get('start')} to {result.get('date_range', {}).get('end')}")
            if page_filter:
                print(f"Page filter: {page_filter}")
            total_label = "Total sessions" if not channel_filter else f"Total {ch_label.lower()} sessions"
            total_value = result.get("total_sessions", result.get("total_organic_sessions", 0))
            print(f"{total_label}: {total_value:,}")
            print()
            for i, page in enumerate(result.get("pages", [])[:20], 1):
                print(f"  {i:2d}. {page['landing_page']}")
                print(f"      Sessions: {page['sessions']:,} | Users: {page['users']:,} | Bounce: {page['bounce_rate']}%")
        elif args.report == "referrals":
            dr = result.get("date_range", {})
            print(f"=== GA4 Referral Sessions ===")
            print(f"Property: {prop} | Period: {dr.get('start')} to {dr.get('end')}")
            sf = result.get("sources_filter")
            if sf is None:
                print("Filter: Referral channel group (all sources)")
            else:
                print(f"Filter: sessionSource IN [{', '.join(sf)}]")
            if page_filter:
                print(f"Page filter: {page_filter}")
            totals = result.get("totals", {})
            print(
                f"\nTotal sessions: {totals.get('sessions', 0):,} | "
                f"Users: {totals.get('users', 0):,} | "
                f"Pageviews: {totals.get('pageviews', 0):,} | "
                f"Sources: {totals.get('source_count', 0)}"
            )
            print()
            for i, src in enumerate(result.get("sources", [])[:25], 1):
                print(f"  {i:2d}. {src['source']}")
                print(
                    f"      Sessions: {src['sessions']:,} | "
                    f"Users: {src['users']:,} | "
                    f"Engagement: {src['engagement_rate']}% | "
                    f"Bounce: {src['bounce_rate']}%"
                )
        elif args.report == "channel-mix":
            dr = result.get("date_range", {})
            print(f"=== GA4 Channel Mix ===")
            print(f"Property: {prop} | Period: {dr.get('start')} to {dr.get('end')}")
            if page_filter:
                print(f"Page filter: {page_filter}")
            totals = result.get("totals", {})
            print(
                f"\nTotal sessions: {totals.get('sessions', 0):,} | "
                f"Users: {totals.get('users', 0):,} | "
                f"Pageviews: {totals.get('pageviews', 0):,} | "
                f"Channels: {totals.get('channel_count', 0)}"
            )
            print()
            for i, ch in enumerate(result.get("channels", []), 1):
                share = ch.get("share_of_sessions", 0)
                print(f"  {i:2d}. {ch['channel']} — {share}%")
                print(
                    f"      Sessions: {ch['sessions']:,} | "
                    f"Users: {ch['users']:,} | "
                    f"Pageviews: {ch['pageviews']:,} | "
                    f"Engagement: {ch['engagement_rate']}%"
                )
        else:
            totals = result.get("totals", {})
            ch_label = channel_filter or "all channels"
            print(f"=== GA4 Traffic Report ({ch_label}) ===")
            print(f"Property: {prop}")
            dr = result.get("date_range", {})
            print(f"Period: {dr.get('start')} to {dr.get('end')}")
            if page_filter:
                print(f"Page filter: {page_filter}")
            print(f"\nSessions: {totals.get('sessions', 0):,} | Users: {totals.get('users', 0):,} | Pageviews: {totals.get('pageviews', 0):,}")
            print(f"Avg Daily Sessions: {totals.get('avg_daily_sessions', 0):,.0f}")

            quota = result.get("quota_tokens_used")
            if quota and quota.get("daily_remaining") is not None:
                print(f"\nQuota: {quota['daily_consumed']} tokens used / {quota['daily_remaining']} remaining (daily)")

            pages = result.get("top_pages", [])
            if pages:
                print(f"\nTop {min(10, len(pages))} Landing Pages:")
                for i, page in enumerate(pages[:10], 1):
                    print(f"  {i:2d}. {page['landing_page']} ({page['sessions']:,} sessions)")


if __name__ == "__main__":
    main()
