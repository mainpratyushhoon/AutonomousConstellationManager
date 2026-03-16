import React from 'react';
import { 
  ScatterChart, Scatter, XAxis, YAxis, ZAxis, 
  CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceDot 
} from 'recharts';

export default function ConjunctionBullseye({ debrisData }) {
  // Since we don't have real collision math from the backend yet, 
  // we are mocking 5 pieces of debris flying towards our satellite.
  // dx and dy are their relative distances on the X and Y axes in kilometers.
  const mockCloseApproaches = [
    { id: 'DEB-842', dx: 0.5, dy: 0.8, distance: 0.94 },  // Critical 
    { id: 'DEB-103', dx: -2.1, dy: 1.5, distance: 2.58 }, // Warning 
    { id: 'DEB-992', dx: 6.0, dy: -4.2, distance: 7.32 }, // Safe 
    { id: 'DEB-711', dx: -0.2, dy: -0.6, distance: 0.63 },// Critical 
    { id: 'DEB-404', dx: 3.5, dy: 3.5, distance: 4.94 },  // Warning 
  ];

  const data = debrisData || mockCloseApproaches;

  return (
    <div style={{ width: '100%', height: '85%', marginTop: '10px' }}>
      <ResponsiveContainer>
        {/* We lock the domain from -10km to 10km to create a radar view */}
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#45a29e" opacity={0.3} />
          
          {/* Radar Crosshairs */}
          <XAxis type="number" dataKey="dx" name="Rel X (km)" domain={[-10, 10]} stroke="#45a29e" tick={{ fill: '#c5c6c7' }} />
          <YAxis type="number" dataKey="dy" name="Rel Y (km)" domain={[-10, 10]} stroke="#45a29e" tick={{ fill: '#c5c6c7' }} />
          {/* ZAxis controls the dot size based on distance! */}
          <ZAxis type="number" dataKey="distance" range={[50, 150]} name="Distance" unit=" km" />
          
          <Tooltip 
            cursor={{ strokeDasharray: '3 3' }} 
            contentStyle={{ backgroundColor: '#0b0c10', borderColor: '#45a29e', color: '#c5c6c7' }}
            itemStyle={{ color: '#66fcf1' }}
          />
          
          {/* The "Satellite" pinned dead center at (0,0) */}
          <ReferenceDot x={0} y={0} r={6} fill="#66fcf1" stroke="none" />

          {/* The Debris Cloud */}
          <Scatter name="Incoming Debris" data={data}>
            {data.map((entry, index) => {
              // Hackathon Risk Indexing Logic!
              let dotColor = '#2ecc71'; // Green = Safe (> 5km)
              if (entry.distance < 1.0) {
                dotColor = '#e74c3c';   // Red = Critical (< 1km)
              } else if (entry.distance <= 5.0) {
                dotColor = '#f1c40f';   // Yellow = Warning (< 5km)
              }
              return <Cell key={`cell-${index}`} fill={dotColor} />;
            })}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}