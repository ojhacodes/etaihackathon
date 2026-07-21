import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

function MapController({ center }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, 11, { duration: 1.5 });
  }, [center, map]);
  return null;
}

export default function MapView({ stations, selectedStation, onSelectStation, cityCenter }) {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    if (selectedStation) {
      axios.get(`https://etaihackathon.onrender.com/api/weather/${selectedStation.lat}/${selectedStation.lon}`)
        .then(res => setWeather(res.data))
        .catch(err => console.error("Failed to fetch weather", err));
    } else {
      setWeather(null);
    }
  }, [selectedStation]);

  return (
    <>
      <div style={{ position: 'absolute', top: 16, left: 16, zIndex: 1000, background: 'rgba(0,0,0,0.7)', padding: '8px 12px', borderRadius: '8px', border: '1px solid var(--glass-border)', fontSize: '12px', backdropFilter: 'blur(4px)' }}>
        <span style={{ color: 'var(--accent)', fontWeight: 600 }}>Interpolated Surface:</span> 1km resolution grid from station data
      </div>
      
      {weather && !weather.error && (
        <div className="glass-panel animate-fade-in" style={{ 
          position: 'absolute', top: 16, right: 16, zIndex: 1000, 
          padding: '12px 16px', display: 'flex', flexDirection: 'column', gap: '8px',
          minWidth: '180px'
        }}>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Live Meteorology
          </div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '24px', fontWeight: 'bold' }}>{Math.round(weather.temp)}°C</span>
            <img src={`https://openweathermap.org/img/wn/${weather.icon}.png`} alt="weather icon" style={{ width: 40, height: 40, margin: '-10px' }} />
          </div>
          <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{weather.description}</div>
          <div style={{ display: 'flex', gap: '12px', marginTop: '4px', fontSize: '12px' }}>
            <span title="Humidity">💧 {weather.humidity}%</span>
            <span title="Wind Speed">💨 {Math.round(weather.wind_speed)} km/h</span>
          </div>
        </div>
      )}

      <MapContainer 
        center={cityCenter || [28.6139, 77.2090]} 
        zoom={11} 
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
      >
        <MapController center={cityCenter || [28.6139, 77.2090]} />
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors'
        />
        
        {stations.map(station => (
          <CircleMarker
            key={station.id}
            center={[station.lat, station.lon]}
            radius={8}
            pathOptions={{ 
              fillColor: selectedStation?.id === station.id ? '#fff' : 'var(--aqi-very-poor)',
              color: '#000',
              weight: 2,
              fillOpacity: 0.8
            }}
            eventHandlers={{
              click: () => onSelectStation(station)
            }}
          >
            <Popup>
              <strong>{station.name}</strong><br/>
              Current AQI: 320
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </>
  );
}
