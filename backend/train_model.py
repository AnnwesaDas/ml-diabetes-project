"""
Model training script for the diabetes prediction system.
Trains both classification and regression models and saves them as pickle files.

Run this script to train models:
    python train_model.py
"""

import pickle
import sys
import warnings
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))
from utils.preprocessing import preprocess_data

warnings.filterwarnings("ignore")

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_CANDIDATES = [
    PROJECT_ROOT / "data" / "diabetes.csv",
    PROJECT_ROOT / "diabetes.csv",
]
MODEL_DIR = Path(__file__).parent / "model"
MODEL_DIR.mkdir(exist_ok=True)

# Model file paths
CLF_MODEL_PATH = MODEL_DIR / "classifier_model.pkl"
REG_MODEL_PATH = MODEL_DIR / "regression_model.pkl"
METADATA_PATH = MODEL_DIR / "preprocessing_metadata.pkl"


def resolve_dataset_path():
    """Find dataset path with backward-compatible fallback."""
    for path in DATA_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Dataset not found. Expected one of: "
        + ", ".join(str(path) for path in DATA_CANDIDATES)
    )


def train_models():
    """Train classification and regression models and save them."""
    
    print("=" * 60)
    print("DIABETES PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # 1. Load dataset
    print("\n1. Loading dataset...")
    data_path = resolve_dataset_path()
    if data_path != DATA_CANDIDATES[0]:
        print(f"   ! Using fallback dataset path: {data_path}")
    df = pd.read_csv(data_path)
    print(f"   ✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 2. Preprocess data
    print("\n2. Preprocessing data...")
    df_encoded, clf_features, reg_features, metadata = preprocess_data(df, fit=True)
    print(f"   ✓ Data preprocessed")
    print(f"   ✓ Classification features: {len(clf_features)}")
    print(f"   ✓ Regression features: {len(reg_features)}")
    
    # 3. Prepare feature matrices and target vectors
    print("\n3. Preparing features and targets...")
    X_clf = df_encoded[clf_features]
    y_clf = df_encoded["Outcome"]
    
    X_reg = df_encoded[reg_features]
    y_reg = df_encoded["Glucose"]
    
    print(f"   ✓ Classification data: X={X_clf.shape}, y={y_clf.shape}")
    print(f"   ✓ Regression data: X={X_reg.shape}, y={y_reg.shape}")
    
    # 4. Train-test split
    print("\n4. Splitting data...")
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
    )
    
    print(f"   ✓ Training set: {len(X_train_clf)} samples")
    print(f"   ✓ Testing set: {len(X_test_clf)} samples")
    
    # 5. Train regression model
    print("\n5. Training regression model (Linear Regression)...")
    reg_model = LinearRegression()
    reg_model.fit(X_train_reg, y_train_reg)
    print("   ✓ Model trained")
    
    # 6. Evaluate regression model
    print("\n6. Evaluating regression model...")
    y_pred_reg = reg_model.predict(X_test_reg)
    mse = mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)
    
    print(f"   • Mean Squared Error (MSE): {mse:.4f}")
    print(f"   • R² Score: {r2:.4f}")
    
    # 7. Train classification model
    print("\n7. Training classification model (Decision Tree)...")
    clf_model = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf_model.fit(X_train_clf, y_train_clf)
    print("   ✓ Model trained")
    
    # 8. Evaluate classification model
    print("\n8. Evaluating classification model...")
    y_pred_clf = clf_model.predict(X_test_clf)
    accuracy = accuracy_score(y_test_clf, y_pred_clf)
    cm = confusion_matrix(y_test_clf, y_pred_clf)
    
    print(f"   • Accuracy: {accuracy:.4f}")
    print(f"   • Confusion Matrix:\n{cm}")
    print(f"   • Classification Report:")
    print(
        classification_report(
            y_test_clf,
            y_pred_clf,
            target_names=["Non-Diabetic", "Diabetic"],
        )
    )
    
    # 9. Save models
    print("\n9. Saving models...")
    with open(CLF_MODEL_PATH, "wb") as f:
        pickle.dump(clf_model, f)
    print(f"   ✓ Classification model saved: {CLF_MODEL_PATH}")
    
    with open(REG_MODEL_PATH, "wb") as f:
        pickle.dump(reg_model, f)
    print(f"   ✓ Regression model saved: {REG_MODEL_PATH}")
    
    # 10. Save preprocessing metadata
    print("\n10. Saving preprocessing metadata...")
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    print(f"   ✓ Metadata saved: {METADATA_PATH}")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"\nModels saved in: {MODEL_DIR}")
    print("\nYou can now deploy the backend API with these models.")


if __name__ == "__main__":
    train_models()
