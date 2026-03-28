import pandas as pd

df = pd.read_csv("diabetes.csv")  # just file name
print(df.head())

import os
print(os.getcwd())

# ============================================
# MACHINE LEARNING LAB PROJECT
# Student Performance Prediction
# ============================================

# 1. IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix

print("Libraries imported successfully!\n")

# ============================================
# 2. CREATE / LOAD DATASET
# (We generate dataset to avoid file issues)
# ============================================

np.random.seed(42)

data = {
    'Hours_Studied': np.random.randint(1, 10, 100),
    'Attendance': np.random.randint(50, 100, 100),
    'Previous_Score': np.random.randint(40, 100, 100),
    'Pass': np.random.randint(0, 2, 100)
}

df = pd.DataFrame(data)

# Create target for regression (Final Score)
df['Final_Score'] = (
    0.3 * df['Hours_Studied'] +
    0.4 * df['Attendance'] +
    0.3 * df['Previous_Score']
) + np.random.randint(-5, 5, 100)

print("Dataset created successfully!\n")
print(df.head())

# ============================================
# 3. DATA PREPROCESSING
# ============================================

print("\n--- DATA INFO ---")
print(df.info())

print("\n--- STATISTICS ---")
print(df.describe())

# Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# No missing values, but example handling:
df = df.dropna()

print("\nData preprocessing completed!\n")

# ============================================
# 4. DATA VISUALIZATION
# ============================================

# Histogram
plt.figure()
df['Final_Score'].hist()
plt.title("Distribution of Final Score")
plt.show()

# Scatter plot
plt.figure()
plt.scatter(df['Hours_Studied'], df['Final_Score'])
plt.xlabel("Hours Studied")
plt.ylabel("Final Score")
plt.title("Hours Studied vs Final Score")
plt.show()

# Heatmap
plt.figure()
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()

print("Visualization completed!\n")

# ============================================
# 5. FEATURE SELECTION
# ============================================

# Regression
X_reg = df[['Hours_Studied', 'Attendance', 'Previous_Score']]
y_reg = df['Final_Score']

# Classification
X_clf = df[['Hours_Studied', 'Attendance', 'Previous_Score']]
y_clf = df['Pass']

print("Features and target selected!\n")

# ============================================
# 6. TRAIN TEST SPLIT
# ============================================

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42
)

print("Data split into training and testing sets!\n")

# ============================================
# 7. MODEL TRAINING
# ============================================

# Linear Regression
reg_model = LinearRegression()
reg_model.fit(X_train_reg, y_train_reg)

print("Linear Regression model trained!")

# Decision Tree Classifier
clf_model = DecisionTreeClassifier()
clf_model.fit(X_train_clf, y_train_clf)

print("Decision Tree model trained!\n")

# ============================================
# 8. MODEL EVALUATION
# ============================================

# Regression Evaluation
y_pred_reg = reg_model.predict(X_test_reg)

mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print("---- REGRESSION RESULTS ----")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

# Classification Evaluation
y_pred_clf = clf_model.predict(X_test_clf)

accuracy = accuracy_score(y_test_clf, y_pred_clf)
cm = confusion_matrix(y_test_clf, y_pred_clf)

print("\n---- CLASSIFICATION RESULTS ----")
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", cm)

# ============================================
# 9. PREDICTION DEMO
# ============================================

# Sample Input
sample = [[5, 80, 70]]  # Hours, Attendance, Previous Score

pred_score = reg_model.predict(sample)
pred_pass = clf_model.predict(sample)

print("\n---- PREDICTION DEMO ----")
print("Input: Hours=5, Attendance=80, Previous Score=70")
print("Predicted Final Score:", pred_score[0])
print("Pass/Fail Prediction:", "Pass" if pred_pass[0] == 1 else "Fail")

# ============================================
# 10. BONUS: USER INPUT PREDICTION
# ============================================

print("\n---- USER INPUT PREDICTION ----")

try:
    h = int(input("Enter Hours Studied: "))
    a = int(input("Enter Attendance: "))
    p = int(input("Enter Previous Score: "))

    user_input = [[h, a, p]]

    user_score = reg_model.predict(user_input)
    user_pass = clf_model.predict(user_input)

    print("\nPredicted Final Score:", user_score[0])
    print("Prediction:", "Pass" if user_pass[0] == 1 else "Fail")

except:
    print("Invalid input, skipping user prediction.")

print("\nPROJECT COMPLETED SUCCESSFULLY!")