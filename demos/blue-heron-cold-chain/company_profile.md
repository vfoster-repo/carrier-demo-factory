# Blue Heron Cold Chain

**Type:** owner_operator
**Location:** Mount Vernon, Washington
**Founded:** 2017
**Owner:** Marcus Kowalczyk
**Primary Freight:** Refrigerated (produce & seafood)
**Fleet Size:** 2 trucks, 2 drivers
**Tagline:** A husband-and-wife reefer team hauling Skagit Valley produce and Bellingham seafood south to Portland and the Bay Area — profitable heading south, bleeding money on the way back.

## Company Story

Marcus Kowalczyk drove reefer for a mid-size Yakima carrier for eleven years before he and his wife, Renata, bought their first truck in 2017 — a used Freightliner Cascadia they financed against their house. They built Blue Heron Cold Chain around a simple pitch to Skagit Valley farmers and Bellingham seafood processors: same-day pickup, a driver who actually shows up on time, and a level of care with temperature logs that the big carriers couldn't be bothered with. It worked. Within two years they'd added a second truck and Renata, a former dispatcher, came on full-time to drive it and run the books.

The business runs on a tight seasonal rhythm. From April through October, Blue Heron hauls Skagit Valley produce — potatoes, berries, and tulip-adjacent specialty crops — and Bellingham Cold Storage seafood south out of the Pacific Northwest to distribution centers in Portland and the Bay Area. Northbound, they scrape together whatever backhaul freight they can find, usually through a load board, because none of their core customers ship much north into Washington.

Marcus drives TRK-01, the original 2016 Freightliner Cascadia, now pushing 766,000 miles. Renata drives TRK-02, a 2021 Kenworth T680 they bought once the business was stable enough to finance new equipment, now at roughly 446,000 miles. The age and mechanical condition gap between the two trucks has become a running argument at the kitchen table — Marcus's truck needs more diesel to do the same job, and it shows up in the fuel bill every single week.

Their three anchor customers are Skagit Valley Produce (Mount Vernon, WA), Bellingham Cold Storage (Bellingham, WA), and Cascade Berry Growers (Burlington, WA), all of whom ship south on a predictable schedule. A fourth relationship, Golden Gate Fresh Distributors in Oakland, CA, receives the bulk of their southbound loads but has grown notorious around the yard for how long it takes to get a trailer unloaded. Marcus and Renata both dread the Oakland stop, but it's also their highest-volume delivery point, so they can't walk away from it.

## Key Operational Facts

- Trucks: TRK-01 (2016 Freightliner Cascadia, Marcus's truck, 766,000+ miles, diesel) and TRK-02 (2021 Kenworth T680, Renata's truck, 446,000+ miles, diesel)
- Drivers: DRV-01 Marcus Kowalczyk (owner, CDL-A, 18 years experience, home terminal Mount Vernon, WA), DRV-02 Renata Kowalczyk (co-owner, CDL-A, 6 years experience, home terminal Mount Vernon, WA)
- Customers: Skagit Valley Produce (Mount Vernon, WA — produce), Bellingham Cold Storage (Bellingham, WA — seafood), Cascade Berry Growers (Burlington, WA — berries/produce), Golden Gate Fresh Distributors (Oakland, CA — receiver, high detention)
- Primary lanes: Mount Vernon, WA → Portland, OR; Bellingham, WA → Oakland, CA; Burlington, WA → Oakland, CA; and northbound backhaul lanes from Oakland/Portland back to Mount Vernon/Bellingham sourced off the load board at low, inconsistent rates
- Base rates: southbound reefer lanes run $2.60-$3.10/mile; northbound backhaul lanes run $1.55-$1.85/mile
- Fleet average MPG target: ~6.9 MPG; TRK-01 (Marcus) consistently runs 5.0-5.4 MPG
- Fleet average detention: ~10 minutes; Golden Gate Fresh Distributors averages 47+ minutes

## Pain Points (to be discovered analytically)

- Truck TRK-01, Marcus's 2016 Freightliner Cascadia with 766,000+ miles, gets 5.0-5.4 MPG (measured fleet-wide average: 5.18 MPG) on runs versus TRK-02's (Renata's 2021 Kenworth T680) 6.8-7.3 MPG (measured average: 7.01 MPG) — roughly 26% worse fuel efficiency on the same lanes, costing an estimated extra $180-$220 per round trip in diesel.
- Customer Golden Gate Fresh Distributors (Oakland, CA) averages 47 minutes of detention per delivery, roughly 5x the fleet average of ~10 minutes, and it is their single highest-volume delivery point, so the cost is unavoidable without renegotiating terms.
- Northbound backhaul loads (Oakland/Portland → Mount Vernon/Bellingham) net under $1.10/mile after fuel on over 70% of trips, well below Blue Heron's breakeven of roughly $1.65/mile for a reefer unit running empty-adjacent backhauls — driven by low load-board rates and materially higher deadhead miles than southbound loaded lanes.
- TRK-01 also shows a rising maintenance cost trend — service costs per event and unplanned downtime hours climb noticeably in the trailing 6 months of the dataset as the truck crosses 600,000 miles, consistent with a truck approaching the end of its economical service life.
- Reefer fuel/reefer-unit runtime is baked into fuel_purchases gallons for both trucks, but TRK-01's combination of tractor age and reefer unit runtime pushes its all-in fuel cost per loaded mile noticeably higher than TRK-02's, compounding the MPG gap already visible in trips.csv.

## What This Company Needs

Marcus and Renata don't need a TMS built for a 100-truck fleet — they need something that turns the numbers they already sense in their gut into hard evidence they can act on. A simple per-truck profitability and fuel-efficiency view would let them finally quantify what Marcus's truck is costing them and decide whether to trade it in, and a lane-level margin view (especially isolating northbound backhauls) would let them see whether they should be pickier about load-board freight or renegotiate their southbound rates to cross-subsidize the empty miles home. A detention tracker aimed squarely at Golden Gate Fresh Distributors — with dollar figures attached — would give them leverage in a rate or accessorial conversation instead of just a shared frustration.

I'd build them a small "two-truck command center": one screen showing cost-per-mile and MPG trends by truck, one showing lane profitability net of fuel and deadhead, and one showing detention exposure by customer with a running dollar total. Nothing more complex than that — they need clarity, not a platform.
