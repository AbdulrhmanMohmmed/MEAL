import { useState, useEffect } from 'react';
import api from '../services/api';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { Users, FolderKanban, DollarSign, BarChart3, Target, MessageSquareWarning, MapPin, TrendingUp } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [charts, setCharts] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get('/dashboard/stats'),
      api.get('/dashboard/charts/beneficiaries-by-governorate'),
      api.get('/dashboard/charts/projects-by-sector'),
      api.get('/dashboard/charts/budget-by-project'),
      api.get('/dashboard/charts/indicator-progress'),
    ]).then(([statsRes, govRes, sectorRes, budgetRes, indicatorRes]) => {
      setStats(statsRes.data);
      setCharts({
        governorates: govRes.data,
        sectors: sectorRes.data,
        budgets: budgetRes.data,
        indicators: indicatorRes.data,
      });
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="text-gray-400">جاري التحميل...</div></div>;
  if (!stats) return <div className="text-center text-red-500 py-8">خطأ في تحميل البيانات</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">لوحة المعلومات الرئيسية</h1>
          <p className="text-gray-500 text-sm mt-1">نظرة شاملة على أداء البرامج والمؤشرات</p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="المشاريع النشطة" value={stats.projects.active} subtitle={`من ${stats.projects.total} مشروع`} icon={FolderKanban} color="blue" />
        <StatCard title="المستفيدين" value={stats.beneficiaries.total} subtitle={`${stats.beneficiaries.active} نشط`} icon={Users} color="green" />
        <StatCard title="نسبة صرف الميزانية" value={`${stats.budget.utilization}%`} subtitle={`$${(stats.budget.spent / 1000).toFixed(0)}K من $${(stats.budget.total / 1000).toFixed(0)}K`} icon={DollarSign} color="amber" />
        <StatCard title="تحقيق المؤشرات" value={`${stats.indicators.achievement}%`} subtitle={`${stats.indicators.on_track} على المسار من ${stats.indicators.total}`} icon={Target} color="purple" />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Beneficiaries by Governorate */}
        <div className="card">
          <h3 className="font-bold text-gray-800 mb-4">المستفيدين حسب المحافظة</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={charts.governorates}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="governorate" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Projects by Sector */}
        <div className="card">
          <h3 className="font-bold text-gray-800 mb-4">المشاريع حسب القطاع</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={charts.sectors} dataKey="count" nameKey="sector" cx="50%" cy="50%" outerRadius={100} label={({ sector, count }) => `${sector}: ${count}`}>
                {charts.sectors?.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Budget by Project */}
        <div className="card">
          <h3 className="font-bold text-gray-800 mb-4">الميزانية والصرف حسب المشروع</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={charts.budgets} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 11 }} />
              <YAxis dataKey="name" type="category" width={150} tick={{ fontSize: 10 }} />
              <Tooltip formatter={(v) => `$${v.toLocaleString()}`} />
              <Bar dataKey="budget" fill="#93c5fd" name="الميزانية" radius={[0, 4, 4, 0]} />
              <Bar dataKey="spent" fill="#3b82f6" name="المصروف" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Indicator Progress */}
        <div className="card">
          <h3 className="font-bold text-gray-800 mb-4">تقدم المؤشرات</h3>
          <div className="space-y-3 max-h-[300px] overflow-y-auto">
            {charts.indicators?.map((ind, i) => (
              <div key={i}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-700 truncate ml-2">{ind.name}</span>
                  <span className="font-bold text-gray-900">{ind.progress}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5">
                  <div
                    className={`h-2.5 rounded-full ${ind.progress >= 80 ? 'bg-emerald-500' : ind.progress >= 50 ? 'bg-amber-500' : 'bg-red-500'}`}
                    style={{ width: `${Math.min(100, ind.progress)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard title="الشكاوى المعلقة" value={stats.complaints.pending} icon={MessageSquareWarning} color="red" />
        <StatCard title="الزيارات الميدانية القادمة" value={stats.field_visits.upcoming} icon={MapPin} color="indigo" />
        <StatCard title="المنح النشطة" value={stats.grants.active} subtitle={`من ${stats.grants.total} منحة`} icon={TrendingUp} color="green" />
      </div>
    </div>
  );
}
