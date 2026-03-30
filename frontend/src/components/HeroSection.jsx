function HeroSection() {
  return (
    <section id="hero-dashboard" className="hero-section" aria-labelledby="project-title">
      <div className="container hero-grid">
        <div className="hero-content">
          <span className="hero-bubble bubble-one" aria-hidden="true" />
          <span className="hero-bubble bubble-two" aria-hidden="true" />
          <span className="hero-bubble bubble-three" aria-hidden="true" />
          <span className="badge">AI-Powered Healthcare Analytics</span>
          <h1 id="project-title">
            Diabetes Risk
            <br />
            Prediction Engine
          </h1>
          <p>
            Advanced machine learning models for early diabetes detection and glucose estimation.
            Empowering clinicians with data-driven insights for proactive patient care.
          </p>
          <div className="hero-actions">
            <a className="btn-primary" href="#prediction-workspace">
              Run Prediction
            </a>
            <a className="btn-ghost" href="#insights-visualizations">
              Explore Insights
            </a>
          </div>
        </div>
        <aside className="hero-note">
          <h3>Platform Summary</h3>
          <p>
            Explore two ML tasks in one interface: classification for diabetes outcome and
            regression for glucose estimation, supported by visual diagnostics and metrics.
          </p>
          <p className="note-small">For educational use only. Not medical advice.</p>
        </aside>
      </div>
    </section>
  );
}

export default HeroSection;
