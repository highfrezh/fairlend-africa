/**
 * Displays model evaluation metrics in a card grid.
 * Gives the loan officer context about model reliability.
 */

export default function ModelMetrics({ metrics }) {
  const cards = [
    { label: "ROC-AUC",   value: metrics.roc_auc,   fmt: v => v.toFixed(4) },
    { label: "Precision", value: metrics.precision,  fmt: v => (v * 100).toFixed(1) + "%" },
    { label: "Recall",    value: metrics.recall,     fmt: v => (v * 100).toFixed(1) + "%" },
    { label: "F1-Score",  value: metrics.f1,         fmt: v => v.toFixed(4) },
  ]

  return (
    <div>
      <p className="text-xs text-gray-500 mb-3">
        Model performance on held-out test set (n={metrics.test_set_size?.toLocaleString()})
      </p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {cards.map(card => (
          <div key={card.label}
               className="bg-gray-50 rounded-lg p-3 text-center border border-gray-100">
            <p className="text-xs text-gray-400 mb-1">{card.label}</p>
            <p className="text-xl font-semibold text-gray-800">
              {card.fmt(card.value)}
            </p>
          </div>
        ))}
      </div>
      <p className="text-xs text-gray-400 mt-3">
        Features: {metrics.feature_count} behavioral indicators ·
        Threshold: {metrics.threshold?.toFixed(4)} ·
        Version: {metrics.model_version}
      </p>
    </div>
  )
}