from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engine.load_balancer import lb_engine

router = APIRouter()

# In-memory mock list of backend servers
backends = [
    {"id": "srv-1", "name": "App-Server-1", "status": "healthy", "active_connections": 0},
    {"id": "srv-2", "name": "App-Server-2", "status": "healthy", "active_connections": 0},
    {"id": "srv-3", "name": "App-Server-3", "status": "healthy", "active_connections": 0}
]

class AlgorithmChange(BaseModel):
    algorithm: str

@router.get("/backends")
def get_backends():
    return backends

@router.post("/algorithm")
def change_algorithm(data: AlgorithmChange):
    lb_engine.algorithm = data.algorithm
    return {"message": f"Algorithm changed to {data.algorithm}"}

@router.post("/route")
def route_request():
    # The load balancer engine picks the best node based on the current algorithm
    result = lb_engine.route_request(backends)
    if "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
    return result