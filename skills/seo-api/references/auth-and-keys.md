# Auth & Keys

The full picture of how to authenticate against SE Ranking's APIs and the MCP server. Used by the `seo-api` skill to answer "how do I auth", "where does the key come from", "what's the OAuth flow", and "how do I run this headlessly in CI".

## Key types — single source of truth

As of 2026, **one API key authenticates everything**. The legacy split into separate Data and Project keys is gone. The same UUID-format key works against:

- All `DATA_*` MCP tools and the underlying `/v1/backlinks/*`, `/v1/domain/*`, `/v1/keywords/*`, `/v1/serp/*`, `/v1/audit/*`, `/v1/ai-search/*`, `/v1/account/*` REST endpoints.
- All `PROJECT_*` MCP tools and the underlying `/v1/projects/*`, `/v1/projects/{id}/keywords/*`, `/v1/projects/{id}/audits/*`, `/v1/projects/{id}/backlinks/*`, `/v1/projects/{id}/airt/*`, `/v1/account/*` REST endpoints.

Get keys at: <https://online.seranking.com/admin.api.dashboard.html>.

You can mint multiple keys per account — useful for splitting rate-limit budgets across environments (dev, staging, prod) or workloads (research vs. recurring jobs).

### Required plan

- **Data API access** ships with: any plan that has API credits — Business / Enterprise plans (100K credits/month included), API add-on (1M+), or standalone API plan (1M+).
- **Project API access** requires: Business or Enterprise plan. The Project API consumes plan limits ("Sites", "Keywords", "Audit Pages", "AIRT Prompts") rather than credits.

If the user is on Essential or Pro, Project API tools will return `403 Subscription required`. Surface the upgrade link: <https://seranking.com/subscription.html>.

## REST API auth

### Recommended — Authorization header

```bash
curl -X GET 'https://api.seranking.com/v1/account/subscription' \
  -H 'Authorization: Token YOUR_API_KEY'
```

Token scheme prefix is **`Token`**, not `Bearer`.

### Fallback — query parameter

```bash
curl -X GET 'https://api.seranking.com/v1/account/subscription?apikey=YOUR_API_KEY'
```

Avoid the query param in production — it leaks the key into access logs, browser history, and HTTP referrers. Header is always preferred.

### Liveness check

The cheapest way to confirm a key is valid (0 credits):

```bash
curl -X GET 'https://api.seranking.com/v1/account/subscription' \
  -H 'Authorization: Token YOUR_API_KEY'
```

`200 OK` with a `subscription_info` payload = key is alive. `401 Unauthorized` = key is invalid or revoked.

## MCP server auth

The MCP server at `https://api.seranking.com/mcp` is the recommended interface for any agentic workflow. It supports two auth modes, **pick one per client**:

### Mode 1 — OAuth 2.1 (interactive, recommended for IDEs and desktop)

Opens a browser on first connect, stores the token locally, reuses across sessions. Right for Claude Desktop, Claude Code on a workstation, Cursor, Codex IDE.

```bash
claude mcp add --transport http se-ranking https://api.seranking.com/mcp
```

First tool call triggers the browser sign-in. Subsequent calls reuse the refresh token (30-day sliding window, configurable via `MCP_REFRESH_TOKEN_TTL` server-side).

### Mode 2 — API key header (non-interactive, recommended for CI / headless)

Pass the key directly. Server skips OAuth entirely.

```bash
claude mcp add --transport http se-ranking https://api.seranking.com/mcp \
  --header "X-Api-Key: $SERANKING_API_KEY"
```

The header `X-Data-Api-Key` is still accepted as an alias for `X-Api-Key` (backwards compat with older self-hosted installs).

### Precedence when both are present

If a request arrives with both header auth and an `Authorization: Bearer …` token from a previous OAuth session, **headers win**. This lets you override a stale Bearer token without reconfiguring the client.

### Discovery endpoints (auto-resolved by spec-compliant clients)

| Endpoint | Purpose |
|---|---|
| `/.well-known/oauth-authorization-server` | RFC 8414 authorization server metadata |
| `/.well-known/oauth-protected-resource` | RFC 9728 protected-resource metadata |
| `/.well-known/openid-configuration` | OIDC compatibility for clients that probe OIDC first |
| `/register` | RFC 7591 dynamic client registration (no manual `client_id` provisioning) |

## Per-client configuration cheat-sheet

### Claude Code

```bash
claude mcp add --transport http se-ranking https://api.seranking.com/mcp
# Then /mcp to complete OAuth.
```

### Claude Desktop / claude.ai

`Customize` → `Connectors` → `+` → `Add custom connector`. Name: `SE Ranking`. URL: `https://api.seranking.com/mcp`.

### Codex (CLI + IDE)

```bash
codex mcp add se-ranking --url https://api.seranking.com/mcp
```

First-time Codex users: enable the rmcp feature in `~/.codex/config.toml`:

```toml
[features]
experimental_use_rmcp_client = true
```

### Cursor

`.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "se-ranking": {
      "url": "https://api.seranking.com/mcp"
    }
  }
}
```

### VS Code

`Cmd+P` → `MCP: Add Server` → `Command (stdio)`:

```bash
npx -y mcp-remote https://api.seranking.com/mcp
```

### Windsurf / Zed / Gemini CLI / others

All use the same `npx -y mcp-remote https://api.seranking.com/mcp` pattern via their respective MCP config files (`~/.codeium/windsurf/mcp_config.json`, `~/.config/zed/settings.json`, `~/.gemini/settings.json`).

## Sub-accounts on a shared workspace

If the user is a sub-account on a master SE Ranking workspace, the "Sign in with SE Ranking" OAuth path won't enumerate any tools — **API access lives with the master account**. Workaround until sub-account API keys ship:

1. Get the API key from the workspace administrator (from the API Dashboard on the master account).
2. In the MCP connection dialog, choose **Enter API key manually** (or use Mode 2 via `X-Api-Key` header) instead of OAuth.
3. Paste the master key.

## Key rotation

Rotate keys when:

- A key leaks (committed to git, posted in a Slack channel, ended up in a screenshot).
- An employee with access leaves.
- A workload moves between environments and you want clean rate-limit accounting.

Rotation:

1. Generate a new key at the API Dashboard.
2. Roll the new key into production (env var, secret manager).
3. Revoke the old key.
4. **Note:** keys are validated and cached server-side. After revoking, allow up to 60 seconds for the cache to invalidate before assuming the old key is fully dead.

## Common 401 / 403 patterns

| HTTP | `error.message` | What it means | Fix |
|---|---|---|---|
| 401 | `Unauthorized` | Key missing, malformed, or revoked. | Re-check `Authorization` header format. Token scheme is `Token`, not `Bearer`. |
| 401 | `API key provided via X-Api-Key failed validation.` | Format check passed (UUID-shaped) but liveness probe to `/v1/account/info` failed. | Key is revoked or typo'd. |
| 403 | `Insufficient funds` | Data API balance too low for the requested cost. | Top up at the API Dashboard, or downsize the request. |
| 403 | `Subscription required` | Project API call from a non-Business/Enterprise plan. | Upgrade plan, or stick to Data API only. |
| 403 | `Limit reached` | Project API plan limit ("Sites", "Keywords", "Audit Pages", "AIRT Prompts") exceeded. | Upgrade plan, or release unused resources via the corresponding `PROJECT_delete*` tool. |

## Storing keys safely

- **Never commit keys to git.** Even in private repos. Use `.env` (gitignored) + a secret manager (1Password, Doppler, AWS Secrets Manager, Vault).
- **Don't pass keys in URL query parameters.** They leak into access logs.
- **For client-side code:** API keys must never reach the browser. Proxy through your own backend.
- **For CI:** use the platform's secret store (GitHub Actions secrets, GitLab CI variables, etc.).
- **For Docker:** pass via `--env-file`, never bake into the image layer.
