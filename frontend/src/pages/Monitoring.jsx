import { useState, useEffect } from 'react';
import api from '../services/api';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import Modal from '../components/Modal';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Target, TrendingUp, AlertTriangle, XCircle, Plus } from 'lucide-react';

export default function Monitoring() {
  const [indicators, setIndicators] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedIndicator, setSelectedIndicator] = useState(null);
  const [measurements, setMeasurements] = useState([]);

  useEffect(() => {
    Promise.all([
      api.get('/monitoring/indicators'),
      api.get('/monitoring/summary'),
    ]).then(([indRes, sumRes]) => {
      setIndicators(indRes.data);
      setSummary(sumRes.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const showMeasurements = async (ind) => {
    setSelectedIndicator(ind);
    const res = await api.get(`/monitoring/indicators/${ind.id}/measurements`);
    setMeasurements(res.data);
    setShowModal(true);
  };

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">المتابعة والتقييم</h1>

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard title="إجمالي المؤشرات" value={summary.total_indicators} icon={Target} color="blue" />
          <StatCard title="على المسار" value={summary.on_track} icon={TrendingUp} color="green" />
          <StatCard title="في خطر" value={summary.at_risk} icon={AlertTriangle} color="amber" />
          <StatCard title="خارج المسار" value={summary.off_track} icon={XCircle} color="red" />
        </div>
      )}

      <div className="card">
        <h3 className="font-bold text-gray-800 mb-4">تقدم المؤشرات</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={indicators.slice(0, 8).map(i => ({ name: i.name.substring(0, 25), target: i.target, current: i.current_value }))}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" tick={{ fontSize: 10 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip />
            <Bar dataKey="target" fill="#93c5fd" name="المستهدف" radius={[4,4,0,0]} />
            <Bar dataKey="current" fill="#3b82f6" name="الفعلي" radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3 className="font-bold text-gray-800 mb-4">جدول المؤشرات</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-right py-3 px-4">المؤشر</th>
                <th className="text-right py-3 px-4">النوع</th>
                <th className="text-right py-3 px-4">خط الأساس</th>
                <th className="text-right py-3 px-4">المستهدف</th>
                <th className="text-right py-3 px-4">الفعلي</th>
                <th className="text-right py-3 px-4">التقدم</th>
                <th className="text-right py-3 px-4">الحالة</th>
              </tr>
            </thead>
            <tbody>
              {indicators.map(ind => (
                <tr key={ind.id} className="border-b border-gray-50 hover:bg-gray-50 cursor-pointer" onClick={() => showMeasurements(ind)}>
                  <td className="py-3 px-4 font-medium">{ind.name}</td>
                  <td className="py-3 px-4">{ind.indicator_type === 'output' ? 'مخرج' : ind.indicator_type === 'outcome' ? 'نتيجة' : 'أثر'}</td>
                  <td className="py-3 px-4">{ind.baseline} {ind.unit}</td>
                  <td className="py-3 px-4">{ind.target} {ind.unit}</td>
                  <td className="py-3 px-4 font-bold">{ind.current_value} {ind.unit}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-100 rounded-full h-2"><div className={`h-2 rounded-full ${ind.progress >= 80 ? 'bg-emerald-500' : ind.progress >= 50 ? 'bg-amber-500' : 'bg-red-500'}`} style={{width:`${Math.min(100,ind.progress)}%`}} /></div>
                      <span className="text-xs font-bold">{ind.progress}%</span>
                    </div>
                  </td>
                  <td className="py-3 px-4"><StatusBadge status={ind.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={`القياسات - ${selectedIndicator?.name || ''}`} size="lg">
        {selectedIndicator && (
          <div>
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-50 p-3 rounded-lg"><p className="text-xs text-gray-500">خط الأساس</p><p className="font-bold">{selectedIndicator.baseline}</p></div>
              <div className="bg-gray-50 p-3 rounded-lg"><p className="text-xs text-gray-500">المستهدف</p><p className="font-bold">{selectedIndicator.target}</p></div>
              <div className="bg-blue-50 p-3 rounded-lg"><p className="text-xs text-gray-500">الفعلي</p><p className="font-bold text-blue-600">{selectedIndicator.current_value}</p></div>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={measurements}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </Modal>
    </div>
  );
}
