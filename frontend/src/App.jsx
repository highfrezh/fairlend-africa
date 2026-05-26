/**
 * FairLend-Africa — main application component.
 * Orchestrates form, prediction, explanation, and metrics views.
 */

import { useState, useEffect } from "react"
import BorrowerForm  from "./components/BorrowerForm"
import CreditScoreCard from "./components/CreditScoreCard"
import ShapChart     from "./components/ShapChart"
import ModelMetrics  from "./components/ModelMetrics"
import ModelVisuals from "./components/ModelVisuals"
import { getPrediction, getExplanation, getEvaluation } from "./api"

export default function App() {
  const [loading,     setLoading]     = useState(false)
  const [prediction,  setPrediction]  = useState(null)
  const [explanation, setExplanation] = useState(null)
  const [metrics,     setMetrics]     = useState(null)
  const [error,       setError]       = useState(null)
  const [activeTab,   setActiveTab]   = useState("form")

  useEffect(() => {
    getEvaluation()
      .then(setMetrics)
      .catch(() => setMetrics(null))
  }, [])

  async function handleSubmit(borrowerData) {
    setLoading(true)
    setError(null)
    setPrediction(null)
    setExplanation(null)

    try {
      const [pred, expl] = await Promise.all([
        getPrediction(borrowerData),
        getExplanation(borrowerData),
      ])
      setPrediction(pred)
      setExplanation(expl)
      setActiveTab("result")
    } catch (err) {
      setError(err.response?.data?.detail ?? "API error — is the backend running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">
              FairLend-Africa
            </h1>
            <p className="text-xs text-gray-400">
              Explainable credit scoring · Research demonstration
            </p>
          </div>
          {metrics && (
            <span className="text-xs bg-green-50 text-green-700
                             border border-green-200 px-3 py-1 rounded-full">
              Model ROC-AUC {metrics.roc_auc.toFixed(3)}
            </span>
          )}
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">

        {/* Tab navigation */}
        <div className="flex gap-1 mb-6 bg-gray-100 rounded-lg p-1 w-fit">
          {[
            { id: "form",    label: "Borrower input" },
            { id: "result",  label: "Credit decision" },
            { id: "metrics", label: "Model metrics"   },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors
                ${activeTab === tab.id
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
                }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Error banner */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg px-4 py-3
                          text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Tab: Borrower input */}
        {activeTab === "form" && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-base font-medium text-gray-800 mb-1">
              Borrower behavioral data
            </h2>
            <p className="text-xs text-gray-400 mb-6">
              Enter mobile money and savings behavior to generate
              a credit assessment with SHAP explanation.
            </p>
            <BorrowerForm onSubmit={handleSubmit} loading={loading} />
          </div>
        )}

        {/* Tab: Credit decision */}
        {activeTab === "result" && (
          <div className="space-y-6">
            {prediction ? (
              <>
                <CreditScoreCard result={prediction} />

                {explanation && (
                  <div className="bg-white rounded-xl border border-gray-200 p-6">
                    <h2 className="text-base font-medium text-gray-800 mb-4">
                      Explainability — why this decision?
                    </h2>
                    <ShapChart explanation={explanation} />
                    <div className="mt-4 border border-gray-100 rounded-xl overflow-hidden">
                      <div className="px-4 py-3 bg-gray-50 border-b border-gray-100">
                        <p className="text-xs font-medium text-gray-600">
                          Sample waterfall explanation — research reference
                        </p>
                      </div>
                      <img
                        src="/waterfall_example.png"
                        alt="SHAP waterfall explanation example"
                        className="w-full object-contain p-4"
                      />
                      <p className="text-xs text-gray-400 px-4 pb-3">
                        Waterfall plots show how each feature pushes the predicted
                        probability above or below the base rate.
                      </p>
                    </div>

                    {/* Top factors summary */}
                    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-xs font-medium text-green-700 mb-2">
                          Top factors supporting repayment
                        </p>
                        <ul className="space-y-1">
                          {explanation.top_positive_factors.map((f, i) => (
                            <li key={i} className="text-xs text-gray-600 flex
                                                   items-center gap-2">
                              <span className="w-1.5 h-1.5 rounded-full
                                               bg-brand-green inline-block"/>
                              {f.feature.replace(/_/g, " ")}
                              <span className="text-green-600 ml-auto">
                                +{f.shap_value.toFixed(4)}
                              </span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <p className="text-xs font-medium text-red-700 mb-2">
                          Top risk factors
                        </p>
                        <ul className="space-y-1">
                          {explanation.top_negative_factors.map((f, i) => (
                            <li key={i} className="text-xs text-gray-600 flex
                                                   items-center gap-2">
                              <span className="w-1.5 h-1.5 rounded-full
                                               bg-brand-red inline-block"/>
                              {f.feature.replace(/_/g, " ")}
                              <span className="text-red-600 ml-auto">
                                {f.shap_value.toFixed(4)}
                              </span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                <button
                  onClick={() => setActiveTab("form")}
                  className="text-sm text-brand-blue hover:underline"
                >
                  ← Assess another borrower
                </button>
              </>
            ) : (
              <div className="bg-white rounded-xl border border-gray-200 p-12
                              text-center text-gray-400">
                <p className="text-sm">
                  No assessment yet — submit borrower data to see results.
                </p>
                <button
                  onClick={() => setActiveTab("form")}
                  className="mt-4 text-sm text-brand-blue hover:underline"
                >
                  Go to borrower input →
                </button>
              </div>
            )}
          </div>
        )}

        {/* Tab: Model metrics */}
        {activeTab === "metrics" && (
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-base font-medium text-gray-800 mb-1">
              Model evaluation
            </h2>
            <p className="text-xs text-gray-400 mb-6">
              Performance metrics from 5-fold stratified cross-validation
              and held-out test set evaluation.
            </p>
           {metrics
              ? <>
                  <ModelMetrics metrics={metrics} />
                  <ModelVisuals />
                </>
              : <p className="text-sm text-gray-400">Loading metrics...</p>
            }
          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="text-center py-8 text-xs text-gray-300">
        FairLend-Africa · Research demonstration ·
        Not for production use
      </footer>
    </div>
  )
}