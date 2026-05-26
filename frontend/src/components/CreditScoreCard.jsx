/**
 * Displays the credit score gauge and decision recommendation.
 */

export default function CreditScoreCard({ result }) {
  const { repayment_probability, credit_score, recommendation, risk_tier } = result

  const pct = Math.round(repayment_probability * 100)

  const colorMap = {
    "Approve":                  { bg: "bg-green-50",  border: "border-green-300", text: "text-green-800",  badge: "bg-green-100 text-green-800"  },
    "Approve with monitoring":  { bg: "bg-blue-50",   border: "border-blue-300",  text: "text-blue-800",   badge: "bg-blue-100 text-blue-800"    },
    "Manual review":            { bg: "bg-amber-50",  border: "border-amber-300", text: "text-amber-800",  badge: "bg-amber-100 text-amber-800"  },
    "Decline":                  { bg: "bg-red-50",    border: "border-red-300",   text: "text-red-800",    badge: "bg-red-100 text-red-800"      },
  }

  const colors = colorMap[recommendation] ?? colorMap["Manual review"]

  // Score bar width: map 300-850 to 0-100%
  const barWidth = Math.round(((credit_score - 300) / 550) * 100)

  return (
    <div className={`rounded-xl border-2 p-6 ${colors.bg} ${colors.border}`}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">
            Credit score
          </p>
          <p className={`text-5xl font-bold ${colors.text}`}>
            {credit_score}
          </p>
          <p className="text-xs text-gray-400 mt-1">Scale 300 – 850</p>
        </div>
        <div className="text-right">
          <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${colors.badge}`}>
            {risk_tier}
          </span>
          <p className={`text-lg font-semibold mt-2 ${colors.text}`}>
            {recommendation}
          </p>
        </div>
      </div>

      {/* Score bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>300</span>
          <span>850</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="h-2.5 rounded-full bg-brand-green transition-all duration-700"
            style={{ width: `${barWidth}%` }}
          />
        </div>
      </div>

      {/* Probability */}
      <div className="flex items-center justify-between bg-white bg-opacity-60
                      rounded-lg px-4 py-3">
        <span className="text-sm text-gray-600">Repayment probability</span>
        <span className={`text-2xl font-bold ${colors.text}`}>{pct}%</span>
      </div>
    </div>
  )
}