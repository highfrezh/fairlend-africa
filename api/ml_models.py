"""
ML artifact loader.
Loaded once at application startup via lifespan context manager.
Routes import the module-level objects directly.
"""

import json
import joblib
import numpy as np
from pathlib import Path


# These are populated by load_artifacts() at startup
pipeline   = None
explainer  = None
threshold  = None

FEATURE_COLS = [
    "monthly_txn_count", "avg_txn_amount_usd", "wallet_balance_trend",
    "airtime_recharge_freq", "airtime_avg_amount_usd",
    "has_savings_account", "savings_consistency_score", "monthly_savings_usd",
    "has_prior_loan", "prior_loan_repayment_rate", "days_late_avg",
    "network_diversity_score", "bill_payment_regularity",
    "merchant_payment_count", "loan_amount_requested_usd", "loan_duration_weeks",
    "txn_intensity", "savings_commitment_ratio", "airtime_stability",
    "no_prior_loan_flag",
]


def load_artifacts():
    """Called once at FastAPI startup."""
    global pipeline, explainer, threshold

    pipeline  = joblib.load("artifacts/model/pipeline.pkl")
    explainer = joblib.load("artifacts/model/shap_explainer.pkl")

    with open("artifacts/model/threshold.json") as f:
        threshold = json.load(f)["optimal_threshold"]

    print(f"✓ Pipeline loaded")
    print(f"✓ SHAP explainer loaded")
    print(f"✓ Threshold: {threshold:.4f}")


def compute_features(data: dict) -> np.ndarray:
    """
    Accepts raw borrower data dict, engineers derived features,
    returns numpy array in the correct feature order.
    """
    import numpy as np

    m  = data["monthly_txn_count"]
    a  = data["avg_txn_amount_usd"]
    ar = data["airtime_recharge_freq"]
    aa = data["airtime_avg_amount_usd"]
    ms = data["monthly_savings_usd"]
    pl = data.get("prior_loan_repayment_rate", np.nan)
    dl = data.get("days_late_avg", np.nan)

    # Engineered features — same logic as notebook 03
    txn_intensity            = round(np.log1p(m) * np.log1p(a), 4)
    savings_commitment_ratio = round(ms / (a + 1), 4)
    airtime_stability        = round(aa / (ar + 1), 4)
    no_prior_loan_flag       = 1 if np.isnan(pl) else 0

    row = [
        m, a,
        data["wallet_balance_trend"],
        ar, aa,
        data["has_savings_account"],
        data["savings_consistency_score"],
        ms,
        data["has_prior_loan"],
        pl, dl,
        data["network_diversity_score"],
        data["bill_payment_regularity"],
        data["merchant_payment_count"],
        data["loan_amount_requested_usd"],
        data["loan_duration_weeks"],
        txn_intensity,
        savings_commitment_ratio,
        airtime_stability,
        no_prior_loan_flag,
    ]

    return np.array(row, dtype=float).reshape(1, -1)