/**
 * Borrower input form.
 * Collects all 16 raw behavioral features.
 * Engineered features are computed server-side.
 */

const DEFAULTS = {
  monthly_txn_count:         25,
  avg_txn_amount_usd:        18.5,
  wallet_balance_trend:       0.4,
  airtime_recharge_freq:     12,
  airtime_avg_amount_usd:     2.5,
  has_savings_account:        1,
  savings_consistency_score: 72,
  monthly_savings_usd:       15,
  has_prior_loan:             1,
  prior_loan_repayment_rate:  0.92,
  days_late_avg:              2.1,
  network_diversity_score:   65,
  bill_payment_regularity:   80,
  merchant_payment_count:    10,
  loan_amount_requested_usd: 200,
  loan_duration_weeks:       12,
}

const FIELDS = [
  { key: "monthly_txn_count",         label: "Monthly transactions",         type: "number", step: 1,    min: 1,   max: 120  },
  { key: "avg_txn_amount_usd",        label: "Avg transaction (USD)",        type: "number", step: 0.01, min: 0.01           },
  { key: "wallet_balance_trend",      label: "Wallet balance trend",         type: "number", step: 0.01, min: -3,  max: 3    },
  { key: "airtime_recharge_freq",     label: "Airtime recharges / month",    type: "number", step: 1,    min: 1,   max: 60   },
  { key: "airtime_avg_amount_usd",    label: "Avg airtime amount (USD)",     type: "number", step: 0.01, min: 0.01           },
  { key: "has_savings_account",       label: "Has savings account (0/1)",    type: "number", step: 1,    min: 0,   max: 1    },
  { key: "savings_consistency_score", label: "Savings consistency (0–100)",  type: "number", step: 0.1,  min: 0,   max: 100  },
  { key: "monthly_savings_usd",       label: "Monthly savings (USD)",        type: "number", step: 0.01, min: 0              },
  { key: "has_prior_loan",            label: "Has prior loan (0/1)",         type: "number", step: 1,    min: 0,   max: 1    },
  { key: "prior_loan_repayment_rate", label: "Prior repayment rate (0–1)",   type: "number", step: 0.01, min: 0,   max: 1    },
  { key: "days_late_avg",             label: "Avg days late",                type: "number", step: 0.1,  min: 0              },
  { key: "network_diversity_score",   label: "Network diversity (0–100)",    type: "number", step: 0.1,  min: 0,   max: 100  },
  { key: "bill_payment_regularity",   label: "Bill payment regularity (0–100)", type: "number", step: 0.1, min: 0, max: 100 },
  { key: "merchant_payment_count",    label: "Merchant payments / month",    type: "number", step: 1,    min: 0,   max: 80   },
  { key: "loan_amount_requested_usd", label: "Loan amount requested (USD)",  type: "number", step: 1,    min: 1              },
  { key: "loan_duration_weeks",       label: "Loan duration (weeks)",        type: "number", step: 1,    min: 4,   max: 52   },
]

export default function BorrowerForm({ onSubmit, loading }) {
  const [form, setForm] = useState(DEFAULTS)

  function handleChange(e) {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: parseFloat(value) }))
  }

  function handleSubmit(e) {
    e.preventDefault()
    const payload = { ...form }
    if (!payload.has_prior_loan) {
      delete payload.prior_loan_repayment_rate
      delete payload.days_late_avg
    }
    onSubmit(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {FIELDS.map(field => (
          <div key={field.key}>
            <label className="block text-xs text-gray-500 mb-1">
              {field.label}
            </label>
            <input
              type={field.type}
              name={field.key}
              value={form[field.key] ?? ""}
              onChange={handleChange}
              step={field.step}
              min={field.min}
              max={field.max}
              className="w-full border border-gray-200 rounded-lg px-3 py-2
                         text-sm focus:outline-none focus:ring-2
                         focus:ring-brand-blue focus:border-transparent"
              required
            />
          </div>
        ))}
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-white border-2 border-brand-green text-brand-green py-3 rounded-lg
                   font-medium text-sm hover:bg-brand-green hover:text-white transition-all
                   disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Analysing..." : "Assess creditworthiness"}
      </button>
    </form>
  )
}

import { useState } from "react"