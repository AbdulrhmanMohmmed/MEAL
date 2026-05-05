import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import { Plus, MapPin } from 'lucide-react';

export default function FieldVisits() {
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => { api.get('/field-visits/').then(r => { setVisits(r.data); setLoading(false); }).catch(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/field-visits/${form.id}`, form);
      else await api.post('/field-visits/', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert('خطأ'); }
  };

  const columns = [
    { header: 'التاريخ', accessor: 'visit_date' },
    { header: 'الموقع', accessor: 'location' },
    { header: 'الغرض', accessor: 'purpose' },
    { header: 'الزائر', accessor: 'visited_by' },
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
  ];

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">الزيارات الميدانية</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> زيارة جديدة</button>
      </div>
      <div className="card"><DataTable columns={columns} data={visits} onRowClick={r => { setForm(r); setShowModal(true); }} /></div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تفاصيل الزيارة' : 'زيارة جديدة'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">تاريخ الزيارة</label><input type="date" className="input-field" value={form.visit_date||''} onChange={e=>setForm({...form,visit_date:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">الموقع</label><input className="input-field" value={form.location||''} onChange={e=>setForm({...form,location:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">الغرض</label><input className="input-field" value={form.purpose||''} onChange={e=>setForm({...form,purpose:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">النتائج</label><textarea className="input-field" rows={3} value={form.findings||''} onChange={e=>setForm({...form,findings:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">التوصيات</label><textarea className="input-field" rows={2} value={form.recommendations||''} onChange={e=>setForm({...form,recommendations:e.target.value})} /></div>
          <div className="flex gap-3 justify-end">
            <button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button>
            <button type="submit" className="btn-primary">{form.id?'تحديث':'إنشاء'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
