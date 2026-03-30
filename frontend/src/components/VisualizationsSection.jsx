import { useState } from 'react';
import SectionHeader from './SectionHeader';
import { chartCards } from '../data/mockData';

function ChartCard({ card }) {
  const [failed, setFailed] = useState(false);

  return (
    <article className="surface-card chart-card fade-up">
      <div className="chart-media">
        {!failed ? (
          <img src={card.imageUrl} alt={card.title} onError={() => setFailed(true)} loading="lazy" />
        ) : (
          <div className="chart-placeholder">
            <p>{card.title}</p>
            <small>Add image in frontend/public/charts</small>
          </div>
        )}
      </div>
      <div className="chart-content">
        <h3>{card.title}</h3>
        <p>{card.caption}</p>
      </div>
    </article>
  );
}

function VisualizationsSection() {
  return (
    <section className="section" aria-labelledby="visualizations-title">
      <div className="container">
        <SectionHeader
          eyebrow="Visualizations"
          title="Data Exploration Plots"
          description="Swap placeholders with backend or local assets at any time without changing component structure."
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
