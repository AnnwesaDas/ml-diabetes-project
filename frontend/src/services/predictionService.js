/**
 * Prediction Service
 * Handles communication with the ML backend API for diabetes predictions
 *
 * API Endpoint: POST /predict
 * 
 * Toggle between mock and real API:
 * - Set USE_MOCK_API = true for local development without backend
 * - Set USE_MOCK_API = false to connect to real backend
 */

const USE_MOCK_API = false; // Set to false to use real backend API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function pickNumber(payload, primaryKey, fallbackKey) {
  const value = payload[primaryKey] ?? payload[fallbackKey];
  return parseFloat(value) || 0;
}

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
  const glucose = pickNumber(payload, 'Glucose', 'glucose');
  const bmi = pickNumber(payload, 'BMI', 'bmi');
  const age = pickNumber(payload, 'Age', 'age');
  const dpf = pickNumber(payload, 'DiabetesPedigreeFunction', 'diabetesPedigreeFunction');
  const insulin = pickNumber(payload, 'Insulin', 'insulin');
  const bloodPressure = pickNumber(payload, 'BloodPressure', 'bloodPressure');
  const skinThickness = pickNumber(payload, 'SkinThickness', 'skinThickness');
  const pregnancies = pickNumber(payload, 'Pregnancies', 'pregnancies');

  const riskScore =
    normalize(glucose, 40, 250) * 0.34 +
    normalize(bmi, 10, 70) * 0.18 +
    normalize(age, 18, 100) * 0.15 +
    normalize(dpf, 0.05, 3) * 0.14 +
    normalize(insulin, 0, 900) * 0.07 +
    normalize(bloodPressure, 30, 140) * 0.06 +
    normalize(skinThickness, 5, 99) * 0.04 +
    normalize(pregnancies, 0, 20) * 0.02;

  const estimatedGlucose = Math.round(
    glucose * 0.82 + bmi * 1.15 + age * 0.25 + insulin * 0.03
  );

  return {
    predicted_outcome: riskScore >= 0.52 ? 1 : 0,
    predicted_outcome_label: riskScore >= 0.52 ? 'Diabetic' : 'Non-Diabetic',
    estimated_glucose: estimatedGlucose,
  };
}

/**
 * Convert form payload to backend API format
 * Frontend uses camelCase, backend expects PascalCase
 */
function formatPayloadForBackend(payload) {
  return {
    Pregnancies: pickNumber(payload, 'Pregnancies', 'pregnancies'),
    Glucose: pickNumber(payload, 'Glucose', 'glucose'),
    BloodPressure: pickNumber(payload, 'BloodPressure', 'bloodPressure'),
    SkinThickness: pickNumber(payload, 'SkinThickness', 'skinThickness'),
    Insulin: pickNumber(payload, 'Insulin', 'insulin'),
    BMI: pickNumber(payload, 'BMI', 'bmi'),
    DiabetesPedigreeFunction: pickNumber(payload, 'DiabetesPedigreeFunction', 'diabetesPedigreeFunction'),
    Age: pickNumber(payload, 'Age', 'age'),
  };
}

/**
 * Transform backend response to frontend format if needed
 */
function transformBackendResponse(response) {
  if (!response || typeof response !== 'object') {
    throw new Error('Invalid API response.');
  }

  return {
    outcome: response.predicted_outcome_label,
    outcomeCode: response.predicted_outcome,
    estimatedGlucose: response.estimated_glucose,
    confidence: 'N/A',
  };
}

function extractApiErrorMessage(errorData, fallbackMessage) {
  if (!errorData) {
    return fallbackMessage;
  }

  if (typeof errorData.detail === 'string') {
    return errorData.detail;
  }

  if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
    const first = errorData.detail[0];
    if (typeof first === 'string') {
      return first;
    }
    if (first && typeof first === 'object' && first.msg) {
      const field = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : 'field';
      return `${field}: ${first.msg}`;
    }
  }

  if (typeof errorData.error === 'string') {
    return errorData.error;
  }

  return fallbackMessage;
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

    const response = await fetch(`${API_BASE_URL}/predict`, {
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
        extractApiErrorMessage(errorData, `API error ${response.status}: ${response.statusText}`)
      );
    }

    const data = await response.json();
    return transformBackendResponse(data);

  } catch (error) {
    console.error('Prediction API Error:', error);
    throw error;
  }
}
