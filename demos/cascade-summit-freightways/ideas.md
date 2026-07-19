# Cascade Summit Freightways — App Ideas

Generated: 2026-07-03
Analyst findings: Independent analysis of 62,000 loads, 61,394 trips, 180,253 fuel purchases, 840 maintenance records, and 165 driver files reveals five distinct, quantifiable problems hiding inside otherwise-healthy aggregate numbers (fleet-wide on-time rate ~88%, fleet-wide MPG 6.78). One aging truck cohort is quietly consuming 8.5x the fleet's average maintenance spend, one customer's dock is responsible for nearly all of the company's detention exposure, one core lane is running at a structural loss despite full utilization, and one satellite terminal's 2023 hiring class is churning at over 4x the rate of the rest of the fleet.

---

## Primary Pain Points Discovered

1. **Truck TRK-047** (2011 Peterbilt 389, ~880K miles) averages **4.92 MPG** versus a fleet average of **6.78 MPG** — a 27% efficiency gap across 606 trips and ~1.15M miles, costing an estimated **$10,972/month** (~$263K over the 24-month data window) in excess fuel versus a fleet-average truck covering the same miles. It is the worst outlier in a broader aging cohort (TRK-041 through TRK-048, all 2010-2012 models) that clusters at 5.9-5.96 MPG, well below every other truck in the fleet (next-worst non-cohort truck: 6.83 MPG).
2. **TitanBolt Industrial Supply** (Dallas, TX / CUST-03), the company's #3 account by revenue ($38.3M, 14.6% of total), averages **47.4 minutes of detention per stop** versus **10.6 minutes** for every other customer combined — a 4.4x gap — and only **2.4%** of TitanBolt stops are on-time (vs. 80-90%+ for every other account). This is costing an estimated **$15,900/month** in idle driver/truck time at a conservative $75/hr opportunity-cost rate.
3. **The Seattle↔Atlanta lane (RTE-04/RTE-08)** nets **$1.30-$1.39/mile** after fuel — the two worst-performing lanes in the network — against the company's **$2.05/mile** breakeven target, despite running full volume (11,656 loads, ~31M miles over the data window, ~480 loads/month). The shortfall versus breakeven annualizes to roughly **$10.7M**, the single largest quantified pain point in the dataset, yet dispatch continues to schedule it at normal volume.
4. **The Chicago terminal's 2023 driver hiring cohort** (21 drivers hired that year) shows a **61.9% termination rate**, versus **14.0%** for the Spokane terminal overall and **20.0%** fleet-wide — a >4x gap concentrated in a single hiring class at a single terminal, pointing to an onboarding, pay, or home-time problem specific to Chicago rather than generic driver-market churn.
5. **The aging truck cohort (TRK-041 through TRK-048, 2010-2012 model years)** averages **$101,488 in maintenance cost** and **1,015 downtime hours** per truck versus a fleet average of **$18,469** and **156 hours** — 5.5x the cost and 6.5x the downtime of the rest of the fleet, concentrated in 8 of 110 trucks. This cohort also drives the low-MPG problem in Finding #1, compounding the fuel and maintenance drag on the same 8 units. Excess maintenance cost alone runs ~**$354K/year** across the cohort versus what a fleet-average truck would cost.

Interesting-but-secondary: customer concentration (top account = 25.4% of revenue), payment terms skew for TitanBolt/Peachtree (45 days vs. 30 for others), and a mild seasonal dip in loads/on-time rate each February — none of these rise to the level of the five primary findings above.

---

## App Ideas

### App 01: Truck True Cost Ranking

**Build ID:** app-01-truck-true-cost
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** trucks.csv, trips.csv, fuel_purchases.csv, maintenance_records.csv
**Additional data needed:** none

**Problem solved:**
Walter and Renee currently judge trucks informally — "that one's always in the shop" — with no single number that combines fuel efficiency, maintenance spend, and downtime into a true operating cost. TRK-047 alone is burning $10,972/month in excess fuel, and the TRK-041–048 cohort is running 5.5x the fleet's average maintenance cost, but neither shows up unless someone actively cross-references three separate CSVs.

**What the app shows:**
- A ranked table of all 110 trucks by "true cost per mile" = (fuel cost + maintenance cost + downtime-hours × estimated hourly opportunity cost) / total miles
- A highlighted red-flag row for TRK-047 and the TRK-041–048 cohort, with a clear callout of how many multiples above fleet average they run
- A scatter plot: MPG (x-axis) vs. maintenance cost per mile (y-axis), sized by total miles driven, so aging-cohort trucks cluster visibly in the bad corner
- A "cost to replace vs. cost to keep" toggle: for the worst 10 trucks, show 12-month trailing true cost vs. an estimated new-truck payment, to support replace/keep decisions
- Truck detail drill-down: click any truck to see its maintenance history (service_type breakdown), fuel trend over time, and driver assignments

**Key metric / headline number:**
"TRK-047 costs $18,057/month more to operate than a fleet-average truck (fuel + maintenance + downtime) — and it's not alone: the TRK-041–048 cohort collectively overspends by $29,500/month."

**Build specification:**
- Merge trips.csv + fuel_purchases.csv (grouped by trip_id, summed) + maintenance_records.csv (grouped by truck_id) on truck_id.
- Compute per-truck: total_miles, total_fuel_cost, total_maintenance_cost, total_downtime_hours, avg_mpg.
- True cost per mile = (fuel + maintenance + downtime_hours * $50/hr placeholder opportunity cost) / total_miles. Make the $/hr assumption a visible, editable input (slider or number field) so Renee can adjust it — this is the single most important interactivity element since it's a judgment call, not a fact in the data.
- Sort descending by true cost per mile; default view shows top 15 worst trucks, with a "show all 110" expand.
- Use a diverging color scale (per the dataviz skill) on the cost-per-mile column: green near fleet median, red for the aging cohort outliers.
- Scatter plot: annotate TRK-047 and the aging cohort by name directly on the chart (not just in a legend) since they're the whole point.
- Layout: headline callout at top, scatter plot + ranked table side-by-side or stacked below, drill-down as an expandable row or modal.
- Filter by make/model/year to let the user quickly confirm "yes, it's specifically the 2010-2012 units."

**Success criteria:**
Renee should be able to answer "which 5 trucks should I consider retiring this year, and how much would it save?" within 60 seconds of opening the app.

---

### App 02: Customer Detention Scorecard

**Build ID:** app-02-detention-scorecard
**Audience:** dispatcher
**Category:** tracker
**Priority:** HIGH
**Data required:** delivery_events.csv, loads.csv, customers.csv
**Additional data needed:** a per-facility detention fee/accessorial policy (if one exists) to compute actual billable detention recovery, not just estimated cost

**Problem solved:**
TitanBolt Industrial Supply's dock averages 47.4 minutes of detention per stop — 4.4x every other customer — and dispatch has no per-customer view that would let Renee negotiate detention fees, adjust scheduling buffers, or push back on TitanBolt specifically instead of treating it as fleet-wide noise.

**What the app shows:**
- A bar chart ranking all 8 customers by average detention minutes per stop, with TitanBolt visibly isolated from the rest of the pack (they cluster at ~10-11 min; TitanBolt sits at 47+)
- A trend line of TitanBolt's detention over time — is it getting better, worse, or flat?
- A facility-type breakdown (shipper / consignee / cross-dock) to identify exactly where in TitanBolt's supply chain the delay happens
- Estimated monthly cost of excess detention per customer, using an adjustable $/hour opportunity-cost input
- A "what if" calculator: if TitanBolt's detention dropped to the fleet average, how many additional loads could the same trucks run per month?

**Key metric / headline number:**
"TitanBolt Industrial Supply costs Cascade Summit ~$15,900/month in excess detention — equivalent to the truck-hours needed to run roughly 8 more loads."

**Build specification:**
- Join delivery_events.csv to loads.csv (on load_id) to customers.csv (on customer_id).
- Compute avg/median detention_minutes and on_time rate grouped by customer_name and facility_type.
- Primary chart: horizontal bar chart of avg detention by customer, sorted descending, TitanBolt called out with a distinct color/annotation per the dataviz skill's emphasis techniques.
- Secondary: line chart of TitanBolt's monthly avg detention (from scheduled_time month) to show whether this is a persistent or worsening pattern.
- Include a facility_type filter/selector so the dispatcher can see if it's specifically TitanBolt's shipping dock, receiving dock, or cross-dock step.
- Add a simple input box for "opportunity cost per hour of driver+truck time" (default $75) driving the monthly cost estimate — label clearly as an estimate.
- Layout: headline number top-left, ranked bar chart top-right, trend line below, facility breakdown as a small multiple or filtered view at the bottom.

**Success criteria:**
Renee can walk into a call with TitanBolt's traffic manager with one screen that proves the detention problem is real, quantified, and specific to their dock — answering "how bad is it and where exactly" in under 60 seconds.

---

### App 03: Lane Profitability Explorer

**Build ID:** app-03-lane-profitability
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, trips.csv, routes.csv, fuel_purchases.csv
**Additional data needed:** an explicit company breakeven rate per mile (assumed $2.05/mile here; ideally sourced from accounting) and driver pay/mile if available, to compute full margin rather than margin after fuel only

**Problem solved:**
Seattle↔Atlanta is being run at full volume (11,656 loads in the data window) while netting $1.30-$1.39/mile against a $2.05 breakeven — a structural loss on one of the company's four core lane pairs that nobody has flagged because lane performance is currently judged load-by-load, not lane-by-lane.

**What the app shows:**
- A ranked bar/table of all 12 routes by average net-revenue-per-mile after fuel, with a horizontal breakeven line at $2.05/mile so underwater lanes are visually obvious
- Seattle→Atlanta and Atlanta→Seattle both clearly below the line, with total loads and total miles run so the scale of the problem is obvious (this isn't a rounding error — it's a top-4 lane)
- A monthly trend for the Seattle-Atlanta lane specifically: is the gap narrowing, widening, or stable?
- An annualized dollar-shortfall callout comparing actual net revenue to what breakeven-rate revenue would have been
- A rate-adjustment simulator: "if base_rate_per_mile increased by $X on this lane, would it clear breakeven?" using the known base_rate_per_mile and fuel-cost trend

**Key metric / headline number:**
"The Seattle↔Atlanta lane pair is running $0.70/mile below breakeven — an estimated $10.7M/year shortfall versus target margin, despite running ~480 loads/month at full utilization."

**Build specification:**
- Merge trips.csv → loads.csv → routes.csv; join fuel_purchases.csv grouped by trip_id for fuel_cost.
- Compute net_per_mile = (revenue + fuel_surcharge - fuel_cost) / actual_miles per trip, then aggregate by route_id.
- Primary chart: horizontal bar chart of all 12 lanes sorted by avg net_per_mile, breakeven line ($2.05, adjustable input) drawn across the chart, bars below the line colored to stand out (see dataviz skill for semantic color use — reserve the alert color for lanes under breakeven only).
- Secondary: line chart filtered to RTE-04/RTE-08 showing monthly avg net_per_mile trend, so the user can see this is persistent and not a one-month blip.
- Shortfall calculation: sum over all loads on the lane of (breakeven_rate - actual_net_per_mile) * actual_miles, displayed both as a total-to-date and annualized figure — label the annualization assumption clearly.
- Lane selector dropdown to let the owner inspect any of the 12 lanes the same way, not just Seattle-Atlanta.
- Layout: headline callout and breakeven bar chart on top, trend + shortfall detail below for the selected lane.

**Success criteria:**
Walter should be able to see, in under 60 seconds, which lane(s) are structurally unprofitable versus just having a bad month, and roughly what rate increase or cost reduction would be needed to fix it.

---

### App 04: Chicago Terminal Retention Dashboard

**Build ID:** app-04-chicago-retention
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** drivers.csv
**Additional data needed:** exit-interview reasons, pay-by-terminal data, and home-time/dispatch-frequency data would substantially strengthen this app; currently it can only show *that* the problem exists, not *why*

**Problem solved:**
The Chicago satellite terminal's 2023 hiring cohort (21 drivers) has a 61.9% termination rate versus 14.0% at Spokane and 20.0% fleet-wide, but this is invisible in aggregate turnover reporting because it's averaged in with Spokane's much larger, much more stable driver population (114 Spokane vs. 51 Chicago drivers).

**What the app shows:**
- Side-by-side termination-rate comparison: Chicago vs. Spokane, by hire-year cohort, so the 2023 spike is visually isolated from both terminals' normal-year churn
- A cohort-survival-style view: of drivers hired in each year at each terminal, what % are still active today?
- Headline stat comparing Chicago 2023 (61.9%) to Spokane 2023 (2 of 8, 25%) hired in the same calendar year — proving it's terminal-specific, not market-wide
- Years-of-experience distribution by terminal, to check whether Chicago is hiring less-experienced drivers who are more likely to churn regardless of terminal conditions
- A simple cost-of-turnover estimate (recruiting + training cost per replaced driver × excess terminations) to put a dollar figure on the retention gap

**Key metric / headline number:**
"Chicago's 2023 hiring class has lost 13 of 21 drivers (61.9%) — more than 4x Spokane's 2023 cohort loss rate (25%) in the same calendar year."

**Build specification:**
- Group drivers.csv by home_terminal and hire_year (derived from hire_date); compute termination rate = count(employment_status == 'terminated') / count(*) per group.
- Primary visualization: grouped/paired bar chart, one bar pair per hire-year, Chicago vs. Spokane, using consistent categorical colors per terminal (dataviz skill) so the eye tracks each terminal's bar across years.
- Overlay or annotate the 2023 pair specifically since it's the standout — do not bury it in a wall of similar-looking bars.
- Secondary: a small table breaking out years_experience distribution for the Chicago 2023 cohort vs. Spokane's typical new hires, to rule out "they just hired less experienced people" as the sole explanation.
- Add a terminal filter and a hire-year range filter for open-ended exploration beyond the headline finding.
- Layout: headline stat top, paired bar chart as the dominant visual, experience-distribution table below.

**Success criteria:**
Renee should be able to point at one chart and say "it's not driver quality, it's something about how we ran Chicago in 2023" — answering whether the problem is terminal-specific within 60 seconds.

---

### App 05: Weekly Owner Scorecard

**Build ID:** app-05-owner-scorecard
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, trips.csv, fuel_purchases.csv, maintenance_records.csv, delivery_events.csv, drivers.csv
**Additional data needed:** none for v1; a target/budget number per KPI (revenue target, on-time target, etc.) would let the scorecard show variance-to-plan rather than just trend

**Problem solved:**
Walter and Renee currently have no single-glance view of business health — each of the five primary pain points lives in a different spreadsheet or gut feeling. A weekly digest would surface all five (aging-truck cost, TitanBolt detention, lane losses, Chicago turnover, plus overall volume/revenue) in one place before Monday morning dispatch decisions get made.

**What the app shows:**
- Top-line KPI row: total loads this week/month, total revenue, fleet avg MPG, fleet on-time %, active driver count — each with trend arrow vs. prior period
- A "watch list" panel that auto-surfaces the 5 primary pain points as standing alerts (TRK-047 efficiency, TitanBolt detention, Seattle-Atlanta margin, Chicago churn, aging-cohort maintenance) with this week's/month's number for each
- A monthly trend chart of loads and revenue (using the existing 24-month history) so seasonal dips (e.g., February) don't get mistaken for a new problem
- A fuel price trend chart, since fuel cost per gallon has risen from ~$3.93 to ~$4.27 over the data window and affects every margin calculation elsewhere in the app suite

**Key metric / headline number:**
"5 standing issues are actively costing Cascade Summit money this month — combined estimated impact: ~$35,000+/month in fuel, detention, and maintenance overspend, plus a structurally unprofitable core lane."

**Build specification:**
- This app is essentially a rollup: reuse the aggregation logic from Apps 01-04 (truck true cost, detention by customer, lane margin, Chicago turnover) and pull each app's headline number into a single watch-list component.
- KPI row: simple stat tiles per the dataviz skill's stat-tile guidance — big number, small trend arrow/sparkline, no chart-junk.
- Trend chart: monthly loads (bars) and revenue (line) combo chart over all 24 months of history, so Walter can see the business is essentially flat/stable in volume — useful context so he doesn't chase phantom problems.
- Watch-list panel: five rows, one per pain point, each with the headline number and a link/button that would (in a full product) deep-link to the relevant detail app.
- No filters needed on this page — it's meant to be a fast, opinionated summary, not an exploration tool. Keep it to one screen, no scrolling if possible.
- Refresh cadence framing: label it "as of {latest load_date in data}" so it reads as a living report rather than a static one-time export.

**Success criteria:**
Walter should be able to open this once a week and know, within 60 seconds, whether anything needs his attention this week — without opening a single spreadsheet.

---

### App 06: Driver Fuel Efficiency & Performance Feedback

**Build ID:** app-06-driver-scorecard
**Audience:** driver
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** trips.csv, fuel_purchases.csv, delivery_events.csv, drivers.csv
**Additional data needed:** idle-time / hard-braking telematics data would make the driving-behavior angle much stronger; currently MPG variance across drivers is modest (6.70-6.85 range) since it's mostly truck-driven, so this app's value depends partly on data not yet collected

**Problem solved:**
Individual drivers have no visibility into how their fuel efficiency and on-time performance compare to peers. While the biggest MPG gaps are truck-driven (aging cohort), a smaller but real driver-level spread exists (worst drivers ~6.70-6.72 MPG vs. fleet 6.78), and on-time rate varies more meaningfully by driver (80.2% to mid-90s%), which is coachable behavior.

**What the app shows:**
- A personal dashboard (driver logs in / selects their ID): their MPG trend over time vs. fleet average, their on-time rate vs. fleet average
- A percentile ranking ("you're in the top 30% of the fleet for on-time performance") framed positively, not punitively
- A note distinguishing truck-driven vs. driver-driven efficiency where possible (e.g., flag if a driver's low MPG correlates with being assigned an aging-cohort truck, so they aren't blamed for equipment issues)
- Simple tips/benchmarks tied to the specific gap observed (e.g., on-time coaching for the ~15 drivers below 86% on-time)

**Key metric / headline number:**
Per-driver, personalized: e.g., "Your on-time rate is 84.9% — the fleet average is 88.4%. Closing that gap would put you in the top half of drivers."

**Build specification:**
- Group trips.csv by driver_id for avg_mpg and on_time_flag rate; join drivers.csv for name/terminal/tenure.
- Cross-reference truck_id assignments per driver (from trips.csv) against the aging-cohort list so the app can show "X% of your trips were in older trucks" as context for MPG performance — this avoids unfairly penalizing drivers who happen to draw TRK-047 often.
- Individual view: line chart of the driver's own MPG and on-time rate over time (monthly), with a fleet-average reference line overlaid for comparison.
- Percentile calculation: rank driver among all 165 for both metrics, display as "top X%" framing.
- Driver selector (dropdown or ID entry) simulates a login; in production this would be tied to actual driver auth.
- Keep tone entirely factual/neutral in copy — no red "you're bad" styling; use the dataviz skill's guidance on restrained, non-alarming color use for individual performance data.

**Success criteria:**
A driver should be able to see, in under 60 seconds, exactly how they compare to peers on the two things that affect their reputation and pay (efficiency, on-time), and whether equipment is a factor.

---

### App 07: Maintenance Cost & Replacement Planner

**Build ID:** app-07-maintenance-planner
**Audience:** fleet manager
**Category:** predictor
**Priority:** MEDIUM
**Data required:** trucks.csv, maintenance_records.csv, trips.csv
**Additional data needed:** new-truck purchase price and financing terms, and manufacturer-suggested service intervals, to make the replace-vs-repair math precise rather than illustrative

**Problem solved:**
There's no tool today that helps decide which of the aging-cohort trucks (or any truck) should be prioritized for replacement versus continued repair. Maintenance records exist but nobody is trending them into a forward-looking cost curve.

**What the app shows:**
- A cost-per-mile-by-age curve across the whole fleet, showing the sharp inflection point at ~14+ years (age-10 trucks run ~$0.0096/mile maintenance; age-14+ trucks run $0.09-$0.11/mile — roughly a 10x jump)
- Per-truck maintenance history: service_type breakdown (routine PM, brake system, cooling system, electrical, tire replacement, etc.) so recurring failure categories are visible
- A downtime-hours trend per truck, since downtime (not just cost) is an operational risk — a truck in the shop can't generate revenue
- A ranked "replace-first" list combining cost trajectory + downtime + current odometer, for budget planning conversations

**Key metric / headline number:**
"Maintenance cost per mile jumps 10x once a truck passes 13 years old — the 8 trucks past that line are running $354,000/year in excess maintenance combined."

**Build specification:**
- Compute truck age = current_year - year (acquisition year alternative also viable); merge with maintenance totals and total_miles from trips.csv.
- Build the age-vs-cost-per-mile curve (scatter or binned bar chart) exactly as computed in the underlying analysis — the inflection at age 14 is the key visual, make sure the x-axis spacing doesn't compress it.
- Per-truck service_type breakdown: stacked bar or small-multiples showing cost by category (routine PM vs. reactive repairs) — a truck dominated by reactive categories (brake, cooling, electrical) signals a different problem than one dominated by routine PM.
- Ranked list: sortable table by total_cost, downtime_hours, cost_per_mile, and current_odometer together, so the fleet manager can build a prioritized capex list.
- Layout: age-cost curve as the primary "why we're talking about this" chart at top, per-truck detail and ranked list below.

**Success criteria:**
The fleet manager should be able to build a data-backed capex request for replacing 3-5 trucks in under a few minutes of use, citing the specific cost curve as justification.

---

### App 08: Customer Profitability & Concentration Report

**Build ID:** app-08-customer-profitability
**Audience:** accountant
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** loads.csv, trips.csv, fuel_purchases.csv, customers.csv, delivery_events.csv
**Additional data needed:** driver pay per load/mile and fixed overhead allocation would allow a true fully-loaded margin per customer instead of margin-after-fuel-only

**Problem solved:**
Accounting has no single view combining revenue, margin-after-fuel, on-time performance, detention exposure, and payment terms per customer. TitanBolt is simultaneously the #3 revenue account, the worst detention offender, and on 45-day payment terms — three risk factors that compound but currently live in three different places.

**What the app shows:**
- A per-customer summary table: total revenue, % of company revenue, avg net-per-mile margin, on-time rate, avg detention minutes, payment terms — all eight customers on one screen
- A revenue-concentration chart (e.g., simple bar or treemap) showing Cascade Paper Products at 25.4% of revenue as the largest single-customer exposure
- A composite "account health" flag combining margin + detention + on-time into a simple traffic-light indicator per customer, so TitanBolt's combination of decent margin but terrible detention is visible at a glance rather than looking fine on revenue alone
- Payment-terms callout: TitanBolt and Peachtree Consumer Goods on 45-day terms vs. 30 days for the rest — relevant to cash-flow planning

**Key metric / headline number:**
"Cascade Paper Products represents 25.4% of total revenue — the largest single-customer concentration in the portfolio. TitanBolt (14.6% of revenue) carries the worst detention profile in the fleet."

**Build specification:**
- Aggregate loads.csv + trips.csv + fuel_purchases.csv + delivery_events.csv by customer_id, joined to customers.csv for terms/industry/location.
- Table columns: customer_name, loads, total_revenue, pct_of_revenue, avg_net_per_mile, on_time_rate, avg_detention_min, payment_terms_days.
- Concentration chart: simple horizontal bar sorted by pct_of_revenue is sufficient and clearer than a treemap for only 8 customers — prefer the simpler form per the dataviz skill's guidance to use the least complex chart that shows the pattern.
- Composite health flag: define simple thresholds (e.g., green/yellow/red) for margin, on-time, and detention, then combine into one flag column — make the thresholds visible/editable so accounting can adjust what counts as "at risk."
- Sort/filter by any column so accounting can re-rank by whichever concern is top of mind that week (margin this month, detention next month).

**Success criteria:**
An accountant should be able to identify, within 60 seconds, which customers are both large and risky (not just large or just risky) — informing which accounts merit a rate or terms renegotiation conversation.

---

### App 09: Load Acceptance Decision Helper

**Build ID:** app-09-load-acceptance-helper
**Audience:** dispatcher
**Category:** calculator
**Priority:** MEDIUM
**Data required:** routes.csv, loads.csv, trips.csv, fuel_purchases.csv, customers.csv (historical data to build reference rates)
**Additional data needed:** a live fuel price feed and current spot-market rate data would turn this from a historical-reference tool into a real-time decision tool

**Problem solved:**
Dispatch currently accepts loads lane-by-lane without a quick reference for "is this a good rate for this lane, for this customer, right now." A dispatcher taking a Seattle-Atlanta load has no easy way to see that the lane historically nets $1.30-1.39/mile against a $2.05 target before committing a truck to it.

**What the app shows:**
- A simple input form: select origin/destination (or route), customer, offered rate per mile
- An instant comparison against historical average net-per-mile for that exact lane and that exact customer, with a clear "below/above breakeven" verdict
- Context: current fuel price trend (rising ~$0.01-0.02/month over the data period) factored into the fuel-cost estimate for the comparison
- A short historical reference panel showing the same lane's last N loads' actual margins, so the dispatcher isn't relying on a single blended average

**Key metric / headline number:**
Dynamic per query: e.g., "This rate nets an estimated $1.35/mile after fuel — $0.70 below the $2.05 breakeven target for this lane."

**Build specification:**
- Precompute historical avg net_per_mile and avg fuel cost per mile by route_id (and optionally by route_id + customer_id) from the merged trips/loads/fuel tables — this is the same aggregation as App 03, reusable.
- Build a simple form: dropdowns for origin/destination (mapped to route_id) and customer, a numeric input for offered rate, and a fuel-price-per-gallon input pre-filled with the most recent observed price from fuel_purchases.csv.
- Calculation: estimated net-per-mile = offered_rate + estimated_fuel_surcharge - (distance_miles/assumed_mpg_for_lane * fuel_price) / distance_miles, compared against the $2.05 breakeven (editable).
- Verdict output: simple, unambiguous accept/caution/reject-style framing based on the breakeven comparison — but avoid literally telling the dispatcher what to do; show the number and let them decide.
- Historical panel: small table of the last 10-20 actual loads on that route (and customer if selected) with their realized net-per-mile, so the estimate has visible grounding in real outcomes.
- Layout: form at top, verdict/headline result prominent immediately below, historical reference table at the bottom.

**Success criteria:**
A dispatcher should be able to type in a rate and get a clear go/no-go signal, grounded in real historical data for that exact lane, in under 30 seconds — before committing a truck.

---

### App 10: Fleet On-Time Performance Explorer

**Build ID:** app-10-ontime-explorer
**Audience:** dispatcher
**Category:** dashboard
**Priority:** LOW
**Data required:** trips.csv, delivery_events.csv, loads.csv, routes.csv, customers.csv, drivers.csv
**Additional data needed:** none

**Problem solved:**
On-time performance varies meaningfully by customer (82.4%-90.2%), by lane (81.9%-91.3%), and by driver (80.2%-95%+), but there's no cross-cutting tool to explore whether a given customer's low on-time rate is actually a lane problem, a detention problem, or a driver-assignment problem in disguise.

**What the app shows:**
- Three linked views (customer, lane, driver) of on-time rate, each sortable/filterable
- A drill-down that shows, for the two worst-performing customers (Peachtree Consumer Goods 82.4%, Pioneer Home Furnishings 83.3%), which lanes and which facility types their loads run through — checking whether it's really a customer issue or a lane issue bleeding into the customer number
- A correlation view cross-referencing on-time rate against detention minutes, since delivery_events.csv links both — testing whether low on-time is actually being caused by dock delays rather than driver lateness
- Monthly on-time trend overlay to separate persistent issues from one-off bad months

**Key metric / headline number:**
"Peachtree Consumer Goods has the fleet's lowest on-time rate (82.4%) — cross-referencing against detention and lane data determines whether this is a customer-side or route-side problem."

**Build specification:**
- Compute on_time_flag rate grouped independently by customer_id, route_id, and driver_id from the merged trip/load/route tables.
- Build three ranked bar charts (or one chart with a dimension selector) — reuse consistent axis scaling (0-100%) across all three so comparisons are visually fair.
- Cross-reference: for the worst 2 customers, break down their on_time_rate further by route_id to isolate whether specific lanes are dragging their average down.
- Scatter plot: detention_minutes (x) vs. on_time (derived as 0/1, aggregated to rate) at the load level, to visually test correlation between dock delay and lateness.
- Filter/selector to switch the "worst performers" drill-down between any customer, not just the two flagged here.
- Layout: three-way comparison up top (tabs or side-by-side), drill-down and correlation view below.

**Success criteria:**
A dispatcher investigating "why is this customer's on-time rate low" should be able to determine whether the root cause is lane-related, detention-related, or driver-related within about a minute.

---

### App 11: Fuel Cost Forecast & Budget Tracker

**Build ID:** app-11-fuel-forecast
**Audience:** accountant
**Category:** predictor
**Priority:** LOW
**Data required:** fuel_purchases.csv, trips.csv, loads.csv
**Additional data needed:** a fuel hedging or surcharge-recovery policy, if one exists, to compare actual fuel-surcharge revenue collected against actual fuel cost incurred

**Problem solved:**
Fuel price per gallon has risen steadily from ~$3.93 (Jul 2024) to ~$4.27 (Jun 2026), a ~9% increase over the data window, with no current tool tracking whether fuel-surcharge revenue collected from customers is keeping pace with actual fuel cost incurred.

**What the app shows:**
- Monthly average fuel price paid and total fuel spend, trended over the full data history
- A side-by-side comparison of fuel_surcharge revenue collected (from loads.csv) vs. actual fuel cost incurred (from fuel_purchases.csv) by month — testing whether the surcharge mechanism is keeping up
- A simple linear trend projection for the next 3-6 months of fuel price, to inform budget conversations
- Fuel cost per mile trend by truck-age cohort, connecting this app back to the aging-fleet finding (older trucks' fuel cost grows faster as a share of spend)

**Key metric / headline number:**
"Fuel surcharge revenue has covered X% of actual fuel cost over the past 12 months" (exact percentage computed from the data — this is the single most decision-relevant number for accounting's margin planning).

**Build specification:**
- Group fuel_purchases.csv by month for avg price_per_gallon and total_cost; group loads.csv by month for total fuel_surcharge collected.
- Primary chart: dual-line chart (price per gallon trend) with a secondary panel comparing total surcharge collected vs. total fuel cost incurred per month — use two clearly distinguished line colors per the dataviz skill, not red/green (this isn't a good/bad binary, it's two related quantities).
- Simple trend line/projection: linear regression on monthly avg price_per_gallon extended 3-6 months forward, clearly labeled as a projection, not a forecast guarantee.
- Cohort cut: fuel cost per mile for the aging cohort (TRK-041-048) vs. rest of fleet, trended monthly, tying back to App 01/07's findings.
- Layout: price trend and projection at top, surcharge-vs-cost comparison below, cohort cut as a supplementary panel.

**Success criteria:**
An accountant should be able to answer "are we keeping up with fuel cost through surcharges, and where is this headed next quarter" within 60 seconds.

---

### App 12: New Terminal Onboarding Health Check (Workflow Tool)

**Build ID:** app-12-onboarding-workflow
**Audience:** owner
**Category:** workflow tool
**Priority:** LOW
**Data required:** drivers.csv
**Additional data needed:** This app's real value requires data the company doesn't currently have: exit interview reasons, onboarding checklist completion, home-time logs, and pay-per-mile by terminal. Without that, this is a lightweight tracking shell rather than a diagnostic tool — flagged as lower priority for that reason.

**Problem solved:**
Once the Chicago retention problem (App 04) is confirmed as terminal-specific, there's currently no repeatable process for monitoring a new hiring cohort's early-tenure health before it turns into another 61.9%-termination situation — useful now for Chicago's recovery and for any future terminal expansion.

**What the app shows:**
- A cohort tracker: for any home_terminal + hire_year combination, live termination rate and tenure-to-date, updated as new data comes in
- An early-warning threshold: if a cohort's termination rate within its first 12 months exceeds a configurable threshold (e.g., 2x the fleet average), it's flagged automatically
- A simple checklist/notes area (manual entry) for tracking onboarding process changes made in response to the Chicago finding, so future cohorts can be compared against "before and after the fix"

**Key metric / headline number:**
"Current cohort termination rate vs. threshold" — e.g., "Chicago 2026 hires: 1 of 1 still active (0% termination) — too early to assess, monitor through month 12."

**Build specification:**
- Group drivers.csv by home_terminal and hire_year; compute rolling termination rate and average tenure-in-months-to-date for each cohort.
- Build a simple monitoring table: one row per terminal+year cohort, columns for headcount, active count, terminated count, termination rate, and a flag if the rate exceeds a configurable multiple of the fleet baseline.
- This is intentionally a lightweight, low-data-dependency tool — be upfront in the UI that predictive power is limited until more descriptive fields (exit reasons, pay, home-time) are added; include a visible note to that effect rather than overstating what the tool can diagnose.
- Manual notes field: simple free-text or structured log per cohort, stored client-side or in a simple flat file, for tracking interventions.
- Layout: cohort monitoring table as the primary view, flagged cohorts highlighted at the top.

**Success criteria:**
Renee should be able to check, at any point in the year, whether a new hiring cohort at any terminal is trending toward another Chicago-2023-style outcome before it fully plays out — early enough to intervene.

---
