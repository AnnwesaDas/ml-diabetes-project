"""
Preprocessing utilities for the diabetes prediction pipeline.
Handles data cleaning, feature engineering, and encoding.
"""

import numpy as np
import pandas as pd


def preprocess_data(df, fit=False, age_bins=None, age_labels=None):
    """
    Preprocess diabetes dataset.
    
    Args:
        df: Input DataFrame with raw features
        fit: If True, also return the age_bins and age_labels for later use
        age_bins: Pre-computed age bins (for inference)
        age_labels: Pre-computed age labels (for inference)
    
    Returns:
        df_processed: Processed and encoded DataFrame
        clf_features: Feature names for classification model
        reg_features: Feature names for regression model
        metadata: Dict with age_bins, age_labels (only if fit=True)
    """
    
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # 1. Handle invalid zeros in medical columns
    zero_invalid_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    for col in zero_invalid_cols:
        df[col] = df[col].replace(0, np.nan)
    
    # 2. Fill missing values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # 3. Create age group categorical feature
    if age_bins is None:
        age_bins = [20, 30, 40, 50, 60, 100]
        age_labels = ["20s", "30s", "40s", "50s", "60+"]
    
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=age_bins,
        labels=age_labels,
        include_lowest=True,
    )
    
    # 4. One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=["AgeGroup"], drop_first=False, dtype=int)
    age_group_cols = [col for col in df_encoded.columns if col.startswith("AgeGroup_")]
    
    # 5. Define feature sets for classification and regression
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
    
    if fit:
        metadata = {
            "age_bins": age_bins,
            "age_labels": age_labels,
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
    
    age_bins = metadata["age_bins"]
    age_labels = metadata["age_labels"]
    clf_features = metadata["clf_features"]
    reg_features = metadata["reg_features"]
    
    # Extract age and create age group
    age = data_dict["Age"]
    age_group = pd.cut(
        pd.Series([age]),
        bins=age_bins,
        labels=age_labels,
        include_lowest=True,
    ).iloc[0]
    
    # Create one-hot encoded age group columns
    age_group_encoding = {}
    for label in age_labels:
        col_name = f"AgeGroup_{label}"
        age_group_encoding[col_name] = 1 if age_group == label else 0
    
    # Prepare classification input
    clf_input_data = {
        "Pregnancies": data_dict.get("Pregnancies", 0),
        "Glucose": data_dict.get("Glucose", 0),
        "BloodPressure": data_dict.get("BloodPressure", 0),
        "SkinThickness": data_dict.get("SkinThickness", 0),
        "Insulin": data_dict.get("Insulin", 0),
        "BMI": data_dict.get("BMI", 0),
        "DiabetesPedigreeFunction": data_dict.get("DiabetesPedigreeFunction", 0),
        "Age": age,
    }
    clf_input_data.update(age_group_encoding)
    clf_df = pd.DataFrame([clf_input_data])
    
    # Prepare regression input (without Glucose feature since we're predicting it)
    reg_input_data = {
        "Pregnancies": data_dict.get("Pregnancies", 0),
        "BloodPressure": data_dict.get("BloodPressure", 0),
        "SkinThickness": data_dict.get("SkinThickness", 0),
        "Insulin": data_dict.get("Insulin", 0),
        "BMI": data_dict.get("BMI", 0),
        "DiabetesPedigreeFunction": data_dict.get("DiabetesPedigreeFunction", 0),
        "Age": age,
    }
    reg_input_data.update(age_group_encoding)
    reg_df = pd.DataFrame([reg_input_data])
    
    # Reorder columns to match training features
    clf_df = clf_df[clf_features]
    reg_df = reg_df[reg_features]
    
    return {
        "clf_input": clf_df,
        "reg_input": reg_df,
    }
