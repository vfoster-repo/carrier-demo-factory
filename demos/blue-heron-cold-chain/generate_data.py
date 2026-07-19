#!/usr/bin/env python3
"""Synthetic data generator for Blue Heron Cold Chain (owner_operator carrier)."""

import csv
import random
import datetime
import os

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

TODAY = datetime.date(2026, 7, 2)
START_DATE = TODAY - datetime.timedelta(days=730)

# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

DRIVERS = [
    {
        "driver_id": "DRV-01",
        "first_name": "Dale",
        "last_name": "Kowalczyk",
        "hire_date": "2017-03-01",
        "employment_status": "active",
        "cdl_class": "A",
        "years_experience": 18,
        "home_terminal": "Mount Vernon, WA",
    },
    {
        "driver_id": "DRV-02",
        "first_name": "Renata",
        "last_name": "Kowalczyk",
        "hire_date": "2019-05-15",
        "employment_status": "active",
        "cdl_class": "A",
        "years_experience": 6,
        "home_terminal": "Mount Vernon, WA",
    },
]

TRUCKS = [
    {
        "truck_id": "TRK-01",
        "make": "Freightliner",
        "model": "Cascadia",
        "year": 2016,
        "status": "active",
        "acquisition_date": "2017-03-10",
        "current_odometer": 641500,
        "fuel_type": "diesel",
    },
    {
        "truck_id": "TRK-02",
        "make": "Kenworth",
        "model": "T680",
        "year": 2021,
        "status": "active",
        "acquisition_date": "2021-06-20",
        "current_odometer": 312800,
        "fuel_type": "diesel",
    },
]

# truck -> driver (mostly fixed pairing, matches company story)
TRUCK_DRIVER = {"TRK-01": "DRV-01", "TRK-02": "DRV-02"}

CUSTOMERS = [
    {
        "customer_id": "CUST-01",
        "customer_name": "Skagit Valley Produce",
        "city": "Mount Vernon",
        "state": "WA",
        "industry": "Produce",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-02",
        "customer_name": "Bellingham Cold Storage",
        "city": "Bellingham",
        "state": "WA",
        "industry": "Seafood",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-03",
        "customer_name": "Cascade Berry Growers",
        "city": "Burlington",
        "state": "WA",
        "industry": "Produce",
        "payment_terms_days": 15,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-04",
        "customer_name": "Golden Gate Fresh Distributors",
        "city": "Oakland",
        "state": "CA",
        "industry": "Distribution",
        "payment_terms_days": 45,
        "account_status": "active",
    },
]

# Routes: southbound loaded lanes (profitable) + northbound backhaul lanes (thin/losing)
ROUTES = [
    {
        "route_id": "RTE-01",
        "origin_city": "Mount Vernon", "origin_state": "WA",
        "destination_city": "Portland", "destination_state": "OR",
        "distance_miles": 260,
        "base_rate_per_mile": 2.85,
        "direction": "southbound",
        "customer_id": "CUST-01",
    },
    {
        "route_id": "RTE-02",
        "origin_city": "Bellingham", "origin_state": "WA",
        "destination_city": "Oakland", "destination_state": "CA",
        "distance_miles": 780,
        "base_rate_per_mile": 2.95,
        "direction": "southbound",
        "customer_id": "CUST-02",
    },
    {
        "route_id": "RTE-03",
        "origin_city": "Burlington", "origin_state": "WA",
        "destination_city": "Oakland", "destination_state": "CA",
        "distance_miles": 800,
        "base_rate_per_mile": 3.05,
        "direction": "southbound",
        "customer_id": "CUST-03",
    },
    {
        "route_id": "RTE-04",
        "origin_city": "Mount Vernon", "origin_state": "WA",
        "destination_city": "Oakland", "destination_state": "CA",
        "distance_miles": 810,
        "base_rate_per_mile": 2.60,
        "direction": "southbound",
        "customer_id": "CUST-04",
    },
    # Northbound backhauls - low rate, load-board sourced, higher deadhead
    {
        "route_id": "RTE-05",
        "origin_city": "Oakland", "origin_state": "CA",
        "destination_city": "Mount Vernon", "destination_state": "WA",
        "distance_miles": 815,
        "base_rate_per_mile": 1.65,
        "direction": "northbound",
        "customer_id": None,
    },
    {
        "route_id": "RTE-06",
        "origin_city": "Portland", "origin_state": "OR",
        "destination_city": "Bellingham", "destination_state": "WA",
        "distance_miles": 300,
        "base_rate_per_mile": 1.75,
        "direction": "northbound",
        "customer_id": None,
    },
    {
        "route_id": "RTE-07",
        "origin_city": "Oakland", "origin_state": "CA",
        "destination_city": "Burlington", "destination_state": "WA",
        "distance_miles": 805,
        "base_rate_per_mile": 1.55,
        "direction": "northbound",
        "customer_id": None,
    },
]

ROUTES_BY_ID = {r["route_id"]: r for r in ROUTES}
SOUTHBOUND_ROUTES = [r for r in ROUTES if r["direction"] == "southbound"]
NORTHBOUND_ROUTES = [r for r in ROUTES if r["direction"] == "northbound"]

# Northbound backhaul customer stand-ins (load-board brokers, not core shippers)
BACKHAUL_CUSTOMERS = [
    {
        "customer_id": "CUST-05",
        "customer_name": "Pacific Coast Load Board Spot",
        "city": "Oakland",
        "state": "CA",
        "industry": "Brokerage",
        "payment_terms_days": 30,
        "account_status": "active",
    },
    {
        "customer_id": "CUST-06",
        "customer_name": "Evergreen Freight Match",
        "city": "Portland",
        "state": "OR",
        "industry": "Brokerage",
        "payment_terms_days": 30,
        "account_status": "active",
    },
]
ALL_CUSTOMERS = CUSTOMERS + BACKHAUL_CUSTOMERS

DIESEL_STATIONS = [
    ("Love's Travel Stop", "Mount Vernon, WA"),
    ("Pilot Flying J", "Portland, OR"),
    ("TA Travel Center", "Redding, CA"),
    ("Love's Travel Stop", "Sacramento, CA"),
    ("Pilot Flying J", "Grants Pass, OR"),
    ("Chevron", "Oakland, CA"),
]

FREIGHT_TYPES = {
    "Produce": "Refrigerated - Produce",
    "Seafood": "Refrigerated - Seafood",
    "Distribution": "Refrigerated - Mixed",
    "Brokerage": "Refrigerated - Backhaul Mixed",
}


def daterange_days(start, end):
    d = start
    while d <= end:
        yield d
        d += datetime.timedelta(days=1)


def diesel_price_for_date(d):
    """Reflect roughly 2023-2025 diesel price swings, $3.80-$4.50, with seasonal wobble."""
    days_in = (d - START_DATE).days
    # slow drift + seasonal sine wobble + noise
    base = 4.05 + 0.20 * ((days_in % 365) / 365 - 0.5)
    seasonal = 0.12 * random.uniform(-1, 1)
    noise = random.uniform(-0.08, 0.08)
    price = base + seasonal + noise
    return round(max(3.75, min(4.55, price)), 3)


def random_time_on(d, hour_start=5, hour_end=9):
    hour = random.randint(hour_start, hour_end)
    minute = random.choice([0, 5, 10, 15, 20, 30, 40, 45, 50])
    return datetime.datetime(d.year, d.month, d.day, hour, minute)


# ---------------------------------------------------------------------------
# Generate loads / trips / fuel / delivery events / maintenance
# ---------------------------------------------------------------------------

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

# Each truck runs roughly 2-3 round trips per week (season-adjusted: heavier Apr-Oct)
# Alternate southbound loaded run + northbound backhaul run per round trip.

odometer_state = {"TRK-01": 500000, "TRK-02": 180000}  # starting odometer 2 yrs ago
last_maint_odo = {"TRK-01": 500000, "TRK-02": 180000}

current_date = START_DATE

# We'll iterate week by week, scheduling trips for each truck.
week_start = START_DATE
while week_start <= TODAY:
    month = week_start.month
    in_season = month in (4, 5, 6, 7, 8, 9, 10)
    trips_this_week_per_truck = random.choice([2, 3]) if in_season else random.choice([1, 2])

    for truck in TRUCKS:
        truck_id = truck["truck_id"]
        driver_id = TRUCK_DRIVER[truck_id]
        is_old_truck = (truck_id == "TRK-01")

        for _ in range(trips_this_week_per_truck):
            day_offset = random.randint(0, 6)
            trip_date = week_start + datetime.timedelta(days=day_offset)
            if trip_date > TODAY:
                continue

            # ---- Southbound loaded leg ----
            route = random.choice(SOUTHBOUND_ROUTES)
            customer_id = route["customer_id"]
            distance = route["distance_miles"]
            freight_industry = next(c["industry"] for c in CUSTOMERS if c["customer_id"] == customer_id)
            freight_type = FREIGHT_TYPES[freight_industry]

            base_rate = route["base_rate_per_mile"] * random.uniform(0.96, 1.05)
            revenue = round(distance * base_rate, 2)
            fuel_surcharge = round(distance * random.uniform(0.15, 0.30), 2)
            weight = random.randint(38000, 44500)

            load_id = f"LOAD-{load_counter:05d}"
            load_counter += 1
            loads.append({
                "load_id": load_id,
                "customer_id": customer_id,
                "route_id": route["route_id"],
                "load_date": trip_date.isoformat(),
                "freight_type": freight_type,
                "weight_lbs": weight,
                "revenue": revenue,
                "fuel_surcharge": fuel_surcharge,
                "load_status": "delivered",
            })

            # Trip
            actual_miles = distance + random.randint(-8, 25)
            if is_old_truck:
                mpg = round(random.uniform(4.95, 5.45), 2)
            else:
                mpg = round(random.uniform(6.75, 7.35), 2)
            gallons = round(actual_miles / mpg, 2)

            dep_dt = random_time_on(trip_date, 4, 7)
            travel_hours = actual_miles / random.uniform(48, 54)
            arr_dt = dep_dt + datetime.timedelta(hours=travel_hours)
            on_time = random.random() < (0.88 if not is_old_truck else 0.82)

            trip_id = f"TRIP-{trip_counter:06d}"
            trip_counter += 1
            trips.append({
                "trip_id": trip_id,
                "load_id": load_id,
                "driver_id": driver_id,
                "truck_id": truck_id,
                "actual_miles": actual_miles,
                "fuel_gallons": gallons,
                "actual_mpg": mpg,
                "departure_time": dep_dt.isoformat(sep=" "),
                "arrival_time": arr_dt.isoformat(sep=" "),
                "on_time_flag": "Y" if on_time else "N",
            })

            odometer_state[truck_id] += actual_miles

            # Fuel purchase(s) for this trip (1-2 stops)
            n_stops = 1 if actual_miles < 400 else random.choice([1, 2])
            gallons_remaining = gallons
            for stop_i in range(n_stops):
                stop_gallons = round(gallons_remaining / (n_stops - stop_i), 2) if stop_i < n_stops - 1 else round(gallons_remaining, 2)
                gallons_remaining -= stop_gallons
                price = diesel_price_for_date(trip_date + datetime.timedelta(hours=stop_i * 5))
                total_cost = round(stop_gallons * price, 2)
                station = random.choice(DIESEL_STATIONS)
                fuel_purchases.append({
                    "purchase_id": f"FUEL-{fuel_counter:06d}",
                    "trip_id": trip_id,
                    "truck_id": truck_id,
                    "driver_id": driver_id,
                    "purchase_date": trip_date.isoformat(),
                    "gallons": stop_gallons,
                    "price_per_gallon": price,
                    "total_cost": total_cost,
                    "location": f"{station[0]}, {station[1]}",
                })
                fuel_counter += 1

            # Delivery event (destination facility)
            is_golden_gate = (customer_id == "CUST-04")
            scheduled_time = arr_dt.replace(minute=0) + datetime.timedelta(hours=1)
            if is_golden_gate:
                detention = max(5, int(random.gauss(47, 12)))
            else:
                detention = max(0, int(random.gauss(10, 5)))
            actual_delivery_time = arr_dt + datetime.timedelta(minutes=random.randint(-10, 20) + detention)
            evt_on_time = detention <= 20 and random.random() < 0.9

            delivery_events.append({
                "event_id": f"EVT-{event_counter:06d}",
                "load_id": load_id,
                "trip_id": trip_id,
                "facility_type": "receiver",
                "scheduled_time": scheduled_time.isoformat(sep=" "),
                "actual_time": actual_delivery_time.isoformat(sep=" "),
                "detention_minutes": detention,
                "on_time": "Y" if evt_on_time else "N",
            })
            event_counter += 1

            # ---- Northbound backhaul leg (usually a day or two later) ----
            if random.random() < 0.85:  # most southbound runs get some backhaul
                back_route = random.choice(NORTHBOUND_ROUTES)
                back_distance = back_route["distance_miles"]
                back_customer = random.choice(BACKHAUL_CUSTOMERS)["customer_id"]
                back_rate = back_route["base_rate_per_mile"] * random.uniform(0.85, 1.10)
                back_revenue = round(back_distance * back_rate, 2)
                back_fsc = round(back_distance * random.uniform(0.10, 0.20), 2)
                back_weight = random.randint(15000, 30000)

                back_load_date = trip_date + datetime.timedelta(days=random.choice([1, 2]))
                if back_load_date > TODAY:
                    back_load_date = TODAY

                back_load_id = f"LOAD-{load_counter:05d}"
                load_counter += 1
                loads.append({
                    "load_id": back_load_id,
                    "customer_id": back_customer,
                    "route_id": back_route["route_id"],
                    "load_date": back_load_date.isoformat(),
                    "freight_type": "Refrigerated - Backhaul Mixed",
                    "weight_lbs": back_weight,
                    "revenue": back_revenue,
                    "fuel_surcharge": back_fsc,
                    "load_status": "delivered",
                })

                back_actual_miles = back_distance + random.randint(0, 40)  # extra deadhead repositioning
                if is_old_truck:
                    back_mpg = round(random.uniform(4.9, 5.4), 2)
                else:
                    back_mpg = round(random.uniform(6.7, 7.3), 2)
                back_gallons = round(back_actual_miles / back_mpg, 2)

                back_dep_dt = random_time_on(back_load_date, 5, 8)
                back_travel_hours = back_actual_miles / random.uniform(46, 52)
                back_arr_dt = back_dep_dt + datetime.timedelta(hours=back_travel_hours)
                back_on_time = random.random() < (0.85 if not is_old_truck else 0.78)

                back_trip_id = f"TRIP-{trip_counter:06d}"
                trip_counter += 1
                trips.append({
                    "trip_id": back_trip_id,
                    "load_id": back_load_id,
                    "driver_id": driver_id,
                    "truck_id": truck_id,
                    "actual_miles": back_actual_miles,
                    "fuel_gallons": back_gallons,
                    "actual_mpg": back_mpg,
                    "departure_time": back_dep_dt.isoformat(sep=" "),
                    "arrival_time": back_arr_dt.isoformat(sep=" "),
                    "on_time_flag": "Y" if back_on_time else "N",
                })

                odometer_state[truck_id] += back_actual_miles

                back_price = diesel_price_for_date(back_load_date)
                back_total_cost = round(back_gallons * back_price, 2)
                back_station = random.choice(DIESEL_STATIONS)
                fuel_purchases.append({
                    "purchase_id": f"FUEL-{fuel_counter:06d}",
                    "trip_id": back_trip_id,
                    "truck_id": truck_id,
                    "driver_id": driver_id,
                    "purchase_date": back_load_date.isoformat(),
                    "gallons": back_gallons,
                    "price_per_gallon": back_price,
                    "total_cost": back_total_cost,
                    "location": f"{back_station[0]}, {back_station[1]}",
                })
                fuel_counter += 1

                back_scheduled = back_arr_dt.replace(minute=0) + datetime.timedelta(hours=1)
                back_detention = max(0, int(random.gauss(9, 4)))
                back_actual_delivery = back_arr_dt + datetime.timedelta(minutes=random.randint(-10, 15) + back_detention)
                back_evt_on_time = back_detention <= 20 and random.random() < 0.88

                delivery_events.append({
                    "event_id": f"EVT-{event_counter:06d}",
                    "load_id": back_load_id,
                    "trip_id": back_trip_id,
                    "facility_type": "receiver",
                    "scheduled_time": back_scheduled.isoformat(sep=" "),
                    "actual_time": back_actual_delivery.isoformat(sep=" "),
                    "detention_minutes": back_detention,
                    "on_time": "Y" if back_evt_on_time else "N",
                })
                event_counter += 1

        # Maintenance: roughly every 18,000-25,000 miles, more frequent/costly for old truck
        interval = 20000 if not is_old_truck else 16000
        if odometer_state[truck_id] - last_maint_odo[truck_id] >= interval and random.random() < 0.35:
            svc_date = week_start + datetime.timedelta(days=random.randint(0, 6))
            if svc_date <= TODAY:
                miles_since_start = odometer_state[truck_id] - (500000 if is_old_truck else 180000)
                pct_through = miles_since_start / 250000  # rough proxy for "months elapsed"
                service_type = random.choice([
                    "Oil & Filter Change", "Brake Service", "Tire Replacement",
                    "Reefer Unit Service", "DPF/Regen Service", "Transmission Service",
                    "Air System Repair", "Alternator Replacement",
                ])
                base_cost = random.uniform(400, 1800)
                base_downtime = random.uniform(3, 14)
                if is_old_truck:
                    # rising cost/downtime trend as truck crosses 600k miles (last ~6 months of data)
                    days_from_today = (TODAY - svc_date).days
                    if days_from_today <= 180 and odometer_state[truck_id] >= 600000:
                        base_cost *= random.uniform(1.6, 2.4)
                        base_downtime *= random.uniform(1.7, 2.6)
                    else:
                        base_cost *= random.uniform(1.15, 1.4)
                        base_downtime *= random.uniform(1.2, 1.5)
                maintenance_records.append({
                    "record_id": f"MAINT-{maint_counter:05d}",
                    "truck_id": truck_id,
                    "service_date": svc_date.isoformat(),
                    "service_type": service_type,
                    "cost": round(base_cost, 2),
                    "downtime_hours": round(base_downtime, 1),
                    "odometer_at_service": odometer_state[truck_id],
                })
                maint_counter += 1
                last_maint_odo[truck_id] = odometer_state[truck_id]

    week_start += datetime.timedelta(days=7)

# Update truck current_odometer to final state
for truck in TRUCKS:
    truck["current_odometer"] = odometer_state[truck["truck_id"]]

# ---------------------------------------------------------------------------
# Write CSVs
# ---------------------------------------------------------------------------

def write_csv(filename, fieldnames, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {len(rows):>6} rows -> {filename}")


write_csv("drivers.csv",
    ["driver_id", "first_name", "last_name", "hire_date", "employment_status",
     "cdl_class", "years_experience", "home_terminal"],
    DRIVERS)

write_csv("trucks.csv",
    ["truck_id", "make", "model", "year", "status", "acquisition_date",
     "current_odometer", "fuel_type"],
    TRUCKS)

write_csv("customers.csv",
    ["customer_id", "customer_name", "city", "state", "industry",
     "payment_terms_days", "account_status"],
    ALL_CUSTOMERS)

write_csv("routes.csv",
    ["route_id", "origin_city", "origin_state", "destination_city",
     "destination_state", "distance_miles", "base_rate_per_mile"],
    [{k: r[k] for k in ["route_id", "origin_city", "origin_state",
                         "destination_city", "destination_state",
                         "distance_miles", "base_rate_per_mile"]} for r in ROUTES])

write_csv("loads.csv",
    ["load_id", "customer_id", "route_id", "load_date", "freight_type",
     "weight_lbs", "revenue", "fuel_surcharge", "load_status"],
    loads)

write_csv("trips.csv",
    ["trip_id", "load_id", "driver_id", "truck_id", "actual_miles",
     "fuel_gallons", "actual_mpg", "departure_time", "arrival_time", "on_time_flag"],
    trips)

write_csv("fuel_purchases.csv",
    ["purchase_id", "trip_id", "truck_id", "driver_id", "purchase_date",
     "gallons", "price_per_gallon", "total_cost", "location"],
    fuel_purchases)

write_csv("delivery_events.csv",
    ["event_id", "load_id", "trip_id", "facility_type", "scheduled_time",
     "actual_time", "detention_minutes", "on_time"],
    delivery_events)

write_csv("maintenance_records.csv",
    ["record_id", "truck_id", "service_date", "service_type", "cost",
     "downtime_hours", "odometer_at_service"],
    maintenance_records)

print("\nDone.")
print(f"Loads: {len(loads)}, Trips: {len(trips)}, Fuel purchases: {len(fuel_purchases)}, "
      f"Delivery events: {len(delivery_events)}, Maintenance records: {len(maintenance_records)}")
