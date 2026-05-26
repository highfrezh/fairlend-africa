/**
 * Displays static model evaluation charts on the metrics tab.
 * These are the actual artifacts from the research notebooks,
 * making the dashboard a live research demonstration.
 */

export default function ModelVisuals() {
  const charts = [
    {
      src:     "/roc_curve.png",
      title:   "ROC curve",
      caption: "AUC = 0.7137 on held-out test set (n=2,000)",
    },
    {
      src:     "/beeswarm.png",
      title:   "SHAP beeswarm",
      caption: "Feature impact across all test borrowers",
    },
    {
      src:     "/model_comparison.png",
      title:   "Model comparison",
      caption: "Baseline vs tuned vs optimal threshold",
    },
  ]

  return (
    <div className="mt-6 space-y-6">
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
        Model evaluation charts
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {charts.map(chart => (
          <div key={chart.title}
               className="border border-gray-200 rounded-xl overflow-hidden bg-white">
            <img
              src={chart.src}
              alt={chart.title}
              className="w-full object-contain p-2"
            />
            <div className="px-3 pb-3">
              <p className="text-xs font-medium text-gray-700">
                {chart.title}
              </p>
              <p className="text-xs text-gray-400 mt-0.5">
                {chart.caption}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}