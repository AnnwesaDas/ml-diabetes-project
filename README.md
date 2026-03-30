# ML Diabetes Project

Beginner-friendly diabetes machine learning project using the Pima Indians dataset.

Core tasks:
- Classification: predict diabetes outcome (Outcome)
- Regression: estimate glucose level (Glucose)

## Project Structure

- data/diabetes.csv: input dataset
- data/plots/: generated plot images from main.py
- main.py: original script-based ML pipeline
- backend/: FastAPI backend for model serving
- frontend/: React dashboard frontend
- ml_diabetes_project.ipynb: notebook version
- requirements.txt: dependencies for main.py

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
py -3.11 -m pip install -r requirements.txt
```

## Train Models (Backend)

The deployable backend uses a separate training script.

1. Install backend dependencies:

```bash
py -3.11 -m pip install -r backend/requirements.txt
```

2. Train and save model artifacts:

```bash
py -3.11 backend/train_model.py
```

This creates:
- backend/model/classifier_model.pkl
- backend/model/regression_model.pkl
- backend/model/preprocessing_metadata.pkl

## Run API Locally

Start the FastAPI server:

```bash
py -3.11 backend/app.py
```

API endpoints:
- GET /health
- POST /predict

Example request:

```bash
curl -X POST http://localhost:5000/predict \
	-H "Content-Type: application/json" \
	-d '{
		"Pregnancies": 2,
		"Glucose": 140,
		"BloodPressure": 70,
		"SkinThickness": 30,
		"Insulin": 100,
		"BMI": 32.0,
		"DiabetesPedigreeFunction": 0.45,
		"Age": 35
	}'
```

Example response:

```json
{
	"predicted_outcome": 1,
	"predicted_outcome_label": "Diabetic",
	"estimated_glucose": 119.01
}
```

## Frontend Connection (Later)

The frontend should call the backend base URL from VITE_API_URL.

Development:
- frontend/.env.local
- VITE_API_URL=http://localhost:5000

Production:
- frontend/.env.production
- VITE_API_URL=https://your-render-service.onrender.com

When wiring API calls, use:
- POST ${VITE_API_URL}/predict

Note: If your frontend currently calls /api/predict, update it to /predict to match the current FastAPI backend.

## Deployment Mapping (Vercel + Render)

Frontend on Vercel:
- Root directory: frontend
- Build command: npm run build
- Output: dist
- Environment variable: VITE_API_URL=<your Render backend URL>

Backend on Render:
- Root directory: backend (or use repo root commands with backend/ prefix)
- Build command: pip install -r backend/requirements.txt && python backend/train_model.py
- Start command: cd backend ; uvicorn app:app --host 0.0.0.0 --port $PORT
- Equivalent Procfile exists at backend/Procfile
- Optional env var: CORS_ORIGINS=https://your-vercel-app.vercel.app

This maps to a standard setup:
- Browser -> Vercel frontend -> Render API -> loaded .pkl model files

## Legacy Script Run

You can still run the original single-file workflow:

```bash
py -3.11 main.py
```

The script will:
- train both models in-memory
- evaluate metrics
- save charts to data/plots/
- ask for optional user input prediction at the end

### Notebook Option (VS Code or Colab)

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

- Core ML logic in main.py is preserved for learning and comparison.
- Generated artifacts are organized under data/ and backend/model/.
- User input prediction is for demonstration purposes only.

## Educational Disclaimer

This project is for educational purposes only and is not medical advice.
