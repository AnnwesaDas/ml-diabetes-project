/**
 * Prediction Service
 * Handles communication with the ML backend API for diabetes predictions
 * 
 * API Endpoint: POST /api/predict
 * 
 * Toggle between mock and real API:
 * - Set USE_MOCK_API = true for local development without backend
 * - Set USE_MOCK_API = false to connect to real backend
 */

const USE_MOCK_API = false; // Set to false to use real backend API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Helper function to normalize values between 0 and 1
 */
function normalize(value, min, max) {
  return Math.max(0, Math.min(1, (value - min) / (max - min)));
}

/**
 * Build a mock prediction for testing without backend
 */
function buildMockPrediction(payload) {
  const riskScore =
    normalize(payload.Glucose, 40, 250) * 0.34 +
    normalize(payload.BMI, 10, 70) * 0.18 +
    normalize(payload.Age, 18, 100) * 0.15 +
    normalize(payload.DiabetesPedigreeFunction, 0.05, 3) * 0.14 +
    normalize(payload.Insulin, 0, 900) * 0.07 +
    normalize(payload.BloodPressure, 30, 140) * 0.06 +
    normalize(payload.SkinThickness, 5, 99) * 0.04 +
    normalize(payload.Pregnancies, 0, 20) * 0.02;

  const estimatedGlucose = Math.round(
    payload.Glucose * 0.82 + payload.BMI * 1.15 + payload.Age * 0.25 + payload.Insulin * 0.03
  );

  return {
    success: true,
    prediction: {
      estimated_glucose: estimatedGlucose,
      diabetes_risk: riskScore >= 0.52 ? 'Diabetic' : 'Non-Diabetic',
      confidence: Math.abs(riskScore - 0.5) * 2,
      diabetes_probability: riskScore,
    }
  };
}

/**
 * Convert form payload to backend API format
 * Frontend uses camelCase, backend expects PascalCase
 */
function formatPayloadForBackend(payload) {
  return {
    Pregnancies: parseFloat(payload.Pregnancies) || 0,
    Glucose: parseFloat(payload.Glucose) || 0,
    BloodPressure: parseFloat(payload.BloodPressure) || 0,
    SkinThickness: parseFloat(payload.SkinThickness) || 0,
    Insulin: parseFloat(payload.Insulin) || 0,
    BMI: parseFloat(payload.BMI) || 0,
    DiabetesPedigreeFunction: parseFloat(payload.DiabetesPedigreeFunction) || 0,
    Age: parseFloat(payload.Age) || 0,
  };
}

/**
 * Transform backend response to frontend format if needed
 */
function transformBackendResponse(response) {
  if (!response.success) {
    throw new Error(response.error || 'Prediction failed');
  }

  return {
    status: 'success',
    prediction: {
      outcome: response.prediction.diabetes_risk,
      diabetesProbability: response.prediction.diabetes_probability,
      estimatedGlucose: response.prediction.estimated_glucose,
      confidence: (response.prediction.confidence * 100).toFixed(1) + '%',
      rawResponse: response.prediction,
    }
  };
}

/**
 * Main prediction function
 * Calls the backend API with patient data and returns predictions
 */
export async function runPrediction(payload) {
  // Use mock API if enabled
  if (USE_MOCK_API) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const formattedPayload = formatPayloadForBackend(payload);
        if (formattedPayload.Glucose <= 0) {
          reject(new Error('Unable to compute prediction. Please verify glucose input.'));
          return;
        }

        resolve(buildMockPrediction(formattedPayload));
      }, 850);
    });
  }

  // Real backend API call
  try {
    const formattedPayload = formatPayloadForBackend(payload);

    const response = await fetch(`${API_BASE_URL}/api/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(formattedPayload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.error || `API error ${response.status}: ${response.statusText}`
      );
    }

    const data = await response.json();
    return transformBackendResponse(data);

  } catch (error) {
    console.error('Prediction API Error:', error);
    throw error;
  }
}
