export const aboutCards = [
  {
    title: 'Dataset Overview',
    description:
      'The Pima Indians Diabetes dataset contains 768 rows and 9 columns, including health and demographic indicators used for ML training.'
  },
  {
    title: 'Task 1: Classification',
    description:
      'Predict if a person is likely diabetic or non-diabetic based on input health values.'
  },
  {
    title: 'Task 2: Regression',
    description:
      'Estimate a likely glucose level using regression style modeling from the same input features.'
  }
];

export const predictionFields = [
  {
    id: 'pregnancies',
    label: 'Pregnancies',
    placeholder: 'e.g. 2',
    helper: 'Number of pregnancies (0-20).',
    min: 0,
    max: 20,
    step: 1
  },
  {
    id: 'glucose',
    label: 'Glucose',
    placeholder: 'e.g. 120',
    helper: 'Plasma glucose concentration (40-250).',
    min: 40,
    max: 250,
    step: 1
  },
  {
    id: 'bloodPressure',
    label: 'Blood Pressure',
    placeholder: 'e.g. 72',
    helper: 'Diastolic blood pressure (30-140).',
    min: 30,
    max: 140,
    step: 1
  },
  {
    id: 'skinThickness',
    label: 'Skin Thickness',
    placeholder: 'e.g. 25',
    helper: 'Triceps skin fold thickness in mm (5-99).',
    min: 5,
    max: 99,
    step: 1
  },
  {
    id: 'insulin',
    label: 'Insulin',
    placeholder: 'e.g. 80',
    helper: '2-Hour serum insulin in mu U/ml (0-900).',
    min: 0,
    max: 900,
    step: 1
  },
  {
    id: 'bmi',
    label: 'BMI',
    placeholder: 'e.g. 28.4',
    helper: 'Body mass index in kg/m² (10-70).',
    min: 10,
    max: 70,
    step: 0.1
  },
  {
    id: 'diabetesPedigreeFunction',
    label: 'Diabetes Pedigree Function',
    placeholder: 'e.g. 0.45',
    helper: 'Family history influence score (0.05-3.0).',
    min: 0.05,
    max: 3,
    step: 0.01
  },
  {
    id: 'age',
    label: 'Age',
    placeholder: 'e.g. 34',
    helper: 'Age in years (18-100).',
    min: 18,
    max: 100,
    step: 1
  }
];

export const chartCards = [
  {
    id: 'glucose-dist',
    title: 'Glucose Distribution',
    caption: 'Histogram of glucose values from the dataset.',
    imageUrl: '/charts/plot_1_glucose_histogram.png'
  },
  {
    id: 'bmi-glucose',
    title: 'BMI vs Glucose',
    caption: 'Scatter plot showing relationship between BMI and glucose.',
    imageUrl: '/charts/plot_2_bmi_vs_glucose_scatter.png'
  },
  {
    id: 'correlation-heatmap',
    title: 'Correlation Heatmap',
    caption: 'Feature correlation matrix used for quick feature inspection.',
    imageUrl: '/charts/plot_3_correlation_heatmap.png'
  }
];

export const pipelineSteps = [
  'Load dataset',
  'Preprocess data',
  'Handle missing values',
  'Encode age groups',
  'Visualize data',
  'Train models',
  'Evaluate models',
  'Predict results'
];

export const metrics = [
  { id: 'accuracy', label: 'Accuracy', value: '78.6%', tone: 'good' },
  { id: 'mse', label: 'Mean Squared Error', value: '246.30', tone: 'neutral' },
  { id: 'r2', label: 'R2 Score', value: '0.42', tone: 'neutral' },
  {
    id: 'confusion',
    label: 'Confusion Matrix Summary',
    value: 'TP: 34 | TN: 67 | FP: 12 | FN: 19',
    tone: 'info'
  }
];
