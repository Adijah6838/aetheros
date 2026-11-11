import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Network from './pages/Network';
import Dashboard from './pages/Dashboard';

const queryClient = new QueryClient();

function Nav() {
  const location = useLocation();
  return (
    <div className="bg-slate-900 p-4 flex gap-6 border-b border-slate-700 items-center">
      <h2 className="text-xl font-bold text-blue-500">AetherOS</h2>
      <Link to="/" className={`text-sm ${location.pathname === '/' ? 'text-blue-400' : 'text-slate-400 hover:text-white'}`}>Dashboard</Link>
      <Link to="/network" className={`text-sm ${location.pathname === '/network' ? 'text-blue-400' : 'text-slate-400 hover:text-white'}`}>Network Topology</Link>
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-900 text-slate-200">
          <Nav />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/network" element={<Network />} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}