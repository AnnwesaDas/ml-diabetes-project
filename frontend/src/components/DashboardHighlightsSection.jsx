import SectionHeader from './SectionHeader';
import { dashboardHighlights } from '../data/mockData';

function DashboardHighlightsSection() {
  return (
    <section id="dashboard-overview" className="section" aria-labelledby="highlights-title">
      <div className="container">
        <SectionHeader
          eyebrow="Dashboard Highlights"
          title="Project Snapshot"
          description="Quick model and dataset indicators designed like a healthcare analytics product overview."
        />

        <div className="card-grid four-col">
          {dashboardHighlights.map((item) => (
            <article key={item.id} className="surface-card highlight-card">
              <p className="highlight-label">{item.label}</p>
              <h3>{item.value}</h3>
              <p className="highlight-helper">{item.helper}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default DashboardHighlightsSection;
