from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="EdgeFleet")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

robots = {
    "AMR-01": {
        "x": 1.0,
        "y": 1.0,
        "battery": 95,
        "status": "IDLE",
    },
    "AMR-02": {
        "x": 5.0,
        "y": 2.0,
        "battery": 87,
        "status": "IDLE",
    },
    "AMR-03": {
        "x": 2.0,
        "y": 6.0,
        "battery": 76,
        "status": "IDLE",
    },
}


@app.get("/")
def root():
    return {
        "system": "EdgeFleet",
        "status": "running",
        "time": datetime.now().isoformat(),
    }


@app.get("/robots")
def get_robots():
    return robots