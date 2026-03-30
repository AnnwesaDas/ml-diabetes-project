"""FastAPI server for diabetes predictions using pre-trained .pkl models."""

import os
import pickle
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.preprocessing import prepare_prediction_input


# Define model paths
MODEL_DIR = Path(__file__).parent / "model"
CLF_MODEL_PATH = MODEL_DIR / "classifier_model.pkl"
REG_MODEL_PATH = MODEL_DIR / "regression_model.pkl"
METADATA_PATH = MODEL_DIR / "preprocessing_metadata.pkl"

# Global model variables loaded once at startup.
clf_model = None
reg_model = None
preprocessing_metadata = None


class PredictRequest(BaseModel):
    Pregnancies: float = Field(ge=0, le=30)
    Glucose: float = Field(ge=0, le=300)
    BloodPressure: float = Field(ge=0, le=200)
    SkinThickness: float = Field(ge=0, le=120)
    Insulin: float = Field(ge=0, le=1200)
    BMI: float = Field(ge=0, le=100)
    DiabetesPedigreeFunction: float = Field(ge=0, le=5)
    Age: float = Field(ge=1, le=120)


class PredictResponse(BaseModel):
    predicted_outcome: int
    predicted_outcome_label: str
    estimated_glucose: float


def load_models():
    """Load trained models and preprocessing artifacts from .pkl files."""
    global clf_model, reg_model, preprocessing_metadata

    try:
        with open(CLF_MODEL_PATH, "rb") as f:
            clf_model = pickle.load(f)
        with open(REG_MODEL_PATH, "rb") as f:
            reg_model = pickle.load(f)
        with open(METADATA_PATH, "rb") as f:
            preprocessing_metadata = pickle.load(f)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Model artifact not found. Run 'python train_model.py' before starting the API."
        ) from exc


def _ensure_models_loaded():
    if clf_model is None or reg_model is None or preprocessing_metadata is None:
        raise HTTPException(status_code=503, detail="Models are not loaded.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Load model artifacts once at startup; never retrain in request path.
    load_models()
    yield


app = FastAPI(title="Diabetes Prediction API", version="1.0.0", lifespan=lifespan)

# CORS setup for local development + Vercel deployments.
origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
allow_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    _ensure_models_loaded()
    return {
        "status": "ok",
        "models_loaded": True,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    _ensure_models_loaded()

    try:
        processed = prepare_prediction_input(payload.model_dump(), preprocessing_metadata)
        outcome_pred = int(clf_model.predict(processed["clf_input"])[0])
        glucose_pred = float(reg_model.predict(processed["reg_input"])[0])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {
        "predicted_outcome": outcome_pred,
        "predicted_outcome_label": "Diabetic" if outcome_pred == 1 else "Non-Diabetic",
        "estimated_glucose": glucose_pred,
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
