export default function AttributionBreakdown({ attribution }) {
  const { modulating_factors, likely_source_profile } = attribution;

  const renderBars = (data, color) => {
    return Object.entries(data)
      .sort(([,a], [,b]) => b - a)
      .map(([key, value]) => (
        <div key={key} style={{ marginBottom: 12 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 4 }}>
            <span style={{ textTransform: 'capitalize' }}>{key.replace('_', ' ')}</span>
            <span style={{ color: 'var(--text-secondary)' }}>{Math.round(value * 100)}%</span>
          </div>
          <div className="progress-bar-bg">
            <div 
              className="progress-bar-fill" 
              style={{ width: `${value * 100}%`, backgroundColor: color }}
            ></div>
          </div>
        </div>
      ));
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <h3 className="section-title" style={{ color: '#a78bfa' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          Weather & Trend Impacts
        </h3>
        <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 16 }}>How weather and historical trends are making the pollution better or worse right now.</p>
        {renderBars(modulating_factors, '#a78bfa')}
      </div>

      <div style={{ height: 1, background: 'var(--glass-border)' }}></div>

      <div>
        <h3 className="section-title" style={{ color: '#34d399' }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
          Primary Pollution Sources
        </h3>
        <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 16 }}>What is actually emitting the pollution in this area (based on real emission datasets).</p>
        {renderBars(likely_source_profile, '#34d399')}
      </div>
    </div>
  );
}
