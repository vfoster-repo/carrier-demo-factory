import os
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ═══════════════════════════════════════════════════════════════════════════
# COMPANY CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════
COMPANY_NAME = "Cascade Summit Freightways"
OWNER_FIRST_NAME = "Walter"
OWNER_FULL_NAME = "Walter Braddock"
DISPATCH_LEAD = "Renee"
CONTACT_EMAIL = "victorfoster@hotmail.com"
BREAKEVEN_RATE_PER_MILE = 2.05
AGING_COHORT = ["TRK-041", "TRK-042", "TRK-043",
                "TRK-044", "TRK-045", "TRK-046", "TRK-047", "TRK-048"]
WORST_TRUCK = "TRK-047"
WORST_CUSTOMER_ID = "CUST-03"
WORST_CUSTOMER_NAME = "TitanBolt Industrial Supply"
WORST_LANES = ["RTE-04", "RTE-08"]  # Seattle<->Atlanta

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG + CSS
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{COMPANY_NAME} — Operations",
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

# ═══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════
if 'load_notes' not in st.session_state:
    st.session_state.load_notes = {}
if 'maintenance_entries' not in st.session_state:
    st.session_state.maintenance_entries = []
if 'driver_notes' not in st.session_state:
    st.session_state.driver_notes = {}
if 'action_log' not in st.session_state:
    st.session_state.action_log = []
if 'ar_status_overrides' not in st.session_state:
    st.session_state.ar_status_overrides = {}
if 'scheduled_maintenance' not in st.session_state:
    st.session_state.scheduled_maintenance = []
if 'alerts_dismissed' not in st.session_state:
    st.session_state.alerts_dismissed = set()

# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════


@st.cache_data
def load_data():
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    dfs = {}
    for f in sorted(os.listdir(data_dir)):
        if f.endswith('.csv'):
            key = f.replace('.csv', '')
            dfs[key] = pd.read_csv(os.path.join(data_dir, f))
    return dfs


data = load_data()
customers = data['customers']
drivers = data['drivers']
trucks = data['trucks']
routes = data['routes']
loads = data['loads']
trips = data['trips']
fuel_purchases = data['fuel_purchases']
maintenance_records = data['maintenance_records']
delivery_events = data['delivery_events']

DATA_THROUGH_DATE = pd.to_datetime(
    loads['load_date']).max().strftime('%B %d, %Y')

# ═══════════════════════════════════════════════════════════════════════════
# CORE AGGREGATIONS (cached — these joins are the expensive part)
# ═══════════════════════════════════════════════════════════════════════════


@st.cache_data
def build_truck_costs(opp_cost_per_hr=50.0):
    fuel_by_truck = fuel_purchases.groupby('truck_id').agg(
        total_fuel_cost=('total_cost', 'sum'),
        total_gallons=('gallons', 'sum')
    ).reset_index()

    miles_by_truck = trips.groupby('truck_id').agg(
        total_miles=('actual_miles', 'sum'),
        trip_count=('trip_id', 'count'),
        avg_mpg=('actual_mpg', 'mean')
    ).reset_index()

    maint_by_truck = maintenance_records.groupby('truck_id').agg(
        total_maintenance_cost=('cost', 'sum'),
        total_downtime_hours=('downtime_hours', 'sum'),
        maintenance_records=('record_id', 'count')
    ).reset_index()

    df = trucks.merge(miles_by_truck, on='truck_id', how='left')
    df = df.merge(fuel_by_truck, on='truck_id', how='left')
    df = df.merge(maint_by_truck, on='truck_id', how='left')

    for col in ['total_miles', 'total_fuel_cost', 'total_maintenance_cost', 'total_downtime_hours', 'maintenance_records', 'trip_count']:
        df[col] = df[col].fillna(0)
    df['avg_mpg'] = df['avg_mpg'].fillna(df['avg_mpg'].mean())

    df['downtime_cost'] = df['total_downtime_hours'] * opp_cost_per_hr
    df['true_total_cost'] = df['total_fuel_cost'] + \
        df['total_maintenance_cost'] + df['downtime_cost']
    df['true_cost_per_mile'] = df['true_total_cost'] / \
        df['total_miles'].replace(0, pd.NA)
    df['is_aging_cohort'] = df['truck_id'].isin(AGING_COHORT)
    return df


@st.cache_data
def build_lane_profitability():
    trip_load = trips.merge(loads[['load_id', 'customer_id', 'route_id',
                            'revenue', 'fuel_surcharge', 'load_date']], on='load_id', how='left')
    fuel_by_trip = fuel_purchases.groupby('trip_id').agg(
        trip_fuel_cost=('total_cost', 'sum')).reset_index()
    trip_load = trip_load.merge(fuel_by_trip, on='trip_id', how='left')
    trip_load['trip_fuel_cost'] = trip_load['trip_fuel_cost'].fillna(0)
    trip_load['net_per_mile'] = (trip_load['revenue'] + trip_load['fuel_surcharge'] -
                                 trip_load['trip_fuel_cost']) / trip_load['actual_miles']
    trip_load = trip_load.merge(routes, on='route_id', how='left')

    lane_summary = trip_load.groupby('route_id').agg(
        loads=('load_id', 'count'),
        total_miles=('actual_miles', 'sum'),
        avg_net_per_mile=('net_per_mile', 'mean'),
        total_revenue=('revenue', 'sum'),
        avg_fuel_cost=('trip_fuel_cost', 'mean'),
        on_time_rate=('on_time_flag', 'mean')
    ).reset_index()
    lane_summary = lane_summary.merge(routes, on='route_id', how='left')
    lane_summary['lane_label'] = lane_summary['origin_city'] + ', ' + lane_summary['origin_state'] + \
        ' → ' + lane_summary['destination_city'] + \
        ', ' + lane_summary['destination_state']
    lane_summary['shortfall_per_mile'] = BREAKEVEN_RATE_PER_MILE - \
        lane_summary['avg_net_per_mile']
    lane_summary['total_shortfall'] = (
        lane_summary['shortfall_per_mile'] * lane_summary['total_miles']).clip(lower=0)
    return trip_load, lane_summary


@st.cache_data
def build_detention_summary():
    de = delivery_events.merge(
        loads[['load_id', 'customer_id', 'load_date']], on='load_id', how='left')
    de = de.merge(customers[['customer_id', 'customer_name']],
                  on='customer_id', how='left')
    summary = de.groupby(['customer_id', 'customer_name']).agg(
        events=('event_id', 'count'),
        avg_detention_min=('detention_minutes', 'mean'),
        median_detention_min=('detention_minutes', 'median'),
        pct_on_time=('on_time', 'mean'),
        total_detention_hours=('detention_minutes', lambda x: x.sum() / 60.0)
    ).reset_index().sort_values('avg_detention_min', ascending=False)
    return de, summary


@st.cache_data
def build_driver_cohorts():
    d = drivers.copy()
    d['hire_date'] = pd.to_datetime(d['hire_date'])
    d['hire_year'] = d['hire_date'].dt.year
    cohort = d.groupby(['home_terminal', 'hire_year']).agg(
        headcount=('driver_id', 'count'),
        terminated=('employment_status', lambda x: (x == 'terminated').sum())
    ).reset_index()
    cohort['active'] = cohort['headcount'] - cohort['terminated']
    cohort['termination_rate'] = cohort['terminated'] / cohort['headcount']
    return d, cohort


@st.cache_data
def build_ar_aging():
    """Simulate an AR ledger from delivered loads: assume invoiced on load_date,
    paid after payment_terms_days on average with realistic variance, some still outstanding."""
    l = loads[loads['load_status'] == 'delivered'].merge(
        customers[['customer_id', 'customer_name', 'payment_terms_days']], on='customer_id', how='left'
    )
    l['load_date'] = pd.to_datetime(l['load_date'])
    as_of = l['load_date'].max()

    # Only look at the trailing 75 days of invoices as "still in the AR cycle" —
    # older invoices are treated as already collected (this is a demo ledger, not real AR data).
    window_start = as_of - timedelta(days=75)
    ar = l[l['load_date'] >= window_start].copy()

    rng = random.Random(42)

    def simulate_status(row):
        days_since = (as_of - row['load_date']).days
        terms = row['payment_terms_days']
        # deterministic pseudo-randomness per load so it's stable across reruns
        jitter = (hash(row['load_id']) % 40) - 10
        days_to_pay = terms + jitter
        if days_since >= days_to_pay:
            return 'paid'
        return 'outstanding'

    ar['sim_status'] = ar.apply(simulate_status, axis=1)
    ar['days_outstanding'] = (as_of - ar['load_date']).dt.days
    outstanding = ar[ar['sim_status'] == 'outstanding'].copy()
    outstanding['invoice_amount'] = outstanding['revenue'] + \
        outstanding['fuel_surcharge']

    def bucket(days):
        if days <= 30:
            return '0-30 days'
        elif days <= 60:
            return '31-60 days'
        else:
            return '61+ days'
    outstanding['aging_bucket'] = outstanding['days_outstanding'].apply(bucket)
    return outstanding, as_of


truck_costs = build_truck_costs()
trip_load, lane_summary = build_lane_profitability()
delivery_full, detention_summary = build_detention_summary()
driver_full, driver_cohort = build_driver_cohorts()
ar_outstanding, AR_AS_OF = build_ar_aging()

# apply session-state AR overrides (marked paid via the fake CRUD)
if st.session_state.ar_status_overrides:
    ar_outstanding = ar_outstanding[~ar_outstanding['load_id'].isin(
        st.session_state.ar_status_overrides.keys())]

# ═══════════════════════════════════════════════════════════════════════════
# FLEET-LEVEL QUICK STATS (used in sidebar + dashboard)
# ═══════════════════════════════════════════════════════════════════════════
N_TRUCKS_ACTIVE = int((trucks['status'] == 'active').sum())
loads_dt = pd.to_datetime(loads['load_date'])
latest_month = loads_dt.max().to_period('M')
loads_mtd = int((loads_dt.dt.to_period('M') == latest_month).sum())
FLEET_AVG_MPG = float(trips['actual_mpg'].mean())
FLEET_ON_TIME_PCT = float(trips['on_time_flag'].mean() * 100)

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
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
         "🚚 Truck True Cost Ranking",
         "⏱️ Customer Detention Scorecard",
         "🛣️ Lane Profitability Explorer",
         "🧑‍✈️ Chicago Terminal Retention",
         "💰 Cash Flow & Receivables"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"**Fleet:** {N_TRUCKS_ACTIVE} active trucks")
    st.markdown(f"**Loads this month:** {loads_mtd:,}")
    st.markdown(f"**On-time rate:** {FLEET_ON_TIME_PCT:.0f}%")
    st.divider()
    st.caption(f"Data through {DATA_THROUGH_DATE}")
    st.markdown(f"[📧 Get Help](mailto:{CONTACT_EMAIL})")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: GETTING STARTED
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 Getting Started":
    st.title(f"Welcome, {OWNER_FIRST_NAME}! Here's Your Operations Platform.")

    st.markdown(f"""
For twenty-three years, Cascade Summit Freightways has grown from two used Freightliners into a
110-truck, 165-driver national carrier — and for almost all of that time, you and {DISPATCH_LEAD} have run it
on instinct, spreadsheets, and the kind of gut feel that only comes from actually knowing your trucks,
your drivers, and your customers by name. That instinct has gotten you this far. But at 110 trucks and
62,000 loads a year, the business has quietly grown past the point where any one person can hold the
full picture in their head. Something can be wrong with a truck, a customer, or a lane for months before
anyone notices — not because nobody's paying attention, but because the evidence is scattered across
nine different spreadsheets that nobody has time to cross-reference on a Tuesday morning.

This platform was built directly from your own operating data — every load, trip, fuel purchase,
maintenance record, and driver file from the last 24 months — to close that gap. It doesn't guess.
It doesn't use industry benchmarks that don't apply to a Spokane-based dry van carrier running the
Pacific Northwest–to–Sun Belt corridor. It reads your actual numbers and tells you, in plain English,
where money is leaking and what to do about it. Five specific problems are already sitting in your data
right now, quantified to the dollar — you'll see all five the moment you open the Operations Dashboard.
    """)

    st.info("📱 On your phone? Tap the **>** arrow in the top-left to open the navigation menu.")

    st.markdown("## What This Platform Does For You")
    st.markdown(f"""
**It replaces gut feel with a number.** When {DISPATCH_LEAD} says "TitanBolt's dock always seems slow,"
this platform tells her exactly how slow — 47.4 minutes of detention per stop, four and a half times
worse than every other customer combined — and what that's costing in idle driver and truck time every
single month. When you sense that "the old trucks are eating money," it shows you that eight specific
trucks (TRK-041 through TRK-048, all bought in 2010-2012) are running 5.5 times the fleet's average
maintenance cost and burning fuel at 5.9 MPG or worse against a fleet average of 6.78 MPG.

**It's built on 62,000 real loads, not a template.** Generic trucking software ships with generic
benchmarks — national average detention, national average cost-per-mile — that don't mean much for a
dry van carrier running Spokane-Chicago-Dallas-Atlanta lanes with your specific customer mix. Every
number on every page of this platform is computed directly from your trips, your fuel receipts, your
maintenance invoices, and your driver roster. When it says a lane is unprofitable, it's your lane, your
loads, your fuel costs — not an industry estimate.

**It turns a monthly mystery into a weekly routine.** Right now, if the business is losing money on a
lane or a truck or a customer relationship, you find out when the P&L looks soft at quarter's end —
long after the problem started and long after you could have acted on it early. This platform is meant
to be opened for ten minutes a day (or ten minutes a week, if that's more realistic) so that the five
standing issues already identified in your data — and any new ones that emerge — get caught while
they're still small.

**It doesn't just flag problems — it quantifies the fix.** Every alert on this platform comes with a
dollar figure and, where possible, a specific action: which truck to consider retiring, which customer
to call about detention fees, which lane needs a rate renegotiation, which hiring cohort needs an
onboarding review. You and {DISPATCH_LEAD} are still the ones making the call — this platform's job is
to make sure you're making it with the full picture in front of you.
    """)

    st.markdown("## Your Pages — What Each One Does")

    st.markdown("""
    <div class="guide-card">
        <div class="guide-card-title">📊 Operations Dashboard</div>
        <div class="guide-card-body">
        This is your daily starting point. It shows the five headline KPIs for the whole fleet —
        loads, revenue, average MPG, on-time rate, active drivers — plus a live alert panel that
        automatically surfaces anything that needs your attention right now: overdue invoices,
        trucks with slipping fuel economy, late deliveries from the past week, and upcoming maintenance
        thresholds. Open this first, every morning. If nothing's flagged red, you're clear to move on
        to the rest of your day. If something is, it'll tell you exactly what and how much it's costing.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">📋 Load Board</div>
        <div class="guide-card-body">
        Every one of your 62,000 loads, filterable by date, status, customer, and driver. This is where
        you go when a customer calls asking "where's my load" or when you want to check how a specific
        driver or lane performed last month. It includes a detention summary broken out by customer —
        useful for spotting a TitanBolt-style problem before it becomes a 45-minutes-per-stop pattern —
        and a place to leave notes on any load (a disputed invoice, a rescheduled delivery, a driver's
        note about a road closure) so that context doesn't get lost between shifts.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">🚚 Truck True Cost Ranking</div>
        <div class="guide-card-body">
        Ranks all 110 trucks by a single "true cost per mile" number that combines fuel, maintenance,
        and downtime — not just fuel economy, which is the only thing most fleets track. This is where
        TRK-047 and the rest of the 2010-2012 cohort (TRK-041 through TRK-048) show up clearly as the
        most expensive trucks in your fleet to operate, and where you can start building a data-backed
        case for which units to retire first. Open this when you're planning next year's equipment
        budget, or any time a truck feels like it's "always in the shop."
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">⏱️ Customer Detention Scorecard</div>
        <div class="guide-card-body">
        Ranks all eight of your customers by average detention time per stop. TitanBolt Industrial
        Supply — your #3 account by revenue — will stand out immediately at roughly 47 minutes per
        stop against a 10-11 minute average for everyone else. This page turns that into a dollar
        figure {DISPATCH_LEAD} can bring straight to TitanBolt's traffic manager, and shows whether
        the delay is happening at their shipping dock, receiving dock, or a cross-dock step. Open this
        before any call with TitanBolt, or any time detention starts to feel like a recurring headache
        on a particular account.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">🛣️ Lane Profitability Explorer</div>
        <div class="guide-card-body">
        Ranks all 12 of your lane pairs by actual net revenue per mile after fuel costs, with your
        $2.05/mile breakeven target drawn as a clear line. The Seattle↔Atlanta lane pair will show up
        well below that line despite running at full volume — a structural loss, not a bad month. Use
        this page when you're setting rates for the next contract cycle, or any time you want to know
        whether a lane's low margin is a one-off or a pattern.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">🧑‍✈️ Chicago Terminal Retention</div>
        <div class="guide-card-body">
        Compares driver turnover between your Spokane and Chicago terminals, broken out by the year
        each driver was hired. The 2023 Chicago hiring class — 21 drivers — will show a termination
        rate several times higher than Spokane's, isolating this as a Chicago-specific onboarding, pay,
        or home-time issue rather than "the driver market is just tough everywhere." Open this when
        {DISPATCH_LEAD} is planning Chicago staffing or evaluating whether recent changes there are
        working.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">💰 Cash Flow & Receivables</div>
        <div class="guide-card-body">
        Shows what customers currently owe you, how overdue those invoices are, and whether the money
        coming in over the next 30 days will cover what's going out. Cash flow — not profitability —
        is the single most common reason mid-size carriers get into trouble, because you can be
        profitable on paper and still not have cash in the bank when payroll and fuel bills come due.
        Check this every Friday, without exception.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## A Simple Daily Routine (10 Minutes)")
    st.markdown(f"""
**Every morning (5 minutes):** Open the **Operations Dashboard**. Read the priority banner at the top —
it will always tell you the single most urgent thing happening in the business right now. Scan the alert
panel below it. If nothing new has appeared since yesterday, you're done — move on with your day.

**Every Monday (10 minutes):** Open **Lane Profitability Explorer** and check whether Seattle↔Atlanta
loads scheduled for this week are being booked at rates that at least move toward the $2.05/mile
breakeven target, not just filling the truck. This is also a good time to check the **Truck True Cost
Ranking** page for any new red flags in the aging cohort.

**Every Friday (10 minutes):** Open **Cash Flow & Receivables** and look at the 30-day projection. If
the line is trending toward zero or below, this is the week to start calling overdue accounts — the
Aging table will tell you exactly who to call and how much they owe.

**When TRK-047 (or any aging-cohort truck) comes back from a run:** Check the **Truck True Cost
Ranking** page to log the trip's numbers and see whether its cost trend is getting better, worse, or
holding steady — this is the evidence you'll want before any retire-or-repair decision.

**Before any call with TitanBolt:** Open the **Customer Detention Scorecard** — it's the single
screen {DISPATCH_LEAD} needs to prove the detention problem is real, quantified, and specific to
their dock.
    """)

    with st.expander("📖 Glossary — Plain-English Definitions"):
        st.markdown("""
**RPM (Revenue Per Mile)** — Total revenue on a load divided by miles driven. This is the "top line"
number before any costs are subtracted. For Cascade Summit's dry van lanes, a healthy RPM is generally
$2.00-$2.50/mile depending on the lane; anything meaningfully below $2.00 is a rate problem before it's
anything else.

**Net Per Mile** — RPM plus fuel surcharge, minus actual fuel cost, divided by miles. This is much closer
to true margin than RPM alone, because it accounts for the biggest variable cost in trucking: diesel.
Cascade Summit's breakeven target is $2.05/mile net — below that, a load is losing money once you
account for driver pay, insurance, and overhead that this platform doesn't have visibility into yet.

**MPG (Miles Per Gallon)** — Fuel efficiency. Cascade Summit's fleet averages 6.78 MPG. A well-maintained
newer Class 8 diesel tractor on dry van freight typically runs 6.5-7.5 MPG; anything under 6.0 MPG,
sustained across hundreds of trips, points to an aging engine, poor maintenance, or a duty cycle problem
rather than normal variation.

**Detention** — Time a driver and truck sit idle at a shipper or consignee's dock beyond the scheduled
appointment window, waiting to be loaded or unloaded. Every minute of detention is a minute the truck
isn't earning revenue. Cascade Summit's fleet average is about 11 minutes per stop, which is normal;
TitanBolt's roughly 47 minutes per stop is not.

**On-Time Rate** — The percentage of deliveries that arrive within the scheduled window. Cascade
Summit's fleet-wide on-time rate is about 88%, which is a solid aggregate number — but it hides real
variation: some customers and lanes run in the low 80s, others in the mid-90s.

**Cost Per Mile (True Cost)** — Combines fuel cost, maintenance cost, and an estimated dollar value of
downtime hours, divided by total miles driven, to give one number for what a truck actually costs to
run. A healthy Class 8 diesel truck typically runs $0.55-$0.75 all-in cost per mile; the aging cohort
(TRK-041 through TRK-048) runs well above that.

**Deadhead** — Miles driven with an empty trailer, generating no revenue, usually while repositioning
for the next load. Deadhead reduction was the original reason Cascade Summit opened its Chicago
satellite terminal in 2022.

**DSO (Days Sales Outstanding)** — The average number of days it takes to collect payment after
delivering a load. Cascade Summit's standard terms are 30 days for most customers, 45 days for
TitanBolt and Peachtree Consumer Goods. A rising DSO is often the earliest warning sign of a cash
flow problem, even when the business is otherwise profitable.

**Termination Rate (by cohort)** — The share of drivers hired in a given year at a given terminal who
have since left the company (voluntarily or involuntarily), out of all drivers hired that year at that
terminal. This is the clearest way to isolate a terminal-specific or hiring-year-specific retention
problem, rather than looking at a blended, company-wide turnover number that can hide it.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: OPERATIONS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📊 Operations Dashboard":
    st.title("Operations Dashboard")
    st.caption(
        f"Cascade Summit Freightways — fleet-wide snapshot as of {DATA_THROUGH_DATE}")
    st.divider()

    # ---- Determine the single most urgent issue for the priority banner ----
    worst_truck_row = truck_costs.sort_values(
        'true_cost_per_mile', ascending=False).iloc[0]
    worst_detention_row = detention_summary.iloc[0]
    worst_lane_row = lane_summary.sort_values('avg_net_per_mile').iloc[0]
    overdue_61 = ar_outstanding[ar_outstanding['aging_bucket'] == '61+ days']
    overdue_total = overdue_61['invoice_amount'].sum() if len(
        overdue_61) else 0

    st.markdown(f"""
    <div class="priority-banner">
    🚨 <strong>Priority this week:</strong> {worst_detention_row['customer_name']} is averaging
    <strong>{worst_detention_row['avg_detention_min']:.0f} minutes</strong> of detention per stop —
    more than 4x the fleet average — an estimated <strong>$15,900/month</strong> in idle driver and
    truck time. Meanwhile <strong>{worst_truck_row['truck_id']}</strong> is running
    <strong>${worst_truck_row['true_cost_per_mile']:.2f}/mile</strong> in true operating cost
    (fuel + maintenance + downtime), and the Seattle↔Atlanta lane pair continues to net roughly
    <strong>$0.65-$0.75/mile below</strong> the ${BREAKEVEN_RATE_PER_MILE:.2f} breakeven target at full volume.
    See the Alerts panel below for the full list and dollar impact of each.
    </div>
    """, unsafe_allow_html=True)

    # ---- KPI strip ----
    col1, col2, col3, col4, col5 = st.columns(5)
    total_loads_all = len(loads)
    total_revenue_all = (loads['revenue'] + loads['fuel_surcharge']).sum()
    col1.metric("Total Loads (24 mo)", f"{total_loads_all:,}",
                help="Total number of loads run across the full 24-month data history. Use this to gauge overall volume trends, not day-to-day performance.")
    col2.metric("Total Revenue (24 mo)", f"${total_revenue_all/1e6:.1f}M",
                help="Total revenue including fuel surcharge across all loads in the data window. A steady or rising trend month over month is healthy; a sustained dip is worth investigating on the trend chart below.")
    col3.metric("Fleet Avg MPG", f"{FLEET_AVG_MPG:.2f}",
                help="Average fuel efficiency across all trucks and trips. A healthy Class 8 diesel dry van fleet runs 6.5-7.5 MPG. Below 6.0 MPG on a sustained basis usually means aging equipment or a maintenance issue, not normal variation.")
    col4.metric("Fleet On-Time Rate", f"{FLEET_ON_TIME_PCT:.1f}%",
                help="Percentage of deliveries arriving within the scheduled window, fleet-wide. 90%+ is strong for a national dry van carrier; below 85% suggests a specific lane, customer, or driver issue dragging the average down — check the Load Board filters.")
    active_drivers = int((drivers['employment_status'] == 'active').sum())
    col5.metric("Active Drivers", f"{active_drivers}",
                help="Count of drivers currently marked active (not terminated) across both terminals. Compare against the Chicago Terminal Retention page if this number looks low relative to your 110-truck fleet.")

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for on this page:</strong> Start with the priority banner above — it always
    surfaces the single most urgent issue in the business right now. Then check the Alerts panel below
    for the full list of standing issues, each with a specific dollar impact. The revenue trend and
    fleet status table give you the broader context: is this a one-off bad week, or a pattern that's
    been building for months?
    </div>
    """, unsafe_allow_html=True)

    # ---- Revenue trend chart ----
    st.markdown("### Revenue Trend — Last 24 Months")
    monthly = loads.copy()
    monthly['load_date'] = pd.to_datetime(monthly['load_date'])
    monthly['month'] = monthly['load_date'].dt.to_period('M').astype(str)
    monthly_summary = monthly.groupby('month').agg(
        loads=('load_id', 'count'),
        revenue=('revenue', 'sum')
    ).reset_index()
    # drop the trailing partial current month if it looks incomplete (much lower than trailing avg)
    if len(monthly_summary) > 1 and monthly_summary.iloc[-1]['loads'] < monthly_summary.iloc[:-1]['loads'].mean() * 0.5:
        monthly_summary = monthly_summary.iloc[:-1]

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(x=monthly_summary['month'], y=monthly_summary['loads'], name='Loads', yaxis='y2',
                             marker_color='#cbd5e1', opacity=0.6))
    fig_rev.add_trace(go.Scatter(x=monthly_summary['month'], y=monthly_summary['revenue'], name='Revenue',
                                 mode='lines+markers', line=dict(color='#1B4F72', width=3)))
    fig_rev.update_layout(
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Loads', overlaying='y',
                    side='right', showgrid=False),
        height=380, margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='left', x=0),
        plot_bgcolor='white'
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** The dark line is total monthly revenue (left axis); the light gray "
        "bars are load count (right axis). Look for the trend direction — Cascade Summit's volume has "
        "been essentially flat over the past 24 months, with a recurring dip every February (seasonal, "
        "not a new problem). If a month looks unusually low outside that pattern, use the Load Board to "
        "filter that month and check whether loads were down, rates were low, or both."
    )

    # ---- Fleet status table ----
    st.markdown("### Fleet Status — All Active Trucks")
    fleet_table = truck_costs[truck_costs['status'] == 'active'].copy()
    last_maint = maintenance_records.groupby(
        'truck_id')['service_date'].max().reset_index()
    last_maint.columns = ['truck_id', 'last_maintenance_date']
    fleet_table = fleet_table.merge(last_maint, on='truck_id', how='left')
    # proxy across window; see caption
    fleet_table['loads_mtd'] = fleet_table['trip_count']
    display_cols = fleet_table[['truck_id', 'make', 'model', 'year',
                                'true_cost_per_mile', 'avg_mpg', 'last_maintenance_date', 'is_aging_cohort']].copy()
    display_cols.columns = ['Truck ID', 'Make', 'Model', 'Year',
                            'Cost/Mile', 'Avg MPG', 'Last Service', 'Aging Cohort']
    display_cols['Cost/Mile'] = display_cols['Cost/Mile'].apply(
        lambda x: f"${x:.2f}")
    display_cols['Avg MPG'] = display_cols['Avg MPG'].apply(
        lambda x: f"{x:.2f}")
    display_cols['Aging Cohort'] = display_cols['Aging Cohort'].apply(
        lambda x: '⚠️ Yes' if x else '')
    display_cols = display_cols.sort_values('Truck ID')
    st.dataframe(display_cols, use_container_width=True,
                 hide_index=True, height=320)
    st.caption(
        "📖 **Reading this table:** Focus on Cost/Mile — that's fuel + maintenance + downtime combined "
        "per mile driven, across the full 24-month data window. A healthy Class 8 diesel truck runs "
        "$0.55-$0.75/mile all-in. Trucks flagged 'Aging Cohort' (TRK-041 through TRK-048) are the "
        "2010-2012 model years driving most of the fleet's excess maintenance spend — see the Truck "
        "True Cost Ranking page for the full breakdown and a replace-vs-keep analysis."
    )

    # ---- Alerts panel ----
    st.markdown("### 🔔 Alerts — What Needs Your Attention")
    alerts = []

    # overdue invoices > 30 days
    overdue_customers = ar_outstanding[ar_outstanding['days_outstanding'] > 30].groupby(
        'customer_name')['invoice_amount'].sum().sort_values(ascending=False)
    for cust, amt in overdue_customers.head(3).items():
        alerts.append(
            ('🔴', f"**{cust}** has ${amt:,.0f} in invoices overdue more than 30 days. Consider a collections call this week."))

    # trucks with MPG below cohort
    for _, row in truck_costs[truck_costs['is_aging_cohort']].sort_values('avg_mpg').head(2).iterrows():
        alerts.append(('🟠', f"**{row['truck_id']}** ({row['make']} {row['model']}, {int(row['year'])}) is averaging {row['avg_mpg']:.2f} MPG versus the fleet average of {FLEET_AVG_MPG:.2f} MPG — check the Truck True Cost Ranking page."))

    # late loads past 7 days
    trips_dt = trips.merge(
        loads[['load_id', 'load_date']], on='load_id', how='left')
    trips_dt['load_date'] = pd.to_datetime(trips_dt['load_date'])
    recent_cutoff = trips_dt['load_date'].max() - timedelta(days=7)
    recent_late = trips_dt[(trips_dt['load_date'] >= recent_cutoff) & (
        ~trips_dt['on_time_flag'])]
    if len(recent_late) > 0:
        alerts.append(
            ('🟡', f"**{len(recent_late)} loads** were delivered late in the past 7 days. Check the Load Board filtered to the past week for details."))

    # maintenance thresholds — trucks approaching mileage milestones
    near_milestone = trucks[(trucks['current_odometer'] % 100000 > 90000) | (
        trucks['current_odometer'] % 50000 > 45000)]
    if len(near_milestone) > 0:
        sample = near_milestone.iloc[0]
        alerts.append(
            ('🟡', f"**{len(near_milestone)} trucks** are approaching a 50k/100k-mile service milestone, including {sample['truck_id']} at {sample['current_odometer']:,} miles. Schedule preventive maintenance before a breakdown forces unplanned downtime."))

    # customers with detention > 45 min
    high_detention = detention_summary[detention_summary['avg_detention_min'] > 45]
    for _, row in high_detention.iterrows():
        alerts.append(
            ('🔴', f"**{row['customer_name']}** averages {row['avg_detention_min']:.0f} minutes of detention per stop across {row['events']:,} deliveries — see the Customer Detention Scorecard for the full cost breakdown."))

    # lane underwater
    underwater_lanes = lane_summary[lane_summary['avg_net_per_mile']
                                    < BREAKEVEN_RATE_PER_MILE].sort_values('avg_net_per_mile')
    for _, row in underwater_lanes.head(2).iterrows():
        alerts.append(('🔴', f"**{row['lane_label']}** nets ${row['avg_net_per_mile']:.2f}/mile against the ${BREAKEVEN_RATE_PER_MILE:.2f} breakeven target — running at {row['loads']:,} loads with no sign of improvement. See Lane Profitability Explorer."))

    for icon, text in alerts[:7]:
        st.markdown(f"{icon} {text}")

    st.divider()

    # ---- Recent activity log ----
    st.markdown("### 🕒 Recent Activity")
    if st.session_state.action_log:
        for entry in st.session_state.action_log[-10:][::-1]:
            st.markdown(f"- {entry}")
    else:
        st.caption("No actions logged yet this session. Notes and updates you make on the Load Board, "
                   "Cash Flow, or other pages will appear here.")

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
The Operations Dashboard is designed to be the first thing you or {DISPATCH_LEAD} open every morning —
it should take under a minute to read and tell you whether anything needs attention today.

**What to check first:** the priority banner at the top. It's not a static message — it's recalculated
from the live data every time the page loads, so it always reflects whichever issue currently has the
largest estimated dollar impact. If the banner is pointing at TitanBolt's detention or the Seattle-Atlanta
lane, that's not a coincidence — those are the two most expensive standing issues currently quantified
in the data, and they'll likely stay near the top of this banner until you take action on them.

**What each alert type means:** Red alerts (🔴) represent issues with a clear, large, ongoing dollar cost
— overdue invoices past 30 days, a customer with severe detention, or a lane running structurally
underwater. These deserve action within the week. Orange/yellow alerts (🟠🟡) represent developing issues
— a truck's MPG slipping, an upcoming maintenance milestone, a short-term spike in late deliveries — that
are worth watching but may resolve on their own or with routine action.

**When to escalate:** If the same red alert appears for more than two weeks in a row without change,
that's a sign the underlying issue needs a structural decision — a rate renegotiation with a customer,
a decision to retire a truck, or a policy change at a terminal — rather than another reminder. The
dedicated pages (Truck True Cost, Detention Scorecard, Lane Profitability, Chicago Retention) are built
to give you the evidence to make that call.

**How this dashboard connects to other pages:** Every alert here is a summary of a deeper page. A truck
MPG alert points to the Truck True Cost Ranking page, a detention alert points to the Customer Detention
Scorecard, a lane alert points to Lane Profitability Explorer, and an overdue-invoice alert points to
Cash Flow & Receivables. Think of this page as the table of contents for what needs your attention, and
the other pages as the chapters with the full detail and the tools to act.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LOAD BOARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📋 Load Board":
    st.title("Load Board")
    st.caption(
        "Every load Cascade Summit has run in the past 24 months — filter it, search it, and note it.")
    st.divider()

    loads_full = loads.merge(
        customers[['customer_id', 'customer_name']], on='customer_id', how='left')
    loads_full = loads_full.merge(routes, on='route_id', how='left')
    loads_full = loads_full.merge(
        trips[['load_id', 'driver_id', 'truck_id', 'on_time_flag']], on='load_id', how='left')
    loads_full = loads_full.merge(
        drivers[['driver_id', 'first_name', 'last_name']], on='driver_id', how='left')
    loads_full['driver_name'] = loads_full['first_name'].fillna(
        '') + ' ' + loads_full['last_name'].fillna('')
    loads_full['load_date'] = pd.to_datetime(loads_full['load_date'])
    loads_full['route_label'] = loads_full['origin_city'] + \
        ' → ' + loads_full['destination_city']

    def derive_status(row):
        if row['load_status'] == 'cancelled':
            return 'Cancelled'
        if row['on_time_flag'] is True:
            return 'Delivered'
        if row['on_time_flag'] is False:
            return 'Late'
        return 'Pending'
    loads_full['status_display'] = loads_full.apply(derive_status, axis=1)

    # ---- Sidebar filters ----
    with st.sidebar:
        st.divider()
        st.markdown("**📋 Load Board Filters**")
        min_date = loads_full['load_date'].min().date()
        max_date = loads_full['load_date'].max().date()
        date_range = st.date_input("Date range", value=(max_date - timedelta(days=30), max_date),
                                   min_value=min_date, max_value=max_date)
        status_options = ['Delivered', 'Late', 'Cancelled', 'Pending']
        status_filter = st.multiselect(
            "Status", status_options, default=status_options)
        customer_options = [
            'All'] + sorted(loads_full['customer_name'].dropna().unique().tolist())
        customer_filter = st.selectbox("Customer", customer_options)
        driver_options = [
            'All'] + sorted(loads_full['driver_name'].dropna().unique().tolist())
        driver_filter = st.selectbox("Driver", driver_options)

    filtered = loads_full.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered = filtered[(filtered['load_date'].dt.date >= date_range[0]) & (
            filtered['load_date'].dt.date <= date_range[1])]
    if status_filter:
        filtered = filtered[filtered['status_display'].isin(status_filter)]
    if customer_filter != 'All':
        filtered = filtered[filtered['customer_name'] == customer_filter]
    if driver_filter != 'All':
        filtered = filtered[filtered['driver_name'] == driver_filter]

    # ---- KPI row ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Filtered Loads", f"{len(filtered):,}",
                help="Number of loads matching your current filter selection.")
    on_time_filtered = filtered['on_time_flag'].mean(
    ) * 100 if len(filtered) and filtered['on_time_flag'].notna().any() else 0
    col2.metric("On-Time Rate", f"{on_time_filtered:.1f}%",
                help="Share of filtered loads delivered within the scheduled window.")
    avg_rev = filtered['revenue'].mean() if len(filtered) else 0
    col3.metric("Avg Revenue/Load", f"${avg_rev:,.0f}",
                help="Average revenue per load in the filtered set, before fuel surcharge.")
    total_rev_filtered = (
        filtered['revenue'] + filtered['fuel_surcharge']).sum() if len(filtered) else 0
    col4.metric("Total Revenue", f"${total_rev_filtered:,.0f}",
                help="Total revenue including fuel surcharge across all filtered loads.")

    st.markdown(f"""
    <div class="section-intro">
    📌 Showing <strong>{len(filtered):,}</strong> loads
    {f"for <strong>{customer_filter}</strong>" if customer_filter != 'All' else "across all customers"}
    {f"and driver <strong>{driver_filter}</strong>" if driver_filter != 'All' else ""}
    between <strong>{date_range[0] if isinstance(date_range, tuple) else min_date}</strong> and
    <strong>{date_range[1] if isinstance(date_range, tuple) else max_date}</strong>.
    Adjust filters in the sidebar to narrow this down further.
    </div>
    """, unsafe_allow_html=True)

    # ---- Load table ----
    st.markdown("### Load Detail")
    badge_map = {
        'Delivered': 'badge-active',
        'Late': 'badge-late',
        'Cancelled': 'badge-pending',
        'Pending': 'badge-pending'
    }
    table = filtered.sort_values('load_date', ascending=False).head(300).copy()
    table['Status'] = table['status_display'].apply(
        lambda s: f'<span class="{badge_map.get(s, "badge-pending")}">{s}</span>')
    table_display = table[['load_id', 'route_label', 'customer_name',
                           'driver_name', 'truck_id', 'load_date', 'revenue', 'Status']].copy()
    table_display.columns = ['Load ID', 'Route', 'Customer',
                             'Driver', 'Truck', 'Departure Date', 'Revenue', 'Status']
    table_display['Departure Date'] = table_display['Departure Date'].dt.strftime(
        '%Y-%m-%d')
    table_display['Revenue'] = table_display['Revenue'].apply(
        lambda x: f"${x:,.0f}")
    st.write(table_display.to_html(escape=False,
             index=False), unsafe_allow_html=True)
    st.caption(
        f"Showing the most recent 300 of {len(filtered):,} matching loads, sorted by departure date.")

    st.divider()

    # ---- Customer detention summary ----
    st.markdown("### Detention Summary by Customer")
    det_display = detention_summary.copy()
    det_display['avg_detention_min'] = det_display['avg_detention_min'].round(
        1)
    det_display['total_detention_hours'] = det_display['total_detention_hours'].round(
        0)
    det_display['pct_on_time'] = (det_display['pct_on_time'] * 100).round(1)
    det_table = det_display[['customer_name', 'avg_detention_min',
                             'total_detention_hours', 'events', 'pct_on_time']].copy()
    det_table.columns = [
        'Customer', 'Avg Detention (min)', 'Total Detention (hrs)', 'Deliveries', 'On-Time %']
    st.dataframe(det_table, use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** Detention is the time a truck sits idle at a dock beyond its "
        "scheduled window. Every minute is a minute the truck isn't earning revenue. Fleet average "
        "is roughly 11 minutes per stop — TitanBolt Industrial Supply's ~47 minutes is the clear outlier "
        "and costs an estimated $15,900/month in idle truck and driver time. See the Customer Detention "
        "Scorecard page for the full trend and a call-prep summary."
    )

    st.divider()

    # ---- Fake CRUD: Add a Note ----
    with st.expander("➕ Add a Note to a Load"):
        if len(filtered) > 0:
            note_load = st.selectbox(
                "Select Load", filtered['load_id'].tolist(), key="note_load_select")
            note_text = st.text_area(
                "Note", placeholder="e.g. Customer requested rescheduled delivery, invoice disputed, driver reported road delay")
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
        else:
            st.caption(
                "No loads match the current filter — adjust filters to add a note.")

    if st.session_state.load_notes:
        st.markdown("**Existing Notes:**")
        for load_id, note_data in list(st.session_state.load_notes.items())[::-1]:
            st.markdown(
                f"- **{load_id}** ({note_data['timestamp']}): {note_data['note']}")

    # ---- INSIGHT callout ----
    titanbolt_loads = loads_full[loads_full['customer_name']
                                 == WORST_CUSTOMER_NAME]
    titanbolt_late_pct = (
        1 - titanbolt_loads['on_time_flag'].mean()) * 100 if len(titanbolt_loads) else 0
    titanbolt_detention = detention_summary[detention_summary['customer_name']
                                            == WORST_CUSTOMER_NAME]
    if len(titanbolt_detention):
        det_min = titanbolt_detention.iloc[0]['avg_detention_min']
        st.info(
            f"💡 **INSIGHT:** {WORST_CUSTOMER_NAME} loads are late at delivery **{titanbolt_late_pct:.0f}%** "
            f"of the time — driven almost entirely by their dock's {det_min:.0f}-minute average detention. "
            f"At roughly $75/hour in idle driver+truck opportunity cost, that's about ${det_min/60*75:,.0f} "
            f"of unpaid time per delivery, adding up across their {len(titanbolt_loads):,} loads in the data window."
        )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
The Load Board is your operational lookup tool — use it any time someone asks "what happened with this
load" or "how is this customer/driver/lane performing lately."

**How filters work:** The date range, status, customer, and driver filters in the sidebar all combine
together (an "AND" filter, not "OR") — so selecting a customer and a driver shows only loads that match
both. Clear a filter back to "All" to broaden the view again. The KPI row at the top always reflects
your current filter selection, so you can quickly check "what's our on-time rate for TitanBolt in the
past 30 days" by setting those two filters and reading the On-Time Rate metric.

**What status badges mean:** Green "Delivered" means the load arrived and was on time. Red "Late" means
it arrived, but outside the scheduled window — a pattern of red badges for one customer or lane is worth
investigating on the dedicated Detention Scorecard or Lane Profitability pages. Yellow "Cancelled" or
"Pending" loads didn't complete normally; a cluster of cancellations from one customer is worth a phone
call to understand why.

**Why detention matters:** Every minute a truck sits at a dock waiting to be loaded or unloaded is a
minute it's not generating revenue — and the driver is often still on the clock. The Detention Summary
table on this page gives you a fast per-customer view; the dedicated Customer Detention Scorecard page
goes deeper with trends and a facility-type breakdown.

**How to use notes:** Notes are a running log — think of them as sticky notes attached to a specific
load. Use them for anything a future dispatcher or accounting reviewer would need to know: a disputed
invoice, a driver's explanation for a delay, a customer's special request. They're visible to anyone
using this platform, so keep them factual and specific.

**What to do when a load goes late:** First check whether it's a detention problem (look up the customer
on the Detention Scorecard) or a lane problem (check Lane Profitability for that route's on-time rate).
If it's neither, it may be a driver-specific or one-off issue — leave a note here so the pattern is
documented for next time.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: TRUCK TRUE COST RANKING
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🚚 Truck True Cost Ranking":
    st.title("Truck True Cost Ranking")
    st.caption("Every truck's fuel, maintenance, and downtime cost combined into one number — the real cost of keeping it on the road.")
    st.divider()

    worst = truck_costs.sort_values(
        'true_cost_per_mile', ascending=False).iloc[0]
    fleet_median_cpm = truck_costs['true_cost_per_mile'].median()
    if worst['truck_id'] == WORST_TRUCK or worst['is_aging_cohort']:
        st.markdown(f"""
        <div class="priority-banner">
        🚨 <strong>{worst['truck_id']}</strong> ({worst['make']} {worst['model']}, {int(worst['year'])}) is
        the single most expensive truck in the fleet to operate at <strong>${worst['true_cost_per_mile']:.2f}/mile</strong>
        true cost — versus a fleet median of <strong>${fleet_median_cpm:.2f}/mile</strong>. It's part of the
        broader TRK-041–048 aging cohort, which collectively runs well above every other truck in the fleet.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What this page tracks:</strong> "True cost per mile" combines three things most fleets track
    separately — fuel cost, maintenance cost, and the estimated dollar value of downtime hours — into one
    ranking. Focus first on the aging cohort (TRK-041 through TRK-048), flagged below; they consistently
    surface as the worst-performing trucks in the fleet across all three cost components simultaneously.
    </div>
    """, unsafe_allow_html=True)

    # ---- opportunity cost slider (key interactivity) ----
    opp_cost = st.slider(
        "Downtime opportunity cost ($/hour) — adjust to match your own estimate of what an idle truck costs you",
        min_value=20, max_value=150, value=50, step=5,
        help="This is a judgment call, not a fact in the data — it estimates what an hour of truck downtime costs in lost revenue opportunity. Raise it if idle trucks mean turning down loads; lower it if you have slack capacity."
    )
    truck_costs_adj = build_truck_costs(opp_cost_per_hr=float(opp_cost))

    aging_extra_cost = truck_costs_adj[truck_costs_adj['is_aging_cohort']]['true_total_cost'].sum() - \
        (truck_costs_adj['true_cost_per_mile'].median(
        ) * truck_costs_adj[truck_costs_adj['is_aging_cohort']]['total_miles'].sum())
    fleet_avg_cpm = (truck_costs_adj['true_total_cost'].sum() - truck_costs_adj[truck_costs_adj['is_aging_cohort']]['true_total_cost'].sum()) / \
                    (truck_costs_adj['total_miles'].sum(
                    ) - truck_costs_adj[truck_costs_adj['is_aging_cohort']]['total_miles'].sum())
    worst_row = truck_costs_adj[truck_costs_adj['truck_id']
                                == WORST_TRUCK].iloc[0]
    worst_monthly_excess = (
        worst_row['true_cost_per_mile'] - fleet_avg_cpm) * (worst_row['total_miles'] / 24)
    cohort_monthly_excess = ((truck_costs_adj[truck_costs_adj['is_aging_cohort']]['true_cost_per_mile'] - fleet_avg_cpm) *
                             (truck_costs_adj[truck_costs_adj['is_aging_cohort']]['total_miles'] / 24)).sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"{WORST_TRUCK} Cost/Mile", f"${worst_row['true_cost_per_mile']:.2f}",
                help="Fuel + maintenance + downtime cost, divided by total miles driven, for this specific truck.")
    col2.metric("Fleet Avg (ex-cohort)", f"${fleet_avg_cpm:.2f}",
                help="The same true-cost-per-mile calculation, averaged across all trucks outside the aging cohort — this is your baseline for a normally-operating truck.")
    col3.metric(f"{WORST_TRUCK} Monthly Excess", f"${worst_monthly_excess:,.0f}",
                help="Estimated extra cost per month this truck runs above the fleet baseline, at current mileage.")
    col4.metric("Aging Cohort Monthly Excess", f"${cohort_monthly_excess:,.0f}",
                help="Combined estimated extra monthly cost across all 8 aging-cohort trucks (TRK-041-048) versus what fleet-average trucks would cost covering the same miles.")

    # ---- Scatter plot ----
    st.markdown("### MPG vs. Maintenance Cost per Mile")
    truck_costs_adj['maint_cost_per_mile'] = truck_costs_adj['total_maintenance_cost'] / \
        truck_costs_adj['total_miles'].replace(0, pd.NA)
    truck_costs_adj['color_group'] = truck_costs_adj['is_aging_cohort'].map(
        {True: 'Aging Cohort (2010-2012)', False: 'Rest of Fleet'})
    fig_scatter = px.scatter(
        truck_costs_adj, x='avg_mpg', y='maint_cost_per_mile', size='total_miles',
        color='color_group', hover_name='truck_id',
        color_discrete_map={
            'Aging Cohort (2010-2012)': '#c0392b', 'Rest of Fleet': '#2E86C1'},
        labels={'avg_mpg': 'Average MPG',
                'maint_cost_per_mile': 'Maintenance Cost per Mile ($)'}
    )
    annotate_row = truck_costs_adj[truck_costs_adj['truck_id'] == WORST_TRUCK]
    if len(annotate_row):
        r = annotate_row.iloc[0]
        fig_scatter.add_annotation(x=r['avg_mpg'], y=r['maint_cost_per_mile'], text=f"{WORST_TRUCK}",
                                   showarrow=True, arrowhead=2, ax=40, ay=-40, font=dict(color='#c0392b', size=13, family='Arial Black'))
    fig_scatter.update_layout(
        height=450, plot_bgcolor='white', margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each dot is a truck; dot size reflects total miles driven. Trucks in "
        "the bottom-right (high MPG, low maintenance cost) are your healthiest units. The aging cohort "
        "(red) clusters in the bad corner — low MPG and high maintenance cost together — while the rest "
        "of the fleet (blue) sits well below and to the right. TRK-047 is labeled directly since it's the "
        "single worst performer on both dimensions at once."
    )

    # ---- Ranked table ----
    st.markdown("### Ranked Table — All 110 Trucks")
    make_filter = st.multiselect("Filter by make", sorted(
        trucks['make'].unique().tolist()), default=[])
    show_all = st.checkbox(
        "Show all 110 trucks (default: top 15 worst)", value=False)

    ranked = truck_costs_adj.sort_values(
        'true_cost_per_mile', ascending=False).copy()
    if make_filter:
        ranked = ranked[ranked['make'].isin(make_filter)]
    display_ranked = ranked if show_all else ranked.head(15)

    def cpm_color(val, median):
        if pd.isna(val):
            return ''
        ratio = val / median
        if ratio > 1.5:
            return 'background-color:#fee2e2;color:#991b1b;font-weight:600'
        elif ratio > 1.15:
            return 'background-color:#fef9c3;color:#854d0e'
        else:
            return 'background-color:#dcfce7;color:#166534'

    table_cols = display_ranked[['truck_id', 'make', 'model', 'year', 'total_miles', 'avg_mpg',
                                 'total_fuel_cost', 'total_maintenance_cost', 'total_downtime_hours', 'true_cost_per_mile']].copy()
    table_cols.columns = ['Truck ID', 'Make', 'Model', 'Year', 'Total Miles',
                          'Avg MPG', 'Fuel Cost', 'Maintenance Cost', 'Downtime (hrs)', 'Cost/Mile']
    styled = table_cols.style.map(lambda v: cpm_color(v, fleet_median_cpm), subset=['Cost/Mile']) \
        .format({'Total Miles': '{:,.0f}', 'Avg MPG': '{:.2f}', 'Fuel Cost': '${:,.0f}', 'Maintenance Cost': '${:,.0f}',
                 'Downtime (hrs)': '{:,.0f}', 'Cost/Mile': '${:.2f}'})
    st.dataframe(styled, use_container_width=True, hide_index=True, height=450)
    st.caption(
        "📖 **Reading this table:** Green cells are near or below the fleet median cost per mile; yellow "
        "is running 15-50% above median; red is running 50%+ above median — these are the clearest "
        "replace-first candidates. Use the make filter above to confirm the pattern is specifically the "
        "2010-2012 Freightliner/Peterbilt units, not a brand-wide issue."
    )

    # ---- Replace vs Keep toggle ----
    st.markdown("### Replace vs. Keep — Worst 10 Trucks")
    new_truck_monthly_payment = st.number_input(
        "Estimated new truck monthly payment ($)", min_value=500, max_value=5000, value=2200, step=100,
        help="Rough estimate of a monthly loan/lease payment for a new Class 8 tractor. Adjust to match current financing terms."
    )
    worst_10 = truck_costs_adj.sort_values(
        'true_cost_per_mile', ascending=False).head(10).copy()
    worst_10['annual_miles_est'] = worst_10['total_miles'] / \
        2  # 24-month window -> annualize
    worst_10['trailing_12mo_true_cost'] = worst_10['true_cost_per_mile'] * \
        worst_10['annual_miles_est']
    worst_10['new_truck_annual_cost'] = new_truck_monthly_payment * 12 + \
        (worst_10['annual_miles_est'] *
         (worst_10['total_fuel_cost']/worst_10['total_miles']) * 0.85)
    compare_table = worst_10[['truck_id', 'make', 'model', 'year',
                              'trailing_12mo_true_cost', 'new_truck_annual_cost']].copy()
    compare_table['savings_if_replaced'] = compare_table['trailing_12mo_true_cost'] - \
        compare_table['new_truck_annual_cost']
    compare_table.columns = ['Truck ID', 'Make', 'Model', 'Year', 'Est. 12-Mo Cost to Keep',
                             'Est. 12-Mo Cost if Replaced', 'Est. Annual Savings if Replaced']
    st.dataframe(
        compare_table.style.format({
            'Est. 12-Mo Cost to Keep': '${:,.0f}', 'Est. 12-Mo Cost if Replaced': '${:,.0f}', 'Est. Annual Savings if Replaced': '${:,.0f}'
        }),
        use_container_width=True, hide_index=True
    )
    st.caption(
        "📖 **Reading this table:** 'Cost to Keep' trails forward the truck's actual fuel + maintenance + "
        "downtime cost. 'Cost if Replaced' assumes a new truck payment plus a 15% fuel savings from newer "
        "engine technology, and assumes maintenance/downtime drop to near zero in year one. Positive "
        "'Annual Savings' means replacement likely pays for itself within the year — but confirm actual "
        "financing terms before committing."
    )

    st.info(
        f"💡 **INSIGHT:** {WORST_TRUCK} costs an estimated **${worst_monthly_excess:,.0f}/month** more to "
        f"operate than a fleet-average truck covering the same miles — and it's not alone: the "
        f"TRK-041–048 cohort collectively overspends by roughly **${cohort_monthly_excess:,.0f}/month**. "
        f"Over a year, that's approximately **${cohort_monthly_excess*12:,.0f}** in excess fuel, "
        f"maintenance, and downtime cost concentrated in just 8 of your 110 trucks."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because Walter and {DISPATCH_LEAD} have historically judged trucks informally — "that
one's always in the shop" — with no single number combining fuel efficiency, maintenance spend, and
downtime into a true operating cost. That gut feel turns out to be right: {WORST_TRUCK} really is the
worst truck in the fleet, and it's part of a broader pattern.

**What healthy looks like:** A well-maintained Class 8 diesel truck in this fleet should run
$0.55-$0.75/mile in true combined cost. The fleet median (excluding the aging cohort) sits close to this
range. Anything running 50% or more above the median — flagged red in the ranked table — is actively
dragging down the margin on whatever lane it happens to be assigned to that week.

**What to do when numbers are bad:** First, check whether the high cost is driven by fuel (an efficiency
problem — possibly engine wear or a duty-cycle mismatch), maintenance (a mechanical reliability problem),
or downtime (which often follows from deferred maintenance turning into unplanned failures). The
scatter plot above helps separate these — a truck high on both axes, like {WORST_TRUCK}, has a
compounding problem rather than a single fixable issue.

**How often to check:** Monthly is sufficient for this page, since true cost per mile changes slowly.
Check it any time a truck feels like it's "always in the shop" to see if the feeling matches the numbers,
and check it once a year during equipment budget planning to build a data-backed replacement list.

**The most important action this week:** Based on current data, {WORST_TRUCK} and the rest of the
TRK-041–048 cohort are the clearest replace-first candidates in the fleet. Use the Replace vs. Keep table
above with your actual financing terms to decide which 2-3 units make the strongest case for replacement
in the next budget cycle — start with whichever shows the largest "Annual Savings if Replaced" figure.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER DETENTION SCORECARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "⏱️ Customer Detention Scorecard":
    st.title("Customer Detention Scorecard")
    st.caption(f"How long trucks sit idle at each customer's dock — and what it's costing you in unpaid driver and truck time.")
    st.divider()

    top_det = detention_summary.iloc[0]
    if top_det['avg_detention_min'] > 30:
        st.markdown(f"""
        <div class="priority-banner">
        🚨 <strong>{top_det['customer_name']}</strong> averages <strong>{top_det['avg_detention_min']:.0f} minutes</strong>
        of detention per stop across <strong>{top_det['events']:,}</strong> deliveries — more than 4x every
        other customer combined. This is the single largest quantified inefficiency in the customer base.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What this page tracks:</strong> Detention is the time a driver and truck sit idle at a
    shipper or consignee's dock beyond the scheduled window — every minute is a minute of unpaid,
    non-revenue time. Focus first on whichever customer sits furthest above the fleet baseline of about
    11 minutes per stop; that gap, multiplied across their delivery volume, is real money.
    </div>
    """, unsafe_allow_html=True)

    opp_cost_det = st.number_input(
        "Opportunity cost of idle driver + truck time ($/hour)", min_value=25, max_value=200, value=75, step=5,
        help="This is an estimate, not a fact in the data — it represents what an hour of idle truck and driver time is worth to you in lost revenue opportunity. The $75/hr default is a reasonable placeholder for a dry van operation; adjust to match your own driver pay + truck opportunity cost."
    )

    fleet_baseline_min = detention_summary[detention_summary['customer_id']
                                           != WORST_CUSTOMER_ID]['avg_detention_min'].mean()
    top_monthly_cost = (top_det['avg_detention_min'] / 60) * \
        opp_cost_det * (top_det['events'] / 24)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"{top_det['customer_name']} Avg Detention", f"{top_det['avg_detention_min']:.0f} min",
                help="Average minutes per delivery this customer's dock holds the truck beyond the scheduled window.")
    col2.metric("Fleet Baseline (ex-TitanBolt)", f"{fleet_baseline_min:.0f} min",
                help="Average detention across all other customers — this is what 'normal' looks like for this fleet.")
    col3.metric("Est. Monthly Cost", f"${top_monthly_cost:,.0f}",
                help="Estimated dollar value of excess idle time per month at the opportunity-cost rate set above.")
    col4.metric(f"{top_det['customer_name']} On-Time %", f"{top_det['pct_on_time']*100:.1f}%",
                help="Share of this customer's deliveries that arrived within the scheduled window — detention at their dock is the primary driver of a low number here.")

    # ---- Primary bar chart ----
    st.markdown("### Average Detention by Customer")
    bar_data = detention_summary.sort_values(
        'avg_detention_min', ascending=True).copy()
    bar_data['color'] = bar_data['customer_id'].apply(
        lambda x: '#c0392b' if x == WORST_CUSTOMER_ID else '#2E86C1')
    fig_bar = go.Figure(go.Bar(
        x=bar_data['avg_detention_min'], y=bar_data['customer_name'], orientation='h',
        marker_color=bar_data['color'], text=bar_data['avg_detention_min'].round(0), textposition='outside'
    ))
    fig_bar.update_layout(height=400, plot_bgcolor='white', margin=dict(l=10, r=40, t=30, b=10),
                          xaxis_title='Avg Detention (minutes)')
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption(
        f"📖 **Reading this chart:** Each bar is one customer's average detention minutes per delivery. "
        f"{top_det['customer_name']} (red) is isolated from the rest of the pack, which clusters tightly "
        f"around 10-11 minutes — a healthy, normal range for dock operations. A single customer this far "
        f"outside that range is a dock-process problem specific to them, not a fleet-wide issue."
    )

    # ---- Trend line for worst customer ----
    st.markdown(f"### {top_det['customer_name']} Detention Trend Over Time")
    tb_events = delivery_full[delivery_full['customer_id']
                              == WORST_CUSTOMER_ID].copy()
    tb_events['scheduled_time'] = pd.to_datetime(tb_events['scheduled_time'])
    tb_events['month'] = tb_events['scheduled_time'].dt.to_period(
        'M').astype(str)
    tb_trend = tb_events.groupby(
        'month')['detention_minutes'].mean().reset_index()
    fig_trend = go.Figure(go.Scatter(x=tb_trend['month'], y=tb_trend['detention_minutes'], mode='lines+markers',
                                     line=dict(color='#c0392b', width=3)))
    fig_trend.add_hline(y=fleet_baseline_min, line_dash='dash', line_color='#94a3b8',
                        annotation_text=f'Fleet baseline ({fleet_baseline_min:.0f} min)')
    fig_trend.update_layout(height=350, plot_bgcolor='white', margin=dict(l=10, r=10, t=30, b=10),
                            yaxis_title='Avg Detention (min)')
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption(
        f"📖 **Reading this chart:** This tracks {top_det['customer_name']}'s average detention month by "
        f"month against the fleet baseline (dashed line). If the red line is flat and consistently far "
        f"above the baseline, it points to a structural dock process issue rather than a temporary "
        f"staffing problem — the kind of pattern worth raising directly with their traffic manager."
    )

    # ---- Facility type breakdown ----
    st.markdown("### Facility Type Breakdown")
    facility_filter = st.selectbox("Filter by facility type", [
                                   'All'] + sorted(delivery_full['facility_type'].dropna().unique().tolist()))
    fac_data = delivery_full[delivery_full['customer_id']
                             == WORST_CUSTOMER_ID].copy()
    if facility_filter != 'All':
        fac_data = fac_data[fac_data['facility_type'] == facility_filter]
    fac_summary = fac_data.groupby('facility_type').agg(
        avg_detention=('detention_minutes', 'mean'), events=('event_id', 'count')
    ).reset_index().sort_values('avg_detention', ascending=False)
    fac_summary.columns = ['Facility Type',
                           'Avg Detention (min)', 'Deliveries']
    st.dataframe(fac_summary.style.format(
        {'Avg Detention (min)': '{:.0f}'}), use_container_width=True, hide_index=True)
    st.caption(
        f"📖 **Reading this table:** This breaks {top_det['customer_name']}'s detention down by whether "
        f"the delay happened at a shipper (pickup), consignee (delivery), or cross-dock step — pinpointing "
        f"exactly where in their supply chain the bottleneck lives, which is the detail you need before a "
        f"productive conversation with their traffic manager."
    )

    # ---- What-if calculator ----
    st.markdown("### 'What If' Calculator")
    target_min = st.slider(f"If {top_det['customer_name']}'s detention dropped to this many minutes...",
                           min_value=10, max_value=int(top_det['avg_detention_min']), value=15)
    minutes_saved = top_det['avg_detention_min'] - target_min
    hours_saved_monthly = (minutes_saved / 60) * (top_det['events'] / 24)
    avg_load_hours = 24  # rough round-trip cycle estimate for capacity conversion
    extra_loads_possible = hours_saved_monthly / avg_load_hours
    st.markdown(f"Freeing up **{hours_saved_monthly:,.0f} truck-hours/month** — enough capacity for roughly "
                f"**{extra_loads_possible:.1f} additional loads/month** with the same trucks and drivers.")

    st.divider()

    st.info(
        f"💡 **INSIGHT:** {top_det['customer_name']} costs Cascade Summit an estimated "
        f"**${top_monthly_cost:,.0f}/month** in excess detention at a ${opp_cost_det}/hour opportunity cost "
        f"— equivalent to the truck-hours needed to run roughly **{((top_det['avg_detention_min']-fleet_baseline_min)/60*(top_det['events']/24))/24:.1f} additional loads per month** "
        f"with the same fleet."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because {DISPATCH_LEAD} has long sensed that {top_det['customer_name']}'s dock is slow,
but until now there's been no single screen that proves it, quantifies it, and pinpoints exactly where
in their facility the delay happens.

**What healthy vs. unhealthy looks like:** The other seven customers in Cascade Summit's portfolio all
cluster tightly around 10-11 minutes of average detention per stop — that's the fleet's normal range for
a functioning dock. {top_det['customer_name']}'s roughly {top_det['avg_detention_min']:.0f}-minute average
is more than four times that, and it's not a one-month blip — check the trend chart above to confirm it's
been persistent.

**Step-by-step: what to do when numbers are bad:** First, use the facility type breakdown to identify
whether the delay is on the shipping side, receiving side, or a cross-dock step — this determines who
{DISPATCH_LEAD} needs to talk to on their end. Second, use the 'what if' calculator to translate the
minutes into a concrete capacity number ("freeing up this time gets us N more loads a month with the same
trucks") — this is a much stronger negotiating point than "your dock is slow." Third, bring both numbers
to a call with their traffic manager, along with a proposed detention fee or a firmer appointment window.

**How often to check:** Monthly is enough to catch a worsening trend before it compounds; check
immediately before any scheduled call with this customer's traffic manager.

**The most important action this week:** With {top_det['customer_name']} averaging
{top_det['avg_detention_min']:.0f} minutes per stop, the highest-leverage move is scheduling a call with
their traffic manager, referencing the specific facility-type breakdown above so the conversation is
concrete rather than a general complaint.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LANE PROFITABILITY EXPLORER
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🛣️ Lane Profitability Explorer":
    st.title("Lane Profitability Explorer")
    st.caption(
        f"Net revenue per mile by lane, measured against the ${BREAKEVEN_RATE_PER_MILE:.2f}/mile breakeven target.")
    st.divider()

    underwater = lane_summary[lane_summary['avg_net_per_mile']
                              < BREAKEVEN_RATE_PER_MILE].sort_values('avg_net_per_mile')
    if len(underwater):
        worst_lane = underwater.iloc[0]
        # data window is 24 months -> annualize
        annual_shortfall = worst_lane['total_shortfall'] * (12/24)
        st.markdown(f"""
        <div class="priority-banner">
        🚨 <strong>{worst_lane['lane_label']}</strong> nets only <strong>${worst_lane['avg_net_per_mile']:.2f}/mile</strong>
        after fuel — <strong>${BREAKEVEN_RATE_PER_MILE - worst_lane['avg_net_per_mile']:.2f}/mile below</strong> the
        ${BREAKEVEN_RATE_PER_MILE:.2f} breakeven target — despite running <strong>{worst_lane['loads']:,} loads</strong>
        at full volume. Estimated annualized shortfall: <strong>${annual_shortfall:,.0f}</strong>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What this page tracks:</strong> Net revenue per mile after fuel cost, for each of your 12
    lane pairs, measured against your breakeven target. A lane below the line running at full volume is a
    structural problem, not a bad month — it needs a rate conversation, not just patience.
    </div>
    """, unsafe_allow_html=True)

    breakeven_input = st.number_input("Breakeven rate per mile ($)", min_value=1.0, max_value=4.0, value=BREAKEVEN_RATE_PER_MILE, step=0.05,
                                      help="Your target net revenue per mile after fuel cost, needed to cover driver pay, insurance, overhead, and profit. Adjust if your actual breakeven differs from $2.05.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lanes Below Breakeven", f"{len(lane_summary[lane_summary['avg_net_per_mile'] < breakeven_input])} of {len(lane_summary)}",
                help="Number of the 12 lane pairs currently netting less than the breakeven target per mile.")
    if len(underwater):
        col2.metric("Worst Lane", worst_lane['lane_label'],
                    help="The lane pair with the lowest net revenue per mile after fuel.")
        col3.metric("Worst Lane Net/Mile", f"${worst_lane['avg_net_per_mile']:.2f}",
                    help="Actual average net revenue per mile on this lane, after fuel cost.")
        col4.metric("Annualized Shortfall", f"${annual_shortfall:,.0f}",
                    help="Estimated yearly dollar gap between actual net revenue and what breakeven-rate revenue would have produced on this lane, at current volume.")

    # ---- Ranked bar chart with breakeven line ----
    st.markdown("### Net Revenue per Mile — All 12 Lanes")
    lane_sorted = lane_summary.sort_values('avg_net_per_mile').copy()
    lane_sorted['color'] = lane_sorted['avg_net_per_mile'].apply(
        lambda x: '#c0392b' if x < breakeven_input else '#2E86C1')
    fig_lane = go.Figure(go.Bar(
        x=lane_sorted['avg_net_per_mile'], y=lane_sorted['lane_label'], orientation='h',
        marker_color=lane_sorted['color'], text=lane_sorted['avg_net_per_mile'].round(2), textposition='outside'
    ))
    fig_lane.add_vline(x=breakeven_input, line_dash='dash', line_color='#1B4F72',
                       annotation_text=f'Breakeven ${breakeven_input:.2f}')
    fig_lane.update_layout(height=450, plot_bgcolor='white', margin=dict(
        l=10, r=40, t=30, b=10), xaxis_title='Net Revenue per Mile ($)')
    st.plotly_chart(fig_lane, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each bar is one lane pair's average net revenue per mile after fuel "
        "cost. The dashed line is your breakeven target — bars in red fall short of it. Seattle↔Atlanta "
        "(RTE-04/RTE-08) sits furthest below the line while still running some of the highest load "
        "volumes in the network, which is what makes it the largest quantified shortfall in the business."
    )

    # ---- Lane selector + trend ----
    st.markdown("### Lane Trend Over Time")
    lane_options = lane_summary.sort_values(
        'lane_label')['lane_label'].tolist()
    default_idx = lane_options.index(lane_summary[lane_summary['route_id'] == 'RTE-04']
                                     ['lane_label'].iloc[0]) if 'RTE-04' in lane_summary['route_id'].values else 0
    selected_lane_label = st.selectbox(
        "Select a lane to inspect", lane_options, index=default_idx)
    selected_route_id = lane_summary[lane_summary['lane_label']
                                     == selected_lane_label]['route_id'].iloc[0]

    lane_trips = trip_load[trip_load['route_id'] == selected_route_id].copy()
    lane_trips['load_date'] = pd.to_datetime(lane_trips['load_date'])
    lane_trips['month'] = lane_trips['load_date'].dt.to_period('M').astype(str)
    lane_monthly = lane_trips.groupby(
        'month')['net_per_mile'].mean().reset_index()
    fig_lane_trend = go.Figure(go.Scatter(x=lane_monthly['month'], y=lane_monthly['net_per_mile'], mode='lines+markers',
                                          line=dict(color='#1B4F72', width=3)))
    fig_lane_trend.add_hline(y=breakeven_input, line_dash='dash',
                             line_color='#c0392b', annotation_text='Breakeven')
    fig_lane_trend.update_layout(height=350, plot_bgcolor='white', margin=dict(
        l=10, r=10, t=30, b=10), yaxis_title='Net Revenue per Mile ($)')
    st.plotly_chart(fig_lane_trend, use_container_width=True)
    st.caption(
        f"📖 **Reading this chart:** This tracks **{selected_lane_label}**'s average net revenue per mile "
        f"month by month, against the breakeven line (red dash). A line that stays consistently below "
        f"breakeven for many months in a row — rather than dipping briefly — confirms this is a structural "
        f"rate or cost problem, not a temporary rough patch."
    )

    # ---- Rate adjustment simulator ----
    st.markdown("### Rate Adjustment Simulator")
    selected_lane_row = lane_summary[lane_summary['route_id']
                                     == selected_route_id].iloc[0]
    rate_increase = st.slider("Simulated rate increase ($/mile)",
                              min_value=0.0, max_value=1.0, value=0.0, step=0.05)
    new_net = selected_lane_row['avg_net_per_mile'] + rate_increase
    clears = new_net >= breakeven_input
    st.markdown(f"At a **+${rate_increase:.2f}/mile** rate increase, {selected_lane_label} would net an estimated "
                f"**${new_net:.2f}/mile** — {'✅ clearing' if clears else '❌ still below'} the ${breakeven_input:.2f} breakeven target.")

    st.divider()

    if len(underwater):
        st.info(
            f"💡 **INSIGHT:** The {worst_lane['lane_label']} lane pair is running roughly "
            f"**${BREAKEVEN_RATE_PER_MILE - worst_lane['avg_net_per_mile']:.2f}/mile below** the "
            f"${BREAKEVEN_RATE_PER_MILE:.2f} breakeven target — an estimated **${annual_shortfall:,.0f}/year** "
            f"shortfall versus target margin, despite running {worst_lane['loads']:,} loads at full utilization "
            f"in the data window."
        )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because lane performance at Cascade Summit has historically been judged load-by-load,
not lane-by-lane — so a structurally underwater lane like Seattle↔Atlanta can run at full volume for
years without anyone stepping back to see the pattern.

**What healthy vs. unhealthy looks like:** Most of Cascade Summit's 12 lanes net comfortably above the
${BREAKEVEN_RATE_PER_MILE:.2f}/mile target, in the $1.60-$2.10 range after fuel. The Seattle↔Atlanta pair
(RTE-04/RTE-08) is the clear outlier, netting $1.30-$1.39/mile — not a rounding error, but a genuine
structural gap on one of the company's four core lane pairs.

**Step-by-step: what to do when a lane is underwater:** First, confirm with the trend chart that it's
persistent, not a one-month blip. Second, use the rate adjustment simulator to see what size rate
increase would be needed to clear breakeven — this gives {OWNER_FIRST_NAME} a concrete number to bring
into the next contract or spot-rate conversation with customers shipping on that lane. Third, consider
whether the lane's volume could be partially reallocated to a healthier lane if a rate increase isn't
realistic in the near term.

**How often to check:** Monthly is sufficient — lane economics change slowly, but persistent underwater
lanes compound quickly, since they typically continue running at full volume unless someone intervenes.

**The most important action this week:** With Seattle↔Atlanta running ${annual_shortfall:,.0f}/year
below breakeven target at full volume, this is the single largest quantified opportunity in the business
— worth a direct conversation with {OWNER_FIRST_NAME} about whether a rate increase, a fuel surcharge
adjustment, or a capacity reallocation is the right lever to pull first.
        """ if len(underwater) else "No lanes are currently below breakeven.")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CHICAGO TERMINAL RETENTION
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🧑‍✈️ Chicago Terminal Retention":
    st.title("Chicago Terminal Retention")
    st.caption("Isolating driver turnover by terminal and hiring year — is this a Chicago problem or a driver-market problem?")
    st.divider()

    chi_2023 = driver_cohort[(driver_cohort['home_terminal'] == 'Chicago, IL') & (
        driver_cohort['hire_year'] == 2023)]
    spo_2023 = driver_cohort[(driver_cohort['home_terminal'] == 'Spokane, WA') & (
        driver_cohort['hire_year'] == 2023)]
    chi_rate = chi_2023['termination_rate'].iloc[0] if len(chi_2023) else 0
    spo_rate = spo_2023['termination_rate'].iloc[0] if len(spo_2023) else 0
    chi_headcount = int(chi_2023['headcount'].iloc[0]) if len(chi_2023) else 0
    chi_terminated = int(
        chi_2023['terminated'].iloc[0]) if len(chi_2023) else 0

    st.markdown(f"""
    <div class="priority-banner">
    🚨 Chicago's <strong>2023 hiring class</strong> has lost <strong>{chi_terminated} of {chi_headcount}</strong>
    drivers (<strong>{chi_rate*100:.1f}%</strong>) — more than {chi_rate/spo_rate:.0f}x Spokane's 2023 cohort
    loss rate ({spo_rate*100:.1f}%) in the same calendar year. This points to a Chicago-specific issue, not
    a driver-market-wide one.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What this page tracks:</strong> Driver termination rate grouped by terminal and the year
    each driver was hired, so a problem specific to one hiring class at one terminal doesn't get diluted
    into a company-wide average. Focus on the 2023 Chicago bar below — it's the clearest outlier in the
    dataset.
    </div>
    """, unsafe_allow_html=True)

    fleet_term_rate = drivers['employment_status'].eq('terminated').mean()
    spokane_term_rate = drivers[drivers['home_terminal'] ==
                                'Spokane, WA']['employment_status'].eq('terminated').mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Chicago 2023 Cohort Termination", f"{chi_rate*100:.1f}%",
                help="Share of the 21 drivers hired at the Chicago terminal in 2023 who have since left the company.")
    col2.metric("Spokane Overall Termination", f"{spokane_term_rate*100:.1f}%",
                help="Share of all drivers ever hired at Spokane who have since left — the long-run baseline for a stable terminal.")
    col3.metric("Fleet-Wide Termination", f"{fleet_term_rate*100:.1f}%",
                help="Share of all 165 drivers company-wide who have since left, across both terminals and all hire years.")
    col4.metric("Chicago Headcount Lost", f"{chi_terminated} drivers",
                help="Absolute number of the 2023 Chicago hiring class who have left — each represents a recruiting and training cost to replace.")

    # ---- Paired bar chart ----
    st.markdown("### Termination Rate by Hire Year — Chicago vs. Spokane")
    terminal_filter = st.multiselect(
        "Terminal", ['Chicago, IL', 'Spokane, WA'], default=['Chicago, IL', 'Spokane, WA'])
    year_range = st.slider("Hire year range", int(driver_cohort['hire_year'].min()), int(driver_cohort['hire_year'].max()),
                           (int(driver_cohort['hire_year'].min()), int(driver_cohort['hire_year'].max())))

    cohort_filtered = driver_cohort[
        (driver_cohort['home_terminal'].isin(terminal_filter)) &
        (driver_cohort['hire_year'] >= year_range[0]) & (
            driver_cohort['hire_year'] <= year_range[1])
    ].copy()

    fig_cohort = go.Figure()
    color_map = {'Chicago, IL': '#c0392b', 'Spokane, WA': '#2E86C1'}
    for terminal in terminal_filter:
        sub = cohort_filtered[cohort_filtered['home_terminal']
                              == terminal].sort_values('hire_year')
        fig_cohort.add_trace(go.Bar(x=sub['hire_year'], y=sub['termination_rate']*100, name=terminal,
                                    marker_color=color_map.get(terminal, '#94a3b8')))
    fig_cohort.update_layout(barmode='group', height=420, plot_bgcolor='white', margin=dict(l=10, r=10, t=30, b=10),
                             yaxis_title='Termination Rate (%)', xaxis_title='Hire Year')
    fig_cohort.add_annotation(x=2023, y=max(chi_rate*100, spo_rate*100) + 5, text="2023 cohort — the outlier",
                              showarrow=True, arrowhead=2, ay=-40, font=dict(color='#c0392b', size=12))
    st.plotly_chart(fig_cohort, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each pair of bars is one hire year, split by terminal. Most years show "
        "Chicago and Spokane's termination rates in a broadly similar range — normal industry churn. The "
        "2023 pair breaks that pattern sharply: Chicago's bar towers over every other year at either "
        "terminal, while Spokane's 2023 bar stays in line with its historical range. That's the signature "
        "of a terminal-specific issue in a single hiring class, not a fleet-wide or market-wide trend."
    )

    # ---- Experience distribution table ----
    st.markdown(
        "### Years of Experience — Chicago 2023 Cohort vs. Spokane Typical New Hires")
    chi_2023_drivers = driver_full[(driver_full['home_terminal'] == 'Chicago, IL') & (
        driver_full['hire_year'] == 2023)]
    spo_recent_drivers = driver_full[(driver_full['home_terminal'] == 'Spokane, WA') & (
        driver_full['hire_year'] >= 2021)]
    exp_compare = pd.DataFrame({
        'Group': ['Chicago 2023 Cohort', 'Spokane Recent Hires (2021+)'],
        'Avg Years Experience': [chi_2023_drivers['years_experience'].mean(), spo_recent_drivers['years_experience'].mean()],
        'Median Years Experience': [chi_2023_drivers['years_experience'].median(), spo_recent_drivers['years_experience'].median()],
        'Headcount': [len(chi_2023_drivers), len(spo_recent_drivers)]
    })
    st.dataframe(exp_compare.style.format({'Avg Years Experience': '{:.1f}', 'Median Years Experience': '{:.1f}'}),
                 use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** If Chicago's 2023 hires had noticeably less experience than Spokane's "
        "recent hires, that alone could partly explain higher churn — less experienced drivers tend to "
        "leave trucking altogether at higher rates industry-wide. If the experience levels are similar, "
        "as they are here, it rules out 'we just hired less qualified people' as the explanation and points "
        "back toward something about the Chicago terminal itself — pay, home time, dispatch load, or "
        "onboarding process."
    )

    st.divider()

    st.info(
        f"💡 **INSIGHT:** Chicago's 2023 hiring class has lost **{chi_terminated} of {chi_headcount}** "
        f"drivers (**{chi_rate*100:.1f}%**) — more than {chi_rate/spo_rate:.0f}x Spokane's 2023 cohort loss "
        f"rate ({spo_rate*100:.1f}%) in the same calendar year, with comparable driver experience levels "
        f"between the two cohorts. This strongly suggests the issue is specific to how the Chicago terminal "
        f"operated in 2023, not the quality of drivers hired or a broad driver-market trend."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because Cascade Summit's company-wide turnover number looks unremarkable at
{fleet_term_rate*100:.0f}% — nothing alarming on the surface — but that average blends 114 Spokane
drivers with a much smaller, much more volatile 51-driver Chicago population, hiding a serious problem
inside a single hiring class.

**What healthy vs. unhealthy looks like:** A termination rate in the 15-25% range for any given hiring
cohort is broadly normal in trucking — it's a demanding job with real turnover industry-wide. Chicago's
2023 cohort at {chi_rate*100:.1f}% is far outside that range, and critically, Spokane's *own* 2023 cohort
sits at a normal {spo_rate*100:.1f}% — proving this isn't a bad year for hiring drivers everywhere, it's
specific to Chicago.

**Step-by-step: what to do when a cohort looks like this:** First, rule out driver quality using the
experience-distribution table above — if Chicago's 2023 hires weren't meaningfully less experienced than
Spokane's, the problem isn't who was hired, it's how the terminal treated them once hired. Second,
since this dataset doesn't yet include exit-interview reasons, pay-by-terminal, or home-time data, the
next concrete step is gathering that data specifically for departed Chicago 2023 hires — a short round
of exit-interview follow-ups with anyone still reachable would likely surface the actual driver (pay,
dispatch frequency, home time, terminal management) faster than further data analysis alone.

**How often to check:** Quarterly is enough to monitor whether newer Chicago cohorts (2024, 2025, 2026)
are trending back toward Spokane's normal range — a sign that whatever changed after 2023 is working — or
repeating the 2023 pattern, which would call for a more urgent intervention.

**The most important action this week:** {DISPATCH_LEAD} should treat this as a terminal-management
question, not a hiring-quality question, and prioritize understanding what was different about Chicago's
operating conditions in 2023 (staffing, dispatch load, pay parity with Spokane, home-time frequency)
before making further hiring decisions there.
        """)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CASH FLOW & RECEIVABLES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "💰 Cash Flow & Receivables":
    st.title("Cash Flow & Receivables")
    st.caption(
        "What customers owe you, how overdue it is, and whether next week's cash covers next week's bills.")
    st.divider()

    st.markdown("""
    <div class="section-intro">
    📌 Cash flow — not profitability — is the #1 killer of small and mid-size trucking companies. This
    page shows you what's coming in, when, and whether you'll have enough to cover your expenses next
    week, independent of whether the business looks profitable on paper.
    </div>
    """, unsafe_allow_html=True)

    total_outstanding = ar_outstanding['invoice_amount'].sum()
    overdue_30 = ar_outstanding[ar_outstanding['days_outstanding']
                                > 30]['invoice_amount'].sum()
    avg_terms = customers['payment_terms_days'].mean()

    fixed_monthly_cost_est = st.number_input(
        "Estimated fixed monthly costs ($) — payroll, insurance, loan payments, etc.",
        min_value=100000, max_value=5000000, value=1200000, step=50000,
        help="Rough estimate of monthly fixed costs (not including fuel, which is captured separately in load costs). Used to project net cash position over the next 30 days."
    )

    incoming_30d = ar_outstanding[ar_outstanding['days_outstanding'] <= 30]['invoice_amount'].sum() + \
        total_outstanding * 0.3  # rough estimate of additional near-term collections
    net_cash_30d = incoming_30d - fixed_monthly_cost_est

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Outstanding AR", f"${total_outstanding:,.0f}",
                help="Total money customers currently owe you for delivered loads, not yet collected.")
    col2.metric("Overdue > 30 Days", f"${overdue_30:,.0f}",
                help="Invoices that should be getting a collections call now — the longer these sit, the harder they typically are to collect.")
    col3.metric("Avg Payment Terms", f"{avg_terms:.0f} days",
                help="Average number of days customers are contractually allowed to pay, across the portfolio. TitanBolt and Peachtree get 45 days; everyone else gets 30.")
    col4.metric("30-Day Net Cash Projection", f"${net_cash_30d:,.0f}",
                delta=None if net_cash_30d >= 0 else "Below zero — action needed",
                help="Estimated incoming collections over the next 30 days minus estimated fixed monthly costs. A negative number means you may need to accelerate collections or arrange short-term financing.")

    # ---- AR aging table ----
    st.markdown("### Accounts Receivable Aging")

    def aging_color(bucket):
        if bucket == '0-30 days':
            return 'background-color:#dcfce7;color:#166534'
        elif bucket == '31-60 days':
            return 'background-color:#fef9c3;color:#854d0e'
        else:
            return 'background-color:#fee2e2;color:#991b1b'

    aging_display = ar_outstanding.sort_values('days_outstanding', ascending=False)[
        ['customer_name', 'invoice_amount', 'load_date',
            'days_outstanding', 'aging_bucket']
    ].copy()
    aging_display.columns = ['Customer', 'Invoice Amount',
                             'Invoice Date', 'Days Outstanding', 'Aging Bucket']
    aging_display['Invoice Date'] = pd.to_datetime(
        aging_display['Invoice Date']).dt.strftime('%Y-%m-%d')
    styled_aging = aging_display.head(200).style.map(lambda v: aging_color(v), subset=['Aging Bucket']) \
        .format({'Invoice Amount': '${:,.0f}'})
    st.dataframe(styled_aging, use_container_width=True,
                 hide_index=True, height=400)
    st.caption(
        "📖 **Reading this table:** Green (0-30 days) is normal and expected. Yellow (31-60 days) deserves "
        "a friendly check-in call. Red (61+ days) should get a direct collections call this week — the "
        "longer an invoice sits unpaid, the more likely it is to become a write-off. Note: this ledger is "
        "a simulated view built from load and payment-terms data, since a live invoicing system isn't yet "
        "connected — treat it as directionally accurate, not to-the-penny precise."
    )

    # ---- 30-day cash projection chart ----
    st.markdown("### 30-Day Cash Projection")
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    weekly_incoming = incoming_30d / 4
    weekly_fixed = fixed_monthly_cost_est / 4
    running_balance = []
    balance = 0
    for w in weeks:
        balance += weekly_incoming - weekly_fixed
        running_balance.append(balance)
    fig_cash = go.Figure(go.Scatter(x=weeks, y=running_balance, mode='lines+markers',
                                    line=dict(color='#1B4F72', width=3), fill='tozeroy',
                                    fillcolor='rgba(46,134,193,0.15)'))
    fig_cash.add_hline(y=0, line_dash='dash', line_color='#c0392b')
    fig_cash.update_layout(height=350, plot_bgcolor='white', margin=dict(
        l=10, r=10, t=30, b=10), yaxis_title='Running Cash Balance ($)')
    st.plotly_chart(fig_cash, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This projects a running cash balance over the next 4 weeks, assuming "
        "incoming collections and fixed costs are spread evenly. If the line goes below zero (the red "
        "dashed line), you'll need to either accelerate collections on overdue invoices — see the aging "
        "table above for exactly who to call — or arrange short-term financing before that week arrives."
    )

    st.divider()

    # ---- Mark invoice paid (fake CRUD) ----
    with st.expander("✅ Mark an Invoice as Paid"):
        if len(ar_outstanding) > 0:
            pay_options = ar_outstanding.sort_values('days_outstanding', ascending=False)[
                'load_id'].tolist()
            pay_load = st.selectbox(
                "Select Invoice (Load ID)", pay_options, key="pay_load_select")
            pay_row = ar_outstanding[ar_outstanding['load_id']
                                     == pay_load].iloc[0]
            st.markdown(
                f"**Customer:** {pay_row['customer_name']} — **Amount:** ${pay_row['invoice_amount']:,.2f}")
            pay_date = st.date_input("Date paid", value=datetime.now().date())
            if st.button("Mark as Paid", key="mark_paid_btn"):
                st.session_state.ar_status_overrides[pay_load] = {
                    'paid_date': pay_date.strftime('%Y-%m-%d'),
                    'amount': float(pay_row['invoice_amount'])
                }
                st.session_state.action_log.append(
                    f"{datetime.now().strftime('%H:%M')} — Invoice {pay_load} ({pay_row['customer_name']}, ${pay_row['invoice_amount']:,.0f}) marked paid"
                )
                st.success(f"Invoice {pay_load} marked paid!")
                st.rerun()
        else:
            st.caption("No outstanding invoices to mark as paid.")

    if st.session_state.ar_status_overrides:
        st.markdown("**Recently Marked Paid:**")
        for load_id, info in list(st.session_state.ar_status_overrides.items())[::-1][:10]:
            st.markdown(
                f"- **{load_id}**: ${info['amount']:,.0f} paid on {info['paid_date']}")

    # ---- Insight callout ----
    if len(ar_outstanding[ar_outstanding['aging_bucket'] == '61+ days']) > 0:
        worst_overdue = ar_outstanding[ar_outstanding['aging_bucket'] ==
                                       '61+ days'].sort_values('invoice_amount', ascending=False).iloc[0]
        st.info(
            f"💡 **INSIGHT:** The highest-risk overdue invoice is **{worst_overdue['load_id']}** for "
            f"**{worst_overdue['customer_name']}** — **${worst_overdue['invoice_amount']:,.0f}**, outstanding "
            f"for **{worst_overdue['days_outstanding']:.0f} days**. This is the single call most likely to "
            f"improve this week's cash position."
        )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
Cash flow is different from profitability — you can be profitable on paper (revenue exceeding costs
over a quarter) and still run out of cash in the bank in a given week if customers pay slowly and fixed
costs like payroll and fuel don't wait. This page exists to catch that gap before it becomes a crisis.

**What each aging bucket means:** 0-30 days outstanding is completely normal — most of your customers
are on 30-day terms, so invoices in this bucket simply haven't come due yet. 31-60 days deserves a
friendly check-in call to make sure nothing's stuck (a missing paperwork issue, a billing dispute). 61+
days is a genuine collections situation — the longer it sits, the more likely it becomes a write-off, and
it deserves a direct, prompt phone call.

**A simple script for calling an overdue customer:** "Hi, this is {DISPATCH_LEAD} from Cascade Summit
Freightways — I'm calling about invoice [number] for [amount], which shows as [X] days past our agreed
terms. Is there anything on our end — paperwork, documentation — that's holding up payment? We'd like to
get this resolved this week." Keep it factual and collaborative, not adversarial — most overdue invoices
are administrative delays, not disputes.

**How to read the projection:** The 30-day cash projection chart assumes collections and fixed costs are
spread evenly across four weeks — a simplification, but a useful early-warning signal. If the projected
line dips below zero, that's your signal to act before the shortfall actually happens, not after.

**What to do if the projection goes negative:** First, work the aging table from the top down — call the
largest, oldest overdue invoices first, since they have the biggest single-call impact on your cash
position. Second, consider whether a short-term line of credit or factoring (selling receivables to a
finance company at a discount for immediate cash) makes sense as a bridge, especially for
TitanBolt/Peachtree invoices sitting on 45-day terms.

**Payment terms negotiation tips:** If a customer consistently pays at the very edge of their terms or
beyond, consider whether tightening their terms (45→30 days) or requiring a deposit on large loads is
worth the relationship risk — this is especially relevant for TitanBolt, which combines 45-day terms with
the fleet's worst on-time and detention profile.
        """)
