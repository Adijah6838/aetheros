from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class NodeCreate(BaseModel):
    name: str
    total_cpu: int
    total_ram: int
    total_storage: int

class NodeResponse(BaseModel):
    id: UUID
    name: str
    status: str
    total_cpu: int
    total_ram: int
    total_storage: int
    used_cpu: int
    used_ram: int
    used_storage: int

    class Config:
        from_attributes = True