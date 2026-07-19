import csv
import json
from pathlib import Path

BASE = Path(__file__).parent
AO = BASE / "analysis_output"

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

# ---------- Section 1: Lane Profitability ----------
route_margin = read_csv(AO / "route_net_margin.csv")
lanes = []
for r in route_margin:
    lanes.append({
        "label": f"{r['origin_city']}→{r['destination_city']}",
        "value": round(float(r["net_per_mile"]), 2),
        "loads": int(r["loads"]),
        "revenue": round(float(r["total_revenue"]), 0),
    })
lanes.sort(key=lambda d: d["value"])

BREAKEVEN = 2.05

# ---------- Section 2: Truck Health (TRK-006) ----------
truck_mpg = read_csv(AO / "truck_mpg.csv")
maint_by_truck = {r["truck_id"]: r for r in read_csv(AO / "maintenance_by_truck.csv")}

trucks = []
for r in truck_mpg:
    tid = r["truck_id"]
    m = maint_by_truck.get(tid, {"total_cost": "0", "total_downtime_hours": "0"})
    total_miles = float(r["total_miles"])
    fuel_cost_est = float(r["total_gallons"]) * 4.0  # rough avg price
    cost_per_mile = (fuel_cost_est + float(m["total_cost"])) / total_miles if total_miles else 0
    trucks.append({
        "truck_id": tid,
        "mpg": round(float(r["avg_mpg"]), 2),
        "maintenance_cost": round(float(m["total_cost"]), 0),
        "downtime_hours": round(float(m["total_downtime_hours"]), 1),
        "cost_per_mile": round(cost_per_mile, 3),
        "year": int(r["year"]),
    })
trucks.sort(key=lambda d: d["cost_per_mile"], reverse=True)

maint_trend = read_csv(AO / "maintenance_trend.csv")
maint_trend_data = [{"month": r["month"], "cost": round(float(r["cost"]), 0)} for r in maint_trend]

# ---------- Section 3: Detention / Ozark ----------
detention = read_csv(AO / "detention_by_customer.csv")
detention_data = []
for r in detention:
    detention_data.append({
        "label": r["customer_name"],
        "value": round(float(r["avg_detention_min"]), 1),
        "on_time_rate": round(float(r["on_time_rate"]) * 100, 1),
    })
detention_data.sort(key=lambda d: d["value"], reverse=True)

# ---------- Section 4: Customer Concentration ----------
cust_rev = read_csv(AO / "customer_revenue.csv")
cust_data = []
for r in cust_rev:
    cust_data.append({
        "label": r["customer_name"],
        "value": round(float(r["total_revenue"]), 0),
        "pct": round(float(r["pct_of_total_revenue"]), 1),
        "avg_per_load": round(float(r["avg_revenue_per_load"]), 2),
        "terms": int(r["payment_terms_days"]),
    })
cust_data.sort(key=lambda d: d["value"], reverse=True)

# ---------- Section 5: Driver Retention ----------
drivers = read_csv(BASE / "data" / "drivers.csv")
cohort_pre = [d for d in drivers if d["hire_date"] < "2025-01-01"]
cohort_post = [d for d in drivers if d["hire_date"] >= "2025-01-01"]

def term_rate(cohort):
    if not cohort:
        return 0
    terminated = sum(1 for d in cohort if d["employment_status"] == "terminated")
    return round(100 * terminated / len(cohort), 1)

retention_cohort_data = [
    {"label": "Hired before Jan 2025", "value": term_rate(cohort_pre), "count": len(cohort_pre)},
    {"label": "Hired Jan 2025 or later", "value": term_rate(cohort_post), "count": len(cohort_post)},
]

driver_timeline = []
for d in drivers:
    driver_timeline.append({
        "label": f"{d['first_name']} {d['last_name']}",
        "hire_date": d["hire_date"],
        "status": d["employment_status"],
        "years_experience": int(d["years_experience"]),
    })
driver_timeline.sort(key=lambda d: d["hire_date"])

datasets = {
    "lanes": lanes,
    "breakeven": BREAKEVEN,
    "trucks": trucks,
    "maint_trend": maint_trend_data,
    "detention": detention_data,
    "customers": cust_data,
    "retention_cohort": retention_cohort_data,
    "driver_timeline": driver_timeline,
}

print(json.dumps(datasets, indent=2))
