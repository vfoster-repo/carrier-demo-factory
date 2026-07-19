# VPS Setup Guide

How to set up the Carrier Demo Factory on a Linux VPS so the pipeline runs
automatically and the output is served at your domain.

**Estimated time:** 30–60 minutes for a fresh server.

---

## Prerequisites

- A Linux VPS (Ubuntu 22.04 or Debian 12 recommended) with root access
- A domain name pointed at your server's IP (e.g. `carrier-demo-factory.yourdomain.com`)
- An Anthropic API key with Claude Code access
- Basic comfort with the Linux command line

---

## Step 1 — System dependencies

```bash
# Update and install basics
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git curl nodejs npm

# Install Claude Code
npm install -g @anthropic-ai/claude-code
claude --version   # verify

# Install Caddy (HTTPS reverse proxy)
apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install -y caddy
```

---

## Step 2 — Create the agent user and directory structure

```bash
# Create a non-root user for the agent
useradd -m -s /bin/bash agent
usermod -aG sudo agent   # needed for systemd service management

# Create directory structure
mkdir -p /opt/carrier-factory/{companies,prompts,scripts,logs,web}
chown -R agent:agent /opt/carrier-factory

# Create Python virtual environment
python3 -m venv /opt/carrier-factory/venv
/opt/carrier-factory/venv/bin/pip install streamlit pandas plotly
```

---

## Step 3 — Clone the repo and configure

```bash
su - agent
cd /opt/carrier-factory

git clone https://github.com/vfoster-repo/carrier-demo-factory .repo

# Copy prompts and scripts into place
cp .repo/prompts/* /opt/carrier-factory/prompts/
cp .repo/scripts/* /opt/carrier-factory/

# Configure
cp .repo/config.env.example /opt/carrier-factory/config.env
nano /opt/carrier-factory/config.env
```

Fill in `config.env`:

```bash
AGENT_DOMAIN=carrier-demo-factory.yourdomain.com
AGENT_EMAIL=hello@yourdomain.com
COMPANIES_DIR=/opt/carrier-factory/companies
AGENT_DIR=/opt/carrier-factory
```

**Authenticate Claude Code** (do this as the `agent` user):

```bash
claude login
# Follow the browser prompt to authenticate with your Anthropic account
```

---

## Step 4 — Configure Caddy

Edit `/etc/caddy/Caddyfile` (or wherever Caddy looks for its config):

```caddy
carrier-demo-factory.yourdomain.com {
    # Static files (HTML reports and profile pages)
    # Served from /opt/carrier-factory/companies/{slug}/{report,profile}/
    root * /opt/carrier-factory/web
    file_server

    # APPS_START
    # (deploy-app.sh inserts reverse_proxy routes here automatically)
    # APPS_END

    # Fallback to portfolio index
    handle {
        root * /opt/carrier-factory/web
        try_files {path} /index.html
        file_server
    }
}
```

The `# APPS_START` / `# APPS_END` comments are markers that `deploy-app.sh`
uses to insert new Caddy routes automatically. **Do not remove them.**

Reload Caddy:

```bash
systemctl reload caddy
systemctl status caddy   # verify no config errors
```

---

## Step 5 — Configure deploy scripts

The deploy scripts copy HTML files into the web directory Caddy serves.
Check the paths at the top of each script match your setup:

```bash
# In deploy-report.sh and deploy-profile.sh:
WEB_DIR="${WEB_DIR:-/opt/carrier-factory/web}"

# In deploy-app.sh:
AGENT_DIR="/opt/carrier-factory"
CADDYFILE="$AGENT_DIR/Caddyfile"   # point this at your actual Caddyfile location
```

If your Caddyfile is at `/etc/caddy/Caddyfile`, update `deploy-app.sh` accordingly.

---

## Step 6 — Test a manual run

```bash
su - agent
source /opt/carrier-factory/config.env
cd /opt/carrier-factory

# Initialize state
echo "PHASE: create_company" > /opt/carrier-factory/current_state.txt

# Run one full pipeline cycle
bash /opt/carrier-factory/run-cycle.sh
```

Watch the logs:

```bash
tail -f /opt/carrier-factory/logs/latest.log
```

A full cycle takes 20–90 minutes depending on carrier size. When it completes,
`/opt/carrier-factory/companies/{slug}/` will contain `report.html`, `profile.html`,
and `apps/ops/app.py`, and the Streamlit service will be running.

---

## Step 7 — Set up the systemd timer (automated runs)

Create `/etc/systemd/system/carrier-demo-factory.service`:

```ini
[Unit]
Description=Carrier Demo Factory — pipeline cycle
After=network.target

[Service]
Type=oneshot
User=agent
WorkingDirectory=/opt/carrier-factory
EnvironmentFile=/opt/carrier-factory/config.env
ExecStart=/bin/bash /opt/carrier-factory/run-cycle.sh
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/carrier-demo-factory.timer`:

```ini
[Unit]
Description=Run Carrier Demo Factory every 6 hours

[Timer]
OnBootSec=5min
OnUnitActiveSec=6h
Unit=carrier-demo-factory.service

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
systemctl daemon-reload
systemctl enable carrier-demo-factory.timer
systemctl start carrier-demo-factory.timer
systemctl list-timers carrier-demo-factory.timer   # verify
```

---

## Backing Up Demo Output to GitHub

After a company is generated, copy its output into the `demos/` folder of the
repo and commit it. This keeps GitHub as the source of truth and backup.

```bash
SLUG=calloway-freight
REPO_DIR=/opt/carrier-factory/.repo

# Copy output into demos/
cp -r /opt/carrier-factory/companies/$SLUG $REPO_DIR/demos/$SLUG

cd $REPO_DIR
git add demos/$SLUG
git commit -m "Add $SLUG demo output"
git push
```

The HTML files in `demos/` are then served by GitHub Pages immediately.

---

## Troubleshooting

**Claude authentication fails:**
Run `claude login` as the `agent` user. Tokens are stored in `~/.claude/`.

**Caddy route not updating:**
Check that `# APPS_END` exists in your Caddyfile. `deploy-app.sh` inserts
routes immediately before that comment.

**Streamlit service not starting:**
Check `journalctl -u co-{company-slug}-ops -n 50`. Common cause: path to
`app.py` is wrong, or a Python import is missing from the venv.

**Pipeline stops mid-cycle:**
Check `current_state.txt` — it shows the last phase that was reached.
Re-run `run-cycle.sh` to resume from where it left off. Each phase is
idempotent; re-running an already-completed phase will regenerate that
file (safe to do).

**Port conflicts:**
All assigned ports are tracked in `/opt/carrier-factory/port_registry.txt`.
Check it if you suspect port collisions.
