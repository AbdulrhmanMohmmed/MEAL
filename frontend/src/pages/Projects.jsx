import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import { Plus } from 'lucide-react';

export default function Projects() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => {
    api.get('/projects/').then(r => { setData(r.data.items || []); setLoading(false); }).catch(() => setLoading(false));
  };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/projects/${form.id}`, form);
      else await api.post('/projects/', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert(err.response?.data?.detail || 'خطأ'); }
  };

  const columns = [
    { header: 'الكود', accessor: 'code' },
    { header: 'المشروع', accessor: 'name', render: (r) => <span className="font-medium">{r.name}</span> },
    { header: 'القطاع', accessor: 'sector' },
    { header: 'المحافظة', accessor: 'governorate' },
    { header: 'المانح', accessor: 'donor' },
    { header: 'الميزانية', accessor: 'budget', render: (r) => `$${(r.budget||0).toLocaleString()}` },
    { header: 'الصرف', accessor: 'progress', render: (r) => (
      <div className="flex items-center gap-2">
        <div className="w-16 bg-gray-100 rounded-full h-2"><div className="h-2 bg-blue-500 rounded-full" style={{width:`${r.progress}%`}} /></div>
        <span className="text-xs">{r.progress}%</span>
      </div>
    )},
    { header: 'الحالة', accessor: 'status', render: (r) => <StatusBadge status={r.status} /> },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">إدارة المشاريع</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> مشروع جديد
        </button>
      </div>
      <div className="card">
        {loading ? <div className="text-center py-8 text-gray-400">جاري التحميل...</div> :
          <DataTable columns={columns} data={data} onRowClick={(r) => { setForm(r); setShowModal(true); }} />}
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تعديل مشروع' : 'مشروع جديد'} size="lg">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <div><label className="block text-sm font-medium mb-1">اسم المشروع *</label><input className="input-field" value={form.name||''} onChange={e=>setForm({...form,name:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">الكود *</label><input className="input-field" value={form.code||''} onChange={e=>setForm({...form,code:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">القطاع</label>
            <select className="input-field" value={form.sector||''} onChange={e=>setForm({...form,sector:e.target.value})}>
              <option value="">اختر</option>
              {["الصحة","التعليم","الأمن الغذائي","المياه والصرف الصحي","الحماية","المأوى","التغذية"].map(s=><option key={s}>{s}</option>)}
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">المانح</label><input className="input-field" value={form.donor||''} onChange={e=>setForm({...form,donor:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">الميزانية ($)</label><input type="number" className="input-field" value={form.budget||''} onChange={e=>setForm({...form,budget:parseFloat(e.target.value)})} /></div>
          <div><label className="block text-sm font-medium mb-1">المحافظة</label><input className="input-field" value={form.governorate||''} onChange={e=>setForm({...form,governorate:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">تاريخ البدء</label><input type="date" className="input-field" value={form.start_date||''} onChange={e=>setForm({...form,start_date:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">تاريخ الانتهاء</label><input type="date" className="input-field" value={form.end_date||''} onChange={e=>setForm({...form,end_date:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">المستفيدين المستهدفين</label><input type="number" className="input-field" value={form.target_beneficiaries||''} onChange={e=>setForm({...form,target_beneficiaries:parseInt(e.target.value)})} /></div>
          <div><label className="block text-sm font-medium mb-1">الحالة</label>
            <select className="input-field" value={form.status||'active'} onChange={e=>setForm({...form,status:e.target.value})}>
              <option value="planned">مخطط</option><option value="active">نشط</option><option value="completed">مكتمل</option><option value="suspended">معلق</option>
            </select>
          </div>
          <div className="col-span-2"><label className="block text-sm font-medium mb-1">الوصف</label><textarea className="input-field" rows={3} value={form.description||''} onChange={e=>setForm({...form,description:e.target.value})} /></div>
          <div className="col-span-2 flex gap-3 justify-end">
            <button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button>
            <button type="submit" className="btn-primary">{form.id?'تحديث':'إنشاء'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
