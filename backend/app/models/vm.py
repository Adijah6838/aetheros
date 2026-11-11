import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class VirtualMachine(Base):
    __tablename__ = "virtual_machines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    node_id = Column(UUID(as_uuid=True), ForeignKey("compute_nodes.id"), nullable=False)
    name = Column(String, nullable=False)
    os_profile = Column(String, nullable=False)
    status = Column(String, default="running") # created, running, stopped, failed
    
    # Allocated Resources
    cpu = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    storage = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)