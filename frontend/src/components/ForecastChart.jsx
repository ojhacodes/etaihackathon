import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

export default function ForecastChart({ forecast }) {
  // Generate some mock time series based on the forecast endpoint
  const data = [];
  const base = forecast.baseline_value;
  const target = forecast.forecast_value;
  
  for(let i=0; i<=24; i+=3) {
    // interpolate towards target
    const progress = i / 24;
    const modelVal = base + (target - base) * progress + (Math.random() * 20 - 10);
    
    data.push({
      time: `+${i}h`,
      model: Math.round(modelVal),
      baseline: Math.round(base) // persistence baseline is flat
    });
  }

  return (
    <div style={{ height: 200, width: '100%', marginTop: 16 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
          <XAxis dataKey="time" stroke="var(--text-secondary)" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="var(--text-secondary)" fontSize={12} tickLine={false} axisLine={false} domain={['dataMin - 50', 'dataMax + 50']} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'rgba(15,17,26,0.9)', border: '1px solid var(--glass-border)', borderRadius: 8, backdropFilter: 'blur(4px)' }}
            itemStyle={{ color: '#fff' }}
          />
          <Line type="monotone" dataKey="model" stroke="var(--accent)" strokeWidth={3} dot={{ r: 4, fill: 'var(--bg-dark)' }} activeDot={{ r: 6 }} name="LightGBM Forecast" />
          <Line type="step" dataKey="baseline" stroke="var(--text-secondary)" strokeWidth={2} strokeDasharray="5 5" dot={false} name="Persistence Baseline" />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', gap: 16, justifyContent: 'center', fontSize: 12, color: 'var(--text-secondary)', marginTop: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 12, height: 3, background: 'var(--accent)' }}></div> LightGBM Model
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 12, height: 3, borderTop: '2px dashed var(--text-secondary)' }}></div> Persistence Baseline
        </div>
      </div>
    </div>
  );
}
