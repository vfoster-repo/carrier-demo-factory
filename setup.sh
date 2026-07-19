#!/bin/bash
# setup.sh
# One-shot setup for the Carrier Demo Factory on a fresh Ubuntu/Debian VPS.
#
# Usage:
#   bash setup.sh <your-domain.com>
#
# What this does:
#   1. Installs system dependencies (Caddy, Node, Python, Claude Code)
#   2. Creates the agent user and /opt/carrier-factory/ directory structure
#   3. Copies repo files into place
#   4. Writes config.env from your domain
#   5. Configures Caddy to serve the portfolio
#   6. Sets up a systemd timer to run the pipeline every 6 hours
#
# Run as root on a fresh server. Takes ~5 minutes.

set -euo pipefail

DOMAIN="${1:-}"
if [ -z "$DOMAIN" ]; then
    echo "Usage: bash setup.sh <your-domain.com>"
    echo "Example: bash setup.sh your-domain.com"
    exit 1
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_DIR="/opt/carrier-factory"
WEB_DIR="$AGENT_DIR/web"

echo "================================================================"
echo "  CARRIER DEMO FACTORY — VPS SETUP"
echo "  Domain: $DOMAIN"
echo "  $(date +'%Y-%m-%d %H:%M:%S')"
echo "================================================================"

# --- 1. System dependencies --------------------------------------------------

echo ""
echo "[1/6] Installing system dependencies..."

apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm curl

# Caddy
if ! command -v caddy &>/dev/null; then
    apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
        | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
        | tee /etc/apt/sources.list.d/caddy-stable.list
    apt-get update -qq
    apt-get install -y -qq caddy
fi
echo "  Caddy: $(caddy version)"

# Claude Code
if ! command -v claude &>/dev/null; then
    npm install -g @anthropic-ai/claude-code --prefix /usr/local
fi
echo "  Claude Code: $(claude --version)"

# --- 2. Agent user and directories -------------------------------------------

echo ""
echo "[2/6] Creating agent user and directories..."

if ! id agent &>/dev/null; then
    useradd -m -s /bin/bash agent
    echo "  Created user: agent"
fi

# Allow agent to manage its own systemd services
echo "agent ALL=(ALL) NOPASSWD: /bin/systemctl daemon-reload, /bin/systemctl enable *, /bin/systemctl start *, /bin/systemctl restart *, /bin/cp, /bin/mv" \
    > /etc/sudoers.d/agent-caddy
chmod 440 /etc/sudoers.d/agent-caddy

mkdir -p "$AGENT_DIR"/{companies,prompts,scripts,logs,web}
chown -R agent:agent "$AGENT_DIR"

# Python venv
python3 -m venv "$AGENT_DIR/venv"
"$AGENT_DIR/venv/bin/pip" install -q streamlit pandas plotly
echo "  Python venv ready: $AGENT_DIR/venv"

# --- 3. Copy repo files ------------------------------------------------------

echo ""
echo "[3/6] Copying repo files..."

cp -r "$REPO_DIR/prompts/"* "$AGENT_DIR/prompts/"
cp -r "$REPO_DIR/scripts/"* "$AGENT_DIR/scripts/"
chmod +x "$AGENT_DIR/scripts/"*.sh

# Copy web assets (portfolio page + companies.json)
cp -r "$REPO_DIR/web/"* "$WEB_DIR/"

# Copy any existing demos into web/
if [ -d "$REPO_DIR/demos" ]; then
    for demo_dir in "$REPO_DIR/demos"/*/; do
        slug=$(basename "$demo_dir")
        [ "$slug" = "*" ] && continue

        # Copy report.html
        if [ -f "$demo_dir/report.html" ]; then
            mkdir -p "$WEB_DIR/$slug/report"
            cp "$demo_dir/report.html" "$WEB_DIR/$slug/report/index.html"
            echo "  Deployed: $slug/report"
        fi

        # Copy profile.html
        if [ -f "$demo_dir/profile.html" ]; then
            mkdir -p "$WEB_DIR/$slug/profile"
            cp "$demo_dir/profile.html" "$WEB_DIR/$slug/profile/index.html"
            echo "  Deployed: $slug/profile"
        fi

        # Copy ops app (Streamlit will be set up separately by deploy-app.sh)
        if [ -f "$demo_dir/apps/ops/app.py" ]; then
            mkdir -p "$AGENT_DIR/companies/$slug/apps/ops"
            cp -r "$demo_dir/"* "$AGENT_DIR/companies/$slug/"
            echo "  Copied ops app: $slug (run deploy-app.sh to start Streamlit service)"
        fi
    done
fi

chown -R agent:agent "$AGENT_DIR"

# --- 4. Write config.env -----------------------------------------------------

echo ""
echo "[4/6] Writing config.env..."

cat > "$AGENT_DIR/config.env" <<EOF
AGENT_DOMAIN=$DOMAIN
AGENT_EMAIL=hello@$DOMAIN
AGENT_DIR=$AGENT_DIR
COMPANIES_DIR=$AGENT_DIR/companies
PYTHON_BIN=$AGENT_DIR/venv/bin/python3
STREAMLIT_BIN=$AGENT_DIR/venv/bin/streamlit
EOF

echo "  Written: $AGENT_DIR/config.env"

# --- 5. Configure Caddy ------------------------------------------------------

echo ""
echo "[5/6] Configuring Caddy..."

CADDYFILE="/etc/caddy/Caddyfile"
cat > "$CADDYFILE" <<CADDY
$DOMAIN {
    root * $WEB_DIR
    file_server

    # APPS_START
    # (deploy-app.sh inserts Streamlit reverse_proxy routes here)
    # APPS_END

    handle {
        root * $WEB_DIR
        try_files {path} {path}/ /index.html
        file_server
    }
}
CADDY

systemctl reload caddy
echo "  Caddy configured for $DOMAIN"

# --- 6. Systemd timer --------------------------------------------------------

echo ""
echo "[6/6] Setting up pipeline timer..."

cat > /etc/systemd/system/carrier-demo-factory.service <<SVC
[Unit]
Description=Carrier Demo Factory — pipeline cycle
After=network.target

[Service]
Type=oneshot
User=agent
WorkingDirectory=$AGENT_DIR
EnvironmentFile=$AGENT_DIR/config.env
ExecStart=/bin/bash $AGENT_DIR/scripts/run-cycle.sh
StandardOutput=journal
StandardError=journal
SVC

cat > /etc/systemd/system/carrier-demo-factory.timer <<TMR
[Unit]
Description=Run Carrier Demo Factory every 6 hours

[Timer]
OnBootSec=10min
OnUnitActiveSec=6h
Unit=carrier-demo-factory.service

[Install]
WantedBy=timers.target
TMR

systemctl daemon-reload
# Note: timer is installed but NOT started automatically.
# Start it manually when you're ready to generate companies:
#   systemctl enable --now carrier-demo-factory.timer
echo "  Timer installed (not started — run 'systemctl enable --now carrier-demo-factory.timer' when ready)"

# --- Done --------------------------------------------------------------------

echo ""
echo "================================================================"
echo "  SETUP COMPLETE"
echo "================================================================"
echo ""
echo "Next steps:"
echo ""
echo "  1. Authenticate Claude Code (as agent user):"
echo "     su - agent && claude login"
echo ""
echo "  2. Point your DNS: A record for $DOMAIN -> $(curl -s ifconfig.me 2>/dev/null || echo '<this server IP>')"
echo ""
echo "  3. Start generating demos:"
echo "     systemctl enable --now carrier-demo-factory.timer"
echo "     # or run one cycle manually:"
echo "     su - agent -c 'bash $AGENT_DIR/scripts/run-cycle.sh'"
echo ""
echo "  4. Portfolio live at: https://$DOMAIN"
echo ""
