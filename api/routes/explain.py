"""
/explain endpoint
Returns SHAP-based explanation for a credit decision.
This is the core explainability contribution of the system.
"""

import json
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas  import BorrowerInput, ExplanationResponse
from api.database import get_db, PredictionLog
import api.ml_models as ml

router = APIRouter()


@router.post("/explain", response_model=ExplanationResponse)
def explain(
    borrower: BorrowerInput,
    db: Session = Depends(get_db)
):
    """
    Returns prediction + SHAP explanation for each feature.
    Separates positive factors (support repayment) from
    negative factors (indicate default risk).
    """
    try:
        features  = ml.compute_features(borrower.model_dump())
        proba     = float(ml.pipeline.predict_proba(features)[0][1])

        # Transform features through preprocessor before SHAP
        preprocessor      = ml.pipeline[:-1]
        model             = ml.pipeline[-1]
        features_transformed = preprocessor.transform(features)

        features_df = pd.DataFrame(
            features_transformed,
            columns=ml.FEATURE_COLS
        )

        # Compute SHAP values for this single borrower
        shap_vals = ml.explainer(features_df)
        sv        = shap_vals.values[0]       # shape: (n_features,)
        base_val  = float(ml.explainer.expected_value)

        # Build named SHAP dict
        shap_named = {
            feat: round(float(val), 6)
            for feat, val in zip(ml.FEATURE_COLS, sv)
        }

        # Separate positive and negative contributors
        sorted_shap = sorted(
            shap_named.items(), key=lambda x: x[1], reverse=True
        )

        positive_factors = [
            {"feature": k, "shap_value": v, "direction": "increases repayment probability"}
            for k, v in sorted_shap if v > 0
        ][:5]

        negative_factors = [
            {"feature": k, "shap_value": v, "direction": "decreases repayment probability"}
            for k, v in sorted_shap if v < 0
        ][-5:][::-1]

        rec = "Approve" if proba >= 0.75 else \
              "Approve with monitoring" if proba >= 0.50 else \
              "Manual review" if proba >= 0.25 else "Decline"

        # Update prediction log with SHAP values
        log = PredictionLog(
            repayment_probability = proba,
            credit_score          = int(300 + proba * 550),
            recommendation        = rec,
            risk_tier             = "computed",
            input_data            = json.dumps(borrower.model_dump()),
            shap_values           = json.dumps(shap_named),
        )
        db.add(log)
        db.commit()

        return ExplanationResponse(
            borrower_id           = None,
            repayment_probability = round(proba, 4),
            recommendation        = rec,
            top_positive_factors  = positive_factors,
            top_negative_factors  = negative_factors,
            all_shap_values       = shap_named,
            base_value            = round(base_val, 6),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))