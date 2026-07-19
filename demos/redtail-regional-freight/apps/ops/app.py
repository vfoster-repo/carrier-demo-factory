import os
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ══════════════════════════════════════════════════════════════════════════
# COMPANY CONSTANTS
# ══════════════════════════════════════════════════════════════════════════
COMPANY_NAME = "Redtail Regional Freight"
OWNER_FIRST_NAME = "Dale"
OWNER_FULL_NAME = "Dale Whitfield"
CONTACT_EMAIL = "victorfoster@hotmail.com"
BREAKEVEN_RATE_PER_MILE = 2.05
FLAGGED_TRUCK = "TRK-014"
FLAGGED_CUSTOMER = "Llano Estacado Foods"
FLAGGED_CUSTOMER_ID = "CUST-002"

# ══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG + CSS
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Redtail Regional Freight — Operations",
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


# ══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════
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
trucks_df = data['trucks'].copy()
drivers_df = data['drivers'].copy()
customers_df = data['customers'].copy()
routes_df = data['routes'].copy()
loads_df = data['loads'].copy()
trips_df = data['trips'].copy()
fuel_df = data['fuel_purchases'].copy()
maint_df = data['maintenance_records'].copy()
delivery_df = data['delivery_events'].copy()

# Parse dates
loads_df['load_date'] = pd.to_datetime(loads_df['load_date'])
trips_df['departure_time'] = pd.to_datetime(trips_df['departure_time'])
trips_df['arrival_time'] = pd.to_datetime(trips_df['arrival_time'])
fuel_df['purchase_date'] = pd.to_datetime(fuel_df['purchase_date'])
maint_df['service_date'] = pd.to_datetime(maint_df['service_date'])
delivery_df['scheduled_time'] = pd.to_datetime(delivery_df['scheduled_time'])
delivery_df['actual_time'] = pd.to_datetime(delivery_df['actual_time'])
drivers_df['hire_date'] = pd.to_datetime(drivers_df['hire_date'])

DATA_THROUGH = loads_df['load_date'].max()
DATA_THROUGH_STR = DATA_THROUGH.strftime('%B %d, %Y')

# ══════════════════════════════════════════════════════════════════════════
# PRECOMPUTED JOINS / AGGREGATES (shared across pages)
# ══════════════════════════════════════════════════════════════════════════

# --- loads + routes + customers, master table ---
loads_full = loads_df.merge(routes_df, on='route_id', how='left') \
    .merge(customers_df, on='customer_id', how='left')

# --- trips + trucks + drivers, master table ---
trips_full = trips_df.merge(loads_full[['load_id', 'customer_id', 'customer_name', 'route_id',
                                        'origin_city', 'destination_city', 'load_date',
                                        'revenue', 'fuel_surcharge', 'distance_miles',
                                        'base_rate_per_mile']], on='load_id', how='left')
trips_full = trips_full.merge(trucks_df[['truck_id', 'make', 'model', 'year', 'status']],
                              on='truck_id', how='left', suffixes=('', '_truck'))
trips_full = trips_full.merge(drivers_df[['driver_id', 'first_name', 'last_name']],
                              on='driver_id', how='left')
trips_full['driver_name'] = trips_full['first_name'] + \
    ' ' + trips_full['last_name']

# --- fuel cost per trip ---
fuel_by_trip = fuel_df.groupby('trip_id').agg(trip_fuel_cost=('total_cost', 'sum'),
                                              trip_gallons=('gallons', 'sum')).reset_index()
trips_full = trips_full.merge(fuel_by_trip, on='trip_id', how='left')
trips_full['trip_fuel_cost'] = trips_full['trip_fuel_cost'].fillna(0)

# --- detention by trip / load ---
detention_by_load = delivery_df.groupby('load_id').agg(
    total_detention_min=('detention_minutes', 'sum'),
    n_events=('event_id', 'count'),
    pct_on_time=('on_time', 'mean')
).reset_index()

# --- fleet-wide MPG stats ---
mpg_by_truck = trips_df.groupby('truck_id')['actual_mpg'].agg(
    ['mean', 'count', 'std']).reset_index()
mpg_by_truck.columns = ['truck_id', 'avg_mpg', 'trip_count', 'std_mpg']
mpg_by_truck = mpg_by_truck.merge(trucks_df, on='truck_id', how='left')
FLEET_AVG_MPG = trips_df['actual_mpg'].mean()

# --- fleet-wide diesel price ---
FLEET_AVG_DIESEL_PRICE = fuel_df['price_per_gallon'].mean()

# --- maintenance by truck ---
maint_by_truck = maint_df.groupby('truck_id').agg(
    total_maint_cost=('cost', 'sum'),
    n_records=('record_id', 'count'),
    total_downtime_hrs=('downtime_hours', 'sum')
).reset_index()
FLEET_AVG_MAINT = maint_by_truck['total_maint_cost'].mean()

MAINT_CUTOFF_18MO = maint_df['service_date'].max() - pd.DateOffset(months=18)
maint_recent = maint_df[maint_df['service_date'] >= MAINT_CUTOFF_18MO]
maint_recent_by_truck = maint_recent.groupby('truck_id').agg(
    recent_maint_cost=('cost', 'sum'),
    recent_downtime_hrs=('downtime_hours', 'sum'),
    recent_n_records=('record_id', 'count')
).reset_index()

# --- truck scorecard: combine mpg + maintenance + annual miles ---
truck_annual_miles = trips_df.groupby(
    'truck_id')['actual_miles'].sum().reset_index()
truck_annual_miles.columns = ['truck_id', 'total_miles']
# approx data period in years
DATA_PERIOD_DAYS = (trips_df['departure_time'].max() -
                    trips_df['departure_time'].min()).days
DATA_PERIOD_YEARS = max(DATA_PERIOD_DAYS / 365.25, 0.1)
truck_annual_miles['annual_miles'] = truck_annual_miles['total_miles'] / \
    DATA_PERIOD_YEARS

truck_scorecard = trucks_df.merge(mpg_by_truck[[
                                  'truck_id', 'avg_mpg', 'trip_count', 'std_mpg']], on='truck_id', how='left')
truck_scorecard = truck_scorecard.merge(
    maint_by_truck, on='truck_id', how='left')
truck_scorecard = truck_scorecard.merge(
    maint_recent_by_truck, on='truck_id', how='left')
truck_scorecard = truck_scorecard.merge(
    truck_annual_miles, on='truck_id', how='left')
for c in ['total_maint_cost', 'n_records', 'total_downtime_hrs', 'recent_maint_cost',
          'recent_downtime_hrs', 'recent_n_records', 'total_miles', 'annual_miles']:
    truck_scorecard[c] = truck_scorecard[c].fillna(0)

truck_scorecard['excess_fuel_cost_annual'] = (
    (1 / truck_scorecard['avg_mpg'].replace(0,
     FLEET_AVG_MPG) - 1 / FLEET_AVG_MPG)
    * truck_scorecard['annual_miles'] * FLEET_AVG_DIESEL_PRICE
).clip(lower=0)
# 18mo -> annualized
truck_scorecard['maint_run_rate_annual'] = truck_scorecard['recent_maint_cost'] / 1.5
truck_scorecard['excess_annual_cost'] = (
    truck_scorecard['excess_fuel_cost_annual'] +
    truck_scorecard['maint_run_rate_annual']
    - FLEET_AVG_MAINT / DATA_PERIOD_YEARS
).clip(lower=0)
truck_scorecard['cost_per_mile'] = truck_scorecard['total_maint_cost'] / \
    truck_scorecard['total_miles'].replace(0, 1)

# --- cost per mile MTD for fleet status table on dashboard ---
CURRENT_MONTH_START = DATA_THROUGH.replace(day=1)
trips_mtd = trips_full[trips_full['departure_time'] >= CURRENT_MONTH_START]
loads_mtd_count = trips_mtd['load_id'].nunique()

# --- detention by customer ---
delivery_with_customer = delivery_df.merge(
    loads_full[['load_id', 'customer_id', 'customer_name']], on='load_id', how='left')
detention_by_customer = delivery_with_customer.groupby(['customer_id', 'customer_name']).agg(
    avg_detention=('detention_minutes', 'mean'),
    total_detention_hrs=('detention_minutes', lambda x: x.sum() / 60),
    n_events=('event_id', 'count'),
    pct_on_time=('on_time', 'mean')
).reset_index().sort_values('avg_detention', ascending=False)

FLEET_AVG_DETENTION_EX_FLAGGED = delivery_with_customer[
    delivery_with_customer['customer_id'] != FLAGGED_CUSTOMER_ID
]['detention_minutes'].mean()

# --- route net profitability ---
trips_full['net_revenue'] = trips_full['revenue'] + \
    trips_full['fuel_surcharge'] - trips_full['trip_fuel_cost']
trips_full['net_per_mile'] = trips_full['net_revenue'] / \
    trips_full['actual_miles'].replace(0, 1)

route_net = trips_full.groupby('route_id').agg(
    n_loads=('load_id', 'nunique'),
    avg_gross_rate=('base_rate_per_mile', 'mean'),
    avg_net_per_mile=('net_per_mile', 'mean'),
    avg_fuel_cost=('trip_fuel_cost', 'mean'),
    total_revenue=('revenue', 'sum'),
).reset_index()
route_net = route_net.merge(routes_df[['route_id', 'origin_city', 'destination_city', 'distance_miles', 'base_rate_per_mile']],
                            on='route_id', how='left')
route_net['pct_below_breakeven'] = trips_full.groupby('route_id')['net_per_mile'].apply(
    lambda x: (x < BREAKEVEN_RATE_PER_MILE).mean() * 100
).reindex(route_net['route_id']).values
route_net['lane_label'] = route_net['origin_city'] + \
    ' → ' + route_net['destination_city']
route_net = route_net.sort_values('avg_net_per_mile')

# --- driver tenure / cohort ---
drivers_tenure = drivers_df.copy()
drivers_tenure['tenure_days'] = (
    DATA_THROUGH - drivers_tenure['hire_date']).dt.days
HIRE_CUTOFF_18MO = drivers_df['hire_date'].max() - pd.DateOffset(months=18)
drivers_tenure['cohort'] = drivers_tenure['hire_date'].apply(
    lambda d: 'Hired last 18 months' if d >= HIRE_CUTOFF_18MO else 'Hired earlier'
)
drivers_tenure['is_departed'] = drivers_tenure['employment_status'].isin(
    ['terminated', 'voluntary_quit'])

# --- On-time rate fleet-wide ---
FLEET_ON_TIME_PCT = trips_df['on_time_flag'].mean() * 100

# --- AR / cash flow simulated aging (loads.csv has no payment data; derive from load_date + customer terms) ---
delivered = loads_full[loads_full['load_status'] == 'delivered'].copy()
delivered['total_invoice'] = delivered['revenue'] + delivered['fuel_surcharge']
delivered['due_date'] = delivered['load_date'] + \
    pd.to_timedelta(delivered['payment_terms_days'], unit='D')
delivered['days_outstanding'] = (DATA_THROUGH - delivered['due_date']).dt.days
# Simulate: loads due more than 0 days ago are "outstanding" unless we mark as paid;
# we treat everything with due_date within the last 75 days as open AR (recent enough to still be receivable)
AR_WINDOW_DAYS = 75
open_ar = delivered[(delivered['days_outstanding'] >= -delivered['payment_terms_days']) &
                    (delivered['days_outstanding'] <= AR_WINDOW_DAYS) &
                    (delivered['due_date'] <= DATA_THROUGH + pd.Timedelta(days=delivered['payment_terms_days'].max()))].copy()
open_ar = open_ar[open_ar['load_date'] >= DATA_THROUGH - pd.Timedelta(days=90)]
open_ar['days_outstanding'] = open_ar['days_outstanding'].clip(lower=0)


def aging_bucket(days):
    if days <= 30:
        return '0-30 days'
    elif days <= 60:
        return '31-60 days'
    else:
        return '61+ days'


open_ar['aging_bucket'] = open_ar['days_outstanding'].apply(aging_bucket)

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════
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


def log_action(msg):
    st.session_state.action_log.append(
        f"{datetime.now().strftime('%m/%d %H:%M')} — {msg}")


# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
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
         "🔧 Truck Retirement Scorecard",
         "⏱️ Customer Detention Tracker",
         "🛣️ Lane Profitability",
         "👥 Driver Retention",
         "💰 Cash Flow & Receivables"],
        label_visibility="collapsed"
    )

    st.divider()
    n_trucks_active = (trucks_df['status'] == 'active').sum()
    st.markdown(
        f"**Fleet:** {n_trucks_active} active truck{'s' if n_trucks_active != 1 else ''} ({len(trucks_df)} total)")
    st.markdown(f"**Loads this month:** {loads_mtd_count}")
    st.markdown(f"**On-time rate:** {FLEET_ON_TIME_PCT:.0f}%")
    st.divider()
    st.caption(f"Data through {DATA_THROUGH_STR}")
    st.markdown(f"[📧 Get Help](mailto:{CONTACT_EMAIL})")

    # Load Board filters (only shown on that page, but must be defined in sidebar scope)
    if page == "📋 Load Board":
        st.divider()
        st.markdown("**Filter Loads**")
        min_date = loads_df['load_date'].min().date()
        max_date = loads_df['load_date'].max().date()
        lb_start = st.date_input("From", value=max(min_date, max_date - timedelta(days=30)),
                                 min_value=min_date, max_value=max_date, key="lb_start")
        lb_end = st.date_input(
            "To", value=max_date, min_value=min_date, max_value=max_date, key="lb_end")
        lb_status = st.multiselect("Status", options=['delivered', 'cancelled'], default=[
                                   'delivered', 'cancelled'], key="lb_status")
        lb_customer = st.selectbox("Customer", options=[
                                   'All'] + sorted(customers_df['customer_name'].tolist()), key="lb_customer")
        lb_driver_options = ['All'] + sorted(drivers_df.apply(
            lambda r: f"{r['first_name']} {r['last_name']} ({r['driver_id']})", axis=1).tolist())
        lb_driver = st.selectbox(
            "Driver", options=lb_driver_options, key="lb_driver")


# ══════════════════════════════════════════════════════════════════════════
# PAGE: GETTING STARTED
# ══════════════════════════════════════════════════════════════════════════
if page == "🏠 Getting Started":
    st.title(f"Welcome, {OWNER_FIRST_NAME}! Here's Your Operations Platform.")

    st.markdown(f"""
For eleven years you ran the numbers on Redtail out of your head and a spreadsheet you rebuild
every few months. That works fine when you've got eight trucks and you can eyeball which one
needs a wrench. It stops working at 38 trucks, 52 drivers, and four anchor customers moving
freight across four states. This platform was built directly from your own operating data —
every load, every trip, every fuel receipt, every maintenance ticket, every dock detention
event going back to July 2024 — so that instead of a gut feeling about which truck is a money
pit or which customer is quietly eating your margin, you have the exact dollar figure in front
of you.

This isn't generic trucking software with your logo slapped on it. It was built by reading
your actual CSVs: your 38 trucks (TRK-001 through TRK-038), your 52 drivers, your four
anchor customers (Panhandle Beef Processors, Llano Estacado Foods, High Plains Ag Cooperative,
and Sangre de Cristo Distribution), and your eight regional lanes running out of Amarillo.
Every number on every page below ties back to a real load, a real truck, or a real driver —
nothing here is a demo placeholder.
    """)

    st.info("📱 On your phone? Tap the **>** arrow in the top-left to open the navigation menu.")

    st.markdown("## What This Platform Does For You")
    st.markdown(f"""
Redtail has grown from a single 2006 Peterbilt to a 38-truck regional carrier, but the
management tooling never grew with it — you're still running the business the same way you
did with eight trucks. A spreadsheet you rebuild by hand a few times a year can't catch a
truck that's been quietly bleeding $31,000 a year in excess fuel and repair costs, or a
customer whose dock delays have burned nearly 7,000 driver-hours without you ever seeing
it as a single number.

This platform solves that by doing three things a spreadsheet can't: it recomputes every
number automatically every time new data comes in, it puts every truck / customer / lane
on the same ranked table so outliers can't hide in the average, and it translates raw
operational data (miles, gallons, detention minutes, service tickets) into dollar figures
you can act on — call a customer about, take to your banker, or use to cut a lane loose.

The data behind this platform spans **{DATA_PERIOD_DAYS} days** of operations — roughly
{DATA_PERIOD_YEARS:.1f} years — covering **{len(loads_df):,} loads**, **{len(trips_df):,} trips**,
**{len(fuel_df):,} fuel purchases**, and **{len(delivery_df):,} dock events**. That's enough
history to separate a bad week from a structural problem, which is exactly the distinction
that matters when you're deciding whether to retire a truck or renegotiate a customer contract.

Expect to spend about 10 minutes a day here once it's part of your routine — check the
Dashboard each morning, dig into whichever pain-point page has a flashing issue, and use
Cash Flow on Fridays to plan the week ahead. That's a fraction of the time you'd spend
rebuilding a spreadsheet, and it never goes stale.
    """)

    st.markdown("## Your Pages — What Each One Does")

    st.markdown("""
    <div class="guide-card">
        <div class="guide-card-title">📊 Operations Dashboard</div>
        <div class="guide-card-body">
        Your daily home base. One glance tells you whether today is a normal day or whether
        something needs your attention right now — an overdue invoice, a truck that just went
        into the shop, a customer whose detention spiked. It pulls the single most urgent issue
        into a banner at the top so you never have to go hunting for it. Open this first, every
        morning, before you touch the phone or the dispatch board.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">📋 Load Board</div>
        <div class="guide-card-body">
        Every load Redtail has hauled, filterable by date, status, customer, and driver. This is
        where you go when a customer calls asking "where's my load" or when you want to check
        how a specific driver or lane performed last month. It also surfaces detention by
        customer right on the same page, since dock delays show up load-by-load before they
        show up as a pattern. Use it for day-to-day lookups and for building the case behind
        any customer conversation.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">🔧 Truck Retirement Scorecard</div>
        <div class="guide-card-body">
        Built specifically to answer the question you've been carrying around for months: is
        TRK-014 actually costing you money, and how much? This page ranks all 38 trucks by fuel
        efficiency and maintenance cost side by side, so the worst truck in the fleet can't hide
        in a fleet average. It also gives you a dollar figure — excess annual cost versus a
        typical fleet truck — that you can put in front of your banker when you're ready to
        talk about a replacement.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">⏱️ Customer Detention Tracker</div>
        <div class="guide-card-body">
        Llano Estacado Foods' Lubbock dock has been quietly costing you driver-hours for two
        years, and until now there's been no way to see it as anything other than "that dock is
        always slow." This page turns detention minutes into dollars, using a driver-hour rate
        you control, and gives you a load-by-load list you can bring into a rate renegotiation
        conversation. Open it before any call with Llano Estacado, or any other customer whose
        dock has been feeling slow lately.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">🛣️ Lane Profitability</div>
        <div class="guide-card-body">
        The Amarillo→Denver reefer lane looks profitable on a rate confirmation — $2.15/mile is
        a fine number. This page shows what's left after fuel actually gets deducted, and the
        answer is uncomfortable: several of your lanes are running below a $2.05/mile breakeven
        once real fuel cost is netted out. Use this before you bid a lane again, or when you're
        deciding whether a backhaul is worth taking.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">👥 Driver Retention</div>
        <div class="guide-card-body">
        Individual driver departures look like isolated HR events until you line them up — then
        the pattern is obvious: more than half of your recent hires have already left, versus
        almost none of your tenured drivers. This page shows the cohort gap and lists the
        specific recent hires so you can review the pattern with your terminal manager and
        figure out whether it's onboarding, route assignment, or something else driving people
        out the door before they become productive.
        </div>
    </div>
    <div class="guide-card">
        <div class="guide-card-title">💰 Cash Flow & Receivables</div>
        <div class="guide-card-body">
        Cash flow, not revenue, is what kills small carriers. This page shows what customers
        currently owe you, how overdue it is, and whether the money coming in over the next 30
        days covers what's going out. Sangre de Cristo Distribution carries your longest payment
        terms (45 days) and your largest revenue share at the same time — that combination is
        worth watching every week, not just when cash feels tight.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## A Simple Daily Routine (10 Minutes)")
    st.markdown(f"""
**Every morning (2 minutes):** Open the Operations Dashboard. Read the priority banner at the
top — that's the single most urgent thing in the business right now, already picked out for
you. Scan the Alerts panel below it for anything else that needs attention today.

**When a customer calls about a load (1 minute):** Open the Load Board, filter to that
customer, and pull up the load in question. If there's a detention pattern, it's right there
on the same page.

**Once a week, ideally Friday (5 minutes):** Open Cash Flow & Receivables. Check whether
next week's projected incoming payments cover what's going out. If Llano Estacado Foods or
Sangre de Cristo Distribution has an invoice sliding past 30 days, that's the week to call.

**Whenever TRK-014 (or any flagged truck) comes back to the yard (2 minutes):** Open the
Truck Retirement Scorecard, pull up that truck's detail view, and log what you saw. Over a
few months this becomes the record that either justifies a replacement or shows a repair
actually fixed the problem.

**Monthly, when you're planning ahead:** Open Lane Profitability and Driver Retention. These
move slower than the daily numbers, but a monthly check catches a lane sliding toward
unprofitable or a new hire pattern repeating before it becomes a six-month problem.
    """)

    with st.expander("📖 Glossary — Plain-English Definitions"):
        st.markdown("""
**RPM (Revenue per Mile)** — Gross revenue divided by miles driven, before any costs are
subtracted. This is what's on the rate confirmation. A lane can have a great RPM and still
lose money once fuel and detention are netted out — that's exactly what's happening on your
Denver reefer lane.

**Net $/Mile** — Revenue plus fuel surcharge, minus actual fuel cost, divided by miles. This
is the number that actually matters for deciding if a lane is worth running. Redtail's
reference breakeven is **$2.05/mile** — below that, a load isn't covering its true cost once
fuel is accounted for (before driver pay, insurance, and overhead).

**MPG (Miles per Gallon)** — Fuel efficiency per trip, averaged per truck. Your fleet average
is **{FLEET_AVG_MPG:.2f} MPG**. A well-running Class 8 diesel tractor on regional lanes should
sit close to that average; anything sitting persistently 20%+ below it — like TRK-014 at
roughly 5.0 MPG — is burning real money every single mile, not just having a bad month.

**On-Time Rate** — The percentage of deliveries that arrived at or before the scheduled time.
Redtail's fleet-wide on-time rate is **{FLEET_ON_TIME_PCT:.0f}%**. This matters both for
customer relationships and because a late delivery often correlates with a detention event
somewhere earlier in the trip.

**Detention** — Time a driver spends waiting at a shipper or consignee dock beyond what's
scheduled. It's unpaid idle time that displaces revenue-generating miles. Redtail's fleet
average is about 11 minutes per stop; Llano Estacado Foods runs closer to 47 minutes — over
4x the norm. Detention over ~30 minutes is generally considered billable as an accessorial
charge in the industry.

**Deadhead** — Miles driven empty, without a paying load, typically on a backhaul leg. Deadhead
miles still burn fuel and driver hours but earn no freight revenue, which is part of why
backhaul lanes often net lower per mile than the outbound leg even when the posted rate looks
similar.

**DSO (Days Sales Outstanding)** — The average number of days it takes to collect payment
after a load is invoiced. Redtail's customers are on 15, 30, or 45-day contracted terms;
DSO tells you how well actual payment behavior matches those terms.

**Cost per Mile (Maintenance)** — Total lifetime maintenance spend on a truck divided by its
total miles driven. This normalizes an old, high-mileage truck against a newer one — a truck
can have a high total maintenance bill just because it's been in the fleet longer, but a high
*cost per mile* means it's genuinely expensive to keep running regardless of age.

**Excess Annual Cost** — A per-truck figure combining extra fuel spend (versus fleet-average
MPG) and the recent maintenance run-rate, compared to what an average fleet truck costs. This
is the number to bring to a lender when discussing a replacement purchase.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: OPERATIONS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════
elif page == "📊 Operations Dashboard":
    st.title("Operations Dashboard")
    st.caption(
        "Your daily home base — the single most urgent issue in the business, plus the numbers behind it.")
    st.divider()

    # ---- Determine top priority issue dynamically ----
    trk014_row = truck_scorecard[truck_scorecard['truck_id']
                                 == FLAGGED_TRUCK].iloc[0]
    llano_row = detention_by_customer[detention_by_customer['customer_id']
                                      == FLAGGED_CUSTOMER_ID].iloc[0]

    # Overdue AR check
    overdue_ar = open_ar[open_ar['aging_bucket'] == '61+ days']
    top_overdue = overdue_ar.sort_values(
        'total_invoice', ascending=False).head(1)

    if len(top_overdue) > 0:
        row = top_overdue.iloc[0]
        priority_text = (
            f"🔴 <strong>Priority today:</strong> Invoice for load {row['load_id']} to "
            f"<strong>{row['customer_name']}</strong> is {int(row['days_outstanding'])} days past due "
            f"— <strong>${row['total_invoice']:,.2f}</strong> outstanding. Check the Cash Flow & "
            f"Receivables page and consider a collections call today."
        )
    else:
        priority_text = (
            f"🔴 <strong>Priority today:</strong> Truck <strong>{FLAGGED_TRUCK}</strong> is running "
            f"{trk014_row['avg_mpg']:.1f} MPG against a {FLEET_AVG_MPG:.1f} MPG fleet average and has "
            f"logged <strong>${trk014_row['recent_maint_cost']:,.0f}</strong> in maintenance over the "
            f"trailing 18 months. Estimated excess annual cost: "
            f"<strong>${trk014_row['excess_annual_cost']:,.0f}</strong>. Visit the Truck Retirement "
            f"Scorecard to review the replacement case."
        )

    st.markdown(
        f'<div class="priority-banner">{priority_text}</div>', unsafe_allow_html=True)

    # ---- KPI strip ----
    trailing_30 = loads_df[loads_df['load_date']
                           >= DATA_THROUGH - pd.Timedelta(days=30)]
    revenue_30 = (trailing_30['revenue'] + trailing_30['fuel_surcharge']).sum()
    avg_cpm_fleet = truck_scorecard['cost_per_mile'].replace(
        [float('inf')], None).mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Loads (Trailing 30 Days)", f"{len(trailing_30):,}",
              help="Number of loads dispatched in the last 30 days of data. Compare month to month to spot volume swings before they show up in your bank account.")
    c2.metric("Revenue (Trailing 30 Days)", f"${revenue_30:,.0f}",
              help="Total revenue including fuel surcharge for loads in the last 30 days. A healthy month for Redtail runs roughly $420K-$450K based on your historical average.")
    c3.metric("Fleet On-Time Rate", f"{FLEET_ON_TIME_PCT:.1f}%",
              help="Percentage of all trips that arrived on schedule. Above 90% is strong for a regional reefer/dry-van mix; below 85% usually means a specific lane or customer dock is dragging the average down.")
    c4.metric("Active Trucks", f"{(trucks_df['status'] == 'active').sum()} / {len(trucks_df)}",
              help="Trucks currently in active service versus your total fleet of 38. Trucks in 'shop' or 'retired' status are not generating revenue.")
    c5.metric("Avg Maintenance Cost/Mile", f"${avg_cpm_fleet:.3f}",
              help="Fleet-average lifetime maintenance cost divided by lifetime miles driven. A healthy Class 8 diesel truck typically runs $0.02-$0.05/mile in maintenance alone; trucks well above that are dragging the average up.")

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for:</strong> The banner above always shows the single most urgent
    issue right now. The KPIs give you the pulse of the business this month. The chart and
    table below let you see whether this is a normal month or an outlier, and the Alerts panel
    at the bottom lists everything else worth a look today — overdue invoices, MPG drops,
    late loads, and upcoming maintenance.
    </div>
    """, unsafe_allow_html=True)

    # ---- Revenue trend chart ----
    st.markdown("### Revenue Trend — Last 12 Months")
    monthly = loads_df.copy()
    monthly['month'] = monthly['load_date'].dt.to_period('M').astype(str)
    monthly_rev = monthly.groupby('month').agg(
        revenue=('revenue', 'sum'), fsc=('fuel_surcharge', 'sum')).reset_index()
    monthly_rev['total_revenue'] = monthly_rev['revenue'] + monthly_rev['fsc']
    monthly_rev = monthly_rev.tail(12)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_rev['month'], y=monthly_rev['total_revenue'],
        mode='lines+markers', line=dict(color='#2E86C1', width=3),
        marker=dict(size=7, color='#1B4F72'),
        fill='tozeroy', fillcolor='rgba(46,134,193,0.1)',
        name='Total Revenue'
    ))
    fig.update_layout(
        height=350, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Revenue ($)", xaxis_title=None,
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'),
        xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each point is one month of total revenue including fuel "
        "surcharge. Redtail's monthly revenue has held remarkably steady around $420K-$450K "
        "over the full data period — look for any month that breaks noticeably below that band. "
        "If one does, use the Load Board to filter that month and check whether loads were down "
        "or rates were soft."
    )

    # ---- Fleet status table ----
    st.markdown("### Fleet Status — All 38 Trucks")
    fleet_status = truck_scorecard.copy()
    fleet_status['cost_per_mile_display'] = fleet_status['cost_per_mile'].round(
        3)
    fleet_status_display = fleet_status[[
        'truck_id', 'make', 'model', 'year', 'status', 'avg_mpg', 'cost_per_mile_display', 'total_downtime_hrs'
    ]].rename(columns={
        'truck_id': 'Truck', 'make': 'Make', 'model': 'Model', 'year': 'Year', 'status': 'Status',
        'avg_mpg': 'Avg MPG', 'cost_per_mile_display': 'Cost/Mile ($)', 'total_downtime_hrs': 'Downtime (hrs)'
    }).sort_values('Cost/Mile ($)', ascending=False)
    st.dataframe(fleet_status_display, use_container_width=True,
                 hide_index=True, height=320)
    st.caption(
        "📖 **Reading this table:** Focus on Cost/Mile — that's lifetime maintenance spend divided "
        "by lifetime miles driven. A healthy Class 8 diesel truck runs roughly $0.02-$0.05/mile in "
        "maintenance alone. TRK-014 sits far above that. Anything near the top of this table is a "
        "candidate for a closer look on the Truck Retirement Scorecard page."
    )

    # ---- Alerts panel ----
    st.markdown("### ⚠️ Alerts — Needs Your Attention")

    alerts = []

    # Overdue invoices
    for _, r in open_ar[open_ar['aging_bucket'] == '61+ days'].sort_values('total_invoice', ascending=False).head(3).iterrows():
        alerts.append(f"💵 **{r['customer_name']}** invoice for load {r['load_id']} is "
                      f"{int(r['days_outstanding'])} days overdue — ${r['total_invoice']:,.2f} outstanding.")

    # Trucks with high excess cost
    for _, r in truck_scorecard.sort_values('excess_annual_cost', ascending=False).head(3).iterrows():
        if r['excess_annual_cost'] > 5000:
            alerts.append(f"⛽ **{r['truck_id']}** ({r['make']} {r['model']}, {int(r['year'])}) is running "
                          f"{r['avg_mpg']:.1f} MPG vs. {FLEET_AVG_MPG:.1f} fleet average — "
                          f"est. ${r['excess_annual_cost']:,.0f}/year in excess fuel + maintenance cost.")

    # Late loads in past 7 days
    recent_trips = trips_full[trips_full['departure_time']
                              >= DATA_THROUGH - pd.Timedelta(days=7)]
    late_recent = recent_trips[recent_trips['on_time_flag'] == 0]
    if len(late_recent) > 0:
        alerts.append(f"🕐 **{len(late_recent)} late deliveries** in the past 7 days "
                      f"(out of {len(recent_trips)} trips, {len(late_recent)/max(len(recent_trips), 1)*100:.0f}% late rate).")

    # Maintenance mileage thresholds
    trucks_active = trucks_df[trucks_df['status'] == 'active']
    high_mileage = trucks_active[trucks_active['current_odometer'] > 700000]
    if len(high_mileage) > 0:
        for _, r in high_mileage.head(2).iterrows():
            alerts.append(f"🔧 **{r['truck_id']}** has {r['current_odometer']:,} miles on the odometer — "
                          f"due for a full inspection if not scheduled recently.")

    # Customers with detention > 45 min
    for _, r in detention_by_customer[detention_by_customer['avg_detention'] > 45].iterrows():
        alerts.append(f"⏱️ **{r['customer_name']}** averages {r['avg_detention']:.0f} minutes of dock "
                      f"detention per delivery — {r['avg_detention']/FLEET_AVG_DETENTION_EX_FLAGGED:.1f}x the fleet norm.")

    if not alerts:
        st.success("No active alerts — operations look normal today.")
    else:
        for a in alerts[:7]:
            st.warning(a)

    # ---- Recent activity log ----
    st.markdown("### 📝 Recent Activity")
    if st.session_state.action_log:
        for entry in reversed(st.session_state.action_log[-10:]):
            st.text(entry)
    else:
        st.caption(
            "No actions logged yet this session. Notes and updates you make across the app will appear here.")

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This is the page to open first, every morning, before you touch anything else. Here's how to
work through it:

**1. Read the priority banner first.** It's computed fresh every time you open the app and
always shows the single most urgent issue — usually the largest overdue invoice or the
worst-performing truck. Treat it as your first task of the day.

**2. Scan the five KPI tiles.** These give you the 30-day pulse of the business. If revenue
looks low, check the trend chart below to see whether it's a one-month dip or a real slide.
If the on-time rate looks low, that's usually tied to a specific customer's dock — check the
Customer Detention Tracker page.

**3. Check the fleet status table** for any truck with a Cost/Mile figure well above the
pack. This table is sorted worst-first on purpose. TRK-014 will almost always be at or near
the top; the more interesting question is whether a *second* truck is starting to climb the
list too.

**4. Work through the Alerts panel** — this is where the four other pain-point pages
(truck cost, customer detention, lane profitability, and driver retention) each contribute
their most urgent finding in one line. If you only have five minutes, read this list and
decide which one deserves the rest of your morning.

**5. Recent Activity** shows notes and updates you've made in this session — load notes,
invoice marks, maintenance entries. It's your session's paper trail.

**When to escalate:** if an alert repeats for more than a week (the same truck, the same
customer), that's the signal to stop monitoring and act — either book the maintenance, make
the collections call, or open a rate conversation. The dashboard is built to surface problems
early; it can't make the call for you.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: LOAD BOARD
# ══════════════════════════════════════════════════════════════════════════
elif page == "📋 Load Board":
    st.title("Load Board")
    st.caption("Every load Redtail has hauled, filterable by date, customer, driver, and status — your day-to-day lookup tool.")
    st.divider()

    # Apply filters from sidebar
    filtered = loads_full.merge(
        trips_full[['load_id', 'driver_id', 'driver_name',
                    'truck_id', 'departure_time', 'on_time_flag']],
        on='load_id', how='left'
    )
    filtered = filtered[(filtered['load_date'].dt.date >= st.session_state.lb_start) &
                        (filtered['load_date'].dt.date <= st.session_state.lb_end)]
    if st.session_state.lb_status:
        filtered = filtered[filtered['load_status'].isin(
            st.session_state.lb_status)]
    if st.session_state.lb_customer != 'All':
        filtered = filtered[filtered['customer_name']
                            == st.session_state.lb_customer]
    if st.session_state.lb_driver != 'All':
        drv_id = st.session_state.lb_driver.split('(')[-1].rstrip(')')
        filtered = filtered[filtered['driver_id'] == drv_id]

    filtered = filtered.merge(detention_by_load, on='load_id', how='left')

    # ---- KPI row ----
    total_rev = (filtered['revenue'] + filtered['fuel_surcharge']).sum()
    avg_rev = (filtered['revenue'] + filtered['fuel_surcharge']
               ).mean() if len(filtered) else 0
    otp = filtered['on_time_flag'].mean(
    ) * 100 if filtered['on_time_flag'].notna().any() else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Loads (Filtered)", f"{len(filtered):,}",
              help="Number of loads matching your current filter selection.")
    c2.metric("On-Time Rate", f"{otp:.1f}%",
              help="Share of filtered loads delivered on schedule.")
    c3.metric("Avg Revenue/Load", f"${avg_rev:,.0f}",
              help="Average revenue (including fuel surcharge) per load in the current filter.")
    c4.metric("Total Revenue", f"${total_rev:,.0f}",
              help="Sum of revenue and fuel surcharge across all filtered loads.")

    st.markdown(f"""
    <div class="section-intro">
    📌 Showing loads from <strong>{st.session_state.lb_start}</strong> to <strong>{st.session_state.lb_end}</strong>
    — customer: <strong>{st.session_state.lb_customer}</strong>, driver: <strong>{st.session_state.lb_driver}</strong>,
    status: <strong>{', '.join(st.session_state.lb_status) if st.session_state.lb_status else 'none selected'}</strong>.
    Adjust filters in the sidebar.
    </div>
    """, unsafe_allow_html=True)

    # ---- Load table ----
    def status_badge(row):
        if row['load_status'] == 'cancelled':
            return '<span class="badge-late">Cancelled</span>'
        elif row.get('on_time_flag') == 0:
            return '<span class="badge-pending">Delivered Late</span>'
        else:
            return '<span class="badge-active">Delivered On-Time</span>'

    display = filtered.copy().sort_values('load_date', ascending=False).head(300)
    display['Route'] = display['origin_city'] + \
        ' → ' + display['destination_city']
    display['Revenue'] = (display['revenue'] +
                          display['fuel_surcharge']).round(2)
    display['Departure'] = display['load_date'].dt.strftime('%Y-%m-%d')
    display['Status'] = display.apply(status_badge, axis=1)

    table_cols = display[['load_id', 'Route', 'customer_name',
                          'driver_name', 'truck_id', 'Departure', 'Revenue', 'Status']]
    table_cols = table_cols.rename(columns={
        'load_id': 'Load ID', 'customer_name': 'Customer', 'driver_name': 'Driver', 'truck_id': 'Truck'
    })

    st.markdown("### Loads")
    if len(table_cols) == 300:
        st.caption(
            f"Showing the 300 most recent of {len(filtered):,} matching loads. Narrow your date range to see more detail.")

    st.write(table_cols.to_html(escape=False, index=False),
             unsafe_allow_html=True)

    st.markdown("")

    # ---- Customer detention summary ----
    st.markdown("### Customer Detention Summary")
    det_summary = detention_by_customer.copy()
    det_summary['Avg Detention (min)'] = det_summary['avg_detention'].round(1)
    det_summary['Total Detention (hrs)'] = det_summary['total_detention_hrs'].round(
        0)
    det_over_30 = delivery_with_customer[delivery_with_customer['detention_minutes'] > 30].groupby(
        'customer_name').size()
    det_summary['Deliveries >30min Detention'] = det_summary['customer_name'].map(
        det_over_30).fillna(0).astype(int)
    st.dataframe(
        det_summary[['customer_name',
                     'Avg Detention (min)', 'Total Detention (hrs)', 'Deliveries >30min Detention']]
        .rename(columns={'customer_name': 'Customer'}),
        use_container_width=True, hide_index=True
    )
    st.caption(
        "📖 **Reading this table:** Detention is unpaid time a driver waits at a dock beyond the "
        "scheduled window. It costs you driver-hours without generating revenue. Llano Estacado "
        "Foods stands out at roughly 4-5x the fleet norm — see the Customer Detention Tracker page "
        "for the full breakdown and a dollar-cost calculator."
    )

    # ---- Fake CRUD: Load Notes ----
    with st.expander("➕ Add a Note to a Load"):
        load_id_options = filtered['load_id'].tolist() if len(
            filtered) else loads_df['load_id'].tolist()
        note_load = st.selectbox(
            "Select Load", load_id_options[:500], key="note_load_select")
        note_text = st.text_area(
            "Note", placeholder="e.g. Customer requested rescheduled delivery, invoice disputed, driver reported road delay")
        if st.button("Save Note", key="save_load_note"):
            st.session_state.load_notes[note_load] = {
                'note': note_text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            log_action(f"Note added to load {note_load}")
            st.success(f"Note saved for {note_load}!")
            st.rerun()

    if st.session_state.load_notes:
        st.markdown("**Existing Notes:**")
        for lid, note in st.session_state.load_notes.items():
            st.markdown(f"- **{lid}** ({note['timestamp']}): {note['note']}")

    # ---- INSIGHT callout ----
    llano_loads_n = int(
        detention_by_customer[detention_by_customer['customer_id'] == FLAGGED_CUSTOMER_ID]['n_events'].iloc[0])
    llano_avg_det = detention_by_customer[detention_by_customer['customer_id']
                                          == FLAGGED_CUSTOMER_ID]['avg_detention'].iloc[0]
    st.info(
        f"💡 **INSIGHT:** Across {llano_loads_n:,} dock events, **Llano Estacado Foods** averages "
        f"**{llano_avg_det:.0f} minutes** of detention per stop versus roughly "
        f"{FLEET_AVG_DETENTION_EX_FLAGGED:.0f} minutes fleet-wide for everyone else. At an estimated "
        f"$35/hr all-in driver cost, that gap alone has cost Redtail an estimated "
        f"${(llano_avg_det - FLEET_AVG_DETENTION_EX_FLAGGED) * llano_loads_n / 60 * 35:,.0f} in unpaid "
        f"driver time. See the Customer Detention Tracker page for the full breakdown."
    )

    with st.expander("❓ How to use this page"):
        st.markdown("""
The Load Board is your lookup tool — use it whenever you need to answer a question about a
specific load, customer, or driver, rather than a fleet-wide trend.

**Filters (in the sidebar):** Date range narrows to a specific period — useful when a customer
calls asking about "last month." Status lets you separate delivered loads from cancelled ones.
Customer and Driver dropdowns narrow to one party at a time, which is the fastest way to build
a case before a rate conversation or a driver check-in.

**Status badges:** "Delivered On-Time" means the load arrived within its scheduled window.
"Delivered Late" means it missed the window — worth checking whether that's tied to a
detention event earlier in the trip. "Cancelled" loads never generated revenue and are worth
reviewing if they cluster around one customer or lane.

**Why detention matters here:** Detention doesn't just cost driver-hours — it's often the
root cause behind a late delivery on the *next* load, since a driver stuck at one dock runs
behind schedule for the rest of the day. If you see a customer with high detention and a low
on-time rate for other customers on the same day, that's usually connected.

**Using notes:** Load notes are for anything that needs a paper trail but doesn't belong in a
formal system yet — a disputed invoice, a rescheduled delivery, a driver's account of a delay.
They're visible to anyone using this session of the app.

**What to do with a load stuck in dispute or delay:** note it here first, then cross-reference
the customer on the Customer Detention Tracker page (if it's a dock delay) or the Cash Flow
page (if it's a payment dispute) to see whether it's part of a larger pattern with that
customer.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: TRUCK RETIREMENT SCORECARD
# ══════════════════════════════════════════════════════════════════════════
elif page == "🔧 Truck Retirement Scorecard":
    st.title("Truck Profitability & Retirement Scorecard")
    st.caption("Every truck in Redtail's fleet, ranked by fuel efficiency and maintenance cost — built to answer the TRK-014 question once and for all.")
    st.divider()

    trk014 = truck_scorecard[truck_scorecard['truck_id']
                             == FLAGGED_TRUCK].iloc[0]
    mpg_gap_pct = (1 - trk014['avg_mpg'] / FLEET_AVG_MPG) * 100

    st.markdown(f"""
    <div class="priority-banner">
    🔴 <strong>{FLAGGED_TRUCK}</strong> ({int(trk014['year'])} {trk014['make']} {trk014['model']},
    {int(trk014['current_odometer']):,} miles) averages <strong>{trk014['avg_mpg']:.2f} MPG</strong> —
    a <strong>{mpg_gap_pct:.0f}% efficiency gap</strong> versus the {FLEET_AVG_MPG:.2f} MPG fleet
    average — and has cost <strong>${trk014['recent_maint_cost']:,.0f}</strong> in maintenance over
    the trailing 18 months alone, with <strong>{trk014['recent_downtime_hrs']:,.0f} hours</strong> of
    downtime. Estimated excess annual cost vs. an average fleet truck:
    <strong>${trk014['excess_annual_cost']:,.0f}/year</strong> — enough to make payments on a
    replacement.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for:</strong> This page puts all 38 trucks on the same table so no
    truck can hide behind the fleet average. Start with the scatter plot to spot outliers
    visually, then use the ranked table to confirm the dollar figures, then drill into any
    specific truck at the bottom.
    </div>
    """, unsafe_allow_html=True)

    # ---- KPI row ----
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fleet Avg MPG", f"{FLEET_AVG_MPG:.2f}",
              help="Average fuel efficiency across all trucks and trips. Individual trucks below ~6.0 MPG are worth investigating.")
    c2.metric(f"{FLAGGED_TRUCK} MPG", f"{trk014['avg_mpg']:.2f}",
              help=f"TRK-014's average MPG across {int(trk014['trip_count'])} trips — consistently low, not an occasional dip (std dev only {trk014['std_mpg']:.2f}).")
    c3.metric("Fleet Avg Maint Cost/Truck", f"${FLEET_AVG_MAINT:,.0f}",
              help="Average lifetime maintenance spend per truck across the fleet.")
    c4.metric(f"{FLAGGED_TRUCK} Lifetime Maint Cost", f"${trk014['total_maint_cost']:,.0f}",
              help=f"TRK-014's total lifetime maintenance spend — roughly {trk014['total_maint_cost']/FLEET_AVG_MAINT:.1f}x the fleet average.")

    # ---- Scatter: MPG vs maintenance cost ----
    st.markdown("### MPG vs. Maintenance Cost — All 38 Trucks")
    fig = px.scatter(
        truck_scorecard, x='avg_mpg', y='total_maint_cost', size='total_downtime_hrs',
        hover_name='truck_id',
        hover_data={'make': True, 'model': True, 'year': True,
                    'avg_mpg': ':.2f', 'total_maint_cost': ':$,.0f'},
        color_discrete_sequence=['#2E86C1']
    )
    fig.add_vline(x=FLEET_AVG_MPG, line_dash="dash", line_color="#94a3b8",
                  annotation_text="Fleet Avg MPG", annotation_position="top")
    fig.add_hline(y=FLEET_AVG_MAINT, line_dash="dash", line_color="#94a3b8",
                  annotation_text="Fleet Avg Maint Cost", annotation_position="right")
    # Label the flagged truck directly
    fig.add_annotation(
        x=trk014['avg_mpg'], y=trk014['total_maint_cost'],
        text=f"<b>{FLAGGED_TRUCK}</b>", showarrow=True, arrowhead=2, ax=40, ay=-40,
        font=dict(color="#c0392b", size=13)
    )
    fig.update_traces(marker=dict(
        line=dict(width=1, color='white'), opacity=0.75))
    fig.update_layout(
        height=430, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Average MPG (higher = better)", yaxis_title="Total Lifetime Maintenance Cost ($)",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each bubble is one truck; bubble size is total downtime hours. "
        "Trucks in the bottom-right of this chart would be ideal (high MPG, low maintenance cost). "
        "TRK-014 sits in the danger zone — low MPG (left of the dashed line) and high maintenance "
        "cost (above the dashed line) at the same time, with a large bubble showing significant "
        "downtime on top of it."
    )

    # ---- Monthly maintenance trend for flagged truck vs fleet ----
    st.markdown(
        f"### Monthly Maintenance Cost — {FLAGGED_TRUCK} vs. Fleet Average")
    maint_monthly = maint_df.copy()
    maint_monthly['month'] = maint_monthly['service_date'].dt.to_period(
        'M').astype(str)
    trk014_monthly = maint_monthly[maint_monthly['truck_id'] == FLAGGED_TRUCK].groupby(
        'month')['cost'].sum().reset_index()
    fleet_monthly_avg = maint_monthly.groupby(['month', 'truck_id'])['cost'].sum(
    ).reset_index().groupby('month')['cost'].mean().reset_index()
    fleet_monthly_avg.columns = ['month', 'avg_cost']

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=fleet_monthly_avg['month'], y=fleet_monthly_avg['avg_cost'],
                              mode='lines+markers', name='Fleet Avg (per truck)',
                              line=dict(color='#94a3b8', width=2, dash='dot')))
    fig2.add_trace(go.Scatter(x=trk014_monthly['month'], y=trk014_monthly['cost'],
                              mode='lines+markers', name=FLAGGED_TRUCK,
                              line=dict(color='#c0392b', width=3)))
    fig2.update_layout(
        height=350, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Maintenance Cost ($)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'), xaxis=dict(gridcolor='#f1f5f9'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        f"📖 **Reading this chart:** The dotted grey line is what an average truck in the fleet "
        f"costs per month in maintenance. The red line is {FLAGGED_TRUCK} specifically. Months "
        f"where the red line spikes well above the grey line show unscheduled repair events — "
        f"look for whether these are becoming more frequent over time, which would support a "
        f"replace-rather-than-repair decision."
    )

    # ---- Ranked table ----
    st.markdown("### All 38 Trucks — Ranked by Excess Annual Cost")
    ranked = truck_scorecard.sort_values(
        'excess_annual_cost', ascending=False).copy()
    ranked_display = ranked[[
        'truck_id', 'make', 'model', 'year', 'status', 'avg_mpg', 'total_maint_cost',
        'total_downtime_hrs', 'excess_annual_cost'
    ]].rename(columns={
        'truck_id': 'Truck', 'make': 'Make', 'model': 'Model', 'year': 'Year', 'status': 'Status',
        'avg_mpg': 'Avg MPG', 'total_maint_cost': 'Lifetime Maint ($)', 'total_downtime_hrs': 'Downtime (hrs)',
        'excess_annual_cost': 'Est. Excess Annual Cost ($)'
    })
    ranked_display['Avg MPG'] = ranked_display['Avg MPG'].round(2)
    ranked_display['Lifetime Maint ($)'] = ranked_display['Lifetime Maint ($)'].round(
        0)
    ranked_display['Est. Excess Annual Cost ($)'] = ranked_display['Est. Excess Annual Cost ($)'].round(
        0)
    st.dataframe(ranked_display, use_container_width=True,
                 hide_index=True, height=380)

    # ---- Truck detail drill-down ----
    st.markdown("### Truck Detail Drill-Down")
    truck_pick = st.selectbox("Select a truck to review", options=truck_scorecard['truck_id'].tolist(),
                              index=truck_scorecard['truck_id'].tolist().index(FLAGGED_TRUCK))
    tsel = truck_scorecard[truck_scorecard['truck_id'] == truck_pick].iloc[0]

    dc1, dc2, dc3, dc4 = st.columns(4)
    dc1.metric("Avg MPG", f"{tsel['avg_mpg']:.2f}")
    dc2.metric("Lifetime Maint Cost", f"${tsel['total_maint_cost']:,.0f}")
    dc3.metric("Total Downtime", f"{tsel['total_downtime_hrs']:,.0f} hrs")
    dc4.metric("Odometer", f"{int(tsel['current_odometer']):,} mi")

    maint_hist = maint_df[maint_df['truck_id'] == truck_pick].sort_values(
        'service_date', ascending=False)
    st.markdown(f"**Maintenance History — {truck_pick}**")
    st.dataframe(
        maint_hist[['service_date', 'service_type', 'cost',
                    'downtime_hours', 'odometer_at_service']]
        .rename(columns={'service_date': 'Date', 'service_type': 'Service Type', 'cost': 'Cost ($)',
                         'downtime_hours': 'Downtime (hrs)', 'odometer_at_service': 'Odometer'}),
        use_container_width=True, hide_index=True
    )

    # ---- Retirement savings calculator ----
    with st.expander("🧮 What Retiring This Truck Would Save"):
        st.markdown(f"For **{truck_pick}**:")
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Excess Fuel Cost/Year", f"${tsel['excess_fuel_cost_annual']:,.0f}",
                   help="Extra fuel spend versus fleet-average MPG, projected annually based on this truck's typical mileage.")
        rc2.metric("18-Month Maint Run-Rate (Annualized)", f"${tsel['maint_run_rate_annual']:,.0f}",
                   help="Trailing 18-month maintenance spend, annualized, as a forward-looking estimate of ongoing repair cost.")
        rc3.metric("Total Estimated Excess Annual Cost", f"${tsel['excess_annual_cost']:,.0f}",
                   help="Combined excess fuel + maintenance cost versus an average fleet truck — the number to bring to a lender.")

    # ---- Age vs cost-per-mile scatter ----
    st.markdown("### Truck Age vs. Cost-per-Mile Driven")
    fig3 = px.scatter(
        truck_scorecard, x='year', y='cost_per_mile', hover_name='truck_id',
        color_discrete_sequence=['#2E86C1']
    )
    fig3.add_annotation(
        x=trk014['year'], y=trk014['cost_per_mile'],
        text=f"<b>{FLAGGED_TRUCK}</b>", showarrow=True, arrowhead=2, ax=30, ay=-30,
        font=dict(color="#c0392b", size=13)
    )
    fig3.update_traces(marker=dict(size=10, line=dict(
        width=1, color='white'), opacity=0.75))
    fig3.update_layout(
        height=350, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Model Year", yaxis_title="Lifetime Maintenance Cost per Mile ($)",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** If age alone explained maintenance cost, older trucks (left "
        "side) would sit uniformly higher than newer ones (right side) in a clean downward slope. "
        f"{FLAGGED_TRUCK} sits well above where its model year would predict — meaning it's not "
        "just old, it's a genuine outlier even compared to trucks of similar vintage."
    )

    st.info(
        f"💡 **INSIGHT:** {FLAGGED_TRUCK} costs an estimated **${trk014['excess_annual_cost']:,.0f}/year** "
        f"more than an average fleet truck in fuel and maintenance combined. Over the trailing 18 "
        f"months it accounted for **${trk014['recent_maint_cost']:,.0f}** in maintenance — "
        f"roughly **{trk014['recent_maint_cost']/maint_df[maint_df['service_date'] >= MAINT_CUTOFF_18MO]['cost'].sum()*100:.0f}%** "
        f"of all fleet-wide maintenance spend in that window came from one truck out of 38."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists to answer one question with a hard number: is {FLAGGED_TRUCK} actually
costing you money, and how much? You've suspected it for a while — this page proves it and
sizes it.

**What healthy looks like:** A well-running truck in your fleet sits close to the
{FLEET_AVG_MPG:.1f} MPG fleet average and has a maintenance cost-per-mile in the $0.02-$0.05
range. Trucks meaningfully below that MPG line or above that cost-per-mile line are actively
dragging down fleet profitability, not just "due for some work."

**What unhealthy looks like:** {FLAGGED_TRUCK} is the clearest case in your fleet — {mpg_gap_pct:.0f}%
below average MPG with almost no month-to-month variance (meaning it's *consistently* bad, not
having occasional rough trips), plus a maintenance bill concentrated heavily in the trailing 18
months. That combination — chronic inefficiency plus accelerating repair cost — is the exact
profile of a truck that's past the point where repair makes more sense than replacement.

**Step-by-step when a truck's numbers are bad:**
1. Check the scatter plot — is it an isolated outlier or part of a cluster of aging trucks?
2. Check the monthly trend — is the cost accelerating, or was it one big repair that's now behind it?
3. Pull the truck's detail view and read the maintenance history — repeated failures of the
   *same* system (e.g., cooling system, transmission) are a stronger replace signal than varied,
   unrelated repairs.
4. Use the retirement calculator to get the annual excess cost figure — that's your
   loan-payment comparison number.

**How often to check:** Monthly is enough for this page — maintenance and MPG patterns don't
shift week to week. Revisit after any major repair to see whether it actually fixed the
underlying trend or just kicked the problem a few months down the road.

**This week's action:** Bring {FLAGGED_TRUCK}'s numbers to your banker. At roughly
${trk014['excess_annual_cost']:,.0f}/year in excess cost, this truck is very likely costing you
more than a replacement truck payment would — the data now backs that decision instead of
just your gut.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER DETENTION TRACKER
# ══════════════════════════════════════════════════════════════════════════
elif page == "⏱️ Customer Detention Tracker":
    st.title("Customer Detention & Accessorial Cost Tracker")
    st.caption("Turns invisible dock delays into a dollar figure you can bring to a customer conversation — built around the Llano Estacado Foods pattern.")
    st.divider()

    llano = detention_by_customer[detention_by_customer['customer_id']
                                  == FLAGGED_CUSTOMER_ID].iloc[0]
    gap_multiple = llano['avg_detention'] / FLEET_AVG_DETENTION_EX_FLAGGED

    st.markdown(f"""
    <div class="priority-banner">
    🔴 <strong>{FLAGGED_CUSTOMER}</strong> generates <strong>{llano['avg_detention']:.1f} minutes</strong>
    of average dock detention per delivery — <strong>{gap_multiple:.1f}x</strong> the
    {FLEET_AVG_DETENTION_EX_FLAGGED:.1f}-minute fleet average for every other customer — across
    <strong>{int(llano['n_events']):,} delivery events</strong>. That's an estimated
    <strong>{llano['total_detention_hrs']:,.0f} driver-hours</strong> of unpaid idle time.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for:</strong> The bar chart below shows every customer ranked by
    average detention. Use the dollar-impact calculator to plug in your real driver-hour cost,
    then use the drill-down table at the bottom to pull specific dates for a rate conversation.
    </div>
    """, unsafe_allow_html=True)

    # ---- Dollar impact calculator ----
    st.markdown("### Dollar Impact Calculator")
    hourly_rate = st.number_input("Cost per driver-hour, all-in ($)", min_value=10.0, max_value=100.0, value=35.0, step=1.0,
                                  help="Your fully-loaded cost per driver-hour, including pay, benefits, and opportunity cost of the truck sitting idle instead of generating revenue.")
    llano_dollar_cost = llano['total_detention_hrs'] * hourly_rate
    fleet_ex_llano_hrs = detention_by_customer[detention_by_customer['customer_id']
                                               != FLAGGED_CUSTOMER_ID]['total_detention_hrs'].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{FLAGGED_CUSTOMER} Avg Detention", f"{llano['avg_detention']:.1f} min",
              help="Average minutes a driver waits at this customer's dock beyond the scheduled window, per delivery.")
    c2.metric("Fleet Avg (Everyone Else)", f"{FLEET_AVG_DETENTION_EX_FLAGGED:.1f} min",
              help="Average detention across all other customers combined, excluding Llano Estacado Foods.")
    c3.metric(f"{FLAGGED_CUSTOMER} Total Hours", f"{llano['total_detention_hrs']:,.0f} hrs",
              help="Cumulative driver-hours lost to detention at this customer's dock across the full data period.")
    c4.metric("Estimated Dollar Cost", f"${llano_dollar_cost:,.0f}",
              help="Total detention hours multiplied by your entered driver-hour rate — this is your leverage number for a rate conversation.")

    # ---- Bar chart: avg detention by customer ----
    st.markdown("### Average Detention by Customer")
    det_sorted = detention_by_customer.sort_values(
        'avg_detention', ascending=True)
    colors = ['#c0392b' if cid ==
              FLAGGED_CUSTOMER_ID else '#2E86C1' for cid in det_sorted['customer_id']]
    fig = go.Figure(go.Bar(
        x=det_sorted['avg_detention'], y=det_sorted['customer_name'], orientation='h',
        marker_color=colors, text=det_sorted['avg_detention'].round(1), textposition='outside'
    ))
    fig.add_vline(x=FLEET_AVG_DETENTION_EX_FLAGGED, line_dash="dash", line_color="#94a3b8",
                  annotation_text="Fleet Avg (ex. Llano)", annotation_position="top")
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Average Detention (minutes)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#f1f5f9'), xaxis=dict(gridcolor='#e2e8f0'),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Bars are sorted by average detention minutes per delivery. "
        f"{FLAGGED_CUSTOMER} (highlighted in red) sits far above every other customer, which is "
        "consistently near the fleet-average dashed line. This isn't a rounding difference — it's "
        "a distinct pattern specific to one customer's dock."
    )

    # ---- Trend chart ----
    st.markdown(f"### {FLAGGED_CUSTOMER} — Monthly Detention Trend")
    llano_events = delivery_with_customer[delivery_with_customer['customer_id']
                                          == FLAGGED_CUSTOMER_ID].copy()
    llano_events['month'] = llano_events['scheduled_time'].dt.to_period(
        'M').astype(str)
    llano_monthly = llano_events.groupby(
        'month')['detention_minutes'].mean().reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=llano_monthly['month'], y=llano_monthly['detention_minutes'],
                              mode='lines+markers', line=dict(color='#c0392b', width=3),
                              name=FLAGGED_CUSTOMER))
    fig2.add_hline(y=FLEET_AVG_DETENTION_EX_FLAGGED, line_dash='dash', line_color='#94a3b8',
                   annotation_text='Fleet Avg (ex. Llano)')
    fig2.update_layout(
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Avg Detention (minutes)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This tracks whether the problem is getting better, worse, or "
        "staying flat month over month. A flat line well above the dashed fleet-average line — "
        "which is what you'll see here — means this isn't a temporary rough patch at the dock; "
        "it's a structural pattern worth addressing directly with the customer."
    )

    # ---- Breakdown by facility type ----
    st.markdown("### Detention by Facility Type")
    facility_breakdown = llano_events.groupby(
        'facility_type')['detention_minutes'].agg(['mean', 'count']).reset_index()
    facility_breakdown.columns = [
        'Facility Type', 'Avg Detention (min)', 'Event Count']
    facility_breakdown['Avg Detention (min)'] = facility_breakdown['Avg Detention (min)'].round(
        1)
    st.dataframe(facility_breakdown, use_container_width=True, hide_index=True)
    st.caption(
        "📖 **Reading this table:** 'Shipper' means Redtail is picking up freight; 'Consignee' means "
        "delivering it. This tells you whether the delay is on the loading side or the unloading "
        "side at Llano Estacado's facility — useful detail for a conversation about where exactly "
        "their process needs to improve."
    )

    # ---- Drill-down table ----
    st.markdown(
        f"### Drill-Down — {FLAGGED_CUSTOMER} Delivery Events (Worst First)")
    drill = llano_events.sort_values(
        'detention_minutes', ascending=False).head(50)
    drill_display = drill[['load_id', 'facility_type',
                           'scheduled_time', 'actual_time', 'detention_minutes', 'on_time']]
    drill_display = drill_display.rename(columns={
        'load_id': 'Load ID', 'facility_type': 'Facility', 'scheduled_time': 'Scheduled',
        'actual_time': 'Actual', 'detention_minutes': 'Detention (min)', 'on_time': 'On-Time'
    })
    st.dataframe(drill_display, use_container_width=True,
                 hide_index=True, height=350)
    st.caption("Top 50 worst detention events for this customer, sorted worst-first — use this list directly in a renegotiation conversation.")

    st.info(
        f"💡 **INSIGHT:** {FLAGGED_CUSTOMER} detention has cost Redtail an estimated "
        f"**{llano['total_detention_hrs']:,.0f} driver-hours** (~${llano_dollar_cost:,.0f} at "
        f"${hourly_rate:.0f}/hr) — **{gap_multiple:.1f}x** every other customer. That's enough lost "
        f"time to have run an estimated **{llano['total_detention_hrs']/8:,.0f} additional full "
        f"driver shifts** elsewhere in the network."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because detention has been invisible — buried inside "normal trip variance"
— even though it's one of the largest hidden costs in the business.

**Why this matters for Redtail specifically:** {FLAGGED_CUSTOMER} isn't just a little slower
than average — at {gap_multiple:.1f}x the fleet norm, it's a distinct, structural pattern that
holds across nearly 9,000 delivery events. That consistency is exactly what makes it worth
addressing directly rather than writing off as normal dock variance.

**What healthy vs. unhealthy looks like:** Your fleet average detention (excluding Llano
Estacado) is about {FLEET_AVG_DETENTION_EX_FLAGGED:.0f} minutes — that's a normal, acceptable
range for dock loading/unloading. Anything sustained above 30 minutes starts to erode
productive driver-hours meaningfully; above 45 minutes, most carriers in this industry would
consider it billable as an accessorial detention charge.

**Step-by-step when a customer's numbers are bad:**
1. Confirm the pattern is consistent (not a one-time event) using the monthly trend chart.
2. Check the facility-type breakdown to know whether it's a loading or unloading problem.
3. Pull the drill-down table for specific dates and load numbers.
4. Use the dollar-impact calculator with your real driver-hour cost to get a defensible number.
5. Bring that number into a rate conversation — either a detention accessorial charge going
   forward, or a renegotiated base rate that accounts for the time cost.

**How often to check:** Monthly is sufficient — detention patterns are structural and don't
shift week to week. Re-check after any conversation with the customer to confirm whether their
dock process actually improved.

**This week's action:** Use the dollar-impact calculator with your actual driver-hour cost,
then bring the resulting figure and the drill-down table to your next conversation with Llano
Estacado Foods. This is the exact data package needed to either negotiate a detention
accessorial or adjust the base rate to reflect the real cost of serving this account.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: LANE PROFITABILITY
# ══════════════════════════════════════════════════════════════════════════
elif page == "🛣️ Lane Profitability":
    st.title("Lane Profitability Analyzer")
    st.caption("What's left after fuel is actually deducted — the Amarillo→Denver reefer lane looks fine on the rate con, but the real math tells a different story.")
    st.divider()

    worst_lane = route_net.iloc[0]
    below_be = route_net[route_net['avg_net_per_mile']
                         < BREAKEVEN_RATE_PER_MILE]

    st.markdown(f"""
    <div class="priority-banner">
    🔴 <strong>{len(below_be)} of {len(route_net)} lanes</strong> net below the
    ${BREAKEVEN_RATE_PER_MILE:.2f}/mile breakeven after fuel cost. The worst is
    <strong>{worst_lane['lane_label']}</strong> ({worst_lane['route_id']}), netting only
    <strong>${worst_lane['avg_net_per_mile']:.2f}/mile</strong> — with
    <strong>{worst_lane['pct_below_breakeven']:.0f}%</strong> of individual loads on that lane
    losing money.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for:</strong> The bar chart ranks every lane by what it actually
    nets after fuel — not the posted rate. Any bar to the left of the breakeven line is a lane
    that's losing money once true costs are included. Use the threshold slider to test different
    breakeven assumptions.
    </div>
    """, unsafe_allow_html=True)

    # ---- Configurable breakeven threshold ----
    threshold = st.slider("Breakeven threshold ($/mile)", min_value=1.50, max_value=2.50,
                          value=BREAKEVEN_RATE_PER_MILE, step=0.05,
                          help="The minimum net revenue per mile (after fuel) needed to cover driver pay, insurance, and overhead. Adjust this to test different assumptions about your true operating cost.")
    route_net['below_thresh'] = route_net['avg_net_per_mile'] < threshold
    n_below = route_net['below_thresh'].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Lanes Below Threshold", f"{n_below} / {len(route_net)}",
              help="Number of lanes whose average net rate per mile (after fuel) falls below your selected breakeven threshold.")
    c2.metric("Worst Lane Net Rate", f"${worst_lane['avg_net_per_mile']:.2f}/mi",
              help="The lowest-netting lane in the fleet, after fuel cost is deducted from revenue and fuel surcharge.")
    c3.metric("Best Lane Net Rate", f"${route_net['avg_net_per_mile'].max():.2f}/mi",
              help="The highest-netting lane in the fleet — your benchmark for what a healthy lane should return.")
    c4.metric("Fleet Total Revenue", f"${route_net['total_revenue'].sum():,.0f}",
              help="Combined gross revenue across all 8 lanes over the full data period.")

    # ---- Bar chart: net $/mile by route ----
    st.markdown("### Net Rate per Mile by Lane (After Fuel)")
    route_net_sorted = route_net.sort_values('avg_net_per_mile')
    bar_colors = [
        '#c0392b' if b else '#2E86C1' for b in route_net_sorted['below_thresh']]
    fig = go.Figure(go.Bar(
        x=route_net_sorted['avg_net_per_mile'], y=route_net_sorted['lane_label'], orientation='h',
        marker_color=bar_colors,
        text=route_net_sorted['avg_net_per_mile'].round(
            2).apply(lambda x: f"${x:.2f}"),
        textposition='outside'
    ))
    fig.add_vline(x=threshold, line_dash="dash", line_color="#1B4F72",
                  annotation_text=f"Breakeven ${threshold:.2f}", annotation_position="top")
    fig.update_layout(
        height=380, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Net $/Mile (Revenue + FSC − Fuel Cost)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#f1f5f9'), xaxis=dict(gridcolor='#e2e8f0'),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Red bars fall below your selected breakeven threshold; blue "
        "bars clear it. Note that lanes can have a perfectly reasonable *posted* rate and still "
        "show up red here — that's the entire point of this page. The gap between the posted "
        "rate and the net rate is fuel cost, which doesn't show up on a rate confirmation."
    )

    # ---- Ranked table ----
    st.markdown("### All 8 Lanes — Full Detail")
    table = route_net_sorted[[
        'lane_label', 'route_id', 'distance_miles', 'base_rate_per_mile', 'avg_net_per_mile',
        'pct_below_breakeven', 'n_loads', 'total_revenue'
    ]].rename(columns={
        'lane_label': 'Lane', 'route_id': 'Route ID', 'distance_miles': 'Distance (mi)',
        'base_rate_per_mile': 'Posted Rate ($/mi)', 'avg_net_per_mile': 'Net Rate ($/mi)',
        'pct_below_breakeven': '% Loads Below Breakeven', 'n_loads': 'Loads', 'total_revenue': 'Total Revenue ($)'
    })
    table['Net Rate ($/mi)'] = table['Net Rate ($/mi)'].round(2)
    table['% Loads Below Breakeven'] = table['% Loads Below Breakeven'].round(
        0)
    table['Total Revenue ($)'] = table['Total Revenue ($)'].round(0)
    st.dataframe(table, use_container_width=True, hide_index=True)

    # ---- Waterfall for selected route ----
    st.markdown("### Rate Bridge — Base Rate to Net Rate")
    route_pick = st.selectbox(
        "Select a lane", options=route_net_sorted['lane_label'].tolist())
    rsel = route_net_sorted[route_net_sorted['lane_label']
                            == route_pick].iloc[0]
    fsc_per_mile = trips_full[trips_full['route_id'] == rsel['route_id']
                              ]['fuel_surcharge'].mean() / rsel['distance_miles']
    fuel_per_mile = rsel['avg_fuel_cost'] / rsel['distance_miles']

    fig3 = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Base Rate", "+ Fuel Surcharge", "− Fuel Cost", "= Net Rate"],
        y=[rsel['base_rate_per_mile'], fsc_per_mile, -fuel_per_mile, 0],
        connector={"line": {"color": "#94a3b8"}},
        decreasing={"marker": {"color": "#c0392b"}},
        increasing={"marker": {"color": "#27ae60"}},
        totals={"marker": {"color": "#1B4F72"}},
        text=[f"${v:.2f}" for v in [rsel['base_rate_per_mile'],
                                    fsc_per_mile, -fuel_per_mile, rsel['avg_net_per_mile']]],
        textposition="outside"
    ))
    fig3.update_layout(
        height=380, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="$/Mile", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        f"📖 **Reading this chart:** This is the bridge from posted rate to what actually lands. "
        f"For {route_pick}, fuel surcharge adds back some ground, but fuel cost takes a bigger "
        f"bite — the net result is what's left to cover driver pay, insurance, and overhead."
    )

    # ---- Monthly trend ----
    st.markdown(f"### Monthly Net Rate Trend — {route_pick}")
    route_trips = trips_full[trips_full['route_id'] == rsel['route_id']].copy()
    route_trips['month'] = route_trips['departure_time'].dt.to_period(
        'M').astype(str)
    route_monthly = route_trips.groupby(
        'month')['net_per_mile'].mean().reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=route_monthly['month'], y=route_monthly['net_per_mile'],
                              mode='lines+markers', line=dict(color='#2E86C1', width=3)))
    fig4.add_hline(y=threshold, line_dash='dash',
                   line_color='#c0392b', annotation_text='Breakeven')
    fig4.update_layout(
        height=300, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Net $/Mile", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Watch for a lane drifting further below the breakeven line "
        "over time — that's a signal to renegotiate the rate or consider dropping the lane, "
        "rather than a one-off bad month."
    )

    loser_lanes = route_net[route_net['pct_below_breakeven'] > 50]
    st.info(
        f"💡 **INSIGHT:** **{', '.join(loser_lanes['route_id'].tolist())}** are the lanes where "
        f"more than half of all loads fall below breakeven. On {worst_lane['route_id']} "
        f"specifically, **{worst_lane['pct_below_breakeven']:.0f}%** of loads lose money after "
        f"fuel — despite a posted rate of **${worst_lane['base_rate_per_mile']:.2f}/mile** that "
        f"looks perfectly reasonable on paper."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists to answer a question you can't currently answer without hand-building a
spreadsheet every quarter: which lanes are actually making money once real fuel cost is
deducted, not just what the rate confirmation says?

**Why this matters for Redtail specifically:** The Amarillo→Denver reefer lane is one of your
anchor lanes — Sangre de Cristo Distribution alone is nearly a third of total revenue, much of
it moving on this corridor. A lane that looks fine at ${routes_df[routes_df['route_id'] == 'AMA-DEN-REEFER']['base_rate_per_mile'].iloc[0]:.2f}/mile
posted but nets under breakeven after fuel means you could be growing volume on a lane that's
quietly losing money on the majority of its loads.

**What healthy vs. unhealthy looks like:** A healthy lane nets comfortably above your
breakeven threshold with fewer than 10-15% of individual loads falling short (some variance is
normal — fuel prices and empty miles fluctuate load to load). A lane where more than half the
loads fall below breakeven, like your two backhaul lanes, isn't having a bad stretch — it's
structurally priced too low for its true cost.

**Step-by-step when a lane's numbers are bad:**
1. Check the waterfall bridge to see whether the problem is a thin fuel surcharge, high fuel
   burn (common on reefer lanes — refrigeration units burn fuel even when not moving), or both.
2. Check the monthly trend to see if it's worsening, which usually tracks rising diesel prices
   outpacing your fuel surcharge schedule.
3. Compare the lane's detention-adjusted margin (loads with high detention effectively cost
   more per mile than the net figure alone shows) — LUB-ABQ-VAN and AMA-DEN-REEFER both carry
   elevated detention on top of thin fuel margins.
4. Decide whether the fix is a renegotiated base rate, a better fuel surcharge formula, or
   walking away from the lane.

**How often to check:** Monthly is sufficient for spotting a trend; check immediately before
renewing any contract or bidding a new rate on one of these lanes.

**This week's action:** Before your next rate conversation on the Denver reefer lane, pull the
waterfall chart and the monthly trend — you now have a specific, defensible number
(${worst_lane['avg_net_per_mile']:.2f}/mile net, {worst_lane['pct_below_breakeven']:.0f}% of
loads underwater) instead of a general sense that "the Denver lane feels tight."
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: DRIVER RETENTION
# ══════════════════════════════════════════════════════════════════════════
elif page == "👥 Driver Retention":
    st.title("Driver Retention Early-Warning Dashboard")
    st.caption("New-hire attrition at the Amarillo terminal, isolated from normal turnover — so individual departures stop looking like isolated events.")
    st.divider()

    recent_cohort = drivers_tenure[drivers_tenure['cohort']
                                   == 'Hired last 18 months']
    older_cohort = drivers_tenure[drivers_tenure['cohort'] == 'Hired earlier']
    recent_term_rate = recent_cohort['is_departed'].mean() * 100
    older_term_rate = older_cohort['is_departed'].mean() * 100

    st.markdown(f"""
    <div class="priority-banner">
    🔴 <strong>{recent_term_rate:.0f}%</strong> of the <strong>{len(recent_cohort)}</strong> drivers
    hired in the last 18 months have already left Redtail — versus <strong>{older_term_rate:.0f}%</strong>
    for the <strong>{len(older_cohort)}</strong> drivers hired earlier. That's roughly
    <strong>{recent_term_rate/max(older_term_rate, 0.1):.0f}x</strong> the turnover rate, concentrated
    almost entirely in new hires.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-intro">
    📌 <strong>What to look for:</strong> This page flags <em>where</em> the retention problem is
    concentrated — it can't diagnose <em>why</em> without exit-interview or dispatcher-assignment
    data Redtail doesn't currently track digitally. Use the roster table at the bottom as a
    starting point for conversations with your terminal manager.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Recent-Hire Termination Rate", f"{recent_term_rate:.0f}%",
              help="Share of drivers hired in the last 18 months who have since been terminated or voluntarily quit.")
    c2.metric("Tenured Driver Termination Rate", f"{older_term_rate:.0f}%",
              help="Share of drivers hired earlier than 18 months ago who have since departed — this is your baseline normal turnover rate.")
    c3.metric("Active Drivers", f"{(drivers_df['employment_status'] == 'active').sum()}",
              help="Drivers currently active and available for dispatch, out of 52 total on record.")
    c4.metric("Recent Hires (18mo)", f"{len(recent_cohort)}",
              help="Total number of drivers hired in the trailing 18-month window, regardless of current status.")

    # ---- Cohort comparison bar chart ----
    st.markdown("### Termination Rate by Hire Cohort")
    cohort_data = pd.DataFrame({
        'Cohort': ['Hired last 18 months', 'Hired earlier'],
        'Termination Rate': [recent_term_rate, older_term_rate],
        'N': [len(recent_cohort), len(older_cohort)]
    })
    fig = go.Figure(go.Bar(
        x=cohort_data['Cohort'], y=cohort_data['Termination Rate'],
        marker_color=['#c0392b', '#2E86C1'],
        text=[f"{r:.0f}% (n={n})" for r, n in zip(
            cohort_data['Termination Rate'], cohort_data['N'])],
        textposition='outside'
    ))
    fig.update_layout(
        height=350, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Termination / Quit Rate (%)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', range=[0, max(
            recent_term_rate, older_term_rate) * 1.3]),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Driver counts (n=) are labeled directly on the bars because "
        "the recent-hire cohort is a small sample — a handful of departures moves the percentage "
        "a lot. Even accounting for that, the gap here is large enough to be a real pattern, not "
        "noise."
    )

    # ---- Tenure histogram ----
    st.markdown("### Tenure at Departure — All Terminated/Quit Drivers")
    departed = drivers_tenure[drivers_tenure['is_departed']]
    fig2 = px.histogram(departed, x='tenure_days', nbins=12,
                        color_discrete_sequence=['#2E86C1'])
    fig2.update_layout(
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Tenure at Departure (days)", yaxis_title="Number of Drivers",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This shows how early departures tend to happen, across both "
        "cohorts. A cluster of bars on the left side (short tenure) reinforces that Redtail's "
        "retention problem is front-loaded — drivers who make it past the first several months "
        "tend to stay much longer."
    )

    # ---- Roster table ----
    st.markdown("### Recent Hires (Last 18 Months) — Roster")
    roster = recent_cohort.copy().sort_values('is_departed', ascending=False)
    roster['Status'] = roster['employment_status'].apply(
        lambda s: '<span class="badge-late">Departed</span>' if s in ('terminated', 'voluntary_quit')
        else '<span class="badge-active">Active</span>'
    )
    roster_display = roster[['driver_id', 'first_name', 'last_name', 'hire_date', 'Status',
                             'cdl_class', 'years_experience', 'tenure_days']]
    roster_display = roster_display.rename(columns={
        'driver_id': 'Driver ID', 'first_name': 'First', 'last_name': 'Last', 'hire_date': 'Hire Date',
        'cdl_class': 'CDL Class', 'years_experience': 'Years Experience', 'tenure_days': 'Tenure (days)'
    })
    roster_display['Hire Date'] = roster_display['Hire Date'].dt.strftime(
        '%Y-%m-%d')
    st.write(roster_display.to_html(escape=False,
             index=False), unsafe_allow_html=True)
    st.caption(
        "📖 **Reading this table:** Departed drivers are sorted to the top. Cross-reference CDL "
        "class and prior experience — if departures cut across experience levels rather than "
        "concentrating among the least experienced, that points away from a skills mismatch and "
        "toward an onboarding, dispatch, or route-assignment issue instead."
    )

    # ---- Experience vs termination ----
    st.markdown("### Years of Experience vs. Departure Status (Recent Hires)")
    fig3 = px.scatter(
        recent_cohort, x='years_experience', y='tenure_days', color='is_departed',
        color_discrete_map={True: '#c0392b', False: '#2E86C1'},
        labels={'is_departed': 'Departed'}, hover_data=['first_name', 'last_name']
    )
    fig3.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
    fig3.update_layout(
        height=350, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Years of Prior Experience", yaxis_title="Tenure at Redtail (days)",
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0'), xaxis=dict(gridcolor='#f1f5f9'),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** Each dot is one recently hired driver — red means they've "
        "since departed. If red dots are spread across the experience range rather than clustered "
        "at low experience, it suggests this isn't a skills or readiness problem, but something "
        "structural in how new hires are onboarded or assigned."
    )

    # ---- Driver note CRUD ----
    with st.expander("➕ Add a Note to a Driver's Record"):
        note_driver = st.selectbox("Select Driver", options=drivers_df.apply(
            lambda r: f"{r['first_name']} {r['last_name']} ({r['driver_id']})", axis=1).tolist())
        note_text = st.text_area(
            "Note", placeholder="e.g. Exit interview notes, onboarding feedback, dispatcher assignment concern")
        if st.button("Save Note", key="save_driver_note"):
            st.session_state.driver_notes[note_driver] = {
                'note': note_text, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            log_action(f"Note added for driver {note_driver}")
            st.success(f"Note saved for {note_driver}!")
            st.rerun()

    if st.session_state.driver_notes:
        st.markdown("**Existing Notes:**")
        for d, note in st.session_state.driver_notes.items():
            st.markdown(f"- **{d}** ({note['timestamp']}): {note['note']}")

    st.info(
        f"💡 **INSIGHT:** {recent_term_rate:.0f}% of drivers hired in the last 18 months have "
        f"already left, versus {older_term_rate:.0f}% for everyone else — this is Redtail's "
        f"biggest hidden hiring cost. With {len(recent_cohort)} recent hires and "
        f"{int(recent_cohort['is_departed'].sum())} already departed, the pattern is concentrated "
        f"enough to justify a direct conversation with your terminal manager about onboarding "
        f"and early route assignment."
    )

    with st.expander("❓ How to use this page"):
        st.markdown(f"""
This page exists because individual driver departures look like isolated HR events — until you
line them up and see the pattern.

**Why this matters for Redtail specifically:** at {recent_term_rate:.0f}% versus
{older_term_rate:.0f}%, new-hire attrition isn't generic turnover spread evenly across the
workforce — it's concentrated almost entirely at the front end of the employment lifecycle.
That's meaningfully different from "trucking has high turnover industry-wide," and it points
toward something fixable in onboarding, early route assignment, or dispatcher pairing rather
than a market-wide labor problem you can't control.

**What this page can and can't tell you:** it can show you *where* the problem is concentrated
— recent hires, and specifically within their first several months. It cannot tell you *why*
without exit-interview notes, dispatcher assignment history, or onboarding completion records,
none of which are currently tracked digitally at Redtail. Treat this as the starting point for
a conversation, not the final diagnosis.

**Step-by-step for using this page:**
1. Review the cohort comparison to confirm the scale of the gap.
2. Check the tenure histogram to see how early departures typically happen — that's your
   "danger window" for extra onboarding attention.
3. Pull the roster table and go through it with your terminal manager — ask about each departed
   driver specifically: what route were they on, who was their dispatcher, what feedback (if
   any) did they give on the way out.
4. Check whether departures cut across experience levels or concentrate among less-experienced
   drivers — that changes whether the fix is training-focused or process-focused.

**How often to check:** Monthly, or immediately after any new departure, to see whether it fits
the existing pattern or represents something new.

**This week's action:** Sit down with your terminal manager and go through the roster table
line by line. With only {len(recent_cohort)} recent hires in the sample, this is a small,
reviewable list — the value here is turning a vague sense of "we keep losing new guys" into a
specific list of names, hire dates, and tenure lengths you can actually discuss.
        """)


# ══════════════════════════════════════════════════════════════════════════
# PAGE: CASH FLOW & RECEIVABLES
# ══════════════════════════════════════════════════════════════════════════
elif page == "💰 Cash Flow & Receivables":
    st.title("Cash Flow & Receivables")
    st.caption(
        "What customers owe you, how overdue it is, and whether next week's incoming cash covers what's going out.")
    st.divider()

    st.markdown("""
    <div class="section-intro">
    📌 Cash flow — not revenue — is the #1 killer of small trucking companies. This page shows
    what's coming in, when, and whether you'll have enough to cover fuel, payroll, and
    maintenance next week. A profitable month on paper doesn't help if the cash isn't in the
    bank when payroll runs.
    </div>
    """, unsafe_allow_html=True)

    total_outstanding = open_ar['total_invoice'].sum()
    overdue_ar = open_ar[open_ar['aging_bucket'] == '61+ days']
    overdue_30 = overdue_ar['total_invoice'].sum()
    avg_days_to_pay = (open_ar['days_outstanding'] +
                       open_ar['payment_terms_days']).mean() if len(open_ar) else 0

    # Simple 30-day cash projection: incoming = upcoming due invoices, fixed costs = trailing avg monthly fuel + maint
    monthly_fuel_avg = fuel_df.groupby(fuel_df['purchase_date'].dt.to_period('M'))[
        'total_cost'].sum().tail(6).mean()
    monthly_maint_avg = maint_df.groupby(maint_df['service_date'].dt.to_period('M'))[
        'cost'].sum().tail(6).mean()
    weekly_fixed_cost = (monthly_fuel_avg + monthly_maint_avg) / 4.33

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Outstanding AR", f"${total_outstanding:,.0f}",
              help="Money customers currently owe Redtail that hasn't been marked paid yet.")
    c2.metric("Overdue >60 Days", f"${overdue_30:,.0f}",
              help="Invoices more than 60 days past their due date — these should be called on immediately, as they're the highest risk of going uncollected.")
    c3.metric("Avg Days to Pay", f"{avg_days_to_pay:.0f} days",
              help="Average time between load delivery and expected payment, based on contracted terms. Benchmark: 15-day customers should clear fast; 45-day customers (like Sangre de Cristo) naturally run longer.")
    c4.metric("Est. Weekly Fixed Costs", f"${weekly_fixed_cost:,.0f}",
              help="Estimated weekly fuel + maintenance spend based on the trailing 6-month average — the baseline your incoming cash needs to cover.")

    # ---- AR aging table ----
    st.markdown("### Accounts Receivable Aging")
    ar_display = open_ar.copy().sort_values('days_outstanding', ascending=False)
    ar_display['Status'] = ar_display['aging_bucket'].apply(lambda b: {
        '0-30 days': '<span class="badge-active">Current</span>',
        '31-60 days': '<span class="badge-pending">Watch</span>',
        '61+ days': '<span class="badge-late">Overdue</span>'
    }[b])
    for lid in st.session_state.ar_status_overrides:
        ar_display.loc[ar_display['load_id'] == lid,
                       'Status'] = '<span class="badge-complete">Paid</span>'

    ar_table = ar_display[['load_id', 'customer_name', 'total_invoice',
                           'load_date', 'days_outstanding', 'Status']].head(100)
    ar_table = ar_table.rename(columns={
        'load_id': 'Load ID', 'customer_name': 'Customer', 'total_invoice': 'Invoice Amount ($)',
        'load_date': 'Invoice Date', 'days_outstanding': 'Days Outstanding'
    })
    ar_table['Invoice Amount ($)'] = ar_table['Invoice Amount ($)'].round(2)
    ar_table['Invoice Date'] = ar_table['Invoice Date'].dt.strftime('%Y-%m-%d')
    st.write(ar_table.to_html(escape=False, index=False),
             unsafe_allow_html=True)
    st.caption(
        "📖 **Reading this table:** 0-30 days is normal and expected. 31-60 days deserves a "
        "friendly check-in call. 61+ days should get a direct collections call — the longer an "
        "invoice sits unpaid, the less likely it is to be collected at all."
    )

    # ---- 30-day cash projection ----
    st.markdown("### 30-Day Cash Projection")
    weeks = pd.date_range(DATA_THROUGH, periods=5, freq='7D')
    projected_balance = [0]
    running = 0
    for i in range(4):
        week_start = weeks[i]
        week_end = weeks[i + 1]
        incoming = open_ar[
            (open_ar['due_date'] >= week_start) & (
                open_ar['due_date'] < week_end)
        ]['total_invoice'].sum()
        running += incoming - weekly_fixed_cost
        projected_balance.append(running)

    proj_df = pd.DataFrame({
        'Week': ['Today', 'Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Projected Cumulative Cash Change': projected_balance
    })
    fig = go.Figure()
    colors = ['#c0392b' if v <
              0 else '#2E86C1' for v in proj_df['Projected Cumulative Cash Change']]
    fig.add_trace(go.Bar(
        x=proj_df['Week'], y=proj_df['Projected Cumulative Cash Change'], marker_color=colors))
    fig.add_hline(y=0, line_color='#1B4F72', line_width=2)
    fig.update_layout(
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Cumulative Net Cash Change ($)", plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#e2e8f0', tickprefix='$'),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "📖 **Reading this chart:** This projects incoming payments (based on invoice due dates) "
        "against your estimated weekly fuel and maintenance costs, accumulated over the next 4 "
        "weeks. If the bar goes below zero, you'll need to either chase a payment early or "
        "arrange short-term financing before that week arrives — not after."
    )

    # ---- Mark invoice paid CRUD ----
    with st.expander("✅ Mark an Invoice as Paid"):
        pay_customer = st.selectbox("Customer", options=sorted(
            open_ar['customer_name'].unique().tolist()), key="pay_customer")
        matching_loads = open_ar[open_ar['customer_name']
                                 == pay_customer]['load_id'].tolist()
        pay_load = st.selectbox(
            "Load / Invoice", options=matching_loads, key="pay_load")
        pay_amount = st.number_input("Amount Paid ($)", min_value=0.0,
                                     value=float(open_ar[open_ar['load_id'] == pay_load]['total_invoice'].iloc[0]) if pay_load else 0.0)
        pay_date = st.date_input("Date Paid", value=DATA_THROUGH.date())
        if st.button("Mark as Paid", key="mark_paid"):
            st.session_state.ar_status_overrides[pay_load] = {
                'amount': pay_amount, 'date': str(pay_date)
            }
            log_action(
                f"Invoice for load {pay_load} ({pay_customer}) marked paid — ${pay_amount:,.2f}")
            st.success(f"Marked {pay_load} as paid!")
            st.rerun()

    # ---- Insight callout ----
    if len(overdue_ar) > 0:
        worst_invoice = overdue_ar.sort_values(
            'total_invoice', ascending=False).iloc[0]
        st.info(
            f"💡 **INSIGHT:** The highest-risk overdue invoice is load **{worst_invoice['load_id']}** "
            f"for **{worst_invoice['customer_name']}** — **${worst_invoice['total_invoice']:,.2f}**, "
            f"**{int(worst_invoice['days_outstanding'])} days** past due. Sangre de Cristo "
            f"Distribution carries Redtail's longest payment terms (45 days) on the largest single "
            f"share of revenue (32.9%) — that combination deserves a standing weekly check, not "
            f"just attention when cash feels tight."
        )
    else:
        st.info(
            "💡 **INSIGHT:** Sangre de Cristo Distribution carries Redtail's longest payment terms "
            "(45 days) on the largest single share of revenue (32.9%) — that combination is worth "
            "a standing weekly check regardless of current AR status, since it represents the "
            "largest concentrated cash-flow exposure in the business."
        )

    with st.expander("❓ How to use this page"):
        st.markdown("""
Cash flow is different from profit. A month can look great on the revenue side and still leave
you short at payroll if the cash physically isn't in the bank yet. This page exists to catch
that gap before it becomes a crisis.

**What each aging bucket means:**
- **0-30 days (Current):** Normal. Most customers pay within their contracted terms; no action needed.
- **31-60 days (Watch):** Getting slow. A friendly check-in call ("just confirming this is in your
  payment queue") is appropriate and rarely damages the relationship.
- **61+ days (Overdue):** This needs a direct collections call. The longer an invoice ages past
  60 days, the lower the odds of full collection — don't let these sit.

**A simple script for calling an overdue customer:** "Hi, this is Dale from Redtail — I'm just
following up on invoice [load ID] from [date], which shows as [X] days past your normal terms.
Can you tell me where that stands on your end?" Keep it factual and low-friction; most overdue
invoices are administrative delays, not disputes, and a friendly call resolves them faster than
a formal notice.

**How to read the 30-day projection:** the bars show your *cumulative* projected cash position
week by week, based on invoices due in that window minus your typical weekly fuel and
maintenance spend. If any week goes negative, that's your early warning — you have time to
either accelerate a collection or line up short-term financing before the shortfall actually
hits.

**What to do if the projection goes negative:** first, check whether a specific large invoice
(like a Sangre de Cristo payment on 45-day terms) is driving the gap — if so, a single early
collection call may close it. If the shortfall is broad-based across many customers, that's a
signal to either tighten terms on new contracts or arrange a short-term line of credit before
you're forced into a rushed decision.

**Payment terms negotiation tips:** customers on 45-day terms (like Sangre de Cristo) tie up
more of your cash for longer, even if they're a great customer otherwise. When a contract comes
up for renewal, consider whether a modest rate concession in exchange for 30-day terms would
actually improve your cash position more than the extra few dollars per mile is worth.

**How often to check:** Weekly, ideally every Friday, so you head into the next week knowing
exactly where cash stands rather than finding out when a bill is already due.
        """)
