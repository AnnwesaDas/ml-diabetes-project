import SectionHeader from './SectionHeader';
import { aboutCards } from '../data/mockData';

function AboutSection() {
  return (
    <section className="section" aria-labelledby="about-title">
      <div className="container">
        <SectionHeader
          eyebrow="About"
          title="Dataset and Learning Goals"
          description="A compact overview of what this lab project teaches and how the dataset is used."
        />
        <div className="card-grid three-col">
          {aboutCards.map((item) => (
            <article key={item.title} className="surface-card fade-up">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default AboutSection;
