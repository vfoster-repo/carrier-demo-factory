# CARRIER DEMO FACTORY — COMPANY PROFILE BUILDER PROMPT

You are Phase 3 of a five-phase autonomous agent pipeline. Your job is to build
one polished, self-contained HTML "Company Profile" page that tells the full story
of this carrier — who they are, what data was analyzed, what problems were found,
and what was built to address them.

This page lives at: `https://{DOMAIN}/{company-slug}/profile/`

It serves two purposes:
1. **For the prospect:** A transparent look at the process — "here's what we found
   in your data and why we built what we built."
2. **For everyone else:** Context that makes the demo meaningful — without this,
   a visitor to {DOMAIN} sees apps but doesn't know the story behind them.

---

## STEP 1 — READ ALL SOURCES

Read every file before writing any HTML:

1. `company_profile.md` — full company identity, fleet, drivers, customers, lanes,
   owner info, financial baseline, and operational context. Read it completely.
2. `ideas.md` — the PRIMARY PAIN POINTS section tells you what was discovered in
   the data. Read the full description of each pain point.
3. `data/*.csv` — for each CSV file, read the first 5 rows and get: row count,
   column names, date range (if any date column exists), and 2-3 notable raw facts.
   Use `pd.read_csv(f).shape`, `.columns.tolist()`, `.head(5)`, `.describe()`.
4. Look for `apps/report/deployment_url.txt` and `apps/ops/deployment_url.txt` to
   get the live URLs for both products. If those don't exist yet, construct the
   URLs from the company slug: `https://{DOMAIN}/{slug}/report/` and
   `https://{DOMAIN}/{slug}/ops`.

---

## STEP 2 — EXTRACT KEY FACTS

Before writing HTML, compute these values in Python:

```python
import pandas as pd, os, json
from pathlib import Path

data_dir = Path('data')
csv_summaries = []
for f in sorted(data_dir.glob('*.csv')):
    df = pd.read_csv(f)
    summary = {
        'filename': f.name,
        'rows': len(df),
        'columns': df.columns.tolist(),
    }
    # find date column if any
    for col in df.columns:
        if 'date' in col.lower() or 'month' in col.lower() or 'year' in col.lower():
            try:
                dates = pd.to_datetime(df[col], errors='coerce').dropna()
                if len(dates) > 0:
                    summary['date_range'] = f"{dates.min().strftime('%b %Y')} – {dates.max().strftime('%b %Y')}"
            except: pass
            break
    csv_summaries.append(summary)

print(json.dumps(csv_summaries, indent=2))
```

Also pull the top 3-5 headline numbers from the data — the most striking facts
(e.g. "6 trucks averaging 5.18 MPG vs 6.88 fleet average", "47 min avg detention
at Magnolia Foods"). These go in the "What We Found" section.

---

## STEP 3 — BUILD THE HTML PAGE

Write the complete HTML to `profile.html` in the working directory.

Use this exact design system — inline CSS, no external dependencies except the
Google Font import:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Company Name} — Company Profile | Carrier Demo Factory</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0f1117;color:#c9d1d9;line-height:1.65;min-height:100vh}
a{color:#58a6ff;text-decoration:none}
a:hover{text-decoration:underline}

/* Layout */
.page{max-width:860px;margin:0 auto;padding:2.5rem 1.25rem 5rem}

/* Hero */
.hero{background:linear-gradient(135deg,#1a2744 0%,#1e2a3a 100%);border:1px solid #21262d;border-radius:16px;padding:2.5rem;margin-bottom:2rem}
.hero-tag{font-size:0.72rem;font-weight:700;color:#58a6ff;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.75rem}
.hero-company{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;color:#e6edf3;line-height:1.2;margin-bottom:0.5rem}
.hero-meta{font-size:0.85rem;color:#8b949e;margin-bottom:1.25rem}
.hero-tagline{font-size:1rem;color:#adbac7;line-height:1.7;max-width:680px;border-left:3px solid #1f6feb;padding-left:1rem}

/* Stat strip */
.stat-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1rem;margin-bottom:2rem}
.stat-box{background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.1rem 1.25rem;text-align:center}
.stat-value{font-size:1.6rem;font-weight:700;color:#e6edf3;line-height:1}
.stat-label{font-size:0.72rem;color:#8b949e;margin-top:0.35rem;text-transform:uppercase;letter-spacing:0.06em}

/* Sections */
.section{margin-bottom:2.5rem}
.section-title{font-size:1.05rem;font-weight:700;color:#e6edf3;margin-bottom:1.1rem;padding-bottom:0.5rem;border-bottom:1px solid #21262d;display:flex;align-items:center;gap:0.5rem}

/* Pain point cards */
.pain-card{background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.3rem 1.5rem;margin-bottom:0.85rem}
.pain-card-title{font-size:0.95rem;font-weight:600;color:#e6edf3;margin-bottom:0.5rem;display:flex;align-items:center;gap:0.5rem}
.pain-card-body{font-size:0.875rem;color:#8b949e;line-height:1.65}
.pain-number{background:#1f6feb;color:white;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;flex-shrink:0}

/* Data table */
.data-table{width:100%;border-collapse:collapse;font-size:0.85rem}
.data-table th{text-align:left;font-size:0.72rem;font-weight:600;color:#8b949e;text-transform:uppercase;letter-spacing:0.06em;padding:0.5rem 0.75rem;border-bottom:1px solid #21262d}
.data-table td{padding:0.65rem 0.75rem;border-bottom:1px solid #161b22;color:#c9d1d9;vertical-align:top}
.data-table tr:last-child td{border-bottom:none}
.data-table .col-tag{background:#21262d;border-radius:4px;padding:1px 6px;font-size:0.7rem;display:inline-block;margin:1px}

/* Product cards */
.product-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}
.product-card{background:#161b22;border:1px solid #21262d;border-radius:12px;padding:1.5rem;display:flex;flex-direction:column;gap:0.75rem;transition:border-color 0.15s}
.product-card:hover{border-color:#58a6ff}
.product-card-icon{font-size:1.75rem}
.product-card-type{font-size:0.7rem;font-weight:700;color:#58a6ff;text-transform:uppercase;letter-spacing:0.08em}
.product-card-title{font-size:1rem;font-weight:700;color:#e6edf3}
.product-card-desc{font-size:0.85rem;color:#8b949e;line-height:1.6;flex:1}
.product-card-link{display:inline-flex;align-items:center;gap:0.4rem;font-size:0.85rem;font-weight:600;color:#58a6ff;margin-top:0.25rem}

/* Fact highlight */
.fact-highlight{background:#1a2744;border:1px solid #1f6feb33;border-radius:10px;padding:0.85rem 1.1rem;margin-bottom:0.6rem;font-size:0.9rem;color:#adbac7;line-height:1.6}
.fact-highlight strong{color:#e6edf3}

/* Footer */
.footer{text-align:center;font-size:0.75rem;color:#484f58;margin-top:4rem;padding-top:1.5rem;border-top:1px solid #21262d}

/* Mobile */
@media(max-width:600px){
  .hero{padding:1.5rem}
  .hero-company{font-size:1.5rem}
  .stat-strip{grid-template-columns:repeat(2,1fr)}
}
</style>
</head>
<body>
<div class="page">

  <!-- HERO -->
  <div class="hero">
    <div class="hero-tag">Company Profile · Carrier Demo Factory</div>
    <div class="hero-company">{Company Name}</div>
    <div class="hero-meta">{carrier type} · {location}</div>
    <div class="hero-tagline">{full company tagline from company_profile.md — copy it verbatim}</div>
  </div>

  <!-- STAT STRIP -->
  <!-- Pull these from company_profile.md — trucks, drivers, customers, years in business, etc. -->
  <div class="stat-strip">
    <div class="stat-box"><div class="stat-value">{N}</div><div class="stat-label">Trucks</div></div>
    <div class="stat-box"><div class="stat-value">{N}</div><div class="stat-label">Drivers</div></div>
    <div class="stat-box"><div class="stat-value">{N}</div><div class="stat-label">Customers</div></div>
    <div class="stat-box"><div class="stat-value">{$XM}</div><div class="stat-label">Est. Revenue</div></div>
    <!-- Add more as relevant: Lanes, States, Years in Business, etc. -->
  </div>

  <!-- ABOUT -->
  <div class="section">
    <div class="section-title">🏢 About This Company</div>
    <!-- 3-4 paragraphs from company_profile.md. Include:
         - Who owns/runs it, how long they've been in business
         - What they haul, where they run, who their key customers are
         - What their current operational challenges look like
         - Why they were selected as a demo target (what makes their situation typical/interesting)
         Write in plain English as if introducing them to a sales prospect. -->
    <p>{paragraph 1}</p>
    <p style="margin-top:1rem">{paragraph 2}</p>
    <p style="margin-top:1rem">{paragraph 3}</p>
  </div>

  <!-- WHAT WE FOUND -->
  <div class="section">
    <div class="section-title">🔍 What We Found in the Data</div>
    <!-- 4-7 specific, quantified facts pulled from the data analysis.
         Format each as a fact-highlight div. Lead with the number.
         These should be the most striking / actionable findings.
         Example: "<strong>$335K/year in excess fuel costs</strong> — 6 legacy trucks
         averaging 5.18 MPG consume nearly a third of the fuel budget despite
         making up only 40% of the fleet." -->
    <div class="fact-highlight"><strong>{Number + label}</strong> — {1-2 sentence explanation of why it matters}</div>
    <!-- repeat for each key finding, 4-7 total -->
  </div>

  <!-- DATA ANALYZED -->
  <div class="section">
    <div class="section-title">📂 Data Analyzed</div>
    <p style="font-size:0.875rem;color:#8b949e;margin-bottom:1rem">
      The following datasets were provided by {Company Name} and analyzed to produce
      the insights report and operations platform below.
    </p>
    <table class="data-table">
      <thead>
        <tr>
          <th>Dataset</th>
          <th>Records</th>
          <th>Period</th>
          <th>Key Fields</th>
        </tr>
      </thead>
      <tbody>
        <!-- One row per CSV. Dataset name: humanize the filename (e.g. "loads.csv" → "Load History").
             Records: row count. Period: date range if found. Key Fields: 4-6 most meaningful columns
             as .col-tag spans. -->
        <tr>
          <td>{Dataset Name}</td>
          <td>{N:,} records</td>
          <td>{date range or "—"}</td>
          <td><span class="col-tag">{col}</span> <span class="col-tag">{col}</span></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- PAIN POINTS -->
  <div class="section">
    <div class="section-title">⚠️ Primary Pain Points Identified</div>
    <p style="font-size:0.875rem;color:#8b949e;margin-bottom:1rem">
      Analysis of the data revealed the following operational pain points, ranked by
      estimated annual dollar impact.
    </p>
    <!-- One pain-card per primary pain point from ideas.md.
         Title: the pain point name.
         Body: 2-3 sentences describing the problem, its root cause, and its cost.
         Be specific — use real names (truck IDs, customer names, dollar amounts). -->
    <div class="pain-card">
      <div class="pain-card-title"><span class="pain-number">1</span> {Pain Point Title}</div>
      <div class="pain-card-body">{2-3 sentences: what the problem is, what causes it, what it costs annually. Specific numbers and names.}</div>
    </div>
    <!-- repeat for each pain point -->
  </div>

  <!-- WHAT WE BUILT -->
  <div class="section">
    <div class="section-title">🛠️ What We Built</div>
    <div class="product-grid">
      <a class="product-card" href="{report_url}" target="_blank" rel="noopener">
        <div class="product-card-icon">📊</div>
        <div class="product-card-type">Free · Insights Report</div>
        <div class="product-card-title">Data Insights Report</div>
        <div class="product-card-desc">
          A self-contained, shareable HTML report covering every major pain point
          with interactive charts. No login required — built to be sent to the
          customer or shared with their bank or accountant.
        </div>
        <div class="product-card-link">View Report →</div>
      </a>
      <a class="product-card" href="{ops_url}" target="_blank" rel="noopener">
        <div class="product-card-icon">🚛</div>
        <div class="product-card-type">Paid · SaaS Platform</div>
        <div class="product-card-title">Operations Platform</div>
        <div class="product-card-desc">
          A multi-page daily-use operations dashboard built on their actual data.
          Includes a Getting Started guide, load board, fleet KPIs, cash flow
          tracking, and driver scorecards — designed for an owner-operator who
          has never used software like this before.
        </div>
        <div class="product-card-link">Open Platform →</div>
      </a>
    </div>
  </div>

  <div class="footer">
    Built autonomously by Carrier Demo Factory · <a href="https://{DOMAIN}">{DOMAIN}</a>
  </div>

</div>
</body>
</html>
```

Fill in ALL placeholder values from the actual data. Do not leave any `{...}` in the final HTML.
Do not abbreviate the pain point descriptions — write the full 2-3 sentences.

---

## STEP 4 — DEPLOY

```bash
COMPANY_SLUG="{company-slug}"
bash /opt/carrier-factory/deploy-profile.sh \
    "$COMPANY_SLUG" \
    "profile.html"
```

Verify `profile_deployment_url.txt` is created and print the URL.

---

## STEP 5 — UPDATE STATE

Write to the master state file:
```
PHASE: build_ops_app
COMPANY: {company-slug}
```

---

## COMPLETION CRITERIA

- [ ] `profile.html` written — no `{...}` placeholders remaining
- [ ] Stat strip has real numbers from company_profile.md
- [ ] "What We Found" section has 4-7 specific quantified facts from the data
- [ ] Data table has one row per CSV with real row counts, date ranges, and column names
- [ ] Pain point cards have specific names, numbers, and dollar amounts — not generic text
- [ ] Both product cards link to the correct live URLs
- [ ] `deploy-profile.sh` ran successfully
- [ ] State updated to `PHASE: build_ops_app`
