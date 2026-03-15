from fastapi import APIRouter, status
from core.state import SIMULATION_STATE

router = APIRouter()

@router.get("/visualization/snapshot", status_code=status.HTTP_200_OK)
async def get_visualization_snapshot():
    """
    Returns the live data currently held in the server's memory.
    """
    
    # Format the Satellites
    formatted_satellites = []
    for sat_id, data in SIMULATION_STATE["satellites"].items():
        formatted_satellites.append({
            "id": sat_id,
            "x": data["r"]["x"],
            "y": data["r"]["y"],
            "z": data["r"]["z"]
        })
        
    # Format the Debris (NEW!)
    formatted_debris = []
    for deb_id, data in SIMULATION_STATE["debris"].items():
        formatted_debris.append({
            "id": deb_id,
            "x": data["r"]["x"],
            "y": data["r"]["y"],
            "z": data["r"]["z"]
        })

    return {
        "timestamp": SIMULATION_STATE["last_updated"],
        "total_tracked_objects": len(SIMULATION_STATE["satellites"]) + len(SIMULATION_STATE["debris"]),
        "satellites": formatted_satellites,
        "debris": formatted_debris  # <-- Now we are actually sending it to the browser!
    }