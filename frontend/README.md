# Frontend (React + Vite)

Modern responsive frontend for the ML Diabetes Project.

Design style:
- Premium healthcare-data dashboard aesthetic
- Responsive product-style sections and cards
- Mock prediction workflow with clear loading, empty, and error states

## Run Locally

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown by Vite (usually http://localhost:5173).

## Build for Production

```bash
npm run build
npm run preview
```

## Component Structure

```text
src/
  components/
    HeroSection.jsx
    DashboardHighlightsSection.jsx
    PredictionFormSection.jsx
    VisualizationsSection.jsx
    PipelineSection.jsx
    MetricsSection.jsx
    FooterSection.jsx
    SectionHeader.jsx
    ResultCard.jsx
  data/
    mockData.js
  services/
    predictionService.js
  styles/
    global.css
  App.jsx
  main.jsx
```

## Chart Images

Copy your chart images into `public/charts/` with these names:
- plot_1_glucose_histogram.png
- plot_2_bmi_vs_glucose_scatter.png
- plot_3_correlation_heatmap.png

If files are missing, the UI shows placeholders automatically.

## API Integration (Future)

Update `src/services/predictionService.js` and replace the mock logic in `runPrediction` with an API call.
