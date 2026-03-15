from fastapi import FastAPI
from contextlib import asynccontextmanager

from api import telemetry, maneuver, simulate, visualization
from core.station_loader import load_ground_stations

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing ACM Core Systems...")
    load_ground_stations()
    yield
    print("Shutting down ACM Core Systems...")

app = FastAPI(
    title="Autonomous Constellation Manager (ACM)",
    description="Backend API for Project AETHER - National Space Hackathon 2026",
    version="1.0.0",
    lifespan=lifespan
)

# The prefix="/api" here automatically adds "/api" to all routes in these files
app.include_router(telemetry.router, prefix="/api", tags=["Telemetry"])
app.include_router(maneuver.router, prefix="/api", tags=["Maneuver Scheduling"])
app.include_router(simulate.router, prefix="/api", tags=["Simulation"])
app.include_router(visualization.router, prefix="/api", tags=["Visualization"])

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "ACM API is online. Navigate to /docs for Swagger UI."
    }