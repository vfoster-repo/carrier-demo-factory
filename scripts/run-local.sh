#!/bin/bash
# run-local.sh
# Local development runner for the Carrier Demo Factory.
# Mirrors run-cycle.sh but skips all deploy/systemd steps.
# Output lands in COMPANIES_DIR; copy finished demos into demos/ to commit.

set -euo pipefail

# --- Load config --------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.env"

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "ERROR: config.env not found. Copy config.env.example to config.env."
    exit 1
fi

AGENT_DIR="${AGENT_DIR:-$SCRIPT_DIR/..}"
COMPANIES_DIR="${COMPANIES_DIR:-$HOME/carrier-demo-factory-output}"
PROMPTS_DIR="$SCRIPT_DIR/../prompts"
STATE_FILE="$AGENT_DIR/current_state.txt"
LOG_DIR="$AGENT_DIR/logs"
LOG_FILE="$LOG_DIR/local_$(date +%Y%m%d_%H%M%S).log"
LATEST_LOG="$LOG_DIR/latest.log"

# Claude Code binary — check common install locations
CLAUDE_BIN=""
for candidate in \
    "$HOME/.local/bin/claude" \
    "$HOME/.npm-global/bin/claude" \
    "$(npm root -g 2>/dev/null)/.bin/claude" \
    "$(which claude 2>/dev/null)"; do
    if [ -x "$candidate" ]; then
        CLAUDE_BIN="$candidate"
        break
    fi
done

if [ -z "$CLAUDE_BIN" ]; then
    echo "ERROR: claude not found. Run: npm install -g @anthropic-ai/claude-code --prefix ~/.local"
    exit 1
fi

# --- Setup --------------------------------------------------------------------

mkdir -p "$LOG_DIR" "$COMPANIES_DIR"
exec > >(tee -a "$LOG_FILE" "$LATEST_LOG") 2>&1

echo "================================================================"
echo "  CARRIER DEMO FACTORY — LOCAL RUN"
echo "  $(date +'%Y-%m-%d %H:%M:%S')"
echo "  Output dir: $COMPANIES_DIR"
echo "================================================================"

# --- Pre-flight ---------------------------------------------------------------

echo ""
echo "Claude Code: $("$CLAUDE_BIN" --version)"
echo "Python:      $(python3 --version)"

if [ ! -f "$STATE_FILE" ]; then
    echo "PHASE: create_company" > "$STATE_FILE"
fi

# --- Read state ---------------------------------------------------------------

echo ""
echo "Current state:"
echo "------------------------------------------------------------"
cat "$STATE_FILE"
echo ""
echo "------------------------------------------------------------"

PHASE=$(grep "^PHASE:" "$STATE_FILE" | awk '{print $2}' | head -1)

if [ "$PHASE" = "complete" ]; then
    echo "Previous company complete. Starting new company."
    echo "PHASE: create_company" > "$STATE_FILE"
    PHASE="create_company"
fi

# --- Phase loop ---------------------------------------------------------------

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
    PYTHON_BIN="${PYTHON_BIN:-$(which python3)}"
    STREAMLIT_BIN="${STREAMLIT_BIN:-$(which streamlit 2>/dev/null || echo 'python3 -m streamlit')}"

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
Domain: ${AGENT_DOMAIN:-your-domain.com}
Contact email: ${AGENT_EMAIL:-hello@your-domain.com}
Python binary: $PYTHON_BIN
Streamlit binary: $STREAMLIT_BIN

⚠️  LOCAL MODE — IMPORTANT:
- Do NOT run any deploy scripts (deploy-app.sh, deploy-report.sh, deploy-profile.sh).
  They are not available locally. Skip all deploy steps entirely.
- For Streamlit testing (ops-builder phase), use: $STREAMLIT_BIN run app.py --server.headless true --server.port 9999 &
- Update the master state file as normal when each phase completes.
- Write all output files to disk as usual — just skip the deploy calls.

Begin immediately. Do not pause between steps."

    echo ""
    echo "Invoking Claude Code (phase: $PHASE)..."
    echo ""

    cd "$WORK_DIR"
    "$CLAUDE_BIN" --dangerously-skip-permissions \
        -p "$CYCLE_PROMPT"

    CLAUDE_EXIT=$?

    echo ""
    echo "Phase $PHASE completed (exit: $CLAUDE_EXIT)"

    PHASE=$(grep "^PHASE:" "$STATE_FILE" | awk '{print $2}' | head -1)
    echo "Next state: $PHASE"
    echo ""

done

# --- Done ---------------------------------------------------------------------

COMPANY=$(grep "^COMPANY:" "$STATE_FILE" | cut -d' ' -f2- | head -1 || true)

echo ""
echo "================================================================"
echo "  PIPELINE COMPLETE"
echo "  Company: $COMPANY"
echo "  Output:  $COMPANIES_DIR/$COMPANY"
echo "================================================================"
echo ""
echo "Next steps:"
echo "  1. Review output in: $COMPANIES_DIR/$COMPANY"
echo "  2. Open report.html and profile.html in a browser"
echo "  3. Run the Streamlit app:"
echo "     cd $COMPANIES_DIR/$COMPANY/apps/ops"
echo "     streamlit run app.py"
echo "  4. When satisfied, copy to repo:"
echo "     cp -r $COMPANIES_DIR/$COMPANY /home/victor/projects/carrier-demo-factory/demos/$COMPANY"
