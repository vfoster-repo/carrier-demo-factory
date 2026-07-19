import json
import pandas as pd
import numpy as np

DATA = "data"

loads = pd.read_csv(f"{DATA}/loads.csv", parse_dates=["load_date"])
trips = pd.read_csv(f"{DATA}/trips.csv", parse_dates=["departure_time", "arrival_time"])
fuel = pd.read_csv(f"{DATA}/fuel_purchases.csv", parse_dates=["purchase_date"])
maint = pd.read_csv(f"{DATA}/maintenance_records.csv", parse_dates=["service_date"])
routes = pd.read_csv(f"{DATA}/routes.csv")
customers = pd.read_csv(f"{DATA}/customers.csv")
delivery = pd.read_csv(f"{DATA}/delivery_events.csv", parse_dates=["scheduled_time", "actual_time"])
trucks = pd.read_csv(f"{DATA}/trucks.csv")

out = {}

# ---------- Section 1: Truck fuel efficiency ----------
trip_fuel = fuel.groupby("trip_id").agg(fuel_cost=("total_cost", "sum")).reset_index()
t1 = trips.merge(trip_fuel, on="trip_id", how="left")
t1["month"] = t1["departure_time"].dt.to_period("M").astype(str)

mpg_by_truck_month = (
    t1.groupby(["truck_id", "month"])["actual_mpg"].mean().reset_index()
)
# rolling 3-month avg per truck
mpg_trend = []
for tid, grp in mpg_by_truck_month.groupby("truck_id"):
    grp = grp.sort_values("month").copy()
    grp["rolling_mpg"] = grp["actual_mpg"].rolling(3, min_periods=1).mean().round(2)
    for _, r in grp.iterrows():
        mpg_trend.append({"truck_id": tid, "month": r["month"], "mpg": round(r["rolling_mpg"], 2)})
out["mpg_trend"] = mpg_trend

avg_mpg = t1.groupby("truck_id")["actual_mpg"].mean().round(2).to_dict()
out["avg_mpg_by_truck"] = [{"truck_id": k, "mpg": v} for k, v in avg_mpg.items()]

maint_agg = maint.groupby("truck_id").agg(
    total_cost=("cost", "sum"), events=("record_id", "count"), downtime=("downtime_hours", "sum")
).round(2).reset_index()
out["maintenance_by_truck"] = maint_agg.to_dict("records")

maint_by_type = maint.groupby(["truck_id", "service_type"])["cost"].sum().reset_index()
out["maintenance_by_type"] = maint_by_type.round(2).to_dict("records")

# ---------- Section 2: Golden Gate detention ----------
de = delivery.merge(loads[["load_id", "customer_id"]], on="load_id", how="left")
de = de.merge(customers[["customer_id", "customer_name"]], on="customer_id", how="left")
de_receiver = de[de["facility_type"] == "receiver"]

det_by_cust = de_receiver.groupby("customer_name").agg(
    avg_detention=("detention_minutes", "mean"),
    events=("event_id", "count"),
    total_hours=("detention_minutes", "sum"),
    on_time_rate=("on_time", lambda s: (s == "Y").mean() * 100),
).round(2)
det_by_cust["total_hours"] = (det_by_cust["total_hours"] / 60).round(1)
det_by_cust = det_by_cust.reset_index().sort_values("avg_detention", ascending=False)
out["detention_by_customer"] = det_by_cust.to_dict("records")

gg = de_receiver[de_receiver["customer_name"] == "Golden Gate Fresh Distributors"]
others = de_receiver[de_receiver["customer_name"] != "Golden Gate Fresh Distributors"]
bins = list(range(0, 90, 10))
gg_hist = pd.cut(gg["detention_minutes"], bins=bins).value_counts().sort_index()
oth_hist = pd.cut(others["detention_minutes"], bins=bins).value_counts().sort_index()
out["detention_histogram"] = [
    {"bucket": f"{int(iv.left)}-{int(iv.right)}", "golden_gate": int(gg_hist.get(iv, 0)),
     "others_avg": round(float(oth_hist.get(iv, 0)) / (len(others["customer_name"].unique()) or 1), 1)}
    for iv in gg_hist.index
]

gg_monthly = gg.copy()
gg_monthly["month"] = gg_monthly["scheduled_time"].dt.to_period("M").astype(str)
gg_trend = gg_monthly.groupby("month")["detention_minutes"].mean().round(1).reset_index()
out["golden_gate_monthly_trend"] = gg_trend.to_dict("records")

out["golden_gate_summary"] = {
    "avg_detention": round(float(gg["detention_minutes"].mean()), 2),
    "events": int(len(gg)),
    "total_hours": round(float(gg["detention_minutes"].sum()) / 60, 1),
    "est_cost_65": round(float(gg["detention_minutes"].sum()) / 60 * 65, 2),
    "on_time_rate": round(float((gg["on_time"] == "Y").mean() * 100), 2),
    "other_on_time_rate": round(float((others["on_time"] == "Y").mean() * 100), 2),
    "other_avg_detention": round(float(others["detention_minutes"].mean()), 2),
}

# ---------- Section 3: Lane / direction profitability ----------
lo = loads.merge(routes, on="route_id", how="left")
lo = lo.merge(trips[["load_id", "trip_id", "actual_miles", "truck_id"]], on="load_id", how="left")
lo = lo.merge(trip_fuel, on="trip_id", how="left")
lo["direction"] = np.where(lo["origin_state"] == "WA", "southbound", "northbound_backhaul")
lo["rev_per_mile"] = (lo["revenue"] + lo["fuel_surcharge"]) / lo["actual_miles"]
lo["net_margin_per_mile"] = lo["rev_per_mile"] - (lo["fuel_cost"] / lo["actual_miles"])

route_perf = lo.groupby(["route_id", "origin_city", "destination_city", "direction"]).agg(
    trips=("trip_id", "count"),
    avg_rev_per_mile=("rev_per_mile", "mean"),
    avg_net_margin_per_mile=("net_margin_per_mile", "mean"),
).round(2).reset_index()
route_perf["label"] = route_perf["origin_city"] + " → " + route_perf["destination_city"]
route_perf = route_perf.sort_values("avg_net_margin_per_mile", ascending=False)
out["route_profitability"] = route_perf.to_dict("records")

dir_perf = lo.groupby("direction").agg(
    avg_rev_per_mile=("rev_per_mile", "mean"),
    avg_net_margin_per_mile=("net_margin_per_mile", "mean"),
    trips=("trip_id", "count"),
    total_revenue=("revenue", "sum"),
).round(2).reset_index()
out["direction_comparison"] = dir_perf.to_dict("records")

nb = lo[lo["direction"] == "northbound_backhaul"]
BREAKEVEN = 1.10
pct_below = round(float((nb["net_margin_per_mile"] < BREAKEVEN).mean() * 100), 1)
out["northbound_below_breakeven_pct"] = pct_below
out["northbound_breakeven_threshold"] = BREAKEVEN

nb_monthly = nb.copy()
nb_monthly["month"] = nb_monthly["load_date"].dt.to_period("M").astype(str)
nb_trend = nb_monthly.groupby("month")["net_margin_per_mile"].mean().round(2).reset_index()
out["northbound_monthly_trend"] = nb_trend.to_dict("records")

# ---------- Section 4: Maintenance burden trend ----------
maint_sorted = maint.sort_values("service_date").copy()
maint_sorted["month"] = maint_sorted["service_date"].dt.to_period("M").astype(str)
maint_monthly = maint_sorted.groupby(["truck_id", "month"]).agg(
    cost=("cost", "sum"), downtime=("downtime_hours", "sum")
).reset_index()
out["maintenance_monthly_trend"] = maint_monthly.round(2).to_dict("records")

half_split = []
for tid, grp in maint_sorted.groupby("truck_id"):
    grp = grp.sort_values("service_date")
    mid = len(grp) // 2
    first, second = grp.iloc[:mid], grp.iloc[mid:]
    half_split.append({
        "truck_id": tid,
        "first_half_cost": round(float(first["cost"].mean()), 2) if len(first) else 0,
        "second_half_cost": round(float(second["cost"].mean()), 2) if len(second) else 0,
        "first_half_downtime": round(float(first["downtime_hours"].mean()), 2) if len(first) else 0,
        "second_half_downtime": round(float(second["downtime_hours"].mean()), 2) if len(second) else 0,
    })
out["maintenance_half_split"] = half_split

# ---------- Section 5: Customer revenue concentration ----------
lo_cust = lo.merge(customers[["customer_id", "customer_name"]], on="customer_id", how="left")
cust_rev = lo_cust.groupby("customer_name").agg(
    total_revenue=("revenue", "sum"), loads=("load_id", "count")
).round(2).reset_index()
total_rev = cust_rev["total_revenue"].sum()
cust_rev["pct_of_revenue"] = (cust_rev["total_revenue"] / total_rev * 100).round(1)
cust_rev = cust_rev.sort_values("total_revenue", ascending=False)
out["customer_revenue"] = cust_rev.to_dict("records")

top3_pct = round(float(cust_rev.sort_values("total_revenue", ascending=False).head(3)["pct_of_revenue"].sum()), 1)
out["top3_concentration_pct"] = top3_pct

print(json.dumps(out, indent=2, default=str))
