import { useState, useCallback, useEffect } from 'react';
import ReactFlow, { Background, Controls, applyNodeChanges, applyEdgeChanges, addEdge } from 'reactflow';
import 'reactflow/dist/style.css';

export default function Network() {
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);

  // Fetch real network topology from backend
  useEffect(() => {
    const fetchTopology = async () => {
      try {
        const nodeRes = await fetch('http://localhost:8000/api/v1/network/nodes');
        const linkRes = await fetch('http://localhost:8000/api/v1/network/links');
        
        const dbNodes = await nodeRes.json();
        const dbLinks = await linkRes.json();

        // Map to React Flow format
        const rfNodes = dbNodes.map((n: any, i: number) => ({
          id: n.id,
          position: { x: 100 + (i % 3) * 250, y: 100 + Math.floor(i / 3) * 150 },
          data: { label: `${n.name} (${n.type})` },
          style: { background: '#1e293b', color: '#fff', border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' }
        }));

        const rfEdges = dbLinks.map((l: any) => ({
          id: l.id,
          source: l.source_id,
          target: l.target_id,
          label: `${l.latency}ms`,
          animated: true,
          style: { stroke: '#3b82f6' }
        }));

        setNodes(rfNodes);
        setEdges(rfEdges);
      } catch (err) {
        console.error("Failed to load network topology", err);
      }
    };
    fetchTopology();
  }, []);

  const onNodesChange = useCallback((changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)), []);
  const onConnect = useCallback((params: any) => setEdges((eds) => addEdge(params, eds)), []);

  return (
    <div className="h-screen w-full flex flex-col">
      <div className="p-4 bg-slate-800 border-b border-slate-700">
        <h1 className="text-2xl font-bold text-blue-400">Network Topology Simulator</h1>
        <p className="text-slate-400 text-sm">Real-time infrastructure graph powered by React Flow</p>
      </div>
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
        >
          <Background color="#334155" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}