from fastapi import APIRouter, status
from core.state import SIMULATION_STATE

router = APIRouter()

@router.get("/visualization/snapshot", status_code=status.HTTP_200_OK)
async def get_visualization_snapshot():
    """
    Returns the live data currently held in the server's memory, 
    including satellites, debris, and collision warnings.
    """
    
    # 1. Format the Satellites
    formatted_satellites = []
    for sat_id, data in SIMULATION_STATE["satellites"].items():
        formatted_satellites.append({
            "id": sat_id,
            "x": data["r"]["x"],
            "y": data["r"]["y"],
            "z": data["r"]["z"]
        })
        
    # 2. Format the Debris
    formatted_debris = []
    for deb_id, data in SIMULATION_STATE["debris"].items():
        formatted_debris.append({
            "id": deb_id,
            "x": data["r"]["x"],
            "y": data["r"]["y"],
            "z": data["r"]["z"]
        })

    # 3. Pull the warnings from memory (Calculated by the KD-Tree in telemetry.py)
    warnings = SIMULATION_STATE.get("active_warnings", [])

    return {
        "timestamp": SIMULATION_STATE["last_updated"],
        "total_tracked_objects": len(formatted_satellites) + len(formatted_debris),
        "warning_count": len(warnings),
        "active_warnings": warnings,  # This will now show the ID pairs and distances
        "satellites": formatted_satellites,
        "debris": formatted_debris
    }