from fastapi import APIRouter, status
from core.state import SIMULATION_STATE  # Import the filing cabinet

router = APIRouter()

@router.get("/visualization/snapshot", status_code=status.HTTP_200_OK)
async def get_visualization_snapshot():
    """
    Returns the live data currently held in the server's memory.
    """
    
    # Format the data exactly how the frontend visualizer expects it
    formatted_satellites = []
    for sat_id, data in SIMULATION_STATE["satellites"].items():
        formatted_satellites.append({
            "id": sat_id,
            "x": data["r"]["x"],
            "y": data["r"]["y"],
            "z": data["r"]["z"]
            # We will calculate Lat/Lon and Fuel later!
        })

    return {
        "timestamp": SIMULATION_STATE["last_updated"],
        "total_tracked_objects": len(SIMULATION_STATE["satellites"]) + len(SIMULATION_STATE["debris"]),
        "satellites": formatted_satellites
    }