from fastapi import APIRouter, status
from backend.core.state import SIMULATION_STATE
from backend.core.coordinates import eci_to_lat_lon_alt # <-- Import your conversion math!

router = APIRouter()

@router.get("/visualization/snapshot", status_code=status.HTTP_200_OK)
async def get_visualization_snapshot():
    
    timestamp = SIMULATION_STATE.get("last_updated", "2026-03-12T08:00:00.000Z")
    
    # 1. Format the Satellites (Converting ECI to Lat/Lon)
    formatted_satellites = []
    for sat_id, data in SIMULATION_STATE.get("satellites", {}).items():
        # Do the math!
        lat, lon, alt = eci_to_lat_lon_alt(
            data["r"]["x"], 
            data["r"]["y"], 
            data["r"]["z"], 
            timestamp
        )
        
        formatted_satellites.append({
            "id": sat_id,
            "lat": round(lat, 3), # Rounding makes the JSON payload smaller
            "lon": round(lon, 3),
            "fuel_kg": data.get("mass", 50.0), # Required by UI fuel gauge [cite: 240, 221]
            "status": "NOMINAL"                # Required by UI [cite: 241]
        })
        
    # 2. Format the Debris (Flattened structure for massive compression)
    formatted_debris = []
    for deb_id, data in SIMULATION_STATE.get("debris", {}).items():
        lat, lon, alt = eci_to_lat_lon_alt(
            data["r"]["x"], 
            data["r"]["y"], 
            data["r"]["z"], 
            timestamp
        )
        
        # Structure MUST be exactly: [ID, Lat, Lon, Alt] 
        formatted_debris.append([
            deb_id,
            round(lat, 3),
            round(lon, 3),
            round(alt, 3)
        ])

    active_warnings = SIMULATION_STATE.get("active_warnings", [])
    predictive_warnings = SIMULATION_STATE.get("predictive_cdms", [])

    return {
        "timestamp": timestamp,
        "total_tracked_objects": len(formatted_satellites) + len(formatted_debris),
        "warning_count": len(active_warnings),
        "active_warnings": active_warnings, 
        "predictive_warning_count": len(predictive_warnings),
        "predictive_warnings": predictive_warnings,
        "satellites": formatted_satellites,
        "debris_cloud": formatted_debris # Ensure this key is 'debris_cloud' [cite: 244]
    }