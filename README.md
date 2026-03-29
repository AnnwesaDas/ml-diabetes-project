# ml-diabetes-project

A machine learning lab project that uses the Pima Indians Diabetes dataset for:
- Classification: predicting diabetes outcome (`Outcome`)
- Regression: estimating glucose level (`Glucose`)

## Dataset

- Name: Pima Indians Diabetes Dataset
- Rows: 768
- Columns: 9
- File: `diabetes.csv`

Columns:
- Pregnancies
- Glucose
- BloodPressure
- SkinThickness
- Insulin
- BMI
- DiabetesPedigreeFunction
- Age
- Outcome

## Setup

Required libraries:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Script Sections

| Step | Section | What it does |
|---|---|---|
| 1 | Import Libraries | Imports data, plotting, and ML libraries |
| 2 | Load Dataset | Reads `diabetes.csv` into a DataFrame |
| 3 | Preprocessing | Converts invalid zeros to missing values, fills missing values with medians, and demonstrates categorical encoding with `get_dummies` |
| 4 | Visualization | Builds and saves histogram, scatter, and heatmap plots |
| 5 | Feature Selection | Defines feature/target sets for classification and regression |
| 6 | Train-Test Split | Splits data for evaluation and stratifies classification target |
| 7 | Model Training | Trains Linear Regression and Decision Tree models |
| 8 | Evaluation | Prints MSE, R2, accuracy, confusion matrix, and classification report |
| 9 | Prediction Demo | Runs a sample prediction for both tasks |
| 10 | User Input | Accepts manual input for a demo prediction |

## Educational Use Only

This project is for educational purposes only and is not medical advice.
