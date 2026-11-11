from pydantic import BaseModel
from uuid import UUID

class NetworkNodeCreate(BaseModel):
    name: str
    type: str

class NetworkNodeResponse(BaseModel):
    id: UUID
    name: str
    type: str
    status: str

    class Config:
        from_attributes = True

class NetworkLinkCreate(BaseModel):
    source_id: UUID
    target_id: UUID
    bandwidth: int
    latency: int

class NetworkLinkResponse(BaseModel):
    id: UUID
    source_id: UUID
    target_id: UUID
    bandwidth: int
    latency: int
    status: str

    class Config:
        from_attributes = True