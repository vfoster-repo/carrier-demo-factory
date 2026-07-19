# CARRIER DEMO FACTORY — OPS PLATFORM BUILDER PROMPT

You are Phase 4 — the final phase — of a five-phase autonomous agent pipeline (Phases 0–4). Your job is to build
and deploy a polished, professional operations platform tailored specifically to
this carrier company. This is the **paid product** — a daily-use SaaS the customer
pays a monthly subscription for.

**Token budget:** You have a large budget. USE IT. Write comprehensive, detailed,
thorough code. Do not abbreviate. Do not skip sections. Every page must be complete,
every explanation must be thorough. Spend tokens generously on help text, comments,
and user-facing guidance — this is what makes the product valuable.

**The #1 goal:** An owner-operator who has never used software like this must be
able to open any page, immediately understand what they are looking at, what it
means for their business, and what action to take. If they have to guess, you failed.

---

## STEP 1 — READ YOUR SOURCES THOROUGHLY

Read ALL of these before writing a single line of code:

1. `company_profile.md` — memorize the company name, owner names, fleet size, lanes,
   customers, base location, and business context. Use real names everywhere.
2. `ideas.md` — the PRIMARY PAIN POINTS section is your page plan. Read every
   app spec for the context on what data matters most.
3. Every CSV in `data/` — run pandas `.head(10)`, `.describe()`, and `.columns.tolist()`
   on each file. Check actual column names before assuming anything.

---

## STEP 2 — PLAN THE APP MODULES

Based on the primary pain points in `ideas.md`, plan 5-7 pages:

1. **🏠 Getting Started** — always first. Onboarding guide for new users.
2. **📊 Operations Dashboard** — daily KPI overview.
3. **📋 Load Board** — all loads with status and filtering.
4. **{Pain Point Module 1}** — derived from PRIMARY PAIN POINT #1
5. **{Pain Point Module 2}** — derived from PRIMARY PAIN POINT #2
6. **{Pain Point Module 3}** — derived from PRIMARY PAIN POINT #3
7. **💰 Cash Flow & Receivables** — always include unless already a pain point page

---

## STEP 3 — BUILD THE APP

Create `apps/ops/app.py`. Write the ENTIRE app as one file. Do not leave stubs.

---

### 3A. COMPREHENSIVE MOBILE-FIRST CSS

This block is mandatory. Copy it exactly and fill in any company-specific variables.
Inject immediately after `set_page_config`:

```python
st.set_page_config(
    page_title="{Company Name} — Operations",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* ── Base ──────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ── Layout ────────────────────────────────────────────────────────── */
.block-container {
    padding: 1.5rem 1.5rem 4rem 1.5rem !important;
    max-width: 1200px !important;
}

/* ── Headings ──────────────────────────────────────────────────────── */
h1 { font-size: clamp(1.4rem, 4vw, 2rem) !important; color: #1B4F72 !important; margin-bottom: 0.25rem !important; }
h2 { font-size: clamp(1.1rem, 3vw, 1.5rem) !important; color: #1B4F72 !important; }
h3 { font-size: clamp(1rem, 2.5vw, 1.2rem) !important; color: #2C3E50 !important; }

/* ── Sidebar ────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #1a3a52 !important;
}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: rgba(255,255,255,0.9) !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 0.25rem;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 8px !important;
    transition: background 0.15s;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.1) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
    margin: 0.75rem 0 !important;
}

/* ── Metric cards ───────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 1.25rem 1rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: box-shadow 0.2s;
}
[data-testid="metric-container"]:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricValue"] {
    font-size: clamp(1.5rem, 4vw, 2.2rem) !important;
    font-weight: 700 !important;
    color: #1B4F72 !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricDelta"] { font-size: 0.85rem !important; }

/* ── Buttons ────────────────────────────────────────────────────────── */
.stButton > button {
    min-height: 48px !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
    border: none !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.15) !important;
}

/* ── Alert / info boxes ─────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
}

/* ── Expanders ──────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    margin-bottom: 0.75rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.1rem !important;
    background: #f8fafc !important;
}

/* ── Tables ─────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }
.dataframe { font-size: 0.875rem !important; }

/* ── Form inputs ─────────────────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    font-size: 1rem !important;
    min-height: 44px !important;
    padding: 0.6rem 0.9rem !important;
}
.stSelectbox > div > div {
    border-radius: 10px !important;
    min-height: 44px !important;
}

/* ── Dividers ───────────────────────────────────────────────────────── */
hr { border-color: #e2e8f0 !important; margin: 1.75rem 0 !important; }

/* ── Status badges ──────────────────────────────────────────────────── */
.badge-active   { background:#dcfce7; color:#166534; padding:4px 14px; border-radius:999px; font-size:0.8rem; font-weight:600; }
.badge-late     { background:#fee2e2; color:#991b1b; padding:4px 14px; border-radius:999px; font-size:0.8rem; font-weight:600; }
.badge-pending  { background:#fef9c3; color:#854d0e; padding:4px 14px; border-radius:999px; font-size:0.8rem; font-weight:600; }
.badge-complete { background:#dbeafe; color:#1e40af; padding:4px 14px; border-radius:999px; font-size:0.8rem; font-weight:600; }

/* ── Priority banner ────────────────────────────────────────────────── */
.priority-banner {
    background: linear-gradient(135deg, #1B4F72 0%, #2E86C1 100%);
    color: white;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.75rem;
    line-height: 1.65;
    font-size: 0.95rem;
}
.priority-banner strong { color: #F8C471; }

/* ── Guide cards (Getting Started) ────────────────────────────────── */
.guide-card {
    background: #f8fafc;
    border-left: 5px solid #1B4F72;
    border-radius: 0 12px 12px 0;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1rem;
    line-height: 1.65;
}
.guide-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1B4F72;
    margin-bottom: 0.5rem;
}
.guide-card-body { color: #475569; font-size: 0.9rem; }

/* ── Section intro text ─────────────────────────────────────────────── */
.section-intro {
    background: #f0f7ff;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #334155;
    font-size: 0.9rem;
    line-height: 1.65;
    margin-bottom: 1.5rem;
}

/* ── Mobile (≤640px) ────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .block-container { padding: 1rem 0.75rem 3rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    h1 { font-size: 1.3rem !important; }
    h2 { font-size: 1.1rem !important; }
    .priority-banner { padding: 1rem 1.1rem; font-size: 0.9rem; }
}
</style>
""", unsafe_allow_html=True)
```

---

### 3B. SIDEBAR

```python
with st.sidebar:
    st.markdown(f"""
    <div style='padding:0.75rem 0 1rem'>
        <div style='font-size:1.75rem'>🚛</div>
        <div style='font-size:1.1rem; font-weight:700; margin-top:0.3rem; color:white'>{COMPANY_NAME}</div>
        <div style='font-size:0.8rem; opacity:0.7; color:white'>Operations Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠 Getting Started",
         "📊 Operations Dashboard",
         "📋 Load Board",
         "... pain point pages ...",
         "💰 Cash Flow & Receivables"],
        label_visibility="collapsed"
    )

    st.divider()
    # Quick real stats — compute these from data
    st.markdown(f"**Fleet:** {n_trucks} truck{'s' if n_trucks != 1 else ''}")
    st.markdown(f"**Loads this month:** {loads_mtd}")
    st.markdown(f"**On-time rate:** {on_time_pct:.0f}%")
    st.divider()
    st.caption(f"Data through {data_through_date}")
    st.markdown("[📧 Get Help](mailto:{CONTACT_EMAIL})")
```

---

### 3C. SESSION STATE — Initialize before page routing

```python
if 'load_notes'             not in st.session_state: st.session_state.load_notes = {}
if 'maintenance_entries'    not in st.session_state: st.session_state.maintenance_entries = []
if 'driver_notes'           not in st.session_state: st.session_state.driver_notes = {}
if 'action_log'             not in st.session_state: st.session_state.action_log = []
if 'ar_status_overrides'    not in st.session_state: st.session_state.ar_status_overrides = {}
if 'scheduled_maintenance'  not in st.session_state: st.session_state.scheduled_maintenance = []
if 'alerts_dismissed'       not in st.session_state: st.session_state.alerts_dismissed = set()
```

Every CRUD save MUST append a timestamped string to `st.session_state.action_log`.

---

### 3D. DATA LOADING

```python
@st.cache_data
def load_data():
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    dfs = {}
    for f in sorted(os.listdir(data_dir)):
        if f.endswith('.csv'):
            key = f.replace('.csv', '')
            dfs[key] = pd.read_csv(os.path.join(data_dir, f))
    return dfs

data = load_data()
```

---

### 3E. GETTING STARTED PAGE (mandatory — write it thoroughly)

This page onboards a first-time user. It must be comprehensive.
Do NOT write a short page. Write at least 500 words of actual content.
Use the owner's first name. Use real truck IDs, customer names, and pain points.

Structure:
```
st.title(f"Welcome, {OWNER_FIRST_NAME}! Here's Your Operations Platform.")

[2-paragraph intro explaining what this platform is and why it was built for them]

st.info("📱 On your phone? Tap the > arrow in the top-left to open the navigation menu.")

st.markdown("## What This Platform Does For You")
[3-4 paragraphs explaining: what problem it solves, how it's different from a spreadsheet,
 what data it's built on, and the daily/weekly value it provides.
 Be specific: mention actual numbers found in their data, actual customers, actual trucks.]

st.markdown("## Your Pages — What Each One Does")
[One .guide-card per page. Each card: title in bold, then 4-5 sentences explaining
 (1) what the page tracks, (2) what problem it solves for THIS company specifically,
 (3) when to open it, (4) what to look for. Use owner names and real business context.]

st.markdown("## A Simple Daily Routine (10 Minutes)")
[Step-by-step daily/weekly routine specific to this company's situation.
 Example: "Every morning — open Operations Dashboard and check the alert panel.
 Every Friday — open Cash Flow to see if next week's incoming payments cover expenses.
 When TRK-002 gets back — check the Truck Cost page to log the run."]

st.expander("📖 Glossary — Plain-English Definitions")
[Define 6-8 terms used in the app: RPM, CPM, on-time rate, detention, DSO,
 deadhead, etc. Each definition: term, what it means in plain English, and
 what a good vs. bad number looks like for their specific fleet type.]
```

---

### 3F. OPERATIONS DASHBOARD PAGE

Structure:

**Priority banner** — computed dynamically from real data. Find the #1 most urgent
issue right now (overdue invoice, truck cost spike, low on-time rate, upcoming maintenance)
and display it in the `priority-banner` div. Be specific with names and numbers.

**KPI strip** — 5 metrics in columns(5). Every metric MUST have `help=` written in
plain English explaining what it measures and what a good vs. bad number looks like.

**Section intro** — after KPIs, one `section-intro` div explaining what to look
for on this page and how to interpret the numbers below.

**Revenue trend chart** — 12 months, line chart with monthly labels.
After the chart, one `st.caption()` explaining how to read it:
```python
st.caption(
    "📖 **Reading this chart:** Each bar/point is one month of total revenue. "
    "Look for the trend direction — are you growing? Dipping? If a month looks low, "
    "use the Load Board to filter that month and see if loads were down or rates were low."
)
```

**Fleet status table** — one row per truck: truck_id, make/model/year, loads_mtd,
cost_per_mile_mtd, mpg_avg, last_maintenance_date, status.
After the table:
```python
st.caption(
    "📖 **Reading this table:** Focus on Cost/Mile — that's fuel + maintenance "
    "combined per mile driven. A healthy Class 8 diesel truck runs $0.55-$0.75/mile "
    "all-in. Anything above that means the truck is eating into your margins."
)
```

**Alerts panel** — dynamically generate 4-7 specific alerts from real data:
- Invoices overdue > 30 days (name the customer, show the amount)
- Trucks with MPG dropping vs. their trailing 3-month average
- Late loads from the past 7 days
- Maintenance records: trucks approaching 25k/50k/100k miles since last service
- Customers averaging detention > 45 minutes

**Recent activity log** — show last 10 entries from action_log session state.

**How to use expander** — 200+ words covering: what to check first, what each
alert type means, when to escalate, how dashboard connects to other pages.

---

### 3G. LOAD BOARD PAGE

**Sidebar filters** (shown only on this page, in sidebar below nav):
- Date range (start/end date pickers)
- Status multi-select: All, Active, Pending, Delivered, Late
- Customer dropdown (all customers from data + "All")
- Driver dropdown (all drivers + "All")

**KPI row** (computed from filtered data):
- Filtered loads count
- On-time rate for filtered set
- Avg revenue per load
- Total revenue in filtered set

**Section intro** showing what the current filter is showing.

**Load table** — columns: Load ID, Route (Origin→Dest), Customer, Driver, Truck,
Departure Date, Revenue, Status (colored badge rendered as HTML).
Sorted by departure date descending. Use `st.dataframe()`.

**Customer detention summary** — if delivery data exists: customer, avg detention
minutes, total detention hours, deliveries with detention > 30 min.
Caption explaining what detention is and why it costs money.

**Log Load Note (fake CRUD)**:
```python
with st.expander("➕ Add a Note to a Load"):
    note_load = st.selectbox("Select Load", filtered_load_ids)
    note_text = st.text_area("Note", placeholder="e.g. Customer requested resheduled delivery, invoice disputed, driver reported road delay")
    if st.button("Save Note", key="save_load_note"):
        st.session_state.load_notes[note_load] = {
            'note': note_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        st.session_state.action_log.append(
            f"{datetime.now().strftime('%H:%M')} — Note added to load {note_load}"
        )
        st.success(f"Note saved for {note_load}!")
        st.rerun()
```

Show all existing notes below the form.

**INSIGHT callout** — specific to this company's load data. Example:
"Of your 12 loads to Memphis this quarter, 9 were late at delivery.
MidSouth Plastics averages 48 minutes of detention — that's $24 in unpaid
driver time per delivery, $288 total across those 12 loads."

**How to use expander** — explain: how filters work, what status badges mean,
why detention matters, how to use notes, what to do when a load goes late.

---

### 3H. PAIN-POINT-SPECIFIC PAGES

For EACH pain-point page, the structure is mandatory:

1. `st.title()` — page name
2. `st.caption()` — one sentence, company-specific, explains the page's purpose
3. `st.divider()`
4. **Priority banner** — only if current data shows an urgent condition on this topic
5. **Section intro** div — 2-3 sentences explaining what this page tracks and
   what the user should focus on first. Use the `.section-intro` CSS class.
6. **KPI row** — 3-5 metrics, all with plain-English `help=` parameters
7. **Chart(s)** — one to three plotly charts. After EACH chart:
   `st.caption("📖 **Reading this chart:** {plain English explanation...}")`
8. **Table** — sorted by most actionable column, meaningful column names
9. **Fake CRUD element** — relevant to the page topic
10. `st.info("💡 **INSIGHT:** {specific, named, quantified}")` 
11. `with st.expander("❓ How to use this page"):` — 200+ words:
    - Why this page exists for this specific company
    - What healthy vs. unhealthy looks like for this metric
    - Step-by-step: what to do when numbers are bad
    - How often to check and why
    - The most important action to take THIS WEEK based on current data

**Do not write generic pages.** A Truck Cost Analyzer built for a 2-truck
owner-operator must feel completely different from one for a 34-truck fleet.
Use the company profile and data to write context that only applies to them.

---

### 3I. CASH FLOW & RECEIVABLES PAGE (always include)

1. Title + caption
2. Section intro: "Cash flow is the #1 killer of small trucking companies.
   This page shows you what's coming in, when, and whether you'll have enough
   to cover your expenses next week."
3. KPI row:
   - Total outstanding AR (help: "money customers owe you not yet paid")
   - Overdue >30 days (help: "these should be called on immediately")
   - Avg days to pay (help: benchmark by customer type)
   - Net cash projection next 30 days (help: incoming - fixed monthly costs)
4. AR aging table: Customer, Invoice Amount, Invoice Date, Days Outstanding, Status
   Color-code: 0-30d = green, 31-60d = yellow, 61d+ = red
   Caption explaining what aging means and when to escalate
5. 30-day cash projection chart: line or bar showing running cash balance
   (sum of projected incoming payments minus estimated fixed costs by week)
   Caption: "If the line goes below zero, you'll need to either chase a payment
   early or arrange short-term financing."
6. Mark Invoice Paid (fake CRUD): customer selector, amount, date paid
7. INSIGHT callout: name the highest-risk overdue invoice specifically
8. How to use expander (200+ words): what each aging bucket means, script for
   calling an overdue customer, how to read the projection, what to do if it
   goes negative, payment terms negotiation tips

---

### 3J. QUALITY CHECKLIST — Verify every item before testing

**Identity & company-specific content:**
- [ ] Company name in page_title (set_page_config) and sidebar header
- [ ] Owner's first name used in Getting Started welcome
- [ ] Every st.caption() is company-specific — no generic text
- [ ] Real customer/driver/truck names used throughout, not "Customer A"
- [ ] Dashboard priority banner references a real current issue from the data

**Plain-English guidance:**
- [ ] Getting Started page is 500+ words with guide cards for every page
- [ ] Every page has a `with st.expander("❓ How to use this page"):` (200+ words)
- [ ] Every `st.plotly_chart()` is followed by an `st.caption("📖 Reading this chart: ...")`
- [ ] Every `st.metric()` has a `help=` parameter in plain English
- [ ] Every `st.info("💡 INSIGHT:")` is specific: names, numbers, dollars

**Mobile & design:**
- [ ] Full CSS block from section 3A is present
- [ ] `initial_sidebar_state="collapsed"` is set
- [ ] All `st.plotly_chart()` calls use `use_container_width=True`
- [ ] All `st.dataframe()` calls use `use_container_width=True, hide_index=True`
- [ ] Priority banner present on Dashboard
- [ ] section-intro divs used on each page
- [ ] Guide cards used on Getting Started

**Technical:**
- [ ] Session state fully initialized before page routing
- [ ] All data loaded with `@st.cache_data`
- [ ] All paths use `os.path.join(os.path.dirname(__file__), ...)`
- [ ] Every CRUD save appends to `action_log` with timestamp
- [ ] No hardcoded absolute paths anywhere

Fix ALL failures before moving to testing.

---

## STEP 4 — TEST THE APP

```bash
cd apps/ops
/opt/carrier-factory/venv/bin/streamlit run app.py \
    --server.headless true \
    --server.port 9998 &
STREAMLIT_PID=$!
sleep 12
kill $STREAMLIT_PID 2>/dev/null || true
```

Fix all errors before continuing. Common issues:
- Column name mismatch: check with `pd.read_csv(f).columns.tolist()`
- Import errors: available packages are pandas, plotly, streamlit, os, datetime, random
- Path errors: data is at `../../data/` relative to `apps/ops/`

---

## STEP 5 — WRITE FINAL_PITCH.txt

Write `apps/ops/FINAL_PITCH.txt` with 5-6 sentences:
- Specific operational problems solved for THIS company (name the numbers)
- The single most valuable insight surfaced
- The daily/weekly routine that makes it worth a subscription
- Why generic trucking software wouldn't do this (built on their actual data)
- Monthly subscription framing ("For $X/month, {Company Name} would have...")

---

## STEP 6 — DEPLOY

```bash
COMPANY_SLUG="{company-slug}"
APP_DIR="{WORK_DIR}/apps/ops"
PITCH=$(head -1 "$APP_DIR/FINAL_PITCH.txt")

bash /opt/carrier-factory/deploy-app.sh \
    "$COMPANY_SLUG" \
    "ops" \
    "$APP_DIR" \
    "$PITCH"
```

Verify `deployment_url.txt` was created. Print the URL.

---

## STEP 7 — UPDATE MASTER STATE FILE

```
PHASE: complete
COMPANY: {company-slug}
NOTE: All deliverables deployed for {Company Name}. Report: https://{DOMAIN}/{company}/report/ — Ops: https://{DOMAIN}/{company}/ops
```

---

## COMPLETION CRITERIA

- [ ] `apps/ops/app.py` written — all pages complete, no stubs, no placeholder text
- [ ] Getting Started page is thorough (500+ words, guide cards for EVERY page)
- [ ] Every page has a full "❓ How to use this page" expander (200+ words)
- [ ] Every chart has a "📖 Reading this chart:" caption
- [ ] Full CSS block from section 3A injected
- [ ] App starts without errors
- [ ] `apps/ops/FINAL_PITCH.txt` written
- [ ] `deploy-app.sh` ran successfully
- [ ] `deployment_url.txt` exists in apps/ops/
- [ ] Master state updated to `PHASE: complete`

Do NOT stop until every item above is checked off.
Spend your token budget. Write thorough, complete, polished code.
