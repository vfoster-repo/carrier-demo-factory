# CARRIER DEMO FACTORY — COMPANY CREATOR PROMPT

You are Phase 0 of a five-phase autonomous agent pipeline. This is the optional demo data generator phase — its purpose is to create a fictional trucking carrier with synthetic operational data when no real carrier data is available. The output of this phase feeds directly into Phase 1 (idea generation).

If you are running against a real carrier's data, this phase should be skipped entirely.

---

## YOUR TASK

Create one complete fictional carrier with:
1. A company profile (prose describing who they are and what their problems are)
2. Synthetic operational data (CSV files that encode the pain points)
3. An updated master state file so the next phase begins automatically

---

## STEP 1 — SELECT CARRIER TYPE

Run this Python command and use the output to select the carrier type:

```python
python3 -c "
import datetime
now = datetime.datetime.utcnow()
seed = (now.day * 1440 + now.hour * 60 + now.minute)
types = ['owner_operator', 'small_fleet', 'regional_carrier', 'mid_size_carrier']
print('CARRIER_TYPE:', types[seed % len(types)])
"
```

Carrier type definitions:
- **owner_operator**: 1-2 trucks, 1-2 drivers, solo or couple-run operation
- **small_fleet**: 5-15 trucks, 8-20 drivers, 1-2 major customer relationships
- **regional_carrier**: 20-50 trucks, 30-70 drivers, multi-state operations
- **mid_size_carrier**: 75-150 trucks, 100-200 drivers, national footprint

---

## STEP 2 — DESIGN THE COMPANY STORY

Before generating any data, design the company story in your head. Write it
as a narrative first. The story must include:

**Identity:**
- Company name (real-sounding, not generic)
- Owner/founder name and brief backstory (2-3 sentences)
- Home terminal city and state
- Year founded
- Primary freight type (dry van, refrigerated, flatbed, tanker, etc.)
- Primary lanes (specific city pairs, e.g., "Denver to Salt Lake City")
- Primary customers (2-4 named shippers, what they ship)

**The Operational Reality (design 3-5 specific pain points):**
This is the most important part. Pick specific, concrete operational problems
that will be visible in the data. Do NOT pick vague problems. Each pain point
must be phrased as a specific fact, for example:

GOOD:
- "Truck TRK-003, a 2012 Peterbilt 389 with 812,000 miles, is getting 5.1 MPG
  on the Denver-Dallas run versus the fleet average of 6.8 MPG."
- "Customer Western Plastics (Albuquerque) averages 41 minutes of detention per
  delivery, nearly 5x higher than the fleet average of 9 minutes."
- "The Denver→Phoenix lane generates only $1.84/mile net after fuel, well below
  the break-even threshold of $2.10/mile."

BAD:
- "The company has fuel efficiency problems."
- "Some customers cause detention."
- "Some lanes are unprofitable."

The pain points drive EVERYTHING. The data must confirm them. The idea
generator will discover them analytically. The apps will quantify them.

---

## STEP 3 — CREATE THE COMPANY DIRECTORY

Create the directory:
`{COMPANIES_DIR}/{company-slug}/`

Where `company-slug` is the company name in lowercase with hyphens
(e.g., "green-mountain-trucking").

Create these subdirectories:
```
{company-slug}/
├── data/       ← synthetic CSV files go here
├── apps/       ← app builder will create subdirs here
└── company_profile.md  ← write this now
```

---

## STEP 4 — WRITE company_profile.md

Write `{company-slug}/company_profile.md` with this exact structure:

```markdown
# {Company Name}

**Type:** {carrier type}
**Location:** {city, state}
**Founded:** {year}
**Owner:** {owner name}
**Primary Freight:** {freight type}
**Fleet Size:** {N trucks, N drivers}
**Tagline:** {one-sentence description of what makes this company interesting}

## Company Story

{3-5 paragraph narrative about the company — who they are, how they got
started, what they haul, who their customers are, what their daily
operations look like. Make it realistic and specific.}

## Key Operational Facts

{Bullet list of specific facts that will appear in the data:
- truck IDs and their characteristics
- customer names and their locations
- lane names and their base rates
- driver names and their roles
All of these must match what gets generated in the CSVs.}

## Pain Points (to be discovered analytically)

{The 3-5 specific pain points you designed. Phrased as concrete facts.
These are for your reference — they must be visibly present in the data.
The idea generator does not read this section — it will discover these from
the raw data.}

## What This Company Needs

{1-2 paragraph description of what kind of tools would genuinely help
this company. Think like a consultant. What would you build for them?
This is free-thinking — the idea generator will do its own analysis.}
```

---

## STEP 5 — GENERATE SYNTHETIC DATA

Write a Python script `{company-slug}/generate_data.py` that produces
realistic CSV files for this company. Then run it.

**Scale by carrier type:**
- owner_operator: ~400-600 loads, 1-2 trucks, 1-2 drivers, 2 years of data
- small_fleet: ~3,000-6,000 loads, 5-15 trucks, 8-20 drivers, 2 years
- regional_carrier: ~15,000-30,000 loads, 20-50 trucks, 30-70 drivers, 2 years
- mid_size_carrier: ~50,000-80,000 loads, 75-150 trucks, 100-200 drivers, 2 years

**Required CSV files** (use only what makes sense for the company size):

`data/drivers.csv` — columns: driver_id, first_name, last_name, hire_date,
  employment_status, cdl_class, years_experience, home_terminal

`data/trucks.csv` — columns: truck_id, make, model, year, status,
  acquisition_date, current_odometer, fuel_type

`data/customers.csv` — columns: customer_id, customer_name, city, state,
  industry, payment_terms_days, account_status

`data/routes.csv` — columns: route_id, origin_city, origin_state,
  destination_city, destination_state, distance_miles, base_rate_per_mile

`data/loads.csv` — columns: load_id, customer_id, route_id, load_date,
  freight_type, weight_lbs, revenue, fuel_surcharge, load_status

`data/trips.csv` — columns: trip_id, load_id, driver_id, truck_id,
  actual_miles, fuel_gallons, actual_mpg, departure_time, arrival_time,
  on_time_flag

`data/fuel_purchases.csv` — columns: purchase_id, trip_id, truck_id,
  driver_id, purchase_date, gallons, price_per_gallon, total_cost, location

`data/delivery_events.csv` — columns: event_id, load_id, trip_id,
  facility_type, scheduled_time, actual_time, detention_minutes, on_time

`data/maintenance_records.csv` — columns: record_id, truck_id, service_date,
  service_type, cost, downtime_hours, odometer_at_service

**Critical data engineering rules:**

1. Pain points must be VISIBLE in the data with statistical significance:
   - If a truck has bad MPG, its actual_mpg values must be consistently 20-30%
     below fleet average across many trips, not just occasionally.
   - If a customer has high detention, their delivery_events rows must show
     detention_minutes consistently 3-6x above average.
   - If a lane is unprofitable, the revenue minus computed fuel cost must be
     below threshold for 70%+ of loads on that lane.

2. Data must be internally consistent:
   - trip_id -> load_id -> route_id must all resolve
   - fuel_purchases must reference valid trip_id and truck_id
   - delivery_events must reference valid load_id

3. Use realistic industry numbers:
   - Class 8 truck MPG: 6.0-7.5 (bad truck: 4.8-5.5)
   - Diesel price range: $3.80-$4.50/gallon (reflect 2023-2025 range)
   - Detention average: 8-15 minutes (problem customer: 35-60 minutes)
   - On-time rate: 85-95% fleet average
   - Driver turnover: 15% annually at regional carriers
   - Base rate per mile: $1.80-$3.20 depending on lane length and freight type

4. Generate dates spanning 2 years ending today.

5. Use meaningful IDs that match the company profile:
   - trucks: TRK-001, TRK-002, etc.
   - drivers: DRV-001, DRV-002, etc.
   - customers: match the names from the profile

After the script runs, verify each CSV was created and print row counts.

---

## STEP 6 — UPDATE MASTER STATE FILE

After all files are written and the data script runs successfully, update
the master state file at the path provided in the session context:

```
PHASE: generate_ideas
COMPANY: {company-slug}
NOTE: {Company Name} created — {carrier type}, {city}, {N} trucks, {N} pain points embedded
```

Write exactly this format. Nothing else. The next phase reads this file.

---

## COMPLETION CRITERIA

You are done when:
- [ ] company_profile.md is written and accurate
- [ ] generate_data.py runs without errors
- [ ] All required CSV files exist in data/
- [ ] Pain points are statistically visible in the data (spot-check 2-3)
- [ ] Master state file updated to PHASE: generate_ideas

Do NOT stop until all five criteria are met.
