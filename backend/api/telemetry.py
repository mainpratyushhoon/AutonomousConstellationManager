from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List
from core.state import SIMULATION_STATE  # Import our new filing cabinet

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

    return {
        "status": "ACK",
        "processed_count": len(payload.objects),
        "active_cdm_warnings": 0
    }