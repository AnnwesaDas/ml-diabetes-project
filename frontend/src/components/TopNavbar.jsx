import { useState } from 'react';

const navLinks = [
  { label: 'Dashboard', href: '#hero-dashboard' },
  { label: 'Overview', href: '#dashboard-overview' },
  { label: 'Prediction', href: '#prediction-workspace' },
  { label: 'Insights', href: '#insights-visualizations' },
  { label: 'Workflow', href: '#workflow-pipeline' },
  { label: 'Metrics', href: '#model-metrics' }
];

function TopNavbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="top-nav-wrap">
      <div className="container top-nav">
        <a className="brand" href="#hero-dashboard">
          <img
            className="brand-logo"
            src="/diabetes-logo.svg"
            alt="Diabetes Risk Prediction logo"
            width="30"
            height="30"
          />
          ML Diabetes Project
        </a>

        <nav className="top-nav-links" aria-label="Primary">
          {navLinks.map((link) => (
            <a key={link.label} href={link.href}>
              {link.label}
            </a>
          ))}
        </nav>

        <button
          className="menu-toggle"
          type="button"
          aria-label="Toggle navigation"
          aria-expanded={open}
          onClick={() => setOpen((prev) => !prev)}
        >
          Menu
        </button>
      </div>

      {open ? (
        <nav className="mobile-nav" aria-label="Mobile Primary">
          {navLinks.map((link) => (
            <a key={link.label} href={link.href} onClick={() => setOpen(false)}>
              {link.label}
            </a>
          ))}
        </nav>
      ) : null}
    </header>
  );
}

export default TopNavbar;