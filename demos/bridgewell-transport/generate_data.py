#!/usr/bin/env python3
"""Synthetic operational data generator for Bridgewell Transport."""

import csv
import datetime
import os
import random

random.seed(42)

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(BASE_DIR, exist_ok=True)

TODAY = datetime.date(2026, 7, 3)
START_DATE = TODAY - datetime.timedelta(days=730)

# ---------------------------------------------------------------------------
# DRIVERS
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "James", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Daniel", "Anthony", "Kevin", "Brian", "Gregory",
    "Larry", "Patrick", "Dennis", "Randy", "Wanda", "Carla",
]
LAST_NAMES = [
    "Holbrook", "Tice", "Munsey", "Gantry", "Osgood", "Pellum", "Rourke",
    "Dunmore", "Fetzer", "Yancey", "Castell", "Brannock", "Suggs", "Hardwick",
]

drivers = []
driver_ids = []

# 14 drivers total. We deliberately give the Little Rock lane / TRK-006
# drivers a much higher termination rate.
driver_specs = [
    # (id_num, hire_days_ago, status, years_exp)
    (1, 680, "active", 22),
    (2, 650, "active", 18),
    (3, 610, "active", 15),
    (4, 590, "active", 12),
    (5, 540, "terminated", 9),   # Little Rock lane driver, quit
    (6, 500, "active", 8),
    (7, 470, "terminated", 6),   # Little Rock lane driver, quit
    (8, 430, "active", 11),
    (9, 400, "active", 7),
    (10, 360, "terminated", 4),  # Little Rock lane driver, quit
    (11, 300, "active", 5),
    (12, 240, "active", 3),
    (13, 150, "active", 2),
    (14, 60, "active", 1),
]

for i, (num, hire_days_ago, status, years_exp) in enumerate(driver_specs):
    did = f"DRV-{num:03d}"
    driver_ids.append(did)
    hire_date = TODAY - datetime.timedelta(days=hire_days_ago)
    drivers.append({
        "driver_id": did,
        "first_name": FIRST_NAMES[i % len(FIRST_NAMES)],
        "last_name": LAST_NAMES[i % len(LAST_NAMES)],
        "hire_date": hire_date.isoformat(),
        "employment_status": status,
        "cdl_class": "A",
        "years_experience": years_exp,
        "home_terminal": "Joplin, MO",
    })

# Little Rock lane drivers (high turnover group) - DRV-005, 007, 010 (terminated)
# plus DRV-006 currently active but primarily assigned to that lane
LITTLE_ROCK_LANE_DRIVERS = {"DRV-005", "DRV-006", "DRV-007", "DRV-010"}

with open(os.path.join(BASE_DIR, "drivers.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "driver_id", "first_name", "last_name", "hire_date",
        "employment_status", "cdl_class", "years_experience", "home_terminal",
    ])
    writer.writeheader()
    writer.writerows(drivers)

# ---------------------------------------------------------------------------
# TRUCKS
# ---------------------------------------------------------------------------

truck_specs = [
    # (num, make, model, year, status, acquisition_days_ago, odometer, fuel_type)
    (1, "Freightliner", "Cascadia", 2021, "active", 900, 285000, "diesel"),
    (2, "Peterbilt", "579", 2022, "active", 700, 210000, "diesel"),
    (3, "Kenworth", "T680", 2020, "active", 1100, 340000, "diesel"),
    (4, "Freightliner", "Cascadia", 2019, "active", 1400, 425000, "diesel"),
    (5, "Peterbilt", "579", 2018, "active", 1600, 480000, "diesel"),
    (6, "Freightliner", "Cascadia", 2013, "active", 3200, 738000, "diesel"),  # bad MPG truck
    (7, "Kenworth", "T680", 2020, "active", 1050, 355000, "diesel"),
    (8, "Peterbilt", "579", 2022, "active", 650, 195000, "diesel"),
    (9, "Freightliner", "Cascadia", 2021, "active", 880, 275000, "diesel"),
    (10, "Kenworth", "T680", 2015, "active", 2400, 610000, "diesel"),
]

trucks = []
truck_ids = []
for num, make, model, year, status, acq_days_ago, odo, fuel in truck_specs:
    tid = f"TRK-{num:03d}"
    truck_ids.append(tid)
    acq_date = TODAY - datetime.timedelta(days=acq_days_ago)
    trucks.append({
        "truck_id": tid,
        "make": make,
        "model": model,
        "year": year,
        "status": status,
        "acquisition_date": acq_date.isoformat(),
        "current_odometer": odo,
        "fuel_type": fuel,
    })

with open(os.path.join(BASE_DIR, "trucks.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "truck_id", "make", "model", "year", "status",
        "acquisition_date", "current_odometer", "fuel_type",
    ])
    writer.writeheader()
    writer.writerows(trucks)

BAD_MPG_TRUCK = "TRK-006"

# ---------------------------------------------------------------------------
# CUSTOMERS
# ---------------------------------------------------------------------------

customers = [
    {
        "customer_id": "CUST-001",
        "customer_name": "Ozark Building Supply",
        "city": "Joplin",
        "state": "MO",
        "industry": "Building Materials",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-002",
        "customer_name": "Route 66 Ag Cooperative",
        "city": "Tulsa",
        "state": "OK",
        "industry": "Agriculture",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-003",
        "customer_name": "Sooner State Lumber",
        "city": "Oklahoma City",
        "state": "OK",
        "industry": "Building Materials",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-004",
        "customer_name": "Delta Farm & Feed",
        "city": "Little Rock",
        "state": "AR",
        "industry": "Agriculture",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-005",
        "customer_name": "Crossroads Hardware Distribution",
        "city": "Springfield",
        "state": "MO",
        "industry": "Building Materials",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-006",
        "customer_name": "Heartland Grain Exchange",
        "city": "Kansas City",
        "state": "MO",
        "industry": "Agriculture",
        "payment_terms_days": 15,
        "account_status": "active",
    },
]

with open(os.path.join(BASE_DIR, "customers.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "customer_id", "customer_name", "city", "state", "industry",
        "payment_terms_days", "account_status",
    ])
    writer.writeheader()
    writer.writerows(customers)

DETENTION_CUSTOMER = "CUST-001"  # Ozark Building Supply
SLOW_PAY_CUSTOMER = "CUST-002"   # Route 66 Ag Cooperative

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

route_specs = [
    ("ROUTE-01", "Joplin", "MO", "Little Rock", "AR", 270, 1.95),   # unprofitable lane
    ("ROUTE-02", "Little Rock", "AR", "Joplin", "MO", 270, 1.90),   # backhaul, also weak
    ("ROUTE-03", "Joplin", "MO", "Tulsa", "OK", 165, 2.55),
    ("ROUTE-04", "Tulsa", "OK", "Joplin", "MO", 165, 2.45),
    ("ROUTE-05", "Joplin", "MO", "Oklahoma City", "OK", 260, 2.35),
    ("ROUTE-06", "Oklahoma City", "OK", "Joplin", "MO", 260, 2.30),
    ("ROUTE-07", "Joplin", "MO", "Kansas City", "MO", 165, 2.60),
    ("ROUTE-08", "Kansas City", "MO", "Joplin", "MO", 165, 2.50),
    ("ROUTE-09", "Joplin", "MO", "Springfield", "MO", 75, 2.90),
    ("ROUTE-10", "Springfield", "MO", "Joplin", "MO", 75, 2.85),
    ("ROUTE-11", "Joplin", "MO", "Dallas", "TX", 430, 2.20),
    ("ROUTE-12", "Dallas", "TX", "Joplin", "MO", 430, 2.15),
]

routes = []
route_ids = []
for rid, oc, os_, dc, ds, dist, rate in route_specs:
    route_ids.append(rid)
    routes.append({
        "route_id": rid,
        "origin_city": oc,
        "origin_state": os_,
        "destination_city": dc,
        "destination_state": ds,
        "distance_miles": dist,
        "base_rate_per_mile": rate,
    })

with open(os.path.join(BASE_DIR, "routes.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "route_id", "origin_city", "origin_state", "destination_city",
        "destination_state", "distance_miles", "base_rate_per_mile",
    ])
    writer.writeheader()
    writer.writerows(routes)

LITTLE_ROCK_ROUTES = {"ROUTE-01", "ROUTE-02"}

# Map customers to the routes their freight typically travels on
CUSTOMER_ROUTE_MAP = {
    "CUST-001": ["ROUTE-01", "ROUTE-02", "ROUTE-09", "ROUTE-10"],  # Ozark - Joplin & Springfield
    "CUST-002": ["ROUTE-03", "ROUTE-04"],                           # Route 66 Ag - Tulsa
    "CUST-003": ["ROUTE-05", "ROUTE-06"],                           # Sooner State - OKC
    "CUST-004": ["ROUTE-01", "ROUTE-02"],                           # Delta Farm & Feed - Little Rock
    "CUST-005": ["ROUTE-09", "ROUTE-10"],                           # Crossroads - Springfield
    "CUST-006": ["ROUTE-07", "ROUTE-08"],                           # Heartland Grain - KC
}

# ---------------------------------------------------------------------------
# LOADS, TRIPS, FUEL PURCHASES, DELIVERY EVENTS
# ---------------------------------------------------------------------------

FREIGHT_TYPES_BY_INDUSTRY = {
    "Building Materials": ["lumber", "roofing supplies", "drywall", "hardware"],
    "Agriculture": ["bagged seed", "bagged feed", "fertilizer", "grain"],
}

FUEL_STOPS = [
    "Joplin, MO", "Springfield, MO", "Tulsa, OK", "Oklahoma City, OK",
    "Little Rock, AR", "Kansas City, MO", "Dallas, TX", "Fort Smith, AR",
]

loads = []
trips = []
fuel_purchases = []
delivery_events = []
maintenance_records = []

load_counter = 1
trip_counter = 1
fuel_counter = 1
event_counter = 1
maint_counter = 1

FLEET_AVG_MPG = 6.9
BAD_TRUCK_MPG = 5.2
FLEET_AVG_DETENTION = 11
BAD_DETENTION = 48

# Diesel price trend across the 2-year window (roughly reflects 2024-2026 range)
def diesel_price(day_offset):
    # linear-ish drift with noise, range ~3.80 - 4.50
    frac = day_offset / 730
    base = 3.85 + 0.5 * frac
    return round(base + random.uniform(-0.15, 0.15), 3)

TOTAL_DAYS = 730
NUM_LOADS = 4500  # within 3,000-6,000 range for small_fleet

# distribute loads across days
for day_offset in range(TOTAL_DAYS):
    current_date = START_DATE + datetime.timedelta(days=day_offset)
    # skip most Sundays (lighter ops)
    if current_date.weekday() == 6 and random.random() < 0.7:
        continue

    loads_today = random.choices([2, 3, 4, 5, 6, 7, 8], weights=[8, 15, 20, 22, 18, 12, 5])[0]

    for _ in range(loads_today):
        if load_counter > NUM_LOADS:
            break

        customer = random.choice(customers)
        cust_id = customer["customer_id"]
        route_id = random.choice(CUSTOMER_ROUTE_MAP[cust_id])
        route = next(r for r in routes if r["route_id"] == route_id)

        freight_type = random.choice(FREIGHT_TYPES_BY_INDUSTRY[customer["industry"]])
        weight = random.randint(28000, 45000)

        distance = route["distance_miles"]
        base_rate = route["base_rate_per_mile"]
        revenue = round(distance * base_rate * random.uniform(0.95, 1.08), 2)
        fuel_surcharge = round(distance * random.uniform(0.15, 0.35), 2)

        load_id = f"LD-{load_counter:06d}"
        load_status = "delivered" if (TODAY - current_date).days > 2 else random.choice(["delivered", "in_transit"])

        loads.append({
            "load_id": load_id,
            "customer_id": cust_id,
            "route_id": route_id,
            "load_date": current_date.isoformat(),
            "freight_type": freight_type,
            "weight_lbs": weight,
            "revenue": revenue,
            "fuel_surcharge": fuel_surcharge,
            "load_status": load_status,
        })

        # ---- Trip ----
        # Assign truck: bias Little Rock routes toward TRK-006 and the
        # high-turnover driver pool
        if route_id in LITTLE_ROCK_ROUTES:
            truck_id = random.choices(
                truck_ids,
                weights=[3 if t != BAD_MPG_TRUCK else 55 for t in truck_ids],
            )[0]
            eligible_drivers = [d for d in driver_ids if d in LITTLE_ROCK_LANE_DRIVERS] or driver_ids
            # only pick drivers who were employed at the time
            valid = []
            for d in eligible_drivers:
                drec = next(x for x in drivers if x["driver_id"] == d)
                hire = datetime.date.fromisoformat(drec["hire_date"])
                if hire <= current_date:
                    valid.append(d)
            driver_id = random.choice(valid) if valid else random.choice(driver_ids)
        else:
            truck_id = random.choices(
                truck_ids,
                weights=[10 if t != BAD_MPG_TRUCK else 2 for t in truck_ids],
            )[0]
            valid = []
            for d in driver_ids:
                drec = next(x for x in drivers if x["driver_id"] == d)
                hire = datetime.date.fromisoformat(drec["hire_date"])
                if hire <= current_date:
                    valid.append(d)
            driver_id = random.choice(valid) if valid else random.choice(driver_ids)

        actual_miles = round(distance * random.uniform(1.0, 1.06), 1)

        if truck_id == BAD_MPG_TRUCK:
            actual_mpg = round(random.uniform(BAD_TRUCK_MPG - 0.3, BAD_TRUCK_MPG + 0.3), 2)
        else:
            actual_mpg = round(random.uniform(FLEET_AVG_MPG - 0.5, FLEET_AVG_MPG + 0.6), 2)

        fuel_gallons = round(actual_miles / actual_mpg, 2)

        dep_hour = random.randint(4, 9)
        departure_dt = datetime.datetime.combine(current_date, datetime.time(dep_hour, random.randint(0, 59)))
        drive_hours = actual_miles / random.uniform(48, 56)
        arrival_dt = departure_dt + datetime.timedelta(hours=drive_hours)

        on_time_flag = random.random() < (0.70 if route_id in LITTLE_ROCK_ROUTES and truck_id == BAD_MPG_TRUCK else 0.90)

        trip_id = f"TRP-{trip_counter:06d}"
        trips.append({
            "trip_id": trip_id,
            "load_id": load_id,
            "driver_id": driver_id,
            "truck_id": truck_id,
            "actual_miles": actual_miles,
            "fuel_gallons": fuel_gallons,
            "actual_mpg": actual_mpg,
            "departure_time": departure_dt.isoformat(sep=" "),
            "arrival_time": arrival_dt.isoformat(sep=" "),
            "on_time_flag": on_time_flag,
        })

        # ---- Fuel purchase ----
        price = diesel_price(day_offset)
        total_cost = round(fuel_gallons * price, 2)
        fuel_purchases.append({
            "purchase_id": f"FUEL-{fuel_counter:06d}",
            "trip_id": trip_id,
            "truck_id": truck_id,
            "driver_id": driver_id,
            "purchase_date": current_date.isoformat(),
            "gallons": fuel_gallons,
            "price_per_gallon": price,
            "total_cost": total_cost,
            "location": random.choice(FUEL_STOPS),
        })
        fuel_counter += 1

        # ---- Delivery event ----
        scheduled_time = arrival_dt.replace(minute=0, second=0)
        if cust_id == DETENTION_CUSTOMER:
            detention = max(5, int(random.gauss(BAD_DETENTION, 10)))
        else:
            detention = max(0, int(random.gauss(FLEET_AVG_DETENTION, 5)))

        actual_time = scheduled_time + datetime.timedelta(minutes=detention + random.randint(-5, 15))
        on_time_delivery = detention < 30 and random.random() < 0.9

        delivery_events.append({
            "event_id": f"EVT-{event_counter:06d}",
            "load_id": load_id,
            "trip_id": trip_id,
            "facility_type": "delivery",
            "scheduled_time": scheduled_time.isoformat(sep=" "),
            "actual_time": actual_time.isoformat(sep=" "),
            "detention_minutes": detention,
            "on_time": on_time_delivery,
        })
        event_counter += 1

        trip_counter += 1
        load_counter += 1

    if load_counter > NUM_LOADS:
        break

with open(os.path.join(BASE_DIR, "loads.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "load_id", "customer_id", "route_id", "load_date", "freight_type",
        "weight_lbs", "revenue", "fuel_surcharge", "load_status",
    ])
    writer.writeheader()
    writer.writerows(loads)

with open(os.path.join(BASE_DIR, "trips.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "trip_id", "load_id", "driver_id", "truck_id", "actual_miles",
        "fuel_gallons", "actual_mpg", "departure_time", "arrival_time",
        "on_time_flag",
    ])
    writer.writeheader()
    writer.writerows(trips)

with open(os.path.join(BASE_DIR, "fuel_purchases.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "purchase_id", "trip_id", "truck_id", "driver_id", "purchase_date",
        "gallons", "price_per_gallon", "total_cost", "location",
    ])
    writer.writeheader()
    writer.writerows(fuel_purchases)

with open(os.path.join(BASE_DIR, "delivery_events.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "event_id", "load_id", "trip_id", "facility_type", "scheduled_time",
        "actual_time", "detention_minutes", "on_time",
    ])
    writer.writeheader()
    writer.writerows(delivery_events)

# ---------------------------------------------------------------------------
# MAINTENANCE RECORDS
# ---------------------------------------------------------------------------

SERVICE_TYPES = [
    "oil change", "tire replacement", "brake service", "DOT inspection",
    "transmission service", "engine repair", "coolant system", "alignment",
]

for truck in trucks:
    tid = truck["truck_id"]
    is_bad_truck = tid == BAD_MPG_TRUCK
    num_services = random.randint(14, 20) if is_bad_truck else random.randint(6, 11)
    odometer_base = truck["current_odometer"]

    for i in range(num_services):
        days_ago = random.randint(10, 720)
        service_date = TODAY - datetime.timedelta(days=days_ago)
        service_type = random.choice(SERVICE_TYPES)
        if is_bad_truck and service_type in ("engine repair", "transmission service", "coolant system"):
            cost = round(random.uniform(2200, 6500), 2)
            downtime = round(random.uniform(24, 96), 1)
        elif service_type in ("engine repair", "transmission service"):
            cost = round(random.uniform(900, 3000), 2)
            downtime = round(random.uniform(8, 40), 1)
        else:
            cost = round(random.uniform(150, 900), 2)
            downtime = round(random.uniform(1, 8), 1)

        odo_at_service = max(0, odometer_base - int(days_ago * random.uniform(140, 220)))

        maintenance_records.append({
            "record_id": f"MAINT-{maint_counter:05d}",
            "truck_id": tid,
            "service_date": service_date.isoformat(),
            "service_type": service_type,
            "cost": cost,
            "downtime_hours": downtime,
            "odometer_at_service": odo_at_service,
        })
        maint_counter += 1

with open(os.path.join(BASE_DIR, "maintenance_records.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "record_id", "truck_id", "service_date", "service_type", "cost",
        "downtime_hours", "odometer_at_service",
    ])
    writer.writeheader()
    writer.writerows(maintenance_records)

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------

print("Data generation complete.")
print(f"  drivers.csv:            {len(drivers)} rows")
print(f"  trucks.csv:             {len(trucks)} rows")
print(f"  customers.csv:          {len(customers)} rows")
print(f"  routes.csv:             {len(routes)} rows")
print(f"  loads.csv:              {len(loads)} rows")
print(f"  trips.csv:              {len(trips)} rows")
print(f"  fuel_purchases.csv:     {len(fuel_purchases)} rows")
print(f"  delivery_events.csv:    {len(delivery_events)} rows")
print(f"  maintenance_records.csv:{len(maintenance_records)} rows")
