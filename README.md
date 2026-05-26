# FairLend-Africa

An explainable machine learning framework for alternative credit
scoring using behavioral financial data in financially excluded
African communities.

> **Research demonstration project** — not for production use.
> Built as part of an academic research portfolio on AI for
> African financial inclusion.

---

## Overview

Conventional credit scoring systems exclude millions of Africans
who lack formal credit histories. FairLend-Africa investigates
whether behavioral financial data — mobile money transactions,
airtime recharge patterns, savings consistency, and bill payment
regularity — can serve as statistically valid proxies for
creditworthiness, while remaining explainable and fair.

**Key results:**
- ROC-AUC of **0.7137** on held-out test set
- **Zero fairness violations** across regional and gender subgroups
- SHAP explainability at both global and individual borrower level
- Full REST API + interactive dashboard

---

## Research findings

| Metric | Value |
|---|---|
| ROC-AUC | 0.7137 |
| Precision | 0.860 |
| Recall | 0.600 |
| F1-Score | 0.710 |
| Top feature | wallet_balance_trend (SHAP: 0.377) |
| Fairness violations | 0 across all groups |
| Dataset size | 10,000 synthetic borrower records |
| Model features | 20 behavioral features |

---

## Project structure

```
fairlend-africa/
├── data/
│   ├── synthetic/          # generated dataset (CSV)
│   └── processed/          # feature-engineered dataset
├── notebooks/
│   ├── 01_dataset_generation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_shap_analysis.ipynb
│   └── 06_fairness_analysis.ipynb
├── src/
│   ├── data/generate_dataset.py
│   ├── features/engineer_features.py
│   ├── models/train.py
│   ├── explainability/shap_analysis.py
│   └── fairness/fairness_metrics.py
├── api/
│   ├── main.py
│   ├── schemas.py
│   ├── ml_models.py
│   ├── database.py
│   └── routes/
│       ├── predict.py
│       ├── explain.py
│       └── evaluate.py
├── frontend/               # React dashboard
├── artifacts/
│   ├── model/              # trained pipeline + SHAP explainer
│   ├── eda/                # EDA plots
│   ├── evaluation/         # model evaluation charts
│   ├── shap/               # SHAP visualizations
│   └── fairness/           # fairness analysis charts
├── paper/
│   └── fairlend_africa.pdf  # research paper
├── requirements.txt
└── docker-compose.yml
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/[your-username]/fairlend-africa.git
cd fairlend-africa
```

### 2. Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Generate the dataset

```bash
python src/data/generate_dataset.py --n 10000
```

### 4. Run the notebooks in order

```
notebooks/01_dataset_generation.ipynb
notebooks/02_eda.ipynb
notebooks/03_feature_engineering.ipynb
notebooks/04_model_training.ipynb
notebooks/05_shap_analysis.ipynb
notebooks/06_fairness_analysis.ipynb
```

### 5. Set up the database

```bash
psql -U postgres -c "CREATE DATABASE fairlend;"
```

### 6. Configure environment variables

```bash
cp api/.env.example api/.env
# Edit api/.env with your database credentials
```

### 7. Start the API

```bash
uvicorn api.main:app --reload --port 8001
```

API documentation available at `http://localhost:8001/docs`

### 8. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at `http://localhost:5173`

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/predict` | Credit decision for a borrower |
| POST | `/api/v1/explain` | Prediction + SHAP explanation |
| GET | `/api/v1/evaluate` | Model performance metrics |
| GET | `/health` | API health check |

### Example request

```bash
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_txn_count": 25,
    "avg_txn_amount_usd": 18.5,
    "wallet_balance_trend": 0.4,
    "airtime_recharge_freq": 12,
    "airtime_avg_amount_usd": 2.5,
    "has_savings_account": 1,
    "savings_consistency_score": 72.0,
    "monthly_savings_usd": 15.0,
    "has_prior_loan": 1,
    "prior_loan_repayment_rate": 0.92,
    "days_late_avg": 2.1,
    "network_diversity_score": 65.0,
    "bill_payment_regularity": 80.0,
    "merchant_payment_count": 10,
    "loan_amount_requested_usd": 200.0,
    "loan_duration_weeks": 12
  }'
```

### Example response

```json
{
  "borrower_id": null,
  "repayment_probability": 0.7428,
  "credit_score": 708,
  "recommendation": "Approve with monitoring",
  "risk_tier": "Medium Risk",
  "threshold_used": 0.1512
}
```

---

## Tech stack

| Layer | Technology |
|---|---|
| ML model | XGBoost |
| Explainability | SHAP |
| Data processing | pandas, scikit-learn |
| Backend API | FastAPI |
| Database | PostgreSQL |
| Frontend | React, Tailwind CSS, Recharts |
| Environment | Python 3.10+, venv |

---

## Behavioral features

The model uses 20 features — 16 raw behavioral indicators
and 4 engineered composite features. Demographic attributes
(region, gender, age, occupation) are **excluded from model
inputs** and retained only for fairness auditing.

| Feature group | Features |
|---|---|
| Mobile money | transaction count, avg amount, wallet balance trend |
| Airtime | recharge frequency, avg recharge amount |
| Savings | account ownership, consistency score, monthly amount |
| Credit history | prior loan flag, repayment rate, days late |
| Payments | network diversity, bill regularity, merchant count |
| Loan request | amount requested, duration |
| Engineered | txn_intensity, savings_commitment_ratio, airtime_stability, no_prior_loan_flag |

---

## Fairness analysis

The model was audited across regional and gender subgroups
using three criteria from the algorithmic fairness literature:
demographic parity, equal opportunity, and predictive parity.

All disparity ratios exceeded the 0.80 threshold across every
group and every criterion. Proxy analysis confirmed that the
top behavioral features have negligible correlation with
demographic group membership (max |r| = 0.054).

---

## Research paper

The full research paper is available at:
- `paper/fairlend_africa.md` — in this repository
- arXiv preprint: [link when published]

**Citation:**
```
Olabintan, I. (2024). FairLend-Africa: An Explainable Machine
Learning Framework for Alternative Credit Scoring Using Behavioral
Financial Data in Financially Excluded African Communities.
Kebbi State University of Science and Technology Aliero.
```

---

## Reproducing the results

All results in the paper are fully reproducible by running
the six notebooks in order from a fresh environment.
The dataset generation uses a fixed random seed (42).
The model training uses a fixed random seed (42).
No external data sources are required.

```bash
# Full reproduction from scratch
python src/data/generate_dataset.py --n 10000
jupyter nbconvert --to notebook --execute notebooks/01_dataset_generation.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_eda.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_feature_engineering.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_model_training.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_shap_analysis.ipynb
jupyter nbconvert --to notebook --execute notebooks/06_fairness_analysis.ipynb
```

---

## Limitations

- Dataset is synthetic — validation on real mobile money data
  is required before deployment claims can be made
- Fairness results reflect the synthetic data's designed
  demographic independence — real-world fairness properties
  may differ
- Model has not been evaluated for temporal stability
  or concept drift

---

## Author

**Ibraheem Olabintan**
Department of Computer Science
Kebbi State University of Science and Technology.
Aliero, Kebbi State, Nigeria

---

## License

MIT License — see `LICENSE` file for details.

*Research demonstration project.
Not intended for production credit decisioning.*
```

---

## Three small files to create alongside the README

**`LICENSE`** — create this file in your project root:

```
MIT License

Copyright (c) 2024 Ibraheem Olabintan

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
```
