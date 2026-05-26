/**
 * Renders SHAP explanation as a horizontal bar chart.
 * Green bars = features supporting repayment.
 * Red bars   = features indicating default risk.
 */

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer, Cell
} from "recharts"

export default function ShapChart({ explanation }) {
  const { all_shap_values, base_value, repayment_probability } = explanation

  // Sort by absolute SHAP value, take top 12
  const chartData = Object.entries(all_shap_values)
    .map(([feature, value]) => ({
      feature: feature.replace(/_/g, " "),
      value:   parseFloat(value.toFixed(4)),
      fill:    value >= 0 ? "#1D9E75" : "#E24B4A",
    }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 12)
    .reverse()  // largest at top for horizontal bar

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload?.length) return null
    const { feature, value } = payload[0].payload
    const direction = value >= 0
      ? "increases repayment probability"
      : "decreases repayment probability"
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-3 shadow text-xs">
        <p className="font-medium text-gray-800 mb-1">{feature}</p>
        <p className={value >= 0 ? "text-green-700" : "text-red-600"}>
          SHAP: {value > 0 ? "+" : ""}{value.toFixed(4)}
        </p>
        <p className="text-gray-500 mt-1">{direction}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-700">
          Feature contributions (SHAP values)
        </h3>
        <div className="flex gap-3 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-brand-green inline-block"/>
            Supports repayment
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-sm bg-brand-red inline-block"/>
            Indicates risk
          </span>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={340}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 4, right: 60, left: 160, bottom: 4 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f0efeb"/>
          <XAxis
            type="number"
            tickFormatter={v => v.toFixed(3)}
            tick={{ fontSize: 11, fill: "#888" }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="feature"
            tick={{ fontSize: 11, fill: "#555" }}
            axisLine={false}
            tickLine={false}
            width={155}
          />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine x={0} stroke="#ccc" strokeWidth={1}/>
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {chartData.map((entry, i) => (
              <Cell key={i} fill={entry.fill} opacity={0.85}/>
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-3 bg-gray-50 rounded-lg px-4 py-3 text-xs text-gray-500">
        <span className="font-medium">Base rate:</span> {base_value.toFixed(4)} →{" "}
        <span className="font-medium">Final probability:</span>{" "}
        {repayment_probability.toFixed(4)}
        <span className="ml-2 text-gray-400">
          (SHAP values sum to the difference)
        </span>
      </div>
    </div>
  )
}