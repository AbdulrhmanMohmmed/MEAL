import { useState, useEffect } from 'react';
import api from '../services/api';
import StatusBadge from '../components/StatusBadge';
import Modal from '../components/Modal';
import { Plus, ClipboardList, FileText } from 'lucide-react';

export default function DataCollection() {
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedForm, setSelectedForm] = useState(null);

  const load = () => { api.get('/data-collection/forms').then(r => { setForms(r.data); setLoading(false); }).catch(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const viewForm = async (f) => {
    const res = await api.get(`/data-collection/forms/${f.id}`);
    setSelectedForm(res.data);
    setShowModal(true);
  };

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">جمع البيانات الميدانية</h1>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {forms.map(f => (
          <div key={f.id} className="card cursor-pointer hover:shadow-md transition-shadow" onClick={() => viewForm(f)}>
            <div className="flex items-start gap-3">
              <div className="p-2 bg-blue-100 rounded-lg"><ClipboardList className="w-5 h-5 text-blue-600" /></div>
              <div className="flex-1">
                <h4 className="font-bold">{f.title}</h4>
                <p className="text-sm text-gray-500 mt-1">{f.description}</p>
                <div className="flex items-center gap-3 mt-3 text-xs text-gray-400">
                  <span>{f.fields_count} حقل</span>
                  <span>{f.submissions_count} إجابة</span>
                  <StatusBadge status={f.status} />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={selectedForm?.title || ''} size="lg">
        {selectedForm && (
          <div className="space-y-4">
            <p className="text-gray-600">{selectedForm.description}</p>
            <h4 className="font-bold">الحقول ({selectedForm.fields?.length || 0})</h4>
            <div className="space-y-2">
              {selectedForm.fields?.map((field, i) => (
                <div key={i} className="bg-gray-50 p-3 rounded-lg">
                  <div className="flex justify-between"><span className="font-medium">{field.label}</span><span className="text-xs badge bg-blue-100 text-blue-700">{field.type}</span></div>
                  {field.options && <div className="mt-1 text-xs text-gray-500">الخيارات: {field.options.join(', ')}</div>}
                </div>
              ))}
            </div>
            <h4 className="font-bold mt-4">الإجابات ({selectedForm.submissions?.length || 0})</h4>
            {selectedForm.submissions?.map((s, i) => (
              <div key={i} className="bg-gray-50 p-3 rounded-lg text-sm">
                <div className="flex justify-between mb-2"><span>بواسطة: {s.submitted_by}</span><span className="text-gray-400">{s.submitted_at?.split('T')[0]}</span></div>
                <pre className="text-xs bg-white p-2 rounded overflow-x-auto">{JSON.stringify(s.data, null, 2)}</pre>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  );
}
