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
import AIInsights from './pages/AIInsights';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import AssessmentTools from './pages/AssessmentTools';
import AuditTrail from './pages/AuditTrail';
import ComplianceDashboard from './pages/ComplianceDashboard';
import EvaluationTools from './pages/EvaluationTools';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import FeedbackLoop from './pages/FeedbackLoop';
import Integrations from './pages/Integrations';
import IPTTDashboard from './pages/IPTTDashboard';
import KoBoIntegration from './pages/KoBoIntegration';
import NeedsAssessment from './pages/NeedsAssessment';
import OfflineMode from './pages/OfflineMode';
import Recommendations from './pages/Recommendations';
import RemoteMonitoring from './pages/RemoteMonitoring';
import Safeguarding from './pages/Safeguarding';
import ScheduledReports from './pages/ScheduledReports';
import SectorIndicators from './pages/SectorIndicators';

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
      <Route path="/ai-insights" element={<ProtectedRoute><AIInsights /></ProtectedRoute>} />
      <Route path="/analytics" element={<ProtectedRoute><AnalyticsDashboard /></ProtectedRoute>} />
      <Route path="/assessment-tools" element={<ProtectedRoute><AssessmentTools /></ProtectedRoute>} />
      <Route path="/audit-trail" element={<ProtectedRoute><AuditTrail /></ProtectedRoute>} />
      <Route path="/compliance" element={<ProtectedRoute><ComplianceDashboard /></ProtectedRoute>} />
      <Route path="/evaluation-tools" element={<ProtectedRoute><EvaluationTools /></ProtectedRoute>} />
      <Route path="/executive" element={<ProtectedRoute><ExecutiveDashboard /></ProtectedRoute>} />
      <Route path="/feedback-loop" element={<ProtectedRoute><FeedbackLoop /></ProtectedRoute>} />
      <Route path="/integrations" element={<ProtectedRoute><Integrations /></ProtectedRoute>} />
      <Route path="/iptt" element={<ProtectedRoute><IPTTDashboard /></ProtectedRoute>} />
      <Route path="/kobo" element={<ProtectedRoute><KoBoIntegration /></ProtectedRoute>} />
      <Route path="/needs-assessment" element={<ProtectedRoute><NeedsAssessment /></ProtectedRoute>} />
      <Route path="/offline-mode" element={<ProtectedRoute><OfflineMode /></ProtectedRoute>} />
      <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
      <Route path="/remote-monitoring" element={<ProtectedRoute><RemoteMonitoring /></ProtectedRoute>} />
      <Route path="/safeguarding" element={<ProtectedRoute><Safeguarding /></ProtectedRoute>} />
      <Route path="/scheduled-reports" element={<ProtectedRoute><ScheduledReports /></ProtectedRoute>} />
      <Route path="/sector-indicators" element={<ProtectedRoute><SectorIndicators /></ProtectedRoute>} />
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
