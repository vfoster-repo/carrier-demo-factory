#!/bin/bash
# deploy-profile.sh
# Deploys a self-contained HTML company profile page as a static file.
#
# Usage:
#   bash /opt/carrier-factory/deploy-profile.sh <company_slug> <profile_html_path>
#
# URL produced: https://your-domain.com/{company-slug}/profile/
#
# What this does:
#   1. Creates /opt/carrier-factory/web/{company-slug}/profile/ directory
#   2. Copies the profile HTML as index.html (served by Caddy's existing file_server)
#   3. Registers the page in companies.json for the portfolio
#   4. Writes profile_deployment_url.txt into the company directory

set -euo pipefail

COMPANY_SLUG="${1:-}"
PROFILE_HTML="${2:-}"

if [ -z "$COMPANY_SLUG" ] || [ -z "$PROFILE_HTML" ]; then
    echo "Usage: bash deploy-profile.sh <company_slug> <profile_html_path>"
    exit 1
fi

if [ ! -f "$PROFILE_HTML" ]; then
    echo "Profile HTML not found: $PROFILE_HTML"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.env"
if [ -f "$CONFIG_FILE" ]; then
    # shellcheck source=../config.env
    source "$CONFIG_FILE"
fi
AGENT_DIR="${AGENT_DIR:-/opt/carrier-factory}"
DOMAIN="${AGENT_DOMAIN:-your-domain.com}"
PROFILE_WEB_DIR="$AGENT_DIR/web/${COMPANY_SLUG}/profile"
DEPLOYMENT_URL="https://${DOMAIN}/${COMPANY_SLUG}/profile/"
COMPANIES_JSON="$AGENT_DIR/web/companies.json"

# --- Deploy static file ------------------------------------------------------

mkdir -p "$PROFILE_WEB_DIR"
cp "$PROFILE_HTML" "$PROFILE_WEB_DIR/index.html"
echo "Profile deployed to: $PROFILE_WEB_DIR/index.html"

# --- Write deployment URL file -----------------------------------------------

PROFILE_DIR=$(dirname "$PROFILE_HTML")
echo "$DEPLOYMENT_URL" > "$PROFILE_DIR/profile_deployment_url.txt"

# --- Register in companies.json ----------------------------------------------

DEPLOY_DATE=$(date '+%Y-%m-%d')
python3 "$SCRIPT_DIR/update_companies_json.py" \
    "$COMPANY_SLUG" \
    "profile" \
    "🗂️ Company Profile" \
    "Full company background — who they are, the data analyzed, pain points identified, and what was built to address them." \
    "/${COMPANY_SLUG}/profile/" \
    "$DEPLOY_DATE" \
    "$COMPANIES_JSON"
echo "Portfolio updated: $COMPANIES_JSON"

echo ""
echo "================================================================"
echo "  PROFILE DEPLOYED"
echo "  Company: $COMPANY_SLUG"
echo "  URL:     $DEPLOYMENT_URL"
echo "================================================================"
