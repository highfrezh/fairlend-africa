"""
/predict endpoint
Accepts borrower behavioral data, returns credit decision.
"""

import json
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas  import BorrowerInput, PredictionResponse
from api.database import get_db, PredictionLog
import api.ml_models as ml

router = APIRouter()


def probability_to_credit_score(prob: float) -> int:
    """
    Maps repayment probability to a 300-850 credit score range.
    This mirrors the FICO scale for interpretability,
    while remaining clearly distinct from it.
    """
    return int(300 + (prob * 550))


def get_risk_tier(prob: float) -> tuple[str, str]:
    """Returns (recommendation, risk_tier) based on probability."""
    if prob >= 0.75:
        return "Approve",           "Low Risk"
    elif prob >= 0.50:
        return "Approve with monitoring", "Medium Risk"
    elif prob >= 0.25:
        return "Manual review",     "High Risk"
    else:
        return "Decline",           "Very High Risk"


@router.post("/predict", response_model=PredictionResponse)
def predict(
    borrower: BorrowerInput,
    db: Session = Depends(get_db)
):
    """
    Returns credit decision for a borrower based on
    behavioral financial features.
    """
    try:
        features = ml.compute_features(borrower.model_dump())
        proba    = float(ml.pipeline.predict_proba(features)[0][1])
        score    = probability_to_credit_score(proba)
        rec, tier = get_risk_tier(proba)

        # Log to database
        log = PredictionLog(
            borrower_id           = borrower.model_dump().get("borrower_id"),
            repayment_probability = proba,
            credit_score          = score,
            recommendation        = rec,
            risk_tier             = tier,
            input_data            = json.dumps(borrower.model_dump()),
            shap_values           = "{}",
        )
        db.add(log)
        db.commit()

        return PredictionResponse(
            borrower_id           = None,
            repayment_probability = round(proba, 4),
            credit_score          = score,
            recommendation        = rec,
            risk_tier             = tier,
            threshold_used        = ml.threshold,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))