"""
Flask API server for diabetes prediction.
Loads pre-trained models and serves predictions via JSON API.

Run this server:
    python app.py

The API will be available at http://localhost:5000

Prediction endpoint:
    POST /api/predict
    Body: {
        "Pregnancies": 2,
        "Glucose": 140,
        "BloodPressure": 70,
        "SkinThickness": 30,
        "Insulin": 100,
        "BMI": 32.0,
        "DiabetesPedigreeFunction": 0.45,
        "Age": 35
    }
"""

import pickle
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.preprocessing import prepare_prediction_input

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define model paths
MODEL_DIR = Path(__file__).parent / "model"
CLF_MODEL_PATH = MODEL_DIR / "classifier_model.pkl"
REG_MODEL_PATH = MODEL_DIR / "regression_model.pkl"
METADATA_PATH = MODEL_DIR / "preprocessing_metadata.pkl"

# Global model variables
clf_model = None
reg_model = None
preprocessing_metadata = None


def load_models():
    """Load trained models from pickle files."""
    global clf_model, reg_model, preprocessing_metadata
    
    try:
        with open(CLF_MODEL_PATH, "rb") as f:
            clf_model = pickle.load(f)
        print(f"✓ Loaded classification model from {CLF_MODEL_PATH}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Classification model not found at {CLF_MODEL_PATH}. "
            "Please run 'python train_model.py' first."
        )
    
    try:
        with open(REG_MODEL_PATH, "rb") as f:
            reg_model = pickle.load(f)
        print(f"✓ Loaded regression model from {REG_MODEL_PATH}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Regression model not found at {REG_MODEL_PATH}. "
            "Please run 'python train_model.py' first."
        )
    
    try:
        with open(METADATA_PATH, "rb") as f:
            preprocessing_metadata = pickle.load(f)
        print(f"✓ Loaded preprocessing metadata from {METADATA_PATH}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Metadata not found at {METADATA_PATH}. "
            "Please run 'python train_model.py' first."
        )


def _ensure_models_loaded():
    """Fail fast if startup model loading did not complete."""
    if clf_model is None or reg_model is None or preprocessing_metadata is None:
        raise RuntimeError("Models are not loaded. Start the API after running train_model.py.")


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Diabetes Prediction API is running",
        "version": "1.0.0",
        "models": {
            "classifier": "DecisionTreeClassifier",
            "regressor": "LinearRegression"
        }
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Make a prediction using patient data.
    
    Expected JSON body:
    {
        "Pregnancies": float,
        "Glucose": float,
        "BloodPressure": float,
        "SkinThickness": float,
        "Insulin": float,
        "BMI": float,
        "DiabetesPedigreeFunction": float,
        "Age": float
    }
    
    Returns:
    {
        "success": true,
        "prediction": {
            "estimated_glucose": float,
            "diabetes_risk": "Diabetic" | "Non-Diabetic",
            "confidence": float (0-1),
            "input_data": {...}
        }
    }
    """
    
    try:
        _ensure_models_loaded()

        # Get JSON data
        data = request.get_json(force=True)
        
        # Validate required fields
        required_fields = [
            "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Prepare input data
        processed_data = prepare_prediction_input(data, preprocessing_metadata)
        
        # Get predictions
        glucose_pred = reg_model.predict(processed_data["reg_input"])[0]
        outcome_pred = clf_model.predict(processed_data["clf_input"])[0]
        
        # Get prediction probabilities for confidence
        outcome_proba = clf_model.predict_proba(processed_data["clf_input"])[0]
        confidence = float(max(outcome_proba))
        
        # Format response
        return jsonify({
            "success": True,
            "prediction": {
                "estimated_glucose": float(glucose_pred),
                "diabetes_risk": "Diabetic" if outcome_pred == 1 else "Non-Diabetic",
                "diabetes_probability": float(outcome_proba[1]),
                "confidence": float(confidence),
                "input_data": {
                    "Pregnancies": float(data["Pregnancies"]),
                    "Glucose": float(data["Glucose"]),
                    "BloodPressure": float(data["BloodPressure"]),
                    "SkinThickness": float(data["SkinThickness"]),
                    "Insulin": float(data["Insulin"]),
                    "BMI": float(data["BMI"]),
                    "DiabetesPedigreeFunction": float(data["DiabetesPedigreeFunction"]),
                    "Age": float(data["Age"])
                }
            }
        })
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Invalid input data: {str(e)}"
        }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Detailed health check endpoint."""
    return jsonify({
        "status": "healthy",
        "models_loaded": {
            "classifier": clf_model is not None,
            "regressor": reg_model is not None,
            "metadata": preprocessing_metadata is not None
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DIABETES PREDICTION API")
    print("=" * 60)
    
    try:
        load_models()
        print("\n✓ All models loaded successfully")
        print("\nStarting Flask server...")
        print("API available at: http://localhost:5000")
        print("Prediction endpoint: POST http://localhost:5000/api/predict")
        print("\nPress CTRL+C to stop the server\n")
        
        app.run(debug=True, host="0.0.0.0", port=5000)
    
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nTo fix this, run the training script first:")
        print("  python train_model.py")
        exit(1)
else:
    # Load artifacts once when imported by production servers (e.g., gunicorn).
    load_models()
