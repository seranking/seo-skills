file: skills/seo-api/references/auth-and-keys.md
=== find
Subsequent calls reuse the refresh token (30-day sliding window, configurable via `MCP_REFRESH_TOKEN_TTL` server-side).
=== replace
Later calls reuse the session (30-day sliding window).
