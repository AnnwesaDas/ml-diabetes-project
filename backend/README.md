# Backend Deployment Guide

This is the backend server for the Diabetes Prediction ML project. It serves predictions via a JSON API that the React frontend can consume.

## Project Structure

```
backend/
├── app.py                          # Flask API server
├── train_model.py                  # Model training script
├── requirements.txt                # Python dependencies
├── model/                          # Trained models directory (auto-created)
│   ├── classifier_model.pkl       # Decision Tree classifier
│   ├── regression_model.pkl       # Linear Regression model
│   └── preprocessing_metadata.pkl # Preprocessing configuration
└── utils/
    ├── __init__.py
    └── preprocessing.py           # Data preprocessing utilities
```

## Setup & Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train Models

Run the training script to create the pickle model files:

```bash
python train_model.py
```

This will:
- Load the diabetes dataset from `data/diabetes.csv`
- Preprocess the data (handle missing values, feature engineering)
- Train a Decision Tree Classifier (diabetes outcomes)
- Train a Linear Regression model (glucose estimation)
- Save both models and preprocessing metadata in the `model/` directory

Expected output:
```
============================================================
DIABETES PREDICTION MODEL TRAINING
============================================================
...
============================================================
TRAINING COMPLETE
============================================================

Models saved in: backend/model
```

### 3. Run the Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

Output:
```
============================================================
DIABETES PREDICTION API
============================================================

✓ All models loaded successfully

Starting Flask server...
API available at: http://localhost:5000
Prediction endpoint: POST http://localhost:5000/api/predict

Press CTRL+C to stop the server
```

## API Endpoints

### 1. Health Check
```
GET /
GET /api/health
```

Returns: Server status and models information

### 2. Make Prediction
```
POST /api/predict
Content-Type: application/json

{
  "Pregnancies": 2,
  "Glucose": 140,
  "BloodPressure": 70,
  "SkinThickness": 30,
  "Insulin": 100,
  "BMI": 32.0,
  "DiabetesPedigreeFunction": 0.45,
  "Age": 35
}
```

Returns:
```json
{
  "success": true,
  "prediction": {
    "estimated_glucose": 138.45,
    "diabetes_risk": "Diabetic",
    "diabetes_probability": 0.78,
    "confidence": 0.78,
    "input_data": {
      "Pregnancies": 2,
      "Glucose": 140,
      ...
    }
  }
}
```

## Environment Variables

Create a `.env` file in the backend directory for deployment:

```
FLASK_ENV=production
FLASK_DEBUG=0
```

## Deployment on Render

### 1. Prepare for Deployment

Add a `render.yaml` configuration:

```yaml
services:
  - type: web
    name: diabetes-prediction-api
    env: python
    buildCommand: pip install -r requirements.txt && python train_model.py
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 5000
```

### 2. Deploy to Render

1. Push code to GitHub
2. Connect your repository to Render
3. Create new Web Service
4. Select the GitHub repository
5. Set Build Command: `pip install -r backend/requirements.txt && python backend/train_model.py`
6. Set Start Command: `python backend/app.py`
7. Deploy!

### 3. Environment Setup

In Render dashboard, set these environment variables:
- `FLASK_ENV`: `production`
- `PORT`: `5000` (Render assigns this automatically)

## Frontend Integration

### React/Vite Frontend Configuration

Update your frontend's API base URL based on environment:

```javascript
// frontend/src/services/predictionService.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export async function runPrediction(formData) {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData),
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}
```

### Configure Environment Variables

Create `.env` files:

**Development** (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:5000
```

**Production** (`frontend/.env.production`):
```
VITE_API_URL=https://your-render-backend-url.onrender.com
```

## Troubleshooting

### Models not found
**Error:** `FileNotFoundError: Classification model not found`

**Solution:**
```bash
python train_model.py
```

### Port already in use
**Error:** `OSError: [Errno 48] Address already in use`

**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```

### Import errors
**Error:** `ModuleNotFoundError: No module named 'sklearn'`

**Solution:**
```bash
pip install -r requirements.txt
```

### CORS issues
The API has CORS enabled for all origins. If you need to restrict it for production:

```python
# app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.com"],
        "methods": ["GET", "POST"]
    }
})
```

## Development Tips

### Test the API with curl

```bash
curl -X POST http://localhost:5000/api/predict \
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

### Check Backend Logs

When running locally, the console shows detailed logs. For Render, check the logs in the dashboard.

### Model Retraining

To retrain models with new data:

1. Place updated `diabetes.csv` in the `data/` directory
2. Run `python train_model.py`
3. Redeploy the backend

## File Descriptions

### `app.py`
Main Flask application with API endpoints. Loads models on startup and serves predictions.

### `train_model.py`
Standalone script to train ML models. Creates pickle files in the `model/` directory.

### `utils/preprocessing.py`
Shared data preprocessing logic:
- `preprocess_data()`: Handles missing values, feature engineering, encoding
- `prepare_prediction_input()`: Formats API input for both models

### `requirements.txt`
Python dependencies for the backend. Install with `pip install -r requirements.txt`.

## Next Steps

1. ✅ Set up backend locally
2. ✅ Train models and verify pickle files
3. ✅ Update frontend API service to connect to backend
4. ✅ Deploy frontend to Vercel
5. ✅ Deploy backend to Render
6. ✅ Test full-stack integration
