# Blue Heron Cold Chain — App Ideas

Generated: 2026-07-02
Analyst findings: Blue Heron's business is a tale of two trucks and two directions. TRK-01 (Dale's 2016 Freightliner, 766K miles) burns fuel 26% less efficiently than TRK-02 (Renata's 2021 Kenworth) and racks up 3x the maintenance downtime, while northbound backhaul freight nets 44% less per mile than southbound loads and misses a reasonable breakeven on over a third of trips. Layered on top, receiver Golden Gate Fresh Distributors — the company's highest-volume delivery point — holds trucks 43.8 minutes on average (vs. ~9-14 minutes everywhere else) and is on time only 4.5% of the time, quietly costing thousands in detention that's currently uncollected and untracked.

---

## Primary Pain Points Discovered

1. **TRK-01 fuel inefficiency costs ~$280+/round trip.** TRK-01 (2016 Freightliner Cascadia, Dale, 766K mi) averages 5.18 MPG vs. TRK-02's (2021 Kenworth T680, Renata, 446K mi) 7.01 MPG — a 26% gap on the same lanes. On a typical ~680-mile southbound leg, that's an estimated $529.88 in fuel for TRK-01 vs. $389.78 for TRK-02 — roughly $140/leg, ~$280/round trip, or an estimated $50,000+/year if TRK-01 runs a similar load pattern to TRK-02 all year.

2. **Golden Gate Fresh Distributors (Oakland, CA) is a detention black hole.** Average detention is 43.84 minutes per stop — 5x the ~9 minute average at every other customer — with a max of 75 minutes. Across 112 delivery events, that's 81.8 hours of detention (~$5,300 at a conservative $65/hr all-in truck+driver cost), and remarkably, on-time performance there is only 4.46% (vs. 82-90% at all other customers), suggesting the delay is baked into how the facility operates, not an occasional bad day.

3. **Northbound backhaul freight is structurally thin-margin.** Northbound trips (Oakland/Portland → WA) average $1.70/mile revenue and $1.02/mile net margin vs. southbound's $3.05/mile revenue and $2.37/mile net margin — less than half the profitability per mile. 37.6% of all northbound trips fall below a $1.65/mile threshold, meaning over a third of the fleet's return trips are running at or near breakeven.

4. **TRK-01's maintenance burden is rising and already 2-3x TRK-02's.** TRK-01 logged 13 service events totaling $18,253.58 (avg $1,404/event) and 210.8 hours of downtime, vs. TRK-02's 9 events totaling $9,679.29 (avg $1,075/event) and 71.3 hours of downtime — roughly 3x the downtime on top of the fuel penalty. TRK-01's second-half-of-data average cost ($1,463) and downtime (16.8 hrs) are both trending up, while TRK-02's are trending down ($933, 6.3 hrs) — the two trucks are moving in opposite directions.

5. **Customer revenue concentration risk.** Three customers — Bellingham Cold Storage (22.8%), Cascade Berry Growers (20.5%), and Golden Gate Fresh Distributors (19.8%) — account for 63% of total revenue. Golden Gate is both a top-3 revenue customer and the worst detention offender, meaning Blue Heron can't easily walk away from the relationship causing them the most pain.

---

## App Ideas

### App 01: Truck Cost & Fuel Efficiency Command Center

**Build ID:** app-01-truck-cost-command-center
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** trips.csv, fuel_purchases.csv, maintenance_records.csv, trucks.csv
**Additional data needed:** none

**Problem solved:**
Dale and Renata "sense" that TRK-01 costs more to run than TRK-02 but have never seen it as one number. This app puts fuel cost, MPG, and maintenance cost side-by-side per truck so they can decide whether to keep running TRK-01, budget for major repairs, or start shopping for a replacement.

**What the app shows:**
- Side-by-side truck cards (TRK-01 vs TRK-02) with big-number MPG, $/mile fuel cost, and $/mile maintenance cost
- A trend line of MPG over time per truck (flat/stable vs. degrading)
- A trend line of maintenance cost and downtime hours per truck, month over month
- A "total cost of ownership per mile" combined metric (fuel + maintenance) per truck
- A callout translating the MPG gap into a projected annual dollar cost

**Key metric / headline number:**
"TRK-01 is costing an estimated $280+ more per round trip in fuel alone than TRK-02 — plus 3x the maintenance downtime."

**Build specification:**
- Join trips.csv (miles, mpg, truck_id) with fuel_purchases.csv (aggregate total_cost and gallons by trip_id) to get per-trip fuel cost and cost/mile.
- Join maintenance_records.csv by truck_id, bucket by month, to build a maintenance cost and downtime trend.
- Compute a rolling 3-month average MPG per truck to smooth noise and show trend direction (use trips.csv actual_mpg).
- Headline callout: hardcode the comparison logic (not per-truck-agnostic) since this is a 2-truck fleet — directly reference "TRK-01 (Dale)" and "TRK-02 (Renata)" by name in the UI, not just IDs.
- Chart 1: bar comparison of avg MPG, southbound-only (to control for load weight/direction) — TRK-01 vs TRK-02.
- Chart 2: dual line chart, cost/mile (fuel) over time per truck.
- Chart 3: stacked bar of maintenance cost by service_type per truck (to show what's driving TRK-01's higher spend — brakes, tires, air system are visibly rising in the back half of the data).
- Add a "cost of keeping TRK-01" annualized projection box: extrapolate the average round-trip fuel delta × estimated annual round trips.
- Layout: top row = two big KPI cards (per truck), middle = MPG trend chart, bottom = maintenance cost/downtime trend chart with service-type breakdown.
- No filters needed beyond a date range selector — this is a 2-truck company, keep it simple.

**Success criteria:**
Dale or Renata should be able to open this and, within 60 seconds, state the dollar difference in fuel and maintenance cost between the two trucks and see whether TRK-01's costs are getting worse over time.

---

### App 02: Lane & Direction Profitability Explorer

**Build ID:** app-02-lane-profitability
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, routes.csv, trips.csv, fuel_purchases.csv, customers.csv
**Additional data needed:** none

**Problem solved:**
Blue Heron intuitively knows southbound loads (Skagit/Bellingham/Burlington → Portland/Oakland) pay well and northbound backhauls are a scramble, but they've never quantified the gap. This app isolates margin by route and by direction so they can decide whether to be pickier about load-board freight or push southbound customers for rate increases that offset the empty-mile-heavy return trip.

**What the app shows:**
- A route-level table/bar chart ranked by net margin per mile (fuel-cost-adjusted), from best (RTE-03 Burlington→Oakland at $2.58/mi) to worst (RTE-07 Oakland→Burlington at $0.95/mi)
- A southbound vs. northbound-backhaul comparison: revenue/mile, net margin/mile, and trip count
- A "% of northbound trips below breakeven" stat with a definable threshold slider
- Monthly trend of northbound backhaul margin to see if it's getting better or worse
- Highlight of which routes are load-board sourced (low, inconsistent rate) vs. core customer lanes

**Key metric / headline number:**
"Northbound backhauls net $1.02/mile vs. $2.37/mile southbound — less than half — and 37.6% of northbound trips run below a reasonable $1.65/mile breakeven."

**Build specification:**
- Merge loads.csv → routes.csv (route_id) → trips.csv (load_id) → aggregated fuel cost per trip.
- Compute rev_per_mile = (revenue + fuel_surcharge) / actual_miles, and net_margin_per_mile = rev_per_mile minus fuel_cost/actual_miles.
- Tag each route as "southbound" or "northbound_backhaul" using origin_state (WA-origin = southbound).
- Chart 1: horizontal bar chart of all 7 routes sorted by avg net margin/mile, color-coded by direction (use a two-color categorical scheme — southbound vs. backhaul — per the dataviz skill's categorical palette guidance).
- Chart 2: big KPI comparison cards — southbound avg $/mile vs. northbound avg $/mile, plus total dollars earned each direction over the data period.
- Include a breakeven threshold slider (default $1.65/mile) that recalculates "% of northbound trips below breakeven" live — this is the one interactive element that adds real decision value (Dale/Renata can test their own breakeven assumption).
- Table underneath: route, origin→destination, trip count, avg rev/mile, avg net margin/mile, total net margin — sortable.
- Callout box: translate the margin gap into an annual dollar figure (northbound trip count × the per-mile gap × avg miles).
- Layout: KPI cards top, direction comparison chart + breakeven slider middle, full route table bottom.

**Success criteria:**
User can identify, in under 60 seconds, which specific route is the worst performer and roughly how many dollars a year the northbound/southbound margin gap represents.

---

### App 03: Golden Gate Detention Tracker & Leverage Report

**Build ID:** app-03-detention-tracker
**Audience:** owner
**Category:** tracker
**Priority:** HIGH
**Data required:** delivery_events.csv, loads.csv, customers.csv, trips.csv
**Additional data needed:** none

**Problem solved:**
Dale and Renata dread the Golden Gate Fresh Distributors (Oakland) stop but have never had a dollar figure to bring to a rate or accessorial conversation. This app turns detention minutes into a running dollar total specifically callable-out for Golden Gate, giving them hard evidence instead of a shared frustration.

**What the app shows:**
- A per-customer detention leaderboard (avg minutes, event count, total hours) with Golden Gate visibly at the top
- A running/cumulative dollar total of estimated detention cost attributable to Golden Gate, using a configurable hourly rate
- A distribution/histogram of Golden Gate detention times vs. all-other-customers detention times, showing how far outside normal Golden Gate sits
- A monthly trend of Golden Gate detention to show whether it's improving, worsening, or steady
- An "on-time at delivery" comparison: Golden Gate's 4.46% on-time rate vs. 82-90% everywhere else

**Key metric / headline number:**
"Golden Gate Fresh Distributors has cost Blue Heron an estimated $5,300+ in detention time — 5x the fleet's average wait at every other stop."

**Build specification:**
- Join delivery_events.csv to loads.csv (load_id) to customers.csv (customer_id) to attribute every detention_minutes value to a customer.
- Compute per-customer: event count, avg detention minutes, total detention hours, and on_time rate (from delivery_events.on_time).
- Add an editable hourly-rate input (default $65/hr, labeled clearly as "estimated truck + driver cost per hour") that recalculates estimated dollar cost live — this is the single most important interactive element since the rate is a judgment call Dale/Renata should control before using this number externally.
- Chart 1: bar chart, all 6 customers ranked by avg detention minutes — Golden Gate should visually dominate.
- Chart 2: histogram or box plot comparing Golden Gate's detention_minutes distribution against the combined distribution of all other customers.
- Chart 3: monthly line chart of Golden Gate avg detention minutes over the data period, to show whether it's a consistent pattern (supports a "this isn't a one-off" argument).
- Prominent callout box formatted like a one-page leverage brief: "112 deliveries, 81.8 total hours of detention, $X,XXX estimated cost at $Y/hr" — written so it could be screenshotted and shown to Golden Gate's traffic manager.
- Layout: headline dollar callout at top, customer leaderboard bar chart, Golden Gate distribution comparison, monthly trend at bottom.

**Success criteria:**
User can find, in under 60 seconds, a specific dollar figure and event count they could put in an email to Golden Gate Fresh Distributors asking for a detention accessorial fee or better dock scheduling.

---

### App 04: Weekly Owner Scorecard

**Build ID:** app-04-weekly-owner-scorecard
**Audience:** owner
**Category:** dashboard
**Priority:** HIGH
**Data required:** loads.csv, trips.csv, fuel_purchases.csv, delivery_events.csv, maintenance_records.csv

**Additional data needed:** none

**Problem solved:**
Dale and Renata run the business by feel — checking bank balances and trip logs piecemeal. This is a one-page, always-current view of "how did we do this week/month" that condenses everything else in this suite into a single sanity check, so they don't have to open five different apps to know if the business is healthy.

**What the app shows:**
- This week/this month vs. prior period: total loads, total revenue, net margin (after fuel), avg rev/mile
- A single "fleet health" strip: TRK-01 vs TRK-02 MPG this period, any maintenance events this period
- A single "customer watch" strip: on-time rate and detention minutes for Golden Gate this period vs. baseline
- A simple up/down/flat trend arrow next to each metric versus the prior period
- A short auto-generated plain-English callout, e.g., "Revenue up 8% this month, driven by more southbound loads. TRK-01 fuel cost per mile is up 4% — worth a look."

**Key metric / headline number:**
"Net margin this month: $X — {up/down}% vs. last month."

**Build specification:**
- Aggregate loads/trips/fuel/events/maintenance by week and by month; default view = current month vs. prior month, with a toggle for week vs. month.
- Compute the same metrics used in Apps 01-03 but rolled up to single current-period numbers with a delta vs. prior period (%, and up/down arrow icon).
- The "auto-generated callout" doesn't need real NLG — use a simple rules engine (e.g., if fuel cost/mile change > 3%, surface a sentence; if Golden Gate detention this period > baseline, surface a sentence) rendered as 1-3 template sentences, not a chart.
- Layout: single page, 4-6 KPI tiles across the top (loads, revenue, net margin, rev/mile), a fleet health row (2 truck mini-cards), a customer watch row (Golden Gate mini-card), and the plain-English summary as a text block beneath.
- Keep this the "front door" — link out conceptually to Apps 01, 02, 03 for drill-down (label tiles like they could be clicked, even if this is a standalone Streamlit page for now).
- No complex filters — a single period selector (this week / this month / this quarter) is enough.

**Success criteria:**
User opens the app on a Monday morning and knows within 60 seconds whether the business had a good or bad week and what (if anything) needs attention.

---

### App 05: Driver Earnings & Performance View

**Build ID:** app-05-driver-earnings-performance
**Audience:** driver
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** trips.csv, fuel_purchases.csv, loads.csv, delivery_events.csv, drivers.csv

**Additional data needed:** Driver pay structure (per-mile rate, percentage of load, or salary) — not present in current data, needed to show actual take-home earnings rather than just revenue generated.

**Problem solved:**
Since Dale and Renata are both owners and drivers, this reframes the same underlying truck/fuel data specifically as personal performance — so each of them can see "my truck, my numbers" without wading through fleet-wide comparisons that are really about equipment, not driving. It also builds the scaffolding for if/when Blue Heron hires a third driver.

**What the app shows:**
- Personal MPG trend over time with a fleet-average reference line
- Personal on-time delivery rate trend
- Loads hauled this month/quarter and revenue generated
- A "your truck's fuel cost per mile" card so a driver sees their number without it being framed as a fault
- Simple month-over-month comparison of their own performance (not compared against the other driver, to avoid framing this as Dale vs. Renata)

**Key metric / headline number:**
"You've hauled {N} loads this month, averaging {X} MPG and {Y}% on-time."

**Build specification:**
- Filter trips.csv/fuel_purchases.csv/delivery_events.csv by driver_id, selected via a simple dropdown or login-style selector (DRV-01 / DRV-02).
- Compute MPG trend (monthly avg actual_mpg), on-time rate trend (from on_time_flag in trips.csv, or on_time in delivery_events.csv joined via load_id), and load count over time.
- Show fleet-wide average as a light reference line on the MPG chart so the driver has context without an explicit "you vs. them" framing.
- Since pay data isn't available, clearly label revenue metrics as "revenue generated" rather than "earnings," and add a note in the UI that per-load pay isn't yet tracked — this keeps the app honest about what it can and can't show.
- Layout: driver selector at top, 3 KPI cards (loads, MPG, on-time%), MPG trend chart with fleet reference line, on-time trend chart below.
- Keep tone informational/neutral, not evaluative — this is as much for Dale and Renata to see their own numbers as it is a "performance review" tool.

**Success criteria:**
A driver can see, in under 60 seconds, how their fuel efficiency and on-time rate this month compare to their own recent history.

---

### App 06: Maintenance Cost & Replace-vs-Repair Calculator

**Build ID:** app-06-replace-vs-repair-calculator
**Audience:** fleet manager
**Category:** calculator
**Priority:** MEDIUM
**Data required:** maintenance_records.csv, trucks.csv, trips.csv, fuel_purchases.csv

**Additional data needed:** Estimated resale/trade-in value of TRK-01, financing terms/monthly payment for a replacement truck, and current loan payoff (if any) — needed to make a true replace-vs-keep financial comparison rather than just showing rising costs.

**Problem solved:**
TRK-01 is 10 years old with 766K+ miles and both maintenance cost and downtime are trending up. Dale and Renata need more than "it's getting expensive" — they need a side-by-side projection of what keeping TRK-01 costs over the next 1-3 years (fuel + maintenance) vs. what a replacement truck payment would cost, so the trade-in decision is a number, not a gut call.

**What the app shows:**
- TRK-01's maintenance cost and downtime trend over the full data period, annotated by odometer reading (cost tends to climb past 600K miles)
- A "cost per 1,000 miles" trend line to normalize maintenance spend against how much the truck is actually driven
- An interactive calculator: input estimated new/used truck monthly payment + estimated new-truck MPG, and see a projected 12/24/36-month total cost of "keep TRK-01" vs. "replace TRK-01," combining current fuel-cost trajectory and maintenance-cost trajectory
- A service-type breakdown showing which systems are driving the increase (brakes, tires, air system, transmission all show up on TRK-01 in the trailing months)

**Key metric / headline number:**
"At current trends, keeping TRK-01 running is projected to cost $X more than a replacement payment over the next 12 months."

**Build specification:**
- From maintenance_records.csv, compute a linear or rolling trend of cost and downtime_hours over time, and normalize by odometer delta between services to get cost-per-1000-miles.
- Chart 1: dual-axis or small-multiple line chart of maintenance cost and downtime hours over time for TRK-01, with odometer_at_service shown as x-axis secondary labels or a marker annotation at the 600K-mile mark.
- Chart 2: bar chart of total cost by service_type for TRK-01 (brakes, tires, air system, transmission service cluster in the back half of the dataset — make this visually obvious).
- Calculator section: user inputs (1) estimated monthly payment for a replacement truck, (2) expected MPG of a replacement (default to TRK-02's 7.01 MPG as a reasonable proxy since it's a comparable modern reefer tractor), (3) projection horizon (12/24/36 months dropdown).
- Calculation: "cost to keep" = projected fuel cost (current TRK-01 MPG × projected annual miles × fuel price) + projected maintenance cost (extrapolated from the cost/1000-miles trend). "Cost to replace" = monthly payment × months + projected fuel cost at new MPG. Show the delta clearly.
- Because financing/trade-in data isn't in the dataset, clearly label these as user-adjustable assumptions, not derived facts — style the input fields distinctly (e.g., a bordered "your assumptions" panel) from the data-driven charts above.
- Layout: trend charts top, service-type breakdown middle, interactive calculator panel at bottom as the primary call-to-action.

**Success criteria:**
User can plug in a real truck payment quote and get a clear "keep vs. replace" dollar comparison in under a minute, without needing a spreadsheet.

---

### App 07: Customer Profitability & Payment Terms Report

**Build ID:** app-07-customer-profitability-report
**Audience:** accountant
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** loads.csv, customers.csv, trips.csv, fuel_purchases.csv

**Additional data needed:** Actual accounts-receivable / invoice payment dates would sharpen this further (payment_terms_days is contractual, not actual paid-on time data) — none required to ship a first version.

**Problem solved:**
Blue Heron's revenue is concentrated in three customers (63% of revenue across Bellingham Cold Storage, Cascade Berry Growers, and Golden Gate) and payment terms range from 15 to 45 days. Renata, who runs the books, needs one place that ranks customers by true profitability (not just revenue) and flags cash-flow exposure from longer payment terms.

**What the app shows:**
- Customer ranking table: loads, total revenue, net margin (after fuel), avg net margin/mile, % of total revenue, payment terms
- A revenue concentration donut/bar showing the 63% concentration in the top 3 customers
- A "days of revenue outstanding" style exposure metric: payment_terms_days × average monthly revenue from that customer, to show how much cash is tied up at any time (e.g., Golden Gate's 45-day terms on ~$257K/year revenue)
- A margin-per-mile comparison highlighting that Golden Gate, despite being a strong revenue customer, nets less per mile than Cascade Berry Growers or Bellingham Cold Storage due to the detention drag

**Key metric / headline number:**
"Golden Gate Fresh Distributors: 45-day payment terms tie up an estimated $X in outstanding receivables at any given time — the longest terms of any customer."

**Build specification:**
- Merge loads.csv → customers.csv → trips.csv/fuel_purchases.csv to compute per-customer revenue, net margin, and net margin/mile (reuse logic from App 02/03).
- Compute a simple receivables-exposure estimate: (annual revenue from customer / 365) × payment_terms_days = average outstanding balance at any time. Present this per customer, sorted descending.
- Chart 1: horizontal bar, customers ranked by total revenue, colored/annotated with payment_terms_days so the eye connects big-revenue customers to how long the cash takes to arrive.
- Chart 2: table combining revenue rank, net margin/mile rank, and payment terms — sortable by any column, so accounting can toggle between "who pays us the most" and "who is actually most profitable per mile."
- Callout: flag any customer that is both high-revenue AND slow-pay AND low-margin-per-mile (Golden Gate fits two of three — high revenue, slow pay, is margin-diluted by detention even though its raw $/mile isn't the worst).
- Layout: concentration chart top, receivables exposure chart middle, full sortable customer table bottom.

**Success criteria:**
Renata can determine, in under 60 seconds, which customer ties up the most cash and whether that customer is worth the exposure given their actual profitability.

---

### App 08: On-Time Performance & Reliability Dashboard

**Build ID:** app-08-on-time-reliability-dashboard
**Audience:** dispatcher
**Category:** dashboard
**Priority:** MEDIUM
**Data required:** trips.csv, delivery_events.csv, loads.csv, customers.csv

**Additional data needed:** none

**Problem solved:**
Blue Heron's whole pitch to customers is reliability ("a driver who actually shows up on time"), but there's no current view of whether that promise is being kept. This app tracks on-time performance by customer, by route, and over time so Dale/Renata can catch a slipping trend before a customer notices it first.

**What the app shows:**
- Overall fleet on-time rate with a trend line over the data period (ranges roughly 77-90% month to month with no clear seasonal pattern — worth surfacing as "we hover around 85%, is that acceptable?")
- On-time rate by customer, side by side with each customer's avg detention (to separate "we were late" from "we were held at the dock")
- On-time rate by route
- A simple "misses" table: the worst individual late-delivery events (largest gap between scheduled_time and actual_time) with customer and date, so patterns can be spotted (e.g., repeated late arrivals to a specific place/day)

**Key metric / headline number:**
"Fleet-wide on-time rate is {X}% over the trailing 12 months — down from {Y}% a year ago" (direction depends on latest trend computation).

**Build specification:**
- Compute on_time_flag rate from trips.csv monthly, plot as a line chart with a horizontal reference line at a target (e.g., 90%, adjustable).
- Join delivery_events.csv to loads.csv to customers.csv to get on-time rate AND avg detention per customer — display as a two-metric grouped bar chart (on-time % as bars, detention minutes as a secondary line) so a viewer can see Golden Gate is both late-averse to fix (low on-time) and slow to unload (high detention) — two distinct problems, not one.
- Route-level on-time bar chart, sortable.
- "Worst misses" table: compute (actual_time - scheduled_time) in minutes from delivery_events.csv, sort descending, show top 15-20 with load_id, customer, date, and minutes late.
- Layout: trend line top with target reference, customer on-time/detention combo chart middle, route bar chart and worst-misses table side by side or stacked at bottom.
- Add a date-range filter since this is the kind of dashboard that's useful to check quarterly.

**Success criteria:**
Dispatcher (Renata, in practice) can see in under 60 seconds whether reliability is holding steady, which customer relationship is most at risk, and pull up specific dates/loads if a customer calls to complain.

---

### App 09: Load Acceptance Decision Helper

**Build ID:** app-09-load-acceptance-helper
**Audience:** dispatcher
**Category:** calculator
**Priority:** MEDIUM
**Data required:** routes.csv, loads.csv, trips.csv, fuel_purchases.csv

**Additional data needed:** Current live fuel price (could default to most recent known price from data) and a way to input a load-board-offered rate for a prospective load, which isn't in the historical data by definition.

**Problem solved:**
When a load-board backhaul offer comes in, Dale or Renata currently has to eyeball whether it's worth taking. This is a fast go/no-go calculator: type in the offered rate and miles, and get an instant read on whether it clears history-based breakeven, using this company's own historical cost data instead of a rule of thumb.

**What the app shows:**
- An input form: origin/destination (or miles), offered rate ($ total or $/mile), which truck would run it
- An instant net-margin-per-mile estimate using that truck's actual historical MPG and current fuel price
- A comparison against this company's own historical average for that direction (northbound backhaul historical avg $1.02/mile net margin) so the offer is graded against Blue Heron's own real data, not a generic benchmark
- A clear accept/marginal/reject visual signal with the reasoning shown (not a black box)

**Key metric / headline number:**
"This load nets an estimated $X/mile after fuel — {above/below} your historical northbound average of $1.02/mile."

**Build specification:**
- Pre-load each truck's historical avg MPG (TRK-01: 5.18, TRK-02: 7.01, computed from trips.csv) and most recent fuel price (from fuel_purchases.csv, latest purchase_date) as defaults, but let the user override fuel price for a live quote.
- Form inputs: miles (numeric), offered total rate or $/mile (toggle), truck selector (TRK-01/TRK-02).
- Calculation: fuel_cost_estimate = miles / truck_mpg × fuel_price; net_margin_per_mile = (offered_rate / miles) - (fuel_cost_estimate / miles) [or directly if $/mile entered].
- Compare result against stored historical benchmarks (southbound avg net margin/mile $2.37, northbound avg $1.02) pulled from the analysis in App 02, displayed as reference lines/bands.
- Visual signal: green ("clears southbound-tier margin"), yellow ("in line with historical backhaul average"), red ("below historical backhaul average — likely losing money"), using thresholds derived from the actual data quartiles, not arbitrary values.
- Show the math transparently in a small breakdown table beneath the result (miles, fuel cost, net revenue, net margin/mile) so it builds trust rather than feeling like a black box.
- Layout: form on the left/top, big color-coded result callout on the right/below, transparent math breakdown at the very bottom.

**Success criteria:**
A dispatcher can type in a load-board offer and get a clear accept/reject signal grounded in this company's own historical margins in under 30 seconds — fast enough to use while on the phone with a broker.

---

### App 10: Fleet Utilization & Idle Capacity Tracker

**Build ID:** app-10-fleet-utilization-tracker
**Audience:** owner
**Category:** tracker
**Priority:** LOW
**Data required:** trips.csv, loads.csv

**Additional data needed:** Planned/available working days per driver (e.g., days off, home time policy) — without this, "idle" can only be inferred from gaps between trips, not confirmed as true downtime vs. planned rest.

**Problem solved:**
With only 2 trucks, every non-earning day matters. This app surfaces days/weeks where a truck wasn't moving loads, so Dale and Renata can see if there's meaningful idle capacity being left on the table (vs. it just reflecting reasonable home time).

**What the app shows:**
- A calendar-heatmap style view per truck showing days with a trip vs. days without
- Monthly trip count per truck, to spot slow months
- Average trips per week per truck, with a callout on weeks that fall notably below average
- A rough "potential revenue left on the table" estimate: idle days × average daily revenue per truck, clearly labeled as an estimate

**Key metric / headline number:**
"TRK-01 ran {N} fewer loads than TRK-02 over the last 12 months — a gap worth investigating."

**Build specification:**
- From trips.csv, derive trip dates (departure_time) per truck_id, and build a calendar heatmap (e.g., GitHub-contribution-style grid) per truck for the full data period.
- Compute monthly and weekly trip counts per truck; flag weeks more than 1 standard deviation below that truck's own average.
- Estimate "potential revenue left on table" using avg revenue per load for that truck × estimated idle days, but label this prominently as a rough estimate since planned time off isn't in the data (avoid implying idle time is always a problem).
- Layout: two calendar heatmaps stacked (one per truck) at top, monthly trip-count bar chart comparing both trucks below, flagged-low-weeks list at the bottom.
- Keep this app light-touch and exploratory rather than prescriptive, since the underlying "why" for any gap isn't knowable from this data alone.

**Success criteria:**
User can visually spot, in under 60 seconds, whether one truck has meaningfully more idle days than the other and roughly when those gaps occurred.

---

### App 11: Seasonal Revenue & Cash Flow Planner

**Build ID:** app-11-seasonal-cashflow-planner
**Audience:** owner
**Category:** dashboard
**Priority:** LOW
**Data required:** loads.csv, trips.csv, customers.csv

**Additional data needed:** Fixed monthly costs (insurance, truck payments, permits) would let this become a true cash-flow forecast rather than just a revenue-seasonality view.

**Problem solved:**
Load volume clearly dips in November-February (as low as 16-25 loads/month vs. 40-50 in peak months) tied to produce/berry seasonality. Dale and Renata likely feel this every winter but may not have a clean multi-year view to plan around it — e.g., building a cash reserve or lining up alternative freight before the seasonal dip hits.

**What the app shows:**
- Monthly load volume and revenue overlaid across the full data period, with the seasonal dip (Nov-Feb) visually obvious
- A freight-type breakdown by month (produce and seafood loads drop sharply in winter; backhaul/mixed freight is more stable) to show which revenue streams are seasonal vs. steady
- A projected "next 3 months" outlook based on the same period last year, simple year-over-year seasonal projection
- A "lean months" callout identifying which specific months historically run below the annual average

**Key metric / headline number:**
"November-February load volume runs {X}% below the annual average — plan for roughly ${Y} less revenue per lean month."

**Build specification:**
- Aggregate loads.csv by month and by freight_type to show the seasonal pattern already visible in the exploration (Refrigerated - Produce and Refrigerated - Seafood volumes drop sharply Nov-Feb; Backhaul Mixed is comparatively steadier).
- Chart 1: stacked area or grouped bar chart, monthly load volume by freight_type, full data period, so the seasonal produce/seafood dip is visually distinct from the steadier backhaul volume.
- Chart 2: monthly revenue line with a shaded band or marker for months that fall below the trailing-12-month average.
- Simple projection: for the next 3 calendar months, show the same months' actuals from the prior year as a naive forecast (label clearly as "based on last year, not a model").
- Callout box: list the specific historical lean months and the average revenue shortfall vs. the annual monthly average, in dollars.
- Layout: seasonal stacked chart top, revenue trend with lean-month shading middle, next-3-months naive projection and lean-months callout at bottom.

**Success criteria:**
User can identify, in under 60 seconds, which months are historically the leanest and roughly how much less revenue to expect, so they can plan savings or seek alternate freight ahead of time.

---
