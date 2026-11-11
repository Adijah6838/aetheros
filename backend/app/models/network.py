import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class NetworkNode(Base):
    __tablename__ = "network_nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # router, switch, server, load_balancer
    status = Column(String, default="online")
    created_at = Column(DateTime, default=datetime.utcnow)

class NetworkLink(Base):
    __tablename__ = "network_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("network_nodes.id"), nullable=False)
    bandwidth = Column(Integer, nullable=False) # Mbps
    latency = Column(Integer, nullable=False) # ms
    status = Column(String, default="active")