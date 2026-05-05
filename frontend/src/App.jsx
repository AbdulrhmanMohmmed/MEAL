import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Beneficiaries from './pages/Beneficiaries';
import Projects from './pages/Projects';
import Activities from './pages/Activities';
import Monitoring from './pages/Monitoring';
import Indicators from './pages/Indicators';
import Accountability from './pages/Accountability';
import Learning from './pages/Learning';
import MEALPlan from './pages/MEALPlan';
import LogFrame from './pages/LogFrame';
import FieldVisits from './pages/FieldVisits';
import Finance from './pages/Finance';
import Cash from './pages/Cash';
import Inventory from './pages/Inventory';
import HR from './pages/HR';
import DataCollection from './pages/DataCollection';
import Reports from './pages/Reports';
import Documents from './pages/Documents';
import Risks from './pages/Risks';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center h-screen"><div className="text-gray-400">جاري التحميل...</div></div>;
  if (!user) return <Navigate to="/login" />;
  return <Layout>{children}</Layout>;
}

function AppRoutes() {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center h-screen"><div className="text-gray-400">جاري التحميل...</div></div>;

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/beneficiaries" element={<ProtectedRoute><Beneficiaries /></ProtectedRoute>} />
      <Route path="/projects" element={<ProtectedRoute><Projects /></ProtectedRoute>} />
      <Route path="/activities" element={<ProtectedRoute><Activities /></ProtectedRoute>} />
      <Route path="/monitoring" element={<ProtectedRoute><Monitoring /></ProtectedRoute>} />
      <Route path="/indicators" element={<ProtectedRoute><Indicators /></ProtectedRoute>} />
      <Route path="/accountability" element={<ProtectedRoute><Accountability /></ProtectedRoute>} />
      <Route path="/learning" element={<ProtectedRoute><Learning /></ProtectedRoute>} />
      <Route path="/meal-plan" element={<ProtectedRoute><MEALPlan /></ProtectedRoute>} />
      <Route path="/logframe" element={<ProtectedRoute><LogFrame /></ProtectedRoute>} />
      <Route path="/field-visits" element={<ProtectedRoute><FieldVisits /></ProtectedRoute>} />
      <Route path="/finance" element={<ProtectedRoute><Finance /></ProtectedRoute>} />
      <Route path="/cash" element={<ProtectedRoute><Cash /></ProtectedRoute>} />
      <Route path="/inventory" element={<ProtectedRoute><Inventory /></ProtectedRoute>} />
      <Route path="/hr" element={<ProtectedRoute><HR /></ProtectedRoute>} />
      <Route path="/data-collection" element={<ProtectedRoute><DataCollection /></ProtectedRoute>} />
      <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
      <Route path="/documents" element={<ProtectedRoute><Documents /></ProtectedRoute>} />
      <Route path="/risks" element={<ProtectedRoute><Risks /></ProtectedRoute>} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
