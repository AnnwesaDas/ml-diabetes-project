import HeroSection from './components/HeroSection';
import AboutSection from './components/AboutSection';
import PredictionFormSection from './components/PredictionFormSection';
import VisualizationsSection from './components/VisualizationsSection';
import PipelineSection from './components/PipelineSection';
import MetricsSection from './components/MetricsSection';
import FooterSection from './components/FooterSection';

function App() {
  return (
    <div className="app-shell">
      <main>
        <HeroSection />
        <AboutSection />
        <PredictionFormSection />
        <VisualizationsSection />
        <PipelineSection />
        <MetricsSection />
      </main>
      <FooterSection />
    </div>
  );
}

export default App;
