"""
Synthetic data generator for Cascade Summit Freightways (mid_size_carrier).

Embeds 5 pain points:
1. TRK-047 (2011 Freightliner Cascadia, ~880k mi) runs ~4.9 MPG vs fleet ~6.9 MPG.
2. TitanBolt Industrial Supply (Dallas) averages ~48 min detention vs fleet ~11 min.
3. Seattle->Atlanta lane nets ~$1.55/mile after fuel vs $2.05/mile breakeven.
4. Chicago-terminal 2023 hire cohort (~20 drivers) has much higher termination rate.
5. Aging truck cohort TRK-041..TRK-048 (2010-2012) has high maintenance cost/downtime.
"""

import csv
import random
import datetime
import os

random.seed(20260703)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

TODAY = datetime.date(2026, 7, 3)
START_DATE = TODAY - datetime.timedelta(days=730)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

N_TRUCKS = 110
N_DRIVERS = 165
AGING_TRUCK_IDS = [f"TRK-{i:03d}" for i in range(41, 49)]  # TRK-041..TRK-048
BAD_MPG_TRUCK = "TRK-047"

CUSTOMERS = [
    ("CUST-01", "Cascade Paper Products", "Spokane", "WA", "Paper/Pulp", 30),
    ("CUST-02", "Evergreen Foods Co-op", "Portland", "OR", "Food/Grocery", 30),
    ("CUST-03", "TitanBolt Industrial Supply", "Dallas", "TX", "Industrial/Hardware", 45),
    ("CUST-04", "Northwind Appliance Distributors", "Chicago", "IL", "Appliances", 30),
    ("CUST-05", "Rocky Summit Building Materials", "Denver", "CO", "Building Materials", 30),
    ("CUST-06", "Peachtree Consumer Goods", "Atlanta", "GA", "Consumer Goods", 45),
    ("CUST-07", "Lonestar Auto Parts Wholesale", "Dallas", "TX", "Automotive Parts", 30),
    ("CUST-08", "Pioneer Home Furnishings", "Seattle", "WA", "Furniture", 30),
]

ROUTES = [
    # route_id, origin_city, origin_state, dest_city, dest_state, distance, base_rate
    ("RTE-01", "Spokane", "WA", "Chicago", "IL", 1980, 2.35),
    ("RTE-02", "Spokane", "WA", "Dallas", "TX", 1970, 2.30),
    ("RTE-03", "Portland", "OR", "Denver", "CO", 1240, 2.15),
    ("RTE-04", "Seattle", "WA", "Atlanta", "GA", 2630, 2.05),
    ("RTE-05", "Chicago", "IL", "Spokane", "WA", 1980, 2.20),
    ("RTE-06", "Dallas", "TX", "Spokane", "WA", 1970, 2.15),
    ("RTE-07", "Denver", "CO", "Portland", "OR", 1240, 2.10),
    ("RTE-08", "Atlanta", "GA", "Seattle", "WA", 2630, 1.95),
    ("RTE-09", "Spokane", "WA", "Portland", "OR", 350, 2.60),
    ("RTE-10", "Portland", "OR", "Spokane", "WA", 350, 2.55),
    ("RTE-11", "Dallas", "TX", "Chicago", "IL", 930, 2.40),
    ("RTE-12", "Chicago", "IL", "Dallas", "TX", 930, 2.45),
]

ROUTE_TO_CUSTOMERS = {
    "RTE-01": ["CUST-01", "CUST-04"],
    "RTE-05": ["CUST-04", "CUST-01"],
    "RTE-02": ["CUST-01", "CUST-03"],
    "RTE-06": ["CUST-03", "CUST-07"],
    "RTE-03": ["CUST-02", "CUST-05"],
    "RTE-07": ["CUST-05", "CUST-02"],
    "RTE-04": ["CUST-08", "CUST-06"],
    "RTE-08": ["CUST-06", "CUST-08"],
    "RTE-09": ["CUST-01", "CUST-08"],
    "RTE-10": ["CUST-08", "CUST-01"],
    "RTE-11": ["CUST-03", "CUST-07"],
    "RTE-12": ["CUST-04", "CUST-07"],
}

TRUCK_MAKES_MODELS = [
    ("Freightliner", "Cascadia"),
    ("Peterbilt", "579"),
    ("Peterbilt", "389"),
    ("Kenworth", "T680"),
    ("Volvo", "VNL 760"),
]

FIRST_NAMES = [
    "James", "Robert", "Michael", "David", "William", "Richard", "Joseph", "Thomas",
    "Charles", "Daniel", "Matthew", "Anthony", "Mark", "Steven", "Paul", "Andrew",
    "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey",
    "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Stephen", "Jonathan", "Larry",
    "Justin", "Scott", "Brandon", "Frank", "Benjamin", "Gregory", "Samuel", "Raymond",
    "Maria", "Susan", "Margaret", "Dorothy", "Lisa", "Nancy", "Karen", "Betty",
    "Sandra", "Ashley", "Kimberly", "Donna", "Emily", "Michelle", "Carol", "Amanda",
    "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Amy",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Braddock", "Kowalski", "Ferreira", "Nowak", "Okafor",
]

TERMINALS = ["Spokane, WA", "Chicago, IL"]

FUEL_LOCATIONS = [
    "Pilot Travel Center - Spokane, WA", "Love's Travel Stop - Missoula, MT",
    "TA Travel Center - Billings, MT", "Pilot Travel Center - Rapid City, SD",
    "Flying J - North Platte, NE", "Love's Travel Stop - Des Moines, IA",
    "Pilot Travel Center - Chicago, IL", "TA Travel Center - Joliet, IL",
    "Love's Travel Stop - Oklahoma City, OK", "Flying J - Wichita Falls, TX",
    "Pilot Travel Center - Dallas, TX", "Love's Travel Stop - Denver, CO",
    "TA Travel Center - Salt Lake City, UT", "Pilot Travel Center - Portland, OR",
    "Flying J - Boise, ID", "Love's Travel Stop - Atlanta, GA",
    "TA Travel Center - Knoxville, TN", "Pilot Travel Center - Nashville, TN",
    "Flying J - Amarillo, TX", "Love's Travel Stop - Seattle, WA",
]


def random_date(start, end):
    delta = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, max(delta, 0)))


def diesel_price_for_date(d):
    # Reflect 2024-2026 range with mild seasonal wobble
    days_in = (d - START_DATE).days
    base = 3.85 + 0.35 * (days_in / 730.0)
    season = 0.12 * ((d.month % 12) / 12.0)
    noise = random.uniform(-0.15, 0.15)
    return round(max(3.6, base + season + noise), 3)


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------

def gen_drivers():
    drivers = []
    chicago_2023_cohort_ids = set()

    # Reserve driver ids 146-165 as the Chicago 2023 hire cohort (20 drivers)
    chicago_cohort_range = list(range(146, 166))

    for i in range(1, N_DRIVERS + 1):
        driver_id = f"DRV-{i:03d}"
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        if i in chicago_cohort_range:
            # Chicago 2023 hire cohort - hired in 2023, elevated turnover
            hire_date = random_date(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
            home_terminal = "Chicago, IL"
            chicago_2023_cohort_ids.add(driver_id)
            # ~65% terminated within the dataset window
            if random.random() < 0.65:
                employment_status = "terminated"
            else:
                employment_status = "active"
        else:
            hire_date = random_date(START_DATE - datetime.timedelta(days=365 * 8), TODAY - datetime.timedelta(days=60))
            home_terminal = random.choices(TERMINALS, weights=[0.75, 0.25])[0]
            # Baseline ~15% annual turnover -> roughly 12% terminated in dataset
            employment_status = "terminated" if random.random() < 0.12 else "active"

        years_experience = max(1, (TODAY - hire_date).days // 365 + random.randint(1, 6))
        cdl_class = random.choices(["Class A", "Class B"], weights=[0.94, 0.06])[0]

        drivers.append({
            "driver_id": driver_id,
            "first_name": first,
            "last_name": last,
            "hire_date": hire_date.isoformat(),
            "employment_status": employment_status,
            "cdl_class": cdl_class,
            "years_experience": years_experience,
            "home_terminal": home_terminal,
        })

    return drivers, chicago_2023_cohort_ids


# ---------------------------------------------------------------------------
# Trucks
# ---------------------------------------------------------------------------

def gen_trucks():
    trucks = []
    for i in range(1, N_TRUCKS + 1):
        truck_id = f"TRK-{i:03d}"
        if truck_id in AGING_TRUCK_IDS:
            year = random.randint(2010, 2012)
            make, model = random.choice([("Freightliner", "Cascadia"), ("Peterbilt", "389")])
            acquisition_date = random_date(datetime.date(year, 1, 1), datetime.date(year, 12, 31))
            odometer = random.randint(720000, 910000)
        else:
            year = random.randint(2016, 2024)
            make, model = random.choice(TRUCK_MAKES_MODELS)
            acquisition_date = random_date(datetime.date(year, 1, 1), min(datetime.date(year, 12, 31), TODAY))
            odometer = random.randint(90000, 520000)

        status = random.choices(["active", "active", "active", "shop", "retired"], weights=[80, 10, 5, 4, 1])[0]

        trucks.append({
            "truck_id": truck_id,
            "make": make,
            "model": model,
            "year": year,
            "status": status,
            "acquisition_date": acquisition_date.isoformat(),
            "current_odometer": odometer,
            "fuel_type": "diesel",
        })
    return trucks


# ---------------------------------------------------------------------------
# Customers / Routes
# ---------------------------------------------------------------------------

def gen_customers():
    rows = []
    for cid, name, city, state, industry, terms in CUSTOMERS:
        rows.append({
            "customer_id": cid,
            "customer_name": name,
            "city": city,
            "state": state,
            "industry": industry,
            "payment_terms_days": terms,
            "account_status": "active",
        })
    return rows


def gen_routes():
    rows = []
    for rid, oc, os_, dc, ds, dist, rate in ROUTES:
        rows.append({
            "route_id": rid,
            "origin_city": oc,
            "origin_state": os_,
            "destination_city": dc,
            "destination_state": ds,
            "distance_miles": dist,
            "base_rate_per_mile": rate,
        })
    return rows


# ---------------------------------------------------------------------------
# Loads, trips, fuel purchases, delivery events, maintenance
# ---------------------------------------------------------------------------

def gen_operations(drivers, trucks, chicago_2023_cohort_ids):
    active_driver_ids = [d["driver_id"] for d in drivers]
    driver_hire_dates = {d["driver_id"]: datetime.date.fromisoformat(d["hire_date"]) for d in drivers}
    driver_status = {d["driver_id"]: d["employment_status"] for d in drivers}

    truck_status = {t["truck_id"]: t["status"] for t in trucks}
    usable_trucks = [t["truck_id"] for t in trucks if t["status"] != "retired"]

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

    N_LOADS_TARGET = 62000

    route_weights = [0.16, 0.15, 0.12, 0.12, 0.14, 0.12, 0.08, 0.07, 0.02, 0.01, 0.005, 0.005]

    for _ in range(N_LOADS_TARGET):
        route = random.choices(ROUTES, weights=route_weights)[0]
        route_id, oc, os_, dc, ds, distance, base_rate = route
        cust_options = ROUTE_TO_CUSTOMERS.get(route_id, [c[0] for c in CUSTOMERS])
        customer_id = random.choice(cust_options)

        load_date = random_date(START_DATE, TODAY)

        # pick a driver/truck pair that existed at load_date
        eligible_drivers = [d for d in active_driver_ids if driver_hire_dates[d] <= load_date]
        if not eligible_drivers:
            continue
        driver_id = random.choice(eligible_drivers)
        truck_id = random.choice(usable_trucks)

        load_id = f"LD-{load_counter:06d}"
        trip_id = f"TRP-{trip_counter:06d}"

        weight_lbs = random.randint(8000, 45000)
        freight_type = "dry van"

        # Rate variation per load
        rate_variation = random.uniform(0.90, 1.08)
        effective_rate = base_rate * rate_variation

        # Pain point #3: Seattle->Atlanta (RTE-04) and Atlanta->Seattle (RTE-08) run structurally low net margin
        is_low_margin_lane = route_id in ("RTE-04", "RTE-08")
        if is_low_margin_lane:
            effective_rate = base_rate * random.uniform(0.85, 0.98)

        revenue = round(effective_rate * distance, 2)
        fuel_surcharge = round(distance * random.uniform(0.08, 0.22), 2)

        load_status = random.choices(
            ["delivered", "delivered", "delivered", "delivered", "cancelled"],
            weights=[70, 15, 10, 4, 1]
        )[0]

        loads.append({
            "load_id": load_id,
            "customer_id": customer_id,
            "route_id": route_id,
            "load_date": load_date.isoformat(),
            "freight_type": freight_type,
            "weight_lbs": weight_lbs,
            "revenue": revenue,
            "fuel_surcharge": fuel_surcharge,
            "load_status": load_status,
        })

        if load_status == "cancelled":
            load_counter += 1
            continue

        # --- Trip ---
        actual_miles = round(distance * random.uniform(0.98, 1.05), 1)

        # Pain point #1: TRK-047 bad MPG
        if truck_id == BAD_MPG_TRUCK:
            actual_mpg = round(random.uniform(4.6, 5.2), 2)
        elif truck_id in AGING_TRUCK_IDS:
            actual_mpg = round(random.uniform(5.6, 6.3), 2)
        else:
            actual_mpg = round(random.uniform(6.3, 7.4), 2)

        fuel_gallons = round(actual_miles / actual_mpg, 2)

        departure_dt = datetime.datetime.combine(load_date, datetime.time(random.randint(4, 18), random.choice([0, 15, 30, 45])))
        travel_hours = actual_miles / random.uniform(48, 56)
        arrival_dt = departure_dt + datetime.timedelta(hours=travel_hours)

        # On-time rate ~85-95% fleet average, worse for low-margin long-haul lane and TitanBolt detentions
        on_time_prob = 0.90
        if is_low_margin_lane:
            on_time_prob = 0.83
        on_time_flag = random.random() < on_time_prob

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

        # --- Fuel purchases (1-3 per trip) ---
        n_fuel_stops = 1 if actual_miles < 500 else random.randint(2, 4)
        remaining_gallons = fuel_gallons
        for stop in range(n_fuel_stops):
            purchase_id = f"FUEL-{fuel_counter:06d}"
            gallons = round(remaining_gallons / (n_fuel_stops - stop) * random.uniform(0.85, 1.15), 2) if stop < n_fuel_stops - 1 else round(remaining_gallons, 2)
            gallons = max(gallons, 5.0)
            remaining_gallons = max(remaining_gallons - gallons, 0)
            purchase_date = (departure_dt + datetime.timedelta(hours=stop * travel_hours / max(n_fuel_stops, 1))).date()
            price = diesel_price_for_date(purchase_date)
            total_cost = round(gallons * price, 2)

            fuel_purchases.append({
                "purchase_id": purchase_id,
                "trip_id": trip_id,
                "truck_id": truck_id,
                "driver_id": driver_id,
                "purchase_date": purchase_date.isoformat(),
                "gallons": gallons,
                "price_per_gallon": price,
                "total_cost": total_cost,
                "location": random.choice(FUEL_LOCATIONS),
            })
            fuel_counter += 1

        # --- Delivery event ---
        event_id = f"EVT-{event_counter:06d}"
        scheduled_time = arrival_dt.replace(minute=0, second=0) + datetime.timedelta(hours=random.choice([0, 1]))

        # Pain point #2: TitanBolt (CUST-03) has high detention
        if customer_id == "CUST-03":
            detention_minutes = max(0, int(random.gauss(48, 14)))
        else:
            detention_minutes = max(0, int(random.gauss(11, 6)))

        actual_time = scheduled_time + datetime.timedelta(minutes=detention_minutes + random.randint(-10, 20))
        event_on_time = detention_minutes <= 20 and on_time_flag

        delivery_events.append({
            "event_id": event_id,
            "load_id": load_id,
            "trip_id": trip_id,
            "facility_type": random.choice(["shipper", "consignee", "consignee", "cross-dock"]),
            "scheduled_time": scheduled_time.isoformat(sep=" "),
            "actual_time": actual_time.isoformat(sep=" "),
            "detention_minutes": detention_minutes,
            "on_time": event_on_time,
        })

        load_counter += 1
        trip_counter += 1
        event_counter += 1

    # --- Maintenance records ---
    for truck in trucks:
        truck_id = truck["truck_id"]
        is_aging = truck_id in AGING_TRUCK_IDS
        n_records = random.randint(14, 22) if is_aging else random.randint(4, 10)
        acq_date = datetime.date.fromisoformat(truck["acquisition_date"])
        service_window_start = max(acq_date, START_DATE)

        for _ in range(n_records):
            record_id = f"MNT-{maint_counter:06d}"
            service_date = random_date(service_window_start, TODAY)
            if is_aging:
                service_type = random.choices(
                    ["engine repair", "transmission repair", "brake system", "electrical",
                     "cooling system", "routine PM service", "tire replacement", "suspension"],
                    weights=[18, 12, 12, 10, 10, 15, 13, 10]
                )[0]
                cost = round(random.uniform(1800, 9500), 2)
                downtime_hours = round(random.uniform(18, 96), 1)
            else:
                service_type = random.choices(
                    ["routine PM service", "tire replacement", "brake system", "electrical",
                     "engine repair", "cooling system"],
                    weights=[40, 20, 15, 10, 8, 7]
                )[0]
                cost = round(random.uniform(250, 3200), 2)
                downtime_hours = round(random.uniform(2, 24), 1)

            odometer_at_service = random.randint(
                max(0, truck["current_odometer"] - 400000), truck["current_odometer"]
            )

            maintenance_records.append({
                "record_id": record_id,
                "truck_id": truck_id,
                "service_date": service_date.isoformat(),
                "service_type": service_type,
                "cost": cost,
                "downtime_hours": downtime_hours,
                "odometer_at_service": odometer_at_service,
            })
            maint_counter += 1

    return loads, trips, fuel_purchases, delivery_events, maintenance_records


# ---------------------------------------------------------------------------
# Write CSVs
# ---------------------------------------------------------------------------

def write_csv(filename, rows, fieldnames):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {filename}: {len(rows)} rows")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    drivers, chicago_2023_cohort_ids = gen_drivers()
    trucks = gen_trucks()
    customers = gen_customers()
    routes = gen_routes()
    loads, trips, fuel_purchases, delivery_events, maintenance_records = gen_operations(
        drivers, trucks, chicago_2023_cohort_ids
    )

    write_csv("drivers.csv", drivers,
              ["driver_id", "first_name", "last_name", "hire_date", "employment_status",
               "cdl_class", "years_experience", "home_terminal"])

    write_csv("trucks.csv", trucks,
              ["truck_id", "make", "model", "year", "status", "acquisition_date",
               "current_odometer", "fuel_type"])

    write_csv("customers.csv", customers,
              ["customer_id", "customer_name", "city", "state", "industry",
               "payment_terms_days", "account_status"])

    write_csv("routes.csv", routes,
              ["route_id", "origin_city", "origin_state", "destination_city",
               "destination_state", "distance_miles", "base_rate_per_mile"])

    write_csv("loads.csv", loads,
              ["load_id", "customer_id", "route_id", "load_date", "freight_type",
               "weight_lbs", "revenue", "fuel_surcharge", "load_status"])

    write_csv("trips.csv", trips,
              ["trip_id", "load_id", "driver_id", "truck_id", "actual_miles",
               "fuel_gallons", "actual_mpg", "departure_time", "arrival_time", "on_time_flag"])

    write_csv("fuel_purchases.csv", fuel_purchases,
              ["purchase_id", "trip_id", "truck_id", "driver_id", "purchase_date",
               "gallons", "price_per_gallon", "total_cost", "location"])

    write_csv("delivery_events.csv", delivery_events,
              ["event_id", "load_id", "trip_id", "facility_type", "scheduled_time",
               "actual_time", "detention_minutes", "on_time"])

    write_csv("maintenance_records.csv", maintenance_records,
              ["record_id", "truck_id", "service_date", "service_type", "cost",
               "downtime_hours", "odometer_at_service"])

    print("\nDone generating Cascade Summit Freightways synthetic data.")


if __name__ == "__main__":
    main()
