# Diabetes Prediction Full-Stack Application

**AI-Powered Healthcare Analytics**

A production-ready machine learning application for diabetes risk prediction and glucose estimation, deployed as a full-stack web application.

## 🏗️ Architecture Overview

This project consists of three main components:

1. **Frontend** (React + Vite) → Deployed on **Vercel**
2. **Backend** (Flask API) → Deployed on **Render**  
3. **ML Models** (Trained & Pickled) → Served via REST API

```
┌─────────────────────────────────────────────────────────┐
│  VERCEL - React/Vite Frontend            (CDN + SPA)    │
│  └─ TypeScript + CSS                                    │
│  └─ Responsive Healthcare Dashboard                     │
│  └─ Real-time Predictions via API                       │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTPS JSON API
                   ↓
┌─────────────────────────────────────────────────────────┐
│  RENDER - Flask Backend                  (Python API)   │
│  ├─ Flask Server with CORS               (Port 5000)    │
│  ├─ ML Model Inference Engine                           │
│  └─ Pickle-based Model Storage                          │
└──────────────────┬──────────────────────────────────────┘
                   │ Load from Disk
                   ↓
┌─────────────────────────────────────────────────────────┐
│  ML Models (Pickle Files)                               │
│  ├─ classifier_model.pkl  (Decision Tree)               │
│  ├─ regression_model.pkl  (Linear Regression)           │
│  └─ preprocessing_metadata.pkl (Feature Config)         │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
diabetes-ml-project/
├── data/
│   └── diabetes.csv                    # Original Pima Indians dataset
│
├── frontend/                           # React + Vite application
│   ├── public/
│   │   └── charts/                    # Visualization assets (PNG)
│   ├── src/
│   │   ├── components/                # React components
│   │   ├── services/
│   │   │   └── predictionService.js  # Backend API integration
│   │   └── styles/
│   ├── .env.local                     # Dev environment (localhost:5000)
│   ├── .env.production                # Prod environment (Render URL)
│   ├── package.json
│   └── vite.config.js
│
├── backend/                            # Flask API server
│   ├── app.py                         # Main Flask application
│   ├── train_model.py                 # Model training script
│   ├── requirements.txt               # Python dependencies
│   ├── model/                         # Trained models (auto-created)
│   │   ├── classifier_model.pkl
│   │   ├── regression_model.pkl
│   │   └── preprocessing_metadata.pkl
│   ├── utils/
│   │   ├── __init__.py
│   │   └── preprocessing.py           # Shared preprocessing logic
│   ├── .env.example                   # Environment template
│   ├── .gitignore
│   └── README.md                      # Backend documentation
│
├── ml_diabetes_project.ipynb          # Jupyter notebook (reference)
├── main.py                            # Original script (legacy/reference)
├── requirements.txt                   # Root requirements (legacy)
├── diabetes.csv                       # Legacy location (moved to data/)
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- pip & npm

### Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Train models (creates pickle files)
python train_model.py

# Start the API server
python app.py
# Server runs at http://localhost:5000
```

#### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend runs at http://localhost:5173
```

#### 3. Access Application

- **Frontend**: http://localhost:5173 (or the URL shown in terminal)
- **API Health**: http://localhost:5000/
- **Make Prediction**: POST to http://localhost:5000/api/predict

### Test API Endpoint

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

Expected response:
```json
{
  "success": true,
  "prediction": {
    "estimated_glucose": 138.45,
    "diabetes_risk": "Diabetic",
    "diabetes_probability": 0.78,
    "confidence": 0.78,
    "input_data": {...}
  }
}
```

## 🧠 ML Pipeline

The backend implements a two-model system:

### Model 1: Classification (Diabetes Risk)
- **Algorithm**: Decision Tree Classifier
- **Target**: Binary classification (Diabetic / Non-Diabetic)
- **Features**: 8 medical inputs + 5 age-group categories
- **Output**: Diabetes risk probability & confidence

### Model 2: Regression (Glucose Estimation)
- **Algorithm**: Linear Regression
- **Target**: Continuous glucose value prediction
- **Features**: 7 medical inputs + 5 age-group categories (excludes Glucose)
- **Output**: Estimated glucose level

### Data Preprocessing
1. **Missing Value Handling**: Replace zeros with NaN, fill with median
2. **Feature Engineering**: Age binning into 5 categories
3. **Encoding**: One-hot encoding for categorical age groups
4. **Normalization**: Implicit in tree-based classifier, handled by sklearn

## 🔌 API Reference

### Health Check
```
GET /
GET /api/health

Response:
{
  "status": "ok",
  "message": "Diabetes Prediction API is running",
  "version": "1.0.0",
  "models": {
    "classifier": "DecisionTreeClassifier",
    "regressor": "LinearRegression"
  }
}
```

### Make Prediction
```
POST /api/predict
Content-Type: application/json

Request Body:
{
  "Pregnancies": number,
  "Glucose": 0-200,
  "BloodPressure": 0-122,
  "SkinThickness": 0-99,
  "Insulin": 0-846,
  "BMI": 0-67.1,
  "DiabetesPedigreeFunction": 0.078-2.42,
  "Age": 21-81
}

Response:
{
  "success": true,
  "prediction": {
    "estimated_glucose": number,
    "diabetes_risk": "Diabetic" | "Non-Diabetic",
    "diabetes_probability": 0-1,
    "confidence": 0-1,
    "input_data": {...}
  }
}
```

## 📦 Deployment

### Deploy Frontend to Vercel

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy full-stack app"
   git push origin main
   ```

2. **Connect to Vercel**
   - Import GitHub repo at vercel.com
   - Select `frontend` as root directory
   - Framework: Vite
   - Build command: `npm run build`
   - Install command: `npm install`

3. **Set Environment Variables**
   - Variable name: `VITE_API_URL`
   - Value: Your Render backend URL (e.g., `https://diabetes-api.onrender.com`)

4. **Deploy**
   - Vercel auto-deploys on push
   - Visit your Vercel deployment URL

### Deploy Backend to Render

1. **Create Render Web Service**
   - Go to render.com/dashboard
   - New > Web Service
   - Connect your GitHub repo

2. **Configure**
   - **Name**: `diabetes-prediction-api`
   - **Environment**: Python 3
   - **Build Command**:
     ```
     pip install -r backend/requirements.txt && python backend/train_model.py
     ```
   - **Start Command**:
     ```
     python backend/app.py
     ```
   - **Plan**: Free (or Starter for production)

3. **Set Environment Variables**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=0
   PORT=5000
   ```

4. **Deploy**
   - Render auto-deploys on every push
   - Trains models on first deploy (takes ~2-3 minutes)
   - Subsequent deploys reuse existing models in cache

5. **Update Frontend**
   - Copy your Render service URL
   - Update `VITE_API_URL` in Vercel environment variables
   - Trigger a redeploy of frontend

## 🛠️ Development Guide

### Training New Models

To retrain models with updated data:

```bash
cd backend
python train_model.py
```

This will:
- Load latest `data/diabetes.csv`
- Preprocess data consistently
- Train both models
- Save to `model/` directory
- Display performance metrics

### Switching Between Mock and Real API

In `frontend/src/services/predictionService.js`:

```javascript
// Use real backend
const USE_MOCK_API = false;

// Use mock (for offline development)
const USE_MOCK_API = true;
```

### Adding New Features

**For Backend**:
1. Add new model columns to preprocessing
2. Retrain models with `python train_model.py`
3. Update API endpoints in `app.py`
4. Deploy to Render

**For Frontend**:
1. Add form fields in components
2. Update `predictionService.js` payload format
3. Update UI components to display new outputs
4. Deploy to Vercel

## 📊 Dataset

**Pima Indians Diabetes Dataset**
- **Rows**: 768 patients
- **Columns**: 9 features + 1 target

| Feature | Type | Range | Unit |
|---------|------|-------|------|
| Pregnancies | int | 0-17 | count |
| Glucose | float | 44-199 | mg/dL |
| BloodPressure | float | 24-122 | mmHg |
| SkinThickness | float | 7-99 | mm |
| Insulin | float | 14-846 | µU/mL |
| BMI | float | 18.2-67.1 | kg/m² |
| DiabetesPedigreeFunction | float | 0.078-2.42 | score |
| Age | int | 21-81 | years |
| **Outcome** | **binary** | **0-1** | **Non-D/D** |

## ⚠️ Medical Disclaimer

**This ML model is for educational and research purposes only.**

The predictions are not a substitute for professional medical diagnosis or treatment. Always consult with qualified healthcare professionals for actual medical decision-making.

## 🐛 Troubleshooting

### Models Not Found (Backend Won't Start)
```
FileNotFoundError: Classification model not found
```
**Solution**: Run `python train_model.py` in the backend directory

### CORS Errors
```
XMLHttpRequest cannot load due to access control
```
**Solution**: Update frontend `.env` with correct backend URL

### Port Already in Use
```
Address already in use (OSError: [Errno 48])
```
**Solution**: Change port in `app.py` or kill existing process

### API Returns 502 Error
**On Render**: Service may still be starting. Wait 30 seconds and retry.
**Locally**: Ensure Flask backend is running on port 5000.

## 📚 Documents

- [Backend README](backend/README.md) - Detailed backend setup and deployment
- [ml_diabetes_project.ipynb](ml_diabetes_project.ipynb) - Jupyter notebook with EDA
- [main.py](main.py) - Original terminal-based ML script (reference)

## 🎯 Performance Metrics

From baseline model evaluation:

| Metric | Value |
|--------|-------|
| Classifier Accuracy | ~78% |
| Regression R² Score | ~0.52 |
| Average Response Time | <50ms |

## 📝 License

This project uses the public Pima Indians Diabetes Dataset. See original source for licensing terms.

## 🤝 Contributing

To improve this project:

1. Create a new branch
2. Make improvements
3. Test locally with both mock and real API
4. Submit pull request

## ✅ Deployment Checklist

- [ ] Backend models trained and tested locally
- [ ] Frontend connects successfully to local backend
- [ ] Push all code to GitHub
- [ ] Deploy backend to Render
- [ ] Copy Render URL to environment variables
- [ ] Deploy frontend to Vercel
- [ ] Test end-to-end prediction on production
- [ ] Monitor logs and performance for 24 hours

## 📞 Support

For issues:
1. Check backend logs: `python app.py` (local) or Render dashboard (production)
2. Check frontend logs: Browser console (F12)
3. Verify `.env` files have correct API URLs
4. Ensure `python train_model.py` completed successfully

---

**Status**: ✅ Ready for Production Deployment

**Last Updated**: January 2024

**Version**: 1.0.0
