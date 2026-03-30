import SectionHeader from './SectionHeader';
import { metrics } from '../data/mockData';

function MetricsSection() {
  return (
    <section className="section" aria-labelledby="metrics-title">
      <div className="container">
        <SectionHeader
          eyebrow="Model Metrics"
          title="Performance Snapshot"
          description="Sample values are shown for portfolio/demo use. Replace with backend metrics later."
        />
        <div className="card-grid four-col">
          {metrics.map((metric) => (
            <article key={metric.id} className={`surface-card metric-card ${metric.tone} fade-up`}>
              <p>{metric.label}</p>
              <h3>{metric.value}</h3>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default MetricsSection;
