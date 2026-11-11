import httpx
from sqlalchemy.orm import Session
from app.models.node import ComputeNode
from fastapi import HTTPException

class ResourceAllocator:
    @staticmethod
    def allocate(db: Session, vm_req: dict, strategy: str = "first_fit") -> ComputeNode:
        # 1. Fetch all online nodes from PostgreSQL
        nodes = db.query(ComputeNode).filter(ComputeNode.status == "online").all()
        if not nodes:
            raise HTTPException(status_code=400, detail="No online nodes available.")

        # 2. Format data for the C++ Engine
        nodes_data = [
            {
                "id": str(n.id),
                "total_cpu": n.total_cpu, "used_cpu": n.used_cpu,
                "total_ram": n.total_ram, "used_ram": n.used_ram,
                "total_storage": n.total_storage, "used_storage": n.used_storage
            } for n in nodes
        ]

        payload = {
            "nodes": nodes_data,
            "vm": vm_req,
            "strategy": strategy
        }

        # 3. Call the C++ Microservice!
        try:
            with httpx.Client() as client:
                res = client.post("http://cpp-engine:8080/allocate", json=payload, timeout=5.0)
                if res.status_code == 400:
                    raise HTTPException(status_code=400, detail="Insufficient cluster capacity. No suitable node found.")
                res.raise_for_status()
                selected_node_id = res.json()["node_id"]
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"C++ Engine unreachable: {str(e)}")

        # 4. Update the database with the allocated resources
        selected_node = next((n for n in nodes if str(n.id) == selected_node_id), None)
        if not selected_node:
            raise HTTPException(status_code=500, detail="C++ Engine returned an invalid node ID.")

        selected_node.used_cpu += vm_req["cpu"]
        selected_node.used_ram += vm_req["ram"]
        selected_node.used_storage += vm_req["storage"]
        db.commit()
        
        return selected_node