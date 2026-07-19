#!/bin/bash
# deploy-app.sh
# Registers a completed Streamlit app under its carrier company on your-domain.com.
#
# Usage:
#   bash deploy-app.sh <company_slug> <app_name> <app_dir> [pitch_sentence]
#
# URL produced: https://your-domain.com/{company-slug}/{app-name}
#
# What this does:
#   1. Assigns the next available port (starts at 8501)
#   2. Creates a systemd service
#   3. Adds a Caddy reverse_proxy route for nested path
#   4. Reloads Caddy
#   5. Updates companies.json for the portfolio page
#   6. Writes the live URL to deployment_url.txt in the app dir

set -euo pipefail

COMPANY_SLUG="${1:-}"
APP_NAME="${2:-}"
APP_DIR="${3:-}"
PITCH_SENTENCE="${4:-}"

if [ -z "$COMPANY_SLUG" ] || [ -z "$APP_NAME" ] || [ -z "$APP_DIR" ]; then
    echo "Usage: bash deploy-app.sh <company_slug> <app_name> <app_dir> [pitch]"
    exit 1
fi

if [ ! -f "$APP_DIR/app.py" ]; then
    echo "app.py not found in $APP_DIR"
    exit 1
fi

# Load config.env from the repo root (one directory up from scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.env"
if [ -f "$CONFIG_FILE" ]; then
    # shellcheck source=../config.env
    source "$CONFIG_FILE"
else
    echo "WARNING: config.env not found. Copy config.env.example to config.env and fill in your values."
fi

AGENT_DIR="${AGENT_DIR:-/opt/carrier-factory}"
PORT_REGISTRY="$AGENT_DIR/port_registry.txt"
CADDYFILE="$AGENT_DIR/Caddyfile"
COMPANIES_JSON="$AGENT_DIR/web/companies.json"
DOMAIN="${AGENT_DOMAIN:-your-domain.com}"

# --- Find next available port ------------------------------------------------

touch "$PORT_REGISTRY"
LAST_PORT=$(grep -oP ':\K\d+' "$PORT_REGISTRY" 2>/dev/null | sort -n | tail -1 || true)
if [ -z "$LAST_PORT" ]; then
    NEXT_PORT=8501
else
    NEXT_PORT=$(( LAST_PORT + 1 ))
fi

echo "$COMPANY_SLUG/$APP_NAME:$NEXT_PORT" >> "$PORT_REGISTRY"
echo "Assigning port $NEXT_PORT to $COMPANY_SLUG/$APP_NAME"

# --- URL path ----------------------------------------------------------------

BASE_URL_PATH="/${COMPANY_SLUG}/${APP_NAME}"
DEPLOYMENT_URL="https://${DOMAIN}${BASE_URL_PATH}"

# --- Systemd service ---------------------------------------------------------

SERVICE_NAME="co-${COMPANY_SLUG}-${APP_NAME}"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
STREAMLIT_BIN="$AGENT_DIR/venv/bin/streamlit"

# Write service file content to a temp file, then sudo mv it into place
SVCFILE=$(mktemp)
cat > "$SVCFILE" <<SVCEOF
[Unit]
Description=Carrier Demo -- ${COMPANY_SLUG}/${APP_NAME}
After=network.target

[Service]
Type=simple
User=agent
WorkingDirectory=${APP_DIR}
Environment="PATH=${AGENT_DIR}/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=${STREAMLIT_BIN} run app.py \
    --server.address 127.0.0.1 \
    --server.port ${NEXT_PORT} \
    --server.baseUrlPath ${BASE_URL_PATH} \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SVCEOF

sudo cp "$SVCFILE" "$SERVICE_FILE"
unlink "$SVCFILE"

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"
echo "Service started: $SERVICE_NAME"

# --- Caddy route -------------------------------------------------------------

# Named matcher: replace hyphens and slashes with underscores
MATCHER_NAME=$(echo "${COMPANY_SLUG}_${APP_NAME}" | tr '-' '_')

NEW_ROUTE="    # ${COMPANY_SLUG}/${APP_NAME} -- added $(date '+%Y-%m-%d')
    @${MATCHER_NAME} path ${BASE_URL_PATH} ${BASE_URL_PATH}/*
    handle @${MATCHER_NAME} {
        reverse_proxy localhost:${NEXT_PORT}
    }"

if grep -q "# APPS_END" "$CADDYFILE"; then
    TMP=$(mktemp)
    while IFS= read -r line; do
        if [[ "$line" == *"# APPS_END" ]]; then
            printf '%s\n' "$NEW_ROUTE" >> "$TMP"
            echo "" >> "$TMP"
        fi
        echo "$line" >> "$TMP"
    done < "$CADDYFILE"
    sudo cp "$TMP" "$CADDYFILE"
    unlink "$TMP"
else
    echo "WARNING: APPS_END marker not found in Caddyfile"
fi

if caddy validate --config "$CADDYFILE" 2>/dev/null; then
    sudo caddy reload --config "$CADDYFILE"
    echo "Caddy reloaded: ${BASE_URL_PATH}"
else
    echo "Caddyfile invalid -- rolling back port registry entry"
    grep -v "$COMPANY_SLUG/$APP_NAME:$NEXT_PORT" "$PORT_REGISTRY" > "${PORT_REGISTRY}.tmp"
    mv "${PORT_REGISTRY}.tmp" "$PORT_REGISTRY"
    exit 1
fi

# --- Update companies.json ---------------------------------------------------

DEPLOY_DATE=$(date '+%Y-%m-%d')
APP_DISPLAY=$(echo "$APP_NAME" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

python3 "$AGENT_DIR/update_companies_json.py" \
    "$COMPANY_SLUG" \
    "$APP_NAME" \
    "$APP_DISPLAY" \
    "$PITCH_SENTENCE" \
    "$BASE_URL_PATH" \
    "$DEPLOY_DATE" \
    "$COMPANIES_JSON"

# --- Write deployment URL ----------------------------------------------------

echo "$DEPLOYMENT_URL" > "$APP_DIR/deployment_url.txt"

echo ""
echo "================================================================"
echo "  APP DEPLOYED"
echo "  Company: $COMPANY_SLUG"
echo "  App:     $APP_NAME"
echo "  Port:    $NEXT_PORT"
echo "  URL:     $DEPLOYMENT_URL"
echo "================================================================"
