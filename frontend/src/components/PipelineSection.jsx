import SectionHeader from './SectionHeader';
import { pipelineSteps } from '../data/mockData';

function PipelineSection() {
  return (
    <section className="section section-alt" aria-labelledby="pipeline-title">
      <div className="container">
        <SectionHeader
          eyebrow="Workflow"
          title="Machine Learning Pipeline"
          description="A simple step-by-step timeline of the project flow from raw data to model prediction."
        />

        <ol className="pipeline-list">
          {pipelineSteps.map((step, index) => (
            <li key={step} className="pipeline-step fade-up">
              <span className="step-index">{String(index + 1).padStart(2, '0')}</span>
              <span className="step-label">{step}</span>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

export default PipelineSection;
