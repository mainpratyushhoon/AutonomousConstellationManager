import GroundTrackMap from './components/GroundTrackMap';
import TelemetryHeatmap from './components/TelemetryHeatmap';
import ConjunctionBullseye from './components/ConjunctionBullseye';
import ManeuverTimeline from './components/ManeuverTimeline';
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State to hold the massive payload from the backend
  const [telemetry, setTelemetry] = useState({ satellites: [], debris_cloud: [], conjunctions: [], maneuvers: [] });

  // Step 4.1: The API Polling Engine
  useEffect(() => {
    // This fetches data from your backend's snapshot endpoint
    const fetchSnapshot = async () => {
      try {
        // Hitting the specific endpoint required by the hackathon [cite: 753, 908]
        const response = await fetch('http://localhost:8000/api/visualization/snapshot');
        const data = await response.json();
        
        // Make sure we have valid arrays before setting state to prevent crashes
        setTelemetry({
          satellites: data.satellites || [],
          debris_cloud: data.debris_cloud || [],
          conjunctions: data.conjunctions || [],
          maneuvers: []
        });
      } catch (error) {
        console.error("Failed to fetch telemetry. Is the Python backend running?", error);
      }
    };

    // Poll the backend every 1 second (1000 milliseconds)
    const intervalId = setInterval(fetchSnapshot, 1000);
    
    // Cleanup the interval if the component ever unmounts
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="dashboard-container">
      <header>
        <h1>Orbital Insight Visualizer</h1>
      </header>
      
      <main className="grid-layout">
        {/* Module 1: The Ground Track Map */}
        <section className="module map-module">
          <h2>Ground Track (Mercator Projection)</h2>
          <div style={{ position: 'relative', flexGrow: 1, height: '85%', marginTop: '10px' }}>
            <GroundTrackMap 
               satellites={telemetry.satellites} 
               debrisCloud={telemetry.debris_cloud} 
            />
          </div>
          <p style={{ marginTop: '5px' }}>
            Tracking {telemetry.satellites.length} Sats & {telemetry.debris_cloud.length} Debris
          </p>
        </section>

        {/* Module 2: The Conjunction Bullseye Plot */}
        <section className="module polar-module">
          <h2>Conjunction "Bullseye" Plot</h2>
          <ConjunctionBullseye debrisData={telemetry.conjunctions}/>
          {/* Recharts Polar Chart will go here */}
        </section>

        {/* Module 3: Telemetry & Resource Heatmaps */}
        <section className="module telemetry-module">
          <h2>Fleet Telemetry & Fuel</h2>
          <TelemetryHeatmap satellites={telemetry.satellites} />
          {/* Visual fuel gauges go here */}
        </section>

        {/* Module 4: The Maneuver Timeline */}
        <section className="module timeline-module">
          <h2>Maneuver Timeline (Gantt)</h2>
          <ManeuverTimeline maneuvers={telemetry.maneuvers} />
          {/* Scheduler showing burn times and 600-second cooldowns goes here */}
        </section>
      </main>
    </div>
  );
}

export default App;