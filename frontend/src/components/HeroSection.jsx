function HeroSection() {
  return (
    <section className="hero-section" aria-labelledby="project-title">
      <div className="container hero-grid">
        <div className="hero-content fade-up">
          <span className="badge">Educational Project Only</span>
          <h1 id="project-title">Diabetes Risk and Glucose Estimation Dashboard</h1>
          <p>
            Predict diabetes risk and estimate glucose level using machine learning models trained on
            the Pima Indians Diabetes dataset.
          </p>
        </div>
        <aside className="hero-note fade-up">
          <h3>Use Case</h3>
          <p>
            This dashboard demonstrates beginner-friendly ML workflows with classification,
            regression, metrics, and visual insights.
          </p>
          <p className="note-small">For educational use only. Not medical advice.</p>
        </aside>
      </div>
    </section>
  );
}

export default HeroSection;
