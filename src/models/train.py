"""
Model training pipeline for FairLend-Africa.
Uses XGBoost with scikit-learn API for compatibility with SHAP.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
)
from xgboost import XGBClassifier


FEATURE_COLS = [
    "monthly_txn_count", "avg_txn_amount_usd", "wallet_balance_trend",
    "airtime_recharge_freq", "airtime_avg_amount_usd",
    "has_savings_account", "savings_consistency_score", "monthly_savings_usd",
    "has_prior_loan", "prior_loan_repayment_rate", "days_late_avg",
    "network_diversity_score", "bill_payment_regularity",
    "merchant_payment_count", "loan_amount_requested_usd", "loan_duration_weeks",
]
TARGET_COL = "repaid"


def load_data(path: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y


def build_pipeline() -> Pipeline:
    """
    Imputation → Scaling → XGBoost.
    Imputation handles NaN in prior_loan_repayment_rate and days_late_avg
    for borrowers without prior loan history.
    """
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=1,  # adjust if class imbalance exists
            use_label_encoder=False,
            eval_metric="logloss",
            random_state=42,
        )),
    ])


def evaluate_pipeline(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    """5-fold stratified cross-validation."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    results = cross_validate(pipeline, X, y, cv=cv, scoring=scoring)
    return {
        metric: {
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
        }
        for metric, scores in results.items()
        if metric.startswith("test_")
    }


def train_and_save(data_path: str, artifact_dir: str = "artifacts/model") -> None:
    Path(artifact_dir).mkdir(parents=True, exist_ok=True)
    X, y = load_data(data_path)

    pipeline = build_pipeline()
    cv_results = evaluate_pipeline(pipeline, X, y)

    print("Cross-validation results:")
    for metric, stats in cv_results.items():
        print(f"  {metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")

    # Final fit on full training data
    pipeline.fit(X, y)
    joblib.dump(pipeline, f"{artifact_dir}/pipeline.pkl")
    print(f"\nModel saved to {artifact_dir}/pipeline.pkl")


if __name__ == "__main__":
    train_and_save("data/synthetic/fairlend_dataset.csv")