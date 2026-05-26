"""
FairLend-Africa — FastAPI application entry point.

Research demonstration system for explainable credit scoring
using behavioral financial data.

Endpoints:
  POST /predict  — credit decision
  POST /explain  — SHAP explanation
  GET  /evaluate — model metrics
  GET  /health   — liveness check
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database        import create_tables
from api.ml_models       import load_artifacts
from api.routes.predict  import router as predict_router
from api.routes.explain  import router as explain_router
from api.routes.evaluate import router as evaluate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load ML artifacts and create DB tables."""
    print("Starting FairLend-Africa API...")
    create_tables()
    load_artifacts()
    print("API ready.")
    yield
    print("Shutting down.")


app = FastAPI(
    title       = "FairLend-Africa API",
    description = (
        "Explainable ML credit scoring API for financially excluded "
        "African communities. Research demonstration system."
    ),
    version     = "1.0.0",
    lifespan    = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:5173", "http://localhost:3000"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(predict_router,  prefix="/api/v1", tags=["Prediction"])
app.include_router(explain_router,  prefix="/api/v1", tags=["Explanation"])
app.include_router(evaluate_router, prefix="/api/v1", tags=["Evaluation"])


@app.get("/health", tags=["Health"])
def health():
    return {
        "status":  "healthy",
        "model":   "fairlend-xgboost-v1",
        "version": "1.0.0",
    }