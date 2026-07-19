# Redtail Regional Freight

**Type:** regional_carrier
**Location:** Amarillo, Texas
**Founded:** 2009
**Owner:** Dale Whitfield
**Primary Freight:** Dry van and temperature-controlled (reefer) — mixed fleet
**Fleet Size:** 38 trucks, 52 drivers
**Tagline:** A Texas Panhandle carrier that grew up hauling ag and food freight through the Permian Basin boom, now straining under an aging reefer segment and one brutal detention customer.

## Company Story

Dale Whitfield spent eleven years driving oilfield support trucks out of Midland before he bought his first truck in 2009, right as the shale boom was reshaping freight demand across the Panhandle. He started Redtail Regional Freight with a single 2006 Peterbilt and a handshake contract hauling frac sand and ag inputs between Amarillo and Lubbock. By the early 2010s he'd added reefer capacity to chase food-processing freight, and the company settled into its current identity: a dry van/reefer hybrid regional carrier running a tight corridor across the Texas Panhandle, eastern New Mexico, western Oklahoma, and southern Colorado.

Today Redtail runs 38 trucks and employs 52 drivers out of a single terminal in Amarillo. The fleet is a mix of newer Freightliner Cascadias bought in the last five years and a stubborn tail of older trucks Dale has been reluctant to retire because they're paid off. The company's bread and butter is agricultural and food freight — beef, dairy, produce, and packaged foods moving out of Panhandle processing plants to distribution centers in Denver, Oklahoma City, and Albuquerque, plus backhauls of packaging materials and dry goods.

Redtail's four anchor customers are Panhandle Beef Processors (Amarillo, protein/frozen), Llano Estacado Foods (Lubbock, dairy and packaged foods), High Plains Ag Cooperative (Hereford, TX, grain and ag inputs), and Sangre de Cristo Distribution (Denver, CO, mixed retail goods as a backhaul partner). These four customers account for the large majority of Redtail's freight volume.

Dale still works the dispatch desk most mornings and prides himself on knowing every driver by name. But the operation has outgrown his spreadsheet-and-gut-feel management style. He knows something is dragging down margins on the Denver reefer lane and suspects one of his older trucks is a money pit, but he's never had the data laid out in front of him to prove it or size the problem.

## Key Operational Facts

- Fleet: 38 trucks (TRK-001 through TRK-038), primarily Freightliner Cascadia and Peterbilt 579/389 tractors, model years 2013-2024, mixed dry van and reefer configurations.
- Drivers: 52 drivers (DRV-001 through DRV-052), home terminal Amarillo, TX.
- Customers:
  - CUST-001: Panhandle Beef Processors — Amarillo, TX — protein/food processing
  - CUST-002: Llano Estacado Foods — Lubbock, TX — dairy/food processing
  - CUST-003: High Plains Ag Cooperative — Hereford, TX — agriculture
  - CUST-004: Sangre de Cristo Distribution — Denver, CO — retail/distribution
- Primary lanes:
  - Amarillo, TX → Denver, CO (reefer, ~430 miles)
  - Amarillo, TX → Oklahoma City, OK (dry van, ~260 miles)
  - Lubbock, TX → Albuquerque, NM (dry van/reefer, ~280 miles)
  - Amarillo, TX → Hereford, TX → local ag hauls (~50 miles)
  - Amarillo, TX → Denver, CO backhaul with Sangre de Cristo mixed retail goods
- TRK-014: 2013 Freightliner Cascadia, 781,000+ miles, chronically low MPG and high maintenance downtime.
- Llano Estacado Foods (CUST-002) is the outlier detention customer at the Lubbock dock.

## Pain Points (to be discovered analytically)

- Truck TRK-014, a 2013 Freightliner Cascadia with roughly 781,000 miles, averages approximately 5.0 MPG across its trips, compared to a fleet average near 6.9 MPG — a persistent ~28% efficiency gap, not an occasional dip.
- Customer Llano Estacado Foods (Lubbock, TX) generates average detention of roughly 47 minutes per delivery at their dock, versus a fleet-wide average of about 11 minutes — over 4x higher, consistently, across nearly every load.
- The Amarillo→Denver reefer lane (route AMA-DEN-REEFER) nets below the $2.05/mile break-even threshold after fuel cost on the large majority of loads, despite reasonable gross base rates, because of the long empty-adjusted deadhead and reefer fuel burn on that corridor.
- TRK-014 also drives a disproportionate share of the fleet's maintenance cost and downtime hours — frequent unscheduled repairs concentrated in the last 18 months, well above the per-truck fleet average.
- A small cluster of drivers hired in the past 18 months at the Amarillo terminal show much shorter tenure before termination/quit compared to tenured drivers, consistent with turnover concentrated among newer hires rather than being evenly spread across the workforce.

## What This Company Needs

Dale needs a way to see, in dollar terms, which trucks and lanes are quietly bleeding margin instead of relying on gut feel from the dispatch desk. A per-truck profitability and MPG scorecard would let him build the case (to himself, and to his banker) for retiring TRK-014 rather than continuing to patch it. Separately, a customer scorecard that tracks detention minutes and accessorial cost per customer would give him leverage to either renegotiate detention terms with Llano Estacado Foods or pass the cost through — right now that cost is invisible, buried inside "normal" trip variance.

A lane profitability tool that nets out fuel, deadhead, and detention against base rate would let him see that the Denver reefer lane looks fine on paper (decent rate per mile) but is actually a loser once true costs are included — something he can't currently see without hand-building a spreadsheet every quarter. Finally, a lightweight driver retention view flagging early-tenure attrition at the Amarillo terminal would help him figure out whether it's a specific dispatcher, route assignment, or onboarding gap driving new hires out the door before they become productive.
