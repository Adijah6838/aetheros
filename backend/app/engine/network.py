import heapq
from typing import Dict, List, Tuple

class NetworkGraph:
    def __init__(self):
        # Adjacency list: { node_id: [(neighbor_id, latency), ...] }
        self.graph: Dict[str, List[Tuple[str, int]]] = {}

    def add_edge(self, u: str, v: str, latency: int):
        if u not in self.graph: self.graph[u] = []
        if v not in self.graph: self.graph[v] = []
        self.graph[u].append((v, latency))
        self.graph[v].append((u, latency)) # Undirected network

    def dijkstra(self, start: str, end: str) -> Tuple[List[str], int]:
        """Returns the shortest path and total latency using Dijkstra's algorithm."""
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        
        previous_nodes = {node: None for node in self.graph}
        pq = [(0, start)] # (distance, node)

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_dist > distances[current_node]:
                continue
            if current_node == end:
                break

            for neighbor, latency in self.graph.get(current_node, []):
                distance = current_dist + latency
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        if distances[end] == float('inf'):
            return [], -1
        return path, distances[end]