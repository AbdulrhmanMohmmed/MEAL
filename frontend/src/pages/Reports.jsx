import { useState, useEffect } from 'react';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { FileText, Download, Users, Target, DollarSign, Package } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function Reports() {
  const [activeReport, setActiveReport] = useState('project');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const reports = [
    { id: 'project', label: 'تقدم المشاريع', icon: FileText, endpoint: '/reports/project-progress' },
    { id: 'beneficiary', label: 'ملخص المستفيدين', icon: Users, endpoint: '/reports/beneficiary-summary' },
    { id: 'indicator', label: 'تتبع المؤشرات', icon: Target, endpoint: '/reports/indicator-tracking' },
    { id: 'financial', label: 'الملخص المالي', icon: DollarSign, endpoint: '/reports/financial-summary' },
    { id: 'accountability', label: 'المساءلة', icon: Package, endpoint: '/reports/accountability-summary' },
  ];

  const loadReport = (id) => {
    const report = reports.find(r => r.id === id);
    if (!report) return;
    setActiveReport(id); setLoading(true);
    api.get(report.endpoint).then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
  };

  useEffect(() => { loadReport('project'); }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">التقارير</h1>
      <div className="flex gap-2 flex-wrap">
        {reports.map(r => {
          const Icon = r.icon;
          return (
            <button key={r.id} onClick={() => loadReport(r.id)} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeReport === r.id ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
              <Icon className="w-4 h-4" />{r.label}
            </button>
          );
        })}
      </div>
      <div className="card">
        {loading ? <div className="text-center py-8 text-gray-400">جاري التحميل...</div> : data && (
          <div>
            {activeReport === 'project' && Array.isArray(data) && (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead><tr className="border-b">{['المشروع','الحالة','الميزانية','المصروف','الصرف %','المستهدفين','الواصلين','الوصول %'].map(h=><th key={h} className="text-right py-3 px-3">{h}</th>)}</tr></thead>
                  <tbody>{data.map((p,i)=>(
                    <tr key={i} className="border-b border-gray-50">
                      <td className="py-3 px-3 font-medium">{p.project}</td><td className="py-3 px-3">{p.status}</td>
                      <td className="py-3 px-3">${p.budget?.toLocaleString()}</td><td className="py-3 px-3">${p.spent?.toLocaleString()}</td>
                      <td className="py-3 px-3">{p.budget_utilization}%</td><td className="py-3 px-3">{p.target_beneficiaries?.toLocaleString()}</td>
                      <td className="py-3 px-3">{p.reached_beneficiaries?.toLocaleString()}</td><td className="py-3 px-3">{p.beneficiary_reach}%</td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            )}
            {activeReport === 'beneficiary' && data.by_governorate && (
              <div>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg"><p className="text-sm text-gray-500">الإجمالي</p><p className="text-2xl font-bold">{data.total?.toLocaleString()}</p></div>
                  <div className="bg-amber-50 p-4 rounded-lg"><p className="text-sm text-gray-500">النازحين</p><p className="text-2xl font-bold">{data.idp_count}</p></div>
                  <div className="bg-purple-50 p-4 rounded-lg"><p className="text-sm text-gray-500">أسر تعيلها امرأة</p><p className="text-2xl font-bold">{data.female_headed}</p></div>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.by_governorate}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="governorate" tick={{fontSize:11}} /><YAxis /><Tooltip /><Bar dataKey="count" fill="#3b82f6" radius={[4,4,0,0]} /></BarChart>
                </ResponsiveContainer>
              </div>
            )}
            {activeReport === 'indicator' && data.indicators && (
              <div>
                <div className="grid grid-cols-4 gap-4 mb-6">
                  <div className="bg-blue-50 p-3 rounded-lg text-center"><p className="text-xs">الإجمالي</p><p className="text-xl font-bold">{data.total_indicators}</p></div>
                  <div className="bg-emerald-50 p-3 rounded-lg text-center"><p className="text-xs">على المسار</p><p className="text-xl font-bold text-emerald-600">{data.on_track}</p></div>
                  <div className="bg-amber-50 p-3 rounded-lg text-center"><p className="text-xs">في خطر</p><p className="text-xl font-bold text-amber-600">{data.at_risk}</p></div>
                  <div className="bg-red-50 p-3 rounded-lg text-center"><p className="text-xs">خارج المسار</p><p className="text-xl font-bold text-red-600">{data.off_track}</p></div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm"><thead><tr className="border-b">{['المؤشر','النوع','خط الأساس','المستهدف','الفعلي','التحقيق %'].map(h=><th key={h} className="text-right py-3 px-3">{h}</th>)}</tr></thead>
                    <tbody>{data.indicators.map((ind,i)=>(
                      <tr key={i} className="border-b border-gray-50"><td className="py-3 px-3">{ind.name}</td><td className="py-3 px-3">{ind.type}</td><td className="py-3 px-3">{ind.baseline}</td><td className="py-3 px-3">{ind.target}</td><td className="py-3 px-3 font-bold">{ind.current}</td>
                        <td className="py-3 px-3"><span className={ind.achievement>=80?'text-emerald-600':ind.achievement>=50?'text-amber-600':'text-red-600'}>{ind.achievement}%</span></td></tr>
                    ))}</tbody>
                  </table>
                </div>
              </div>
            )}
            {activeReport === 'financial' && data.grants && (
              <div>
                <div className="grid grid-cols-4 gap-4 mb-6">
                  <div className="bg-blue-50 p-3 rounded-lg text-center"><p className="text-xs">إجمالي التمويل</p><p className="text-xl font-bold">${(data.total_funding/1000).toFixed(0)}K</p></div>
                  <div className="bg-amber-50 p-3 rounded-lg text-center"><p className="text-xs">المصروف</p><p className="text-xl font-bold">${(data.total_spent/1000).toFixed(0)}K</p></div>
                  <div className="bg-emerald-50 p-3 rounded-lg text-center"><p className="text-xs">المتبقي</p><p className="text-xl font-bold">${(data.remaining/1000).toFixed(0)}K</p></div>
                  <div className="bg-purple-50 p-3 rounded-lg text-center"><p className="text-xs">نسبة الصرف</p><p className="text-xl font-bold">{data.utilization_rate}%</p></div>
                </div>
              </div>
            )}
            {activeReport === 'accountability' && (
              <div className="grid grid-cols-4 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg text-center"><p className="text-sm">إجمالي الشكاوى</p><p className="text-2xl font-bold">{data.total_complaints}</p></div>
                <div className="bg-emerald-50 p-4 rounded-lg text-center"><p className="text-sm">تم الحل</p><p className="text-2xl font-bold">{data.resolved}</p></div>
                <div className="bg-amber-50 p-4 rounded-lg text-center"><p className="text-sm">معلقة</p><p className="text-2xl font-bold">{data.pending}</p></div>
                <div className="bg-purple-50 p-4 rounded-lg text-center"><p className="text-sm">نسبة الحل</p><p className="text-2xl font-bold">{data.resolution_rate}%</p></div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
