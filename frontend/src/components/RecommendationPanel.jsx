import { useState } from 'react';

export default function RecommendationPanel({ recommendation }) {
  const [lang, setLang] = useState('en');

  if (!recommendation.action) return null;

  const advisories = recommendation.advisories[lang];

  return (
    <div>
      <h3 className="section-title" style={{ color: '#60a5fa' }}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        Suggested Intervention
      </h3>
      
      <div className="recommendation-action">
        {recommendation.action}
      </div>

      <div style={{ marginTop: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <h4 style={{ fontSize: 14, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: 1 }}>Citizen Advisory (Demo)</h4>
          <div className="advisory-tabs">
            <button className={`tab-btn ${lang === 'en' ? 'active' : ''}`} onClick={() => setLang('en')}>EN</button>
            <button className={`tab-btn ${lang === 'hi' ? 'active' : ''}`} onClick={() => setLang('hi')}>HI</button>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {Object.entries(advisories).map(([audience, text]) => (
            <div key={audience} className="advisory-content">
              <strong style={{ display: 'block', marginBottom: 4, textTransform: 'capitalize', color: '#fff' }}>
                {audience.replace('_', ' ')}
              </strong>
              {text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
