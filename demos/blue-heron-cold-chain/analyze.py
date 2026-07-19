import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

out = []
def log(*args):
    s = ' '.join(str(a) for a in args)
    print(s)
    out.append(s)

# ---------- LOAD ----------
customers = pd.read_csv('data/customers.csv')
events = pd.read_csv('data/delivery_events.csv', parse_dates=['scheduled_time', 'actual_time'])
drivers = pd.read_csv('data/drivers.csv', parse_dates=['hire_date'])
fuel = pd.read_csv('data/fuel_purchases.csv', parse_dates=['purchase_date'])
loads = pd.read_csv('data/loads.csv', parse_dates=['load_date'])
maint = pd.read_csv('data/maintenance_records.csv', parse_dates=['service_date'])
routes = pd.read_csv('data/routes.csv')
trips = pd.read_csv('data/trips.csv', parse_dates=['departure_time', 'arrival_time'])
trucks = pd.read_csv('data/trucks.csv', parse_dates=['acquisition_date'])

log("="*80)
log("DESCRIBE: loads")
log(loads.describe(include='all'))
log("="*80)
log("DESCRIBE: trips")
log(trips.describe(include='all'))
log("="*80)
log("DESCRIBE: fuel")
log(fuel.describe(include='all'))
log("="*80)
log("DESCRIBE: maintenance")
log(maint.describe(include='all'))
log("="*80)
log("DESCRIBE: delivery_events")
log(events.describe(include='all'))

# ---------- BUILD MASTER JOIN ----------
# loads + routes + trips + fuel(aggregated per trip)
loads_r = loads.merge(routes, on='route_id', how='left')
loads_r = loads_r.merge(customers, on='customer_id', how='left')

fuel_per_trip = fuel.groupby('trip_id').agg(
    fuel_cost=('total_cost', 'sum'),
    fuel_gallons_purchased=('gallons', 'sum'),
    avg_price_per_gal=('price_per_gallon', 'mean')
).reset_index()

master = trips.merge(loads_r, on='load_id', how='left')
master = master.merge(fuel_per_trip, on='trip_id', how='left')

master['month'] = master['load_date'].dt.to_period('M').astype(str)
master['total_revenue'] = master['revenue'] + master['fuel_surcharge']
master['rev_per_mile'] = master['total_revenue'] / master['actual_miles']
master['net_margin'] = master['total_revenue'] - master['fuel_cost']
master['net_margin_per_mile'] = master['net_margin'] / master['actual_miles']
master['direction'] = np.where(master['origin_state'] == 'WA', 'southbound', 'northbound_backhaul')

master.to_csv('analysis_output/master_trips.csv', index=False)

log("="*80)
log("MASTER TABLE SAMPLE")
log(master[['trip_id','truck_id','driver_id','customer_name','route_id','actual_miles',
            'actual_mpg','total_revenue','fuel_cost','net_margin','rev_per_mile',
            'net_margin_per_mile','direction']].head(10))

# ============================================================
# REVENUE & PROFITABILITY
# ============================================================
log("\n" + "="*80)
log("REVENUE PER MILE BY ROUTE")
by_route = master.groupby(['route_id','origin_city','destination_city']).agg(
    trips=('trip_id','count'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    avg_net_margin_per_mile=('net_margin_per_mile','mean'),
    total_revenue=('total_revenue','sum'),
    total_net_margin=('net_margin','sum'),
).sort_values('avg_net_margin_per_mile')
log(by_route)

log("\n" + "="*80)
log("PROFITABILITY BY DIRECTION (southbound vs northbound backhaul)")
by_dir = master.groupby('direction').agg(
    trips=('trip_id','count'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    avg_net_margin_per_mile=('net_margin_per_mile','mean'),
    total_revenue=('total_revenue','sum'),
    total_net_margin=('net_margin','sum'),
    avg_miles=('actual_miles','mean'),
)
log(by_dir)

log("\n" + "="*80)
log("NORTHBOUND BACKHAUL: % of trips below $1.65/mile breakeven-ish net margin")
nb = master[master['direction']=='northbound_backhaul']
log("Northbound trip count:", len(nb))
for thresh in [1.10, 1.65]:
    pct = (nb['rev_per_mile'] < thresh).mean()*100
    log(f"  % northbound trips with rev_per_mile < ${thresh}: {pct:.1f}%")
log("Northbound avg net_margin_per_mile:", nb['net_margin_per_mile'].mean())
log("Northbound avg rev_per_mile:", nb['rev_per_mile'].mean())

log("\n" + "="*80)
log("REVENUE & MARGIN BY CUSTOMER")
by_cust = master.groupby('customer_name').agg(
    loads=('load_id','count'),
    total_revenue=('total_revenue','sum'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    total_net_margin=('net_margin','sum'),
    avg_net_margin_per_mile=('net_margin_per_mile','mean'),
).sort_values('total_revenue', ascending=False)
log(by_cust)
log("\nCustomer revenue concentration (% of total revenue):")
log((by_cust['total_revenue'] / by_cust['total_revenue'].sum() * 100).round(1))

log("\n" + "="*80)
log("MONTHLY LOAD VOLUME & REVENUE TREND")
monthly = master.groupby('month').agg(
    loads=('load_id','count'),
    total_revenue=('total_revenue','sum'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    total_net_margin=('net_margin','sum'),
).sort_index()
log(monthly)

# ============================================================
# OPERATIONAL EFFICIENCY
# ============================================================
log("\n" + "="*80)
log("FUEL EFFICIENCY (MPG) BY TRUCK")
by_truck_mpg = master.groupby('truck_id').agg(
    trips=('trip_id','count'),
    avg_mpg=('actual_mpg','mean'),
    min_mpg=('actual_mpg','min'),
    max_mpg=('actual_mpg','max'),
    std_mpg=('actual_mpg','std'),
)
log(by_truck_mpg)

log("\n" + "="*80)
log("FUEL EFFICIENCY (MPG) BY DRIVER")
by_driver_mpg = master.groupby('driver_id').agg(
    trips=('trip_id','count'),
    avg_mpg=('actual_mpg','mean'),
    min_mpg=('actual_mpg','min'),
    max_mpg=('actual_mpg','max'),
)
log(by_driver_mpg)

log("\n" + "="*80)
log("FUEL COST PER LOADED MILE BY TRUCK")
master['fuel_cost_per_mile'] = master['fuel_cost'] / master['actual_miles']
by_truck_fuelcost = master.groupby('truck_id').agg(
    avg_fuel_cost_per_mile=('fuel_cost_per_mile','mean'),
    total_fuel_cost=('fuel_cost','sum'),
    total_miles=('actual_miles','sum'),
)
log(by_truck_fuelcost)

log("\n" + "="*80)
log("ESTIMATED EXTRA FUEL COST PER ROUND TRIP: TRK-01 vs TRK-02 (matched lanes)")
# Compare southbound trips only (loaded, comparable lanes)
sb = master[master['direction']=='southbound']
mpg_by_truck = sb.groupby('truck_id')['actual_mpg'].mean()
log(mpg_by_truck)
avg_price = fuel['price_per_gallon'].mean()
log("Avg diesel price/gal across dataset:", round(avg_price,3))
avg_miles = sb.groupby('truck_id')['actual_miles'].mean()
log(avg_miles)
for truck in ['TRK-01','TRK-02']:
    gallons_needed = avg_miles[truck] / mpg_by_truck[truck]
    log(f"{truck}: avg southbound miles={avg_miles[truck]:.0f}, mpg={mpg_by_truck[truck]:.2f}, "
        f"est. gallons={gallons_needed:.1f}, est. fuel cost one-way=${gallons_needed*avg_price:.2f}")

log("\n" + "="*80)
log("ON-TIME DELIVERY RATE BY CUSTOMER")
ev_full = events.merge(loads[['load_id','customer_id']], on='load_id', how='left')
ev_full = ev_full.merge(customers[['customer_id','customer_name']], on='customer_id', how='left')
otd_cust = ev_full.groupby('customer_name').agg(
    events=('event_id','count'),
    on_time_rate=('on_time', lambda x: (x=='Y').mean()*100),
    avg_detention_min=('detention_minutes','mean'),
    max_detention_min=('detention_minutes','max'),
).sort_values('avg_detention_min', ascending=False)
log(otd_cust)

log("\n" + "="*80)
log("ON-TIME DELIVERY (trips.csv on_time_flag) BY DRIVER / TRUCK")
otd_driver = master.groupby('driver_id').agg(
    trips=('trip_id','count'),
    on_time_rate=('on_time_flag', lambda x: (x=='Y').mean()*100),
)
log(otd_driver)
otd_truck = master.groupby('truck_id').agg(
    trips=('trip_id','count'),
    on_time_rate=('on_time_flag', lambda x: (x=='Y').mean()*100),
)
log(otd_truck)

log("\n" + "="*80)
log("ON-TIME PERFORMANCE TREND OVER TIME (monthly)")
otd_month = master.groupby('month').agg(
    trips=('trip_id','count'),
    on_time_rate=('on_time_flag', lambda x: (x=='Y').mean()*100),
)
log(otd_month)

log("\n" + "="*80)
log("DETENTION MINUTES BY FACILITY TYPE")
log(events.groupby('facility_type')['detention_minutes'].agg(['count','mean','max']))

log("\n" + "="*80)
log("TOTAL DETENTION HOURS & IMPLIED COST BY CUSTOMER (Golden Gate spotlight)")
otd_cust['total_detention_hours'] = (otd_cust['avg_detention_min'] * otd_cust['events']) / 60
log(otd_cust[['events','avg_detention_min','total_detention_hours']])
# Estimate value of driver time ~ $35/hr fully loaded cost of ownership (rough operating cost/hr estimate)
hourly_cost_estimate = 65  # truck+driver opportunity cost per hour, reefer owner-op typical all-in
otd_cust['est_detention_cost'] = otd_cust['total_detention_hours'] * hourly_cost_estimate
log(otd_cust[['total_detention_hours','est_detention_cost']].sort_values('est_detention_cost', ascending=False))

# ============================================================
# EQUIPMENT / MAINTENANCE
# ============================================================
log("\n" + "="*80)
log("MAINTENANCE RECORDS - ALL")
log(maint.sort_values(['truck_id','service_date']))

log("\n" + "="*80)
log("MAINTENANCE COST & DOWNTIME SUMMARY BY TRUCK")
maint_summary = maint.groupby('truck_id').agg(
    events=('record_id','count'),
    total_cost=('cost','sum'),
    avg_cost=('cost','mean'),
    total_downtime_hrs=('downtime_hours','sum'),
    avg_downtime_hrs=('downtime_hours','mean'),
)
log(maint_summary)

log("\n" + "="*80)
log("MAINTENANCE COST TREND OVER TIME BY TRUCK (chronological)")
maint['month'] = maint['service_date'].dt.to_period('M').astype(str)
for t in maint['truck_id'].unique():
    log(f"\n{t}:")
    log(maint[maint['truck_id']==t][['service_date','service_type','cost','downtime_hours','odometer_at_service']])

log("\n" + "="*80)
log("MAINTENANCE COST TREND - FIRST HALF VS SECOND HALF OF DATASET (by truck)")
maint_sorted = maint.sort_values('service_date')
for t in maint['truck_id'].unique():
    sub = maint_sorted[maint_sorted['truck_id']==t].reset_index(drop=True)
    mid = len(sub)//2
    first_half = sub.iloc[:mid]
    second_half = sub.iloc[mid:]
    log(f"{t}: first-half avg cost=${first_half['cost'].mean():.2f}, "
        f"second-half avg cost=${second_half['cost'].mean():.2f}, "
        f"first-half avg downtime={first_half['downtime_hours'].mean():.1f}hrs, "
        f"second-half avg downtime={second_half['downtime_hours'].mean():.1f}hrs")

log("\n" + "="*80)
log("MAINTENANCE COST PER MILE BY TRUCK (total maint cost / current odometer)")
maint_pm = maint.groupby('truck_id')['cost'].sum().reset_index()
maint_pm = maint_pm.merge(trucks[['truck_id','current_odometer','year']], on='truck_id')
maint_pm['cost_per_mile'] = maint_pm['cost'] / maint_pm['current_odometer']
log(maint_pm)

# ============================================================
# DRIVER SIGNALS
# ============================================================
log("\n" + "="*80)
log("DRIVER TENURE")
drivers['tenure_years'] = (pd.Timestamp('2026-07-02') - drivers['hire_date']).dt.days / 365.25
log(drivers[['driver_id','first_name','last_name','hire_date','years_experience','tenure_years']])

log("\n" + "="*80)
log("LOAD COUNT BY DRIVER")
log(master.groupby('driver_id')['trip_id'].count())

# ============================================================
# SEASONAL / TREND
# ============================================================
log("\n" + "="*80)
log("FUEL PRICE TREND OVER TIME (monthly avg $/gal)")
fuel['month'] = fuel['purchase_date'].dt.to_period('M').astype(str)
log(fuel.groupby('month')['price_per_gallon'].mean())

log("\n" + "="*80)
log("MONTHLY LOADS BY FREIGHT TYPE (seasonality check)")
loads['month'] = loads['load_date'].dt.to_period('M').astype(str)
log(loads.groupby(['month','freight_type'])['load_id'].count().unstack(fill_value=0))

log("\n" + "="*80)
log("DATE RANGE OF DATA")
log("Loads:", loads['load_date'].min(), "to", loads['load_date'].max())
log("Maintenance:", maint['service_date'].min(), "to", maint['service_date'].max())

# ============================================================
# CUSTOMER PAYMENT TERMS
# ============================================================
log("\n" + "="*80)
log("CUSTOMER PAYMENT TERMS & REVENUE EXPOSURE")
pay = customers.merge(by_cust.reset_index(), on='customer_name', how='left')
log(pay[['customer_name','payment_terms_days','total_revenue','loads']].sort_values('payment_terms_days', ascending=False))

with open('analysis_output/findings_log.txt', 'w') as f:
    f.write('\n'.join(out))

print("\n\nDONE. Full log written to analysis_output/findings_log.txt")
