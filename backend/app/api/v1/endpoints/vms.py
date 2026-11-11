from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.vm import VirtualMachine
from app.schemas.vm import VMCreate, VMResponse
from app.services.allocation import ResourceAllocator
import redis
import json
from app.core.config import settings

router = APIRouter()
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/", response_model=VMResponse)
def create_vm(
    vm_in: VMCreate, 
    strategy: str = Query("first_fit", description="first_fit, best_fit, worst_fit, balanced"),
    db: Session = Depends(get_db)
):
    vm_dict = vm_in.model_dump()
    node = ResourceAllocator.allocate(db, vm_dict, strategy=strategy)

    vm = VirtualMachine(
        node_id=node.id,
        name=vm_in.name,
        os_profile=vm_in.os_profile,
        cpu=vm_in.cpu,
        ram=vm_in.ram,
        storage=vm_in.storage,
        status="running"
    )
    db.add(vm)
    db.commit()
    db.refresh(vm)

    # Publish event to WebSockets via Redis!
    redis_client.publish("infra_events", json.dumps({
        "event": "VM_CREATED",
        "vm_name": vm.name,
        "node_name": node.name,
        "strategy_used": strategy
    }))

    return vm

@router.get("/", response_model=List[VMResponse])
def list_vms(db: Session = Depends(get_db)):
    return db.query(VirtualMachine).all()