from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.network import NetworkNode, NetworkLink
from app.schemas.network import NetworkNodeCreate, NetworkNodeResponse, NetworkLinkCreate, NetworkLinkResponse
from app.engine.network import NetworkGraph

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/nodes", response_model=NetworkNodeResponse)
def create_network_node(node_in: NetworkNodeCreate, db: Session = Depends(get_db)):
    node = NetworkNode(name=node_in.name, type=node_in.type)
    db.add(node)
    db.commit()
    db.refresh(node)
    return node

@router.get("/nodes", response_model=List[NetworkNodeResponse])
def list_network_nodes(db: Session = Depends(get_db)):
    return db.query(NetworkNode).all()

@router.post("/links", response_model=NetworkLinkResponse)
def create_network_link(link_in: NetworkLinkCreate, db: Session = Depends(get_db)):
    link = NetworkLink(
        source_id=link_in.source_id,
        target_id=link_in.target_id,
        bandwidth=link_in.bandwidth,
        latency=link_in.latency
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

@router.get("/links", response_model=List[NetworkLinkResponse])
def list_network_links(db: Session = Depends(get_db)):
    return db.query(NetworkLink).all()

@router.get("/path")
def find_path(source_id: str, target_id: str, db: Session = Depends(get_db)):
    nodes = db.query(NetworkNode).all()
    links = db.query(NetworkLink).all()

    graph = NetworkGraph()
    for link in links:
        if link.status == "active":
            graph.add_edge(str(link.source_id), str(link.target_id), link.latency)

    path, total_latency = graph.dijkstra(source_id, target_id)
    
    if not path:
        raise HTTPException(status_code=404, detail="No path found between nodes")

    return {"path": path, "total_latency_ms": total_latency}