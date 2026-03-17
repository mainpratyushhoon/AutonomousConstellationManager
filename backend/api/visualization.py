from fastapi import APIRouter, status
from backend.core.state import SIMULATION_STATE
from backend.core.coordinates import eci_to_lat_lon_alt
import math

router = APIRouter()

CONJUNCTION_THRESHOLD_KM = 5.0


def compute_conjunctions(satellites, debris):
    """
    Very simple conjunction detection:
    find debris within threshold distance of satellites.
    """

    conjunctions = []

    for sat in satellites:
        for deb in debris:

            dx = deb[2] - sat["lon"]
            dy = deb[1] - sat["lat"]

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < CONJUNCTION_THRESHOLD_KM:

                conjunctions.append({
                    "satellite_id": sat["id"],
                    "debris_id": deb[0],
                    "dx": dx,
                    "dy": dy,
                    "distance": round(distance, 3)
                })

    return conjunctions


@router.get("/visualization/snapshot", status_code=status.HTTP_200_OK)
async def get_visualization_snapshot():

    timestamp = SIMULATION_STATE.get(
        "last_updated", "2026-03-12T08:00:00.000Z"
    )

    # Format Satellites
    formatted_satellites = []
    for sat_id, data in SIMULATION_STATE.get("satellites", {}).items():

        lat, lon, alt = eci_to_lat_lon_alt(
            data["r"]["x"],
            data["r"]["y"],
            data["r"]["z"],
            timestamp
        )

        formatted_satellites.append({
            "id": sat_id,
            "lat": round(lat, 3),
            "lon": round(lon, 3),
            "fuel_kg": data.get("mass", 50.0),
            "status": "NOMINAL"
        })

    # Format Debris
    formatted_debris = []
    for deb_id, data in SIMULATION_STATE.get("debris", {}).items():

        lat, lon, alt = eci_to_lat_lon_alt(
            data["r"]["x"],
            data["r"]["y"],
            data["r"]["z"],
            timestamp
        )

        formatted_debris.append([
            deb_id,
            round(lat, 3),
            round(lon, 3),
            round(alt, 3)
        ])

    # Compute conjunction warnings
    conjunctions = compute_conjunctions(
        formatted_satellites,
        formatted_debris
    )

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
        "debris_cloud": formatted_debris,
        "conjunctions": conjunctions
    }