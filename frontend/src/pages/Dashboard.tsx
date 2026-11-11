import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [events, setEvents] = useState<any[]>([]);
  const [wsStatus, setWsStatus] = useState('🔴 Disconnected');

  // Fetch Nodes (for the chart)
  const { data: nodes } = useQuery({
    queryKey: ['nodes'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/nodes/');
      return res.json();
    }
  });

  // Connect to WebSockets
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/');
    ws.onopen = () => setWsStatus('🟢 Live Monitoring Active');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setEvents((prev) => [`[${new Date().toLocaleTimeString()}] ${data.event}: ${data.vm_name} deployed to ${data.node_name} (${data.strategy_used})`, ...prev].slice(0, 10));
    };
    return () => { ws.onclose = null; ws.close(); }
  }, []);

  const chartData = nodes?.map((n: any) => ({
    name: n.name,
    "CPU Used": n.used_cpu,
    "CPU Available": n.total_cpu - n.used_cpu,
    "RAM Used": Math.round(n.used_ram / 1024),
    "RAM Available": Math.round((n.total_ram - n.used_ram) / 1024)
  })) || [];

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-400">Infrastructure Dashboard</h1>
        <span className={`px-4 py-2 rounded-full text-sm font-bold ${wsStatus.includes('🟢') ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
          {wsStatus}
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recharts Cluster Utilization */}
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl mb-4 text-slate-200">Cluster Resource Utilization (GB)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155' }} />
              <Bar dataKey="CPU Used" stackId="a" fill="#3b82f6" />
              <Bar dataKey="CPU Available" stackId="a" fill="#1e3a8a" />
              <Bar dataKey="RAM Used" stackId="b" fill="#10b981" />
              <Bar dataKey="RAM Available" stackId="b" fill="#064e3b" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Live Event Stream */}
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <h2 className="text-xl mb-4 text-slate-200">Live Infrastructure Events</h2>
          <div className="bg-black p-4 rounded border border-slate-600 h-[300px] overflow-y-auto font-mono text-sm text-green-400">
            {events.length === 0 ? 'Waiting for events... (Create a VM to see live updates)' : events.map((e, i) => <div key={i}>{e}</div>)}
          </div>
        </div>
      </div>
    </div>
  );
}