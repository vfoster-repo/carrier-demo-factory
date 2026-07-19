# Redtail Regional Freight — App Ideas

Generated: 2026-07-02
Analyst findings: One truck (TRK-014, a 2013 Freightliner Cascadia with 781,400 miles) is dragging fleet fuel efficiency down 27% and single-handedly accounts for roughly $89K of maintenance spend and 635 downtime hours in the last 18 months alone. Llano Estacado Foods generates 4.4x the fleet's average dock detention (46.6 min vs 10.6 min), burning nearly 7,000 driver-hours over the data period, while the Amarillo→Denver reefer lane and both backhaul lanes net well under a $2.05/mile break-even once fuel is deducted. On top of that, 58% of drivers hired in the last 18 months have already been terminated or quit, versus a 5% rate for tenured drivers — a churn problem concentrated almost entirely in new hires.

---

## Primary Pain Points Discovered

1. **TRK-014 fuel inefficiency:** Averages 5.04 MPG across 528 trips vs. a fleet average of 6.90 MPG — a 27% efficiency gap that is chronic, not occasional (std dev only 0.21, meaning it's *consistently* bad, every trip). At current diesel prices (~$4.20/gal fleet average), this truck burns roughly 35% more fuel per mile than the fleet norm.
2. **TRK-014 maintenance/downtime concentration:** $123,170 in total lifetime maintenance cost (vs. fleet average of $10,765/truck — over 11x), with $89,439 of that (73%) incurred in just the last 18 months across 17 service events. Total downtime: 1,097.9 hours lifetime, 634.5 hours (58%) in the last 18 months alone — roughly 26 lost operating days from one truck in a year and a half.
3. **Llano Estacado Foods (CUST-002) detention outlier:** Average detention of 46.6 minutes per delivery event across 8,950 events, vs. a fleet-wide average of 10.6 minutes for every other customer — a 4.4x gap that holds consistently, not as an occasional spike. That's 6,946 cumulative hours of driver/truck time tied up at one customer's dock, effectively unpaid idle time that displaces revenue-generating miles.
4. **Reefer and backhaul lanes are marginal-to-losing after fuel cost:** Once fuel is netted against revenue + fuel surcharge, AMA-DEN-REEFER nets $1.94/mile, DEN-AMA-BACKHAUL nets $1.74/mile, and AMA-OKC-BACKHAUL nets just $1.69/mile — all below the $2.05/mile reference break-even, despite reasonable posted base rates ($1.90–$2.15/mile). On AMA-DEN-REEFER specifically, 79.6% of individual loads fall below breakeven; on the two backhaul lanes, essentially every load (99.5%+) does.
5. **New-hire driver attrition:** Of 12 drivers hired in the last 18 months, 7 (58.3%) have already been terminated or quit — compared to a 5.0% termination rate among drivers hired earlier. This is a structural onboarding/retention problem concentrated at the front end of the employment lifecycle, not random attrition spread evenly across the workforce.

---

## App Ideas

### App 01: Truck Profitability & Retirement Scorecard

**Build ID:** app-01-truck-retirement-scorecard
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** trucks.csv, trips.csv, fuel_purchases.csv, maintenance_records.csv
**Additional data needed:** none (replacement truck financing quotes would sharpen the buy-vs-repair recommendation, but not required to build)

**Problem solved:**
Dale suspects one of his older trucks is a money pit but has never had the numbers laid out to prove it or size the problem. TRK-014, a 2013 Freightliner Cascadia with 781,400 miles, is quietly costing the business in two ways at once: it burns fuel at 5.04 MPG against a 6.90 MPG fleet average, and it has racked up $123,170 in lifetime maintenance with $89,439 of that (73%) in just the last 18 months. This app puts every truck on one ranked table so the worst offender is impossible to miss.

**What the app shows:**
- A ranked table of all 38 trucks with MPG, total maintenance cost, downtime hours, and an estimated "excess annual cost vs. fleet average" figure combining fuel and maintenance
- A scatter plot: MPG (x-axis) vs. total maintenance cost (y-axis), bubble size = downtime hours, so chronic problem trucks visually separate from the healthy fleet
- A trend line for TRK-014 (and any other flagged truck) showing maintenance cost by month over the full data period, to show whether the problem is worsening
- A "what retiring this truck would save" calculator: excess fuel cost/year + trailing-18-month maintenance run-rate, framed as an annualized dollar figure
- Truck age vs. cost-per-mile-driven scatter to show whether the age/mileage relationship is linear or whether TRK-014 is an outlier even for its age cohort

**Key metric / headline number:**
"TRK-014 costs an estimated $31,000+/year more than an average fleet truck in fuel and maintenance combined — enough to make payments on a replacement."

**Build specification:**
- Join trips.csv to trucks.csv on truck_id; compute per-truck avg MPG and trip count.
- Join fuel_purchases.csv by truck_id to get total fuel spend and gallons per truck; compute fleet avg $/mile fuel cost, then compute each truck's "excess fuel spend" as (fleet avg MPG − truck MPG) × truck's annual miles × avg diesel price.
- Aggregate maintenance_records.csv by truck_id for total cost, record count, downtime hours; also compute a trailing-18-month subset (service_date >= max date − 18mo) to show recency concentration.
- Main callout box at top: name TRK-014 explicitly with its MPG gap (27%), 18-month maintenance total ($89,439), and downtime hours (634.5), framed as "this truck needs a decision."
- Primary chart: MPG vs. maintenance cost scatter, all 38 trucks, with fleet-average crosshairs; label the clear outlier(s) directly on the chart rather than relying on a legend.
- Secondary chart: monthly maintenance cost trend line specifically for the top 1-2 flagged trucks, overlaid against fleet average trend, to visually show the divergence accelerating.
- Add a truck selector dropdown so Dale can pull up any truck's individual profile (MPG history, maintenance history table, downtime events) — not just the flagged ones, since he'll want to check others too.
- Layout: headline callout banner top, scatter plot + ranked table side by side in the middle, truck detail drill-down at the bottom.

**Success criteria:**
Dale should be able to open the app and, within 60 seconds, name the single worst truck in his fleet, know its dollar cost, and have a number he can bring to his banker to justify a replacement purchase.

---

### App 02: Customer Detention & Accessorial Cost Tracker

**Build ID:** app-02-customer-detention-tracker
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** delivery_events.csv, loads.csv, customers.csv
**Additional data needed:** Redtail's actual detention billing rate/policy (if one exists) to calculate exact chargeable amounts; currently the app can only show time lost, not dollars billed vs. dollars owed

**Problem solved:**
Detention time is currently invisible — buried inside "normal trip variance" — even though Llano Estacado Foods' Lubbock dock generates 46.6 minutes of average detention per delivery versus a 10.6-minute fleet average across every other customer. That gap has cost the fleet 6,946 hours cumulatively. Dale has no current way to see this pattern, let alone use it as leverage in a rate renegotiation or to bill accessorial charges.

**What the app shows:**
- A ranked bar chart of average detention minutes by customer, with Llano Estacado Foods visually flagged against the fleet-average reference line
- Cumulative detention hours per customer over the full data period, converted to an estimated dollar cost using a configurable driver-hour rate (default editable input, e.g., $35/hr all-in cost)
- A trend chart showing whether Llano Estacado's detention has been getting better, worse, or flat over time (by month)
- Breakdown of detention by facility type (shipper pickup vs. consignee delivery) so Dale knows whether the problem is loading or unloading
- A "load-level drill-down" table for Llano Estacado Foods listing every delivery event with detention minutes, sorted worst-first, for use in a renegotiation conversation

**Key metric / headline number:**
"Llano Estacado Foods detention has cost Redtail an estimated 6,946 driver-hours (~$243,000 at $35/hr) — 4.4x every other customer."

**Build specification:**
- Join delivery_events.csv to loads.csv on load_id to get customer_id, then to customers.csv for customer_name.
- Group by customer_id: mean detention_minutes, sum detention_minutes (converted to hours), count of events, % on_time.
- Compute fleet-wide average detention (excluding or including the flagged customer — show both so the "with vs without Llano" gap is explicit).
- Add an editable numeric input for "cost per driver-hour" so Dale can plug in his own number and watch the dollar-impact figure update live — this is the leverage number he'll use in a negotiation.
- Bar chart: avg detention minutes by customer, horizontal, sorted descending, with a dashed vertical line at the fleet average.
- Line chart: Llano Estacado's monthly average detention over time, to answer "is this getting worse."
- Bottom section: sortable/filterable data table of individual delivery events for the selected customer (dropdown, default Llano Estacado Foods) so specific dates/loads can be pulled for a conversation with the customer.
- Layout: headline callout, bar chart + dollar-impact calculator at top, trend chart middle, drill-down table bottom.

**Success criteria:**
Dale should be able to walk into a call with Llano Estacado Foods (or draft a rate amendment) with an exact, defensible detention-hours and dollar-cost figure pulled directly from the app, in under 60 seconds.

---

### App 03: Lane Profitability Analyzer

**Build ID:** app-03-lane-profitability-analyzer
**Audience:** owner
**Category:** calculator
**Priority:** HIGH
**Data required:** loads.csv, routes.csv, trips.csv, fuel_purchases.csv, delivery_events.csv
**Additional data needed:** driver pay/mile or per-load driver compensation data (not in current CSVs) would let the app show fully-loaded margin instead of margin after fuel only

**Problem solved:**
The Amarillo→Denver reefer lane looks fine on paper — a competitive $2.15/mile base rate — but nets only $1.94/mile after fuel cost, below the $2.05/mile reference breakeven, and 79.6% of individual loads on that lane fall under breakeven. The two backhaul lanes (AMA-OKC-BACKHAUL and DEN-AMA-BACKHAUL) are worse still, netting $1.69 and $1.74/mile with essentially every load underwater. Dale currently has no way to see this without hand-building a spreadsheet every quarter.

**What the app shows:**
- A ranked table of all 8 routes showing base rate/mile, net rate/mile after fuel, and % of loads falling below a configurable breakeven threshold (default $2.05/mile)
- A waterfall or bar breakdown for each route: base rate → + fuel surcharge → − fuel cost → = net rate/mile, so the "where did the margin go" story is visual, not just a number
- Route selector that reveals detention-adjusted net margin (net rate minus estimated cost of detention hours on that lane) since AMA-DEN-REEFER and LUB-ABQ-VAN both carry meaningfully elevated detention
- Monthly trend of net rate/mile per route, to catch lanes that are drifting toward unprofitability
- A clear "loser lanes" callout list: routes where more than 50% of loads fall below breakeven

**Key metric / headline number:**
"The Amarillo→Denver reefer lane nets $1.94/mile after fuel — 5% below breakeven — and 8 of every 10 loads on this lane lose money."

**Build specification:**
- Merge loads.csv → routes.csv on route_id for distance and base_rate_per_mile.
- Merge trips.csv → fuel_purchases.csv (grouped sum by trip_id) to get per-trip fuel cost; merge to loads via load_id.
- Merge delivery_events.csv (summed detention_minutes by trip_id) for the detention-adjustment view.
- Compute net_revenue = revenue + fuel_surcharge − fuel_cost; net_per_mile = net_revenue / distance_miles.
- Configurable breakeven threshold input (default 2.05) — recompute % of loads below threshold live as the user adjusts it, since this is a judgment call Dale may want to test.
- Primary visualization: horizontal bar chart of all 8 routes sorted by net $/mile, with breakeven threshold as a reference line, color-coded (e.g., muted red for below threshold, neutral for above — follow the dataviz skill's palette rules rather than raw red/green).
- Waterfall chart per selected route (dropdown) showing the bridge from base rate to net rate.
- Explicit callout text naming AMA-DEN-REEFER, AMA-OKC-BACKHAUL, and DEN-AMA-BACKHAUL as the three lanes below breakeven, with their exact net $/mile.
- Layout: headline + ranked bar chart top, waterfall drill-down middle, monthly trend bottom.

**Success criteria:**
Dale should be able to identify, within 60 seconds, exactly which lanes are losing money after true costs and see the size of the gap in cents-per-mile terms he can use when negotiating rates or deciding whether to keep bidding a lane.

---

### App 04: Driver Retention Early-Warning Dashboard

**Build ID:** app-04-driver-retention-dashboard
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** drivers.csv, trips.csv
**Additional data needed:** exit interview notes or termination reason codes, dispatcher assignment history, and onboarding/training completion records would let the app diagnose *why* new hires are leaving, not just confirm that they are

**Problem solved:**
Of the 12 drivers hired in the last 18 months, 7 (58.3%) have already been terminated or quit — an eleven-fold higher rate than the 5.0% termination rate among drivers hired earlier. Dale has no current lens on this; individual departures look like isolated HR events rather than a systemic pattern concentrated at the front end of tenure.

**What the app shows:**
- A cohort comparison: termination rate for drivers hired in the last 18 months vs. drivers hired earlier, shown as a simple side-by-side bar
- A tenure-at-departure histogram for terminated/quit drivers, showing how early most departures happen
- A roster table of the 12 recent hires with hire date, current status, tenure so far, CDL class, and years of prior experience — sorted to surface the terminated ones first
- A "years of experience vs. termination" scatter or grouped comparison, to test whether it's inexperienced drivers specifically who are churning, or whether it cuts across experience levels
- A simple headcount/active-driver trend line over time, since heavy new-hire churn eventually shows up as a fleet capacity risk if hiring can't keep pace

**Key metric / headline number:**
"58% of drivers hired in the last 18 months have already left — versus 5% for everyone else. This is Redtail's biggest hidden hiring cost."

**Build specification:**
- Compute tenure_days for every driver as (today, or termination-implied date if available, minus hire_date).
- Split into two cohorts by hire_date relative to (max hire_date − 18 months); compute termination/quit rate for each cohort.
- Bar chart: two bars, "hired last 18 months" vs. "hired earlier," each showing % terminated/quit, with driver counts labeled directly on the bars (n=12 vs n=40) since the small sample size matters for interpretation.
- Table: all drivers hired in the trailing 18-month window, columns = driver_id, name, hire_date, employment_status, years_experience, cdl_class; sort terminated/quit rows to the top with a clear status indicator.
- Histogram: tenure in days at departure, for all terminated/voluntary_quit drivers regardless of hire cohort, to show the typical "danger window" (e.g., most departures happen within X days).
- Do not fabricate a root cause (no dispatcher or route data links to termination in the current CSVs) — instead include an explicit note in the app that this view flags *where* the problem is concentrated, and that root-cause diagnosis needs onboarding/exit-interview data Redtail doesn't currently track digitally.
- Layout: headline callout, cohort comparison bar chart top, tenure histogram middle, recent-hires roster table bottom.

**Success criteria:**
Dale should be able to see, within 60 seconds, that new-hire attrition is a distinct and severe problem (not generic turnover), know roughly how many people and dollars are involved, and have the specific list of affected recent hires to review with his terminal manager.

---

### App 05: Weekly Dispatch Health Snapshot

**Build ID:** app-05-dispatch-health-snapshot
**Audience:** owner
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** loads.csv, trips.csv, fuel_purchases.csv, delivery_events.csv, maintenance_records.csv
**Additional data needed:** none for a backward-looking view; a live TMS/ELD feed would be needed to make this truly real-time rather than historical

**Problem solved:**
Dale runs the business from the dispatch desk on gut feel and a spreadsheet he rebuilds occasionally. There's no single weekly view that rolls up load volume, revenue, on-time performance, fuel cost, and maintenance spend so he can sanity-check "is this a normal week or not" without digging through five different files.

**What the app shows:**
- A top-row KPI strip: loads this week, revenue this week, on-time %, avg fuel price paid, active trucks in shop
- Week-over-week and vs.-trailing-13-week-average deltas for each KPI, so Dale can tell at a glance if something moved
- A small multiples view of the 4-5 key trends (loads/week, revenue/week, on-time %/week, fuel price/week) as sparkline-style charts
- An "attention needed" list auto-generated from thresholds: any truck currently in maintenance status, any customer with detention >2x fleet average this week, any route currently netting below breakeven
- A simple week selector to look back at any historical week in the dataset

**Key metric / headline number:**
"This week: {N} loads, ${revenue}, {OTP}% on-time — {N} items need attention."

**Build specification:**
- Aggregate loads.csv, trips.csv, delivery_events.csv, fuel_purchases.csv, and maintenance_records.csv all to weekly grain using their respective date columns.
- Compute trailing 13-week rolling averages for each core KPI to give delta context (this is a regional carrier with clear day-to-day noise, so week-over-week alone would be too jumpy).
- KPI tiles: use the dataviz skill's stat-tile pattern — headline number, small trend arrow/delta, sparkline beneath each tile.
- "Attention needed" panel: pull from the other four apps' logic in miniature — flag TRK-014-style outliers (maintenance status = shop, or trailing-4-week MPG >15% below fleet avg), flag any customer whose trailing-4-week avg detention exceeds 2x fleet average, flag any route whose trailing-4-week net $/mile is below the $2.05 threshold. Render as a short bulleted list, not a full sub-dashboard.
- Week selector (dropdown or date picker) defaulting to the most recent complete week in the data.
- Layout: KPI tile strip across the top, attention-needed list directly below (this is the highest-value real estate), trend sparklines/small multiples beneath that.

**Success criteria:**
Dale should be able to open the app on a Monday morning and know within 60 seconds whether last week was normal, and if not, exactly which truck, customer, or lane needs his attention first.

---

### App 06: Customer Profitability & Concentration Report

**Build ID:** app-06-customer-profitability-report
**Audience:** accountant
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** loads.csv, customers.csv, delivery_events.csv, fuel_purchases.csv, trips.csv

**Additional data needed:** accounts-receivable/actual payment date data would allow a true DSO (days sales outstanding) calculation; currently only contracted payment_terms_days is available, not actual payment behavior

**Problem solved:**
Sangre de Cristo Distribution alone accounts for 32.9% of total revenue, and the top 4 customers combine for 89.5% — a concentration risk that isn't quantified anywhere today. Meanwhile customers aren't equally profitable once detention and fuel costs are factored in: Llano Estacado Foods generates strong revenue but also the worst detention drag in the fleet, while Sangre de Cristo carries the longest payment terms (45 days) of any customer.

**What the app shows:**
- A revenue concentration chart (e.g., Pareto/treemap) showing each customer's share of total revenue, with the 89.5% top-4 concentration called out explicitly
- A customer profitability table combining revenue, fuel-adjusted net revenue, detention hours, and payment terms in one place — a true "which customers are actually good customers" view
- Payment terms comparison across customers (15/30/45 day terms) cross-referenced with load volume, to flag cash-flow exposure (High Plains Ag Cooperative and Caprock Grain Exchange get paid fastest at 15 days; Sangre de Cristo at 45 days ties up the most cash the longest)
- A "customer risk score" combining revenue share + payment terms length, to visualize which customers represent the largest combined revenue-concentration and cash-flow risk

**Key metric / headline number:**
"Top 4 customers = 89.5% of revenue. Sangre de Cristo Distribution alone = 32.9% of revenue on 45-day terms — the single largest concentration and cash-flow exposure in the business."

**Build specification:**
- Group loads.csv by customer_id, merge to customers.csv for name/terms/industry.
- Compute % of total revenue per customer; sort descending; compute cumulative % for a Pareto-style chart.
- Merge in detention (from delivery_events via loads) and fuel-adjusted net revenue (from trips/fuel, same method as App 03) per customer.
- Treemap or horizontal bar for revenue share, sized/colored by revenue, annotated with cumulative % line to show the 89.5%-in-top-4 concentration visually.
- Table columns: customer, revenue, % of total, payment terms (days), avg detention (min), fuel-adjusted net revenue, net margin estimate.
- Scatter or quadrant chart: x = payment terms days, y = % of revenue, to visually separate "big and slow to pay" (top-right, highest risk) from "small and fast to pay" (bottom-left, lowest risk) customers.
- Layout: headline concentration callout + Pareto chart top, full profitability table middle, payment-terms risk quadrant bottom.

**Success criteria:**
The accountant/owner should be able to state, in under 60 seconds, exactly how concentrated revenue is, which customer represents the biggest combined revenue and cash-flow risk, and which customers are quietly the most/least profitable once true costs are included.

---

### App 07: Driver Fuel & Efficiency Scorecard

**Build ID:** app-07-driver-efficiency-scorecard
**Audience:** driver
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** trips.csv, fuel_purchases.csv, drivers.csv

**Additional data needed:** idle-time/engine-hours data from ELD systems would sharpen this from "MPG only" to a full driving-behavior scorecard (harsh braking, idling, speeding)

**Problem solved:**
MPG varies meaningfully by driver (fleet range from ~6.85 to ~6.99 across drivers with 20+ trips) but no driver currently gets individual feedback on their fuel efficiency relative to peers. This app gives each driver a private, non-punitive view of their own performance so fuel efficiency becomes something they can see and improve, not just something dispatch grumbles about.

**What the app shows:**
- A driver selector (or login-style single-driver view) showing that driver's average MPG vs. the fleet average and vs. the top-quartile driver
- A monthly MPG trend for the selected driver, to show whether they're improving, flat, or declining
- Percentile ranking within the fleet ("you're in the top 40% of drivers for fuel efficiency")
- A simple, non-judgmental framing: estimated fuel dollars per year the driver could save by closing the gap to the fleet average (not to the top driver, to keep the target realistic)
- Trip-level detail table showing individual trips with MPG, so a driver can see which specific runs were efficient vs. not

**Key metric / headline number:**
"Your average: {X.XX} MPG. Fleet average: 6.90 MPG. You're in the {Nth} percentile."

**Build specification:**
- Group trips.csv by driver_id for avg MPG, trip count, and percentile rank against all drivers with sufficient trip volume (min ~20 trips to avoid noise).
- Compute fleet average and top-quartile average as reference lines.
- Driver selector dropdown (in a real deployment this would be a login; for the demo, a dropdown simulating "select your driver ID" is appropriate).
- Primary display: large headline number (driver's MPG) next to a simple horizontal gauge/bar showing their position between fleet-worst and fleet-best.
- Monthly trend line for the selected driver's MPG, with fleet average as a flat reference line for comparison.
- Framing must stay constructive per the app's audience (driver, not owner) — avoid "you are the worst driver" language; use neutral percentile/gap framing and a savings-oriented dollar estimate instead.
- Layout: headline gauge top, monthly trend middle, trip-level table bottom (collapsible/paginated given ~500+ trips per driver).

**Success criteria:**
A driver should be able to open the app, select their ID, and within 60 seconds know exactly how their fuel efficiency compares to the fleet and whether they're trending better or worse.

---

### App 08: Maintenance Cost Forecaster & Repair-vs-Replace Calculator

**Build ID:** app-08-maintenance-forecaster
**Audience:** fleet manager
**Category:** predictor
**Priority:** MEDIUM
**Data required:** maintenance_records.csv, trucks.csv

**Additional data needed:** new/replacement truck purchase price and financing terms would let the calculator output an actual "months to payback" figure instead of a relative cost comparison

**Problem solved:**
Maintenance cost isn't just about which truck has spent the most historically — it's about which trucks are trending toward becoming the next TRK-014. This app gives the fleet manager a forward-looking view, using service-type and cost trends per truck, to catch a problem truck 6-12 months before it becomes a $100K+ liability rather than discovering it after the fact.

**What the app shows:**
- A ranked list of all trucks by trailing-6-month maintenance cost trend (rate of increase, not just total), to catch trucks accelerating toward failure
- Cost-per-mile-driven by truck, adjusted for age, to separate "old but cheap to maintain" trucks from "old and expensive" ones
- A breakdown of maintenance spend by service_type (e.g., cooling system, brakes, tires) fleet-wide, to identify whether certain repair categories are disproportionately expensive or frequent
- A simple repair-vs-replace flag: trucks where trailing-12-month maintenance cost exceeds a configurable % of estimated truck value, suggesting replacement economics may beat continued repair
- Downtime hours by truck plotted against maintenance cost, to separate "expensive but reliable" from "expensive AND unreliable" trucks (the latter being the highest-priority replacement candidates)

**Key metric / headline number:**
"3 trucks are on a maintenance cost trajectory that will exceed $20,000/year if current trends continue — TRK-014 already has."

**Build specification:**
- Group maintenance_records.csv by truck_id and month; compute a rolling 6-month sum per truck to detect acceleration (compare most recent 6-month window to the prior 6-month window as a simple trend indicator).
- Merge to trucks.csv for age, odometer, make/model.
- Compute cost-per-mile-driven (total maintenance cost / current_odometer) per truck as an age-normalized comparison metric.
- Group by service_type fleet-wide for a bar chart of total cost and frequency per repair category (e.g., is cooling_system_repair disproportionately expensive fleet-wide, not just for TRK-014).
- Configurable "replacement trigger" threshold input (e.g., trailing-12-month maintenance cost as % of an assumed truck value, default $150K for a comparable used Class 8 tractor) — trucks exceeding it get flagged in a callout list.
- Scatter: downtime hours (x) vs. total maintenance cost (y) per truck, quadrant-labeled so "high cost + high downtime" trucks (top-right) are visually the priority replacement candidates.
- Layout: headline flagged-trucks callout top, trend-ranked table + service-type breakdown middle, downtime/cost scatter bottom.

**Success criteria:**
The fleet manager should be able to identify, within 60 seconds, which trucks (beyond the already-obvious TRK-014) are trending toward becoming expensive liabilities, and have a defensible threshold-based reason to prioritize them for repair budget or replacement planning.

---

### App 09: Load Acceptance Advisor (Dispatcher Tool)

**Build ID:** app-09-load-acceptance-advisor
**Audience:** dispatcher
**Category:** calculator
**Priority:** MEDIUM
**Data required:** routes.csv, loads.csv, trips.csv, fuel_purchases.csv, delivery_events.csv, customers.csv

**Additional data needed:** real-time fuel price feed and current truck/driver availability data would make this usable for live load acceptance decisions rather than historical reference only

**Problem solved:**
When a load comes in, the dispatcher currently has no quick way to check "is this actually a good load" beyond the quoted rate — they can't see at a glance that a load on AMA-OKC-BACKHAUL nets under $1.70/mile after fuel, or that a load for Llano Estacado Foods carries a near-certain 45+ minute detention tax that eats into the driver's productive time. This tool turns route/customer history into a quick green-light/yellow-light/red-light check before a load is accepted.

**What the app shows:**
- A route + customer selector that instantly surfaces historical net $/mile, average detention minutes, and on-time rate for that specific lane/customer combination
- A simple stoplight-style indicator (using accessible, non-red/green-only encoding per the dataviz skill) showing whether this lane+customer combination has historically been profitable
- A "what this load is really worth" calculator: input the quoted rate and miles, and see estimated net revenue after typical fuel cost and typical detention time for that customer/route
- A comparison against the fleet's $2.05/mile breakeven reference and against what other lanes are currently netting, so a marginal load can be weighed against opportunity cost
- Historical load count and volume trend for that lane/customer, so the dispatcher knows if it's a one-off or a repeat pattern worth optimizing around

**Key metric / headline number:**
"This lane + customer combination has historically netted ${X.XX}/mile after fuel and detention — {above/below} your $2.05 breakeven."

**Build specification:**
- Precompute historical net $/mile by route_id × customer_id combination (not just route alone), using the same fuel-cost-netting method as App 03, plus detention-minutes-as-cost overlay from delivery_events.
- Build a two-dropdown selector (route, customer) that filters to the matching historical combination and displays its stats; handle the case of route/customer combinations with few or no historical loads gracefully (show "insufficient history" rather than a misleading number).
- Input fields for quoted rate and miles on the prospective load; live-calculate estimated net $/mile using historical average fuel cost/mile and historical average detention cost for that combination, updating as the dispatcher types.
- Stoplight indicator: use shape/pattern plus color (not color alone) per accessibility guidance — e.g., a labeled badge "BELOW BREAKEVEN" in addition to color coding.
- Small supporting table: last 10 loads on this lane/customer combination with actual net $/mile, for the dispatcher to sanity-check the average against real examples.
- Layout: route/customer selector + live calculator at the very top (this is the primary interaction), stoplight verdict immediately beside it, supporting history table below.

**Success criteria:**
A dispatcher should be able to plug in a route, customer, and quoted rate, and within 60 seconds get a clear verdict on whether the load is likely to be profitable based on this company's actual historical performance on that lane/customer combination.

---

### App 10: Driver Earnings & Trip Statement Viewer

**Build ID:** app-10-driver-earnings-viewer
**Audience:** driver
**Category:** tracker
**Priority:** LOW
**Data required:** trips.csv, loads.csv, fuel_purchases.csv, drivers.csv

**Additional data needed:** actual driver pay structure (per-mile rate, percentage-of-load, or hourly) is not in the current data — this app currently can only show trip/mileage/fuel activity, not real earnings, without that input

**Problem solved:**
Drivers have no self-service way to see their own trip history, miles driven, and fuel efficiency in one place — they'd otherwise have to ask dispatch. Even without exact pay data, a trip-and-mileage log gives drivers transparency into their own activity and performance trends, which supports both trust and the fuel-efficiency coaching goal from App 07.

**What the app shows:**
- A personal trip log: date, route, miles, MPG, on-time flag, for the selected driver
- Monthly summary tiles: total miles driven, total trips, average MPG, on-time %
- A simple estimated-earnings calculator where the driver (or Redtail) can input a $/mile rate to see estimated gross pay by month, since actual pay data isn't available
- Trend charts for miles/month and on-time %/month, so drivers can see their own productivity over time

**Key metric / headline number:**
"{Driver Name}: {X} trips, {Y} miles, {Z}% on-time this month."

**Build specification:**
- Filter trips.csv (joined to loads.csv for route info) by selected driver_id.
- Group by month for miles, trip count, on-time %, avg MPG.
- Include a clearly-labeled "estimated earnings" section with an editable $/mile input defaulting to a placeholder rate, with an explicit disclaimer that this is an estimate since actual driver pay data isn't in the system — do not present it as authoritative pay.
- Simple line/bar charts for monthly miles and on-time % trends.
- Layout: driver selector + monthly summary tiles top, estimated earnings calculator middle, trip log table bottom.

**Success criteria:**
A driver should be able to select their ID and see, within 60 seconds, a clear picture of their own recent activity and performance trend without needing to call dispatch.

---

### App 11: Fuel Price & Spend Tracker

**Build ID:** app-11-fuel-price-tracker
**Audience:** accountant
**Category:** tracker
**Priority:** LOW
**Data required:** fuel_purchases.csv

**Additional data needed:** a fuel hedging/contract benchmark price, if Redtail uses one, to show actual spend against a contracted or budgeted rate rather than just market trend

**Problem solved:**
Fuel is the largest controllable variable cost in the business (roughly $110K-$124K/month across the data period) and prices have trended up over the data period (from ~$3.84/gal in late 2024 to $4.27+/gal by mid-2026), but there's no current view isolating fuel spend from everything else for budgeting purposes.

**What the app shows:**
- Monthly total fuel spend and average price/gallon trend over the full data period
- Fuel spend by purchase location, to identify if certain fueling stops are consistently more expensive
- Total gallons purchased by month, to separate price effects from volume effects
- A simple projection: if current price trend continues, estimated next-quarter fuel spend at current volume levels

**Key metric / headline number:**
"Fuel price is up {X}% since {start date} — current monthly spend run-rate: ${Y}."

**Build specification:**
- Group fuel_purchases.csv by month for total_cost, total gallons, and average price_per_gallon.
- Group by location for average price paid, to surface any consistently expensive fueling stops.
- Simple linear trend line fit on monthly average price to project forward one quarter, clearly labeled as a naive projection, not a forecast model.
- Layout: headline trend callout top, monthly price/spend dual-axis chart middle, location breakdown table bottom.

**Success criteria:**
The accountant should be able to see, within 60 seconds, the fuel spend trend and current run-rate for budgeting purposes.

---

### App 12: Fleet Utilization & Idle Capacity Report

**Build ID:** app-12-fleet-utilization-report
**Audience:** owner
**Category:** dashboard
**Priority:** LOW
**Data required:** trucks.csv, trips.csv, drivers.csv

**Additional data needed:** planned/scheduled load calendar data would let this show true idle time between assigned loads rather than just relative trip-count variation

**Problem solved:**
Trip counts vary across both trucks and drivers (drivers range from 515 to 604 trips over the data period), and some trucks carry a "shop"/"retired" status that removes capacity from the fleet. There's currently no single view of how much of the fleet's theoretical capacity is actually being used, which matters given that Dale is already looking at retiring TRK-014 and will want to know how much replacement capacity he actually needs.

**What the app shows:**
- Truck status breakdown (active / shop / retired) as a simple count and % of fleet
- Trip count distribution by truck and by driver, to identify meaningfully under- or over-utilized units
- A simple utilization index (trips relative to fleet median) to flag trucks/drivers well outside the normal range
- Fleet capacity trend: active truck count over time, to show whether capacity has been shrinking (e.g., due to trucks going into shop status)

**Key metric / headline number:**
"{X} of 38 trucks are currently active; fleet capacity utilization is {Y}% of theoretical maximum."

**Build specification:**
- Count trucks.csv by status (active/shop/retired).
- Group trips.csv by truck_id and driver_id for trip counts; compute median and flag units more than 1.5x IQR below median as underutilized.
- Simple bar charts for status breakdown and trip-count distribution (histogram).
- Layout: status summary tiles top, utilization distribution charts middle, flagged under/over-utilized unit list bottom.

**Success criteria:**
Dale should be able to see, within 60 seconds, how much of his fleet is actually working and whether any trucks or drivers are significantly under-utilized relative to peers.

---
