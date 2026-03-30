import SectionHeader from './SectionHeader';
import { metrics } from '../data/mockData';

function MetricsSection() {
  return (
    <section id="model-metrics" className="section" aria-labelledby="metrics-title">
      <div className="container">
        <SectionHeader
          eyebrow="Model Metrics"
          title="Performance Analytics"
          description="Mock performance figures are displayed in a production-style analytics layout."
        />
        <div className="card-grid four-col">
          {metrics.map((metric) => (
            <article key={metric.id} className={`surface-card metric-card ${metric.tone}`}>
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
