# 🚀 Full-Stack Architecture: Quick Reference

Your diabetes ML project has been refactored into a production-ready full-stack architecture.

## What Was Created

### ✅ Backend Structure (`backend/`)
```
backend/
├── app.py                      # Flask API server (async prediction endpoint)
├── train_model.py             # Model training & pickle generation
├── requirements.txt           # Python dependencies (Flask, scikit-learn, pandas)
├── model/                     # Trained models directory (created when you run train_model.py)
│   ├── classifier_model.pkl
│   ├── regression_model.pkl
│   └── preprocessing_metadata.pkl
├── utils/preprocessing.py     # Shared data preprocessing logic
├── README.md                  # Backend documentation
├── .env.example              # Environment template
└── .gitignore               # Git ignore rules
```

### ✅ Frontend Updates
- Updated `predictionService.js` to connect to real backend API
- Added `.env.local` (development) - points to `http://localhost:5000`
- Added `.env.production` (production) - points to your Render deployment

### ✅ Root Documentation
- `DEPLOYMENT.md` - Complete deployment guide for Vercel & Render

---

## 🎯 Getting Started (5 Steps)

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Train Models (Creates Pickle Files)
```bash
python train_model.py
```
Expected output:
```
============================================================
DIABETES PREDICTION MODEL TRAINING
============================================================

1. Loading dataset...
   ✓ Dataset loaded: 768 rows, 9 columns

2. Preprocessing data...
   ✓ Data preprocessed

...

9. Saving models...
   ✓ Classification model saved: backend/model/classifier_model.pkl
   ✓ Regression model saved: backend/model/regression_model.pkl
   
============================================================
TRAINING COMPLETE
============================================================
```

### Step 3: Start Backend Server
```bash
python app.py
```

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

### Step 4: Start Frontend Server (in new terminal)
```bash
cd frontend
npm run dev
```

### Step 5: Test End-to-End
- Open frontend at `http://localhost:5173`
- Fill in patient data
- Click "Run Prediction"
- Backend returns real ML predictions ✅

---

## 🔌 API Endpoints

### GET - Health Check
```bash
curl http://localhost:5000/
```

### POST - Make Prediction
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

**Response:**
```json
{
  "success": true,
  "prediction": {
    "estimated_glucose": 138.45,
    "diabetes_risk": "Diabetic",
    "diabetes_probability": 0.78,
    "confidence": 0.78
  }
}
```

---

## 🌐 Deploying to Production

### Deploy Backend to Render (https://render.com)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy full-stack diabetes app"
   git push
   ```

2. **Create Render Web Service**
   - Go to render.com → New Web Service
   - Connect your GitHub repository

3. **Configure Render**
   | Setting | Value |
   |---------|-------|
   | Name | `diabetes-prediction-api` |
   | Environment | Python 3 |
   | Build Command | `pip install -r backend/requirements.txt && python backend/train_model.py` |
   | Start Command | `python backend/app.py` |

4. **Deploy** → Render auto-deploys and trains models

5. **Copy URL** → Example: `https://diabetes-prediction-api.onrender.com`

### Deploy Frontend to Vercel (https://vercel.com)

1. **Import GitHub Repo**
   - Go to vercel.com → Import Project
   - Select your repository

2. **Configure**
   | Setting | Value |
   |---------|-------|
   | Framework | Vite |
   | Root Directory | `frontend` |
   | Build Command | `npm run build` |

3. **Add Environment Variable**
   - Name: `VITE_API_URL`
   - Value: `https://diabetes-prediction-api.onrender.com` (from Render)

4. **Deploy** → Vercel auto-deploys

---

## 📊 Project Architecture

```
┌─────────────────────────────────────────┐
│       VERCEL (Frontend)                 │
│  - React + Vite                         │
│  - Responsive Dashboard UI              │
│  - Patient Input Form                   │
└────────────────┬────────────────────────┘
                 │ JSON API (HTTPS)
                 ↓
┌─────────────────────────────────────────┐
│       RENDER (Backend)                  │
│  - Flask API Server                     │
│  - Loads .pkl Models                  │
│  - Inference Engine                     │
└────────────────┬────────────────────────┘
                 │ Load from Disk
                 ↓
┌─────────────────────────────────────────┐
│    Pickle Files (Models)                │
│  - classifier_model.pkl                 │
│  - regression_model.pkl                 │
│  - preprocessing_metadata.pkl           │
└─────────────────────────────────────────┘
```

---

## 🔧 Key Files Explained

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask server. Loads models, serves `/api/predict` endpoint. |
| `backend/train_model.py` | Trains models on `data/diabetes.csv`, saves to `model/` as pickle files. |
| `backend/utils/preprocessing.py` | Shared logic for data cleaning, feature engineering, one-hot encoding. |
| `frontend/src/services/predictionService.js` | Frontend service. Calls backend API, formats requests/responses. |
| `frontend/.env.local` | Dev config: Backend at `localhost:5000` |
| `frontend/.env.production` | Prod config: Backend at Render URL |

---

## 📋 Files Structure After Setup

```
diabetes-ml-project/
├── data/
│   └── diabetes.csv                    # Training data
├── backend/
│   ├── app.py                          # ✅ Flask API
│   ├── train_model.py                  # ✅ Training script
│   ├── requirements.txt                # ✅ Dependencies
│   ├── model/                          # ✅ Created after train_model.py
│   │   ├── classifier_model.pkl
│   │   ├── regression_model.pkl
│   │   └── preprocessing_metadata.pkl
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py            # ✅ Utilities
├── frontend/                           # Already exists
│   ├── src/
│   │   ├── components/                 # Components
│   │   └── services/
│   │       └── predictionService.js   # ✅ Updated to use real API
│   ├── .env.local                      # ✅ Dev database
│   ├── .env.production                 # ✅ Prod database
│   └── package.json
├── DEPLOYMENT.md                       # ✅ Full deployment guide
└── README.md
```

---

## ⚡ Common Commands

**Backend Development**
```bash
cd backend
pip install -r requirements.txt    # Install dependencies
python train_model.py              # Train & save models
python app.py                       # Run API server
```

**Frontend Development**
```bash
cd frontend
npm install                         # Install dependencies
npm run dev                        # Run dev server
npm run build                      # Build for production
```

**Full Stack Locally**
```bash
# Terminal 1
cd backend && python app.py        # Start API at :5000

# Terminal 2
cd frontend && npm run dev         # Start UI at :5173
```

---

## ✅ What You Can Do Now

- ✅ Train ML models locally
- ✅ Save models as pickle files (no external storage needed)
- ✅ Run Flask API server for predictions
- ✅ Frontend connects to real backend (not mock anymore)
- ✅ Deploy backend to Render (automatic model training on deploy)
- ✅ Deploy frontend to Vercel (automatic build on push)
- ✅ Scale to thousands of predictions per day
- ✅ Update models by retraining and redeploying

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'sklearn'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: diabetes.csv` | Ensure `data/diabetes.csv` exists |
| `FileNotFoundError: classifier_model.pkl` | Run `python train_model.py` first |
| `Address already in use` | Change port (5001) or kill process using 5000 |
| Frontend shows "API error" | Check backend is running, verify `.env.local` URL |
| Models train forever on Render | Expected on first deploy (2-3 min). Cached after. |

---

## 🎓 Next Steps

1. **Local Testing**: Follow steps above, verify predictions work
2. **GitHub Setup**: Push code to GitHub if not already done
3. **Deploy Backend**: Follow Render deployment instructions
4. **Deploy Frontend**: Follow Vercel deployment instructions
5. **Verify Integration**: Test prediction on live URLs
6. **Monitor**: Check backend logs on Render for errors

---

## 📖 More Information

- Backend setup: `backend/README.md`
- Full deployment guide: `DEPLOYMENT.md`
- Original ML project: `main.py`, `ml_diabetes_project.ipynb`

---

**Status**: ✅ Ready for production deployment

**Your new workflow**:
1. Update data/code locally
2. Push to GitHub
3. Auto-deploy to Vercel (frontend) & Render (backend)
4. Live predictions at your domain 🎉
