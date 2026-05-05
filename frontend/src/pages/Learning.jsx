import { useState, useEffect } from 'react';
import api from '../services/api';
import Modal from '../components/Modal';
import { Plus, BookOpen, Lightbulb } from 'lucide-react';

export default function Learning() {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => { api.get('/learning/lessons').then(r => { setLessons(r.data); setLoading(false); }).catch(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/learning/lessons/${form.id}`, form);
      else await api.post('/learning/lessons', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert('خطأ'); }
  };

  const catLabels = { program:'البرامج', operations:'العمليات', coordination:'التنسيق', monitoring:'المتابعة', finance:'المالية' };

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">التعلم - الدروس المستفادة</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> درس جديد</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {lessons.map(l => (
          <div key={l.id} className="card cursor-pointer hover:shadow-md transition-shadow" onClick={() => { setForm(l); setShowModal(true); }}>
            <div className="flex items-start gap-3">
              <div className="p-2 bg-amber-100 rounded-lg"><Lightbulb className="w-5 h-5 text-amber-600" /></div>
              <div className="flex-1">
                <h4 className="font-bold text-gray-800">{l.title}</h4>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{l.description}</p>
                <div className="flex items-center gap-2 mt-3">
                  <span className="badge bg-blue-100 text-blue-700">{catLabels[l.category] || l.category}</span>
                  <span className="text-xs text-gray-400">{l.date}</span>
                </div>
                {l.recommendations && <p className="text-xs text-gray-600 mt-2 bg-gray-50 p-2 rounded"><strong>التوصيات:</strong> {l.recommendations}</p>}
              </div>
            </div>
          </div>
        ))}
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تعديل الدرس' : 'درس مستفاد جديد'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">العنوان *</label><input className="input-field" value={form.title||''} onChange={e => setForm({...form, title: e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">الوصف *</label><textarea className="input-field" rows={3} value={form.description||''} onChange={e => setForm({...form, description: e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">التصنيف</label>
            <select className="input-field" value={form.category||''} onChange={e => setForm({...form, category: e.target.value})}>
              <option value="">اختر</option>{Object.entries(catLabels).map(([k,v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">التوصيات</label><textarea className="input-field" rows={2} value={form.recommendations||''} onChange={e => setForm({...form, recommendations: e.target.value})} /></div>
          <div className="flex gap-3 justify-end">
            <button type="button" onClick={() => setShowModal(false)} className="btn-secondary">إلغاء</button>
            <button type="submit" className="btn-primary">{form.id ? 'تحديث' : 'إضافة'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
