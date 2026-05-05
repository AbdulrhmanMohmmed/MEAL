import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import StatCard from '../components/StatCard';
import { Plus, ShieldAlert, AlertTriangle } from 'lucide-react';

export default function Risks() {
  const [risks, setRisks] = useState([]);
  const [matrix, setMatrix] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => {
    Promise.all([api.get('/risks/'), api.get('/risks/matrix')]).then(([r, m]) => {
      setRisks(r.data); setMatrix(m.data); setLoading(false);
    }).catch(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/risks/${form.id}`, form);
      else await api.post('/risks/', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert('خطأ'); }
  };

  const columns = [
    { header: 'الخطر', accessor: 'title', render: r => <span className="font-medium">{r.title}</span> },
    { header: 'التصنيف', accessor: 'category' },
    { header: 'الاحتمالية', accessor: 'likelihood' },
    { header: 'الأثر', accessor: 'impact' },
    { header: 'الدرجة', accessor: 'risk_score', render: r => <span className="font-bold">{r.risk_score}</span> },
    { header: 'المستوى', accessor: 'risk_level', render: r => <StatusBadge status={r.risk_level} /> },
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
  ];

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  const matrixColors = [[0,'#d1fae5'],[6,'#fef3c7'],[12,'#fed7aa'],[20,'#fecaca']];
  const getColor = (score) => { for (let i = matrixColors.length-1; i >= 0; i--) if (score >= matrixColors[i][0]) return matrixColors[i][1]; return '#f0f0f0'; };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">سجل المخاطر</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> خطر جديد</button>
      </div>

      {matrix && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatCard title="مخاطر مفتوحة" value={matrix.total_open} icon={ShieldAlert} color="blue" />
          <StatCard title="حرجة" value={matrix.critical} icon={AlertTriangle} color="red" />
          <StatCard title="عالية" value={matrix.high} icon={AlertTriangle} color="amber" />
        </div>
      )}

      {matrix && (
        <div className="card">
          <h3 className="font-bold mb-4">مصفوفة المخاطر</h3>
          <div className="overflow-x-auto">
            <table className="text-sm text-center">
              <thead><tr><th className="p-2">الاحتمالية / الأثر</th>{[1,2,3,4,5].map(i=><th key={i} className="p-2">{i}</th>)}</tr></thead>
              <tbody>{[5,4,3,2,1].map(l=>(
                <tr key={l}><td className="p-2 font-bold">{l}</td>
                  {[1,2,3,4,5].map(i=><td key={i} className="p-2 w-16 h-12 rounded" style={{backgroundColor:getColor(l*i)}}>{matrix.matrix[l-1]?.[i-1]||0}</td>)}
                </tr>
              ))}</tbody>
            </table>
          </div>
        </div>
      )}

      <div className="card"><h3 className="font-bold mb-4">قائمة المخاطر</h3><DataTable columns={columns} data={risks} onRowClick={r=>{setForm(r);setShowModal(true);}} /></div>

      <Modal isOpen={showModal} onClose={()=>setShowModal(false)} title={form.id?'تعديل الخطر':'خطر جديد'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">العنوان *</label><input className="input-field" value={form.title||''} onChange={e=>setForm({...form,title:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">الوصف</label><textarea className="input-field" rows={2} value={form.description||''} onChange={e=>setForm({...form,description:e.target.value})} /></div>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium mb-1">التصنيف</label>
              <select className="input-field" value={form.category||''} onChange={e=>setForm({...form,category:e.target.value})}>
                <option value="">اختر</option>{["أمني","تشغيلي","مالي","سمعة","بيئي","صحي"].map(c=><option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium mb-1">الاحتمالية (1-5)</label><input type="number" min="1" max="5" className="input-field" value={form.likelihood||3} onChange={e=>setForm({...form,likelihood:parseInt(e.target.value)})} /></div>
            <div><label className="block text-sm font-medium mb-1">الأثر (1-5)</label><input type="number" min="1" max="5" className="input-field" value={form.impact||3} onChange={e=>setForm({...form,impact:parseInt(e.target.value)})} /></div>
          </div>
          <div><label className="block text-sm font-medium mb-1">إجراءات التخفيف</label><textarea className="input-field" rows={2} value={form.mitigation||''} onChange={e=>setForm({...form,mitigation:e.target.value})} /></div>
          <div className="flex gap-3 justify-end"><button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button><button type="submit" className="btn-primary">{form.id?'تحديث':'إنشاء'}</button></div>
        </form>
      </Modal>
    </div>
  );
}
