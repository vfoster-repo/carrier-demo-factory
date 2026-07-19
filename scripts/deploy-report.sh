#!/bin/bash
# deploy-report.sh
# Deploys a self-contained HTML report for a carrier company as a static page.
#
# Usage:
#   bash /opt/carrier-factory/deploy-report.sh <company_slug> <report_html_path>
#
# URL produced: https://your-domain.com/{company-slug}/report/
#
# What this does:
#   1. Creates /opt/carrier-factory/web/{company-slug}/report/ directory
#   2. Copies the report HTML as index.html (served by Caddy's existing file_server)
#   3. Writes deployment_url.txt into the company directory alongside report.html

set -euo pipefail

COMPANY_SLUG="${1:-}"
REPORT_HTML="${2:-}"

if [ -z "$COMPANY_SLUG" ] || [ -z "$REPORT_HTML" ]; then
    echo "Usage: bash deploy-report.sh <company_slug> <report_html_path>"
    exit 1
fi

if [ ! -f "$REPORT_HTML" ]; then
    echo "Report HTML not found: $REPORT_HTML"
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
REPORT_WEB_DIR="$AGENT_DIR/web/${COMPANY_SLUG}/report"
DEPLOYMENT_URL="https://${DOMAIN}/${COMPANY_SLUG}/report/"
COMPANIES_JSON="$AGENT_DIR/web/companies.json"

# --- Deploy static file ------------------------------------------------------

mkdir -p "$REPORT_WEB_DIR"
cp "$REPORT_HTML" "$REPORT_WEB_DIR/index.html"
echo "Report deployed to: $REPORT_WEB_DIR/index.html"

# --- Write deployment URL ----------------------------------------------------

# Write next to report.html in the company directory
REPORT_DIR=$(dirname "$REPORT_HTML")
echo "$DEPLOYMENT_URL" > "$REPORT_DIR/deployment_url.txt"

# --- Register in companies.json ---------------------------------------------

DEPLOY_DATE=$(date '+%Y-%m-%d')
python3 "$SCRIPT_DIR/update_companies_json.py" \
    "$COMPANY_SLUG" \
    "report" \
    "📊 Insights Report" \
    "Free data-driven insights report — key performance metrics, cost drivers, and operational opportunities for this carrier." \
    "/${COMPANY_SLUG}/report/" \
    "$DEPLOY_DATE" \
    "$COMPANIES_JSON"
echo "Portfolio updated: $COMPANIES_JSON"

echo ""
echo "================================================================"
echo "  REPORT DEPLOYED"
echo "  Company: $COMPANY_SLUG"
echo "  URL:     $DEPLOYMENT_URL"
echo "================================================================"
