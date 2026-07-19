import pandas as pd
import json
import numpy as np

BASE = "analysis_output"
DATA = "data"

# -------------------------------------------------------------------
# SECTION 1: TRK-014 fuel inefficiency + maintenance/downtime concentration
# -------------------------------------------------------------------
mpg = pd.read_csv(f"{BASE}/mpg_by_truck.csv")
maint = pd.read_csv(f"{BASE}/maintenance_by_truck.csv")

fleet_avg_mpg = mpg["mean"].mean()

# scatter: MPG vs maintenance cost, bubble = downtime hours
scatter = mpg.merge(maint[["truck_id", "total_cost", "total_downtime_hrs"]], on="truck_id", how="left")
scatter["total_cost"] = scatter["total_cost"].fillna(0)
scatter["total_downtime_hrs"] = scatter["total_downtime_hrs"].fillna(0)

mpg_scatter_data = [
    {
        "truck_id": r.truck_id,
        "mpg": round(r.mean, 2),
        "maintenance_cost": round(r.total_cost, 0),
        "downtime_hrs": round(r.total_downtime_hrs, 1),
        "flagged": r.truck_id == "TRK-014",
    }
    for r in scatter.itertuples()
]

# ranked bar: top 10 worst trucks by MPG (lowest MPG first)
worst_mpg = mpg.sort_values("mean").head(10)
mpg_bar_data = [
    {"truck_id": r.truck_id, "mpg": round(r.mean, 2), "flagged": r.truck_id == "TRK-014"}
    for r in worst_mpg.itertuples()
]

# top 10 trucks by maintenance cost
worst_maint = maint.sort_values("total_cost", ascending=False).head(10)
maint_bar_data = [
    {"truck_id": r.truck_id, "cost": round(r.total_cost, 0), "flagged": r.truck_id == "TRK-014"}
    for r in worst_maint.itertuples()
]

trk014_mpg = mpg.loc[mpg.truck_id == "TRK-014", "mean"].iloc[0]
trk014_maint = maint.loc[maint.truck_id == "TRK-014"].iloc[0]
fleet_avg_maint_cost = maint["total_cost"].mean()

section1 = {
    "fleet_avg_mpg": round(fleet_avg_mpg, 2),
    "trk014_mpg": round(trk014_mpg, 2),
    "mpg_gap_pct": round((1 - trk014_mpg / fleet_avg_mpg) * 100, 1),
    "trk014_total_maint": round(trk014_maint.total_cost, 0),
    "fleet_avg_maint": round(fleet_avg_maint_cost, 0),
    "trk014_downtime_hrs": round(trk014_maint.total_downtime_hrs, 1),
    "scatter": mpg_scatter_data,
    "mpg_bar": mpg_bar_data,
    "maint_bar": maint_bar_data,
}

# -------------------------------------------------------------------
# SECTION 2: Customer detention outlier (Llano Estacado Foods)
# -------------------------------------------------------------------
det = pd.read_csv(f"{BASE}/detention_by_customer.csv")
det_sorted = det.sort_values("avg_detention", ascending=False)

detention_bar_data = [
    {
        "customer": r.customer_name,
        "avg_detention_min": round(r.avg_detention, 1),
        "flagged": r.customer_id == "CUST-002",
    }
    for r in det_sorted.itertuples()
]

fleet_avg_detention_excl = det.loc[det.customer_id != "CUST-002", "avg_detention"].mean()
llano = det.loc[det.customer_id == "CUST-002"].iloc[0]

# monthly detention trend for Llano Estacado — derive from delivery_events + loads
delivery_events = pd.read_csv(f"{DATA}/delivery_events.csv")
loads = pd.read_csv(f"{DATA}/loads.csv")

de = delivery_events.merge(loads[["load_id", "customer_id"]], on="load_id", how="left")
de["scheduled_time"] = pd.to_datetime(de["scheduled_time"], errors="coerce")
llano_events = de[de.customer_id == "CUST-002"].copy()
llano_events["month"] = llano_events["scheduled_time"].dt.to_period("M").astype(str)
llano_monthly = llano_events.groupby("month")["detention_minutes"].mean().reset_index()
llano_monthly = llano_monthly.sort_values("month")

detention_trend_data = [
    {"month": r.month, "avg_detention_min": round(r.detention_minutes, 1)}
    for r in llano_monthly.itertuples()
]

section2 = {
    "llano_avg_detention": round(llano.avg_detention, 1),
    "fleet_avg_detention_excl_llano": round(fleet_avg_detention_excl, 1),
    "llano_total_hours": round(llano.total_detention_hrs, 0),
    "llano_dollar_cost_35hr": round(llano.total_detention_hrs * 35, 0),
    "bar": detention_bar_data,
    "trend": detention_trend_data,
}

# -------------------------------------------------------------------
# SECTION 3: Lane profitability (route net $/mile after fuel)
# -------------------------------------------------------------------
routes = pd.read_csv(f"{BASE}/route_net_profitability.csv")
routes_sorted = routes.sort_values("avg_net_per_mile")

BREAKEVEN = 2.05

route_bar_data = [
    {
        "route": r.route_id,
        "net_per_mile": round(r.avg_net_per_mile, 2),
        "gross_per_mile": round(r.avg_gross_rev_per_mile, 2),
        "pct_below_breakeven": round(r.pct_loads_below_205, 1),
        "below_breakeven": r.avg_net_per_mile < BREAKEVEN,
    }
    for r in routes_sorted.itertuples()
]

losing_routes = routes[routes.avg_net_per_mile < BREAKEVEN].sort_values("avg_net_per_mile")

section3 = {
    "breakeven": BREAKEVEN,
    "bar": route_bar_data,
    "worst_route": losing_routes.iloc[0].route_id,
    "worst_route_net": round(losing_routes.iloc[0].avg_net_per_mile, 2),
    "n_losing_routes": int((routes.avg_net_per_mile < BREAKEVEN).sum()),
    "ama_den_reefer_net": round(routes.loc[routes.route_id == "AMA-DEN-REEFER", "avg_net_per_mile"].iloc[0], 2),
    "ama_den_reefer_pct_below": round(routes.loc[routes.route_id == "AMA-DEN-REEFER", "pct_loads_below_205"].iloc[0], 1),
}

# -------------------------------------------------------------------
# SECTION 4: New-hire driver attrition
# -------------------------------------------------------------------
drivers = pd.read_csv(f"{BASE}/drivers_tenure.csv")
drivers["hire_date"] = pd.to_datetime(drivers["hire_date"])
max_hire = drivers["hire_date"].max()
cutoff = max_hire - pd.DateOffset(months=18)

drivers["cohort"] = np.where(drivers["hire_date"] >= cutoff, "Last 18 Months", "Earlier Hires")
drivers["left"] = drivers["employment_status"].isin(["terminated", "voluntary_quit"])

cohort_summary = drivers.groupby("cohort").agg(
    n=("driver_id", "count"), n_left=("left", "sum")
).reset_index()
cohort_summary["pct_left"] = round(cohort_summary["n_left"] / cohort_summary["n"] * 100, 1)

cohort_bar_data = [
    {"cohort": r.cohort, "pct_left": r.pct_left, "n": int(r.n), "n_left": int(r.n_left)}
    for r in cohort_summary.itertuples()
]

# tenure-at-departure histogram (days) for terminated/quit drivers, bucketed
departed = drivers[drivers.left]
bins = [0, 180, 365, 730, 1095, 1460, 10000]
labels = ["0-6mo", "6-12mo", "1-2yr", "2-3yr", "3-4yr", "4yr+"]
departed = departed.copy()
departed["bucket"] = pd.cut(departed["tenure_days"], bins=bins, labels=labels)
tenure_hist = departed["bucket"].value_counts().reindex(labels, fill_value=0).reset_index()
tenure_hist.columns = ["bucket", "count"]

tenure_hist_data = [
    {"bucket": r.bucket, "count": int(r.count)} for r in tenure_hist.itertuples()
]

recent_hires = drivers[drivers.cohort == "Last 18 Months"].sort_values("left", ascending=False)
recent_hires_data = [
    {
        "driver_id": r.driver_id,
        "name": f"{r.first_name} {r.last_name}",
        "hire_date": str(r.hire_date.date()),
        "status": r.employment_status,
        "tenure_days": int(r.tenure_days),
        "years_experience": round(r.years_experience, 1),
    }
    for r in recent_hires.itertuples()
]

last18 = cohort_summary.loc[cohort_summary.cohort == "Last 18 Months"].iloc[0]
earlier = cohort_summary.loc[cohort_summary.cohort == "Earlier Hires"].iloc[0]

section4 = {
    "last18_pct_left": last18.pct_left,
    "last18_n": int(last18.n),
    "last18_n_left": int(last18.n_left),
    "earlier_pct_left": earlier.pct_left,
    "earlier_n": int(earlier.n),
    "cohort_bar": cohort_bar_data,
    "tenure_hist": tenure_hist_data,
    "recent_hires": recent_hires_data,
}

# -------------------------------------------------------------------
# OUTPUT
# -------------------------------------------------------------------
report_data = {
    "section1": section1,
    "section2": section2,
    "section3": section3,
    "section4": section4,
}

print(json.dumps(report_data, indent=2))
