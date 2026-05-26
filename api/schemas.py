"""
Request and response schemas for FairLend API.
All monetary values are in USD for consistency.
"""

from pydantic import BaseModel, Field
from typing import Optional


class BorrowerInput(BaseModel):
    """
    Raw behavioral data submitted for credit assessment.
    Optional fields represent borrowers with no prior loan history.
    """
    monthly_txn_count:          int   = Field(..., ge=1,  le=120,    description="Monthly mobile money transaction count")
    avg_txn_amount_usd:         float = Field(..., gt=0,             description="Average transaction amount (USD)")
    wallet_balance_trend:       float = Field(..., ge=-3, le=3,      description="Normalized wallet balance trend (-3 to 3)")
    airtime_recharge_freq:      int   = Field(..., ge=1,  le=60,     description="Monthly airtime recharge frequency")
    airtime_avg_amount_usd:     float = Field(..., gt=0,             description="Average airtime recharge amount (USD)")
    has_savings_account:        int   = Field(..., ge=0,  le=1,      description="Has savings account (0/1)")
    savings_consistency_score:  float = Field(..., ge=0,  le=100,    description="Savings consistency score (0-100)")
    monthly_savings_usd:        float = Field(..., ge=0,             description="Monthly savings amount (USD)")
    has_prior_loan:             int   = Field(..., ge=0,  le=1,      description="Has prior loan history (0/1)")
    prior_loan_repayment_rate:  Optional[float] = Field(None, ge=0, le=1, description="Prior loan repayment rate (0-1), null if no history")
    days_late_avg:              Optional[float] = Field(None, ge=0,  description="Average days late on payments, null if no history")
    network_diversity_score:    float = Field(..., ge=0,  le=100,    description="Unique counterparty diversity score (0-100)")
    bill_payment_regularity:    float = Field(..., ge=0,  le=100,    description="Bill payment regularity score (0-100)")
    merchant_payment_count:     int   = Field(..., ge=0,  le=80,     description="Monthly merchant payment count")
    loan_amount_requested_usd:  float = Field(..., gt=0,             description="Requested loan amount (USD)")
    loan_duration_weeks:        int   = Field(..., ge=4,  le=52,     description="Requested loan duration (weeks)")

    class Config:
        json_schema_extra = {
            "example": {
                "monthly_txn_count":         25,
                "avg_txn_amount_usd":         18.5,
                "wallet_balance_trend":        0.4,
                "airtime_recharge_freq":       12,
                "airtime_avg_amount_usd":       2.5,
                "has_savings_account":          1,
                "savings_consistency_score":   72.0,
                "monthly_savings_usd":         15.0,
                "has_prior_loan":               1,
                "prior_loan_repayment_rate":    0.92,
                "days_late_avg":                2.1,
                "network_diversity_score":     65.0,
                "bill_payment_regularity":     80.0,
                "merchant_payment_count":      10,
                "loan_amount_requested_usd":  200.0,
                "loan_duration_weeks":         12,
            }
        }


class PredictionResponse(BaseModel):
    borrower_id:          Optional[str]
    repayment_probability: float
    credit_score:          int
    recommendation:        str
    risk_tier:             str
    threshold_used:        float


class ExplanationResponse(BaseModel):
    borrower_id:           Optional[str]
    repayment_probability: float
    recommendation:        str
    top_positive_factors:  list[dict]
    top_negative_factors:  list[dict]
    all_shap_values:       dict
    base_value:            float


class EvaluationResponse(BaseModel):
    model_version:  str
    roc_auc:        float
    accuracy:       float
    precision:      float
    recall:         float
    f1:             float
    threshold:      float
    test_set_size:  int
    feature_count:  int