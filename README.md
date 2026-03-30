# ML Diabetes Project

Beginner-friendly diabetes machine learning project using the Pima Indians dataset.

Core tasks:
- Classification: predict diabetes outcome (`Outcome`)
- Regression: estimate glucose level (`Glucose`)

## Project Structure

- `data/diabetes.csv`: input dataset
- `data/plots/`: generated plot images from `main.py`
- `main.py`: original script-based ML pipeline
- `backend/`: deployable FastAPI backend for model serving
- `frontend/`: React dashboard frontend
- `ml_diabetes_project.ipynb`: notebook version
- `requirements.txt`: dependencies for `main.py`

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

Install dependencies for the script:

```bash
pip install -r requirements.txt
```

## How To Run

### Option 1: Run Script Version

```bash
py -3.11 main.py
```

The script will:
- train both models
- evaluate metrics
- save charts to `data/plots/`
- ask for optional user input prediction at the end

### Option 2: Run Notebook (VS Code or Colab)

1. Open ml_diabetes_project.ipynb
2. Select Python kernel/interpreter
3. Click Run All

### Option 3: Run Frontend Dashboard (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

For backend API setup and deployment, see `backend/README.md`.

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

- Core ML logic in `main.py` is preserved for learning and comparison.
- Generated artifacts are organized under `data/` and `backend/model/`.
- User input prediction is for demonstration purposes only.

## Educational Disclaimer

This project is for educational purposes only and is not medical advice.
