from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class VMCreate(BaseModel):
    name: str
    os_profile: str
    cpu: int
    ram: int
    storage: int

class VMResponse(BaseModel):
    id: UUID
    node_id: UUID
    name: str
    os_profile: str
    status: str
    cpu: int
    ram: int
    storage: int

    class Config:
        from_attributes = True