"""
/evaluate endpoint
Returns model performance metrics.
Used by the frontend dashboard to display model context.
"""

from fastapi import APIRouter, HTTPException
from api.schemas import EvaluationResponse
import api.ml_models as ml

router = APIRouter()

# Cached results from notebook 04 — avoids rerunning evaluation on every call
EVALUATION_RESULTS = {
    "model_version": "fairlend-xgboost-v1",
    "roc_auc":       0.7137,
    "accuracy":      0.6200,
    "precision":     0.8600,
    "recall":        0.6000,
    "f1":            0.7100,
    "test_set_size": 2000,
    "feature_count": 20,
}


@router.get("/evaluate", response_model=EvaluationResponse)
def evaluate():
    """
    Returns cached model evaluation metrics.
    These are fixed from the training run in notebook 04
    and serve as model documentation for the frontend.
    """
    try:
        return EvaluationResponse(
            **EVALUATION_RESULTS,
            threshold=ml.threshold,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))