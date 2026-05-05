import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import StatCard from '../components/StatCard';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { MessageSquareWarning, CheckCircle, Clock, Plus } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function Accountability() {
  const [complaints, setComplaints] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => {
    Promise.all([
      api.get('/accountability/complaints'),
      api.get('/accountability/summary'),
    ]).then(([cRes, sRes]) => { setComplaints(cRes.data); setSummary(sRes.data); setLoading(false); }).catch(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/accountability/complaints/${form.id}`, form);
      else await api.post('/accountability/complaints', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert(err.response?.data?.detail || 'خطأ'); }
  };

  const columns = [
    { header: 'الرقم المرجعي', accessor: 'reference_number' },
    { header: 'القناة', accessor: 'channel', render: r => ({ phone:'هاتف', box:'صندوق', whatsapp:'واتساب', in_person:'حضوري', sms:'رسالة', email:'بريد' }[r.channel] || r.channel) },
    { header: 'التصنيف', accessor: 'category', render: r => ({ service_quality:'جودة الخدمة', targeting:'الاستهداف', distribution:'التوزيع', staff_behavior:'سلوك الموظفين', suggestion:'اقتراح' }[r.category] || r.category) },
    { header: 'الأولوية', accessor: 'priority', render: r => <StatusBadge status={r.priority} /> },
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
    { header: 'الموقع', accessor: 'location' },
    { header: 'التاريخ', accessor: 'created_at', render: r => r.created_at?.split('T')[0] || r.created_at?.split(' ')[0] },
  ];

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  const channelData = summary ? Object.entries(summary.by_channel).map(([k, v]) => ({ name: k, value: v })) : [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">المساءلة - آلية الشكاوى والملاحظات (CFM)</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> شكوى جديدة</button>
      </div>

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard title="إجمالي الشكاوى" value={summary.total} icon={MessageSquareWarning} color="blue" />
          <StatCard title="تم الحل" value={summary.resolved} icon={CheckCircle} color="green" />
          <StatCard title="معلقة" value={summary.total - summary.resolved} icon={Clock} color="amber" />
          <StatCard title="نسبة الحل" value={`${summary.resolution_rate}%`} color="purple" />
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card lg:col-span-2">
          <h3 className="font-bold mb-4">قائمة الشكاوى والملاحظات</h3>
          <DataTable columns={columns} data={complaints} onRowClick={r => { setForm(r); setShowModal(true); }} />
        </div>
        <div className="card">
          <h3 className="font-bold mb-4">حسب القناة</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={channelData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {channelData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تفاصيل الشكوى' : 'شكوى جديدة'} size="lg">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <div className="col-span-2"><label className="block text-sm font-medium mb-1">الوصف *</label><textarea className="input-field" rows={3} value={form.description||''} onChange={e=>setForm({...form,description:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">القناة</label>
            <select className="input-field" value={form.channel||'phone'} onChange={e=>setForm({...form,channel:e.target.value})}>
              <option value="phone">هاتف</option><option value="box">صندوق</option><option value="whatsapp">واتساب</option><option value="in_person">حضوري</option><option value="sms">رسالة</option>
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">التصنيف</label>
            <select className="input-field" value={form.category||'other'} onChange={e=>setForm({...form,category:e.target.value})}>
              <option value="service_quality">جودة الخدمة</option><option value="targeting">الاستهداف</option><option value="distribution">التوزيع</option><option value="staff_behavior">سلوك الموظفين</option><option value="suggestion">اقتراح</option><option value="other">أخرى</option>
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">الأولوية</label>
            <select className="input-field" value={form.priority||'medium'} onChange={e=>setForm({...form,priority:e.target.value})}>
              <option value="low">منخفضة</option><option value="medium">متوسطة</option><option value="high">مرتفعة</option><option value="critical">حرجة</option>
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">الموقع</label><input className="input-field" value={form.location||''} onChange={e=>setForm({...form,location:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">اسم مقدم الشكوى</label><input className="input-field" value={form.complainant_name||''} onChange={e=>setForm({...form,complainant_name:e.target.value})} /></div>
          <div className="flex items-center gap-2"><input type="checkbox" checked={form.is_anonymous||false} onChange={e=>setForm({...form,is_anonymous:e.target.checked})} /><label className="text-sm">مجهول الهوية</label></div>
          {form.id && <div className="col-span-2"><label className="block text-sm font-medium mb-1">الحل</label><textarea className="input-field" rows={2} value={form.resolution||''} onChange={e=>setForm({...form,resolution:e.target.value})} /></div>}
          {form.id && <div><label className="block text-sm font-medium mb-1">الحالة</label>
            <select className="input-field" value={form.status||''} onChange={e=>setForm({...form,status:e.target.value})}>
              <option value="received">مستلمة</option><option value="under_review">قيد المراجعة</option><option value="in_progress">قيد التنفيذ</option><option value="resolved">محلولة</option><option value="closed">مغلقة</option>
            </select>
          </div>}
          <div className="col-span-2 flex gap-3 justify-end">
            <button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button>
            <button type="submit" className="btn-primary">{form.id?'تحديث':'تسجيل'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
