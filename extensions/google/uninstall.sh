#!/usr/bin/env bash
# extensions/google/uninstall.sh — remove the seo-skills Google API config.
#
# Removes ~/.config/seo-skills/google-api.json and oauth-token.json. Does NOT
# uninstall the pip-installed Google API libraries (those are user-site
# packages and may be used by other tools — uninstall manually with
# 'python3 -m pip uninstall google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-analytics-data').
#
# Service account JSON files referenced by `service_account_path` are NOT deleted
# — those live wherever the user placed them and may be reused by other tools.

set -euo pipefail

CONFIG_DIR="${SEO_SKILLS_CONFIG_DIR:-$HOME/.config/seo-skills}"
CONFIG_FILE="$CONFIG_DIR/google-api.json"
TOKEN_FILE="$CONFIG_DIR/oauth-token.json"

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }

removed_any=0

if [ -f "$CONFIG_FILE" ]; then
  rm -f "$CONFIG_FILE"
  green "✓ Removed $CONFIG_FILE"
  removed_any=1
fi

if [ -f "$TOKEN_FILE" ]; then
  rm -f "$TOKEN_FILE"
  green "✓ Removed $TOKEN_FILE"
  removed_any=1
fi

if [ "$removed_any" -eq 0 ]; then
  echo "No seo-skills Google config found at $CONFIG_DIR; nothing to uninstall."
  exit 0
fi

if [ -d "$CONFIG_DIR" ] && [ -z "$(ls -A "$CONFIG_DIR")" ]; then
  rmdir "$CONFIG_DIR"
  green "✓ Removed empty $CONFIG_DIR"
fi

echo ""
red "Note: pip-installed libraries (google-api-python-client etc.) were NOT removed."
echo "If you want to remove them, run:"
echo "  python3 -m pip uninstall google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-analytics-data"
echo ""
echo "Service account JSON files (referenced by service_account_path) were NOT deleted."
echo "Delete them manually if no longer needed."
