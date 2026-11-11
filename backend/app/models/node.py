import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class ComputeNode(Base):
    __tablename__ = "compute_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="online") # online, offline, failed
    
    # Total Capacity
    total_cpu = Column(Integer, nullable=False) # in cores
    total_ram = Column(Integer, nullable=False) # in MB
    total_storage = Column(Integer, nullable=False) # in GB
    
    # Allocated Resources
    used_cpu = Column(Integer, default=0)
    used_ram = Column(Integer, default=0)
    used_storage = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)