---
title: 'FairLend-Africa: An Explainable Machine Learning Framework for Alternative Credit Scoring Using Behavioral Financial Data'
tags:
  - Python
  - machine learning
  - credit scoring
  - explainable AI
  - SHAP
  - fairness
  - financial inclusion
  - Africa
  - XGBoost
authors:
  - name: Ibraheem Olabintan
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Department of Computer Science, Kebbi State University of Science and Technology Aliero, Nigeria
    index: 1
date: 2025
bibliography: paper.bib
---

# Summary

FairLend-Africa is an open-source Python framework for explainable
alternative credit scoring using behavioral financial data. The
software provides a complete, reproducible pipeline for researchers
and practitioners working on machine learning-based credit assessment
for financially excluded populations in African mobile money contexts.

The framework addresses a practical gap in the financial inclusion
research ecosystem: the absence of an accessible, open-source
implementation that combines behavioral feature engineering, gradient
boosted tree classification, SHAP-based explainability, and systematic
fairness auditing in a single deployable system. FairLend-Africa
provides this infrastructure as a research demonstration tool,
enabling microfinance institutions (MFIs) and researchers to
experiment with alternative credit scoring approaches without
requiring proprietary data partnerships or institutional cloud
resources.

# Statement of Need

Approximately 1.4 billion adults worldwide remain unbanked, with
Sub-Saharan Africa accounting for a disproportionate share
[@demirguckunt2022]. Conventional credit scoring systems exclude
individuals who lack formal credit histories, regardless of their
actual financial behavior or repayment capacity. Mobile money
platforms — including M-Pesa in Kenya and MTN Mobile Money across
West Africa — generate behavioral transaction records that prior
research has shown to carry meaningful creditworthiness signals
[@bjorkegren2018; @suri2016].

Several methodological gaps limit progress in this area. First,
existing research on alternative credit scoring rarely releases
reproducible implementations. Second, explainability requirements
for credit decisions — increasingly mandated by regulation —
are seldom integrated into published frameworks. Third, fairness
auditing across demographic subgroups is frequently omitted despite
its importance for equitable lending.

FairLend-Africa addresses all three gaps. It provides:

1. A documented synthetic data generator producing realistic
   mobile money behavioral records, enabling research without
   requiring data access agreements with telecom operators or MFIs.

2. A complete XGBoost classification pipeline with SHAP
   TreeExplainer integration, producing both global feature
   importance rankings and individual borrower explanations
   suitable for loan officer review.

3. A systematic fairness audit module evaluating demographic
   parity, equal opportunity, and predictive parity across
   regional and gender subgroups, with threshold robustness
   analysis at multiple operating points.

4. A FastAPI REST backend and React dashboard enabling
   interactive demonstration of credit decisions with
   real-time SHAP explanations.

The framework is designed for researchers in financial inclusion,
responsible AI, and alternative credit scoring, as well as
practitioners at MFIs experimenting with ML-based underwriting.

# Software Architecture


FairLend-Africa is structured as four integrated components:

**Data pipeline** (`src/data/`): A synthetic dataset generator
producing 10,000 borrower records with 16 raw behavioral features
derived from mobile money transaction patterns, airtime recharge
behavior, savings consistency, and loan repayment history. Labels
are generated via a logistic data generating process with
documented coefficients, ensuring full reproducibility
[@jordon2022].

**ML pipeline** (`src/models/`): A scikit-learn Pipeline
[@pedregosa2011] combining median imputation, standard scaling,
and XGBoost classification [@chen2016]. Hyperparameter optimization
uses RandomizedSearchCV with 5-fold stratified cross-validation.
The pipeline achieves a held-out test ROC-AUC of 0.7137, consistent
with behavioral credit scoring benchmarks [@bjorkegren2018;
@khandani2010].

**Explainability module** (`src/explainability/`): SHAP
TreeExplainer [@lundberg2017; @lundberg2020] integration providing
global feature importance via mean absolute SHAP values, beeswarm
and dependence plots, and individual waterfall explanations for
any borrower record. The module acknowledges SHAP's feature
independence assumption and its adversarial vulnerability
[@slack2020; @kumar2020].

**Fairness module** (`src/fairness/`): Systematic audit across
regional and gender subgroups evaluating demographic parity
[@dwork2012], equal opportunity [@hardt2016], and predictive
parity. Disparity ratios are reported with threshold robustness
analysis at 30%, 50%, 70%, and 100% approval rates. The
framework acknowledges Chouldechova's impossibility theorem
[@chouldechova2017] and applies the 80% rule as an international
reference benchmark.

![Global feature importance measured by mean absolute SHAP value
across all 2,000 test borrowers. Wallet balance trend dominates
all other features.\label{fig:shap}](global_importance.png)

# Example Usage

```python
# Generate synthetic dataset
from src.data.generate_dataset import generate_dataset
df = generate_dataset(n=10_000)
df.to_csv("data/synthetic/fairlend_dataset.csv", index=False)

# Train model
from src.models.train import train_and_save
train_and_save("data/synthetic/fairlend_dataset.csv")

# Start API
# uvicorn api.main:app --reload --port 8001

# Predict via API
import requests
response = requests.post(
    "http://localhost:8001/api/v1/explain",
    json={
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
    }
)
print(response.json())
```

# Reproducibility

All experiments are fully reproducible from a fixed random seed
(42) using the six Jupyter notebooks included in the repository.
The data generation process uses documented coefficients (see
Table 2 of the accompanying paper). No external data sources,
API keys, or institutional access are required.

The complete pipeline from data generation through fairness
analysis can be reproduced by running:

```bash
python src/data/generate_dataset.py --n 10000
jupyter nbconvert --to notebook --execute notebooks/01_dataset_generation.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_eda.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_feature_engineering.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_model_training.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_shap_analysis.ipynb
jupyter nbconvert --to notebook --execute notebooks/06_fairness_analysis.ipynb
```

# Research Context

The accompanying research paper describing the methodology,
experimental results, and fairness analysis is available as a
preprint [@olabintan2025zenodo; @olabintan2025ssrn]. The paper
reports a held-out test ROC-AUC of 0.7137, consistent with
comparable alternative credit scoring studies using behavioral
data [@bjorkegren2018; @khandani2010]. A logistic regression
baseline achieves near-identical performance (AUC 0.713),
suggesting that the synthetic data generating process produces
primarily linear feature relationships. Fairness auditing reveals
no demographic disparity violations under the 80% rule across
regional and gender subgroups, with the caveat that results
reflect the synthetic data's designed demographic-behavioral
independence rather than empirical claims about real borrower
populations.

# Acknowledgements

The author thanks the open-source communities behind scikit-learn,
XGBoost, SHAP, FastAPI, and React, whose tools make reproducible
ML research accessible to independent researchers.

# AI usage disclosure

AI tools were used to assist with code development and manuscript
drafting during this project. All technical content, experimental
results, and conclusions were independently verified by the author.

# References
