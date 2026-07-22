import { useState, useEffect } from 'react';
import axios from 'axios';
import MapView from './components/MapView';
import StationDrilldown from './components/StationDrilldown';
import './index.css';

const CITIES = {
  "Delhi": [28.6139, 77.2090],
  "Mumbai": [19.0760, 72.8777],
  "Bengaluru": [12.9716, 77.5946],
  "Chennai": [13.0827, 80.2707],
  "Kolkata": [22.5726, 88.3639],
  "Hyderabad": [17.3850, 78.4867],
  "Pune": [18.5204, 73.8567],
  "Ahmedabad": [23.0225, 72.5714],
  "Jaipur": [26.9124, 75.7873],
  "Lucknow": [26.8467, 80.9462]
};

function App() {
  const [stations, setStations] = useState([]);
  const [selectedCity, setSelectedCity] = useState("Delhi");
  const [selectedStation, setSelectedStation] = useState(null);

  useEffect(() => {
    // Fetch stations on load
    axios.get('https://etaihackathon.onrender.com/api/stations')
      .then(res => {
        setStations(res.data);
      })
      .catch(err => console.error("Error fetching stations", err));
  }, []);

  const filteredStations = stations.filter(s => s.city === selectedCity);

  useEffect(() => {
    if (filteredStations.length > 0 && (!selectedStation || selectedStation.city !== selectedCity)) {
      setSelectedStation(filteredStations[0]);
    }
  }, [selectedCity, filteredStations, selectedStation]);

  return (
    <>
      <header className="app-header">
        <div className="app-title">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop stopColor="#60a5fa" offset="0%" />
              <stop stopColor="#a78bfa" offset="100%" />
            </linearGradient>
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
          </svg>
          AQI Sentinel
        </div>
        
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <span style={{ color: 'var(--text-secondary)', fontSize: 14 }}>City:</span>
          <select 
            value={selectedCity} 
            onChange={(e) => setSelectedCity(e.target.value)}
            style={{
              background: 'rgba(255,255,255,0.05)', color: '#fff', border: '1px solid var(--glass-border)', 
              padding: '6px 12px', borderRadius: 8, fontSize: 15, cursor: 'pointer', outline: 'none'
            }}
          >
            {Object.keys(CITIES).map(city => (
              <option key={city} value={city} style={{ background: '#1a1d29' }}>{city}</option>
            ))}
          </select>
        </div>

        <div className="city-stats">
          <div className="stat-pill">
            <span style={{ color: 'var(--text-secondary)' }}>{selectedCity} Avg</span>
            <span style={{ color: 'var(--aqi-very-poor)', fontWeight: 'bold' }}>320 (Very Poor)</span>
          </div>
        </div>
      </header>
      
      <main className="layout-grid">
        <div className="map-container glass-panel animate-fade-in" style={{ padding: 0 }}>
          <MapView 
            stations={filteredStations} 
            selectedStation={selectedStation}
            onSelectStation={setSelectedStation}
            cityCenter={CITIES[selectedCity]}
          />
        </div>
        
        <div className="sidebar">
          {selectedStation && (
            <StationDrilldown station={selectedStation} />
          )}
        </div>
      </main>
    </>
  );
}

export default App;
