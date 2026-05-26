"""
Central configuration loaded from environment variables.
Using pydantic-settings keeps config validated and typed.
"""

import json
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MODEL_PATH: str = "artifacts/model/pipeline.pkl"
    EXPLAINER_PATH: str = "artifacts/model/shap_explainer.pkl"
    THRESHOLD_PATH: str = "artifacts/model/threshold.json"
    DEBUG: bool = False

    class Config:
        env_file = "api/.env"


settings = Settings()