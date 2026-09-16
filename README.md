# LPDG Smart Gateway

A Python 3.12 FastAPI-based decision-support project for smart gateway risk assessment and visit recommendation. The application loads gateway data, calculates risk scores using weighted factors, visualizes output, and provides a multi-page web experience for manual review and decision-making.

## Project Goal

The system evaluates each gateway using operational KPIs such as:
- failure rate
- incidents in the last 30 days
- downtime hours in the last 30 days
- days since last incident

It then calculates a risk score and assigns a priority band:
- LOW
- MEDIUM
- HIGH
- CRITICAL

The recommendation engine decides whether the gateway should:
- VISIT
- MONITOR

The app is designed to support both:
- automatic generation from dataset records
- manual recalculation using custom input values for one gateway or a general scenario

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- pytest
- Static frontend pages with HTML, CSS, and JavaScript

---

## Project Structure

```text
LPDG_Smart_Gateway_23091a32c5/
├── README.md
├── 23091a32c5.pdf
├── SUBMISSION_CHECKLIST.md
├── requirements.txt
├── run.py
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── ranking/
│   │   ├── __init__.py
│   │   └── engine.py
│   ├── routers/
│   │   ├── admin.py
│   │   ├── analytics.py
│   │   ├── gateways.py
│   │   └── recommendations.py
│   └── services/
│       ├── analytics.py
│       └── recommendation.py
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── gateways.html
│   ├── risk.html
│   ├── analytics.html
│   ├── plots.html
│   ├── app.js
│   └── style.css
├── data/
│   └── gateways.csv
├── docs/
│   └── plots/
│       ├── risk_priority_distribution.png
│       ├── gateway_risk_scores.png
│       └── risk_components.png
├── tests/
│   ├── test_api.py
│   ├── test_core.py
│   └── test_upload.py
├── gateway.db
└── .venv312/
```

---

## Setup and Run

### Recommended environment

Use Python 3.12 for compatibility and stability.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```

Then open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

### Alternative quick launch

```powershell
cd "C:\path\to\project"
.\.venv312\Scripts\python.exe run.py
```

---

## Application Flow

The project is structured as a small multi-page application with a landing screen and separate feature sections.

### Home Page
- Project name and landing view
- Navigation links to the main modules

### Dashboard
- Total gateways
- High/Critical count
- Visit count
- Weekly exposure overview

### Gateway Data
- Full list of raw gateway entries from the SQLite database
- Shows operational metrics for each gateway

### Risk Analysis
- Manual risk calculator
- Custom input values for failure rate, incidents, downtime, and recency
- Recalculation output with score, priority, decision, confidence, and reasons
- Gateway-specific recalculation section

### Analytics
- Summary metrics across all gateways
- Risk exposure statistics
- Visit recommendations overview

### Visualization Plots
- Image-based report pages for charts and visual outputs

---

## Data Model

The dataset is loaded from `data/gateways.csv` into SQLite during startup.

Required CSV columns:

```text
gateway_id,name,failure_rate,incidents_30d,downtime_hours_30d,days_since_last_incident,status
```

Example row:

```text
GW-001,Gateway A,0.18,7,58,3,ACTIVE
```

### Notes
- `failure_rate` should be in the range 0 to 1
- `incidents_30d` is integer count
- `downtime_hours_30d` is a numeric value
- `days_since_last_incident` is integer count
- `status` is stored in uppercase

---

## Risk Scoring Logic

The decision engine uses a normalized weighted score:

- failure rate: 40%
- incidents: 25%
- downtime: 20%
- recency: 15%

Formula conceptually:

```text
risk_score = failure_weighted + incidents_weighted + downtime_weighted + recency_weighted
```

The score is clamped to a 0-100 range.

Priority mapping:
- 80+ -> CRITICAL
- 60-79 -> HIGH
- 30-59 -> MEDIUM
- below 30 -> LOW

Decision logic:
- if recurring broken cost is greater than visit cost, decision is VISIT
- otherwise decision is MONITOR

Business rule values:
- visit_cost = €380
- broken_cost_per_week = €600

These values can be adjusted in `backend/config.py`.

---

## API Endpoints

### Gateway APIs

```text
GET /api/gateways
GET /api/gateways/{gateway_id}
```

### Recommendation APIs

```text
GET /api/recommendations
GET /api/recommendations/{gateway_id}
POST /api/recommendations/run
```

### Analytics APIs

```text
GET /api/analytics/summary
```

### Admin APIs

```text
GET /api/admin/config
GET /api/admin/audit
POST /api/admin/upload-csv
```

### Health Check

```text
GET /health
```

---

## Manual Risk Calculation

The project includes a manual risk calculator on the risk page. Users can enter values directly instead of relying only on the generated recommendation list.

Fields supported:
- failure rate (%)
- incidents in 30 days
- downtime hours in 30 days
- days since last incident

The page immediately computes:
- risk score
- priority level
- decision
- confidence
- explanation/reasons

This is useful for testing "what-if" cases and validating decisions before finalizing action.

---

## Visualization Plots

The repository includes three generated plots in `docs/plots`:

### 1. Risk priority distribution

![Gateway Risk Priority Distribution](docs/plots/risk_priority_distribution.png)

### 2. Gateway risk scores

![Gateway Risk Scores](docs/plots/gateway_risk_scores.png)

### 3. Risk components

![Normalized Risk Components](docs/plots/risk_components.png)

These plots are based on the synthetic demo dataset and are intended for demonstration, documentation, and presentation purposes.

---

## Testing

Run the project tests with:

```powershell
.\.venv312\Scripts\python.exe -m pytest -q
```

The repository includes tests for:
- API behavior
- core ranking logic
- CSV upload/import handling

---

## Notes and Limitations

- The app uses synthetic demo data by default.
- Replace the CSV with the official challenge dataset if required for final deployment.
- The scoring rules are transparent and explainable, which makes the logic easy to review and modify.
- The project is designed to support manual scenario testing and demo-style walkthroughs.

---

## Submission Checklist Summary

This repository contains:
- backend API and recommendation engine
- frontend multi-page dashboard and landing screen
- database with SQLite storage
- analytics and reporting views
- risk calculation logic and manual recalculation
- CSV upload support
- audit trail and configuration endpoints
- documentation and visualization plots

The resume file is included at the project root as:
- `23091a32c5.pdf`

---

## Final Run Command

```powershell
cd "C:\Users\reshu\Downloads\LPDG_Smart_Gateway_23091a32c5"
.\.venv312\Scripts\python.exe run.py
```

Then open the app in a web browser:
- http://127.0.0.1:8000/


##Output images pdf

https://drive.google.com/file/d/1GL6nwQUdHr-olA859IQBKpoJ_qEOeJHw/view?usp=drive_link
