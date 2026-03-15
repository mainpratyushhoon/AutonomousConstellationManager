import requests
import time
import uuid
import math
from datetime import datetime, timezone
from sgp4.api import Satrec, jday

# --- Configuration ---
API_URL = "http://localhost:8000/api/telemetry"
URL_ACTIVE = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
URL_DEBRIS = "https://celestrak.org/NORAD/elements/gp.php?GROUP=debris&FORMAT=tle"

TARGET_SATELLITES = 50
TARGET_DEBRIS = 500  # Start with 500 for testing, scale up to 10,000+ later

def fetch_tle_data(url, limit):
    """Fetches TLE data from CelesTrak and parses it."""
    print(f"Fetching TLE data from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.strip().split("\n")
        
        objects = []
        # TLEs come in blocks of 3 lines: Name, Line 1, Line 2
        for i in range(0, min(len(data), limit * 3), 3):
            if i + 2 < len(data):
                objects.append({
                    "name": data[i].strip(),
                    "line1": data[i+1].strip(),
                    "line2": data[i+2].strip()
                })
        return objects
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def tle_to_state(line1, line2):
    """Converts a TLE to an ECI state vector (r, v) at the current UTC time."""
    sat = Satrec.twoline2rv(line1, line2)
    now = datetime.now(timezone.utc)
    
    jd, fr = jday(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
    )
    
    # e = error code (0 means success), r = position (km), v = velocity (km/s)
    e, r, v = sat.sgp4(jd, fr)
    
    if e != 0:
        return None, None # Propagation error (e.g., decayed orbit)
        
    return r, v

def build_telemetry_object(r, v, obj_id, obj_type):
    """Formats the state vector into the required JSON schema."""
    return {
        "id": obj_id,
        "type": obj_type,
        "r": {"x": r[0], "y": r[1], "z": r[2]},
        "v": {"x": v[0], "y": v[1], "z": v[2]}
    }

def send_telemetry_batch(objects):
    """Fires the JSON payload to the FastAPI backend."""
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "objects": objects
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"[{payload['timestamp']}] Successfully ingested {len(objects)} objects. Server ACK: {response.json().get('status')}")
        else:
            print(f"Server returned error code {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Connection Refused. Is your FastAPI server running on port 8000?")

def run_simulation():
    """Main loop to continuously generate and push data."""
    print("--- Initializing Space Environment ---")
    active_tles = fetch_tle_data(URL_ACTIVE, TARGET_SATELLITES)
    debris_tles = fetch_tle_data(URL_DEBRIS, TARGET_DEBRIS)
    
    print(f"Loaded {len(active_tles)} satellites and {len(debris_tles)} debris fragments.")
    print("Starting continuous telemetry stream... Press Ctrl+C to stop.")
    
    step = 0
    while True:
        telemetry_objects = []
        
        # Process Active Satellites
        for i, tle in enumerate(active_tles):
            r, v = tle_to_state(tle["line1"], tle["line2"])
            if r and v:
                # Use a consistent ID format for active satellites
                obj = build_telemetry_object(r, v, f"SAT-Alpha-{i:02d}", "SATELLITE")
                telemetry_objects.append(obj)
                
        # Process Debris
        for i, tle in enumerate(debris_tles):
            r, v = tle_to_state(tle["line1"], tle["line2"])
            if r and v:
                obj = build_telemetry_object(r, v, f"DEB-{i:05d}", "DEBRIS")
                telemetry_objects.append(obj)
                
        # Send the massive batch to your backend
        send_telemetry_batch(telemetry_objects)
        
        step += 1
        time.sleep(2) # Send updates every 2 seconds

if __name__ == "__main__":
    run_simulation()