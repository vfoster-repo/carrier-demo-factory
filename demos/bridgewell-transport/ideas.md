# Bridgewell Transport — App Ideas

Generated: 2026-07-03
Analyst findings: Bridgewell's data shows a two-year-old blind spot Curtis has felt in his gut but never measured: the Joplin↔Little Rock lane nets barely $1.46-$1.50/mile after fuel against a ~$2.05/mile breakeven, a chronically underperforming truck (TRK-006) is quietly burning ~$1,287/month in excess fuel and leads the fleet in maintenance cost and downtime, and Ozark Building Supply — a top-5 customer — is racking up 37 extra minutes of detention per stop (295+ hours total, ~12/month) with a shockingly low 3.4% on-time rate. Layer on 21% driver turnover among recent hires and a slow-paying customer tying up roughly a month of revenue in receivables, and the picture is a business with decent top-line volume but real, fixable margin leakage.

---

## Primary Pain Points Discovered

1. **The Joplin↔Little Rock lane is structurally unprofitable.** Both directions (ROUTE-01, ROUTE-02) net only ~$1.46–$1.50/mile after fuel — the two worst lanes in the network — against Curtis's own ~$2.05/mile breakeven target, and it happens to be the lane TRK-006 (the oldest, least efficient truck) runs most. Combined volume on this lane is 791 loads generating ~$470K in revenue, but true margin is far thinner than any other lane (best lanes net $2.55–$2.61/mile).
2. **TRK-006 is a rolling cost center.** This 2013 Freightliner Cascadia (738,000 miles) averages 5.20 MPG vs. a 6.95 MPG fleet average for every other truck — burning an estimated 7,505 extra gallons over the ~24-month data window, or **~$1,287/month in excess fuel cost alone**. It also leads the fleet in total maintenance spend ($42,912, more than 4x the next truck) and downtime (461 hours), and it's disproportionately assigned to the very lane (Little Rock) that's already the least profitable.
3. **Ozark Building Supply's dock is destroying on-time performance and burning driver hours.** Ozark averages 47.7 minutes of detention per delivery vs. a 10.5-minute average at every other customer — a 37-minute gap repeated across 476 stops (~295 excess hours, ~12 hours/month). Ozark's on-time rate is a startling 3.4% (vs. 85-92% elsewhere), meaning virtually every delivery there is scored late even though the truck usually arrives on schedule — the wait, not the drive, is the failure point.
4. **Customer concentration + slow pay is a cash-flow risk.** The top 4 customers are 78.4% of revenue. Route 66 Ag Cooperative (16.4% of revenue, ~$9,553/month) pays on a de facto net-60 cycle against net-30 terms, meaning roughly a full month of revenue — about $9,500 — is perpetually tied up in receivables beyond contract terms.
5. **Driver turnover is concentrated in the newest hires.** 3 of 14 drivers (21%) have been terminated, and all three were hired within the last ~18 months (2025-01 through 2025-07) — meaning 30% of drivers hired since January 2025 didn't last. Losing drivers this early destroys any training investment and forces repeated onboarding cost.

---

## App Ideas

### App 1: Lane Profitability Explorer

**Build ID:** app-01-lane-profitability
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, routes.csv, trips.csv, fuel_purchases.csv
**Additional data needed:** none (fixed operating cost per mile — insurance, driver pay, depreciation — would sharpen true net margin beyond fuel, but fuel-adjusted margin is calculable now)

**Problem solved:**
Curtis has always suspected "one of his lanes barely pays for itself" but has never had it proven or sized. The data confirms it: Joplin↔Little Rock nets only $1.46-$1.50/mile after fuel, roughly 40% worse than the best lane (Joplin↔Springfield at $2.55-$2.61/mile), despite carrying nearly 800 loads of volume. This app puts every lane side-by-side so Curtis can decide whether to renegotiate the Little Rock rate, shift better trucks onto it, or de-prioritize it for growth.

**What the app shows:**
- A ranked bar chart of all 10 lanes by net margin per mile (revenue + fuel surcharge, minus estimated fuel cost), lowest to highest
- A callout comparing the worst lane (Little Rock, both directions) against Curtis's stated $2.05/mile breakeven threshold
- Lane-level table: distance, load count, avg revenue/mile, fuel cost/mile, net/mile, total lane revenue
- A trend view of monthly net margin per mile for the selected lane to show whether it's getting better or worse
- Filter/selector to pick a lane and drill into which trucks and drivers run it most

**Key metric / headline number:**
"Joplin → Little Rock nets $1.50/mile after fuel — $0.55/mile below Curtis's $2.05 breakeven, costing an estimated $150+ per round trip."

**Build specification:**
- Merge loads + routes on route_id; compute total_revenue = revenue + fuel_surcharge; rev_per_mile = total_revenue / distance_miles
- Merge trips + fuel_purchases (via trip_id) to get per-trip fuel cost; join to route via load_id → route_id; compute fleet-level avg fuel_cost_per_mile per route
- net_per_mile = avg_rev_per_mile - avg_fuel_cost_per_mile; sort ascending so worst lanes are immediately visible
- Primary chart: horizontal bar chart, one bar per lane (both directions combined or shown as paired bars), color-coded red/amber/green relative to the $2.05 breakeven line (draw as a reference line/annotation)
- Secondary chart: line chart of monthly net_per_mile for Little Rock lane specifically, overlaid with the breakeven line, to answer "is this getting worse?"
- Table below the chart: sortable by any column, with Little Rock rows highlighted by default
- Interactivity: dropdown to select a lane, which filters a "which trucks/drivers run this lane" mini-table underneath
- Headline callout box at the top of the page stating the Little Rock shortfall in dollars per round trip and per month, not just per mile — owners think in trips and monthly P&L, not abstract per-mile units

**Success criteria:**
Within 60 seconds, Curtis should be able to say "the Little Rock lane is the problem, it's losing about $X/month relative to breakeven, and here's whether it's getting better or worse" — enough to decide whether to renegotiate the rate with the customer or reassign equipment.

---

### App 2: Truck Health & Cost Scorecard

**Build ID:** app-02-truck-health-scorecard
**Audience:** fleet manager
**Category:** dashboard
**Priority:** HIGH
**Data required:** trucks.csv, trips.csv, fuel_purchases.csv, maintenance_records.csv
**Additional data needed:** none (resale/trade-in values would sharpen a replace-vs-repair recommendation but aren't required for the core scorecard)

**Problem solved:**
TRK-006 is bleeding money in three ways at once — worst fuel economy (5.2 MPG vs. 6.95 fleet average), highest total maintenance cost ($42,912, over 4x the next truck), and highest downtime (461 hours) — but because these numbers live in three different spreadsheets, Curtis has never seen them combined into one truck-level verdict. This app gives every truck a single composite health score so fleet decisions (repair vs. retire, which truck gets the good lane) are obvious at a glance.

**What the app shows:**
- A scorecard grid, one card per truck (TRK-001 through TRK-010), each showing: MPG vs. fleet average, total maintenance cost, total downtime hours, and a composite "cost per mile" (fuel + maintenance ÷ total miles driven)
- TRK-006 flagged with a red badge and a specific dollar callout: "$1,287/month in excess fuel cost vs. fleet average, plus $42,912 in cumulative repairs — the highest-cost unit in the fleet by a wide margin"
- A scatter plot: truck age (or odometer) on the x-axis vs. total cost per mile on the y-axis, to visually show where the cost curve bends upward
- Maintenance cost trend by month for the whole fleet, with a toggle to isolate a single truck
- A ranked table sortable by total cost per mile, so the worst-value truck is always at the top

**Key metric / headline number:**
"TRK-006 costs $0.34/mile more than the fleet average once fuel and maintenance are combined — roughly $52,000/year in excess cost for one 2013 unit with 738,000 miles."

**Build specification:**
- Compute per-truck: avg_mpg (from trips), total_fuel_cost (from fuel_purchases), total_maintenance_cost + total_downtime_hours (from maintenance_records), total_miles (from trips)
- cost_per_mile = (total_fuel_cost + total_maintenance_cost) / total_miles; compute fleet average and each truck's delta from it
- Scorecard cards use a traffic-light color (green/amber/red) based on cost_per_mile percentile within the fleet — do NOT use arbitrary fixed thresholds, base it on the fleet's own distribution since this is a small 10-truck fleet
- Scatter plot: x = truck year (proxy for age) or current_odometer, y = cost_per_mile, sized by total_downtime_hours, labeled with truck_id — TRK-006 should visually separate itself from the cluster
- Include a specific annotation/callout on the scatter plot pointing at TRK-006
- Maintenance trend chart: monthly total cost across the fleet, with a truck selector dropdown that overlays that truck's line against the fleet total for comparison
- Since this is a small fleet (10 trucks), don't over-engineer with pagination — show all 10 in the grid at once

**Success criteria:**
Curtis or his fleet manager should be able to open this and immediately identify which single truck, if any, is worth planning for replacement — backed by a specific dollar-per-year figure, not just a gut feeling about "the old one."

---

### App 3: Customer Detention & Dock Performance Tracker

**Build ID:** app-03-detention-tracker
**Audience:** dispatcher
**Category:** tracker
**Priority:** HIGH
**Data required:** delivery_events.csv, loads.csv, customers.csv

**Problem solved:**
Curtis knows "one customer's dock crew is chronically slow" but has no way to quantify it or use it in rate negotiations. Ozark Building Supply averages 47.7 minutes of detention per delivery — more than 4x the 10.5-minute average everywhere else — across 476 stops, and it's dragging Ozark's on-time score down to 3.4% even though trucks generally leave on schedule. This app turns that pattern into a concrete negotiating position and a dispatcher early-warning tool.

**What the app shows:**
- A ranked bar chart of average detention minutes by customer, with Ozark clearly the outlier
- A callout: "Ozark Building Supply averages 47.7 min of detention vs. 10.5 min fleet-wide — costing an estimated 295+ driver-hours over the past 2 years"
- On-time rate by customer shown side-by-side with detention, to make the causal link visible (Ozark's on-time collapse tracks its detention, not driving performance)
- A distribution/histogram of detention minutes at Ozark specifically, to show whether it's consistently bad or occasionally catastrophic (max 76 minutes)
- A trend line of Ozark's detention over time — is it getting worse, or was there a specific period that was worse?

**Key metric / headline number:**
"Ozark Building Supply detention costs Bridgewell ~12 driver-hours per month — equivalent to nearly 2 extra full driving days lost to waiting, not driving."

**Build specification:**
- Merge delivery_events with loads (via load_id) and customers (via customer_id); group by customer to compute avg/median/max detention_minutes and on_time rate
- Primary chart: bar chart of avg detention by customer, sorted descending, with a horizontal reference line at the fleet average (10.5 min) so the Ozark bar visibly towers over it
- Secondary paired chart: on_time_rate by customer next to detention by customer (dual-axis or two side-by-side bars) to make the correlation obvious without stating it as fact — let the visual do the work
- Histogram of Ozark's individual detention_minutes values to show the shape of the problem (is it always ~45 min, or wildly variable?)
- Time series: monthly avg detention at Ozark overlaid with fleet average, so dispatchers/owner can see if a conversation with Ozark's dock manager actually changed anything after it happens
- Add a small "cost estimate" panel: excess_minutes × stops × (assumed driver cost/hour, make this an adjustable input field defaulting to $28/hr) so the dollar impact updates interactively — this is the number Curtis would bring into a rate renegotiation conversation
- Customer selector so the same view can be applied to any customer, not just Ozark, since this becomes a standing operational tool

**Success criteria:**
A dispatcher or Curtis should be able to pull this up before a call with Ozark and state, in specific numbers, how much extra time and money Ozark's dock delays cost — turning a gut feeling into a negotiating fact.

---

### App 4: Driver Fuel Efficiency Leaderboard

**Build ID:** app-04-driver-fuel-leaderboard
**Audience:** driver
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** trips.csv, drivers.csv, fuel_purchases.csv

**Problem solved:**
Fuel efficiency varies meaningfully by driver (from 6.34 MPG for David Osgood down to 6.87 for James Holbrook, a ~8% spread) independent of truck assignment, but no driver currently gets feedback on how their driving style affects fuel spend. This app gives each driver visibility into their own number relative to peers, which is both a coaching tool and a fairness check (since raw MPG can be confounded by which truck/lane a driver is assigned).

**What the app shows:**
- A personal MPG scorecard for the logged-in/selected driver vs. the fleet average and the top-performing driver
- A leaderboard ranking all 14 drivers by average MPG, with an adjustment note that assignment to older trucks (like TRK-006) affects this and should be read carefully
- A trend line of the selected driver's MPG over time, to show whether they're improving
- Total gallons and estimated fuel cost attributable to the driver's trips, framed as "your trips used X gallons this month"

**Key metric / headline number:**
"Your average MPG is 6.34 vs. a fleet average of 6.64 — closing that gap could save the company about $40/month on your routes alone."

**Build specification:**
- Group trips by driver_id to get avg_mpg, total_miles, total_gallons; join with fuel_purchases (via trip_id) for total_cost per driver
- IMPORTANT: control for truck assignment — compute each driver's mpg_vs_truck_baseline (their MPG relative to what that specific truck normally gets across all drivers) so a driver isn't penalized for being assigned TRK-006 disproportionately. Show both raw MPG rank and truck-adjusted rank, and label clearly which is which
- Leaderboard: horizontal bar chart sorted by adjusted MPG performance, highlight the selected driver's bar
- Personal trend chart: line of the driver's monthly avg MPG, with a shaded band showing the fleet's normal range, so the driver can see if they're inside or outside normal variation
- Keep tone constructive, not punitive — frame headline numbers around savings opportunity, not blame ("closing the gap could save...")
- Driver selector dropdown at the top (this app would eventually be scoped per-driver-login, but for the demo a selector works)

**Success criteria:**
A driver should be able to see, in under 60 seconds, exactly where they rank on fuel efficiency and whether it's about their driving or their truck assignment — enough to know if there's something actionable to change.

---

### App 5: Customer Profitability & Concentration Dashboard

**Build ID:** app-05-customer-profitability
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, customers.csv, delivery_events.csv, trips.csv

**Problem solved:**
Curtis's top 4 customers are 78.4% of revenue, which he knows gives him "pricing leverage in theory but real exposure in practice." What he hasn't seen quantified is that these customers aren't equally good: Sooner State Lumber delivers the best revenue-per-load ($680.60) while Crossroads Hardware trails badly ($237.67), and Route 66 Ag Cooperative's slow pay ties up roughly $9,500/month in receivables beyond terms. This app lets Curtis see profitability and risk by customer in one place instead of just gross revenue.

**What the app shows:**
- A ranked table/chart of customers by total revenue, with % of total revenue clearly shown (concentration risk)
- Revenue per load by customer, to separate "high volume" from "high value" customers
- A combined risk flag column: payment terms vs. actual pay cycle, detention performance, on-time rate — so a customer like Route 66 Ag shows both its revenue contribution AND its cash-flow drag
- A "what if we lost this customer" stress-test: selecting a customer shows what % of monthly revenue would disappear
- Industry breakdown (building materials vs. agriculture) to show diversification within the customer base

**Key metric / headline number:**
"Your top 4 customers are 78.4% of revenue — losing Sooner State Lumber alone (your best-margin account at $680.60/load) would remove 23% of total revenue overnight."

**Build specification:**
- Aggregate loads by customer_id: total_revenue, load_count, avg_revenue_per_load, pct_of_total_revenue
- Join customers.csv for payment_terms_days and industry
- Compute actual pay cycle proxy: since raw payment data isn't in this dataset, note in the "Additional data needed" that AR aging data would let this be precise — for now, surface payment_terms_days as-is and flag it as a placeholder until real AR data is connected
- Join delivery_events (via loads) for on_time_rate and avg_detention_minutes by customer — reuse the same aggregation logic as App 3
- Main chart: treemap or stacked bar of revenue by customer, sized by revenue, colored by revenue-per-load (so big-but-low-value customers like Crossroads stand out differently from big-and-high-value like Sooner State)
- Concentration callout: pie or donut chart showing top-4 vs. rest, with the 78.4% figure as a large headline number
- Interactive "stress test" selector: click/select a customer, show a before/after bar of total monthly revenue with and without that customer
- Small multiples or a compact table combining revenue %, on-time %, and avg detention per customer so risk and value are visible in the same row

**Success criteria:**
Curtis should be able to answer "which customer can I least afford to lose, and which one is actually costing me the most in hidden ways (detention, slow pay)?" within 60 seconds.

---

### App 6: Driver Retention & Onboarding Risk Monitor

**Build ID:** app-06-driver-retention-risk
**Audience:** owner
**Category:** tracker
**Priority:** MEDIUM
**Data required:** drivers.csv, trips.csv
**Additional data needed:** exit interview notes or termination reason codes would make this far more actionable — currently only hire date and status are available

**Problem solved:**
3 of Bridgewell's 14 drivers (21%) have been terminated, and all three were hired within an 18-month window (Jan–Jul 2025) — meaning 30% of drivers hired since January 2025 didn't last. Curtis has felt driver turnover as "a driver who quit without notice" but hasn't seen it as a pattern concentrated in a specific hiring cohort. This app surfaces that pattern so hiring/onboarding practices can be examined before the next hire is lost.

**What the app shows:**
- A timeline/gantt-style view of all 14 drivers showing hire date, current status (active/terminated), and tenure length
- A cohort breakdown: turnover rate for drivers hired before vs. after January 2025
- Years of experience at hire date vs. termination status, to check whether newer-to-trucking drivers are more likely to leave than veterans
- A simple "at risk" flag for currently active drivers who share characteristics (low tenure, low years_experience) with the terminated cohort

**Key metric / headline number:**
"30% of drivers hired since January 2025 have already left — more than 1 in 4 of your newest hires isn't making it past the first year."

**Build specification:**
- Compute tenure_days = a synthetic "as-of" date (max date in trips.csv) minus hire_date for active drivers, and note that termination date isn't in the dataset (flag as a data gap — recommend the company start tracking termination_date to make this precise)
- Timeline chart: horizontal bars per driver from hire_date to either today (active) or a visual "X" marker (terminated) at approximate position — since exact termination date isn't available, be transparent in a caption that termination timing is approximate
- Cohort comparison: bar chart of termination rate for two buckets (hired before 2025-01-01 vs. on/after), clearly showing the 0% vs. 30% split
- Scatter: years_experience at hire vs. status (active/terminated), color-coded, to check if newer-to-trucking hires churn more
- Callout box recommending what additional data would sharpen this: termination reason codes, exit interview flags, or pay/route assignment history for terminated drivers
- Keep this app modest in scope given the small sample (14 drivers, 3 terminations) — present it as a pattern worth watching, not a statistically bulletproof model

**Success criteria:**
Curtis should walk away understanding that turnover isn't random — it's concentrated in recent hires — and have a starting hypothesis (onboarding? route assignment? pay?) to investigate before it happens again.

---

### App 7: Load Acceptance Calculator (Dispatcher Tool)

**Build ID:** app-07-load-acceptance-calculator
**Audience:** dispatcher
**Category:** calculator
**Priority:** HIGH
**Data required:** routes.csv, loads.csv, trucks.csv, trips.csv (for historical fuel cost/mile by route and truck)
**Additional data needed:** live/current fuel price feed would make this precise day-to-day; deadhead mile estimates for backhaul planning would strengthen it further

**Problem solved:**
Curtis dispatches from a whiteboard and spreadsheets, deciding in his head whether a load is worth taking. The data shows this matters — Little Rock loads net $1.46-1.50/mile while Springfield loads net $2.55-2.61/mile — but there's no tool that tells a dispatcher in the moment, before accepting a load, whether the offered rate clears breakeven for that specific lane and truck. This app is a real-time "should we take this load" calculator built directly from Bridgewell's own historical cost structure.

**What the app shows:**
- Input fields: origin/destination (or route selector), offered rate, distance, which truck would run it
- Instant calculation: estimated fuel cost (using that truck's historical MPG and current fuel price), net revenue per mile, and a clear ACCEPT / MARGINAL / REJECT verdict against the $2.05/mile breakeven benchmark
- A comparison panel showing how this load's economics stack up against the lane's historical average
- A "what if a different truck ran this" toggle — e.g., show that assigning TRK-006 to this load changes the math meaningfully worse than assigning a fuel-efficient truck

**Key metric / headline number:**
"This load nets $1.52/mile after fuel with TRK-006 assigned — $0.53/mile below breakeven. Swapping to TRK-008 would net $1.71/mile."

**Build specification:**
- Pre-load historical per-route and per-truck MPG/cost data (from trips.csv + fuel_purchases.csv + routes.csv) as the calculation baseline
- Build a simple form: route/lane dropdown (pre-fills distance and typical base_rate_per_mile from routes.csv), offered rate input, truck dropdown (pre-fills that truck's historical avg MPG)
- Calculation: fuel_cost = distance / truck_mpg × current_fuel_price (expose fuel_price as an editable input defaulting to the most recent avg from fuel_purchases.csv); net_per_mile = (offered_rate - fuel_cost/distance)
- Verdict logic: green ("ACCEPT") if net_per_mile > $2.05, amber ("MARGINAL") if within $0.15 of breakeven, red ("REJECT") if below — make the $2.05 threshold an editable setting since it's Curtis's own stated number, not a universal constant
- Side panel: bar comparing this calculated net/mile against the historical average net/mile for that same lane, so the dispatcher knows if this specific offer is better or worse than usual
- Truck swap comparison: small table showing net/mile if each of the 10 trucks were assigned, sorted best to worst, so a dispatcher can see the assignment opportunity at a glance
- This should feel like a fast, single-screen tool — dispatchers need an answer in seconds, not a multi-page report

**Success criteria:**
A dispatcher facing an incoming load offer should get an ACCEPT/MARGINAL/REJECT answer and a truck-assignment recommendation in under 30 seconds, without doing math by hand.

---

### App 8: Fleet & Revenue Command Center (Owner Home Dashboard)

**Build ID:** app-08-owner-command-center
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, trips.csv, fuel_purchases.csv, maintenance_records.csv, drivers.csv, customers.csv, routes.csv

**Problem solved:**
Curtis runs the business from a whiteboard and "a handful of spreadsheets," meaning there's no single place to see business health at a glance. This app is the front door — a weekly-glance summary combining revenue trend, fleet cost, on-time performance, and the top 3 issues (Little Rock lane, TRK-006, Ozark detention) into one view, so Curtis doesn't have to open five spreadsheets to know how the business is doing.

**What the app shows:**
- Top-row KPI tiles: total revenue (trailing 30 days), total loads, fleet-wide on-time %, fleet-wide avg MPG, total maintenance spend — each with a trend arrow vs. the prior period
- A "top issues this month" callout panel automatically surfacing the biggest deviations (worst lane, worst truck, worst customer for detention) — pulling directly from the other apps' logic so it stays consistent
- Monthly revenue and load volume trend chart (24 months of history available)
- A fuel cost trend line (price per gallon has crept from ~$3.87 to ~$4.34/gallon over the data period) with commentary on how much of that is passed through via fuel surcharge vs. absorbed
- Quick links / drill-through to the more detailed apps (lane profitability, truck health, detention tracker) for follow-up

**Key metric / headline number:**
"Fleet on-time rate: 86.8% (trailing 30 days) — down from a 24-month high of 92%, largely driven by Ozark Building Supply detention."

**Build specification:**
- Compute trailing-30-day and trailing-90-day rollups for: total_revenue, load_count, on_time_rate, avg_mpg, total_maintenance_cost — compare each to the prior equivalent period for a trend arrow (up/down/flat, colored appropriately)
- KPI tiles across the top of the page, using large numerals with small trend sparklines beneath each (reuse the dataviz skill's stat-tile pattern)
- Auto-generated "top issues" panel: hardcode the logic to check (a) which lane has the lowest net_per_mile, (b) which truck has the highest cost_per_mile, (c) which customer has the highest avg_detention — surface whichever crosses a materiality threshold, don't just always show all three if one resolves itself over time
- Fuel price trend chart: monthly avg price_per_gallon line, annotated with the surcharge revenue collected in the same months so Curtis can see the relationship
- Revenue/volume trend: dual-axis or combo chart (bars for load count, line for revenue) across all 24 months of history
- This is the landing page — keep it information-dense but scannable, prioritize the KPI row and top-issues panel above the fold
- Since this pulls logic from multiple other apps (lane margin, truck cost, detention), factor those calculations into shared functions so the numbers are guaranteed consistent across apps, not recalculated slightly differently in each

**Success criteria:**
Curtis should be able to open this Monday morning, and in under 60 seconds know: is revenue up or down, is the fleet running efficiently, and what's the single biggest problem to deal with this week.

---

### App 9: Maintenance Cost & Downtime Forecaster

**Build ID:** app-09-maintenance-forecaster
**Audience:** fleet manager
**Category:** predictor
**Priority:** MEDIUM
**Data required:** maintenance_records.csv, trucks.csv
**Additional data needed:** scheduled/preventive maintenance intervals (mileage- or time-based) would allow a true predictive model; currently only historical repair records exist, so this is a trend-based forecaster rather than a failure predictor

**Problem solved:**
Maintenance cost is lumpy and unpredictable month to month ($185 in June 2026 vs. $15,131 in August 2024), and engine repair + transmission service are the two most expensive categories ($30,273 and $28,636 total respectively) — but there's no forward-looking view of what's likely coming due. This app gives the fleet manager a rolling forecast based on each truck's mileage accumulation and service history, so big-ticket repairs are budgeted for rather than a surprise.

**What the app shows:**
- Per-truck maintenance cost history as a timeline, with service_type labeled at each event
- A rolling 3-month and 12-month average cost per truck, projected forward as a simple trend line
- A flag for trucks approaching known high-cost service intervals based on odometer patterns in the historical data (e.g., transmission service and engine repair cluster at certain mileage bands)
- Fleet-wide monthly maintenance budget estimate based on trailing 12-month average, so accounting can budget realistically instead of being surprised

**Key metric / headline number:**
"Based on trailing 12-month trends, expect ~$5,800/month in fleet maintenance spend — TRK-006 alone accounts for roughly 35% of that."

**Build specification:**
- Build a per-truck timeline (scatter or event-marker chart) of maintenance events, x-axis = service_date, y-axis = cost, marker color = service_type, sized by downtime_hours
- Compute trailing 12-month rolling average total maintenance cost fleet-wide as the primary forecast number; break out the same rolling average per truck to identify concentration (TRK-006 driving a disproportionate share)
- Odometer-based analysis: plot cost vs. odometer_at_service across all trucks combined to see if certain service types cluster at particular mileage bands (e.g., does engine repair spike after 400K miles?) — use this as a soft predictive signal, not a hard model, and be honest in the UI that this is a trend observation, not a certified prediction
- Simple forward projection: extend the trailing-average line forward 3 months as a dotted/shaded projection band, clearly labeled as an estimate
- Budget summary panel: total projected fleet maintenance spend for the next quarter, broken down by truck, so accounting has a number to plan around
- Note prominently in the UI that adding scheduled PM (preventive maintenance) intervals as a data source would upgrade this from a trend forecaster to a true predictive maintenance tool

**Success criteria:**
The fleet manager should be able to answer "roughly how much should we budget for maintenance next quarter, and which truck is driving that number" without digging through 92 individual repair records.

---

### App 10: Fuel Surcharge Recovery Analyzer

**Build ID:** app-10-fuel-surcharge-recovery
**Audience:** accountant
**Category:** calculator
**Priority:** MEDIUM
**Data required:** loads.csv, fuel_purchases.csv, trips.csv

**Problem solved:**
Diesel price per gallon rose from ~$3.87 (Jul 2024) to ~$4.34 (Jun 2026), a 12% increase, and Bridgewell charges a fuel_surcharge on every load — but there's no visibility into whether that surcharge actually keeps pace with real fuel cost increases, or whether rising fuel prices are quietly eroding margin because the surcharge formula lags reality. This app checks whether the fuel surcharge mechanism is actually doing its job.

**What the app shows:**
- A side-by-side monthly trend: total fuel surcharge collected vs. total fuel cost actually paid
- A "surcharge coverage ratio" (surcharge collected ÷ fuel cost incurred) over time — is it staying near 100%, or drifting?
- Breakdown by customer of average fuel surcharge as a % of load revenue, to see if surcharge practices are consistent across accounts
- A simple recommendation panel: if the coverage ratio has drifted below a target (e.g., 90%), flag the dollar gap and suggest a surcharge formula adjustment

**Key metric / headline number:**
"Fuel surcharge collected covers 94% of actual fuel cost this quarter, down from 101% two years ago — a gap of roughly $X,XXX/month as diesel prices rose."

**Build specification:**
- Compute monthly total fuel_surcharge (from loads.csv, grouped by load_date month) and monthly total fuel cost (from fuel_purchases.csv, grouped by purchase_date month)
- coverage_ratio = total_surcharge / total_fuel_cost per month; plot as a line chart with a reference line at 100% (breakeven) so drift below it is immediately visible
- Secondary chart: price_per_gallon trend (already computed in the main analysis) overlaid with the coverage ratio, to visually connect rising fuel prices with surcharge adequacy
- Customer breakdown: avg fuel_surcharge as % of revenue per customer, bar chart, to check for inconsistency in how surcharge is applied across accounts
- Callout panel: compute the most recent quarter's coverage ratio vs. the first quarter of available data, express the drift in both percentage points and estimated dollars per month
- Keep the recommendation conservative and clearly labeled as a suggestion — this app surfaces a gap, it doesn't prescribe the exact new surcharge formula

**Success criteria:**
The accountant or Curtis should be able to say definitively whether the fuel surcharge is keeping up with real fuel costs, and by how much it's fallen behind, in under 60 seconds.

---

### App 11: Driver Earnings & Load Statement (Driver Self-Service Tool)

**Build ID:** app-11-driver-earnings-statement
**Audience:** driver
**Category:** workflow tool
**Priority:** LOW
**Data required:** trips.csv, loads.csv, drivers.csv
**Additional data needed:** actual driver pay structure (per-mile rate, percentage, or hourly) is not in this dataset — this app currently can only show activity, not real earnings, until pay-rate data is connected

**Problem solved:**
Drivers currently have no self-service way to see their own load history, miles driven, and on-time performance without asking dispatch. Even without pay-rate data, a simple activity statement builds trust and transparency, and becomes an earnings statement the moment pay-rate data is added.

**What the app shows:**
- A per-driver activity log: loads hauled, miles driven, and on-time rate for a selected time period (week/month/YTD)
- A simple "miles driven" and "loads completed" trend to show workload over time
- Placeholder earnings estimate section, clearly marked as pending real pay-rate data, showing how the feature would work once pay data is connected
- On-time and MPG performance summary reused from App 4, so drivers have one place for both activity and performance

**Key metric / headline number:**
"You completed 142 loads and drove 23,791 miles this year, with an 89.4% on-time rate."

**Build specification:**
- Filter trips + loads by selected driver_id and date range; summarize total loads, total miles, on_time_rate
- Simple period selector (week/month/YTD/all-time)
- Trend chart: loads per month and miles per month for the selected driver, bar or line
- Clearly labeled "Earnings — Coming Soon" section explaining that once per-mile or percentage pay rate data is added, this section will calculate actual take-home estimates — do not fabricate a pay number from assumptions, since that would mislead drivers about real income
- Reuse on-time and MPG figures from App 4 in a compact summary row so this feels like a complete personal dashboard, not a partial one

**Success criteria:**
A driver should be able to see their own recent work summary without calling dispatch, and understand exactly what's needed (pay-rate data) before this becomes a full earnings tool.

---

### App 12: Empty Miles & Backhaul Opportunity Finder

**Build ID:** app-12-backhaul-finder
**Audience:** dispatcher
**Category:** workflow tool
**Priority:** MEDIUM
**Data required:** routes.csv, loads.csv, trips.csv
**Additional data needed:** this dataset does not directly capture deadhead/empty miles (trips.csv shows actual_miles per loaded trip, but not empty legs between drop and next pickup) — flag clearly that true empty-mile tracking requires a data field the company isn't currently capturing, and this app instead analyzes return-lane balance as a proxy

**Problem solved:**
Bridgewell's routes are structured as clear round trips (e.g., ROUTE-01 Joplin→Little Rock and ROUTE-02 Little Rock→Joplin), and the data shows load counts are reasonably balanced in each direction (388 vs. 403 for Little Rock, 268 vs. 278 for Tulsa) — but nothing currently tracks whether a truck arriving in Little Rock has a backhaul lined up before it needs to leave. This app doesn't have empty-mile data to analyze directly, so it's framed as a workflow tool to help dispatchers manually plan return loads, using the historical volume balance as a planning reference.

**What the app shows:**
- A directional load-volume comparison for each lane pair (outbound vs. return), to show which return legs historically have less demand and may need proactive backhaul sourcing
- A simple lane-balance ratio (return loads ÷ outbound loads) per city-pair, flagging any lane where the ratio suggests a shortage of return freight
- A note/workflow panel reminding dispatchers to check for a backhaul before releasing a truck at a distant terminal
- Explicit callout that real empty-mile / deadhead tracking would require adding pickup/drop GPS or a "trip legs" data field the company doesn't currently collect

**Key metric / headline number:**
"Kansas City → Joplin has 285 loads vs. 280 outbound — historically balanced, but this is a volume proxy, not a true empty-miles measurement."

**Build specification:**
- Group loads by route_id, aggregate to city-pair level, compute load counts in each direction
- Compute balance_ratio = min(outbound, return) / max(outbound, return) per city pair; sort so the most imbalanced pairs surface first
- Bar chart: paired bars (outbound vs. return) per city-pair, visually easy to spot imbalance
- Since this dataset lacks true empty-mile tracking, build this as a lightweight decision-support note rather than a data-rich dashboard — keep the visual simple, and be explicit in the UI copy about the data limitation so the app doesn't overstate its own precision
- Include a clearly separated "what data would make this better" callout box specifically naming deadhead miles or trip-leg tracking as the missing input

**Success criteria:**
A dispatcher should understand which lanes have historically been demand-balanced and be reminded to actively check for backhauls elsewhere — with honest acknowledgment that this is a planning aid, not a precise empty-miles calculator.

---
