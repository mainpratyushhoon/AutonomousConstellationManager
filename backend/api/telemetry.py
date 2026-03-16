from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List
from backend.core.state import SIMULATION_STATE  # Import our filing cabinet
from backend.core.collision import detect_collisions  # <-- NEW: Import the KD-Tree radar

router = APIRouter()

class Vector3D(BaseModel):
    x: float
    y: float
    z: float

class TelemetryObject(BaseModel):
    id: str
    type: str
    r: Vector3D
    v: Vector3D

class TelemetryPayload(BaseModel):
    timestamp: str
    objects: List[TelemetryObject]

@router.post("/telemetry", status_code=status.HTTP_200_OK)
async def ingest_telemetry(payload: TelemetryPayload):
    # Update the timestamp
    SIMULATION_STATE["last_updated"] = payload.timestamp
    
    # Sort the incoming data into the correct filing cabinets
    for obj in payload.objects:
        if obj.type == "SATELLITE":
            SIMULATION_STATE["satellites"][obj.id] = {"r": obj.r.dict(), "v": obj.v.dict()}
        elif obj.type == "DEBRIS":
            SIMULATION_STATE["debris"][obj.id] = {"r": obj.r.dict(), "v": obj.v.dict()}

    # <-- NEW: Trigger the K-D Tree scan on the freshly updated data
    collision_warnings = detect_collisions(SIMULATION_STATE)
    
    # Save the warnings into the server's memory so other endpoints can see them
    SIMULATION_STATE["active_warnings"] = collision_warnings

    # Print a critical alert to your terminal if satellites are in danger
    if collision_warnings:
        print(f"CRITICAL: {len(collision_warnings)} collisions detected!")

    return {
        "status": "ACK",
        "processed_count": len(payload.objects),
        "active_cdm_warnings": len(collision_warnings)  # <-- NEW: Return the actual count instead of 0
    }