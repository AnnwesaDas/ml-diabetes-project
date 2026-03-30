import { useState } from 'react';
import SectionHeader from './SectionHeader';
import { chartCards } from '../data/mockData';

function ChartCard({ card }) {
  const [failed, setFailed] = useState(false);

  return (
    <article className="surface-card chart-card">
      <div className="chart-head">
        <p>{card.title}</p>
        <span>Analytics</span>
      </div>
      <div className="chart-media">
        {!failed ? (
          <img src={card.imageUrl} alt={card.title} onError={() => setFailed(true)} loading="lazy" />
        ) : (
          <div className="chart-placeholder">
            <p>{card.title}</p>
            <small>Add chart image in frontend/public/charts</small>
          </div>
        )}
      </div>
      <div className="chart-content">
        <h3>{card.title}</h3>
        <p>{card.caption}</p>
        <p className="insight-text">Insight: {card.insight}</p>
      </div>
    </article>
  );
}

function VisualizationsSection() {
  return (
    <section id="insights-visualizations" className="section" aria-labelledby="visualizations-title">
      <div className="container">
        <SectionHeader
          eyebrow="Visualizations"
          title="Insights and Visual Diagnostics"
          description="Use these polished cards for local chart assets now, then swap to backend-generated images later."
        />
        <div className="card-grid three-col">
          {chartCards.map((card) => (
            <ChartCard key={card.id} card={card} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default VisualizationsSection;
