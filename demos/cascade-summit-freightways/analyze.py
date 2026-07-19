import pandas as pd
import numpy as np

pd.set_option('display.width', 160)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 60)

DATA = 'data/'
OUT = 'analysis_output/'

def section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)

# ---------- LOAD ALL ----------
customers = pd.read_csv(DATA + 'customers.csv')
drivers = pd.read_csv(DATA + 'drivers.csv', parse_dates=['hire_date'])
trucks = pd.read_csv(DATA + 'trucks.csv', parse_dates=['acquisition_date'])
routes = pd.read_csv(DATA + 'routes.csv')
loads = pd.read_csv(DATA + 'loads.csv', parse_dates=['load_date'])
trips = pd.read_csv(DATA + 'trips.csv', parse_dates=['departure_time', 'arrival_time'])
fuel = pd.read_csv(DATA + 'fuel_purchases.csv', parse_dates=['purchase_date'])
maint = pd.read_csv(DATA + 'maintenance_records.csv', parse_dates=['service_date'])
events = pd.read_csv(DATA + 'delivery_events.csv', parse_dates=['scheduled_time', 'actual_time'])

for name, df in [('customers', customers), ('drivers', drivers), ('trucks', trucks),
                  ('routes', routes), ('loads', loads), ('trips', trips),
                  ('fuel', fuel), ('maint', maint), ('events', events)]:
    section(f"SHAPE / DTYPES: {name}  {df.shape}")
    print(df.dtypes)
    print(df.head(10))
    print(df.describe(include='all').T)

# ============================================================
# BUILD MASTER TRIP TABLE
# ============================================================
section("BUILDING MASTER TABLE")

loads2 = loads.merge(routes, on='route_id', how='left')
loads2 = loads2.merge(customers, on='customer_id', how='left')

trip_full = trips.merge(loads2, on='load_id', how='left')
trip_full = trip_full.merge(drivers[['driver_id','first_name','last_name','hire_date','employment_status','home_terminal','years_experience']], on='driver_id', how='left')
trip_full = trip_full.merge(trucks[['truck_id','make','model','year','status','acquisition_date']], on='truck_id', how='left', suffixes=('','_truck'))

# fuel cost per trip
fuel_by_trip = fuel.groupby('trip_id').agg(fuel_cost=('total_cost','sum'), gallons=('gallons','sum')).reset_index()
trip_full = trip_full.merge(fuel_by_trip, on='trip_id', how='left')

trip_full['total_revenue'] = trip_full['revenue'] + trip_full['fuel_surcharge'].fillna(0)
trip_full['rev_per_mile'] = trip_full['total_revenue'] / trip_full['actual_miles']
trip_full['net_after_fuel'] = trip_full['total_revenue'] - trip_full['fuel_cost']
trip_full['net_per_mile'] = trip_full['net_after_fuel'] / trip_full['actual_miles']

print(trip_full.shape)
print(trip_full.columns.tolist())

# ============================================================
# REVENUE / PROFITABILITY BY LANE
# ============================================================
section("REVENUE & MARGIN BY LANE (route)")

lane = trip_full.groupby(['route_id','origin_city','origin_state','destination_city','destination_state','distance_miles','base_rate_per_mile']).agg(
    loads=('load_id','count'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    avg_net_per_mile=('net_per_mile','mean'),
    avg_fuel_cost=('fuel_cost','mean'),
    total_revenue=('total_revenue','sum'),
    on_time_rate=('on_time_flag','mean'),
).reset_index().sort_values('avg_net_per_mile')

print(lane.to_string())
lane.to_csv(OUT + 'lane_profitability.csv', index=False)

BREAKEVEN = 2.05
section(f"LANES BELOW BREAKEVEN (${BREAKEVEN}/mi net-after-fuel)")
below = lane[lane['avg_net_per_mile'] < BREAKEVEN]
print(below.to_string())

# ============================================================
# REVENUE BY CUSTOMER
# ============================================================
section("REVENUE / VOLUME BY CUSTOMER")

cust = trip_full.groupby(['customer_id','customer_name']).agg(
    loads=('load_id','count'),
    total_revenue=('total_revenue','sum'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    avg_net_per_mile=('net_per_mile','mean'),
    on_time_rate=('on_time_flag','mean'),
).reset_index().sort_values('total_revenue', ascending=False)
cust['pct_of_total_revenue'] = 100 * cust['total_revenue'] / cust['total_revenue'].sum()
print(cust.to_string())
cust.to_csv(OUT + 'customer_profitability.csv', index=False)

# ============================================================
# DETENTION BY CUSTOMER
# ============================================================
section("DETENTION MINUTES BY CUSTOMER")

events_loads = events.merge(loads[['load_id','customer_id']], on='load_id', how='left')
events_loads = events_loads.merge(customers[['customer_id','customer_name']], on='customer_id', how='left')

det_cust = events_loads.groupby(['customer_id','customer_name']).agg(
    events=('event_id','count'),
    avg_detention_min=('detention_minutes','mean'),
    median_detention_min=('detention_minutes','median'),
    pct_on_time=('on_time','mean'),
).reset_index().sort_values('avg_detention_min', ascending=False)
print(det_cust.to_string())
det_cust.to_csv(OUT + 'detention_by_customer.csv', index=False)

fleet_avg_detention = events_loads['detention_minutes'].mean()
print(f"\nFLEET AVERAGE DETENTION: {fleet_avg_detention:.1f} min")

# ============================================================
# MPG BY TRUCK
# ============================================================
section("MPG BY TRUCK")

truck_mpg = trip_full.groupby('truck_id').agg(
    trips=('trip_id','count'),
    avg_mpg=('actual_mpg','mean'),
    total_miles=('actual_miles','sum'),
    total_fuel_cost=('fuel_cost','sum'),
).reset_index().merge(trucks[['truck_id','make','model','year']], on='truck_id', how='left').sort_values('avg_mpg')

print(truck_mpg.to_string())
truck_mpg.to_csv(OUT + 'truck_mpg.csv', index=False)

fleet_avg_mpg = trip_full['actual_mpg'].mean()
print(f"\nFLEET AVERAGE MPG: {fleet_avg_mpg:.2f}")
print("\nWORST 10 TRUCKS BY MPG:")
print(truck_mpg.head(10).to_string())

# ============================================================
# MPG BY DRIVER
# ============================================================
section("MPG BY DRIVER")

driver_mpg = trip_full.groupby('driver_id').agg(
    trips=('trip_id','count'),
    avg_mpg=('actual_mpg','mean'),
    on_time_rate=('on_time_flag','mean'),
    total_miles=('actual_miles','sum'),
).reset_index().merge(drivers[['driver_id','first_name','last_name','home_terminal','hire_date','employment_status']], on='driver_id', how='left').sort_values('avg_mpg')

print(driver_mpg.head(15).to_string())
driver_mpg.to_csv(OUT + 'driver_mpg.csv', index=False)

# ============================================================
# ON-TIME PERFORMANCE
# ============================================================
section("ON-TIME RATE BY CUSTOMER / ROUTE / DRIVER")

print("By customer:")
print(cust[['customer_name','on_time_rate','loads']].sort_values('on_time_rate').to_string())

print("\nBy route:")
print(lane[['origin_city','destination_city','on_time_rate','loads']].sort_values('on_time_rate').to_string())

print("\nBy driver (worst 15):")
print(driver_mpg[['driver_id','first_name','last_name','on_time_rate','trips']].sort_values('on_time_rate').head(15).to_string())

# ============================================================
# MAINTENANCE BY TRUCK
# ============================================================
section("MAINTENANCE COST & DOWNTIME BY TRUCK")

maint_truck = maint.groupby('truck_id').agg(
    records=('record_id','count'),
    total_cost=('cost','sum'),
    total_downtime_hrs=('downtime_hours','sum'),
    avg_cost=('cost','mean'),
).reset_index().merge(trucks[['truck_id','make','model','year','current_odometer']], on='truck_id', how='left').sort_values('total_cost', ascending=False)

print(maint_truck.to_string())
maint_truck.to_csv(OUT + 'maintenance_by_truck.csv', index=False)

fleet_avg_maint_cost = maint_truck['total_cost'].mean()
fleet_avg_downtime = maint_truck['total_downtime_hrs'].mean()
print(f"\nFLEET AVG MAINT COST/TRUCK: ${fleet_avg_maint_cost:,.2f}")
print(f"FLEET AVG DOWNTIME HRS/TRUCK: {fleet_avg_downtime:.1f}")

# aging cohort TRK-041 - TRK-048
aging_cohort = [f"TRK-{i:03d}" for i in range(41,49)]
section("AGING COHORT TRK-041 to TRK-048 vs FLEET")
aging_data = maint_truck[maint_truck['truck_id'].isin(aging_cohort)]
rest_data = maint_truck[~maint_truck['truck_id'].isin(aging_cohort)]
print("Aging cohort:")
print(aging_data.to_string())
print(f"\nAging cohort avg cost: ${aging_data['total_cost'].mean():,.2f} | avg downtime: {aging_data['total_downtime_hrs'].mean():.1f} hrs")
print(f"Rest of fleet avg cost: ${rest_data['total_cost'].mean():,.2f} | avg downtime: {rest_data['total_downtime_hrs'].mean():.1f} hrs")

# cost per mile for maintenance by truck age
trucks['age'] = 2026 - trucks['year']
maint_age = maint_truck.merge(trucks[['truck_id','age']], on='truck_id', how='left')
truck_miles = trip_full.groupby('truck_id')['actual_miles'].sum().reset_index()
maint_age = maint_age.merge(truck_miles, on='truck_id', how='left')
maint_age['cost_per_mile'] = maint_age['total_cost'] / maint_age['actual_miles']
section("MAINTENANCE COST PER MILE BY TRUCK AGE")
age_group = maint_age.groupby('age').agg(trucks=('truck_id','count'), avg_cost_per_mile=('cost_per_mile','mean'), avg_total_cost=('total_cost','mean')).reset_index().sort_values('age')
print(age_group.to_string())

# ============================================================
# DRIVER TENURE / TURNOVER
# ============================================================
section("DRIVER TENURE / TURNOVER")

drivers['hire_year'] = drivers['hire_date'].dt.year
print(drivers.groupby(['home_terminal','hire_year','employment_status']).size().unstack(fill_value=0))

term_rate = drivers.groupby('home_terminal').apply(lambda d: (d['employment_status']!='active').mean()).reset_index(name='termination_rate')
print("\nTermination rate by terminal:")
print(term_rate)

chicago_2023 = drivers[(drivers['home_terminal'].str.contains('Chicago')) & (drivers['hire_year']==2023)]
spokane = drivers[drivers['home_terminal'].str.contains('Spokane')]
print(f"\nChicago 2023 hires: {len(chicago_2023)}, termination rate: {(chicago_2023['employment_status']!='active').mean():.1%}")
print(f"Spokane overall termination rate: {(spokane['employment_status']!='active').mean():.1%}")
print(f"Overall fleet termination rate: {(drivers['employment_status']!='active').mean():.1%}")

print("\nAll drivers by terminal and status:")
print(drivers.groupby(['home_terminal','employment_status']).size())

# ============================================================
# SEASONAL / TREND
# ============================================================
section("MONTHLY LOAD VOLUME & REVENUE TREND")

loads['month'] = loads['load_date'].dt.to_period('M')
monthly = loads.groupby('month').agg(loads=('load_id','count'), revenue=('revenue','sum')).reset_index()
print(monthly.to_string())
monthly.to_csv(OUT + 'monthly_trend.csv', index=False)

section("FUEL PRICE TREND OVER TIME")
fuel['month'] = fuel['purchase_date'].dt.to_period('M')
fuel_trend = fuel.groupby('month').agg(avg_price_per_gal=('price_per_gallon','mean'), total_spend=('total_cost','sum')).reset_index()
print(fuel_trend.to_string())

section("ON-TIME TREND OVER TIME")
trip_full['month'] = trip_full['departure_time'].dt.to_period('M')
ontime_trend = trip_full.groupby('month')['on_time_flag'].mean().reset_index()
print(ontime_trend.to_string())

# ============================================================
# CUSTOMER CONCENTRATION
# ============================================================
section("CUSTOMER CONCENTRATION RISK")
print(cust[['customer_name','loads','total_revenue','pct_of_total_revenue']].to_string())
top_customer_share = cust['pct_of_total_revenue'].max()
print(f"\nLargest customer share of revenue: {top_customer_share:.1f}%")

# payment terms
section("PAYMENT TERMS BY CUSTOMER")
print(customers[['customer_name','payment_terms_days']].sort_values('payment_terms_days', ascending=False))

print("\n\nANALYSIS COMPLETE")
