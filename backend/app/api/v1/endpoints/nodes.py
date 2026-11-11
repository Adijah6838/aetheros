from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.node import ComputeNode
from app.schemas.node import NodeCreate, NodeResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/", response_model=NodeResponse)
def create_node(node_in: NodeCreate, db: Session = Depends(get_db)):
    node = ComputeNode(
        name=node_in.name,
        total_cpu=node_in.total_cpu,
        total_ram=node_in.total_ram,
        total_storage=node_in.total_storage
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    return node

@router.get("/", response_model=List[NodeResponse])
def list_nodes(db: Session = Depends(get_db)):
    return db.query(ComputeNode).all()