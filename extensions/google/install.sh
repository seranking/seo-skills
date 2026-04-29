#!/usr/bin/env bash
# extensions/google/install.sh — wire the Google APIs Python toolchain into seo-skills.
#
# What this does:
#   1. Verify Python 3.10+ and pip.
#   2. pip-install the Google API client libraries to user site-packages
#      (google-api-python-client, google-auth, google-auth-oauthlib,
#      google-auth-httplib2, google-analytics-data, requests, plus
#      matplotlib/weasyprint/openpyxl for report generation).
#   3. Create the config directory at ~/.config/seo-skills/.
#   4. If config file is missing, write a stub the user can fill in.
#   5. Run the credential checker to report what tier is unlocked.
#
# Idempotent: re-running upgrades the libraries; existing config is preserved.

set -euo pipefail

CONFIG_DIR="${SEO_SKILLS_CONFIG_DIR:-$HOME/.config/seo-skills}"
CONFIG_FILE="$CONFIG_DIR/google-api.json"
SCRIPTS_DIR="$(cd "$(dirname "$0")/../../scripts" && pwd)"
SKILL_REFS_DIR="$(cd "$(dirname "$0")/../../skills/seo-google/references" && pwd)"

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
bold()  { printf '\033[1m%s\033[0m\n' "$*"; }
dim()   { printf '\033[2m%s\033[0m\n' "$*"; }

# --- 1. Dependency checks -----------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
  red "Error: 'python3' not found on PATH."
  echo "Install Python 3.10+ from https://www.python.org or via your package manager."
  exit 1
fi

PY_OK="$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 10) else 0)')"
if [ "$PY_OK" != "1" ]; then
  PY_VER="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  red "Error: Python $PY_VER detected; seo-google requires Python 3.10+."
  exit 1
fi

PY_VER="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
green "✓ Python $PY_VER detected"

if ! python3 -m pip --version >/dev/null 2>&1; then
  red "Error: pip not available for python3."
  echo "Install pip via 'python3 -m ensurepip --upgrade' or your package manager."
  exit 1
fi

# --- 2. Install Google API libraries -----------------------------------------

bold "Installing Google API client libraries (user site-packages)..."

CORE_PKGS=(
  "google-api-python-client>=2.100.0,<3.0.0"
  "google-auth>=2.20.0,<3.0.0"
  "google-auth-oauthlib>=1.0.0,<2.0.0"
  "google-auth-httplib2>=0.2.0,<1.0.0"
  "google-analytics-data>=0.18.0,<1.0.0"
  "requests>=2.32.4,<3.0.0"
)

REPORT_PKGS=(
  "matplotlib>=3.8.0,<4.0.0"
  "weasyprint>=61.0,<70.0"
  "openpyxl>=3.1.0,<4.0.0"
)

PIP_FLAGS=(--user --upgrade --quiet)
if [ -n "${VIRTUAL_ENV:-}" ]; then
  # Inside a venv — drop --user
  PIP_FLAGS=(--upgrade --quiet)
  dim "  (virtualenv detected at $VIRTUAL_ENV — installing into venv)"
fi

python3 -m pip install "${PIP_FLAGS[@]}" "${CORE_PKGS[@]}" \
  || { red "Error installing core Google API libraries."; exit 1; }
green "✓ Core Google API libraries installed"

bold "Installing report-generation libraries (matplotlib + weasyprint + openpyxl)..."
if python3 -m pip install "${PIP_FLAGS[@]}" "${REPORT_PKGS[@]}"; then
  green "✓ Report libraries installed"
else
  red "⚠ Report libraries failed to install (matplotlib/weasyprint often need system deps like cairo/pango/gdk-pixbuf on Linux, or Xcode CLT on macOS). Core API commands still work — only 'report' command will be unavailable."
fi

# --- 3. Config directory ------------------------------------------------------

mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"
green "✓ Config directory: $CONFIG_DIR"

# --- 4. Stub config file ------------------------------------------------------

if [ ! -f "$CONFIG_FILE" ]; then
  cat > "$CONFIG_FILE" <<'JSON'
{
  "_comment": "seo-skills google-api config. See skills/seo-google/references/auth-setup.md for setup. Remove this comment field once filled in.",
  "service_account_path": "",
  "api_key": "",
  "default_property": "",
  "ga4_property_id": ""
}
JSON
  chmod 600 "$CONFIG_FILE"
  green "✓ Stub config written: $CONFIG_FILE"
  echo ""
  bold "Next: fill in $CONFIG_FILE"
  echo ""
  echo "  At minimum, populate 'api_key' (Tier 0 — unlocks PSI, CrUX, YouTube, NLP, Knowledge Graph)."
  echo "  Add 'service_account_path' (Tier 1 — unlocks GSC + Indexing)."
  echo "  Add 'ga4_property_id' (Tier 2 — unlocks GA4)."
  echo ""
  echo "  Full walkthrough: $SKILL_REFS_DIR/auth-setup.md"
  echo ""
else
  green "✓ Config exists: $CONFIG_FILE (preserved)"
fi

# --- 5. Credential check ------------------------------------------------------

bold "Checking credentials..."
if [ -x "$(command -v python3)" ] && [ -f "$SCRIPTS_DIR/google_auth.py" ]; then
  python3 "$SCRIPTS_DIR/google_auth.py" --check 2>&1 || true
else
  red "  Could not locate scripts/google_auth.py — install layout may be off."
fi

echo ""
green "✓ seo-google extension installed."
echo ""
bold "Next steps:"
echo "  1. If you saw 'No credentials found', open $CONFIG_FILE and fill in fields."
echo "  2. Read $SKILL_REFS_DIR/auth-setup.md for the 8-step walkthrough."
echo "  3. Re-run 'python3 $SCRIPTS_DIR/google_auth.py --check' to confirm tier."
echo "  4. Try a Tier-0 command: 'python3 $SCRIPTS_DIR/pagespeed_check.py https://example.com --json'"
echo ""
bold "All Google APIs are free. Setup is one-time."
