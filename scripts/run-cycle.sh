#!/bin/bash
# run-cycle.sh
# Three-phase state machine for the carrier demo factory.
# Each cycle produces one complete fictional carrier demo:
#   Phase 1 (create_company): generate company profile + synthetic data
#   Phase 2 (generate_ideas): analyze data, produce ideas.md
#   Phase 3 (build_report):   build self-contained HTML insights report
#   Phase 3.5 (build_profile): build static company profile / case-study page
#   Phase 4 (build_ops_app):  build multi-page Streamlit ops platform
#
# Called by systemd timer every 6 hours.

set -euo pipefail

# --- Root guard ---------------------------------------------------------------
if [ "$(id -u)" -eq 0 ]; then
    exec su -s /bin/bash agent -c "bash $0 $*"
fi

# --- Configuration ------------------------------------------------------------

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
COMPANIES_DIR="${COMPANIES_DIR:-$AGENT_DIR/companies}"
PROMPTS_DIR="$AGENT_DIR/prompts"
STATE_FILE="$AGENT_DIR/current_state.txt"
LOG_DIR="$AGENT_DIR/logs"
LOG_FILE="$LOG_DIR/cycle_$(date +%Y%m%d_%H%M%S).log"
LATEST_LOG="$LOG_DIR/latest.log"

# --- Setup --------------------------------------------------------------------

mkdir -p "$LOG_DIR" "$COMPANIES_DIR" "$PROMPTS_DIR"
exec > >(tee -a "$LOG_FILE" "$LATEST_LOG") 2>&1

echo "================================================================"
echo "  CARRIER DEMO FACTORY -- CYCLE START"
echo "  $(date +'%Y-%m-%d %H:%M:%S')"
echo "================================================================"

# --- Pre-flight ---------------------------------------------------------------

echo ""
echo "Running pre-flight checks..."

if ! command -v claude &> /dev/null; then
    echo "Claude Code not found. Run: npm install -g @anthropic-ai/claude-code"
    exit 1
fi
echo "Claude Code: $(claude --version)"

if [ ! -f "$STATE_FILE" ]; then
    echo "PHASE: create_company" > "$STATE_FILE"
fi

# --- Read Master State --------------------------------------------------------

echo ""
echo "Master state:"
echo "------------------------------------------------------------"
cat "$STATE_FILE"
echo ""
echo "------------------------------------------------------------"

PHASE=$(grep "^PHASE:" "$STATE_FILE" | awk '{print $2}' | head -1)

# If previous cycle completed a company, reset for a new one
if [ "$PHASE" = "complete" ]; then
    echo "Previous company complete. Starting new company."
    echo "PHASE: create_company" > "$STATE_FILE"
    PHASE="create_company"
    COMPANY=""
fi

# --- Phase loop: run all phases in one invocation ----------------------------

while [ "$PHASE" != "complete" ]; do

    COMPANY=$(grep "^COMPANY:" "$STATE_FILE" | cut -d' ' -f2- | head -1 || true)

    case "$PHASE" in
        create_company)
            PROMPT_FILE="$PROMPTS_DIR/01-company-creator.md"
            WORK_DIR="$COMPANIES_DIR"
            ;;
        generate_ideas)
            PROMPT_FILE="$PROMPTS_DIR/02-idea-generator.md"
            WORK_DIR="$COMPANIES_DIR/$COMPANY"
            ;;
        build_report)
            PROMPT_FILE="$PROMPTS_DIR/03-report-builder.md"
            WORK_DIR="$COMPANIES_DIR/$COMPANY"
            ;;
        build_profile)
            PROMPT_FILE="$PROMPTS_DIR/04-profile-builder.md"
            WORK_DIR="$COMPANIES_DIR/$COMPANY"
            ;;
        build_ops_app)
            PROMPT_FILE="$PROMPTS_DIR/05-ops-builder.md"
            WORK_DIR="$COMPANIES_DIR/$COMPANY"
            ;;
        *)
            echo "Unknown phase: $PHASE. Resetting."
            echo "PHASE: create_company" > "$STATE_FILE"
            exit 1
            ;;
    esac

    if [ ! -f "$PROMPT_FILE" ]; then
        echo "Prompt not found: $PROMPT_FILE"
        exit 1
    fi

    mkdir -p "$WORK_DIR"

    echo ""
    echo "================================================================"
    echo "  PHASE: $PHASE"
    echo "  Company: ${COMPANY:-[new, to be created]}"
    echo "================================================================"

    CURRENT_STATE=$(cat "$STATE_FILE")
    CURRENT_DATE=$(date +'%Y-%m-%d')
    CURRENT_TIME=$(date +'%H:%M:%S')

    CYCLE_PROMPT="$(cat "$PROMPT_FILE")

---

## CURRENT SESSION CONTEXT

Date: $CURRENT_DATE
Time: $CURRENT_TIME

Master state file ($STATE_FILE):
$CURRENT_STATE

Companies base directory: $COMPANIES_DIR
Your working directory this cycle: $WORK_DIR
Master state file to update when done: $STATE_FILE
deploy-app.sh location: $AGENT_DIR/deploy-app.sh
Domain: ${AGENT_DOMAIN:-your-domain.com}
Contact email: ${AGENT_EMAIL:-hello@your-domain.com}

Begin immediately. Do not pause between steps. Complete the entire
phase before stopping. Update the master state file when done."

    echo ""
    echo "Invoking Claude Code (phase: $PHASE)..."
    echo ""

    cd "$WORK_DIR"
    claude --dangerously-skip-permissions \
        -p "$CYCLE_PROMPT"

    CLAUDE_EXIT=$?

    echo ""
    echo "Phase $PHASE completed with exit code: $CLAUDE_EXIT"

    # Re-read phase in case Claude updated it
    PHASE=$(grep "^PHASE:" "$STATE_FILE" | awk '{print $2}' | head -1)

    echo "State is now: $PHASE"
    echo ""

done

# --- Done ---------------------------------------------------------------------

echo ""
echo "State after full pipeline:"
echo "------------------------------------------------------------"
cat "$STATE_FILE"
echo ""
echo "------------------------------------------------------------"
echo ""
echo "================================================================"
echo "  FULL PIPELINE COMPLETE -- $(date +'%Y-%m-%d %H:%M:%S')"
echo "================================================================"

# Clean up old logs (keep last 30)
ls -t "$LOG_DIR"/cycle_*.log 2>/dev/null | tail -n +31 | xargs -r unlink 2>/dev/null || true
