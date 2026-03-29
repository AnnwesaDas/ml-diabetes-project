import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
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

print("Libraries imported successfully!\n")

# ============================================
# MACHINE LEARNING LAB PROJECT
# Diabetes Prediction + Glucose Regression
# ============================================

# 1. LOAD DATASET
df = pd.read_csv("diabetes.csv")
print("Dataset loaded successfully!\n")
print(df.head())

# 2. DATA PREPROCESSING
print("\n--- DATA INFO ---")
print(df.info())

print("\n--- STATISTICS ---")
print(df.describe())

# Convert invalid zeros to NaN so missing-value handling is explicit and traceable.
zero_invalid_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in zero_invalid_cols:
    df[col] = df[col].replace(0, np.nan)

print("\n--- MISSING VALUES (BEFORE FILLING) ---")
print(df.isnull().sum())

numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

print("\n--- MISSING VALUES (AFTER FILLING) ---")
print(df.isnull().sum())

# Create a categorical feature so encoding is demonstrated in a beginner-friendly way.
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[20, 30, 40, 50, 60, 100],
    labels=["20s", "30s", "40s", "50s", "60+"],
    include_lowest=True,
)

print("\n--- CATEGORICAL FEATURE PREVIEW ---")
print(df[["Age", "AgeGroup"]].head())

df_encoded = pd.get_dummies(df, columns=["AgeGroup"], drop_first=False, dtype=int)
age_group_cols = [col for col in df_encoded.columns if col.startswith("AgeGroup_")]

print("\n--- ENCODING COMPLETED (get_dummies) ---")
print("Encoded columns:", age_group_cols)

print("\nData preprocessing completed!\n")

# 3. DATA VISUALIZATION
plt.figure(figsize=(8, 5))
df["Glucose"].hist(bins=20, color="steelblue", edgecolor="black")
plt.xlabel("Glucose")
plt.ylabel("Frequency")
plt.title("Distribution of Glucose")
plt.tight_layout()
plt.savefig("plot_1_glucose_histogram.png", dpi=150)
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df["BMI"], df["Glucose"], alpha=0.7, color="teal")
plt.xlabel("BMI")
plt.ylabel("Glucose")
plt.title("BMI vs Glucose")
plt.tight_layout()
plt.savefig("plot_2_bmi_vs_glucose_scatter.png", dpi=150)
plt.show()

plt.figure(figsize=(10, 7))
sns.heatmap(df_encoded.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.xlabel("Features")
plt.ylabel("Features")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("plot_3_correlation_heatmap.png", dpi=150)
plt.show()

print("Visualization completed and saved!\n")

# 4. FEATURE SELECTION
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

X_clf = df_encoded[clf_features]
y_clf = df_encoded["Outcome"]

X_reg = df_encoded[reg_features]
y_reg = df_encoded["Glucose"]

print("Features and targets selected!\n")

# 5. TRAIN TEST SPLIT
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
)

print("Data split into training and testing sets!\n")

# 6. MODEL TRAINING
reg_model = LinearRegression()
reg_model.fit(X_train_reg, y_train_reg)
print("Linear Regression model trained!")

clf_model = DecisionTreeClassifier(max_depth=5, random_state=42)
clf_model.fit(X_train_clf, y_train_clf)
print("Decision Tree model trained!\n")

# 7. MODEL EVALUATION
y_pred_reg = reg_model.predict(X_test_reg)
mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print("---- REGRESSION RESULTS ----")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

y_pred_clf = clf_model.predict(X_test_clf)
accuracy = accuracy_score(y_test_clf, y_pred_clf)
cm = confusion_matrix(y_test_clf, y_pred_clf)

print("\n---- CLASSIFICATION RESULTS ----")
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", cm)
print(
    "Classification Report:\n",
    classification_report(y_test_clf, y_pred_clf, target_names=["Non-Diabetic", "Diabetic"]),
)

# 8. PREDICTION DEMO
sample_clf_df = pd.DataFrame(
    [[2, 140, 70, 30, 100, 32.0, 0.45, 35, 0, 1, 0, 0, 0]],
    columns=clf_features,
)
sample_reg_df = pd.DataFrame(
    [[2, 70, 30, 100, 32.0, 0.45, 35, 0, 1, 0, 0, 0]],
    columns=reg_features,
)

pred_glucose = reg_model.predict(sample_reg_df)
pred_outcome = clf_model.predict(sample_clf_df)

print("\n---- PREDICTION DEMO ----")
print("Input sample -> Pregnancies=2, Glucose=140, BloodPressure=70, SkinThickness=30, Insulin=100, BMI=32.0, DPF=0.45, Age=35")
print("Encoded AgeGroup used in sample: 30s")
print("Predicted Glucose (regression):", pred_glucose[0])
print("Predicted Diabetes Outcome:", "Diabetic" if pred_outcome[0] == 1 else "Non-Diabetic")

# 9. USER INPUT PREDICTION
print("\n---- USER INPUT PREDICTION ----")
warnings.warn("This prediction demo is for educational purposes only and is not medical advice.", UserWarning)

try:
    preg = int(input("Enter Pregnancies: "))
    glucose = float(input("Enter Glucose: "))
    bp = float(input("Enter BloodPressure: "))
    skin = float(input("Enter SkinThickness: "))
    insulin = float(input("Enter Insulin: "))
    bmi = float(input("Enter BMI: "))
    dpf = float(input("Enter DiabetesPedigreeFunction: "))
    age = int(input("Enter Age: "))

    user_input_clf = pd.DataFrame(
        [[preg, glucose, bp, skin, insulin, bmi, dpf, age, 0, 0, 0, 0, 0]],
        columns=clf_features,
    )
    user_input_reg = pd.DataFrame(
        [[preg, bp, skin, insulin, bmi, dpf, age, 0, 0, 0, 0, 0]],
        columns=reg_features,
    )

    user_age_group = pd.cut(
        pd.Series([age]),
        bins=[20, 30, 40, 50, 60, 100],
        labels=["20s", "30s", "40s", "50s", "60+"],
        include_lowest=True,
    ).iloc[0]

    if pd.notna(user_age_group):
        age_col = f"AgeGroup_{user_age_group}"
        if age_col in user_input_clf.columns:
            user_input_clf.loc[0, age_col] = 1
        if age_col in user_input_reg.columns:
            user_input_reg.loc[0, age_col] = 1

    user_glucose = reg_model.predict(user_input_reg)
    user_outcome = clf_model.predict(user_input_clf)

    print("\nPredicted Glucose:", user_glucose[0])
    print("Predicted Diabetes Outcome:", "Diabetic" if user_outcome[0] == 1 else "Non-Diabetic")

except ValueError as e:
    print(f"Invalid numeric input ({e}). Skipping user prediction.")

print("\nPROJECT COMPLETED SUCCESSFULLY!")