import { useState, useEffect } from 'react';
import axios from 'axios';
import ForecastChart from './ForecastChart';
import AttributionBreakdown from './AttributionBreakdown';
import RecommendationPanel from './RecommendationPanel';

export default function StationDrilldown({ station }) {
  const [forecast, setForecast] = useState(null);
  const [attribution, setAttribution] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    // Fetch all drilldown data
    Promise.all([
      axios.get(`http://localhost:8000/api/forecast/${station.id}`),
      axios.get(`http://localhost:8000/api/attribution/${station.id}`),
      axios.get(`http://localhost:8000/api/recommendation/${station.id}`)
    ]).then(([forecastRes, attrRes, recRes]) => {
      setForecast(forecastRes.data);
      setAttribution(attrRes.data);
      setRecommendation(recRes.data);
      setLoading(false);
    }).catch(err => {
      console.error("Failed to load drilldown data", err);
      setLoading(false);
    });
  }, [station.id]);

  if (loading) {
    return <div className="glass-panel animate-fade-in">Loading insights...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <h2 style={{ marginBottom: 8 }}>{station.name}</h2>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
          <span style={{ fontSize: 36, fontWeight: 700, color: 'var(--aqi-very-poor)' }}>{forecast?.baseline_value}</span>
          <span style={{ color: 'var(--text-secondary)' }}>AQI</span>
        </div>
      </div>

      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <h3 className="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
          72h Forecast vs Baseline
        </h3>
        {forecast && <ForecastChart forecast={forecast} />}
      </div>

      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.3s' }}>
        {attribution && <AttributionBreakdown attribution={attribution} />}
      </div>

      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.4s' }}>
        {recommendation && <RecommendationPanel recommendation={recommendation} />}
      </div>
    </div>
  );
}
