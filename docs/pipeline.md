# Pipeline Reference

How each phase of the Carrier Demo Factory works — what it reads, what it writes,
and what Claude is actually doing.

---

## Overview

The pipeline is a 5-phase state machine. State is tracked in a plain text file
(`current_state.txt`) with a single `PHASE:` field. `run-cycle.sh` reads the
current phase, selects the matching prompt, builds a session context block,
and invokes Claude Code with `--dangerously-skip-permissions`.

Each phase ends by writing the next phase name into `current_state.txt`. If
the orchestrator is running unattended (systemd timer), the next invocation
picks up exactly where the last one left off.

---

## Phase 1 — Company Creator

**Prompt:** `prompts/01-company-creator.md`  
**Working dir:** `COMPANIES_DIR/`  
**Triggered by:** `PHASE: create_company`  
**Sets next phase:** `PHASE: generate_ideas`

### What Claude does

1. Uses a time-based seed to deterministically pick a carrier type
   (`owner_operator` / `small_fleet` / `regional_carrier` / `mid_size_carrier`)
2. Designs a complete fictional company — name, owner backstory, home terminal,
   primary lanes, customers, and **3–5 specific embedded pain points**
3. Creates `{company-slug}/company_profile.md` with identity, operational facts,
   and pain points
4. Writes and runs `generate_data.py` — a Python script that produces 9 CSV files
   encoding the pain points with statistical significance

### The pain point engineering rule

Pain points must be *visible in the data with statistical significance*. If a
truck has bad MPG, its `actual_mpg` values must be consistently 20–30% below
fleet average across hundreds of trips — not just occasionally. The idea generator
will independently discover these from the raw numbers; the data must make them
obvious to a forensic analyst.

### Output

```
{company-slug}/
├── company_profile.md
├── generate_data.py
└── data/
    ├── drivers.csv
    ├── trucks.csv
    ├── customers.csv
    ├── routes.csv
    ├── loads.csv
    ├── trips.csv
    ├── fuel_purchases.csv
    ├── delivery_events.csv
    └── maintenance_records.csv
```

**Data scale by carrier type:**

| Type | Loads | Trucks | Drivers | Years of data |
|---|---|---|---|---|
| owner_operator | 400–600 | 1–2 | 1–2 | 2 |
| small_fleet | 3,000–6,000 | 5–15 | 8–20 | 2 |
| regional_carrier | 15,000–30,000 | 20–50 | 30–70 | 2 |
| mid_size_carrier | 50,000–80,000 | 75–150 | 100–200 | 2 |

---

## Phase 2 — Idea Generator

**Prompt:** `prompts/02-idea-generator.md`  
**Working dir:** `COMPANIES_DIR/{company-slug}/`  
**Triggered by:** `PHASE: generate_ideas`  
**Sets next phase:** `PHASE: build_report`

### What Claude does

1. Reads `company_profile.md` — but **stops before the "Pain Points" section**.
   This is intentional: Claude must discover the problems analytically, not be told.
2. Loads every CSV with pandas, runs descriptive statistics and analytical queries
   across all dimensions (revenue/mile by route, MPG by truck, detention by customer,
   maintenance cost trends, driver performance, cash flow indicators)
3. Saves analysis output to `analysis_output/`
4. Identifies the 3–5 **Primary Pain Points** — the most costly/urgent findings,
   quantified with actual names and numbers
5. Generates 8–15 distinct app ideas, each with a full build specification
6. Writes `ideas.md`

### The self-blinding trick

The agent is explicitly instructed to stop reading `company_profile.md` when it
hits the "Pain Points" section header. It then independently derives the same
problems from the data. This validates that the pain points are actually visible
in the data (not just asserted in prose) and produces more authentic analyst
language in the output.

### Output

```
{company-slug}/
├── ideas.md
├── analyze.py
└── analysis_output/
    └── summary.txt
```

---

## Phase 3 — Report Builder

**Prompt:** `prompts/03-report-builder.md`  
**Working dir:** `COMPANIES_DIR/{company-slug}/`  
**Triggered by:** `PHASE: build_report`  
**Sets next phase:** `PHASE: build_profile`

### What Claude does

1. Reads `company_profile.md` + `ideas.md` + all CSVs
2. Writes and runs `build_report_data.py` — extracts aggregated chart data as JSON
3. Writes `report.html` — a fully self-contained single-file HTML page with:
   - One section per primary pain point
   - Metric cards with delta indicators
   - Embedded Plotly charts (JSON data inlined in `<script>` blocks)
   - A "key finding" callout per section
   - A pitch section describing the ops platform
   - Mobile-responsive CSS (no external stylesheets)

### Design constraints

- **Zero external file dependencies** except the Plotly CDN — the file must work
  if you email it or open it from a USB drive
- **Mobile-first** — readable on a phone without zooming
- Charts keep datasets to 10–20 rows max (enough for insight, not overwhelming)

### Output

```
{company-slug}/
├── report.html
├── build_report_data.py
└── deployment_url.txt   ← written by deploy-report.sh
```

---

## Phase 3.5 — Profile Builder

**Prompt:** `prompts/04-profile-builder.md`  
**Working dir:** `COMPANIES_DIR/{company-slug}/`  
**Triggered by:** `PHASE: build_profile`  
**Sets next phase:** `PHASE: build_ops_app`

### What Claude does

1. Reads everything: `company_profile.md`, `ideas.md`, all CSVs, and the
   deployment URLs for report + ops app (if they exist)
2. Extracts headline statistics (row counts, date ranges, striking facts)
3. Writes `profile.html` — a dark-theme GitHub-style company profile page with:
   - Hero section (company name, type, tagline)
   - Stat strip (trucks, drivers, customers, estimated revenue)
   - About section (company story in plain English)
   - "What We Found" section (4–7 quantified findings from the data)
   - Data inventory table (one row per CSV with row count, date range, columns)
   - Pain point cards (one per primary pain point)
   - Product cards linking to report + ops platform

### Purpose

This page serves two audiences: the prospect (a transparent look at the process)
and everyone else (context that makes the demo meaningful without the back story).

---

## Phase 4 — Ops Platform Builder

**Prompt:** `prompts/05-ops-builder.md`  
**Working dir:** `COMPANIES_DIR/{company-slug}/`  
**Triggered by:** `PHASE: build_ops_app`  
**Sets next phase:** `PHASE: complete`

### What Claude does

1. Reads company profile + ideas + all CSVs
2. Plans 5–7 pages based on the primary pain points from `ideas.md`
3. Writes the entire Streamlit app as a single `apps/ops/app.py` file
4. Tests that it launches without errors
5. Writes `apps/ops/FINAL_PITCH.txt` — a 5–6 sentence sales pitch for the platform
6. Deploys via `deploy-app.sh`

### Mandatory pages

Every ops platform includes:
- **Getting Started** — 500+ word onboarding guide, guide cards for every page,
  daily/weekly routine, plain-English glossary
- **Operations Dashboard** — KPI strip, priority banner (dynamically generated
  from real data), revenue trend, fleet status table, alerts panel
- **Load Board** — full filterable load table with customer detention summary
- **Pain-point-specific pages** — one page per primary pain point (e.g.
  "Truck Cost Analyzer", "Customer Detention Tracker", "Lane Profitability")
- **Cash Flow & Receivables** — AR aging table, 30-day cash projection, fake CRUD

### Quality rules enforced by the prompt

- Every `st.metric()` must have a `help=` parameter in plain English
- Every chart must be followed by `st.caption("📖 Reading this chart: ...")`
- Every page must have a `with st.expander("❓ How to use this page"):` (200+ words)
- Real customer/driver/truck names used throughout — no generic labels
- The Getting Started welcome uses the owner's first name

---

## State Machine

```
create_company
      │
      ▼
generate_ideas
      │
      ▼
build_report
      │
      ▼
build_profile
      │
      ▼
build_ops_app
      │
      ▼
  complete ──► (reset to create_company for next cycle)
```

State file format (plain text, `current_state.txt`):
```
PHASE: generate_ideas
COMPANY: calloway-freight
NOTE: Company created — 2 trucks, 4 customers, 5 pain points embedded
```

---

## Running a Single Phase Manually

To re-run a specific phase without the full orchestrator:

```bash
source config.env
PHASE=build_report
COMPANY=calloway-freight
WORK_DIR="$COMPANIES_DIR/$COMPANY"
PROMPT_FILE="prompts/03-report-builder.md"

cd "$WORK_DIR"
claude --dangerously-skip-permissions -p "$(cat $PROMPT_FILE)

---

## CURRENT SESSION CONTEXT

Date: $(date +'%Y-%m-%d')
Domain: $AGENT_DOMAIN
Contact email: $AGENT_EMAIL
Companies base directory: $COMPANIES_DIR
Your working directory this cycle: $WORK_DIR
Master state file to update when done: $AGENT_DIR/current_state.txt"
```
