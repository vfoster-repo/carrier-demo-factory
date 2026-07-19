# CARRIER DEMO FACTORY — IDEA GENERATOR PROMPT

You are Phase 1 of a five-phase autonomous agent pipeline. The previous phase established a carrier company profile and operational CSV data — either generated synthetically (Phase 0) or provided directly from a real carrier. Your job this session is to:
1. Independently analyze the company's data (like a consultant who just received files)
2. Discover the pain points embedded in the data (you are NOT told what they are)
3. Brainstorm every possible application that could help this company
4. Write a detailed build specification for each idea
5. Save everything to ideas.md

---

## STEP 1 — READ THE COMPANY PROFILE

Read `company_profile.md` in the working directory. This tells you:
- Who the company is and what they do
- Their fleet size, lanes, and customers (factual reference)

**Do NOT read the "Pain Points" section of the profile.** You will discover
those yourself from the data. Stop reading when you reach that section header.

---

## STEP 2 — EXPLORE THE DATA INDEPENDENTLY

Load each CSV file in `data/` using pandas. For each file, look at:
- Shape (rows × columns)
- Column names and data types
- A sample of 10 rows
- Basic descriptive statistics (describe())

Then run analytical queries to find patterns. Think like a forensic accountant
and a dispatcher who has been handed a box of files. Look for:

**Revenue and profitability signals:**
- Revenue per mile by route — which lanes make money, which don't?
- Revenue per load by customer — which customers drive profit?
- Net margin by lane after estimated fuel cost
- Load volume trends over time — growing or declining?

**Operational efficiency signals:**
- Fuel efficiency (MPG) by truck — outliers on either end?
- Fuel efficiency by driver — who burns the most fuel?
- On-time delivery rate by customer, by route, by driver
- Idle time or empty miles if calculable

**Equipment signals:**
- Maintenance cost trends by truck
- Downtime hours by truck — which units keep breaking?
- Cost per mile for maintenance by truck age

**Driver signals:**
- On-time performance by driver
- Fuel efficiency by driver
- Load count by driver (are some underutilized?)
- Tenure distribution — how many are new hires?

**Customer signals:**
- Detention time by customer (if delivery_events exists)
- Payment terms — who takes longest to pay?
- Load count and revenue by customer — customer concentration risk?

**Seasonal and trend signals:**
- Monthly load volume and revenue
- Fuel cost trends over the data period
- On-time performance trends over time

Write a Python analysis script and run it. Save outputs to
`analysis_output/` subdirectory. Print your findings clearly.

---

## STEP 3 — SUMMARIZE YOUR FINDINGS

After the analysis, write a summary of what you found. Be specific:
- Name the actual trucks, customers, routes, and drivers with anomalies
- Quantify the impact (dollars, percentages, minutes)
- Distinguish between findings that are actionable vs. just interesting

Mark the 3-5 most important findings as **PRIMARY PAIN POINTS** — these are
the problems that cost the most money or pose the biggest operational risk.

---

## STEP 4 — BRAINSTORM ALL POSSIBLE APPLICATIONS

Now think broadly about every type of application that could help this company.
Consider all audiences:

**For the owner/management:**
- What would help them understand business health at a glance?
- What decisions do they make weekly that could be data-driven?

**For the dispatcher:**
- What information do they need before accepting a load?
- What tools would help them route trucks more efficiently?
- What visibility do they need into customer behavior?

**For the driver:**
- What performance feedback would help them improve?
- What financial tools would help them understand their earnings?

**For accounting:**
- What cost tracking or forecasting would help?
- What customer profitability reporting is missing?
- What cash flow visibility is needed?

**For fleet maintenance:**
- What predictive tools would reduce breakdown surprises?
- What cost analysis would help prioritize repairs vs. replacement?

Do NOT limit yourself to what the data supports alone. Also think about:
- What additional data would unlock more powerful tools?
- What workflow tools would save time even without ML models?

Generate a minimum of 8 ideas, maximum of 15. Each idea should be distinct
and genuinely useful — not variations of the same concept.

---

## STEP 5 — WRITE ideas.md

Write `ideas.md` in the working directory with this structure:

```markdown
# {Company Name} — App Ideas

Generated: {date}
Analyst findings: {2-3 sentence summary of the biggest issues found}

---

## Primary Pain Points Discovered

1. {pain point 1 — specific, quantified}
2. {pain point 2 — specific, quantified}
3. {pain point 3 — specific, quantified}
[...]

---

## App Ideas

### App {N}: {App Name}

**Build ID:** app-{N:02d}-{app-slug}
**Audience:** {dispatcher | driver | owner | accountant | fleet manager}
**Category:** {dashboard | calculator | tracker | predictor | workflow tool}
**Priority:** {HIGH | MEDIUM | LOW}
**Data required:** {list of CSV files needed}
**Additional data needed:** {any data the company would need to provide separately, or "none"}

**Problem solved:**
{2-3 sentences describing the specific problem this app addresses. Name
actual customers, trucks, lanes, or drivers from this company's data where
relevant. Do not be generic.}

**What the app shows:**
{Bullet list of the 3-5 key things a user sees when they open the app.
Be specific about numbers, charts, and interactions.}

**Key metric / headline number:**
{The single most important number the user will see. Example: "Driver DRV-003
is costing $847/month more in fuel than the fleet average."}

**Build specification:**
{Detailed instructions for the app builder. Include:
- Data transformations needed
- What charts to build and why
- What the main insight/callout should say
- How data specific to this company should be presented (not generic)
- Any interactivity (filters, selectors) that adds real value
- The recommended layout
This section should be detailed enough that the app builder can work from
it without making major design decisions.}

**Success criteria:**
{How to know the app is good: what question does it answer for the user
in under 60 seconds?}

---
```

Repeat the App block for each idea. Number them App 01, App 02, etc.
The build ID (e.g., `app-01-load-profitability`) becomes the directory name.

---

## STEP 6 — UPDATE MASTER STATE FILE

After ideas.md is written, update the master state file:

```
PHASE: build_report
COMPANY: {company-slug}
NOTE: {N} ideas documented for {Company Name} — building report next
```

Write exactly this format. Nothing else.

---

## COMPLETION CRITERIA

You are done when:
- [ ] All CSV files explored and analyzed
- [ ] Primary pain points identified with specific numbers
- [ ] At least 8 app ideas written with full build specifications
- [ ] ideas.md saved to the company directory
- [ ] Master state file updated to PHASE: build_report

Do NOT stop until all criteria are met.
