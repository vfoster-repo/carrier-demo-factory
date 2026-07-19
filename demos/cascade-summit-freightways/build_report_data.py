"""Extract and aggregate datasets for the Cascade Summit Freightways HTML report."""
import json
import pandas as pd

DATA = "data"
OUT = "analysis_output"

# ---------------------------------------------------------------------------
# Section 1: Truck True Cost / Aging Cohort (TRK-047 + TRK-041-048)
# ---------------------------------------------------------------------------
truck_mpg = pd.read_csv(f"{OUT}/truck_mpg.csv")
maint = pd.read_csv(f"{OUT}/maintenance_by_truck.csv")

AGING_COHORT = [f"TRK-0{n}" for n in range(41, 49)]

merged = truck_mpg.merge(
    maint[["truck_id", "total_cost", "total_downtime_hrs"]], on="truck_id", how="left"
)
merged["total_cost"] = merged["total_cost"].fillna(0)
merged["total_downtime_hrs"] = merged["total_downtime_hrs"].fillna(0)
merged["is_aging_cohort"] = merged["truck_id"].isin(AGING_COHORT)

# Worst 15 trucks by MPG (ascending = worst efficiency)
worst_mpg = merged.sort_values("avg_mpg").head(15)
data_1_mpg_bar = [
    {
        "label": row.truck_id,
        "value": round(row.avg_mpg, 2),
        "cohort": bool(row.is_aging_cohort),
    }
    for row in worst_mpg.itertuples()
]

# Scatter: MPG vs maintenance cost per mile, sized by total miles
merged["maint_cost_per_mile"] = merged["total_cost"] / merged["total_miles"]
scatter_rows = merged[
    ["truck_id", "avg_mpg", "maint_cost_per_mile", "total_miles", "is_aging_cohort"]
].copy()
data_1_scatter = [
    {
        "label": row.truck_id,
        "mpg": round(row.avg_mpg, 2),
        "maint_per_mile": round(row.maint_cost_per_mile, 4),
        "miles": int(row.total_miles),
        "cohort": bool(row.is_aging_cohort),
    }
    for row in scatter_rows.itertuples()
]

fleet_avg_mpg = round(truck_mpg["avg_mpg"].mean(), 2)
trk047 = truck_mpg[truck_mpg.truck_id == "TRK-047"].iloc[0]

# ---------------------------------------------------------------------------
# Section 2: TitanBolt Detention
# ---------------------------------------------------------------------------
detention = pd.read_csv(f"{OUT}/detention_by_customer.csv").sort_values(
    "avg_detention_min", ascending=False
)
data_2_detention = [
    {
        "label": row.customer_name,
        "value": round(row.avg_detention_min, 1),
        "highlight": row.customer_id == "CUST-03",
    }
    for row in detention.itertuples()
]

# TitanBolt monthly detention trend
delivery_events = pd.read_csv(f"{DATA}/delivery_events.csv")
loads = pd.read_csv(f"{DATA}/loads.csv")
customers = pd.read_csv(f"{DATA}/customers.csv")

de_loads = delivery_events.merge(
    loads[["load_id", "customer_id"]], on="load_id", how="left"
)
de_loads["month"] = pd.to_datetime(de_loads["scheduled_time"]).dt.to_period("M").astype(str)

titanbolt = de_loads[de_loads.customer_id == "CUST-03"]
titanbolt_trend = (
    titanbolt.groupby("month")["detention_minutes"].mean().reset_index().sort_values("month")
)
data_2_trend = [
    {"month": row.month, "value": round(row.detention_minutes, 1)}
    for row in titanbolt_trend.itertuples()
]

# ---------------------------------------------------------------------------
# Section 3: Lane Profitability (Seattle<->Atlanta)
# ---------------------------------------------------------------------------
lanes = pd.read_csv(f"{OUT}/lane_profitability.csv").sort_values(
    "avg_net_per_mile"
)
BREAKEVEN = 2.05
data_3_lanes = [
    {
        "label": f"{row.origin_city}→{row.destination_city}",
        "value": round(row.avg_net_per_mile, 2),
        "below_breakeven": row.avg_net_per_mile < BREAKEVEN,
    }
    for row in lanes.itertuples()
]

# Monthly trend for RTE-04/RTE-08 (Seattle<->Atlanta)
trips = pd.read_csv(f"{DATA}/trips.csv")
routes = pd.read_csv(f"{DATA}/routes.csv")
fuel = pd.read_csv(f"{DATA}/fuel_purchases.csv")

sea_atl_routes = ["RTE-04", "RTE-08"]
trips_sa = trips.merge(
    loads[["load_id", "route_id", "revenue", "fuel_surcharge"]], on="load_id", how="left"
)
trips_sa = trips_sa[trips_sa.route_id.isin(sea_atl_routes)].copy()
fuel_by_trip = fuel.groupby("trip_id")["total_cost"].sum().reset_index()
trips_sa = trips_sa.merge(fuel_by_trip, on="trip_id", how="left")
trips_sa["total_cost"] = trips_sa["total_cost"].fillna(0)
trips_sa["net_per_mile"] = (
    trips_sa["revenue"] + trips_sa["fuel_surcharge"] - trips_sa["total_cost"]
) / trips_sa["actual_miles"]
trips_sa["month"] = pd.to_datetime(trips_sa["departure_time"]).dt.to_period("M").astype(str)
sa_trend = trips_sa.groupby("month")["net_per_mile"].mean().reset_index().sort_values("month")
data_3_trend = [
    {"month": row.month, "value": round(row.net_per_mile, 2)}
    for row in sa_trend.itertuples()
]

# ---------------------------------------------------------------------------
# Section 4: Chicago Terminal Retention
# ---------------------------------------------------------------------------
drivers = pd.read_csv(f"{DATA}/drivers.csv")
drivers["hire_year"] = pd.to_datetime(drivers["hire_date"]).dt.year
drivers["terminated"] = (drivers["employment_status"] == "terminated").astype(int)

cohort = (
    drivers.groupby(["home_terminal", "hire_year"])
    .agg(headcount=("driver_id", "count"), terminated=("terminated", "sum"))
    .reset_index()
)
cohort["termination_rate"] = round(cohort["terminated"] / cohort["headcount"] * 100, 1)
cohort = cohort[cohort.headcount >= 3]  # drop tiny/noisy cohorts

data_4_cohort = [
    {
        "terminal": "Chicago" if "Chicago" in row.home_terminal else "Spokane",
        "year": int(row.hire_year),
        "rate": row.termination_rate,
        "headcount": int(row.headcount),
    }
    for row in cohort.itertuples()
]

# ---------------------------------------------------------------------------
# Section 5: Aging Truck Cohort maintenance cost & downtime
# ---------------------------------------------------------------------------
merged["cohort_label"] = merged["is_aging_cohort"].map(
    {True: "Aging Cohort (TRK-041-048)", False: "Rest of Fleet"}
)
cohort_summary = (
    merged.groupby("cohort_label")
    .agg(
        avg_maint_cost=("total_cost", "mean"),
        avg_downtime=("total_downtime_hrs", "mean"),
        count=("truck_id", "count"),
    )
    .reset_index()
)
data_5_cohort_cost = [
    {
        "label": row.cohort_label,
        "avg_maint_cost": round(row.avg_maint_cost, 0),
        "avg_downtime": round(row.avg_downtime, 0),
        "count": int(row.count),
    }
    for row in cohort_summary.itertuples()
]

# Per-truck maintenance cost for the 8 cohort trucks (ranked)
cohort_trucks = merged[merged.is_aging_cohort].sort_values("total_cost", ascending=False)
data_5_trucks = [
    {"label": row.truck_id, "value": round(row.total_cost, 0)}
    for row in cohort_trucks.itertuples()
]

# ---------------------------------------------------------------------------
# Overview stats for hero / KPI strip
# ---------------------------------------------------------------------------
overview = {
    "fleet_avg_mpg": fleet_avg_mpg,
    "trk047_mpg": round(trk047.avg_mpg, 2),
    "titanbolt_detention": round(
        detention[detention.customer_id == "CUST-03"].iloc[0].avg_detention_min, 1
    ),
    "fleet_avg_detention": round(
        detention[detention.customer_id != "CUST-03"].avg_detention_min.mean(), 1
    ),
    "sea_atl_net_per_mile": round(
        lanes[lanes.route_id.isin(["RTE-04", "RTE-08"])].avg_net_per_mile.mean(), 2
    ),
    "chicago_2023_rate": float(
        cohort[(cohort.home_terminal.str.contains("Chicago")) & (cohort.hire_year == 2023)][
            "termination_rate"
        ].iloc[0]
    ),
    "spokane_overall_rate": round(
        drivers[drivers.home_terminal.str.contains("Spokane")]["terminated"].mean() * 100, 1
    ),
    "total_loads": int(loads.shape[0]),
    "total_trips": int(trips.shape[0]),
}

datasets = {
    "data_1_mpg_bar": data_1_mpg_bar,
    "data_1_scatter": data_1_scatter,
    "data_2_detention": data_2_detention,
    "data_2_trend": data_2_trend,
    "data_3_lanes": data_3_lanes,
    "data_3_trend": data_3_trend,
    "data_4_cohort": data_4_cohort,
    "data_5_cohort_cost": data_5_cohort_cost,
    "data_5_trucks": data_5_trucks,
    "overview": overview,
}

print(json.dumps(datasets, indent=None))
