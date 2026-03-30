import { useMemo, useState } from 'react';
import SectionHeader from './SectionHeader';
import ResultCard from './ResultCard';
import { predictionFields } from '../data/mockData';
import { runPrediction } from '../services/predictionService';

const emptyValues = predictionFields.reduce((acc, field) => {
  acc[field.id] = '';
  return acc;
}, {});

function validate(values) {
  const errors = {};

  predictionFields.forEach((field) => {
    const rawValue = values[field.id];

    if (rawValue === '') {
      errors[field.id] = 'This field is required.';
      return;
    }

    const numericValue = Number(rawValue);

    if (Number.isNaN(numericValue)) {
      errors[field.id] = 'Please enter a valid number.';
      return;
    }

    if (numericValue < field.min || numericValue > field.max) {
      errors[field.id] = `Use a value between ${field.min} and ${field.max}.`;
    }
  });

  return errors;
}

function PredictionFormSection() {
  const [formValues, setFormValues] = useState(emptyValues);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState('idle');
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const hasErrors = useMemo(() => Object.keys(errors).length > 0, [errors]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormValues((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: '' }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formErrors = validate(formValues);
    setErrors(formErrors);

    if (Object.keys(formErrors).length > 0) {
      setStatus('empty');
      setResult(null);
      return;
    }

    const payload = predictionFields.reduce((acc, field) => {
      acc[field.id] = Number(formValues[field.id]);
      return acc;
    }, {});

    setStatus('loading');
    setErrorMessage('');

    try {
      const prediction = await runPrediction(payload);
      setResult(prediction);
      setStatus('success');
    } catch (error) {
      setStatus('error');
      setResult(null);
      setErrorMessage(error.message || 'Prediction failed. Please try again.');
    }
  };

  return (
    <section className="section section-alt" aria-labelledby="prediction-title">
      <div className="container">
        <SectionHeader
          eyebrow="Prediction"
          title="Try the ML Predictor"
          description="Enter feature values to simulate diabetes classification and glucose estimation."
        />

        <div className="prediction-layout">
          <form className="surface-card form-card" onSubmit={handleSubmit} noValidate>
            <div className="form-grid">
              {predictionFields.map((field) => {
                const inputId = `field-${field.id}`;
                const errorId = `${inputId}-error`;
                const helperId = `${inputId}-helper`;
                const fieldError = errors[field.id];

                return (
                  <div key={field.id} className="field-wrap">
                    <label htmlFor={inputId}>{field.label}</label>
                    <input
                      id={inputId}
                      name={field.id}
                      type="number"
                      inputMode="decimal"
                      placeholder={field.placeholder}
                      value={formValues[field.id]}
                      min={field.min}
                      max={field.max}
                      step={field.step}
                      aria-invalid={Boolean(fieldError)}
                      aria-describedby={fieldError ? `${helperId} ${errorId}` : helperId}
                      onChange={handleChange}
                    />
                    <small id={helperId} className="helper-text">
                      {field.helper}
                    </small>
                    {fieldError ? (
                      <small id={errorId} className="error-text" role="alert">
                        {fieldError}
                      </small>
                    ) : null}
                  </div>
                );
              })}
            </div>
            <button className="btn-primary" type="submit">
              Run Prediction
            </button>
          </form>

          <aside className="surface-card result-panel" aria-live="polite">
            <h3>Prediction Output</h3>

            {status === 'idle' ? (
              <p className="state-text">Submit the form to view simulated model outputs.</p>
            ) : null}

            {status === 'empty' && hasErrors ? (
              <p className="state-text error">Please resolve validation errors and submit again.</p>
            ) : null}

            {status === 'loading' ? <p className="state-text loading">Running model prediction...</p> : null}

            {status === 'error' ? <p className="state-text error">{errorMessage}</p> : null}

            {status === 'success' && result ? (
              <div className="results-grid">
                <ResultCard
                  label="Predicted Diabetes Outcome"
                  value={result.outcome}
                  tone={result.outcome === 'Diabetic' ? 'critical' : 'good'}
                  helper={`Confidence: ${result.confidence}`}
                />
                <ResultCard
                  label="Estimated Glucose Level"
                  value={`${result.estimatedGlucose} mg/dL`}
                  tone={result.estimatedGlucose > 140 ? 'warning' : 'good'}
                  helper="Mock regression estimate"
                />
              </div>
            ) : null}
          </aside>
        </div>
      </div>
    </section>
  );
}

export default PredictionFormSection;
