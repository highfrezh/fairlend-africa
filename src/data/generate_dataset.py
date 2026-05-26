"""
Synthetic dataset generator for FairLend-Africa.

Design rationale:
- Features are drawn from distributions calibrated to represent
  behavioral patterns observed in mobile money literature
  (Suri & Jack 2016; Lauer & Lyman 2015)
- Feature correlations are constructed deliberately to reflect
  real creditworthiness signals, not random noise
- Protected attributes (region, gender) are included for
  fairness analysis but are NOT used as predictive features
- Label generation uses a logistic model over behavioral features
  to ensure statistical separability without perfect prediction
"""

import numpy as np
import pandas as pd
from scipy.special import expit  # sigmoid
import argparse


SEED = 42
rng = np.random.default_rng(SEED)

REGIONS = ["West Africa", "East Africa", "Southern Africa", "Central Africa"]
GENDERS = ["Male", "Female", "Prefer not to say"]
OCCUPATIONS = ["Trader", "Farmer", "Informal worker", "Salaried", "Self-employed"]


def generate_dataset(n: int = 10_000) -> pd.DataFrame:
    """
    Generate a synthetic dataset representing African alternative
    financial behavior for credit scoring research.

    Returns
    -------
    pd.DataFrame with shape (n, 20) containing behavioral features,
    demographic attributes, and a binary repayment label.
    """

    # --- Demographic attributes (for fairness analysis only) ---
    region = rng.choice(REGIONS, size=n, p=[0.35, 0.30, 0.20, 0.15])
    gender = rng.choice(GENDERS, size=n, p=[0.52, 0.44, 0.04])
    age = rng.integers(18, 65, size=n)
    occupation = rng.choice(OCCUPATIONS, size=n, p=[0.30, 0.25, 0.20, 0.15, 0.10])

    # --- Mobile money transaction behavior ---
    # Higher-income proxies: more transactions, higher amounts
    income_proxy = rng.beta(2, 5, size=n)  # skewed toward lower end

    monthly_txn_count = np.round(
        rng.poisson(lam=income_proxy * 40 + 5, size=n)
    ).clip(1, 120)

    avg_txn_amount_usd = np.round(
        rng.lognormal(mean=np.log(20 + income_proxy * 100), sigma=0.6, size=n), 2
    )

    wallet_balance_trend = np.round(
        rng.normal(loc=income_proxy * 2 - 0.5, scale=0.6, size=n), 3
    )  # normalized: positive = growing balance

    # --- Airtime recharge patterns ---
    # Stress signal: small, frequent recharges near payment dates
    airtime_recharge_freq = np.round(
        rng.poisson(lam=8 + income_proxy * 20, size=n)
    ).clip(1, 60)

    airtime_avg_amount_usd = np.round(
        rng.lognormal(mean=np.log(1.5 + income_proxy * 5), sigma=0.5, size=n), 2
    )

    # --- Savings behavior ---
    has_savings_account = rng.binomial(1, p=0.3 + income_proxy * 0.4, size=n)

    savings_consistency_score = np.where(
        has_savings_account,
        np.round(rng.beta(3, 2, size=n) * 100),
        np.round(rng.beta(1, 4, size=n) * 30),
    )  # 0-100 score

    monthly_savings_usd = np.where(
        has_savings_account,
        np.round(rng.lognormal(mean=np.log(10 + income_proxy * 50), sigma=0.5, size=n), 2),
        0.0,
    )

    # --- Loan repayment history (prior loans, if any) ---
    has_prior_loan = rng.binomial(1, p=0.45, size=n)

    prior_loan_repayment_rate = np.where(
        has_prior_loan,
        np.round(rng.beta(5 + income_proxy * 3, 2, size=n), 3),
        np.nan,
    )

    days_late_avg = np.where(
        has_prior_loan,
        np.round(rng.exponential(scale=(1 - income_proxy) * 15 + 1, size=n), 1),
        np.nan,
    )

    # --- Financial activity composite signals ---
    network_diversity_score = np.round(
        rng.beta(2 + income_proxy * 3, 3, size=n) * 100
    )  # unique counterparties as a diversity score

    bill_payment_regularity = np.round(
        rng.beta(2 + income_proxy * 4, 2, size=n) * 100
    )  # regularity of utility/rent payments

    merchant_payment_count = np.round(
        rng.poisson(lam=income_proxy * 15 + 1, size=n)
    ).clip(0, 80)

    # --- Loan request features ---
    loan_amount_requested_usd = np.round(
        rng.lognormal(mean=np.log(150 + income_proxy * 500), sigma=0.7, size=n), 2
    )

    loan_duration_weeks = rng.choice([4, 8, 12, 24, 52], size=n, p=[0.25, 0.30, 0.25, 0.15, 0.05])

    # --- Construct repayment label via logistic model ---
    # This ensures label has realistic statistical relationship to features
    # Coefficients reflect hypothesized behavioral credit signals
    log_odds = (
        0.0                                      # intercept
        + 0.8  * wallet_balance_trend            # growing balance → positive
        + 0.5  * (monthly_txn_count / 120)       # normalized txn frequency
        + 0.6  * (savings_consistency_score / 100)
        + 0.7  * has_savings_account
        + 0.4  * (airtime_recharge_freq / 60)
        + 0.9  * np.where(has_prior_loan, prior_loan_repayment_rate, 0.5)
        - 0.6  * np.where(has_prior_loan, days_late_avg / 30, 0.2)
        + 0.3  * (bill_payment_regularity / 100)
        + 0.2  * (network_diversity_score / 100)
        - 0.4  * (loan_amount_requested_usd / loan_amount_requested_usd.max())
        + rng.normal(0, 0.3, size=n)             # irreducible noise
    )

    repayment_probability = expit(log_odds)
    repaid = rng.binomial(1, p=repayment_probability, size=n)

    # --- Assemble DataFrame ---
    df = pd.DataFrame({
        # Demographics (fairness analysis only — NOT model features)
        "region": region,
        "gender": gender,
        "age": age,
        "occupation": occupation,

        # Behavioral features (model inputs)
        "monthly_txn_count": monthly_txn_count,
        "avg_txn_amount_usd": avg_txn_amount_usd,
        "wallet_balance_trend": wallet_balance_trend,
        "airtime_recharge_freq": airtime_recharge_freq,
        "airtime_avg_amount_usd": airtime_avg_amount_usd,
        "has_savings_account": has_savings_account,
        "savings_consistency_score": savings_consistency_score,
        "monthly_savings_usd": monthly_savings_usd,
        "has_prior_loan": has_prior_loan,
        "prior_loan_repayment_rate": prior_loan_repayment_rate,
        "days_late_avg": days_late_avg,
        "network_diversity_score": network_diversity_score,
        "bill_payment_regularity": bill_payment_regularity,
        "merchant_payment_count": merchant_payment_count,
        "loan_amount_requested_usd": loan_amount_requested_usd,
        "loan_duration_weeks": loan_duration_weeks,

        # Target variable
        "repaid": repaid,
    })

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--output", type=str, default="data/synthetic/fairlend_dataset.csv")
    args = parser.parse_args()

    df = generate_dataset(n=args.n)
    df.to_csv(args.output, index=False)

    print(f"Generated {len(df):,} rows → {args.output}")
    print(f"Repayment rate: {df['repaid'].mean():.2%}")
    print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")