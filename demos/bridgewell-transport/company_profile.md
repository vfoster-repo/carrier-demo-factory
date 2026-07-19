# Bridgewell Transport

**Type:** small_fleet
**Location:** Joplin, Missouri
**Founded:** 2014
**Owner:** Curtis Rainey
**Primary Freight:** Dry van
**Fleet Size:** 10 trucks, 14 drivers
**Tagline:** A four-corners Midwest hauler that grew out of a dispatch desk and still runs like one truck is always one bad week from trouble.

## Company Story

Curtis Rainey spent eleven years as a dispatcher for a regional LTL carrier in Springfield, Missouri before he scraped together enough credit to buy two used Freightliners in 2014 and start Bridgewell Transport out of a rented lot in Joplin. He picked Joplin on purpose — it sits inside a day's drive of Dallas, Little Rock, Kansas City, Tulsa, and Springfield, which let him build a dense regional network instead of chasing long-haul freight he couldn't service well with a small crew.

The company grew slowly and organically, adding a truck or two a year as Curtis picked up steady freight from building materials suppliers and agricultural cooperatives across the four-state region (Missouri, Arkansas, Oklahoma, Kansas). By 2019 the fleet had reached ten trucks, and it has held there since — Curtis has been reluctant to grow further without fixing what he calls "the leaks," a phrase he uses often and applies to almost everything from a rattling reefer unit to a driver who quit without notice.

Bridgewell hauls exclusively dry van freight: pallets of lumber, roofing supplies, and drywall for building materials customers, and bagged seed, feed, and fertilizer for ag customers. The company's four largest accounts are Ozark Building Supply (Joplin, MO), Route 66 Ag Cooperative (Tulsa, OK), Sooner State Lumber (Oklahoma City, OK), and Delta Farm & Feed (Little Rock, AR). These four shippers account for roughly 70% of Bridgewell's freight volume, which gives Curtis pricing leverage in theory but real exposure in practice — a slow month from any one of them shows up immediately in cash flow.

Curtis still dispatches himself most mornings out of a converted office next to the truck yard, working from a whiteboard and a handful of spreadsheets. He knows in his gut that certain trucks eat more fuel than they should, that one customer's dock crew is chronically slow, and that one of his lanes barely pays for itself — but he has never had the data in front of him to prove it, size it, or decide what to do about it.

## Key Operational Facts

**Trucks:**
- TRK-001 through TRK-010, mix of Freightliner Cascadia, Peterbilt 579, and Kenworth T680, model years 2015-2022
- TRK-006 is a 2013 Freightliner Cascadia with 738,000+ miles — the oldest, highest-mileage unit in the fleet, kept in service on the Joplin-Little Rock lane
- Fleet average fuel economy is ~6.9 MPG; TRK-006 runs ~5.2 MPG

**Drivers:**
- DRV-001 through DRV-014, mix of company drivers, home terminal Joplin, MO
- CDL Class A across the board, experience ranges from 1 to 24 years

**Customers:**
- Ozark Building Supply — Joplin, MO — building materials — contract terms net-30, but averages ~48 minutes of detention per delivery vs. fleet average ~11 minutes
- Route 66 Ag Cooperative — Tulsa, OK — agriculture — contract terms net-30, but pays on a de facto net-60+ cycle
- Sooner State Lumber — Oklahoma City, OK — building materials — reliable payer, average detention
- Delta Farm & Feed — Little Rock, AR — agriculture — reliable payer, average detention

**Routes/Lanes:**
- Joplin, MO → Little Rock, AR (the lane TRK-006 primarily runs) — base rate too low relative to distance and deadhead, nets ~$1.65/mile after fuel vs. a ~$2.05/mile breakeven threshold
- Joplin, MO → Tulsa, OK
- Joplin, MO → Oklahoma City, OK
- Joplin, MO → Kansas City, MO
- Joplin, MO → Springfield, MO
- Joplin, MO → Dallas, TX
- Return/backhaul lanes mirroring the above

## Pain Points (to be discovered analytically)

- **Truck TRK-006**, a 2013 Freightliner Cascadia with 738,000+ miles, averages **5.2 MPG**, roughly 25% below the fleet average of **6.9 MPG**, and it is disproportionately assigned to the Joplin-Little Rock lane, compounding that lane's poor economics.
- **Customer Ozark Building Supply** (Joplin, MO) averages **48 minutes of detention** per delivery, more than 4x the fleet average of **~11 minutes**, driven by a chronically understaffed receiving dock.
- **The Joplin → Little Rock lane** nets only **~$1.65/mile** after fuel costs, well below the fleet's **$2.05/mile** breakeven threshold, making it a loss-leader that the company has kept running out of loyalty to Delta Farm & Feed.
- **Truck TRK-006's maintenance costs and downtime are far out of line with the fleet**: it has logged roughly **$42,900** in maintenance costs over the analysis window (2-4x any other truck) and **461 hours of downtime**, driven by repeated engine, transmission, and coolant-system repairs consistent with its age and mileage.
- **Driver turnover is concentrated**: of the drivers primarily assigned to the Joplin-Little Rock lane (paired with TRK-006), 3 of 4 have separated from the company, versus zero separations among the other ten drivers, suggesting the unprofitable lane and the worn-out truck are also a retention problem, not just a cost problem.

## What This Company Needs

Curtis needs tools that convert his gut feelings into numbers he can act on without hiring an analyst. A fuel-efficiency and truck health dashboard would let him see, truck by truck and lane by lane, where MPG is dragging down margins — and make the case for retiring or reassigning TRK-006. A detention/accessorial tracker tied to customers would let him quantify exactly how much Ozark Building Supply's dock delays are costing him in driver hours and turnaround, giving him leverage to renegotiate accessorial charges or push for dock improvements. A lane profitability tool that nets out fuel, deadhead, and detention against revenue per mile would let him see the Joplin-Little Rock lane's true economics and decide whether to reprice it, restructure it, or drop it. Finally, an AR aging view tied to actual payment cycles (not just contract terms) would show him that Route 66 Ag Cooperative's real payment behavior is a working-capital problem worth addressing directly with that customer.
