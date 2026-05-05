import { useState, useEffect } from 'react';
import api from '../services/api';
import Modal from '../components/Modal';
import { Plus, Network } from 'lucide-react';

const levelLabels = { goal: 'الهدف العام', purpose: 'الغرض', output: 'المخرج', activity: 'النشاط' };
const levelColors = { goal: 'bg-blue-100 border-blue-300', purpose: 'bg-emerald-100 border-emerald-300', output: 'bg-amber-100 border-amber-300', activity: 'bg-gray-100 border-gray-300' };

export default function LogFrame() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});

  const load = () => { api.get('/logframe/').then(r => { setItems(r.data); setLoading(false); }).catch(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) await api.put(`/logframe/${form.id}`, form);
      else await api.post('/logframe/', form);
      setShowModal(false); setForm({}); load();
    } catch (err) { alert('خطأ'); }
  };

  const grouped = {};
  items.forEach(i => { if (!grouped[i.level]) grouped[i.level] = []; grouped[i.level].push(i); });

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">الإطار المنطقي (Log Frame)</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2"><Plus className="w-4 h-4" /> إضافة</button>
      </div>
      {['goal', 'purpose', 'output', 'activity'].map(level => (
        <div key={level}>
          <h3 className="font-bold text-gray-700 mb-3 flex items-center gap-2"><Network className="w-4 h-4" /> {levelLabels[level]}</h3>
          <div className="space-y-2">
            {(grouped[level] || []).map(item => (
              <div key={item.id} className={`p-4 rounded-lg border ${levelColors[level]} cursor-pointer hover:shadow-sm`} onClick={() => { setForm(item); setShowModal(true); }}>
                <div className="flex items-center gap-2"><span className="font-bold text-gray-700">{item.code}</span><span>{item.description}</span></div>
                {item.indicators && <p className="text-xs text-gray-500 mt-1"><strong>المؤشرات:</strong> {item.indicators}</p>}
                {item.means_of_verification && <p className="text-xs text-gray-500"><strong>وسائل التحقق:</strong> {item.means_of_verification}</p>}
                {item.assumptions && <p className="text-xs text-gray-500"><strong>الافتراضات:</strong> {item.assumptions}</p>}
              </div>
            ))}
          </div>
        </div>
      ))}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تعديل' : 'إضافة عنصر'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">المستوى</label>
            <select className="input-field" value={form.level||'output'} onChange={e=>setForm({...form,level:e.target.value})}>
              {Object.entries(levelLabels).map(([k,v])=><option key={k} value={k}>{v}</option>)}
            </select>
          </div>
          <div><label className="block text-sm font-medium mb-1">الكود</label><input className="input-field" value={form.code||''} onChange={e=>setForm({...form,code:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">الوصف *</label><textarea className="input-field" rows={2} value={form.description||''} onChange={e=>setForm({...form,description:e.target.value})} required /></div>
          <div><label className="block text-sm font-medium mb-1">المؤشرات</label><input className="input-field" value={form.indicators||''} onChange={e=>setForm({...form,indicators:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">وسائل التحقق</label><input className="input-field" value={form.means_of_verification||''} onChange={e=>setForm({...form,means_of_verification:e.target.value})} /></div>
          <div><label className="block text-sm font-medium mb-1">الافتراضات</label><input className="input-field" value={form.assumptions||''} onChange={e=>setForm({...form,assumptions:e.target.value})} /></div>
          <div className="flex gap-3 justify-end"><button type="button" onClick={()=>setShowModal(false)} className="btn-secondary">إلغاء</button><button type="submit" className="btn-primary">{form.id?'تحديث':'إنشاء'}</button></div>
        </form>
      </Modal>
    </div>
  );
}
