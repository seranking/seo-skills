file: skills/seo-api/SKILL.md
=== find
`API_TOKEN` (or `X-Api-Key` header for headless) covers both `DATA_*` and `PROJECT_*`. The legacy split into separate Data and Project keys is gone — passing both still works as headers for backwards compatibility, but you can use just `X-Api-Key` now.
=== replace
One SE Ranking API key covers both `DATA_*` and `PROJECT_*`: the `Authorization: Token` header for REST calls, or the `X-Api-Key` header for headless MCP.
