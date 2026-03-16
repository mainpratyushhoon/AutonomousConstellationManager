import React from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { Map } from 'react-map-gl/maplibre';

// Initial camera view (centered roughly over the equator)
const INITIAL_VIEW_STATE = {
  longitude: 0,
  latitude: 0,
  zoom: 1.5,
  pitch: 0,
  bearing: 0
};

export default function GroundTrackMap({ satellites, debrisCloud }) {
  
  // 1. Create the layer for the 10,000+ Debris Objects
  const debrisLayer = new ScatterplotLayer({
    id: 'debris-layer',
    data: debrisCloud,
    // Debris format is [ID, Lat, Lon, Alt]. We need [Lon, Lat]
    getPosition: d => [d[2], d[1]], 
    getFillColor: [255, 65, 54, 180], // Red, slightly transparent
    getRadius: 20000, // Radius in meters
    radiusMinPixels: 2, // Never let the dot get smaller than 2 pixels
    pickable: true,
  });

  // 2. Create the layer for the 50+ Satellites
  const satelliteLayer = new ScatterplotLayer({
    id: 'satellite-layer',
    data: satellites,
    // Satellite format is an object: { id, lat, lon, fuel_kg, status }
    getPosition: d => [d.lon, d.lat], 
    getFillColor: [46, 204, 113, 255], // Bright Green
    getRadius: 50000, // Make satellites bigger than debris
    radiusMinPixels: 4,
    pickable: true,
  });

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', minHeight: '400px' }}>
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true} // Allows user to pan and zoom
        layers={[debrisLayer, satelliteLayer]}
      >
        {/* The Base Map of the Earth */}
        <Map
          mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
        />
      </DeckGL>
    </div>
  );
}