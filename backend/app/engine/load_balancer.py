from typing import List, Dict

class LoadBalancer:
    def __init__(self, algorithm: str = "round_robin"):
        self.algorithm = algorithm
        self.rr_index = 0
        self.request_counts = {}

    def route_request(self, backends: List[Dict]) -> Dict:
        """Routes a request to an available backend based on the algorithm."""
        
        # 1. Health-Aware Routing (Filter out unhealthy nodes)
        healthy_nodes = [n for n in backends if n.get("status") == "healthy"]
        
        if not healthy_nodes:
            return {"error": "No healthy backends available"}

        # 2. Algorithm Selection
        if self.algorithm == "round_robin":
            node = healthy_nodes[self.rr_index % len(healthy_nodes)]
            self.rr_index += 1
            
        elif self.algorithm == "least_connections":
            # Find the node with the fewest active connections
            node = min(healthy_nodes, key=lambda x: x.get("active_connections", 0))
            
        else:
            # Default fallback
            node = healthy_nodes[0]

        # 3. Update stats
        node_id = node["id"]
        if node_id not in self.request_counts:
            self.request_counts[node_id] = 0
        self.request_counts[node_id] += 1
        node["active_connections"] = node.get("active_connections", 0) + 1
        
        return {"routed_to": node, "algorithm": self.algorithm}

# Global instance for state retention across requests
lb_engine = LoadBalancer(algorithm="round_robin")