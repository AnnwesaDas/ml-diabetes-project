# ML Diabetes Project

Beginner-friendly machine learning lab project using the Pima Indians Diabetes dataset.

The project includes two tasks:
- Classification: predict diabetes outcome (Outcome)
- Regression: estimate glucose level (Glucose)

## Project Files

- diabetes.csv: input dataset
- ml_diabetes_project.ipynb: notebook version (best for viva and Colab)
- main.py: script version (run from terminal)
- requirements.txt: Python dependencies
- plot_1_glucose_histogram.png: saved histogram
- plot_2_bmi_vs_glucose_scatter.png: saved scatter plot
- plot_3_correlation_heatmap.png: saved heatmap

## Dataset

- Name: Pima Indians Diabetes Dataset
- Rows: 768
- Columns: 9

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

## Requirements

Libraries used:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

Install all dependencies:

```bash
pip install -r requirements.txt
```

## How To Run

### Option 1: Run Python Script (VS Code Terminal)

```bash
python main.py
```

### Option 2: Run Notebook (VS Code or Colab)

1. Open ml_diabetes_project.ipynb
2. Select Python kernel/interpreter
3. Click Run All

## ML Pipeline Covered

| Step | Description |
|---|---|
| 1 | Import libraries |
| 2 | Load CSV dataset |
| 3 | Preprocessing: info/describe, missing value handling, encoding |
| 4 | Visualization: histogram, scatter plot, heatmap |
| 5 | Feature selection (X and y) |
| 6 | Train-test split |
| 7 | Model training: Linear Regression + Decision Tree Classifier |
| 8 | Evaluation: MSE, R2, accuracy, confusion matrix, classification report |
| 9 | Prediction demo with sample input |
| 10 | User input prediction demo |

## Notes

- Plot images are saved so results remain visible even without rerunning code.
- User input prediction is for demonstration purposes only.

## Educational Disclaimer

This project is for educational purposes only and is not medical advice.
