"""
Preprocessing utilities for the diabetes prediction pipeline.
Handles data cleaning, feature engineering, and encoding.
"""

import numpy as np
import pandas as pd


ZERO_INVALID_COLS = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
AGE_BINS = [20, 30, 40, 50, 60, 100]
AGE_LABELS = ["20s", "30s", "40s", "50s", "60+"]


def _build_feature_lists(age_group_cols):
    """Build ordered feature lists for classifier and regressor."""
    clf_features = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age",
    ] + age_group_cols

    reg_features = [
        "Pregnancies",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age",
    ] + age_group_cols

    return clf_features, reg_features


def preprocess_data(df, fit=False, artifacts=None):
    """
    Preprocess diabetes dataset.
    
    Args:
        df: Input DataFrame with raw features
        fit: If True, fit and return preprocessing artifacts
        artifacts: Saved preprocessing artifacts for inference transforms
    
    Returns:
        df_processed: Processed and encoded DataFrame
        clf_features: Feature names for classification model
        reg_features: Feature names for regression model
        metadata: Dict with preprocessing artifacts (only if fit=True)
    """

    # Create a copy to avoid modifying original
    df = df.copy()

    # 1) Replace clinically invalid zeros with NaN.
    for col in ZERO_INVALID_COLS:
        df[col] = df[col].replace(0, np.nan)

    # 2) Use training medians when provided; otherwise fit from current dataframe.
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if artifacts is not None:
        numeric_medians = artifacts["numeric_medians"]
        for col in numeric_cols:
            if col in numeric_medians:
                df[col] = df[col].fillna(numeric_medians[col])
    else:
        numeric_medians = df[numeric_cols].median().to_dict()
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # 3) Build age groups using stable bins/labels.
    age_bins = AGE_BINS if artifacts is None else artifacts["age_bins"]
    age_labels = AGE_LABELS if artifacts is None else artifacts["age_labels"]

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=age_bins,
        labels=age_labels,
        include_lowest=True,
    )

    # 4) One-hot encode age buckets.
    df_encoded = pd.get_dummies(df, columns=["AgeGroup"], drop_first=False, dtype=int)
    if artifacts is not None:
        age_group_cols = artifacts["age_group_cols"]
        for col in age_group_cols:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
    else:
        age_group_cols = [f"AgeGroup_{label}" for label in age_labels]
        for col in age_group_cols:
            if col not in df_encoded.columns:
                df_encoded[col] = 0

    clf_features, reg_features = _build_feature_lists(age_group_cols)

    if fit:
        metadata = {
            "age_bins": age_bins,
            "age_labels": age_labels,
            "numeric_medians": numeric_medians,
            "zero_invalid_cols": ZERO_INVALID_COLS,
            "age_group_cols": age_group_cols,
            "clf_features": clf_features,
            "reg_features": reg_features,
        }
        return df_encoded, clf_features, reg_features, metadata

    return df_encoded, clf_features, reg_features


def prepare_prediction_input(data_dict, metadata):
    """
    Prepare a single prediction input from a dictionary.
    
    Args:
        data_dict: Dictionary with patient features
        metadata: Preprocessing metadata (contains age_bins, age_labels, feature names)
    
    Returns:
        dict with keys "clf_input" and "reg_input" containing processed DataFrames
    """
    
    clf_features = metadata["clf_features"]
    reg_features = metadata["reg_features"]

    row_df = pd.DataFrame(
        [
            {
                "Pregnancies": float(data_dict.get("Pregnancies", 0)),
                "Glucose": float(data_dict.get("Glucose", 0)),
                "BloodPressure": float(data_dict.get("BloodPressure", 0)),
                "SkinThickness": float(data_dict.get("SkinThickness", 0)),
                "Insulin": float(data_dict.get("Insulin", 0)),
                "BMI": float(data_dict.get("BMI", 0)),
                "DiabetesPedigreeFunction": float(data_dict.get("DiabetesPedigreeFunction", 0)),
                "Age": float(data_dict.get("Age", 0)),
            }
        ]
    )

    transformed_df, _, _ = preprocess_data(row_df, fit=False, artifacts=metadata)

    # Reorder columns to match training features exactly.
    clf_df = transformed_df[clf_features]
    reg_df = transformed_df[reg_features]

    return {
        "clf_input": clf_df,
        "reg_input": reg_df,
    }
