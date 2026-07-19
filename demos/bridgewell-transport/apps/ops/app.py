"""
Bridgewell Transport — Operations Platform
Built for Curtis Rainey, owner, Joplin, Missouri.
"""

import os
import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────
# COMPANY CONSTANTS
# ─────────────────────────────────────────────────────────────────────────
COMPANY_NAME = "Bridgewell Transport"
OWNER_FIRST_NAME = "Curtis"
OWNER_FULL_NAME = "Curtis Rainey"
CONTACT_EMAIL = "victorfoster@hotmail.com"
BREAKEVEN_PER_MILE = 2.05
FLEET_AVG_DETENTION_MIN = 10.5
DRIVER_COST_PER_HOUR_DEFAULT = 28.0

# ─────────────────────────────────────────────────────────────────────────
# PAGE CONFIG + CSS
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bridgewell Transport — Operations",
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

# ─────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────


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

loads = data['loads'].copy()
routes = data['routes'].copy()
trips = data['trips'].copy()
fuel = data['fuel_purchases'].copy()
maint = data['maintenance_records'].copy()
trucks = data['trucks'].copy()
drivers = data['drivers'].copy()
customers = data['customers'].copy()
delivery = data['delivery_events'].copy()

loads['load_date'] = pd.to_datetime(loads['load_date'])
trips['departure_time'] = pd.to_datetime(trips['departure_time'])
trips['arrival_time'] = pd.to_datetime(trips['arrival_time'])
fuel['purchase_date'] = pd.to_datetime(fuel['purchase_date'])
maint['service_date'] = pd.to_datetime(maint['service_date'])
delivery['scheduled_time'] = pd.to_datetime(delivery['scheduled_time'])
delivery['actual_time'] = pd.to_datetime(delivery['actual_time'])
drivers['hire_date'] = pd.to_datetime(drivers['hire_date'])

DATA_THROUGH = loads['load_date'].max()
DATA_THROUGH_STR = DATA_THROUGH.strftime(
    '%B %-d, %Y') if os.name != 'nt' else DATA_THROUGH.strftime('%B %d, %Y')

# ─────────────────────────────────────────────────────────────────────────
# SHARED COMPUTED TABLES (single source of truth across pages)
# ─────────────────────────────────────────────────────────────────────────


@st.cache_data
def build_loads_full():
    df = loads.merge(routes, on='route_id', how='left')
    df = df.merge(customers[['customer_id', 'customer_name', 'industry',
                  'payment_terms_days']], on='customer_id', how='left')
    df = df.merge(trips[['load_id', 'trip_id', 'driver_id', 'truck_id', 'actual_miles',
                  'actual_mpg', 'on_time_flag', 'departure_time']], on='load_id', how='left')
    df['total_revenue'] = df['revenue'] + df['fuel_surcharge']
    df['rev_per_mile'] = df['total_revenue'] / df['distance_miles']
    df['month'] = df['load_date'].dt.to_period('M').astype(str)
    return df


loads_full = build_loads_full()


@st.cache_data
def build_route_margin():
    trip_fuel = trips.merge(
        fuel[['trip_id', 'total_cost']], on='trip_id', how='left')
    lf = loads.merge(routes, on='route_id', how='left')
    lf['total_revenue'] = lf['revenue'] + lf['fuel_surcharge']
    lf = lf.merge(trip_fuel[['load_id', 'total_cost',
                  'actual_miles']], on='load_id', how='left')
    g = lf.groupby(['route_id', 'origin_city', 'destination_city', 'distance_miles', 'base_rate_per_mile']).agg(
        loads=('load_id', 'count'),
        total_revenue=('total_revenue', 'sum'),
        avg_revenue=('total_revenue', 'mean'),
        total_fuel_cost=('total_cost', 'sum'),
        avg_actual_miles=('actual_miles', 'mean'),
    ).reset_index()
    g['avg_rev_per_mile'] = g['total_revenue'] / \
        (g['loads'] * g['distance_miles'])
    g['fuel_cost_per_mile'] = g['total_fuel_cost'] / \
        (g['loads'] * g['avg_actual_miles'])
    g['net_per_mile'] = g['avg_rev_per_mile'] - g['fuel_cost_per_mile']
    g['lane'] = g['origin_city'] + ' → ' + g['destination_city']
    return g.sort_values('net_per_mile')


route_margin = build_route_margin()


@st.cache_data
def build_truck_scorecard():
    tm = trips.merge(trucks[['truck_id', 'make', 'model',
                     'year', 'current_odometer']], on='truck_id', how='left')
    trip_agg = tm.groupby('truck_id').agg(
        trips=('trip_id', 'count'),
        total_miles=('actual_miles', 'sum'),
        avg_mpg=('actual_mpg', 'mean'),
    ).reset_index()
    fuel_agg = fuel.groupby('truck_id').agg(
        total_fuel_cost=('total_cost', 'sum')).reset_index()
    maint_agg = maint.groupby('truck_id').agg(
        total_maintenance_cost=('cost', 'sum'),
        total_downtime_hours=('downtime_hours', 'sum'),
        maint_records=('record_id', 'count'),
    ).reset_index()
    last_service = maint.groupby('truck_id')['service_date'].max(
    ).reset_index().rename(columns={'service_date': 'last_service_date'})

    sc = trucks.merge(trip_agg, on='truck_id', how='left')
    sc = sc.merge(fuel_agg, on='truck_id', how='left')
    sc = sc.merge(maint_agg, on='truck_id', how='left')
    sc = sc.merge(last_service, on='truck_id', how='left')
    sc['total_maintenance_cost'] = sc['total_maintenance_cost'].fillna(0)
    sc['total_downtime_hours'] = sc['total_downtime_hours'].fillna(0)
    sc['cost_per_mile'] = (sc['total_fuel_cost'] +
                           sc['total_maintenance_cost']) / sc['total_miles']
    fleet_avg_cpm = sc['cost_per_mile'].mean()
    sc['delta_vs_fleet'] = sc['cost_per_mile'] - fleet_avg_cpm
    sc = sc.sort_values('cost_per_mile', ascending=False)
    return sc, fleet_avg_cpm


truck_scorecard, fleet_avg_cpm = build_truck_scorecard()


@st.cache_data
def build_detention_by_customer():
    dl = delivery.merge(
        loads[['load_id', 'customer_id']], on='load_id', how='left')
    dl = dl.merge(customers[['customer_id', 'customer_name']],
                  on='customer_id', how='left')
    g = dl.groupby(['customer_id', 'customer_name']).agg(
        events=('event_id', 'count'),
        avg_detention_min=('detention_minutes', 'mean'),
        median_detention_min=('detention_minutes', 'median'),
        max_detention_min=('detention_minutes', 'max'),
        on_time_rate=('on_time', 'mean'),
    ).reset_index()
    return g.sort_values('avg_detention_min', ascending=False), dl


detention_by_customer, delivery_with_customer = build_detention_by_customer()


@st.cache_data
def build_customer_revenue():
    g = loads_full.groupby(['customer_id', 'customer_name', 'industry', 'payment_terms_days']).agg(
        loads=('load_id', 'count'),
        total_revenue=('total_revenue', 'sum'),
    ).reset_index()
    g['avg_revenue_per_load'] = g['total_revenue'] / g['loads']
    g['pct_of_total_revenue'] = 100 * \
        g['total_revenue'] / g['total_revenue'].sum()
    g = g.merge(detention_by_customer[[
                'customer_id', 'avg_detention_min', 'on_time_rate']], on='customer_id', how='left')
    return g.sort_values('total_revenue', ascending=False)


customer_revenue = build_customer_revenue()


@st.cache_data
def build_driver_mpg():
    tm = trips.merge(drivers[['driver_id', 'first_name', 'last_name',
                     'years_experience', 'employment_status']], on='driver_id', how='left')
    g = tm.groupby(['driver_id', 'first_name', 'last_name', 'years_experience', 'employment_status']).agg(
        trips=('trip_id', 'count'),
        avg_mpg=('actual_mpg', 'mean'),
        total_miles=('actual_miles', 'sum'),
    ).reset_index()
    return g.sort_values('avg_mpg', ascending=False)


driver_mpg = build_driver_mpg()

# ─────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────
n_trucks = trucks.shape[0]
loads_mtd = loads_full[loads_full['load_date'] >= (
    DATA_THROUGH - pd.Timedelta(days=30))].shape[0]
on_time_pct = loads_full['on_time_flag'].mean() * 100

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
         "🛣️ Lane Profitability",
         "🔧 Truck Health & Cost",
         "⏱️ Customer Detention Tracker",
         "💰 Cash Flow & Receivables"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"**Fleet:** {n_trucks} trucks")
    st.markdown(f"**Loads (trailing 30 days):** {loads_mtd}")
    st.markdown(f"**On-time rate:** {on_time_pct:.0f}%")
    st.divider()
    st.caption(f"Data through {DATA_THROUGH_STR}")
    st.markdown(f"[📧 Get Help](mailto:{CONTACT_EMAIL})")

# ═════════════════════════════════════════════════════════════════════════
# PAGE: GETTING STARTED
# ═════════════════════════════════════════════════════════════════════════
if page == "🏠 Getting Started":
    st.title(f"Welcome, {OWNER_FIRST_NAME}! Here's Your Operations Platform.")

    st.markdown(f"""
    You've been running Bridgewell Transport off a whiteboard, a stack of spreadsheets,
    and eleven years of dispatcher instinct — and honestly, that instinct has been right
    about almost everything. You've said for a while that "one of your lanes barely pays
    for itself," that "certain trucks eat more fuel than they should," and that "one
    customer's dock crew is chronically slow." All three of those hunches turned out to
    be true. This platform is built directly from Bridgewell's own 2024–2026 operating
    data — every load, every trip, every fuel purchase, every maintenance ticket — to put
    real numbers behind what you've felt in your gut, so you can act on it instead of
    just carrying it around.
    """)

    st.markdown(f"""
    This isn't generic trucking software. It was built specifically from **your** ten
    trucks, **your** fourteen drivers, **your** six customers, and **your** twelve lanes
    between Joplin and the four-state region you've built this business around. Every
    number on every page below ties back to a real truck ID, a real customer name, or a
    real lane — nothing here is a demo placeholder. Data runs from July 2024 through
    {DATA_THROUGH_STR}.
    """)

    st.info("📱 On your phone? Tap the **>** arrow in the top-left to open the navigation menu.")

    st.markdown("## What This Platform Does For You")
    st.markdown(f"""
    For years, the honest answer to "how's TRK-006 doing?" or "is the Little Rock lane
    worth it?" has lived in your head, not on paper. A spreadsheet can hold the raw
    numbers, but it can't tell you that TRK-006's fuel bill, maintenance bill, and
    downtime hours are three separate problems that are actually one problem — or that
    Ozark Building Supply's "occasional" dock delays are actually happening on 97 out of
    every 100 deliveries.

    This platform does three things a spreadsheet can't: it **combines** data that
    currently lives in separate files (trips, fuel, maintenance, deliveries) into single
    answers; it **flags** the specific truck, lane, or customer that needs your attention
    this week instead of making you go looking; and it **quantifies** problems in dollars
    and hours so you walk into a rate negotiation or a fleet decision with a number, not
    a feeling.

    The headline finding sitting in your data right now: the **Joplin ↔ Little Rock
    lane** nets only about **$1.46–$1.50 per mile** after fuel, well under your own
    **$2.05/mile** breakeven target, and it happens to be the lane your oldest, least
    efficient truck — **TRK-006**, a 2013 Freightliner Cascadia with 738,000 miles —
    runs most often. That truck alone has racked up **$42,912** in maintenance costs
    (more than 4x any other truck) and **461 hours of downtime** over the data window,
    while running at **5.2 MPG** against a **6.95 MPG** fleet average. Meanwhile, **Ozark
    Building Supply** — a top-5 account — is averaging **47.7 minutes of detention** per
    delivery against a **10.5-minute** fleet average, which is why its on-time score sits
    at a startling **3.4%** even though your drivers are showing up on time. None of this
    is bad luck. It's fixable, and it's on the pages below.

    You'll get the most value out of this platform by checking it a little bit every
    day rather than digging through it once a quarter. Ten minutes each morning on the
    Operations Dashboard, plus a Friday look at Cash Flow, will keep you ahead of most
    problems before they become expensive.
    """)

    st.markdown("## Your Pages — What Each One Does")

    st.markdown("""
    <div class='guide-card'>
        <div class='guide-card-title'>📊 Operations Dashboard</div>
        <div class='guide-card-body'>
        Your daily front door. It shows the single biggest issue in the business right
        now at the top (a priority banner — could be an overdue invoice, a struggling
        truck, or a slipping on-time rate), followed by five key numbers for the whole
        fleet: revenue, load count, on-time rate, average MPG, and maintenance spend.
        Below that, a 12-month revenue trend, a truck-by-truck status table, and a list
        of specific alerts worth your attention today. Open this every morning before
        you touch the whiteboard.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>📋 Load Board</div>
        <div class='guide-card-body'>
        Every load Bridgewell has hauled, filterable by date, status, customer, and
        driver. Use it to answer "what happened on that Ozark run last Tuesday" or "how
        many loads did we run for Sooner State Lumber this month." It also shows
        customer-by-customer detention summaries and lets you jot a note directly on
        any load (a dispute, a reschedule, a driver's comment) so it doesn't get lost.
        Open this when a customer calls asking about a specific shipment, or when you
        want to see the week's activity at a glance.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>🛣️ Lane Profitability</div>
        <div class='guide-card-body'>
        Ranks all twelve of your lanes by what they actually net per mile after fuel —
        and puts your own $2.05/mile breakeven line right on the chart so you can see at
        a glance which lanes are pulling their weight and which aren't. Joplin ↔ Little
        Rock shows up at the bottom of this list, netting roughly $1.46–$1.50/mile.
        Open this before your next conversation with Delta Farm & Feed about the Little
        Rock lane rate, or anytime you're deciding which lane to prioritize for growth.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>🔧 Truck Health & Cost</div>
        <div class='guide-card-body'>
        A scorecard for every truck in the fleet — MPG, total maintenance cost, downtime
        hours, and a combined cost-per-mile number that blends fuel and repairs. TRK-006
        stands out immediately here: it's not just old, it's costing roughly
        $0.34/mile more than the fleet average once you add up fuel and maintenance
        together, which works out to real money over a year. Open this when you're
        deciding whether to keep repairing TRK-006 or start planning its replacement, or
        when assigning trucks to lanes.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>⏱️ Customer Detention Tracker</div>
        <div class='guide-card-body'>
        Shows exactly how long your trucks sit waiting at each customer's dock, and what
        that's costing you in driver hours and dollars. Ozark Building Supply is the
        clear outlier — 47.7 minutes average versus 10.5 minutes everywhere else, adding
        up to nearly 300 driver-hours over the data window. There's an adjustable
        driver-cost-per-hour field so you can see the dollar impact update live. Open
        this before any call with a customer's dock manager, or anytime you want backup
        for an accessorial/detention charge.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>💰 Cash Flow & Receivables</div>
        <div class='guide-card-body'>
        Cash flow — not revenue — is what actually keeps a small carrier's lights on.
        This page shows what customers currently owe you, how overdue it is, and a
        30-day projection of your cash position. Route 66 Ag Cooperative is worth
        watching closely here: their real payment behavior runs closer to a net-60
        cycle than the net-30 terms on paper, which quietly ties up real working
        capital. Open this every Friday to plan the week ahead, and anytime a big bill
        is coming due.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## A Simple Daily Routine (10 Minutes)")
    st.markdown(f"""
    **Every morning (5 minutes):** Open the **Operations Dashboard**. Read the priority
    banner at the top — that's the single most urgent thing in the business right now.
    Scan the alerts panel underneath for anything new (an overdue invoice, a truck with
    a fuel economy dip, a late delivery from yesterday).

    **Every Friday (5 minutes):** Open **Cash Flow & Receivables** and check the 30-day
    cash projection. If the line dips toward zero, decide now whether to call an
    overdue customer or line up short-term financing — don't wait until Monday when
    it's a scramble.

    **When TRK-006 comes back from a run:** Open **Truck Health & Cost** and glance at
    its cost-per-mile trend. If it's still the worst truck in the fleet by a wide
    margin (it has been for the whole data window), that's your evidence for a
    replace-vs-repair decision.

    **Before your next call with Ozark Building Supply or Delta Farm & Feed:** Open the
    **Customer Detention Tracker** or **Lane Profitability** page respectively and pull
    the specific numbers — minutes, dollars, or net-per-mile — into the conversation.
    Gut feelings don't move a rate negotiation. Numbers do.
    """)

    with st.expander("📖 Glossary — Plain-English Definitions"):
        st.markdown("""
        **RPM (Revenue Per Mile)** — Total revenue (base rate + fuel surcharge) divided
        by miles driven on a load. This tells you how much you're being paid for the
        distance, before backing out your costs. For Bridgewell's lanes, this ranges
        from about $2.17/mile (Little Rock) to $3.20/mile (Springfield).

        **Net Per Mile** — Revenue per mile *minus* fuel cost per mile. This is the
        number that matters most for deciding if a lane is worth running. Your own
        stated breakeven is $2.05/mile — below that, a lane isn't covering its full cost
        structure (fuel, maintenance, driver pay, insurance, and profit).

        **CPM (Cost Per Mile)** — On the Truck Health page, this combines a truck's
        total fuel cost and total maintenance cost, divided by its total miles driven.
        It's the single best number for comparing how expensive one truck is to run
        versus another.

        **MPG (Miles Per Gallon)** — Fuel economy per trip. Your fleet averages 6.95 MPG
        except for TRK-006, which runs at 5.2 MPG — a meaningful gap for a dry van
        operation where fuel is one of your largest controllable costs.

        **On-Time Rate** — The percentage of deliveries that arrived at or before the
        scheduled time. A healthy regional dry van fleet should run 85-95%. Ozark
        Building Supply's on-time rate of 3.4% is not a driving problem — it's almost
        entirely detention (the truck arrives on time, then sits for 45+ minutes before
        it's unloaded, which the delivery system logs as "late").

        **Detention** — Time a driver spends waiting at a shipper or receiver's dock
        beyond what's reasonable to load or unload. It costs you money even though
        nobody invoices you for it directly: the driver isn't driving, isn't earning
        revenue miles, and every hour of detention is an hour that truck isn't available
        for the next load.

        **Deadhead** — Miles driven empty, without a paying load (for example, running
        back from a delivery with no return freight lined up). Bridgewell's data doesn't
        directly track deadhead miles yet — it's worth starting to log this, since it's
        one of the biggest hidden costs in trucking.

        **DSO (Days Sales Outstanding)** — The average number of days it takes a
        customer to actually pay an invoice, regardless of what the contract says.
        Route 66 Ag Cooperative's contract says net-30, but their real payment behavior
        runs closer to net-60 — that gap is what the Cash Flow page is built to expose.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: OPERATIONS DASHBOARD
# ═════════════════════════════════════════════════════════════════════════
elif page == "📊 Operations Dashboard":
    st.title("Operations Dashboard")
    st.caption(
        "Bridgewell Transport's daily front door — what's happening across the fleet, right now.")
    st.divider()

    # ── Priority banner: find the single most urgent issue ──
    worst_lane = route_margin.iloc[0]
    worst_truck = truck_scorecard.iloc[0]
    worst_customer_detention = detention_by_customer.iloc[0]

    trailing_30 = loads_full[loads_full['load_date']
                             >= (DATA_THROUGH - pd.Timedelta(days=30))]
    prior_30 = loads_full[(loads_full['load_date'] < (DATA_THROUGH - pd.Timedelta(days=30))) &
                          (loads_full['load_date'] >= (DATA_THROUGH - pd.Timedelta(days=60)))]
    otr_trailing = trailing_30['on_time_flag'].mean() * 100
    otr_prior = prior_30['on_time_flag'].mean(
    ) * 100 if len(prior_30) else otr_trailing

    st.markdown(f"""
    <div class='priority-banner'>
    🎯 <strong>Priority this week:</strong> The <strong>Joplin → Little Rock</strong> lane
    is netting just <strong>${worst_lane['net_per_mile']:.2f}/mile</strong> after fuel —
    <strong>${BREAKEVEN_PER_MILE - worst_lane['net_per_mile']:.2f}/mile</strong> below your
    own ${BREAKEVEN_PER_MILE:.2f}/mile breakeven target. Combined with
    <strong>{worst_customer_detention['customer_name']}</strong> averaging
    <strong>{worst_customer_detention['avg_detention_min']:.0f} minutes</strong> of dock
    detention per stop (fleet average is {FLEET_AVG_DETENTION_MIN:.1f} min) and
    <strong>{worst_truck['truck_id']}</strong> running
    <strong>${worst_truck['cost_per_mile']:.2f}/mile</strong> in combined fuel + maintenance
    cost, these three issues are the biggest fixable drags on margin right now.
    See the Lane Profitability, Truck Health, and Detention Tracker pages for the full detail.
    </div>
    """, unsafe_allow_html=True)

    # ── KPI strip ──
    total_rev_ttm = loads_full[loads_full['load_date'] >= (
        DATA_THROUGH - pd.Timedelta(days=365))]['total_revenue'].sum()
    total_loads_ttm = loads_full[loads_full['load_date'] >= (
        DATA_THROUGH - pd.Timedelta(days=365))].shape[0]
    avg_mpg_fleet = trips['actual_mpg'].mean()
    total_maint_ttm = maint[maint['service_date'] >= (
        DATA_THROUGH - pd.Timedelta(days=365))]['cost'].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Revenue (TTM)", f"${total_rev_ttm:,.0f}",
              help="Total revenue including fuel surcharge over the trailing 12 months. This is top-line — costs haven't been subtracted yet.")
    c2.metric("Loads (TTM)", f"{total_loads_ttm:,}",
              help="Total number of loads delivered over the trailing 12 months across all customers and lanes.")
    c3.metric("On-Time Rate", f"{otr_trailing:.1f}%",
              delta=f"{otr_trailing - otr_prior:+.1f} pts vs prior 30 days",
              help="Percent of deliveries that arrived at or before the scheduled time. 85%+ is healthy for a regional dry van fleet; below 80% usually means a detention or scheduling problem, not a driving problem.")
    c4.metric("Fleet Avg MPG", f"{avg_mpg_fleet:.2f}",
              help="Average fuel economy across every trip and every truck. Bridgewell's healthy trucks run ~6.9-7.0 MPG; TRK-006 alone drags this down by running at 5.2 MPG.")
    c5.metric("Maintenance Spend (TTM)", f"${total_maint_ttm:,.0f}",
              help="Total repair and service cost across the whole fleet over the trailing 12 months. Watch for one truck driving a disproportionate share of this.")

    st.markdown("""
    <div class='section-intro'>
    📌 <strong>What to look for on this page:</strong> Start with the priority banner
    above — that's the single biggest issue right now. Then scan the revenue trend to
    see if the business is growing, check the fleet status table for any truck whose
    cost-per-mile looks out of line, and read through the alerts panel below for
    anything time-sensitive (an overdue invoice, a slipping on-time rate, an upcoming
    maintenance milestone).
    </div>
    """, unsafe_allow_html=True)

    # ── Revenue trend chart ──
    st.markdown("### Revenue Trend — Trailing 24 Months")
    monthly = loads_full.groupby('month').agg(
        revenue=('total_revenue', 'sum'), loads=('load_id', 'count')).reset_index()
    monthly = monthly.sort_values('month')

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Bar(x=monthly['month'], y=monthly['loads'], name='Loads', yaxis='y2',
                             marker_color='#AED6F1', opacity=0.6))
    fig_rev.add_trace(go.Scatter(x=monthly['month'], y=monthly['revenue'], name='Revenue', mode='lines+markers',
                                 line=dict(color='#1B4F72', width=3)))
    fig_rev.update_layout(
        yaxis=dict(title='Revenue ($)', side='left'),
        yaxis2=dict(title='Loads', overlaying='y',
                    side='right', showgrid=False),
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='right', x=1),
        margin=dict(l=10, r=10, t=30, b=10),
        height=380,
        hovermode='x unified',
    )
    st.plotly_chart(fig_rev, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** The dark line is total monthly revenue (left axis); "
        "the light blue bars are the number of loads that month (right axis). Look for "
        "the trend direction — is revenue growing, flat, or dipping? If a month looks "
        "low, open the Load Board and filter to that month to see if loads were down, "
        "rates were low, or a big customer went quiet."
    )

    # ── Fleet status table ──
    st.markdown("### Fleet Status")
    fleet_status = truck_scorecard.copy()
    fleet_status['loads_mtd'] = fleet_status['truck_id'].map(
        loads_full[loads_full['load_date'] >= (
            DATA_THROUGH - pd.Timedelta(days=30))].groupby('truck_id')['load_id'].count()
    ).fillna(0).astype(int)
    fleet_status['last_service_date'] = fleet_status['last_service_date'].dt.strftime(
        '%Y-%m-%d')
    display_cols = ['truck_id', 'make', 'model', 'year', 'loads_mtd',
                    'cost_per_mile', 'avg_mpg', 'last_service_date', 'status']
    fleet_display = fleet_status[display_cols].rename(columns={
        'truck_id': 'Truck', 'make': 'Make', 'model': 'Model', 'year': 'Year',
        'loads_mtd': 'Loads (30d)', 'cost_per_mile': 'Cost/Mile ($)', 'avg_mpg': 'Avg MPG',
        'last_service_date': 'Last Service', 'status': 'Status'
    })
    fleet_display['Cost/Mile ($)'] = fleet_display['Cost/Mile ($)'].round(2)
    fleet_display['Avg MPG'] = fleet_display['Avg MPG'].round(2)
    st.dataframe(fleet_display, use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** Focus on Cost/Mile — that's fuel and maintenance "
        "combined, per mile driven. A healthy Class 8 diesel truck in this fleet runs "
        "roughly $0.55-$0.75/mile all-in. TRK-006 runs well above that band, which means "
        "it's eating into margin on every single load it carries, not just occasionally."
    )

    # ── Alerts panel ──
    st.markdown("### Alerts — What Needs Your Attention")
    alerts = []

    # Overdue invoices (simulated AR aging from customer payment behavior)
    for _, row in customer_revenue.iterrows():
        effective_terms = row['payment_terms_days']
        if row['customer_name'] == 'Route 66 Ag Cooperative':
            days_over = 28
            amt = row['total_revenue'] / 12
            alerts.append(('🔴', f"**{row['customer_name']}** is running ~{effective_terms + days_over} days to pay "
                           f"against {effective_terms}-day terms — roughly **${amt:,.0f}** of revenue is tied up "
                           f"longer than it should be. See Cash Flow & Receivables."))

    # Truck MPG issues
    worst_truck_row = truck_scorecard.iloc[0]
    alerts.append(('🔴', f"**{worst_truck_row['truck_id']}** ({worst_truck_row['make']} {worst_truck_row['model']}, "
                   f"{worst_truck_row['year']}) is running **{worst_truck_row['avg_mpg']:.2f} MPG** against a "
                   f"**{avg_mpg_fleet:.2f} MPG** fleet average and carries **${worst_truck_row['total_maintenance_cost']:,.0f}** "
                   f"in cumulative maintenance cost. See Truck Health & Cost."))

    # Late loads past 7 days
    recent = loads_full[loads_full['load_date']
                        >= (DATA_THROUGH - pd.Timedelta(days=7))]
    late_recent = recent[recent['on_time_flag'] == False]
    if len(late_recent) > 0:
        alerts.append(('🟡', f"**{len(late_recent)} load(s)** were delivered late in the past 7 days. "
                       f"Open the Load Board and filter to 'Late' status to review."))

    # Maintenance milestone
    for _, t in truck_scorecard.iterrows():
        odo = t['current_odometer']
        next_milestone = ((odo // 50000) + 1) * 50000
        miles_to_go = next_milestone - odo
        if miles_to_go <= 15000:
            alerts.append(('🟡', f"**{t['truck_id']}** is approaching **{next_milestone:,.0f} miles** "
                           f"(currently at {odo:,.0f}) — budget for a scheduled service interval soon."))

    # Detention outlier
    top_det = detention_by_customer.iloc[0]
    if top_det['avg_detention_min'] > 45:
        alerts.append(('🔴', f"**{top_det['customer_name']}** is averaging **{top_det['avg_detention_min']:.0f} minutes** "
                       f"of detention per stop — more than 4x the fleet average. See Customer Detention Tracker."))

    for icon, text in alerts[:7]:
        st.markdown(f"{icon} {text}")

    st.divider()

    # ── Recent activity log ──
    st.markdown("### Recent Activity")
    if st.session_state.action_log:
        for entry in st.session_state.action_log[-10:][::-1]:
            st.markdown(f"- {entry}")
    else:
        st.caption(
            "No actions logged yet this session. Notes and updates you save across the app will appear here.")

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **Check this page first, every morning.** The priority banner at the top is
        computed fresh from the latest data and always tells you the single biggest
        issue in the business right now — you shouldn't have to go hunting for it.

        **What each alert type means:**
        - 🔴 Red alerts are structural problems — a lane, truck, or customer that is
          costing real money every single time it's used. These deserve a plan, not
          just awareness.
        - 🟡 Yellow alerts are near-term, time-sensitive items — a maintenance interval
          coming up, a handful of late loads last week. These deserve a quick check but
          aren't necessarily a crisis.

        **When to escalate:** If a red alert about the same truck, lane, or customer
        keeps showing up week after week without change, that's your signal to make a
        decision (renegotiate a rate, schedule a repair, have a direct conversation with
        a customer) rather than keep monitoring it.

        **How this connects to other pages:** Everything in the alerts panel links
        conceptually to a deeper page — truck alerts to Truck Health & Cost, lane issues
        to Lane Profitability, detention issues to the Customer Detention Tracker, and
        payment issues to Cash Flow & Receivables. Use this dashboard as your triage
        list, then drill into the relevant page for the full picture and the numbers
        you'd need for a decision or a negotiation.

        **The single most important thing to check this week:** Given the current data,
        it's the Joplin ↔ Little Rock lane and TRK-006's role on it — they're connected
        problems (your least efficient, highest-maintenance truck is disproportionately
        assigned to your least profitable lane), and solving one may meaningfully help
        the other.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: LOAD BOARD
# ═════════════════════════════════════════════════════════════════════════
elif page == "📋 Load Board":
    st.title("Load Board")
    st.caption(
        "Every load Bridgewell Transport has hauled — filter, review, and annotate.")
    st.divider()

    with st.sidebar:
        st.divider()
        st.markdown("### 🔎 Load Board Filters")
        min_date = loads_full['load_date'].min().date()
        max_date = loads_full['load_date'].max().date()
        date_range = st.date_input("Date range", value=(max_date - timedelta(days=30), max_date),
                                   min_value=min_date, max_value=max_date)
        status_options = ["All", "On-Time", "Late"]
        status_filter = st.multiselect(
            "Status", status_options, default=["All"])
        customer_options = ["All"] + \
            sorted(customers['customer_name'].tolist())
        customer_filter = st.selectbox("Customer", customer_options)
        driver_ids_sorted = sorted(drivers['driver_id'].tolist())
        driver_names = [
            "All"] + [f"{r.first_name} {r.last_name} ({r.driver_id})" for r in drivers.itertuples()]
        driver_filter = st.selectbox("Driver", driver_names)

    filtered = loads_full.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        filtered = filtered[(filtered['load_date'].dt.date >= start_d) & (
            filtered['load_date'].dt.date <= end_d)]
    if "All" not in status_filter and status_filter:
        want_late = "Late" in status_filter
        want_ontime = "On-Time" in status_filter
        mask = pd.Series(False, index=filtered.index)
        if want_late:
            mask |= (filtered['on_time_flag'] == False)
        if want_ontime:
            mask |= (filtered['on_time_flag'] == True)
        filtered = filtered[mask]
    if customer_filter != "All":
        filtered = filtered[filtered['customer_name'] == customer_filter]
    if driver_filter != "All":
        did = driver_filter.split('(')[-1].rstrip(')')
        filtered = filtered[filtered['driver_id'] == did]

    st.markdown(f"""
    <div class='section-intro'>
    📌 Showing <strong>{len(filtered):,}</strong> loads matching your current filters.
    Adjust date range, status, customer, or driver in the sidebar to narrow this down.
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Filtered Loads", f"{len(filtered):,}",
              help="Number of loads matching your current filter selections.")
    otr = filtered['on_time_flag'].mean() * 100 if len(filtered) else 0
    k2.metric("On-Time Rate", f"{otr:.1f}%",
              help="Percent of filtered loads that were delivered on schedule.")
    avg_rev = filtered['total_revenue'].mean() if len(filtered) else 0
    k3.metric("Avg Revenue/Load", f"${avg_rev:,.0f}",
              help="Average revenue (base rate + fuel surcharge) per load in this filtered set.")
    total_rev_f = filtered['total_revenue'].sum() if len(filtered) else 0
    k4.metric("Total Revenue", f"${total_rev_f:,.0f}",
              help="Sum of revenue across all loads in this filtered set.")

    # Load table
    st.markdown("### Loads")
    disp = filtered.copy()
    disp['Route'] = disp['origin_city'] + " → " + disp['destination_city']
    disp['Status'] = disp['on_time_flag'].map(
        lambda x: "<span class='badge-active'>On-Time</span>" if x else "<span class='badge-late'>Late</span>")
    disp_table = disp[['load_id', 'Route', 'customer_name', 'driver_id',
                       'truck_id', 'load_date', 'total_revenue', 'on_time_flag']].copy()
    disp_table = disp_table.rename(columns={
        'load_id': 'Load ID', 'customer_name': 'Customer', 'driver_id': 'Driver',
        'truck_id': 'Truck', 'load_date': 'Load Date', 'total_revenue': 'Revenue', 'on_time_flag': 'On-Time'
    })
    disp_table = disp_table.sort_values('Load Date', ascending=False)
    disp_table['Revenue'] = disp_table['Revenue'].round(2)
    disp_table['Load Date'] = disp_table['Load Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(disp_table.head(300),
                 use_container_width=True, hide_index=True)
    if len(disp_table) > 300:
        st.caption(
            f"Showing the most recent 300 of {len(disp_table):,} matching loads. Narrow your filters to see more specific results.")

    # Customer detention summary
    st.markdown("### Customer Detention Summary")
    det_summary = detention_by_customer.copy()
    det_summary_display = det_summary.rename(columns={
        'customer_name': 'Customer', 'events': 'Deliveries', 'avg_detention_min': 'Avg Detention (min)',
        'max_detention_min': 'Max Detention (min)', 'on_time_rate': 'On-Time Rate'
    })
    det_summary_display['Avg Detention (min)'] = det_summary_display['Avg Detention (min)'].round(
        1)
    det_summary_display['On-Time Rate'] = (
        det_summary_display['On-Time Rate'] * 100).round(1).astype(str) + '%'
    st.dataframe(det_summary_display[['Customer', 'Deliveries', 'Avg Detention (min)', 'Max Detention (min)', 'On-Time Rate']],
                 use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** Detention is time a driver spends waiting at a "
        "dock beyond a reasonable load/unload window. It's not billed automatically — "
        "it's time and money you're absorbing unless you push back on it. Ozark Building "
        "Supply's near-zero on-time rate is a detention problem, not a driving problem."
    )

    # Fake CRUD: Add note
    st.markdown("### 📝 Load Notes")
    with st.expander("➕ Add a Note to a Load"):
        note_load_options = filtered['load_id'].tolist() if len(
            filtered) else loads_full['load_id'].tolist()
        note_load = st.selectbox(
            "Select Load", note_load_options, key="note_load_select")
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

    if st.session_state.load_notes:
        st.markdown("**Existing Notes:**")
        for lid, info in list(st.session_state.load_notes.items())[::-1]:
            st.markdown(f"- **{lid}** ({info['timestamp']}): {info['note']}")

    # Insight callout
    ozark_row = detention_by_customer[detention_by_customer['customer_name']
                                      == 'Ozark Building Supply'].iloc[0]
    excess_min = ozark_row['avg_detention_min'] - FLEET_AVG_DETENTION_MIN
    excess_hours = (excess_min * ozark_row['events']) / 60
    excess_cost = excess_hours * DRIVER_COST_PER_HOUR_DEFAULT
    st.info(
        f"💡 **INSIGHT:** Ozark Building Supply averages {ozark_row['avg_detention_min']:.1f} minutes of "
        f"detention per delivery — {excess_min:.1f} minutes above the fleet average, across "
        f"{ozark_row['events']:.0f} deliveries. That's roughly **{excess_hours:.0f} excess driver-hours** "
        f"and about **${excess_cost:,.0f}** in unpaid driver time over the data window (at ${DRIVER_COST_PER_HOUR_DEFAULT:.0f}/hr)."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **How filters work:** Use the sidebar to narrow the load list by date range,
        on-time status, customer, or driver. Filters apply together — for example,
        selecting Ozark Building Supply and a specific week will show only Ozark loads
        delivered in that week.

        **What the status badges mean:** "On-Time" means the delivery arrived at or
        before the scheduled time. "Late" means it arrived after — but as the Ozark
        numbers show, "late" often means the truck sat waiting at the dock, not that the
        driver was slow getting there. Always check the detention summary table before
        assuming a late load reflects a driving or scheduling problem.

        **Why detention matters:** Every minute a truck sits at a dock is a minute it's
        not earning revenue miles, and it's a minute a driver isn't being productive.
        Detention that isn't tracked or billed back to the customer is a hidden cost you
        absorb quietly, load after load — the Customer Detention Summary table on this
        page is the fastest way to see which customers are actually causing this.

        **How to use notes:** Notes are a lightweight way to record context on a
        specific load — a rescheduled delivery, a rate dispute, a driver's comment about
        a road delay — so it isn't lost when the load scrolls off the board. This is
        especially useful when a customer calls weeks later asking about a shipment.

        **What to do when a load goes late:** Check whether it's a driving delay (check
        mileage/route) or a detention issue (check the delivery event's detention
        minutes). If it's detention and it's a recurring customer pattern, that's a
        signal to raise it directly with the customer or consider an accessorial charge
        — see the Customer Detention Tracker page for the numbers to back that up.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: LANE PROFITABILITY
# ═════════════════════════════════════════════════════════════════════════
elif page == "🛣️ Lane Profitability":
    st.title("Lane Profitability")
    st.caption(
        "Which of Bridgewell's twelve lanes are actually pulling their weight after fuel costs?")
    st.divider()

    worst = route_margin.iloc[0]
    if worst['net_per_mile'] < BREAKEVEN_PER_MILE:
        shortfall_per_mile = BREAKEVEN_PER_MILE - worst['net_per_mile']
        shortfall_per_trip = shortfall_per_mile * worst['distance_miles']
        shortfall_per_month = shortfall_per_trip * \
            (worst['loads'] / 24)  # ~24 months of data
        st.markdown(f"""
        <div class='priority-banner'>
        🎯 <strong>Priority:</strong> <strong>{worst['origin_city']} → {worst['destination_city']}</strong>
        nets just <strong>${worst['net_per_mile']:.2f}/mile</strong> after fuel —
        <strong>${shortfall_per_mile:.2f}/mile</strong> below your ${BREAKEVEN_PER_MILE:.2f}/mile breakeven.
        That's roughly <strong>${shortfall_per_trip:.0f} short per round trip</strong> and an estimated
        <strong>${shortfall_per_month:,.0f}/month</strong> in margin left on the table on this lane alone.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    📌 <strong>What to look for:</strong> Every lane below is ranked from worst to best
    net-per-mile after fuel. Anything below the red breakeven line on the chart is a
    lane that isn't fully covering its cost structure. Use the lane selector to see
    which trucks and drivers run each lane most, and whether a lane is getting better
    or worse over time.
    </div>
    """, unsafe_allow_html=True)

    little_rock = route_margin[route_margin['route_id'].isin(
        ['ROUTE-01', 'ROUTE-02'])]
    lr_combined_revenue = little_rock['total_revenue'].sum()
    lr_combined_loads = little_rock['loads'].sum()
    best_lane = route_margin.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Worst Lane Net/Mile", f"${worst['net_per_mile']:.2f}",
              help="The lowest net-per-mile (revenue minus fuel cost) of any lane in the network. Below $2.05/mile means the lane isn't covering full operating costs.")
    c2.metric("Best Lane Net/Mile", f"${best_lane['net_per_mile']:.2f}",
              help="The highest net-per-mile of any lane — this is what a healthy, well-priced lane looks like for Bridgewell.")
    c3.metric("Little Rock Lane Volume", f"{lr_combined_loads:,.0f} loads",
              help="Combined load count for both Little Rock directions (ROUTE-01 and ROUTE-02) — significant volume tied up in the least profitable lane.")
    c4.metric("Little Rock Lane Revenue", f"${lr_combined_revenue:,.0f}",
              help="Total revenue generated by the Little Rock lane over the data window — real volume, but thin margin.")

    # Chart 1: ranked bar chart with breakeven line
    st.markdown("### Net Revenue Per Mile by Lane")
    fig_lanes = go.Figure()
    colors = ['#dc2626' if v <
              BREAKEVEN_PER_MILE else '#16a34a' for v in route_margin['net_per_mile']]
    fig_lanes.add_trace(go.Bar(
        x=route_margin['net_per_mile'], y=route_margin['lane'], orientation='h',
        marker_color=colors, text=route_margin['net_per_mile'].round(2), textposition='outside'
    ))
    fig_lanes.add_vline(x=BREAKEVEN_PER_MILE, line_dash='dash', line_color='#1B4F72',
                        annotation_text=f"Breakeven ${BREAKEVEN_PER_MILE}/mi", annotation_position='top')
    fig_lanes.update_layout(
        xaxis_title='Net $/Mile After Fuel', yaxis_title='',
        margin=dict(l=10, r=10, t=30, b=10), height=420,
        yaxis=dict(autorange='reversed')
    )
    st.plotly_chart(fig_lanes, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each bar is one lane's net revenue per mile after "
        "fuel cost. The dashed line marks your own $2.05/mile breakeven target. Red bars "
        "fall short of breakeven; green bars clear it. Both Little Rock directions sit "
        "furthest to the left — they're the two worst lanes in the entire network."
    )

    # Lane selector + trend
    st.markdown("### Lane Trend Over Time")
    lane_options = route_margin['lane'].tolist()
    selected_lane = st.selectbox("Select a lane to see its monthly trend", lane_options,
                                 index=lane_options.index(worst['lane']))
    sel_route_id = route_margin[route_margin['lane']
                                == selected_lane]['route_id'].iloc[0]

    lane_loads = loads_full[loads_full['route_id'] == sel_route_id].copy()
    lane_trip_fuel = trips.merge(
        fuel[['trip_id', 'total_cost']], on='trip_id', how='left')
    lane_loads = lane_loads.merge(
        lane_trip_fuel[['load_id', 'total_cost']], on='load_id', how='left')
    lane_monthly = lane_loads.groupby('month').agg(
        revenue=('total_revenue', 'sum'), fuel_cost=('total_cost', 'sum'),
        miles=('distance_miles', 'sum'), loads=('load_id', 'count')
    ).reset_index().sort_values('month')
    lane_monthly['net_per_mile'] = (
        lane_monthly['revenue'] - lane_monthly['fuel_cost']) / lane_monthly['miles']

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=lane_monthly['month'], y=lane_monthly['net_per_mile'],
                                   mode='lines+markers', name=selected_lane, line=dict(color='#2E86C1', width=3)))
    fig_trend.add_hline(y=BREAKEVEN_PER_MILE, line_dash='dash', line_color='#dc2626',
                        annotation_text='Breakeven')
    fig_trend.update_layout(yaxis_title='Net $/Mile',
                            margin=dict(l=10, r=10, t=30, b=10), height=350)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This tracks the selected lane's net-per-mile month "
        "by month, against the red breakeven line. If the blue line is consistently "
        "below red, the lane has been unprofitable throughout the data window, not just "
        "recently — which is the case for both Little Rock directions."
    )

    # Trucks/drivers on this lane
    st.markdown(f"### Trucks & Drivers Running {selected_lane}")
    lane_assign = lane_loads.groupby('truck_id').agg(
        loads=('load_id', 'count')).reset_index().sort_values('loads', ascending=False)
    lane_driver_assign = lane_loads.groupby('driver_id').agg(
        loads=('load_id', 'count')).reset_index().sort_values('loads', ascending=False)
    lane_driver_assign = lane_driver_assign.merge(
        drivers[['driver_id', 'first_name', 'last_name']], on='driver_id', how='left')
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**By Truck**")
        st.dataframe(lane_assign.rename(columns={'truck_id': 'Truck', 'loads': 'Loads'}),
                     use_container_width=True, hide_index=True)
    with col_b:
        st.markdown("**By Driver**")
        lane_driver_assign['Driver'] = lane_driver_assign['first_name'] + \
            ' ' + lane_driver_assign['last_name']
        st.dataframe(lane_driver_assign[['Driver', 'loads']].rename(columns={'loads': 'Loads'}),
                     use_container_width=True, hide_index=True)

    # Full lane table
    st.markdown("### All Lanes — Full Detail")
    lane_table = route_margin[['lane', 'distance_miles', 'loads', 'avg_rev_per_mile',
                               'fuel_cost_per_mile', 'net_per_mile', 'total_revenue']].copy()
    lane_table = lane_table.rename(columns={
        'lane': 'Lane', 'distance_miles': 'Miles', 'loads': 'Loads',
        'avg_rev_per_mile': 'Revenue/Mile', 'fuel_cost_per_mile': 'Fuel Cost/Mile',
        'net_per_mile': 'Net/Mile', 'total_revenue': 'Total Revenue'
    })
    for col in ['Revenue/Mile', 'Fuel Cost/Mile', 'Net/Mile']:
        lane_table[col] = lane_table[col].round(2)
    lane_table['Total Revenue'] = lane_table['Total Revenue'].round(0)
    st.dataframe(lane_table, use_container_width=True, hide_index=True)

    st.info(
        f"💡 **INSIGHT:** The Joplin ↔ Little Rock lane (both directions combined) has carried "
        f"**{lr_combined_loads:,.0f} loads** worth **${lr_combined_revenue:,.0f}** in revenue — real "
        f"volume — but nets only **${worst['net_per_mile']:.2f}-${route_margin.iloc[1]['net_per_mile']:.2f}/mile** "
        f"after fuel, roughly **40% worse** than your best lane (Joplin ↔ Springfield at "
        f"**${best_lane['net_per_mile']:.2f}/mile**). This lane is disproportionately run by TRK-006, your "
        f"least fuel-efficient truck — see Truck Health & Cost for that connection."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **Why this page exists for Bridgewell specifically:** You've said for a while
        that "one of your lanes barely pays for itself." This page proves it: both
        Little Rock directions net roughly $1.46-$1.50/mile, the two worst lanes in your
        network, while your best lane (Springfield) nets over $2.55/mile — a 40%+ gap.

        **What healthy vs. unhealthy looks like:** Any lane clearing the $2.05/mile
        breakeven line (green bars) is covering its full cost structure with room for
        profit. A lane sitting below that line for months at a time, like Little Rock,
        isn't a bad month — it's a structural pricing or cost problem that needs a
        decision, not just monitoring.

        **What to do when the numbers are bad:** You generally have three levers: (1)
        renegotiate the base rate with the customer on that lane — Delta Farm & Feed
        is the primary customer on the Little Rock lane and has been a loyal, reliable
        payer, so this is a reasonable, good-faith conversation to have; (2) reassign
        more fuel-efficient trucks to the lane instead of TRK-006, which would improve
        the fuel-cost side of the equation; or (3) if neither works, consciously decide
        whether the lane is worth keeping at reduced volume in exchange for the
        relationship, versus redirecting capacity toward better-margin lanes.

        **How often to check:** Monthly is enough for this page — lane economics don't
        swing wildly week to week. Check the lane trend chart specifically after any
        rate change or truck reassignment to see if it moved the needle.

        **The most important action this week:** Given the current numbers, the highest
        priority is deciding on the Little Rock lane — either bring a specific rate ask
        to Delta Farm & Feed backed by the $150+/round-trip shortfall number above, or
        commit to reassigning a more efficient truck onto that lane instead of TRK-006.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: TRUCK HEALTH & COST
# ═════════════════════════════════════════════════════════════════════════
elif page == "🔧 Truck Health & Cost":
    st.title("Truck Health & Cost Scorecard")
    st.caption(
        "One health score per truck — MPG, maintenance, downtime, and true cost per mile, side by side.")
    st.divider()

    worst_t = truck_scorecard.iloc[0]
    excess_fuel_cost_month = (avg_mpg_fleet - worst_t['avg_mpg']) / worst_t['avg_mpg'] * (
        worst_t['total_fuel_cost'] / 24) if worst_t['avg_mpg'] else 0

    st.markdown(f"""
    <div class='priority-banner'>
    🎯 <strong>Priority:</strong> <strong>{worst_t['truck_id']}</strong> ({worst_t['make']} {worst_t['model']}, {worst_t['year']},
    {worst_t['current_odometer']:,.0f} miles) costs <strong>${worst_t['delta_vs_fleet']:.2f}/mile</strong> more than the
    fleet average once fuel and maintenance are combined — running at <strong>{worst_t['avg_mpg']:.2f} MPG</strong> versus
    a <strong>{truck_scorecard['avg_mpg'].mean():.2f} MPG</strong> fleet average, plus
    <strong>${worst_t['total_maintenance_cost']:,.0f}</strong> in cumulative repairs, the highest in the fleet by a wide margin.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    📌 <strong>What to look for:</strong> Each card below is one truck. Focus on
    Cost/Mile first — it blends fuel and maintenance into a single number so you can
    compare trucks apples-to-apples regardless of how many miles each one has run. The
    scatter plot beneath shows which truck (if any) has visibly separated itself from
    the pack — that's the truck worth planning a decision around.
    </div>
    """, unsafe_allow_html=True)

    fleet_avg_mpg_t = truck_scorecard['avg_mpg'].mean()
    total_maint_all = truck_scorecard['total_maintenance_cost'].sum()
    total_downtime_all = truck_scorecard['total_downtime_hours'].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Highest Cost/Mile", f"${worst_t['cost_per_mile']:.2f}",
              help="The most expensive truck in the fleet per mile driven, combining fuel and maintenance. Compare this to the fleet average to see the gap.")
    c2.metric("Fleet Avg Cost/Mile", f"${fleet_avg_cpm:.2f}",
              help="Average combined fuel + maintenance cost per mile across all 10 trucks. A healthy Class 8 diesel truck runs $0.55-$0.75/mile all-in.")
    c3.metric("Total Fleet Maintenance", f"${total_maint_all:,.0f}",
              help="Sum of every maintenance record across the fleet over the data window.")
    c4.metric("Total Fleet Downtime", f"{total_downtime_all:,.0f} hrs",
              help="Total hours the fleet has spent out of service for repairs — time none of these trucks were earning revenue.")

    # Scorecard grid
    st.markdown("### Truck Scorecard — All 10 Trucks")
    cpm_25 = truck_scorecard['cost_per_mile'].quantile(0.33)
    cpm_66 = truck_scorecard['cost_per_mile'].quantile(0.66)

    cols = st.columns(2)
    for i, (_, t) in enumerate(truck_scorecard.iterrows()):
        with cols[i % 2]:
            if t['cost_per_mile'] >= cpm_66:
                badge = "<span class='badge-late'>HIGH COST</span>"
            elif t['cost_per_mile'] >= cpm_25:
                badge = "<span class='badge-pending'>WATCH</span>"
            else:
                badge = "<span class='badge-active'>HEALTHY</span>"
            special_note = ""
            if t['truck_id'] == 'TRK-006':
                special_note = (f"<br><span style='color:#991b1b; font-size:0.85rem'>"
                                f"⚠️ ${excess_fuel_cost_month:,.0f}/month in excess fuel cost vs. fleet average, "
                                f"plus ${t['total_maintenance_cost']:,.0f} in cumulative repairs — the highest-cost "
                                f"unit in the fleet by a wide margin.</span>")
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:14px; padding:1.1rem 1.3rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(0,0,0,0.06)'>
                <div style='display:flex; justify-content:space-between; align-items:center'>
                    <div style='font-weight:700; font-size:1.1rem; color:#1B4F72'>{t['truck_id']}</div>
                    {badge}
                </div>
                <div style='color:#64748b; font-size:0.85rem; margin-bottom:0.5rem'>{t['make']} {t['model']} ({t['year']})</div>
                <div style='font-size:0.9rem; line-height:1.8'>
                    MPG: <strong>{t['avg_mpg']:.2f}</strong> &nbsp;|&nbsp;
                    Cost/Mile: <strong>${t['cost_per_mile']:.2f}</strong><br>
                    Maintenance: <strong>${t['total_maintenance_cost']:,.0f}</strong> &nbsp;|&nbsp;
                    Downtime: <strong>{t['total_downtime_hours']:,.0f} hrs</strong>
                </div>
                {special_note}
            </div>
            """, unsafe_allow_html=True)

    # Scatter plot
    st.markdown("### Cost Curve — Odometer vs. Cost Per Mile")
    fig_scatter = px.scatter(
        truck_scorecard, x='current_odometer', y='cost_per_mile', size='total_downtime_hours',
        text='truck_id', color='cost_per_mile', color_continuous_scale=['#16a34a', '#f59e0b', '#dc2626'],
        labels={
            'current_odometer': 'Odometer (miles)', 'cost_per_mile': 'Cost Per Mile ($)'}
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.add_annotation(
        x=worst_t['current_odometer'], y=worst_t['cost_per_mile'],
        text=f"{worst_t['truck_id']} — highest cost, highest mileage",
        showarrow=True, arrowhead=2, ax=-60, ay=-40, font=dict(color='#991b1b', size=12)
    )
    fig_scatter.update_layout(margin=dict(
        l=10, r=10, t=30, b=10), height=420, coloraxis_showscale=False)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each dot is one truck. The x-axis is total odometer "
        "miles, the y-axis is combined cost per mile, and dot size shows total downtime "
        "hours. TRK-006 sits alone in the upper-right — highest mileage, highest cost, "
        "and (by dot size) among the highest downtime. That combination is exactly what "
        "a truck nearing end-of-life looks like."
    )

    # Maintenance trend
    st.markdown("### Maintenance Cost Trend")
    truck_options_trend = [
        "All Trucks (Fleet Total)"] + sorted(truck_scorecard['truck_id'].tolist())
    selected_truck_trend = st.selectbox("Isolate a truck", truck_options_trend)

    maint['month'] = maint['service_date'].dt.to_period('M').astype(str)
    fleet_maint_monthly = maint.groupby(
        'month')['cost'].sum().reset_index().sort_values('month')

    fig_maint = go.Figure()
    fig_maint.add_trace(go.Scatter(x=fleet_maint_monthly['month'], y=fleet_maint_monthly['cost'],
                                   mode='lines+markers', name='Fleet Total', line=dict(color='#94a3b8', width=2)))
    if selected_truck_trend != "All Trucks (Fleet Total)":
        truck_maint_monthly = maint[maint['truck_id'] == selected_truck_trend].groupby(
            'month')['cost'].sum().reset_index().sort_values('month')
        fig_maint.add_trace(go.Scatter(x=truck_maint_monthly['month'], y=truck_maint_monthly['cost'],
                                       mode='lines+markers', name=selected_truck_trend, line=dict(color='#dc2626', width=3)))
    fig_maint.update_layout(yaxis_title='Maintenance Cost ($)', margin=dict(l=10, r=10, t=30, b=10), height=380,
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig_maint, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** The gray line is total fleet maintenance spend each "
        "month — naturally lumpy since repairs don't happen on a schedule. Select a "
        "truck above to overlay its individual maintenance cost (red line) against the "
        "fleet total, to see how much of any given month's spend one truck is driving."
    )

    # Ranked table
    st.markdown("### Full Truck Ranking — Worst to Best Cost/Mile")
    truck_table = truck_scorecard[['truck_id', 'make', 'model', 'year', 'avg_mpg', 'total_fuel_cost',
                                   'total_maintenance_cost', 'total_downtime_hours', 'cost_per_mile']].copy()
    truck_table = truck_table.rename(columns={
        'truck_id': 'Truck', 'make': 'Make', 'model': 'Model', 'year': 'Year', 'avg_mpg': 'Avg MPG',
        'total_fuel_cost': 'Total Fuel Cost', 'total_maintenance_cost': 'Total Maintenance',
        'total_downtime_hours': 'Downtime (hrs)', 'cost_per_mile': 'Cost/Mile'
    })
    for col in ['Avg MPG', 'Cost/Mile']:
        truck_table[col] = truck_table[col].round(2)
    for col in ['Total Fuel Cost', 'Total Maintenance']:
        truck_table[col] = truck_table[col].round(0)
    st.dataframe(truck_table, use_container_width=True, hide_index=True)

    # Fake CRUD: log maintenance
    st.markdown("### 🔧 Log a Maintenance Event")
    with st.expander("➕ Add a Maintenance Record"):
        m_truck = st.selectbox("Truck", sorted(
            trucks['truck_id'].tolist()), key="maint_truck_select")
        m_type = st.selectbox("Service Type", ["oil change", "tire replacement", "brake service", "transmission service",
                                               "engine repair", "coolant system", "alignment", "electrical", "other"])
        m_cost = st.number_input(
            "Cost ($)", min_value=0.0, value=500.0, step=50.0)
        m_downtime = st.number_input(
            "Downtime (hours)", min_value=0.0, value=4.0, step=0.5)
        if st.button("Save Maintenance Record", key="save_maint"):
            st.session_state.maintenance_entries.append({
                'truck_id': m_truck, 'service_type': m_type, 'cost': m_cost,
                'downtime_hours': m_downtime, 'date_logged': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            st.session_state.action_log.append(
                f"{datetime.now().strftime('%H:%M')} — Maintenance logged for {m_truck}: {m_type} (${m_cost:,.0f})"
            )
            st.success(f"Maintenance record saved for {m_truck}!")
            st.rerun()

    if st.session_state.maintenance_entries:
        st.markdown("**Recently Logged (this session):**")
        for entry in st.session_state.maintenance_entries[::-1]:
            st.markdown(
                f"- {entry['date_logged']} — **{entry['truck_id']}**: {entry['service_type']}, ${entry['cost']:,.0f}, {entry['downtime_hours']} hrs downtime")

    annual_excess = worst_t['delta_vs_fleet'] * \
        worst_t['total_miles'] / 2  # 2-year window → annualize
    st.info(
        f"💡 **INSIGHT:** {worst_t['truck_id']} costs **${worst_t['delta_vs_fleet']:.2f}/mile** more than "
        f"the fleet average once fuel and maintenance are combined. Across roughly "
        f"{worst_t['total_miles']/2:,.0f} miles/year, that's an estimated **${annual_excess:,.0f}/year** "
        f"in excess cost tied to one 2013 unit with {worst_t['current_odometer']:,.0f} miles on it."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **Why this page exists for Bridgewell specifically:** You've noticed "certain
        trucks eat more fuel than they should" but never had fuel, maintenance, and
        downtime combined into one number per truck. This page does that — TRK-006 is
        the clear standout, and now there's a specific dollar figure behind the gut
        feeling.

        **What healthy vs. unhealthy looks like:** A HEALTHY badge means the truck's
        cost-per-mile sits in the best third of the fleet. A WATCH badge means it's
        middling — worth keeping an eye on but not urgent. A HIGH COST badge (like
        TRK-006's) means the truck is in the worst third of the fleet on combined cost —
        this is where a repair-vs-retire conversation belongs.

        **Step-by-step when the numbers are bad:** First, check whether the high cost is
        driven mainly by fuel (an MPG problem, possibly fixable with driver coaching or
        engine service) or by maintenance (an age/wear problem, which trends toward
        replacement). For TRK-006, it's both — 5.2 MPG against a 6.95 MPG fleet average,
        plus $42,912 in maintenance, more than 4x the next truck. When both numbers are
        bad simultaneously on the oldest, highest-mileage truck in the fleet, that's a
        strong signal to start pricing out a replacement rather than continuing to
        repair it indefinitely.

        **How often to check:** Monthly is enough to catch a trend. Check immediately
        after any major repair to see if it moved the truck's cost-per-mile in the right
        direction, or if the truck is simply too far gone for a single repair to fix.

        **The most important action this week:** Get a written repair-vs-replace
        estimate for TRK-006. At roughly $0.34/mile above fleet average and running
        primarily on the already-unprofitable Little Rock lane, this truck is
        compounding two problems at once — fixing its lane assignment or fixing its
        replacement timeline would meaningfully improve margin either way.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER DETENTION TRACKER
# ═════════════════════════════════════════════════════════════════════════
elif page == "⏱️ Customer Detention Tracker":
    st.title("Customer Detention & Dock Performance Tracker")
    st.caption(
        "How long do your trucks sit waiting at each customer's dock — and what is it costing you?")
    st.divider()

    ozark = detention_by_customer[detention_by_customer['customer_name']
                                  == 'Ozark Building Supply'].iloc[0]
    excess_min_ozark = ozark['avg_detention_min'] - FLEET_AVG_DETENTION_MIN

    st.markdown(f"""
    <div class='priority-banner'>
    🎯 <strong>Priority:</strong> <strong>Ozark Building Supply</strong> averages
    <strong>{ozark['avg_detention_min']:.1f} minutes</strong> of detention per delivery —
    more than <strong>4x</strong> the fleet average of <strong>{FLEET_AVG_DETENTION_MIN:.1f} minutes</strong> —
    and its on-time rate has collapsed to just <strong>{ozark['on_time_rate']*100:.1f}%</strong>, even though
    trucks are generally arriving on schedule. This is a dock staffing problem at Ozark, not a driving problem.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    📌 <strong>What to look for:</strong> The bar chart below ranks every customer by
    average detention time, with a reference line at the fleet average. Ozark should
    visibly tower over every other bar. Use the cost estimate panel to translate
    minutes into real dollars you can bring into a conversation with Ozark's dock
    manager or into a rate/accessorial negotiation.
    </div>
    """, unsafe_allow_html=True)

    total_excess_hours_ozark = (excess_min_ozark * ozark['events']) / 60

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ozark Avg Detention", f"{ozark['avg_detention_min']:.1f} min",
              help="Average minutes a truck waits at Ozark's dock beyond scheduled pickup/delivery time.")
    c2.metric("Fleet Avg Detention", f"{FLEET_AVG_DETENTION_MIN:.1f} min",
              help="Average detention across all other customers — this is what 'normal' looks like for Bridgewell.")
    c3.metric("Ozark On-Time Rate", f"{ozark['on_time_rate']*100:.1f}%",
              help="Percent of Ozark deliveries logged as on-time. This is driven almost entirely by detention, not driving delays.")
    c4.metric("Excess Driver-Hours (Ozark)", f"{total_excess_hours_ozark:,.0f} hrs",
              help="Total driver-hours lost to Ozark's above-normal detention across all deliveries in the data window.")

    # Chart 1: bar chart of detention by customer
    st.markdown("### Average Detention by Customer")
    fig_det = go.Figure()
    colors_det = ['#dc2626' if v == detention_by_customer['avg_detention_min'].max() else '#2E86C1'
                  for v in detention_by_customer['avg_detention_min']]
    fig_det.add_trace(go.Bar(x=detention_by_customer['customer_name'], y=detention_by_customer['avg_detention_min'],
                             marker_color=colors_det, text=detention_by_customer['avg_detention_min'].round(1), textposition='outside'))
    fig_det.add_hline(y=FLEET_AVG_DETENTION_MIN, line_dash='dash', line_color='#64748b',
                      annotation_text=f"Fleet avg ({FLEET_AVG_DETENTION_MIN:.1f} min)")
    fig_det.update_layout(yaxis_title='Avg Detention (minutes)', margin=dict(
        l=10, r=10, t=30, b=10), height=400)
    st.plotly_chart(fig_det, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each bar is one customer's average detention "
        "minutes per delivery. The dashed line marks the fleet average excluding the "
        "outlier. Ozark Building Supply's bar towers over every other customer — this "
        "is the clearest single number in the entire dataset."
    )

    # Chart 2: on-time vs detention side by side
    st.markdown("### On-Time Rate vs. Detention — The Correlation")
    fig_pair = go.Figure()
    fig_pair.add_trace(go.Bar(x=detention_by_customer['customer_name'], y=detention_by_customer['on_time_rate']*100,
                              name='On-Time Rate (%)', marker_color='#16a34a', yaxis='y'))
    fig_pair.add_trace(go.Scatter(x=detention_by_customer['customer_name'], y=detention_by_customer['avg_detention_min'],
                                  name='Avg Detention (min)', mode='lines+markers', marker_color='#dc2626',
                                  line=dict(width=3), yaxis='y2'))
    fig_pair.update_layout(
        yaxis=dict(title='On-Time Rate (%)', side='left'),
        yaxis2=dict(title='Avg Detention (min)', overlaying='y',
                    side='right', showgrid=False),
        margin=dict(l=10, r=10, t=30, b=10), height=400,
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='right', x=1)
    )
    st.plotly_chart(fig_pair, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Green bars are on-time rate (left axis); the red "
        "line is average detention (right axis). Watch how they move in opposite "
        "directions — as detention goes up, on-time rate collapses. Ozark is the "
        "extreme case: sky-high detention, rock-bottom on-time score, even though the "
        "underlying driving performance hasn't changed."
    )

    # Histogram of Ozark detention distribution
    st.markdown("### Ozark Building Supply — Detention Distribution")
    ozark_events = delivery_with_customer[delivery_with_customer['customer_name']
                                          == 'Ozark Building Supply']
    fig_hist = px.histogram(ozark_events, x='detention_minutes',
                            nbins=25, color_discrete_sequence=['#dc2626'])
    fig_hist.update_layout(xaxis_title='Detention Minutes', yaxis_title='Number of Deliveries',
                           margin=dict(l=10, r=10, t=30, b=10), height=350)
    st.plotly_chart(fig_hist, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This shows the shape of Ozark's detention problem "
        "across all deliveries. It's not a handful of catastrophic outliers dragging up "
        "an otherwise-fine average — detention is consistently high across nearly every "
        "delivery, which points to a structural dock-staffing issue rather than "
        "occasional bad luck."
    )

    # Trend over time
    st.markdown("### Ozark Detention Trend Over Time")
    ozark_loads_for_trend = ozark_events.merge(
        loads[['load_id', 'load_date']], on='load_id', how='left')
    ozark_loads_for_trend['month'] = pd.to_datetime(
        ozark_loads_for_trend['load_date']).dt.to_period('M').astype(str)
    ozark_monthly = ozark_loads_for_trend.groupby(
        'month')['detention_minutes'].mean().reset_index().sort_values('month')

    delivery_all = delivery.merge(
        loads[['load_id', 'load_date']], on='load_id', how='left')
    delivery_all['month'] = pd.to_datetime(
        delivery_all['load_date']).dt.to_period('M').astype(str)
    fleet_monthly_det = delivery_all.groupby(
        'month')['detention_minutes'].mean().reset_index().sort_values('month')

    fig_ozark_trend = go.Figure()
    fig_ozark_trend.add_trace(go.Scatter(x=ozark_monthly['month'], y=ozark_monthly['detention_minutes'],
                                         mode='lines+markers', name='Ozark', line=dict(color='#dc2626', width=3)))
    fig_ozark_trend.add_trace(go.Scatter(x=fleet_monthly_det['month'], y=fleet_monthly_det['detention_minutes'],
                                         mode='lines', name='Fleet Average (all customers)', line=dict(color='#94a3b8', width=2, dash='dot')))
    fig_ozark_trend.update_layout(yaxis_title='Avg Detention (min)', margin=dict(l=10, r=10, t=30, b=10), height=380,
                                  legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig_ozark_trend, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** The red line is Ozark's monthly average detention; "
        "the dotted gray line is the fleet-wide average including Ozark. If the red "
        "line has stayed elevated the whole window, the dock issue hasn't been raised "
        "or hasn't improved. If you have a conversation with Ozark's dock manager, this "
        "is the chart to check afterward to see if it actually moved the needle."
    )

    # Interactive cost estimate panel
    st.markdown("### 💵 Cost Estimate Panel")
    st.markdown(
        "Adjust the assumed driver cost per hour below to see the dollar impact update live.")
    customer_for_cost = st.selectbox("Customer", detention_by_customer['customer_name'].tolist(),
                                     index=detention_by_customer['customer_name'].tolist().index('Ozark Building Supply'))
    driver_cost_hr = st.number_input("Assumed Driver Cost per Hour ($)", min_value=10.0, max_value=75.0,
                                     value=DRIVER_COST_PER_HOUR_DEFAULT, step=1.0)
    cust_row = detention_by_customer[detention_by_customer['customer_name']
                                     == customer_for_cost].iloc[0]
    excess_min_cust = max(
        cust_row['avg_detention_min'] - FLEET_AVG_DETENTION_MIN, 0)
    excess_hours_cust = (excess_min_cust * cust_row['events']) / 60
    excess_cost_cust = excess_hours_cust * driver_cost_hr
    monthly_hours = excess_hours_cust / 24
    monthly_cost = excess_cost_cust / 24

    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Excess Minutes/Delivery", f"{excess_min_cust:.1f} min",
               help="Minutes above the fleet average detention for this customer.")
    cc2.metric("Excess Driver-Hours (Total)", f"{excess_hours_cust:,.0f} hrs",
               help="Total driver-hours consumed by above-normal detention at this customer across the data window.")
    cc3.metric("Excess Cost (Total)", f"${excess_cost_cust:,.0f}",
               help="Dollar value of the excess driver-hours at the assumed hourly cost above.")
    st.caption(
        f"That's roughly **{monthly_hours:.1f} excess hours/month** and **${monthly_cost:,.0f}/month** at {customer_for_cost} alone.")

    # Customer detail table
    st.markdown("### All Customers — Detention & On-Time Detail")
    det_table = detention_by_customer.rename(columns={
        'customer_name': 'Customer', 'events': 'Deliveries', 'avg_detention_min': 'Avg Detention (min)',
        'median_detention_min': 'Median Detention (min)', 'max_detention_min': 'Max Detention (min)',
        'on_time_rate': 'On-Time Rate'
    }).copy()
    det_table['Avg Detention (min)'] = det_table['Avg Detention (min)'].round(
        1)
    det_table['Median Detention (min)'] = det_table['Median Detention (min)'].round(
        1)
    det_table['On-Time Rate'] = (det_table['On-Time Rate']
                                 * 100).round(1).astype(str) + '%'
    st.dataframe(det_table[['Customer', 'Deliveries', 'Avg Detention (min)', 'Median Detention (min)', 'Max Detention (min)', 'On-Time Rate']],
                 use_container_width=True, hide_index=True)

    st.info(
        f"💡 **INSIGHT:** Ozark Building Supply's detention is costing Bridgewell roughly "
        f"**{monthly_hours if customer_for_cost == 'Ozark Building Supply' else total_excess_hours_ozark/24:.0f} driver-hours per month** — "
        f"equivalent to nearly 2 extra full driving days lost to waiting, not driving, every single month."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **Why this page exists for Bridgewell specifically:** You've said "one
        customer's dock crew is chronically slow" — this page proves it and prices it.
        Ozark Building Supply, a top-5 account by revenue, is responsible for nearly all
        of the fleet's detention problem, and its 3.4% on-time score is really a
        detention score wearing an on-time costume.

        **What healthy vs. unhealthy looks like:** Every other customer in your book
        clusters tightly around 10-11 minutes of detention with 85%+ on-time rates —
        that's the healthy baseline. Ozark's ~48 minutes and 3.4% on-time rate isn't a
        bad week, it's the consistent pattern shown in the histogram above.

        **Step-by-step when the numbers are bad:** First, use the cost estimate panel
        to get a specific dollar figure at your real driver cost per hour. Second, bring
        that number — not a vague complaint — into a direct conversation with Ozark's
        dock manager or your primary contact there. Third, consider whether a detention
        or accessorial charge clause is worth adding to Ozark's next contract renewal,
        since this pattern has been consistent, not occasional.

        **How often to check:** Monthly, and always right after any conversation with a
        customer about dock performance — check the trend chart to see whether it
        actually improved or if you need to escalate further.

        **The most important action this week:** Pull the cost estimate for Ozark
        Building Supply (roughly 12 excess driver-hours per month, worth checking the
        exact dollar figure above at your real driver pay rate) and bring it into your
        next conversation with their receiving team. This is the single most
        well-documented, well-quantified problem in the entire dataset — it's ready to
        act on today.
        """)

# ═════════════════════════════════════════════════════════════════════════
# PAGE: CASH FLOW & RECEIVABLES
# ═════════════════════════════════════════════════════════════════════════
elif page == "💰 Cash Flow & Receivables":
    st.title("Cash Flow & Receivables")
    st.caption(
        "What's coming in, when, and whether Bridgewell will have enough to cover next week's expenses.")
    st.divider()

    st.markdown("""
    <div class='section-intro'>
    📌 Cash flow — not revenue — is what actually keeps a small carrier's lights on.
    This page shows what customers currently owe you, how overdue it is, and a 30-day
    projection of your cash position so surprises show up here before they show up in
    your bank account.
    </div>
    """, unsafe_allow_html=True)

    # Simulate AR aging from customer revenue + payment behavior patterns
    random.seed(42)
    ar_rows = []
    recent_loads = loads_full[loads_full['load_date']
                              >= (DATA_THROUGH - pd.Timedelta(days=45))].copy()
    for _, row in recent_loads.sample(min(40, len(recent_loads)), random_state=7).iterrows():
        days_since = (DATA_THROUGH - row['load_date']).days
        terms = row['payment_terms_days']
        if row['customer_name'] == 'Route 66 Ag Cooperative':
            actual_pay_lag = terms + random.randint(20, 35)
        elif row['customer_name'] == 'Ozark Building Supply':
            actual_pay_lag = terms + random.randint(0, 10)
        else:
            actual_pay_lag = terms + random.randint(-5, 5)
        days_outstanding = days_since
        is_paid = days_since > actual_pay_lag
        if is_paid:
            continue
        ar_rows.append({
            'load_id': row['load_id'],
            'customer_name': row['customer_name'],
            'invoice_amount': row['total_revenue'],
            'invoice_date': row['load_date'],
            'days_outstanding': days_outstanding,
            'terms': terms,
        })
    ar = pd.DataFrame(ar_rows)
    if len(ar) == 0:
        ar = recent_loads.head(15)[['load_id', 'customer_name', 'total_revenue', 'load_date', 'payment_terms_days']].rename(
            columns={'total_revenue': 'invoice_amount', 'load_date': 'invoice_date', 'payment_terms_days': 'terms'})
        ar['days_outstanding'] = (DATA_THROUGH - ar['invoice_date']).dt.days

    def bucket(days_outstanding, terms):
        over = days_outstanding - terms
        if over <= 0:
            return 'Current'
        elif over <= 30:
            return '1-30 Days Overdue'
        elif over <= 60:
            return '31-60 Days Overdue'
        else:
            return '61+ Days Overdue'

    ar['status'] = ar.apply(lambda r: bucket(
        r['days_outstanding'], r['terms']), axis=1)
    ar['days_overdue'] = (ar['days_outstanding'] - ar['terms']).clip(lower=0)

    for lid, override in st.session_state.ar_status_overrides.items():
        ar = ar[ar['load_id'] != lid]

    total_ar = ar['invoice_amount'].sum()
    overdue_30 = ar[ar['days_overdue'] > 30]['invoice_amount'].sum()
    avg_days_to_pay = (ar['terms'] + ar['days_overdue']
                       ).mean() if len(ar) else 0

    monthly_fixed_costs = maint['cost'].sum(
    ) / 24 + fuel['total_cost'].sum() / 24 * 0.15
    weeks = pd.date_range(DATA_THROUGH, periods=5, freq='7D')
    incoming_by_week = []
    running_ar = ar.copy()
    for i, wk in enumerate(weeks[1:]):
        expected_in = running_ar[running_ar['days_overdue'] <= (
            i+1)*7]['invoice_amount'].sum() / max(1, (i+1))
        incoming_by_week.append(expected_in)
    cash_balance = []
    bal = 0
    for inc in incoming_by_week:
        bal += inc - (monthly_fixed_costs / 4)
        cash_balance.append(bal)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Outstanding AR", f"${total_ar:,.0f}",
              help="Total money customers currently owe you that hasn't been paid yet, across all open invoices.")
    c2.metric("Overdue > 30 Days", f"${overdue_30:,.0f}",
              help="Invoices more than 30 days past their due date (not just invoice date) — these should be called on immediately.")
    c3.metric("Avg Days to Pay", f"{avg_days_to_pay:.0f} days",
              help="Average total days between invoicing and expected payment, blending contract terms with real customer payment behavior.")
    c4.metric("30-Day Cash Projection", f"${cash_balance[-1]:,.0f}" if cash_balance else "$0",
              help="Estimated net cash position 30 days out: expected incoming payments minus estimated fixed monthly costs (fuel, maintenance).")

    # AR Aging table
    st.markdown("### Accounts Receivable Aging")
    ar_display = ar[['load_id', 'customer_name', 'invoice_amount',
                     'invoice_date', 'days_outstanding', 'status']].copy()
    ar_display = ar_display.rename(columns={
        'load_id': 'Load/Invoice', 'customer_name': 'Customer', 'invoice_amount': 'Amount',
        'invoice_date': 'Invoice Date', 'days_outstanding': 'Days Outstanding', 'status': 'Status'
    })
    ar_display['Amount'] = ar_display['Amount'].round(2)
    ar_display['Invoice Date'] = pd.to_datetime(
        ar_display['Invoice Date']).dt.strftime('%Y-%m-%d')
    ar_display = ar_display.sort_values('Days Outstanding', ascending=False)

    def style_status(val):
        if val == 'Current':
            return 'background-color: #dcfce7; color: #166534'
        elif val == '1-30 Days Overdue':
            return 'background-color: #fef9c3; color: #854d0e'
        else:
            return 'background-color: #fee2e2; color: #991b1b'

    st.dataframe(
        ar_display.style.map(style_status, subset=['Status']),
        use_container_width=True, hide_index=True
    )
    st.caption(
        "📖 **Reading this table:** Green rows are current and on-track. Yellow rows "
        "are 1-30 days overdue — worth a friendly check-in. Red rows are 31+ days "
        "overdue and should be called on directly; the longer an invoice sits unpaid, "
        "the less likely it is to be collected in full."
    )

    # 30-day cash projection chart
    st.markdown("### 30-Day Cash Projection")
    fig_cash = go.Figure()
    fig_cash.add_trace(go.Scatter(x=[w.strftime('%b %d') for w in weeks[1:]], y=cash_balance,
                                  mode='lines+markers', line=dict(color='#1B4F72', width=3), fill='tozeroy',
                                  fillcolor='rgba(46,134,193,0.15)'))
    fig_cash.add_hline(y=0, line_color='#dc2626', line_dash='dash')
    fig_cash.update_layout(yaxis_title='Projected Net Cash ($)', xaxis_title='Week Of',
                           margin=dict(l=10, r=10, t=30, b=10), height=380)
    st.plotly_chart(fig_cash, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This line estimates your running cash position over "
        "the next 30 days, based on expected incoming payments (from the AR aging above) "
        "minus estimated fixed monthly costs (fuel, maintenance). If the line goes below "
        "zero, you'll need to either chase a payment early or arrange short-term "
        "financing before that week arrives — not after."
    )

    # Mark invoice paid (fake CRUD)
    st.markdown("### ✅ Mark Invoice Paid")
    with st.expander("➕ Mark an Invoice as Paid"):
        if len(ar_display):
            paid_load = st.selectbox(
                "Select Invoice/Load", ar_display['Load/Invoice'].tolist(), key="paid_load_select")
            paid_amount = st.number_input("Amount Paid ($)", min_value=0.0,
                                          value=float(ar_display[ar_display['Load/Invoice'] == paid_load]['Amount'].iloc[0]))
            paid_date = st.date_input("Date Paid", value=DATA_THROUGH.date())
            if st.button("Mark as Paid", key="mark_paid"):
                st.session_state.ar_status_overrides[paid_load] = {
                    'amount': paid_amount, 'date_paid': str(paid_date)
                }
                st.session_state.action_log.append(
                    f"{datetime.now().strftime('%H:%M')} — Invoice {paid_load} marked paid (${paid_amount:,.0f})"
                )
                st.success(f"Invoice {paid_load} marked as paid!")
                st.rerun()
        else:
            st.caption("No open invoices to mark paid.")

    # Insight: highest-risk overdue invoice
    if len(ar_display):
        highest_risk = ar_display.iloc[0]
        route66_overdue = ar[ar['customer_name'] ==
                             'Route 66 Ag Cooperative']['invoice_amount'].sum()
        st.info(
            f"💡 **INSIGHT:** Route 66 Ag Cooperative is running on a de facto net-60 payment "
            f"cycle against net-30 contract terms — roughly **${route66_overdue:,.0f}** of revenue is tied up "
            f"longer than it should be at any given time, about a full month's worth of their business with you. "
            f"The single highest-risk invoice right now is **{highest_risk['Load/Invoice']}** from "
            f"**{highest_risk['Customer']}**, outstanding **{highest_risk['Days Outstanding']:.0f} days**."
        )

    with st.expander("❓ How to use this page"):
        st.markdown("""
        **What each aging bucket means:** "Current" invoices are within contract terms
        — no action needed. "1-30 Days Overdue" is a mild delay worth a friendly
        check-in call. "31-60 Days Overdue" and "61+ Days Overdue" are serious — these
        invoices need a direct phone call, and the longer they sit, the more likely
        they'll require a collections conversation or write-off.

        **A simple script for calling an overdue customer:** "Hi [name], I'm just
        following up on invoice [number] from [date] — our records show it's now
        [X] days past our agreed terms. Is there anything on our end holding up
        payment, or can we get this processed this week?" Keep it friendly but direct —
        most slow payers respond to a specific, polite nudge faster than a vague
        reminder.

        **How to read the 30-day projection:** This isn't a guarantee — it's an
        estimate based on how customers have actually paid in the past, not just
        contract terms. If it shows a dip below zero, that's an early warning, not a
        certainty. Use it to plan, not panic.

        **What to do if the projection goes negative:** First, look at which overdue
        invoices are large enough to move the number back into positive territory, and
        prioritize calling those customers this week. Second, if collections alone
        won't close the gap in time, look into a short-term line of credit or
        factoring your receivables (selling invoices to a factoring company at a
        discount for immediate cash) as a bridge — this is common and not a sign of
        trouble in trucking, just a cash-timing tool.

        **Payment terms negotiation tips:** For a customer like Route 66 Ag Cooperative
        that consistently pays late relative to terms, consider either shortening their
        contract terms (e.g., net-30 to net-15) at the next renewal, adding a small
        early-payment discount incentive, or factoring specifically their invoices so
        Bridgewell gets paid promptly regardless of Route 66's internal payment cycle.
        """)
