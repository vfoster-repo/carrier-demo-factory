#!/usr/bin/env python3
"""Synthetic data generator for Redtail Regional Freight."""

import csv
import os
import random
from datetime import datetime, timedelta

random.seed(20090614)

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(BASE_DIR, exist_ok=True)

TODAY = datetime(2026, 7, 2)
START_DATE = TODAY - timedelta(days=730)

FIRST_NAMES = [
    "James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas",
    "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Steven", "Paul", "Kenneth",
    "Andrew", "Joshua", "Kevin", "Brian", "George", "Edward", "Ronald", "Jason",
    "Jeff", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Larry", "Justin",
    "Scott", "Brandon", "Frank", "Raymond", "Cody", "Wyatt", "Colton", "Travis",
    "Maria", "Linda", "Susan", "Karen", "Lisa", "Nancy", "Sandra", "Ashley",
    "Amanda", "Dorothy", "Melissa", "Deborah",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts",
]

# ---------------------------------------------------------------------------
# TRUCKS
# ---------------------------------------------------------------------------
TRUCK_COUNT = 38
MAKES_MODELS = [
    ("Freightliner", "Cascadia"),
    ("Peterbilt", "579"),
    ("Peterbilt", "389"),
    ("Kenworth", "T680"),
    ("International", "LT"),
]

trucks = []
for i in range(1, TRUCK_COUNT + 1):
    truck_id = f"TRK-{i:03d}"
    if truck_id == "TRK-014":
        make, model = "Freightliner", "Cascadia"
        year = 2013
        odometer = 781400
        status = "active"
        acq = datetime(2013, 9, 12)
    else:
        make, model = random.choice(MAKES_MODELS)
        year = random.randint(2016, 2024)
        age_years = TODAY.year - year
        odometer = int(random.uniform(90000, 145000) * max(age_years, 1))
        odometer = min(odometer, 650000)
        status = random.choices(["active", "active", "active", "shop", "retired"], weights=[80, 10, 5, 4, 1])[0]
        acq_days_ago = random.randint(30, min(730, (TODAY.year - year) * 365 + 300))
        acq = TODAY - timedelta(days=acq_days_ago)
    fuel_type = "diesel"
    trucks.append({
        "truck_id": truck_id,
        "make": make,
        "model": model,
        "year": year,
        "status": status,
        "acquisition_date": acq.strftime("%Y-%m-%d"),
        "current_odometer": odometer,
        "fuel_type": fuel_type,
    })

with open(os.path.join(BASE_DIR, "trucks.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["truck_id", "make", "model", "year", "status",
                                       "acquisition_date", "current_odometer", "fuel_type"])
    w.writeheader()
    w.writerows(trucks)

# ---------------------------------------------------------------------------
# DRIVERS
# ---------------------------------------------------------------------------
DRIVER_COUNT = 52
drivers = []
used_names = set()
# Designate a cluster of "high turnover, recent hire" drivers (Amarillo terminal, short tenure)
recent_high_turnover_ids = set(f"DRV-{i:03d}" for i in range(41, 49))  # 8 drivers

for i in range(1, DRIVER_COUNT + 1):
    driver_id = f"DRV-{i:03d}"
    while True:
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        if (fn, ln) not in used_names:
            used_names.add((fn, ln))
            break
    if driver_id in recent_high_turnover_ids:
        hire_days_ago = random.randint(60, 400)
        hire_date = TODAY - timedelta(days=hire_days_ago)
        # short tenure: terminated/quit within 30-160 days of hire
        term_days_after_hire = random.randint(30, 160)
        term_date = hire_date + timedelta(days=term_days_after_hire)
        if term_date >= TODAY:
            employment_status = "active"
        else:
            employment_status = random.choice(["terminated", "voluntary_quit"])
        years_experience = round(random.uniform(0.5, 3.0), 1)
    else:
        hire_days_ago = random.randint(200, 5800)
        hire_date = TODAY - timedelta(days=hire_days_ago)
        employment_status = random.choices(
            ["active", "active", "active", "active", "terminated", "voluntary_quit", "retired"],
            weights=[70, 10, 5, 5, 4, 4, 2]
        )[0]
        years_experience = round(random.uniform(2.0, 28.0), 1)

    cdl_class = random.choices(["A", "A", "A", "B"], weights=[85, 8, 4, 3])[0]
    drivers.append({
        "driver_id": driver_id,
        "first_name": fn,
        "last_name": ln,
        "hire_date": hire_date.strftime("%Y-%m-%d"),
        "employment_status": employment_status,
        "cdl_class": cdl_class,
        "years_experience": years_experience,
        "home_terminal": "Amarillo, TX",
    })

with open(os.path.join(BASE_DIR, "drivers.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["driver_id", "first_name", "last_name", "hire_date",
                                       "employment_status", "cdl_class", "years_experience", "home_terminal"])
    w.writeheader()
    w.writerows(drivers)

active_driver_ids = [d["driver_id"] for d in drivers if d["employment_status"] == "active"]
all_driver_ids = [d["driver_id"] for d in drivers]
active_truck_ids = [t["truck_id"] for t in trucks if t["status"] in ("active", "shop")]

# ---------------------------------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------------------------------
customers = [
    {"customer_id": "CUST-001", "customer_name": "Panhandle Beef Processors", "city": "Amarillo", "state": "TX",
     "industry": "Food Processing (Protein)", "payment_terms_days": 30, "account_status": "active"},
    {"customer_id": "CUST-002", "customer_name": "Llano Estacado Foods", "city": "Lubbock", "state": "TX",
     "industry": "Food Processing (Dairy/Packaged)", "payment_terms_days": 30, "account_status": "active"},
    {"customer_id": "CUST-003", "customer_name": "High Plains Ag Cooperative", "city": "Hereford", "state": "TX",
     "industry": "Agriculture", "payment_terms_days": 15, "account_status": "active"},
    {"customer_id": "CUST-004", "customer_name": "Sangre de Cristo Distribution", "city": "Denver", "state": "CO",
     "industry": "Retail Distribution", "payment_terms_days": 45, "account_status": "active"},
    {"customer_id": "CUST-005", "customer_name": "Caprock Grain Exchange", "city": "Plainview", "state": "TX",
     "industry": "Agriculture", "payment_terms_days": 15, "account_status": "active"},
    {"customer_id": "CUST-006", "customer_name": "Sooner State Foods", "city": "Oklahoma City", "state": "OK",
     "industry": "Food Distribution", "payment_terms_days": 30, "account_status": "active"},
]

with open(os.path.join(BASE_DIR, "customers.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["customer_id", "customer_name", "city", "state", "industry",
                                       "payment_terms_days", "account_status"])
    w.writeheader()
    w.writerows(customers)

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------
routes = [
    {"route_id": "AMA-DEN-REEFER", "origin_city": "Amarillo", "origin_state": "TX",
     "destination_city": "Denver", "destination_state": "CO", "distance_miles": 432, "base_rate_per_mile": 2.15},
    {"route_id": "AMA-OKC-VAN", "origin_city": "Amarillo", "origin_state": "TX",
     "destination_city": "Oklahoma City", "destination_state": "OK", "distance_miles": 261, "base_rate_per_mile": 2.35},
    {"route_id": "LUB-ABQ-VAN", "origin_city": "Lubbock", "origin_state": "TX",
     "destination_city": "Albuquerque", "destination_state": "NM", "distance_miles": 284, "base_rate_per_mile": 2.40},
    {"route_id": "AMA-HFD-AG", "origin_city": "Amarillo", "origin_state": "TX",
     "destination_city": "Hereford", "destination_state": "TX", "distance_miles": 51, "base_rate_per_mile": 3.10},
    {"route_id": "DEN-AMA-BACKHAUL", "origin_city": "Denver", "origin_state": "CO",
     "destination_city": "Amarillo", "destination_state": "TX", "distance_miles": 432, "base_rate_per_mile": 1.95},
    {"route_id": "AMA-LUB-VAN", "origin_city": "Amarillo", "origin_state": "TX",
     "destination_city": "Lubbock", "destination_state": "TX", "distance_miles": 123, "base_rate_per_mile": 2.55},
    {"route_id": "PLV-AMA-AG", "origin_city": "Plainview", "origin_state": "TX",
     "destination_city": "Amarillo", "destination_state": "TX", "distance_miles": 68, "base_rate_per_mile": 2.95},
    {"route_id": "AMA-OKC-BACKHAUL", "origin_city": "Oklahoma City", "origin_state": "OK",
     "destination_city": "Amarillo", "destination_state": "TX", "distance_miles": 261, "base_rate_per_mile": 1.90},
]

with open(os.path.join(BASE_DIR, "routes.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["route_id", "origin_city", "origin_state", "destination_city",
                                       "destination_state", "distance_miles", "base_rate_per_mile"])
    w.writeheader()
    w.writerows(routes)

route_by_id = {r["route_id"]: r for r in routes}
route_ids = [r["route_id"] for r in routes]

# customer -> preferred routes/freight
customer_route_pref = {
    "CUST-001": (["AMA-OKC-VAN", "AMA-LUB-VAN", "AMA-OKC-BACKHAUL"], "refrigerated"),
    "CUST-002": (["LUB-ABQ-VAN", "AMA-LUB-VAN"], "refrigerated"),
    "CUST-003": (["AMA-HFD-AG", "PLV-AMA-AG"], "dry_bulk_ag"),
    "CUST-004": (["AMA-DEN-REEFER", "DEN-AMA-BACKHAUL"], "refrigerated"),
    "CUST-005": (["PLV-AMA-AG", "AMA-HFD-AG"], "dry_bulk_ag"),
    "CUST-006": (["AMA-OKC-VAN", "AMA-OKC-BACKHAUL"], "dry_van"),
}

# ---------------------------------------------------------------------------
# LOADS + TRIPS + FUEL + DELIVERY EVENTS
# ---------------------------------------------------------------------------
LOAD_COUNT = 22000

DIESEL_PRICE_BY_MONTH = {}
# reflect 2024-2026 range roughly $3.80-$4.50, with some seasonal noise
d = START_DATE
base_prices = []
cur = datetime(START_DATE.year, START_DATE.month, 1)
while cur <= TODAY:
    key = (cur.year, cur.month)
    # slow drift with noise
    months_from_start = (cur.year - START_DATE.year) * 12 + (cur.month - START_DATE.month)
    price = 3.85 + 0.35 * (months_from_start / 24.0) + random.uniform(-0.12, 0.12)
    price = max(3.75, min(4.55, price))
    DIESEL_PRICE_BY_MONTH[key] = round(price, 3)
    if cur.month == 12:
        cur = datetime(cur.year + 1, 1, 1)
    else:
        cur = datetime(cur.year, cur.month + 1, 1)

def diesel_price_for(dt):
    key = (dt.year, dt.month)
    return DIESEL_PRICE_BY_MONTH.get(key, 4.10)

FACILITY_TYPES = ["shipper", "consignee"]

loads_rows = []
trips_rows = []
fuel_rows = []
delivery_rows = []

load_counter = 1
trip_counter = 1
fuel_counter = 1
event_counter = 1

# maintenance-truck-14 downtime windows (unavailable periods) to reduce its trip share slightly but not exclude
truck14_shop_days = set()
cur = START_DATE
while cur <= TODAY:
    # roughly one 4-7 day shop stint every ~45 days
    truck14_shop_days.add(cur.strftime("%Y-%m-%d"))
    cur += timedelta(days=1)

def random_date_in_range():
    days_span = (TODAY - START_DATE).days
    offset = random.randint(0, days_span)
    return START_DATE + timedelta(days=offset)

for _ in range(LOAD_COUNT):
    load_id = f"LOAD-{load_counter:06d}"
    load_counter += 1

    customer_id = random.choices(
        [c["customer_id"] for c in customers],
        weights=[24, 20, 16, 18, 12, 10]
    )[0]
    pref_routes, freight_type = customer_route_pref[customer_id]
    route_id = random.choice(pref_routes)
    route = route_by_id[route_id]

    load_date = random_date_in_range()

    weight_lbs = random.randint(28000, 45000)
    distance = route["distance_miles"]
    base_rate = route["base_rate_per_mile"]
    fsc_rate = round(random.uniform(0.28, 0.55), 3)

    revenue = round(distance * base_rate * random.uniform(0.94, 1.06), 2)
    fuel_surcharge = round(distance * fsc_rate, 2)

    load_status = random.choices(
        ["delivered", "delivered", "delivered", "delivered", "cancelled"],
        weights=[90, 4, 3, 2, 1]
    )[0]

    loads_rows.append({
        "load_id": load_id,
        "customer_id": customer_id,
        "route_id": route_id,
        "load_date": load_date.strftime("%Y-%m-%d"),
        "freight_type": freight_type,
        "weight_lbs": weight_lbs,
        "revenue": revenue,
        "fuel_surcharge": fuel_surcharge,
        "load_status": load_status,
    })

    if load_status == "cancelled":
        continue

    # assign truck/driver
    # TRK-014 gets ~2.5% of loads (a bit less than average given downtime), rest spread among other active trucks
    if random.random() < 0.025:
        truck_id = "TRK-014"
    else:
        truck_id = random.choice([t for t in active_truck_ids if t != "TRK-014"])

    driver_id = random.choice(active_driver_ids if active_driver_ids else all_driver_ids)

    trip_id = f"TRIP-{trip_counter:06d}"
    trip_counter += 1

    actual_miles = round(distance * random.uniform(0.98, 1.05), 1)

    if truck_id == "TRK-014":
        actual_mpg = round(random.uniform(4.7, 5.4), 2)
    else:
        actual_mpg = round(random.uniform(6.3, 7.6), 2)

    fuel_gallons = round(actual_miles / actual_mpg, 2)

    departure_dt = datetime.combine(load_date.date(), datetime.min.time()) + timedelta(hours=random.randint(4, 9), minutes=random.randint(0, 59))
    drive_hours = actual_miles / random.uniform(48, 56)
    arrival_dt = departure_dt + timedelta(hours=drive_hours)

    on_time_flag = 1 if random.random() < 0.90 else 0
    if truck_id == "TRK-014" and random.random() < 0.35:
        on_time_flag = 0  # unreliable truck contributes to lateness too

    trips_rows.append({
        "trip_id": trip_id,
        "load_id": load_id,
        "driver_id": driver_id,
        "truck_id": truck_id,
        "actual_miles": actual_miles,
        "fuel_gallons": fuel_gallons,
        "actual_mpg": actual_mpg,
        "departure_time": departure_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "arrival_time": arrival_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "on_time_flag": on_time_flag,
    })

    # fuel purchases: 1-2 per trip
    num_purchases = 1 if actual_miles < 200 else 2
    gallons_remaining = fuel_gallons
    for p in range(num_purchases):
        purchase_id = f"FUEL-{fuel_counter:06d}"
        fuel_counter += 1
        gallons = round(fuel_gallons / num_purchases * random.uniform(0.85, 1.15), 2)
        gallons_remaining -= gallons
        price = diesel_price_for(load_date) * random.uniform(0.97, 1.04)
        price = round(price, 3)
        total_cost = round(gallons * price, 2)
        purchase_date = (departure_dt + timedelta(hours=drive_hours * (p / max(num_purchases, 1)))).strftime("%Y-%m-%d")
        location = f"{route['origin_city']}, {route['origin_state']}" if p == 0 else f"{route['destination_city']}, {route['destination_state']}"
        fuel_rows.append({
            "purchase_id": purchase_id,
            "trip_id": trip_id,
            "truck_id": truck_id,
            "driver_id": driver_id,
            "purchase_date": purchase_date,
            "gallons": gallons,
            "price_per_gallon": price,
            "total_cost": total_cost,
            "location": location,
        })

    # delivery events: shipper (pickup) + consignee (delivery)
    for facility_type in FACILITY_TYPES:
        event_id = f"EVT-{event_counter:06d}"
        event_counter += 1
        if facility_type == "shipper":
            scheduled_dt = departure_dt - timedelta(minutes=random.randint(0, 30))
        else:
            scheduled_dt = arrival_dt - timedelta(minutes=random.randint(0, 30))

        if customer_id == "CUST-002":
            # Llano Estacado Foods: severe detention outlier
            detention_minutes = max(0, int(random.gauss(47, 9)))
        else:
            detention_minutes = max(0, int(random.gauss(11, 5)))

        actual_dt = scheduled_dt + timedelta(minutes=detention_minutes + random.randint(-3, 8))
        on_time = 1 if detention_minutes <= 20 else 0

        delivery_rows.append({
            "event_id": event_id,
            "load_id": load_id,
            "trip_id": trip_id,
            "facility_type": facility_type,
            "scheduled_time": scheduled_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "actual_time": actual_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "detention_minutes": detention_minutes,
            "on_time": on_time,
        })

with open(os.path.join(BASE_DIR, "loads.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["load_id", "customer_id", "route_id", "load_date", "freight_type",
                                       "weight_lbs", "revenue", "fuel_surcharge", "load_status"])
    w.writeheader()
    w.writerows(loads_rows)

with open(os.path.join(BASE_DIR, "trips.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["trip_id", "load_id", "driver_id", "truck_id", "actual_miles",
                                       "fuel_gallons", "actual_mpg", "departure_time", "arrival_time", "on_time_flag"])
    w.writeheader()
    w.writerows(trips_rows)

with open(os.path.join(BASE_DIR, "fuel_purchases.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["purchase_id", "trip_id", "truck_id", "driver_id", "purchase_date",
                                       "gallons", "price_per_gallon", "total_cost", "location"])
    w.writeheader()
    w.writerows(fuel_rows)

with open(os.path.join(BASE_DIR, "delivery_events.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["event_id", "load_id", "trip_id", "facility_type", "scheduled_time",
                                       "actual_time", "detention_minutes", "on_time"])
    w.writeheader()
    w.writerows(delivery_rows)

# ---------------------------------------------------------------------------
# MAINTENANCE RECORDS
# ---------------------------------------------------------------------------
SERVICE_TYPES_ROUTINE = ["oil_change", "tire_rotation", "brake_inspection", "pm_service", "dot_inspection"]
SERVICE_TYPES_REPAIR = ["engine_repair", "transmission_repair", "turbo_replacement", "electrical_repair",
                         "cooling_system_repair", "aftertreatment_repair", "suspension_repair"]

maintenance_rows = []
rec_counter = 1

for truck in trucks:
    truck_id = truck["truck_id"]
    odometer = truck["current_odometer"]
    if truck_id == "TRK-014":
        num_events = random.randint(22, 28)
    else:
        num_events = random.randint(6, 12)

    for _ in range(num_events):
        record_id = f"MAINT-{rec_counter:06d}"
        rec_counter += 1
        service_date = random_date_in_range()

        if truck_id == "TRK-014":
            service_type = random.choices(
                SERVICE_TYPES_REPAIR + SERVICE_TYPES_ROUTINE,
                weights=[14, 10, 10, 8, 9, 8, 6, 5, 5, 4, 4, 3]
            )[0]
            if service_type in SERVICE_TYPES_REPAIR:
                cost = round(random.uniform(2200, 9800), 2)
                downtime_hours = round(random.uniform(18, 96), 1)
            else:
                cost = round(random.uniform(180, 650), 2)
                downtime_hours = round(random.uniform(1, 6), 1)
        else:
            service_type = random.choices(
                SERVICE_TYPES_ROUTINE + SERVICE_TYPES_REPAIR,
                weights=[22, 18, 16, 14, 10, 5, 4, 3, 3, 2, 2, 1]
            )[0]
            if service_type in SERVICE_TYPES_REPAIR:
                cost = round(random.uniform(900, 4500), 2)
                downtime_hours = round(random.uniform(4, 30), 1)
            else:
                cost = round(random.uniform(150, 550), 2)
                downtime_hours = round(random.uniform(0.5, 4), 1)

        odometer_at_service = max(5000, int(odometer * random.uniform(0.55, 0.99)))

        maintenance_rows.append({
            "record_id": record_id,
            "truck_id": truck_id,
            "service_date": service_date.strftime("%Y-%m-%d"),
            "service_type": service_type,
            "cost": cost,
            "downtime_hours": downtime_hours,
            "odometer_at_service": odometer_at_service,
        })

with open(os.path.join(BASE_DIR, "maintenance_records.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "truck_id", "service_date", "service_type", "cost",
                                       "downtime_hours", "odometer_at_service"])
    w.writeheader()
    w.writerows(maintenance_rows)

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("Data generation complete.")
print(f"drivers.csv: {len(drivers)} rows")
print(f"trucks.csv: {len(trucks)} rows")
print(f"customers.csv: {len(customers)} rows")
print(f"routes.csv: {len(routes)} rows")
print(f"loads.csv: {len(loads_rows)} rows")
print(f"trips.csv: {len(trips_rows)} rows")
print(f"fuel_purchases.csv: {len(fuel_rows)} rows")
print(f"delivery_events.csv: {len(delivery_rows)} rows")
print(f"maintenance_records.csv: {len(maintenance_rows)} rows")
