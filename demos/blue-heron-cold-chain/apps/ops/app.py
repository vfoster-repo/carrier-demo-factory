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
COMPANY_NAME = "Blue Heron Cold Chain"
OWNER_FIRST_NAME = "Marcus"
CONTACT_EMAIL = "victorfoster@hotmail.com"

# Colors (validated palette — blue for "good"/TRK-02/southbound, red for TRK-01/northbound/problem)
COLOR_BLUE = "#2a78d6"
COLOR_RED = "#e34948"
COLOR_AQUA = "#1baf7a"
COLOR_YELLOW = "#eda100"
COLOR_VIOLET = "#4a3aa7"
COLOR_GOOD = "#0ca30c"
COLOR_WARNING = "#fab219"
COLOR_CRITICAL = "#d03b3b"
COLOR_MUTED = "#898781"

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG + CSS
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Blue Heron Cold Chain — Operations",
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
delivery_events = data['delivery_events']
drivers = data['drivers']
fuel_purchases = data['fuel_purchases']
loads = data['loads']
maintenance_records = data['maintenance_records']
routes = data['routes']
trips = data['trips']
trucks = data['trucks']

# ═══════════════════════════════════════════════════════════════════════════
# MASTER JOINED DATASET (built once, reused across pages)
# ═══════════════════════════════════════════════════════════════════════════


@st.cache_data
def build_master(trips, loads, fuel_purchases, routes, customers, delivery_events):
    fuel_by_trip = fuel_purchases.groupby(
        'trip_id')['total_cost'].sum().reset_index()
    fuel_by_trip.columns = ['trip_id', 'fuel_cost']

    m = trips.merge(fuel_by_trip, on='trip_id', how='left')
    m = m.merge(loads[['load_id', 'customer_id', 'route_id', 'load_date', 'freight_type',
                       'revenue', 'fuel_surcharge']], on='load_id', how='left')
    m = m.merge(routes[['route_id', 'origin_city', 'origin_state', 'destination_city',
                        'destination_state', 'distance_miles', 'base_rate_per_mile']],
                on='route_id', how='left')
    m = m.merge(customers[['customer_id', 'customer_name', 'payment_terms_days']],
                on='customer_id', how='left')

    m['direction'] = m['origin_state'].apply(
        lambda x: 'Southbound' if x == 'WA' else 'Northbound Backhaul')
    m['gross_revenue'] = m['revenue'] + m['fuel_surcharge']
    m['rev_per_mile'] = m['gross_revenue'] / m['actual_miles']
    m['fuel_cost_per_mile'] = m['fuel_cost'] / m['actual_miles']
    m['net_margin_per_mile'] = m['rev_per_mile'] - m['fuel_cost_per_mile']
    m['net_margin_total'] = m['net_margin_per_mile'] * m['actual_miles']
    m['departure_time'] = pd.to_datetime(m['departure_time'])
    m['load_date'] = pd.to_datetime(m['load_date'])
    m['month'] = m['departure_time'].dt.to_period('M').astype(str)
    m['is_on_time'] = m['on_time_flag'] == 'Y'

    # attach detention (aggregate at delivery event level, one row per load/trip typically)
    det = delivery_events.groupby('load_id').agg(
        detention_minutes=('detention_minutes', 'sum'),
        on_time_delivery=('on_time', lambda x: (x == 'Y').mean())
    ).reset_index()
    m = m.merge(det, on='load_id', how='left')

    return m


master = build_master(trips, loads, fuel_purchases,
                      routes, customers, delivery_events)

# truck display names
TRUCK_LABEL = {
    'TRK-01': 'TRK-01 (Marcus — 2016 Freightliner Cascadia)',
    'TRK-02': 'TRK-02 (Renata — 2021 Kenworth T680)'
}
TRUCK_SHORT = {'TRK-01': "TRK-01 (Marcus)", 'TRK-02': "TRK-02 (Renata)"}

# ═══════════════════════════════════════════════════════════════════════════
# PRECOMPUTED FLEET STATS (used across dashboard + sidebar)
# ═══════════════════════════════════════════════════════════════════════════
data_through_date = master['departure_time'].max().strftime('%B %d, %Y')
n_trucks = trucks['truck_id'].nunique()

current_month_period = master['departure_time'].max().to_period('M')
loads_mtd = master[master['month'] == str(
    current_month_period)]['load_id'].nunique()
on_time_pct = master['is_on_time'].mean() * 100

mpg_by_truck = trips.groupby('truck_id')['actual_mpg'].mean()
fuel_cost_per_mile_by_truck = master.groupby('truck_id').apply(
    lambda g: g['fuel_cost'].sum() / g['actual_miles'].sum()
)
maint_by_truck = maintenance_records.groupby('truck_id').agg(
    total_cost=('cost', 'sum'), avg_cost=('cost', 'mean'),
    events=('cost', 'count'), total_downtime=('downtime_hours', 'sum'),
    avg_downtime=('downtime_hours', 'mean')
)

# customer detention leaderboard
det_by_customer = delivery_events.merge(
    loads[['load_id', 'customer_id']], on='load_id', how='left'
).merge(
    customers[['customer_id', 'customer_name']], on='customer_id', how='left'
).groupby('customer_name').agg(
    events=('event_id', 'count'),
    avg_detention=('detention_minutes', 'mean'),
    total_hours=('detention_minutes', lambda x: x.sum() / 60),
    on_time_rate=('on_time', lambda x: (x == 'Y').mean() * 100)
).reset_index().sort_values('avg_detention', ascending=False)

GG_NAME = "Golden Gate Fresh Distributors"
gg_row = det_by_customer[det_by_customer['customer_name'] == GG_NAME].iloc[0]

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
         "🚛 Truck Cost & Fuel Command Center",
         "🗺️ Lane & Backhaul Profitability",
         "⏱️ Golden Gate Detention Tracker",
         "💰 Cash Flow & Receivables"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"**Fleet:** {n_trucks} trucks")
    st.markdown(f"**Loads this month:** {loads_mtd}")
    st.markdown(f"**On-time rate:** {on_time_pct:.0f}%")
    st.divider()
    st.caption(f"Data through {data_through_date}")
    st.markdown(f"[📧 Get Help](mailto:{CONTACT_EMAIL})")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: GETTING STARTED
# ═══════════════════════════════════════════════════════════════════════════
if page == "🏠 Getting Started":
    st.title(f"Welcome, {OWNER_FIRST_NAME}! Here's Your Operations Platform.")

    st.markdown(f"""
This platform was built from Blue Heron Cold Chain's own trip logs, fuel receipts, maintenance
records, and delivery data — **{len(loads):,} loads**, **{len(trips):,} trips**, and
**{len(fuel_purchases):,} fuel purchases** going back to July 2024. Nothing on these pages is a
generic industry benchmark. Every number is calculated from what TRK-01 and TRK-02 actually did,
what Skagit Valley Produce, Bellingham Cold Storage, Cascade Berry Growers, and Golden Gate Fresh
Distributors actually paid and did at the dock, and what diesel actually cost at the pump on the
day you bought it.

You and Renata have been running this business by feel for years — checking the bank balance,
eyeballing the fuel card statement, and trusting your gut about which truck is more expensive to
run. That gut feeling turns out to be right, but "TRK-01 feels expensive" doesn't get you a repair
budget, a trade-in decision, or leverage in a conversation with a customer. This platform turns
that feeling into a number you can act on — and it's built specifically around Blue Heron's
situation: two trucks with a real fuel-efficiency gap, one direction of freight that pays well and
one that barely breaks even, and one customer whose loading dock is quietly costing you thousands
of dollars a year in detention.
""")

    st.info("📱 On your phone? Tap the **>** arrow in the top-left to open the navigation menu.")

    st.markdown("## What This Platform Does For You")
    st.markdown(f"""
**It's not a spreadsheet you have to maintain — it's a live read on the business.** A spreadsheet
only tells you what you remember to type into it. This platform pulls directly from your trip
logs, fuel receipts, and delivery records, so the moment a new load is entered, the numbers here
update automatically. You don't need to reconcile anything or double-check formulas.

**It's built on your real numbers, not industry averages.** When this platform tells you TRK-01
(Marcus's 2016 Freightliner Cascadia, now past 766,000 miles) gets 5.18 MPG against TRK-02's
(Renata's 2021 Kenworth T680) 7.01 MPG, that's not a guess from a fleet-efficiency guide — that's
the actual average across every trip both of you have logged. When it tells you Golden Gate Fresh
Distributors in Oakland holds your trailer 43.8 minutes on average against 9 minutes everywhere
else, that's calculated from 112 real delivery events, not a hunch.

**It surfaces what's costing you money before it becomes a crisis.** The Operations Dashboard
leads with whatever the single most urgent issue is right now — an overdue invoice, a truck cost
spike, a maintenance milestone coming up — so you don't have to hunt for it across five different
records.

**It gives you numbers you can use outside the truck, too.** The detention tracker on the Golden
Gate page is built so you could screenshot it and put it in an email to their traffic manager. The
lane profitability page tells you, in dollars, whether a load-board backhaul offer is worth taking
before you say yes on the phone.
""")

    st.markdown("## Your Pages — What Each One Does")

    st.markdown("""
    <div class='guide-card'>
        <div class='guide-card-title'>📊 Operations Dashboard</div>
        <div class='guide-card-body'>
        Your morning check-in. One page that rolls up the whole business: this month's revenue,
        margin, and load count against last month, a fleet health strip comparing TRK-01 and TRK-02,
        and an alerts panel that flags anything that needs attention today — an overdue invoice, a
        truck's fuel economy sliding, a maintenance milestone coming up, or a load that came in late.
        Open this first, every morning, before you open anything else. If nothing's flagged, you're
        clear to focus on the road. If something is, it tells you exactly what and where to go next.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>📋 Load Board</div>
        <div class='guide-card-body'>
        Every load you've hauled, filterable by date, status, customer, or driver. This is where you
        go when a customer calls asking "did that load deliver on time?" or when you want to see how
        many loads went to Golden Gate Fresh Distributors last quarter. It also shows a detention
        summary by customer, so you can see at a glance which stops are eating into your day, and it
        lets you attach a note to any load — a disputed invoice, a rescheduled delivery, a driver's
        comment about road conditions — so that context doesn't get lost.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>🚛 Truck Cost & Fuel Command Center</div>
        <div class='guide-card-body'>
        The page that finally puts a number on the running argument at the kitchen table. Side-by-side,
        it shows TRK-01's and TRK-02's fuel cost per mile, MPG trend, and maintenance spend — so you can
        see exactly what Marcus's truck is costing versus Renata's, whether the gap is growing, and
        whether it's time to start budgeting for a replacement instead of another repair. Open this
        whenever a big fuel or repair bill comes in, or at least once a month to track the trend.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>🗺️ Lane & Backhaul Profitability</div>
        <div class='guide-card-body'>
        Answers the question "is this load-board backhaul worth taking?" with your own historical
        numbers instead of a gut call. It breaks out every route by direction — southbound loads to
        Portland and the Bay Area versus the northbound backhauls you scrape together off the load
        board — and shows the real margin gap between them. Use this before accepting a marginal
        backhaul, or when you're deciding whether to push a southbound customer for a rate increase to
        offset the empty miles home.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>⏱️ Golden Gate Detention Tracker</div>
        <div class='guide-card-body'>
        Turns the dread you both feel about the Oakland stop into a dollar figure you can put in front
        of Golden Gate's traffic manager. It tracks detention minutes and on-time performance
        specifically for Golden Gate Fresh Distributors against every other customer, with a running
        cost estimate at an hourly rate you control. Open this before any rate renegotiation or
        accessorial conversation with Golden Gate — it's built to be screenshotted and used as leverage.
        </div>
    </div>
    <div class='guide-card'>
        <div class='guide-card-title'>💰 Cash Flow & Receivables</div>
        <div class='guide-card-body'>
        Shows what customers owe you, how overdue it is, and whether you'll have enough cash on hand
        to cover costs over the next month. With payment terms ranging from 15 days (Cascade Berry
        Growers) to 45 days (Golden Gate Fresh Distributors), it's easy to lose track of who's actually
        slow to pay versus who's just on longer contractual terms. Check this weekly — especially
        before a big expense like an insurance payment or a truck repair.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## A Simple Daily Routine (10 Minutes)")
    st.markdown(f"""
You don't need to check every page every day. Here's a routine that takes about 10 minutes and
covers what actually matters for a two-truck operation:

- **Every morning, before the trucks roll:** Open the **Operations Dashboard** and read the
  alert panel. If nothing's flagged, you're done — go drive.
- **Whenever a truck gets back from a run:** Log the trip's fuel receipts as usual, then check the
  **Truck Cost & Fuel Command Center** once a week to see if TRK-01's fuel cost per mile is holding
  steady or climbing. A steady climb over a couple months is your early warning that a repair is
  coming.
- **Whenever a load-board offer comes in for a northbound backhaul:** Open **Lane & Backhaul
  Profitability**, check the current breakeven line, and decide with a number instead of a gut call.
- **Every Friday:** Open **Cash Flow & Receivables** and check whether next week's expected
  incoming payments cover what you owe. If Golden Gate's invoice is creeping past 30 days, that's
  the week to call.
- **Once a quarter, or after a bad week at the Oakland dock:** Open the **Golden Gate Detention
  Tracker**, update the hourly rate if your costs have changed, and screenshot the leverage brief if
  you're heading into a rate conversation with them.
""")

    with st.expander("📖 Glossary — Plain-English Definitions"):
        st.markdown("""
- **RPM (Revenue Per Mile):** Total revenue from a load (including fuel surcharge) divided by the
  miles driven. For Blue Heron's southbound reefer lanes, a healthy RPM is **$2.60–$3.10/mile**.
  Northbound backhauls typically run **$1.55–$1.85/mile** — lower by nature, which is exactly why
  they need to be watched closely.

- **CPM (Cost Per Mile):** What it costs you to drive one mile — usually broken into fuel cost/mile
  and maintenance cost/mile. TRK-02 (Renata) runs about **$0.58/mile** in fuel alone; TRK-01 (Marcus)
  runs closer to **$0.78/mile** — that 20-cent gap is the core of the "TRK-01 problem."

- **Net Margin Per Mile:** RPM minus CPM — what's actually left over after fuel. This is the number
  that matters most when deciding whether a load or lane is worth running. Blue Heron's southbound
  lanes average **$2.37/mile** net margin; northbound backhauls average **just over $1.00/mile**.

- **On-Time Rate:** The percentage of deliveries that arrived at or before the scheduled time.
  Blue Heron's fleet-wide average sits around **85%**. Most individual customers run **82–90%** —
  except Golden Gate Fresh Distributors, which sits at just **4.5%**, a sign the problem is the
  dock, not your drivers.

- **Detention:** Time your truck sits at a dock waiting to be loaded or unloaded beyond what's
  reasonable, during which the driver isn't earning miles. Blue Heron's average across most
  customers is **8–10 minutes** — normal dock friction. Golden Gate averages **43.8 minutes**,
  which is the difference between "normal" and "a problem worth billing for."

- **Deadhead:** Miles driven with an empty trailer, earning no revenue. Northbound backhaul lanes
  are more exposed to this because Blue Heron's core customers don't ship much freight north — the
  return trip has to be pieced together from the load board.

- **DSO (Days Sales Outstanding):** How many days, on average, it takes to actually collect payment
  after a load delivers. Combined with each customer's contractual payment terms (15–45 days), this
  tells you how much cash is tied up in unpaid invoices at any given moment.

- **MPG (Miles Per Gallon):** Fuel efficiency. Blue Heron's fleet target is **6.9 MPG**. TRK-02
  (Renata, 2021 Kenworth) runs **7.01 MPG** — right at target. TRK-01 (Marcus, 2016 Freightliner)
  runs **5.18 MPG** — a 26% gap that shows up directly in the fuel bill every week.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: OPERATIONS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📊 Operations Dashboard":
    st.title("Operations Dashboard")
    st.caption(
        "Your daily check-in — the health of Blue Heron Cold Chain in one page.")
    st.divider()

    # ── Priority banner: find the single most urgent issue ──
    # Compute overdue AR for banner
    ar_temp = master.copy()
    ar_temp['days_outstanding'] = (pd.Timestamp(
        master['departure_time'].max()) - ar_temp['load_date']).dt.days
    ar_overdue = ar_temp[ar_temp['days_outstanding']
                         > ar_temp['payment_terms_days'] + 30]
    gg_detention_hours = gg_row['total_hours']
    gg_cost_est = gg_detention_hours * 65

    banner_msg = (
        f"<strong>Priority this week:</strong> Golden Gate Fresh Distributors has held your trailers "
        f"for <strong>{gg_detention_hours:.0f} hours</strong> of detention across {int(gg_row['events'])} "
        f"deliveries — an estimated <strong>${gg_cost_est:,.0f}</strong> at $65/hr, with an on-time rate "
        f"of just <strong>{gg_row['on_time_rate']:.1f}%</strong>. See the Golden Gate Detention Tracker "
        f"page for the full leverage brief."
    )
    st.markdown(
        f"<div class='priority-banner'>{banner_msg}</div>", unsafe_allow_html=True)

    # ── KPI strip ──
    total_revenue = master['gross_revenue'].sum()
    total_margin = master['net_margin_total'].sum()
    avg_rpm = master['rev_per_mile'].mean()
    fleet_on_time = master['is_on_time'].mean() * 100
    total_loads = master['load_id'].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue (all-time)", f"${total_revenue:,.0f}",
              help="Sum of all load revenue plus fuel surcharge across every trip on record.")
    c2.metric("Net Margin (after fuel)", f"${total_margin:,.0f}",
              help="Revenue minus fuel cost. Doesn't yet subtract maintenance, insurance, or truck "
                   "payments — this is the margin available to cover everything else.")
    c3.metric("Avg Revenue / Mile", f"${avg_rpm:.2f}",
              help="Total revenue divided by miles driven, blended across southbound and northbound "
                   "lanes. Southbound alone runs $2.60-$3.10/mile; a blended average below $2.00 "
                   "usually means too many low-paying backhauls.")
    c4.metric("Fleet On-Time Rate", f"{fleet_on_time:.1f}%",
              help="Percentage of trips that arrived at or before the scheduled time. Blue Heron's "
                   "pitch to customers is reliability — 85%+ is healthy, below 75% is a warning sign.")
    c5.metric("Total Loads Hauled", f"{total_loads:,}",
              help="Every delivered load in the data, both trucks combined, since July 2024.")

    st.markdown("""
    <div class='section-intro'>
    <strong>What to look for:</strong> Check the alert panel below first — it's sorted by urgency.
    Then scan the fleet status table to see if either truck's cost-per-mile has crept up since last
    month. The revenue trend chart tells you whether the business overall is growing or shrinking;
    everything else on this page is about <em>why</em>.
    </div>
    """, unsafe_allow_html=True)

    # ── Revenue trend chart ──
    st.markdown("### Revenue Trend — Last 12 Months")
    monthly = master.groupby('month').agg(
        revenue=('gross_revenue', 'sum'), margin=('net_margin_total', 'sum'), loads=('load_id', 'nunique')
    ).reset_index().sort_values('month').tail(12)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['revenue'], mode='lines+markers', name='Revenue',
        line=dict(color=COLOR_BLUE, width=2), marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=monthly['month'], y=monthly['margin'], mode='lines+markers', name='Net Margin (after fuel)',
        line=dict(color=COLOR_AQUA, width=2), marker=dict(size=8)
    ))
    fig.update_layout(
        height=380, margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='left', x=0),
        yaxis_title="Dollars", xaxis_title=None,
        yaxis=dict(gridcolor='#e1e0d9'), xaxis=dict(gridcolor='#e1e0d9')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each point is one month of total revenue (blue) and what's left "
        "after fuel costs (green). Look for the trend direction — are you growing? Dipping? If a "
        "month looks low, use the Load Board to filter that month and see if loads were down or "
        "rates were low. Expect a seasonal dip November–February as produce and seafood volume drops."
    )

    # ── Fleet status table ──
    st.markdown("### Fleet Status")
    fleet_rows = []
    for _, tr in trucks.iterrows():
        tid = tr['truck_id']
        tm = master[master['truck_id'] == tid]
        this_month = tm[tm['month'] == str(current_month_period)]
        last_maint = maintenance_records[maintenance_records['truck_id'] == tid].sort_values(
            'service_date').tail(1)
        last_maint_date = last_maint['service_date'].values[0] if len(
            last_maint) else "No record"
        cpm_fuel = tm['fuel_cost'].sum(
        ) / tm['actual_miles'].sum() if tm['actual_miles'].sum() else 0
        maint_cpm = maint_by_truck.loc[tid, 'total_cost'] / tm['actual_miles'].sum(
        ) if tid in maint_by_truck.index and tm['actual_miles'].sum() else 0
        fleet_rows.append({
            'Truck': TRUCK_SHORT[tid],
            'Make / Model / Year': f"{tr['make']} {tr['model']} ({tr['year']})",
            'Odometer': f"{tr['current_odometer']:,} mi",
            'Loads (This Month)': this_month['load_id'].nunique(),
            'Fuel Cost / Mile': f"${cpm_fuel:.2f}",
            'Maint Cost / Mile': f"${maint_cpm:.2f}",
            'All-In Cost / Mile': f"${cpm_fuel + maint_cpm:.2f}",
            'Avg MPG': f"{mpg_by_truck.get(tid, 0):.2f}",
            'Last Service': last_maint_date,
            'Status': tr['status'].title()
        })
    fleet_df = pd.DataFrame(fleet_rows)
    st.dataframe(fleet_df, use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** Focus on All-In Cost/Mile — that's fuel plus maintenance combined "
        "per mile driven. A healthy Class 8 diesel reefer tractor runs $0.55-$0.75/mile all-in. "
        "TRK-01 (Marcus) is running noticeably above that band; TRK-02 (Renata) is running within it. "
        "That gap is real money — see the Truck Cost & Fuel Command Center for the full breakdown."
    )

    # ── Alerts panel ──
    st.markdown("### Alerts — What Needs Attention")
    alerts = []

    # Overdue invoices > 30 days past terms
    if len(ar_overdue) > 0:
        worst_overdue = ar_overdue.sort_values('days_outstanding', ascending=False).groupby('customer_name').agg(
            amount=('gross_revenue', 'sum'), max_days=('days_outstanding', 'max')
        ).reset_index().sort_values('max_days', ascending=False)
        for _, row in worst_overdue.head(3).iterrows():
            alerts.append(('🔴', f"**{row['customer_name']}** has invoices **{int(row['max_days'])} days** past "
                           f"terms, totaling an estimated **${row['amount']:,.0f}** outstanding."))

    # MPG drop vs trailing 3-month average, per truck
    for tid in trucks['truck_id']:
        tm = trips[trips['truck_id'] == tid].copy()
        tm['departure_time'] = pd.to_datetime(tm['departure_time'])
        tm = tm.sort_values('departure_time')
        if len(tm) >= 6:
            recent = tm.tail(3)['actual_mpg'].mean()
            trailing = tm.tail(15).head(12)['actual_mpg'].mean() if len(
                tm) >= 15 else tm['actual_mpg'].mean()
            if trailing > 0 and recent < trailing * 0.95:
                pct_drop = (1 - recent / trailing) * 100
                alerts.append(('🟡', f"**{TRUCK_SHORT[tid]}** MPG has dropped **{pct_drop:.1f}%** vs. its "
                               f"trailing average ({recent:.2f} vs {trailing:.2f} MPG) — worth a look "
                               f"at the Truck Cost page."))

    # Late loads in past 7 days of data
    max_date = master['departure_time'].max()
    recent_window = master[master['departure_time']
                           >= max_date - pd.Timedelta(days=7)]
    late_recent = recent_window[recent_window['is_on_time'] == False]
    if len(late_recent) > 0:
        alerts.append(('🟡', f"**{len(late_recent)} load(s)** in the most recent 7 days of data arrived "
                       f"late. Check the Load Board filtered to that date range for details."))

    # Maintenance milestones — trucks approaching 25k/50k/100k mile markers since last service
    for tid in trucks['truck_id']:
        tr = trucks[trucks['truck_id'] == tid].iloc[0]
        last_service = maintenance_records[maintenance_records['truck_id'] == tid].sort_values(
            'service_date').tail(1)
        if len(last_service):
            miles_since = tr['current_odometer'] - \
                last_service['odometer_at_service'].values[0]
            if miles_since > 20000:
                alerts.append(('🟡', f"**{TRUCK_SHORT[tid]}** has run **{miles_since:,.0f} miles** since its "
                               f"last service — approaching the next maintenance interval."))

    # Customers averaging detention > 45 min
    high_detention = det_by_customer[det_by_customer['avg_detention'] > 30]
    for _, row in high_detention.iterrows():
        alerts.append(('🔴', f"**{row['customer_name']}** averages **{row['avg_detention']:.0f} minutes** "
                       f"of detention per stop across {int(row['events'])} deliveries."))

    if not alerts:
        st.success("No urgent alerts right now — the business looks steady.")
    else:
        for icon, msg in alerts[:7]:
            if icon == '🔴':
                st.error(f"{icon} {msg}")
            else:
                st.warning(f"{icon} {msg}")

    # ── Recent activity log ──
    st.markdown("### Recent Activity")
    if st.session_state.action_log:
        for entry in reversed(st.session_state.action_log[-10:]):
            st.markdown(f"- {entry}")
    else:
        st.caption(
            "No notes or actions logged yet this session. Add a note from the Load Board to see it here.")

    with st.expander("❓ How to use this page"):
        st.markdown("""
This dashboard is meant to be the first thing you open every morning, and the only thing you need
to open if nothing's wrong. Here's how to use it well:

**Start with the priority banner.** It always shows the single most urgent issue the platform can
detect from your data — usually the thing costing the most money or posing the biggest risk right
now. If it's an overdue invoice, that's a phone call to make today. If it's a detention or
maintenance issue, that's worth a deeper look on the relevant page.

**Scan the alerts panel next.** Alerts are sorted roughly by severity — red items (🔴) mean money is
actively at risk or overdue; yellow items (🟡) are trends worth watching but not yet urgent. A quiet
alerts panel with zero items is a genuinely good sign — it means nothing in the data crossed a
concerning threshold this week.

**Check the fleet status table if you haven't looked in a while.** The All-In Cost/Mile column is
the fastest way to see whether TRK-01 is still the more expensive truck to run, and whether that gap
is closing or widening. If TRK-01's cost/mile jumps sharply in one month, that's usually tied to a
fuel price spike or a maintenance event — cross-reference with the Truck Cost page.

**Use the revenue trend to sanity-check the season.** Blue Heron's business is seasonal — expect a
real dip from November through February as Skagit Valley produce and Bellingham seafood volumes
drop. A dip in that window isn't a red flag by itself. A dip in July or August, during peak season,
is worth investigating.

**How this connects to other pages:** Every section on this dashboard is a summary of a deeper page
elsewhere in the platform. Fuel and MPG numbers link conceptually to the Truck Cost & Fuel Command
Center. Detention alerts link to the Golden Gate Detention Tracker. Overdue invoice alerts link to
Cash Flow & Receivables. Think of this page as the table of contents, not the whole book — when
something here catches your eye, go to the matching page for the full picture.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LOAD BOARD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "📋 Load Board":
    st.title("Load Board")
    st.caption(
        "Every load Blue Heron Cold Chain has hauled — filter, review, and add notes.")
    st.divider()

    with st.sidebar:
        st.divider()
        st.markdown("**🔍 Load Board Filters**")
        min_date = master['load_date'].min().date()
        max_date = master['load_date'].max().date()
        date_range = st.date_input("Date range", value=(
            min_date, max_date), min_value=min_date, max_value=max_date)
        status_filter = st.multiselect(
            "Status", ["On-Time", "Late"], default=["On-Time", "Late"])
        customer_options = [
            "All"] + sorted(master['customer_name'].dropna().unique().tolist())
        customer_filter = st.selectbox("Customer", customer_options)
        driver_options = ["All"] + \
            sorted(drivers['driver_id'].unique().tolist())
        driver_filter = st.selectbox("Driver", driver_options,
                                     format_func=lambda x: x if x == "All" else
                                     f"{drivers[drivers.driver_id == x]['first_name'].values[0]} ({x})")

    filtered = master.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered = filtered[(filtered['load_date'].dt.date >= date_range[0]) & (
            filtered['load_date'].dt.date <= date_range[1])]
    status_map = {"On-Time": True, "Late": False}
    wanted_bools = [status_map[s]
                    for s in status_filter] if status_filter else [True, False]
    filtered = filtered[filtered['is_on_time'].isin(wanted_bools)]
    if customer_filter != "All":
        filtered = filtered[filtered['customer_name'] == customer_filter]
    if driver_filter != "All":
        filtered = filtered[filtered['driver_id'] == driver_filter]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filtered Loads", f"{len(filtered):,}",
              help="Number of loads matching your current filters.")
    c2.metric("On-Time Rate", f"{filtered['is_on_time'].mean()*100:.1f}%" if len(filtered) else "—",
              help="Share of these loads that arrived at or before the scheduled time.")
    c3.metric("Avg Revenue / Load", f"${filtered['gross_revenue'].mean():,.0f}" if len(filtered) else "—",
              help="Average total revenue (base rate plus fuel surcharge) per load in this filtered set.")
    c4.metric("Total Revenue", f"${filtered['gross_revenue'].sum():,.0f}" if len(filtered) else "—",
              help="Sum of all revenue across the filtered loads.")

    st.markdown(f"""
    <div class='section-intro'>
    Showing <strong>{len(filtered):,} loads</strong> between {date_range[0] if isinstance(date_range, tuple) else min_date}
    and {date_range[1] if isinstance(date_range, tuple) else max_date}
    {f", customer: {customer_filter}" if customer_filter != "All" else ""}
    {f", driver: {driver_filter}" if driver_filter != "All" else ""}.
    Adjust filters in the sidebar to narrow this down.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Load Table")
    display_df = filtered.sort_values(
        'departure_time', ascending=False).head(300).copy()
    display_df['Route'] = display_df['origin_city'] + ", " + display_df['origin_state'] + " → " + \
        display_df['destination_city'] + ", " + display_df['destination_state']
    display_df['Status Badge'] = display_df['is_on_time'].apply(
        lambda x: "<span class='badge-active'>On-Time</span>" if x else "<span class='badge-late'>Late</span>"
    )
    display_df['Driver'] = display_df['driver_id'].map(
        drivers.set_index('driver_id')['first_name'].to_dict()
    )
    show_cols = display_df[['load_id', 'Route', 'customer_name', 'Driver', 'truck_id',
                            'departure_time', 'gross_revenue']].copy()
    show_cols.columns = ['Load ID', 'Route', 'Customer',
                         'Driver', 'Truck', 'Departure', 'Revenue']
    show_cols['Departure'] = show_cols['Departure'].dt.strftime('%Y-%m-%d')
    show_cols['Revenue'] = show_cols['Revenue'].apply(lambda x: f"${x:,.2f}")
    show_cols['Status'] = display_df['is_on_time'].apply(
        lambda x: "On-Time" if x else "Late").values
    st.dataframe(show_cols, use_container_width=True, hide_index=True)
    if len(filtered) > 300:
        st.caption(
            f"Showing the most recent 300 of {len(filtered):,} matching loads. Narrow the date range to see more detail.")

    # ── Customer detention summary ──
    st.markdown("### Customer Detention Summary (Filtered Set)")
    if len(filtered) and filtered['detention_minutes'].notna().any():
        det_summary = filtered.groupby('customer_name').agg(
            avg_detention=('detention_minutes', 'mean'),
            total_hours=('detention_minutes', lambda x: x.sum() / 60),
            over_30=('detention_minutes', lambda x: (x > 30).sum())
        ).reset_index().sort_values('avg_detention', ascending=False)
        det_summary.columns = [
            'Customer', 'Avg Detention (min)', 'Total Detention (hrs)', 'Deliveries >30 min']
        det_summary['Avg Detention (min)'] = det_summary['Avg Detention (min)'].round(
            1)
        det_summary['Total Detention (hrs)'] = det_summary['Total Detention (hrs)'].round(
            1)
        st.dataframe(det_summary, use_container_width=True, hide_index=True)
        st.caption(
            "📖 **What this means:** Detention is time your truck sits at a dock beyond a reasonable "
            "loading/unloading window, earning nothing. Every hour of detention is an hour your driver "
            "isn't running miles. Customers averaging well above 15-20 minutes are worth a "
            "conversation about dock scheduling or an accessorial fee."
        )
    else:
        st.caption("No detention data available for the current filter.")

    # ── Fake CRUD: add note to load ──
    st.markdown("### Add a Note to a Load")
    with st.expander("➕ Add a Note to a Load"):
        note_load_options = filtered['load_id'].tolist() if len(
            filtered) else master['load_id'].tolist()
        note_load = st.selectbox("Select Load", note_load_options)
        note_text = st.text_area("Note", placeholder="e.g. Customer requested rescheduled delivery, "
                                 "invoice disputed, driver reported road delay")
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
        for lid, note_info in reversed(list(st.session_state.load_notes.items())):
            st.markdown(
                f"- **{lid}** ({note_info['timestamp']}): {note_info['note']}")

    # ── Insight callout ──
    if len(det_by_customer):
        top_det = det_by_customer.iloc[0]
        gg_loads_count = int(top_det['events'])
        gg_cost = top_det['total_hours'] * 65
        st.info(
            f"💡 **INSIGHT:** Across {gg_loads_count} deliveries, **{top_det['customer_name']}** "
            f"averages **{top_det['avg_detention']:.1f} minutes** of detention — accounting for "
            f"**{top_det['total_hours']:.0f} total hours**, an estimated **${gg_cost:,.0f}** in unpaid "
            f"driver and truck time at $65/hr. See the Golden Gate Detention Tracker page for the full "
            f"breakdown."
        )

    with st.expander("❓ How to use this page"):
        st.markdown("""
The Load Board is your searchable record of everything Blue Heron has hauled. Use it any time you
need to answer a specific question about a specific load, customer, or time period.

**Using the filters:** The date range, status, customer, and driver filters in the sidebar all work
together — narrowing one narrows the results of the others. Use the status filter to isolate late
deliveries if you want to investigate a pattern, or filter by customer to pull up everything you've
hauled for Golden Gate Fresh Distributors or Cascade Berry Growers in a given quarter.

**Reading the status badges:** "On-Time" means the delivery arrived at or before its scheduled
time. "Late" means it arrived after. This is measured at the trip level — it doesn't yet capture
*why* a load was late (traffic, weather, a hold-up at the dock), which is what the detention summary
below the table is for.

**Why detention matters:** A load can be "on-time" for departure and arrival and still cost you
money if the truck then sits at the dock for 45 minutes before it's unloaded. That's exactly what's
happening with Golden Gate Fresh Distributors. The detention summary breaks this out by customer so
you can see which stops are costing you time that isn't reflected in the on-time percentage alone.

**Using notes:** Notes are for anything that doesn't fit neatly into the data — a disputed invoice,
a customer's special request, a driver's comment about a specific delivery. They're timestamped and
kept with the load record so the context isn't lost by the time you need it again (for example, at
tax time or during a rate negotiation).

**When a load goes late:** Check whether it's a one-off (weather, traffic) or a pattern tied to a
specific customer or route. If it's a pattern, that's worth surfacing on the On-Time / Detention
pages and potentially raising with the customer directly.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: TRUCK COST & FUEL COMMAND CENTER
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🚛 Truck Cost & Fuel Command Center":
    st.title("Truck Cost & Fuel Command Center")
    st.caption(
        "TRK-01 (Marcus) vs. TRK-02 (Renata) — fuel, maintenance, and cost per mile, side by side.")
    st.divider()

    mpg_gap_pct = (1 - mpg_by_truck['TRK-01'] / mpg_by_truck['TRK-02']) * 100
    fuel_cpm_01 = fuel_cost_per_mile_by_truck['TRK-01']
    fuel_cpm_02 = fuel_cost_per_mile_by_truck['TRK-02']

    st.markdown(f"""
    <div class='priority-banner'>
    <strong>The core issue:</strong> TRK-01 (Marcus, 2016 Freightliner Cascadia, {trucks[trucks.truck_id == 'TRK-01']['current_odometer'].values[0]:,} miles)
    averages <strong>{mpg_by_truck['TRK-01']:.2f} MPG</strong> versus TRK-02's (Renata, 2021 Kenworth T680)
    <strong>{mpg_by_truck['TRK-02']:.2f} MPG</strong> — a <strong>{mpg_gap_pct:.0f}% fuel efficiency gap</strong>
    on the same lanes. Maintenance tells the same story: TRK-01 has logged <strong>${maint_by_truck.loc['TRK-01', 'total_cost']:,.0f}</strong>
    across {int(maint_by_truck.loc['TRK-01', 'events'])} service events versus TRK-02's <strong>${maint_by_truck.loc['TRK-02', 'total_cost']:,.0f}</strong>
    across {int(maint_by_truck.loc['TRK-02', 'events'])} events.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    <strong>What to focus on:</strong> The KPI cards below show each truck's all-in cost per mile —
    that's the number that matters most. The charts show whether the gap is a one-time blip or a
    persistent trend. If TRK-01's cost keeps climbing while TRK-02 stays flat, that's the strongest
    signal that TRK-01 is approaching the end of its economical service life.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {TRUCK_SHORT['TRK-01']}")
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Avg MPG", f"{mpg_by_truck['TRK-01']:.2f}",
                   help="Miles per gallon, averaged across all logged trips. Fleet target is 6.9 MPG.")
        cc2.metric("Fuel Cost / Mile", f"${fuel_cpm_01:.2f}",
                   help="Total fuel spend divided by miles driven for this truck.")
        cc3.metric("Maint. Cost / Mile", f"${maint_by_truck.loc['TRK-01', 'total_cost']/master[master.truck_id == 'TRK-01']['actual_miles'].sum():.2f}",
                   help="Total maintenance spend divided by miles driven for this truck.")
    with col2:
        st.markdown(f"#### {TRUCK_SHORT['TRK-02']}")
        cc4, cc5, cc6 = st.columns(3)
        cc4.metric("Avg MPG", f"{mpg_by_truck['TRK-02']:.2f}",
                   help="Miles per gallon, averaged across all logged trips. Fleet target is 6.9 MPG.")
        cc5.metric("Fuel Cost / Mile", f"${fuel_cpm_02:.2f}",
                   help="Total fuel spend divided by miles driven for this truck.")
        cc6.metric("Maint. Cost / Mile", f"${maint_by_truck.loc['TRK-02', 'total_cost']/master[master.truck_id == 'TRK-02']['actual_miles'].sum():.2f}",
                   help="Total maintenance spend divided by miles driven for this truck.")

    # Chart 1: southbound-only MPG bar comparison
    st.markdown(
        "### MPG Comparison — Southbound Loads Only (Controls for Load Weight)")
    southbound_only = master[master['direction'] == 'Southbound']
    sb_mpg = southbound_only.groupby(
        'truck_id')['actual_mpg'].mean().reindex(['TRK-01', 'TRK-02'])
    fig1 = go.Figure(go.Bar(
        x=[TRUCK_SHORT['TRK-01'], TRUCK_SHORT['TRK-02']], y=sb_mpg.values,
        marker_color=[COLOR_RED, COLOR_BLUE], text=[
            f"{v:.2f} MPG" for v in sb_mpg.values],
        textposition='outside'
    ))
    fig1.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       yaxis_title="MPG", yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This isolates southbound loads only, so both trucks are being "
        "compared on the same lanes carrying similar loaded weight. The gap you see here is as close "
        "to an apples-to-apples comparison of the two trucks' mechanical efficiency as this data allows."
    )

    # Chart 2: dual line chart, fuel cost/mile over time per truck
    st.markdown("### Fuel Cost Per Mile — Trend Over Time")
    monthly_fuel = master.groupby(['month', 'truck_id']).apply(
        lambda g: g['fuel_cost'].sum() / g['actual_miles'].sum()
    ).reset_index()
    monthly_fuel.columns = ['month', 'truck_id', 'fuel_cpm']
    monthly_fuel = monthly_fuel.sort_values('month')

    fig2 = go.Figure()
    for tid, color in [('TRK-01', COLOR_RED), ('TRK-02', COLOR_BLUE)]:
        sub = monthly_fuel[monthly_fuel['truck_id'] == tid]
        fig2.add_trace(go.Scatter(x=sub['month'], y=sub['fuel_cpm'], mode='lines+markers',
                                  name=TRUCK_SHORT[tid], line=dict(color=color, width=2)))
    fig2.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       legend=dict(orientation='h', yanchor='bottom',
                                   y=1.02, xanchor='left', x=0),
                       yaxis_title="Fuel Cost / Mile ($)", yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each line is one truck's fuel cost per mile by month. Both lines "
        "move up and down with diesel prices, but TRK-01's line consistently sits above TRK-02's — "
        "that gap, not the up-and-down movement, is the real signal. If the gap between the lines "
        "widens over time, TRK-01's mechanical condition is likely worsening, not just diesel prices rising."
    )

    # Chart 3: maintenance cost by service_type per truck (stacked bar)
    st.markdown("### Maintenance Cost by Service Type")
    maint_by_type = maintenance_records.groupby(['truck_id', 'service_type'])[
        'cost'].sum().reset_index()
    fig3 = px.bar(maint_by_type, x='service_type', y='cost', color='truck_id',
                  color_discrete_map={
                      'TRK-01': COLOR_RED, 'TRK-02': COLOR_BLUE},
                  labels={
                      'cost': 'Total Cost ($)', 'service_type': 'Service Type', 'truck_id': 'Truck'},
                  barmode='group')
    fig3.for_each_trace(lambda t: t.update(
        name=TRUCK_SHORT.get(t.name, t.name)))
    fig3.update_layout(height=400, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       legend=dict(orientation='h', yanchor='bottom',
                                   y=1.02, xanchor='left', x=0),
                       yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Bars grouped by service type show what's driving each truck's "
        "maintenance spend. If TRK-01 shows noticeably higher costs in brakes, tires, or air system "
        "work compared to TRK-02, that's consistent with a truck approaching the end of its "
        "economical service life — those are wear-and-tear systems, not one-off failures."
    )

    # ── Annualized cost-of-keeping callout ──
    st.markdown("### Cost of Keeping TRK-01 — Annualized Estimate")
    avg_miles_per_trip = master[master['truck_id']
                                == 'TRK-01']['actual_miles'].mean()
    fuel_price_recent = fuel_purchases.sort_values(
        'purchase_date')['price_per_gallon'].tail(20).mean()
    fuel_delta_per_mile = fuel_cpm_01 - fuel_cpm_02
    trips_per_year_01 = trips[trips['truck_id'] == 'TRK-01'].shape[0] / \
        max(1, (pd.to_datetime(trips['departure_time']).max(
        ) - pd.to_datetime(trips['departure_time']).min()).days / 365)
    annual_miles_01 = trips_per_year_01 * avg_miles_per_trip
    annual_fuel_delta = fuel_delta_per_mile * annual_miles_01
    maint_delta_annual = (
        maint_by_truck.loc['TRK-01', 'total_cost'] - maint_by_truck.loc['TRK-02', 'total_cost'])

    ann_col1, ann_col2, ann_col3 = st.columns(3)
    ann_col1.metric("Extra Fuel Cost / Year (est.)", f"${annual_fuel_delta:,.0f}",
                    help="TRK-01's higher fuel cost per mile, multiplied by its estimated annual mileage.")
    ann_col2.metric("Maintenance Cost Gap (data period)", f"${maint_delta_annual:,.0f}",
                    help="Total maintenance cost difference between TRK-01 and TRK-02 across the full data period.")
    ann_col3.metric("Combined Est. Annual Penalty", f"${annual_fuel_delta + maint_delta_annual:,.0f}",
                    help="Rough combined estimate of what running TRK-01 costs extra per year versus TRK-02, "
                    "in fuel and maintenance alone — not counting downtime or lost revenue while it's in the shop.")

    st.info(
        f"💡 **INSIGHT:** At current trends, TRK-01 costs an estimated **${annual_fuel_delta:,.0f} more per "
        f"year in fuel alone** than TRK-02, plus **{maint_by_truck.loc['TRK-01', 'total_downtime']:.0f} hours** "
        f"of maintenance downtime (vs. **{maint_by_truck.loc['TRK-02', 'total_downtime']:.0f} hours** for TRK-02) "
        f"— roughly **{maint_by_truck.loc['TRK-01', 'total_downtime']/max(1, maint_by_truck.loc['TRK-02', 'total_downtime']):.1f}x** "
        f"the downtime. That's time TRK-01 isn't earning revenue at all."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
This page exists to answer one question with a number instead of a feeling: **is TRK-01 costing us
enough extra to justify a repair budget, or is it time to think seriously about a replacement?**

**What healthy looks like:** A well-maintained Class 8 diesel reefer tractor should run somewhere
between $0.55 and $0.75 all-in cost per mile (fuel plus maintenance). TRK-02 sits comfortably in
that range. TRK-01 runs above it, and the gap is the direct result of a 10-year-old, 766,000-mile
engine working harder to move the same load as a 2021 truck with 446,000 miles.

**What to do if the numbers look bad:** If TRK-01's fuel cost per mile trend (the middle chart) is
climbing month over month — not just tracking diesel price swings — that's a sign of declining
engine or drivetrain efficiency, not just an expensive month. If the maintenance chart shows brakes,
tires, air system, or transmission costs clustering in recent months, that's consistent with a
truck crossing into its expensive final years of service. Combined with rising downtime hours, that's
the classic signal fleet operators use to start pricing a replacement truck rather than continuing
to repair.

**How often to check:** Once a month is enough to catch a trend — checking after every single fuel
fill-up will just show you noise from diesel price swings, not the real signal.

**The most important action this week:** Based on current data, TRK-01's combined fuel and
maintenance penalty is running well into five figures annually. If you haven't already, it's worth
getting an actual trade-in or financing quote for a comparable used or new reefer tractor so you can
compare a real monthly payment against what TRK-01 is already costing you in fuel and repairs. Even
a rough quote turns this from "it feels expensive" into a real financial decision.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LANE & BACKHAUL PROFITABILITY
# ═══════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Lane & Backhaul Profitability":
    st.title("Lane & Backhaul Profitability")
    st.caption(
        "Southbound loads vs. northbound backhauls — where Blue Heron actually makes money.")
    st.divider()

    sb = master[master['direction'] == 'Southbound']
    nb = master[master['direction'] == 'Northbound Backhaul']
    sb_margin = sb['net_margin_per_mile'].mean()
    nb_margin = nb['net_margin_per_mile'].mean()
    margin_gap_pct = (1 - nb_margin / sb_margin) * 100

    st.markdown(f"""
    <div class='priority-banner'>
    <strong>The core issue:</strong> Northbound backhauls net <strong>${nb_margin:.2f}/mile</strong>
    after fuel versus <strong>${sb_margin:.2f}/mile</strong> southbound — <strong>{margin_gap_pct:.0f}% less</strong>
    per mile. These are the load-board loads you scrape together getting back to Mount Vernon and
    Bellingham, and they're structurally thin-margin freight, not a one-off bad run.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    <strong>What to focus on:</strong> Use the breakeven slider below to test your own assumption for
    what a northbound backhaul needs to net to be "worth it." Then check the route table at the
    bottom — it tells you exactly which specific route is dragging the average down the most.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Southbound Rev/Mile", f"${sb['rev_per_mile'].mean():.2f}",
              help="Average revenue per mile on loads originating in Washington, heading to Portland or the Bay Area.")
    c2.metric("Southbound Net Margin/Mile", f"${sb_margin:.2f}",
              help="Revenue per mile minus fuel cost per mile, southbound only.")
    c3.metric("Northbound Rev/Mile", f"${nb['rev_per_mile'].mean():.2f}",
              help="Average revenue per mile on backhaul loads heading north from Oakland or Portland.")
    c4.metric("Northbound Net Margin/Mile", f"${nb_margin:.2f}",
              help="Revenue per mile minus fuel cost per mile, northbound backhauls only.")

    # breakeven slider
    st.markdown("### Breakeven Threshold Test")
    breakeven = st.slider("Set your northbound backhaul breakeven ($/mile net margin)", 0.50, 2.50, 1.65, 0.05,
                          help="This is a judgment call — the default $1.65/mile reflects a reasonable "
                          "breakeven for a reefer unit running empty-adjacent backhauls. Adjust it "
                          "to match your own cost assumptions.")
    pct_below = (nb['net_margin_per_mile'] < breakeven).mean() * 100
    st.metric(f"% of Northbound Trips Below ${breakeven:.2f}/mile", f"{pct_below:.1f}%",
              help="Share of all northbound backhaul trips that net less than your chosen breakeven "
                   "threshold after fuel cost.")

    annual_nb_trips = len(
        nb) / max(1, (master['departure_time'].max() - master['departure_time'].min()).days / 365)
    annual_gap_dollars = (sb_margin - nb_margin) * \
        nb['actual_miles'].mean() * annual_nb_trips
    st.info(
        f"💡 **INSIGHT:** At roughly **{annual_nb_trips:.0f} northbound backhauls per year** averaging "
        f"**{nb['actual_miles'].mean():.0f} miles**, the southbound-vs-northbound margin gap represents an "
        f"estimated **${annual_gap_dollars:,.0f}/year** in margin left on the table by low-paying backhaul "
        f"freight. **{pct_below:.0f}%** of northbound trips currently fall below your ${breakeven:.2f}/mile "
        f"breakeven line."
    )

    # Chart 1: route bar chart, sorted by margin, colored by direction
    st.markdown("### Net Margin Per Mile by Route")
    route_summary = master.groupby('route_id').agg(
        trips=('trip_id', 'count'),
        origin_city=('origin_city', 'first'), origin_state=('origin_state', 'first'),
        destination_city=('destination_city', 'first'), destination_state=('destination_state', 'first'),
        avg_rev_mi=('rev_per_mile', 'mean'), avg_margin_mi=('net_margin_per_mile', 'mean'),
        total_margin=('net_margin_total', 'sum'), direction=('direction', 'first')
    ).reset_index().sort_values('avg_margin_mi', ascending=True)
    route_summary['route_label'] = route_summary['origin_city'] + \
        " → " + route_summary['destination_city']

    fig1 = go.Figure(go.Bar(
        x=route_summary['avg_margin_mi'], y=route_summary['route_label'], orientation='h',
        marker_color=[COLOR_BLUE if d ==
                      'Southbound' else COLOR_RED for d in route_summary['direction']],
        text=[f"${v:.2f}" for v in route_summary['avg_margin_mi']], textposition='outside'
    ))
    fig1.add_vline(x=breakeven, line_dash='dash', line_color=COLOR_MUTED,
                   annotation_text=f"Breakeven ${breakeven:.2f}")
    fig1.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       xaxis_title="Net Margin / Mile ($)", xaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Blue bars are southbound loaded lanes; red bars are northbound "
        "backhauls. The dashed line marks your breakeven threshold from the slider above. Every red "
        "bar sitting left of the dashed line is backhaul freight that, on average, isn't clearing the "
        "bar you set — that's freight worth being pickier about on the load board."
    )

    # Chart 2: monthly trend of northbound margin
    st.markdown("### Northbound Backhaul Margin — Monthly Trend")
    nb_monthly = nb.groupby('month')['net_margin_per_mile'].mean(
    ).reset_index().sort_values('month')
    fig2 = go.Figure(go.Scatter(x=nb_monthly['month'], y=nb_monthly['net_margin_per_mile'],
                                mode='lines+markers', line=dict(color=COLOR_RED, width=2)))
    fig2.add_hline(y=breakeven, line_dash='dash', line_color=COLOR_MUTED,
                   annotation_text=f"Breakeven ${breakeven:.2f}")
    fig2.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       yaxis_title="Net Margin / Mile ($)", yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This tracks northbound backhaul margin month by month. If the line "
        "sits consistently below the dashed breakeven line, this isn't a one-off bad stretch — it's a "
        "structural feature of backhaul freight that needs a strategy (rate increases south, or being "
        "pickier about which loads you accept north) rather than hoping it improves on its own."
    )

    # Route table
    st.markdown("### Full Route Table")
    table_df = route_summary.sort_values('avg_margin_mi', ascending=False)[
        ['route_label', 'direction', 'trips',
            'avg_rev_mi', 'avg_margin_mi', 'total_margin']
    ].copy()
    table_df.columns = ['Route', 'Direction', 'Trip Count',
                        'Avg Rev/Mile', 'Avg Net Margin/Mile', 'Total Net Margin']
    table_df['Avg Rev/Mile'] = table_df['Avg Rev/Mile'].apply(
        lambda x: f"${x:.2f}")
    table_df['Avg Net Margin/Mile'] = table_df['Avg Net Margin/Mile'].apply(
        lambda x: f"${x:.2f}")
    table_df['Total Net Margin'] = table_df['Total Net Margin'].apply(
        lambda x: f"${x:,.0f}")
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    with st.expander("❓ How to use this page"):
        st.markdown("""
This page exists because Blue Heron's southbound freight (Skagit Valley Produce, Bellingham Cold
Storage, Cascade Berry Growers heading to Portland and the Bay Area) and northbound backhauls
(whatever can be found on the load board heading back to Mount Vernon and Bellingham) are two
completely different businesses stapled together, and they need to be evaluated separately.

**What healthy looks like:** Southbound lanes should net well over $2/mile after fuel — that's the
core, reliable business. Northbound backhauls will always net less (there's no way around thinner
return-freight margins when your core customers don't ship north), but there's a real difference
between "thinner but acceptable" and "barely breaking even." The breakeven slider lets you set your
own line for that distinction.

**What to do if the numbers look bad:** If a large share of northbound trips fall below your
breakeven line, you have two real levers: be pickier about which load-board offers you accept
(use the Load Acceptance calculator logic on the fly — miles × your truck's real MPG × current
fuel price tells you the true cost before you say yes), or push for a modest rate increase on your
southbound core lanes to intentionally cross-subsidize the empty-mile-heavy return trip. Many
reefer carriers price southbound freight assuming the northbound leg won't fully pay for itself.

**Route-level detail:** The full table at the bottom lets you sort by total net margin to see which
specific route is contributing the most (or least) dollars overall — useful when a customer or
broker calls about a specific lane.

**How often to check:** Monthly is enough. This is a strategic, not a daily, decision — it's about
adjusting your pricing and load-acceptance habits over time, not reacting to a single bad week.

**The most important action this week:** Look at which northbound route sits furthest below your
breakeven line in the chart above. If it's a route you run repeatedly, that's the one worth either
avoiding on the load board going forward, or specifically asking a broker for a rate closer to what
your southbound lanes command.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: GOLDEN GATE DETENTION TRACKER
# ═══════════════════════════════════════════════════════════════════════════
elif page == "⏱️ Golden Gate Detention Tracker":
    st.title("Golden Gate Detention Tracker & Leverage Report")
    st.caption(
        "Turning the dreaded Oakland stop into a dollar figure you can put in an email.")
    st.divider()

    st.markdown(f"""
    <div class='priority-banner'>
    <strong>The core issue:</strong> Golden Gate Fresh Distributors averages <strong>{gg_row['avg_detention']:.1f}
    minutes</strong> of detention per stop — roughly <strong>{gg_row['avg_detention']/det_by_customer[det_by_customer.customer_name != GG_NAME]['avg_detention'].mean():.1f}x</strong>
    the average at every other customer — and is on-time only <strong>{gg_row['on_time_rate']:.1f}%</strong>
    of the time, versus 82-90% everywhere else. This is Blue Heron's highest-volume delivery point, so
    it can't simply be avoided.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-intro'>
    <strong>What to focus on:</strong> Set your own hourly cost estimate below — this is a judgment
    call you should control before using this number externally. The leverage brief beneath it is
    built to be screenshotted and used directly in a conversation with Golden Gate's traffic manager.
    </div>
    """, unsafe_allow_html=True)

    hourly_rate = st.number_input(
        "Estimated truck + driver cost per hour ($)", min_value=10.0, max_value=200.0, value=65.0, step=5.0,
        help="This is your own estimate of what an hour of detained truck-and-driver time costs you — "
             "fuel, financing, insurance, and driver time combined. The default of $65/hr is a "
             "conservative starting point; adjust it to match your real costs."
    )
    gg_cost_live = gg_row['total_hours'] * hourly_rate

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Golden Gate Deliveries", f"{int(gg_row['events'])}",
              help="Total delivery events recorded for Golden Gate Fresh Distributors.")
    c2.metric("Avg Detention / Stop", f"{gg_row['avg_detention']:.1f} min",
              help="Average minutes the truck sat at Golden Gate's dock beyond scheduled arrival, per delivery.")
    c3.metric("Total Detention Hours", f"{gg_row['total_hours']:.1f} hrs",
              help="Sum of all detention minutes across every Golden Gate delivery, converted to hours.")
    c4.metric("Estimated Cost", f"${gg_cost_live:,.0f}",
              help="Total detention hours multiplied by your chosen hourly rate above.")

    # Chart 1: bar chart, all customers ranked by avg detention
    st.markdown("### Detention Leaderboard — All Customers")
    fig1 = go.Figure(go.Bar(
        x=det_by_customer['customer_name'], y=det_by_customer['avg_detention'],
        marker_color=[
            COLOR_RED if n == GG_NAME else COLOR_BLUE for n in det_by_customer['customer_name']],
        text=[f"{v:.1f} min" for v in det_by_customer['avg_detention']], textposition='outside'
    ))
    fig1.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       yaxis_title="Avg Detention (minutes)", xaxis_tickangle=-20,
                       yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Golden Gate Fresh Distributors (in red) sits far above every other "
        "customer, all of whom cluster in the 8-10 minute range — normal dock friction. Golden Gate "
        "isn't a slightly-worse customer; it's operating in a completely different category."
    )

    # Chart 2: histogram comparing GG vs all others
    st.markdown("### Detention Distribution — Golden Gate vs. Everyone Else")
    d_all = delivery_events.merge(loads[['load_id', 'customer_id']], on='load_id', how='left').merge(
        customers[['customer_id', 'customer_name']], on='customer_id', how='left')
    gg_dist = d_all[d_all['customer_name'] == GG_NAME]['detention_minutes']
    other_dist = d_all[d_all['customer_name'] != GG_NAME]['detention_minutes']

    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=other_dist, name='All Other Customers',
                   marker_color=COLOR_BLUE, opacity=0.75, nbinsx=20))
    fig2.add_trace(go.Histogram(x=gg_dist, name='Golden Gate Fresh Distributors',
                   marker_color=COLOR_RED, opacity=0.75, nbinsx=20))
    fig2.update_layout(height=380, barmode='overlay', margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       legend=dict(orientation='h', yanchor='bottom',
                                   y=1.02, xanchor='left', x=0),
                       xaxis_title="Detention Minutes", yaxis_title="Number of Deliveries",
                       yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Blue bars (all other customers) cluster tightly near zero — quick, "
        "predictable dock turnaround. Red bars (Golden Gate) are shifted far to the right and spread "
        "wide, all the way up to 75 minutes. This spread, not just the average, is what shows Golden "
        "Gate's delays aren't an occasional bad day — they're the norm."
    )

    # Chart 3: monthly trend of GG detention
    st.markdown("### Golden Gate Detention — Monthly Trend")
    gg_loads_ids = loads[loads['customer_id'] == 'CUST-04']['load_id']
    gg_events = delivery_events[delivery_events['load_id'].isin(
        gg_loads_ids)].copy()
    gg_events = gg_events.merge(
        loads[['load_id', 'load_date']], on='load_id', how='left')
    gg_events['load_date'] = pd.to_datetime(gg_events['load_date'])
    gg_events['month'] = gg_events['load_date'].dt.to_period('M').astype(str)
    gg_monthly = gg_events.groupby(
        'month')['detention_minutes'].mean().reset_index().sort_values('month')

    fig3 = go.Figure(go.Scatter(x=gg_monthly['month'], y=gg_monthly['detention_minutes'],
                                mode='lines+markers', line=dict(color=COLOR_RED, width=2)))
    fleet_avg_other = other_dist.mean()
    fig3.add_hline(y=fleet_avg_other, line_dash='dash', line_color=COLOR_BLUE,
                   annotation_text=f"All-other-customer avg ({fleet_avg_other:.0f} min)")
    fig3.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10),
                       plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                       yaxis_title="Avg Detention (minutes)", yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This tracks Golden Gate's average detention month by month against "
        "the blue dashed line showing what every other customer averages. If Golden Gate's line stays "
        "consistently high rather than spiking occasionally, that supports the argument this is baked "
        "into how their facility operates, not an occasional bad day at the dock."
    )

    # Leverage brief callout
    st.markdown("### 📋 Leverage Brief — Ready to Share")
    st.markdown(f"""
    <div class='priority-banner'>
    <strong>Golden Gate Fresh Distributors — Detention Summary</strong><br><br>
    Across <strong>{int(gg_row['events'])} deliveries</strong>, Blue Heron Cold Chain trucks have been
    detained a total of <strong>{gg_row['total_hours']:.1f} hours</strong> at Golden Gate's Oakland
    facility — an average of <strong>{gg_row['avg_detention']:.1f} minutes per stop</strong>, compared to
    an <strong>{fleet_avg_other:.0f}-minute average</strong> at every other customer we serve.
    On-time performance at this location is just <strong>{gg_row['on_time_rate']:.1f}%</strong>, versus
    82-90% elsewhere in our network.<br><br>
    At a conservative <strong>${hourly_rate:.0f}/hour</strong> estimated truck-and-driver cost, this
    represents approximately <strong>${gg_cost_live:,.0f}</strong> in uncompensated detention time.
    We'd like to discuss a detention accessorial fee or improved dock scheduling to address this.
    </div>
    """, unsafe_allow_html=True)

    st.info(
        f"💡 **INSIGHT:** Golden Gate Fresh Distributors has cost Blue Heron an estimated "
        f"**${gg_cost_live:,.0f}** in detention time across {int(gg_row['events'])} deliveries — "
        f"**{gg_row['avg_detention']/fleet_avg_other:.1f}x** the fleet's average wait at every other stop, "
        f"with a maximum single detention of **{gg_dist.max():.0f} minutes**."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists to turn a shared frustration — everyone at Blue Heron dreads the Golden Gate stop —
into a specific, defensible dollar figure you can use in a business conversation.

**Why this matters:** Golden Gate Fresh Distributors is Blue Heron's third-largest revenue customer
(about 19.7% of total revenue), so walking away from the relationship isn't realistic. But that
doesn't mean you have to absorb the cost of their dock inefficiency silently. Detention accessorial
fees are a standard, common practice in trucking — many shippers and receivers already expect to pay
them when they hold a truck past a reasonable window (typically 1-2 hours free, then billed hourly).

**What to do with this page:** The hourly rate input is yours to control — set it to whatever you
believe genuinely reflects your cost of an hour of detained truck-and-driver time (fuel burn while
idling, financing cost on the truck, insurance, and the driver's opportunity cost of not being on
the road). Once you're comfortable with the number, the leverage brief box above is written and
formatted so you can screenshot it directly into an email or bring it printed to a meeting with
Golden Gate's traffic manager.

**What healthy vs. unhealthy looks like:** Every other Blue Heron customer averages 8-10 minutes of
detention — that's normal, unavoidable dock friction and not worth pursuing a fee over. Golden Gate's
43.8-minute average is nearly 5x that, and its 4.5% on-time rate (versus 82-90% elsewhere) tells you
this isn't your drivers being late — it's the facility failing to unload trucks on schedule.

**How to use the monthly trend chart in conversation:** If you're negotiating and Golden Gate's team
suggests this was a rough patch that's since improved, the monthly trend chart will tell you quickly
whether that's true. If the line has stayed elevated across every month in the data, that's a strong
argument this is systemic, not situational.

**How often to check:** Quarterly is enough to track whether a conversation with Golden Gate is
actually changing behavior — check this page again after any accessorial agreement or process change
to see if their average detention time comes down.

**The most important action:** If you haven't already had a direct conversation with Golden Gate's
traffic manager about a detention fee, this page gives you everything you need to have it. The
combination of a specific dollar figure, a stop-by-stop event count, and a clear "5x every other
customer" comparison is exactly the kind of evidence that turns a frustrated complaint into a
successful accessorial negotiation.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CASH FLOW & RECEIVABLES
# ═══════════════════════════════════════════════════════════════════════════
elif page == "💰 Cash Flow & Receivables":
    st.title("Cash Flow & Receivables")
    st.caption(
        "What's coming in, when, and whether Blue Heron will have enough to cover expenses next week.")
    st.divider()

    st.markdown("""
    <div class='section-intro'>
    Cash flow is the #1 killer of small trucking companies. This page shows you what customers owe
    you, how overdue it is, and a rough projection of the next 30 days — so a slow-paying customer
    doesn't catch you off guard when a fuel bill or truck payment comes due.
    </div>
    """, unsafe_allow_html=True)

    # Build a synthetic AR table: use load_date + payment_terms_days as due date,
    # "days_outstanding" measured against the max date in the dataset (as if "today")
    as_of = master['departure_time'].max()
    ar = master[['load_id', 'customer_name', 'load_date',
                 'payment_terms_days', 'gross_revenue']].copy()
    ar['due_date'] = ar['load_date'] + \
        pd.to_timedelta(ar['payment_terms_days'], unit='D')
    ar['days_outstanding'] = (as_of - ar['due_date']).dt.days
    # keep only "outstanding" — the most recent ~45 days of load activity (a rough open-AR proxy since
    # this is historical delivered-load data, not a true invoice ledger)
    open_window = ar[ar['load_date'] >= as_of - pd.Timedelta(days=45)].copy()
    open_window['status'] = pd.cut(open_window['days_outstanding'], bins=[-9999, 0, 30, 60, 9999],
                                   labels=['Not Yet Due', '0-30 Days', '31-60 Days', '61+ Days'])

    # apply any manual overrides
    for lid, new_status in st.session_state.ar_status_overrides.items():
        open_window.loc[open_window['load_id'] == lid, 'status'] = new_status

    total_ar = open_window['gross_revenue'].sum()
    overdue_30 = open_window[open_window['days_outstanding']
                             > 30]['gross_revenue'].sum()
    avg_days_to_pay = open_window['payment_terms_days'].mean()

    # simple 30-day net cash projection: incoming (loads due to be paid) minus a flat estimated
    # fixed weekly cost (fuel + typical maintenance, derived from trailing average)
    weekly_fuel_cost = fuel_purchases.sort_values('purchase_date')['total_cost'].tail(
        60).sum() / (60 / 7) if len(fuel_purchases) else 0
    # fuel is the dominant recurring cost visible in this data
    weekly_fixed_est = weekly_fuel_cost

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Outstanding AR", f"${total_ar:,.0f}",
              help="Estimated total revenue from recent loads not yet past their payment due date "
                   "cycle — money customers owe that hasn't been collected.")
    c2.metric("Overdue >30 Days", f"${overdue_30:,.0f}",
              help="Outstanding balance more than 30 days past its due date. These should be called "
                   "on immediately — the longer an invoice ages, the less likely it gets paid in full.")
    c3.metric("Avg Payment Terms", f"{avg_days_to_pay:.0f} days",
              help="Average contractual payment terms across your customer base, weighted by recent load volume.")
    c4.metric("Est. Net Cash (Next 30 Days)", f"${total_ar - weekly_fixed_est*4:,.0f}",
              help="A rough projection: outstanding receivables expected to come in, minus an estimate "
                   "of fixed weekly costs (based on recent fuel spend) over the next 4 weeks.")

    # AR aging table
    st.markdown("### Accounts Receivable Aging")
    aging_summary = open_window.groupby(['customer_name', 'status'], observed=True)[
        'gross_revenue'].sum().reset_index()
    aging_pivot = aging_summary.pivot(
        index='customer_name', columns='status', values='gross_revenue').fillna(0)
    for col in ['Not Yet Due', '0-30 Days', '31-60 Days', '61+ Days']:
        if col not in aging_pivot.columns:
            aging_pivot[col] = 0
    aging_pivot = aging_pivot[['Not Yet Due',
                               '0-30 Days', '31-60 Days', '61+ Days']]
    aging_pivot['Total'] = aging_pivot.sum(axis=1)
    aging_display = aging_pivot.reset_index().sort_values('Total', ascending=False)
    for col in ['Not Yet Due', '0-30 Days', '31-60 Days', '61+ Days', 'Total']:
        aging_display[col] = aging_display[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(aging_display, use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** Each column is a bucket of how overdue the balance is. '0-30 Days' "
        "past due is normal — most customers pay somewhere in this window. '31-60 Days' deserves a "
        "friendly check-in call. '61+ Days' should be escalated immediately — the longer it sits, the "
        "harder it typically is to collect in full."
    )

    # 30-day cash projection chart
    st.markdown("### 30-Day Cash Projection")
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    incoming_per_week = total_ar / 4
    running_balance = []
    bal = 0
    for _ in weeks:
        bal += incoming_per_week - weekly_fixed_est
        running_balance.append(bal)
    fig = go.Figure(go.Scatter(x=weeks, y=running_balance, mode='lines+markers',
                               line=dict(color=COLOR_BLUE, width=3), fill='tozeroy',
                               fillcolor='rgba(42,120,214,0.15)'))
    fig.add_hline(y=0, line_color=COLOR_CRITICAL, line_dash='dash')
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10),
                      plot_bgcolor='#fcfcfb', paper_bgcolor='#fcfcfb',
                      yaxis_title="Projected Running Cash Balance ($)", yaxis=dict(gridcolor='#e1e0d9'))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This assumes outstanding receivables come in evenly over the next "
        "4 weeks, minus an estimated weekly fuel cost based on recent spending (the dominant recurring "
        "cost visible in this data — it doesn't yet include insurance, loan payments, or other fixed "
        "costs you carry). If the line goes below zero, you'll need to either chase a payment early or "
        "arrange short-term financing before that week arrives."
    )

    # Mark invoice paid (fake CRUD)
    st.markdown("### Mark Invoice Paid")
    with st.expander("✅ Mark an Invoice Paid"):
        pay_customer = st.selectbox("Customer", sorted(
            open_window['customer_name'].unique()))
        pay_amount = st.number_input(
            "Amount Paid ($)", min_value=0.0, value=1000.0, step=50.0)
        pay_date = st.date_input("Date Paid", value=datetime.now().date())
        if st.button("Mark Paid", key="mark_paid"):
            key = f"{pay_customer}-{pay_date}-{pay_amount}"
            st.session_state.ar_status_overrides[key] = 'Paid'
            st.session_state.action_log.append(
                f"{datetime.now().strftime('%H:%M')} — Marked ${pay_amount:,.0f} from {pay_customer} as paid on {pay_date}"
            )
            st.success(
                f"Recorded ${pay_amount:,.0f} payment from {pay_customer}!")
            st.rerun()

    # Insight: highest-risk overdue invoice
    if len(aging_display) and aging_display['Total'].iloc[0] != "$0":
        highest_risk = aging_pivot.reset_index().assign(
            risk_amt=lambda d: d['31-60 Days'] + d['61+ Days']
        ).sort_values('risk_amt', ascending=False).iloc[0]
        gg_terms = customers[customers['customer_name']
                             == GG_NAME]['payment_terms_days'].values[0]
        st.info(
            f"💡 **INSIGHT:** **{highest_risk['customer_name']}** carries the highest overdue balance "
            f"risk, with **${highest_risk['risk_amt']:,.0f}** sitting in the 31+ day buckets. Golden Gate "
            f"Fresh Distributors' **{gg_terms}-day payment terms** — the longest of any customer — mean "
            f"a meaningful share of Blue Heron's revenue is routinely tied up in receivables before it "
            f"ever hits the bank."
        )

    with st.expander("❓ How to use this page"):
        st.markdown("""
Cash flow, not profitability, is what actually sinks small trucking companies — a business can be
profitable on paper and still run out of cash if customers pay slowly and fuel bills come due weekly.
This page is meant to catch that gap before it becomes an emergency.

**What each aging bucket means:** "Not Yet Due" is money that's expected but hasn't hit its payment
deadline yet — no action needed. "0-30 Days" past due is normal for most business relationships —
still worth tracking, not worth a phone call. "31-60 Days" warrants a polite check-in call to the
customer's accounts payable contact. "61+ Days" should be escalated immediately — call the customer
directly, and consider whether future loads for that customer should require different terms.

**A simple script for calling an overdue customer:** "Hi, I'm following up on invoice [#] for
[amount], which was due on [date]. Can you tell me where that stands and when we should expect
payment?" Keep it friendly and factual — most overdue payments are processing delays, not disputes,
and a friendly nudge is usually all it takes.

**How to read the 30-day projection:** This assumes your outstanding receivables arrive evenly over
the next month and subtracts your recent average weekly fuel spend. It does not yet account for
insurance, loan payments, or other fixed costs — treat it as a floor estimate, not a complete
picture. If the projected line dips below zero, that's your signal to either call a slow-paying
customer early or line up short-term financing (a business line of credit or factoring your
receivables) before the shortfall actually arrives.

**Payment terms negotiation tips:** Customers on longer terms (like Golden Gate's 45 days) tie up
more of your cash for longer. If a customer's payment terms are a persistent strain on your cash
position, it's reasonable to ask for shorter terms (30 days instead of 45) as part of any broader
rate or accessorial conversation — especially if, like Golden Gate, they're already a source of
friction elsewhere in the relationship.

**How often to check:** Weekly, ideally on the same day each week (Friday works well, so you head
into the weekend knowing where you stand) — especially in the weeks leading up to a large known
expense like an insurance renewal or a truck repair.
""")
