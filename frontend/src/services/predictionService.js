const USE_MOCK_API = true;

function normalize(value, min, max) {
  return Math.max(0, Math.min(1, (value - min) / (max - min)));
}

function buildMockPrediction(payload) {
  const riskScore =
    normalize(payload.glucose, 40, 250) * 0.34 +
    normalize(payload.bmi, 10, 70) * 0.18 +
    normalize(payload.age, 18, 100) * 0.15 +
    normalize(payload.diabetesPedigreeFunction, 0.05, 3) * 0.14 +
    normalize(payload.insulin, 0, 900) * 0.07 +
    normalize(payload.bloodPressure, 30, 140) * 0.06 +
    normalize(payload.skinThickness, 5, 99) * 0.04 +
    normalize(payload.pregnancies, 0, 20) * 0.02;

  const estimatedGlucose = Math.round(
    payload.glucose * 0.82 + payload.bmi * 1.15 + payload.age * 0.25 + payload.insulin * 0.03
  );

  return {
    outcome: riskScore >= 0.52 ? 'Diabetic' : 'Non-Diabetic',
    confidence: `${Math.round(Math.abs(riskScore - 0.5) * 200)}%`,
    estimatedGlucose
  };
}

export async function runPrediction(payload) {
  if (!USE_MOCK_API) {
    // Replace this block with backend integration later.
    // Example:
    // const response = await fetch('/api/predict', { method: 'POST', body: JSON.stringify(payload) });
    // return response.json();
  }

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (payload.glucose <= 0) {
        reject(new Error('Unable to compute prediction. Please verify glucose input.'));
        return;
      }

      resolve(buildMockPrediction(payload));
    }, 850);
  });
}
