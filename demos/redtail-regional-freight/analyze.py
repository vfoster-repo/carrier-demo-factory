import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

OUT = 'analysis_output'

customers = pd.read_csv('data/customers.csv')
delivery_events = pd.read_csv('data/delivery_events.csv', parse_dates=['scheduled_time', 'actual_time'])
drivers = pd.read_csv('data/drivers.csv', parse_dates=['hire_date'])
fuel = pd.read_csv('data/fuel_purchases.csv', parse_dates=['purchase_date'])
loads = pd.read_csv('data/loads.csv', parse_dates=['load_date'])
maint = pd.read_csv('data/maintenance_records.csv', parse_dates=['service_date'])
routes = pd.read_csv('data/routes.csv')
trips = pd.read_csv('data/trips.csv', parse_dates=['departure_time', 'arrival_time'])
trucks = pd.read_csv('data/trucks.csv', parse_dates=['acquisition_date'])

log = []
def p(*args):
    s = ' '.join(str(a) for a in args)
    print(s)
    log.append(s)

p("="*90)
p("REDTAIL REGIONAL FREIGHT — INDEPENDENT DATA ANALYSIS")
p("="*90)

# ---------------------------------------------------------------------------
p("\n\n### 1. FLEET FUEL EFFICIENCY (MPG) BY TRUCK ###")
mpg_by_truck = trips.groupby('truck_id')['actual_mpg'].agg(['mean','count','std']).reset_index()
mpg_by_truck = mpg_by_truck.merge(trucks[['truck_id','make','model','year','current_odometer','status']], on='truck_id')
mpg_by_truck = mpg_by_truck.sort_values('mean')
fleet_avg_mpg = trips['actual_mpg'].mean()
p(f"Fleet average MPG across all trips: {fleet_avg_mpg:.2f}")
p("\nWorst 5 trucks by average MPG:")
p(mpg_by_truck.head(5).to_string(index=False))
p("\nBest 5 trucks by average MPG:")
p(mpg_by_truck.tail(5).to_string(index=False))
mpg_by_truck.to_csv(f'{OUT}/mpg_by_truck.csv', index=False)

worst_truck = mpg_by_truck.iloc[0]
gap_pct = (fleet_avg_mpg - worst_truck['mean']) / fleet_avg_mpg * 100
p(f"\n>>> Worst truck: {worst_truck['truck_id']} ({worst_truck['year']:.0f} {worst_truck['make']} {worst_truck['model']}), "
  f"{worst_truck['mean']:.2f} MPG vs fleet avg {fleet_avg_mpg:.2f} MPG -> {gap_pct:.1f}% below fleet average, "
  f"odometer {worst_truck['current_odometer']:,.0f} mi, n={worst_truck['count']:.0f} trips")

# ---------------------------------------------------------------------------
p("\n\n### 2. FUEL EFFICIENCY BY DRIVER ###")
mpg_by_driver = trips.groupby('driver_id')['actual_mpg'].agg(['mean','count']).reset_index().sort_values('mean')
mpg_by_driver = mpg_by_driver[mpg_by_driver['count'] >= 20]
p("Worst 5 drivers by MPG (min 20 trips):")
p(mpg_by_driver.head(5).to_string(index=False))
p("\nBest 5 drivers by MPG (min 20 trips):")
p(mpg_by_driver.tail(5).to_string(index=False))
mpg_by_driver.to_csv(f'{OUT}/mpg_by_driver.csv', index=False)

# ---------------------------------------------------------------------------
p("\n\n### 3. MAINTENANCE COST & DOWNTIME BY TRUCK ###")
maint_by_truck = maint.groupby('truck_id').agg(
    total_cost=('cost','sum'), n_records=('cost','count'),
    total_downtime_hrs=('downtime_hours','sum'), avg_cost=('cost','mean')
).reset_index().merge(trucks[['truck_id','make','model','year','current_odometer']], on='truck_id')
maint_by_truck = maint_by_truck.sort_values('total_cost', ascending=False)
p(f"Fleet-wide avg maintenance cost per truck: ${maint.groupby('truck_id')['cost'].sum().mean():,.2f}")
p(f"Fleet-wide avg downtime hours per truck: {maint.groupby('truck_id')['downtime_hours'].sum().mean():,.1f}")
p("\nTop 5 trucks by total maintenance cost:")
p(maint_by_truck.head(5).to_string(index=False))
maint_by_truck.to_csv(f'{OUT}/maintenance_by_truck.csv', index=False)

# last 18 months maintenance concentration
cutoff = maint['service_date'].max() - pd.DateOffset(months=18)
recent_maint = maint[maint['service_date'] >= cutoff]
recent_by_truck = recent_maint.groupby('truck_id').agg(cost=('cost','sum'), downtime=('downtime_hours','sum'), n=('cost','count')).sort_values('cost', ascending=False)
p(f"\nMaintenance in last 18 months (since {cutoff.date()}), top 5 trucks:")
p(recent_by_truck.head(5).to_string())

# ---------------------------------------------------------------------------
p("\n\n### 4. REVENUE PER MILE / PROFITABILITY BY ROUTE ###")
loads_r = loads.merge(routes, on='route_id')
loads_r['rev_per_mile'] = (loads_r['revenue'] + loads_r['fuel_surcharge']) / loads_r['distance_miles']
route_summary = loads_r.groupby('route_id').agg(
    n_loads=('load_id','count'),
    avg_revenue=('revenue','mean'),
    avg_fsc=('fuel_surcharge','mean'),
    distance=('distance_miles','first'),
    base_rate=('base_rate_per_mile','first'),
    avg_rev_per_mile=('rev_per_mile','mean'),
    total_revenue=('revenue','sum'),
).reset_index().sort_values('avg_rev_per_mile')
p(route_summary.to_string(index=False))
route_summary.to_csv(f'{OUT}/route_summary.csv', index=False)

# Estimate fuel cost per route using trips+fuel joined to loads
trips_fuel = trips.merge(fuel.groupby('trip_id')['total_cost'].sum().reset_index(), on='trip_id', how='left')
trips_full = trips_fuel.merge(loads[['load_id','route_id','revenue','fuel_surcharge']], on='load_id', how='left')
trips_full = trips_full.merge(routes[['route_id','distance_miles','base_rate_per_mile']], on='route_id', how='left')

# detention per trip via delivery_events
det_by_trip = delivery_events.groupby('trip_id')['detention_minutes'].sum().reset_index()
trips_full = trips_full.merge(det_by_trip, on='trip_id', how='left')
trips_full['detention_minutes'] = trips_full['detention_minutes'].fillna(0)

trips_full['net_revenue'] = trips_full['revenue'].fillna(0) + trips_full['fuel_surcharge'].fillna(0) - trips_full['total_cost'].fillna(0)
trips_full['net_per_mile'] = trips_full['net_revenue'] / trips_full['actual_miles']

route_net = trips_full.groupby('route_id').agg(
    n=('trip_id','count'),
    avg_gross_rev_per_mile=('base_rate_per_mile','mean'),
    avg_fuel_cost=('total_cost','mean'),
    avg_net_revenue=('net_revenue','mean'),
    avg_net_per_mile=('net_per_mile','mean'),
    avg_detention_min=('detention_minutes','mean'),
    pct_loads_below_205=('net_per_mile', lambda s: (s < 2.05).mean()*100),
).reset_index().sort_values('avg_net_per_mile')
p("\nNet revenue per mile by route (revenue + FSC - fuel cost), vs $2.05/mi reference breakeven:")
p(route_net.to_string(index=False))
route_net.to_csv(f'{OUT}/route_net_profitability.csv', index=False)

# ---------------------------------------------------------------------------
p("\n\n### 5. REVENUE / PROFIT BY CUSTOMER ###")
cust_summary = loads.merge(customers, on='customer_id').groupby(['customer_id','customer_name']).agg(
    n_loads=('load_id','count'), total_revenue=('revenue','sum'), avg_revenue=('revenue','mean'),
    total_fsc=('fuel_surcharge','sum')
).reset_index().sort_values('total_revenue', ascending=False)
cust_summary['pct_of_revenue'] = cust_summary['total_revenue'] / cust_summary['total_revenue'].sum() * 100
p(cust_summary.to_string(index=False))
cust_summary.to_csv(f'{OUT}/customer_summary.csv', index=False)

# ---------------------------------------------------------------------------
p("\n\n### 6. DETENTION BY CUSTOMER ###")
loads_events = delivery_events.merge(loads[['load_id','customer_id']], on='load_id', how='left')
loads_events = loads_events.merge(customers[['customer_id','customer_name']], on='customer_id', how='left')
det_by_cust = loads_events.groupby(['customer_id','customer_name']).agg(
    avg_detention=('detention_minutes','mean'),
    total_detention_hrs=('detention_minutes', lambda s: s.sum()/60),
    n_events=('event_id','count'),
    pct_on_time=('on_time','mean'),
).reset_index().sort_values('avg_detention', ascending=False)
fleet_avg_det = delivery_events['detention_minutes'].mean()
p(f"Fleet-wide average detention per event: {fleet_avg_det:.1f} min")
p(det_by_cust.to_string(index=False))
det_by_cust.to_csv(f'{OUT}/detention_by_customer.csv', index=False)

# detention by facility type too
det_by_facility = delivery_events.groupby('facility_type')['detention_minutes'].mean()
p(f"\nDetention by facility type:\n{det_by_facility.to_string()}")

# ---------------------------------------------------------------------------
p("\n\n### 7. ON-TIME PERFORMANCE ###")
p(f"Fleet-wide on-time rate (trips): {trips['on_time_flag'].mean()*100:.1f}%")
otp_by_driver = trips.groupby('driver_id')['on_time_flag'].agg(['mean','count']).reset_index()
otp_by_driver = otp_by_driver[otp_by_driver['count']>=20].sort_values('mean')
p("\nWorst 5 drivers by on-time %:")
p(otp_by_driver.head(5).to_string(index=False))

otp_by_route = trips.merge(loads[['load_id','route_id']], on='load_id').groupby('route_id')['on_time_flag'].mean().sort_values()
p(f"\nOn-time % by route:\n{otp_by_route.to_string()}")

otp_by_cust = trips.merge(loads[['load_id','customer_id']], on='load_id').merge(customers[['customer_id','customer_name']], on='customer_id').groupby('customer_name')['on_time_flag'].mean().sort_values()
p(f"\nOn-time % by customer:\n{otp_by_cust.to_string()}")

# ---------------------------------------------------------------------------
p("\n\n### 8. DRIVER LOAD COUNT / UTILIZATION ###")
loads_by_driver = trips.groupby('driver_id')['trip_id'].count().sort_values()
p(f"Trip count by driver — min: {loads_by_driver.min()}, max: {loads_by_driver.max()}, mean: {loads_by_driver.mean():.1f}, median: {loads_by_driver.median():.1f}")
p("\nBottom 5 drivers by trip count (possibly underutilized or recently hired/terminated):")
p(loads_by_driver.head(5).to_string())

# ---------------------------------------------------------------------------
p("\n\n### 9. DRIVER TENURE / TURNOVER ###")
drivers['hire_date'] = pd.to_datetime(drivers['hire_date'])
today = pd.Timestamp('2026-07-02')
drivers['tenure_days'] = (today - drivers['hire_date']).dt.days
p(drivers['employment_status'].value_counts().to_string())

terminated = drivers[drivers['employment_status'].isin(['terminated','quit'])]
active = drivers[drivers['employment_status']=='active']
p(f"\nTerminated/quit drivers: {len(terminated)} of {len(drivers)} ({len(terminated)/len(drivers)*100:.1f}%)")
p(f"Avg tenure at hire for terminated (days): {terminated['tenure_days'].mean():.0f}" if len(terminated) else "")

# recent hires (last 18 months from max hire date observed)
recent_cutoff = drivers['hire_date'].max() - pd.DateOffset(months=18)
recent_hires = drivers[drivers['hire_date'] >= recent_cutoff]
p(f"\nDrivers hired since {recent_cutoff.date()} (last ~18 months): {len(recent_hires)}")
p(recent_hires['employment_status'].value_counts().to_string())
recent_term_rate = (recent_hires['employment_status'].isin(['terminated','quit'])).mean()*100
older_hires = drivers[drivers['hire_date'] < recent_cutoff]
older_term_rate = (older_hires['employment_status'].isin(['terminated','quit'])).mean()*100
p(f"Termination rate among recent hires: {recent_term_rate:.1f}% vs older hires: {older_term_rate:.1f}%")
drivers.to_csv(f'{OUT}/drivers_tenure.csv', index=False)

# ---------------------------------------------------------------------------
p("\n\n### 10. MONTHLY TRENDS — LOAD VOLUME, REVENUE, FUEL COST ###")
loads['month'] = loads['load_date'].dt.to_period('M')
monthly = loads.groupby('month').agg(n_loads=('load_id','count'), revenue=('revenue','sum')).reset_index()
p(monthly.to_string(index=False))
monthly.to_csv(f'{OUT}/monthly_trends.csv', index=False)

fuel['month'] = fuel['purchase_date'].dt.to_period('M')
fuel_monthly = fuel.groupby('month').agg(avg_price=('price_per_gallon','mean'), total_gallons=('gallons','sum'), total_cost=('total_cost','sum')).reset_index()
p("\nMonthly fuel price/cost trend:")
p(fuel_monthly.to_string(index=False))
fuel_monthly.to_csv(f'{OUT}/fuel_monthly_trends.csv', index=False)

trips['month'] = trips['departure_time'].dt.to_period('M')
otp_monthly = trips.groupby('month')['on_time_flag'].mean()
p("\nOn-time % trend by month:")
p(otp_monthly.to_string())

# ---------------------------------------------------------------------------
p("\n\n### 11. PAYMENT TERMS BY CUSTOMER ###")
p(customers[['customer_id','customer_name','payment_terms_days','account_status']].to_string(index=False))

# ---------------------------------------------------------------------------
p("\n\n### 12. TRUCK AGE VS MAINTENANCE COST PER MILE ###")
trucks['age'] = 2026 - trucks['year']
truck_maint_age = maint_by_truck.merge(trucks[['truck_id','age']], on='truck_id', suffixes=('','_y'))
truck_maint_age['cost_per_mile'] = truck_maint_age['total_cost'] / truck_maint_age['current_odometer']
p(truck_maint_age[['truck_id','make','model','year','age','current_odometer','total_cost','cost_per_mile','total_downtime_hrs']].sort_values('cost_per_mile', ascending=False).head(10).to_string(index=False))

# ---------------------------------------------------------------------------
p("\n\n### 13. LOAD/REVENUE CONCENTRATION — CUSTOMER RISK ###")
top_cust_share = cust_summary['pct_of_revenue'].head(4).sum()
p(f"Top 4 customers account for {top_cust_share:.1f}% of total revenue")

with open(f'{OUT}/analysis_log.txt', 'w') as f:
    f.write('\n'.join(log))

print("\n\nDone. Outputs written to analysis_output/")
