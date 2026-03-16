import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function TelemetryHeatmap({ satellites }) {
  // If the backend isn't sending data yet, show a standby message
  if (!satellites || satellites.length === 0) {
    return (
      <div style={{ color: '#888', textAlign: 'center', marginTop: '40px' }}>
        Awaiting telemetry feed...
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '85%', marginTop: '10px' }}>
      <ResponsiveContainer>
        <BarChart data={satellites} margin={{ top: 20, right: 10, left: -20, bottom: 0 }}>
          <XAxis 
            dataKey="id" 
            stroke="#45a29e" 
            tick={{ fill: '#c5c6c7', fontSize: 10 }} 
          />
          {/* We lock the Y-axis to 50 because that's the max initial fuel capacity */}
          <YAxis 
            stroke="#45a29e" 
            domain={[0, 50]} 
            tick={{ fill: '#c5c6c7', fontSize: 12 }} 
          />
          <Tooltip 
            cursor={{ fill: 'rgba(255, 255, 255, 0.1)' }}
            contentStyle={{ backgroundColor: '#0b0c10', borderColor: '#45a29e', color: '#c5c6c7' }}
            itemStyle={{ color: '#66fcf1' }}
          />
          <Bar dataKey="fuel_kg" name="Fuel (kg)" radius={[4, 4, 0, 0]}>
            {satellites.map((satellite, index) => {
              // Color-code the fuel levels just like a real dashboard
              let color = '#2ecc71'; // Safe: Green
              if (satellite.fuel_kg <= 5.0) {
                 color = '#e74c3c'; // Critical: Red (Under 10%)
              } else if (satellite.fuel_kg <= 15.0) {
                 color = '#f1c40f'; // Warning: Yellow
              }
              return <Cell key={`cell-${index}`} fill={color} />;
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}