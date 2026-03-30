import HeroSection from './components/HeroSection';
import TopNavbar from './components/TopNavbar';
import DashboardHighlightsSection from './components/DashboardHighlightsSection';
import PredictionFormSection from './components/PredictionFormSection';
import VisualizationsSection from './components/VisualizationsSection';
import PipelineSection from './components/PipelineSection';
import MetricsSection from './components/MetricsSection';
import FooterSection from './components/FooterSection';

function App() {
  return (
    <div className="app-shell">
      <TopNavbar />
      <main>
        <HeroSection />
        <DashboardHighlightsSection />
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
