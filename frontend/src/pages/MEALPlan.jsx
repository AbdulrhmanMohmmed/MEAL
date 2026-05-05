import { useState, useEffect } from 'react';
import api from '../services/api';
import StatusBadge from '../components/StatusBadge';
import Modal from '../components/Modal';
import { Plus, BookOpen } from 'lucide-react';

export default function MEALPlan() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => { api.get('/meal-plan/').then(r => { setPlans(r.data); setLoading(false); }).catch(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/meal-plan/${form.id}`, form);
      else await api.post('/meal-plan/', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert('خطأ'); }
  };

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">خطة MEAL</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> خطة جديدة</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {plans.map(p => (
          <div key={p.id} className="card cursor-pointer hover:shadow-md" onClick={() => { setForm(p); setShowModal(true); }}>
            <div className="flex items-start gap-3">
              <div className="p-2 bg-blue-100 rounded-lg"><BookOpen className="w-5 h-5 text-blue-600" /></div>
              <div className="flex-1">
                <h4 className="font-bold">{p.title}</h4>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{p.description}</p>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  {p.monitoring_approach && <span className="badge bg-blue-100 text-blue-700">المتابعة: {p.monitoring_approach.substring(0,30)}</span>}
                  {p.evaluation_approach && <span className="badge bg-emerald-100 text-emerald-700">التقييم: {p.evaluation_approach.substring(0,30)}</span>}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تعديل خطة MEAL' : 'خطة MEAL جديدة'} size="lg">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">العنوان *</label><input className="input-field" value={form.title||''} onChange={e=>setForm({...form,title:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">الوصف</label><textarea className="input-field" rows={2} value={form.description||''} onChange={e=>setForm({...form,description:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">نهج المتابعة</label><textarea className="input-field" rows={2} value={form.monitoring_approach||''} onChange={e=>setForm({...form,monitoring_approach:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">نهج التقييم</label><textarea className="input-field" rows={2} value={form.evaluation_approach||''} onChange={e=>setForm({...form,evaluation_approach:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">نهج المساءلة</label><textarea className="input-field" rows={2} value={form.accountability_approach||''} onChange={e=>setForm({...form,accountability_approach:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">نهج التعلم</label><textarea className="input-field" rows={2} value={form.learning_approach||''} onChange={e=>setForm({...form,learning_approach:e.target.value})} /></div>
          <div className="flex gap-3 justify-end"><button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button><button type="submit" className="btn-primary">{form.id?'تحديث':'إنشاء'}</button></div>
        </form>
      </Modal>
    </div>
  );
}
