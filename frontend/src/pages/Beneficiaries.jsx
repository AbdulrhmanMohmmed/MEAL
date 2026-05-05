import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import StatusBadge from '../components/StatusBadge';
import { Plus, Download, Upload } from 'lucide-react';

const GOVERNORATES = ["صنعاء", "عدن", "تعز", "الحديدة", "إب", "مأرب", "حضرموت", "ذمار", "عمران", "صعدة", "لحج", "أبين"];

export default function Beneficiaries() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({});
  const [filter, setFilter] = useState({ governorate: '', status: '' });

  const load = () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filter.governorate) params.append('governorate', filter.governorate);
    if (filter.status) params.append('status', filter.status);
    api.get(`/beneficiaries/?${params}`).then(r => { setData(r.data.items || []); setLoading(false); }).catch(() => setLoading(false));
  };

  useEffect(() => { load(); }, [filter]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (form.id) {
        await api.put(`/beneficiaries/${form.id}`, form);
      } else {
        await api.post('/beneficiaries/', form);
      }
      setShowModal(false);
      setForm({});
      load();
    } catch (err) {
      alert(err.response?.data?.detail || 'حدث خطأ');
    }
  };

  const columns = [
    { header: 'الرقم الوطني', accessor: 'national_id' },
    { header: 'الاسم', accessor: 'full_name', render: (row) => <span className="font-medium">{row.full_name}</span> },
    { header: 'الجنس', accessor: 'gender', render: (row) => row.gender === 'male' ? 'ذكر' : 'أنثى' },
    { header: 'المحافظة', accessor: 'governorate' },
    { header: 'حجم الأسرة', accessor: 'household_size' },
    { header: 'درجة الضعف', accessor: 'vulnerability_score', render: (row) => (
      <span className={`font-bold ${row.vulnerability_score >= 7 ? 'text-red-600' : row.vulnerability_score >= 4 ? 'text-amber-600' : 'text-emerald-600'}`}>
        {row.vulnerability_score}
      </span>
    )},
    { header: 'الحالة', accessor: 'status', render: (row) => <StatusBadge status={row.status} /> },
    { header: 'نازح', accessor: 'is_idp', render: (row) => row.is_idp ? 'نعم' : 'لا' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">إدارة المستفيدين</h1>
        <button onClick={() => { setForm({}); setShowModal(true); }} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> إضافة مستفيد
        </button>
      </div>

      <div className="card flex gap-4 items-center">
        <select value={filter.governorate} onChange={(e) => setFilter({...filter, governorate: e.target.value})} className="input-field w-48">
          <option value="">كل المحافظات</option>
          {GOVERNORATES.map(g => <option key={g} value={g}>{g}</option>)}
        </select>
        <select value={filter.status} onChange={(e) => setFilter({...filter, status: e.target.value})} className="input-field w-48">
          <option value="">كل الحالات</option>
          <option value="active">نشط</option>
          <option value="inactive">غير نشط</option>
          <option value="graduated">متخرج</option>
        </select>
        <span className="text-sm text-gray-500">الإجمالي: {data.length}</span>
      </div>

      <div className="card">
        {loading ? <div className="text-center py-8 text-gray-400">جاري التحميل...</div> : (
          <DataTable columns={columns} data={data} onRowClick={(row) => { setForm(row); setShowModal(true); }} />
        )}
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={form.id ? 'تعديل مستفيد' : 'إضافة مستفيد جديد'} size="lg">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">الاسم الكامل *</label>
            <input className="input-field" value={form.full_name || ''} onChange={e => setForm({...form, full_name: e.target.value})} required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">الرقم الوطني</label>
            <input className="input-field" value={form.national_id || ''} onChange={e => setForm({...form, national_id: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">الجنس</label>
            <select className="input-field" value={form.gender || ''} onChange={e => setForm({...form, gender: e.target.value})}>
              <option value="">اختر</option><option value="male">ذكر</option><option value="female">أنثى</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">المحافظة *</label>
            <select className="input-field" value={form.governorate || ''} onChange={e => setForm({...form, governorate: e.target.value})} required>
              <option value="">اختر</option>
              {GOVERNORATES.map(g => <option key={g} value={g}>{g}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">المديرية</label>
            <input className="input-field" value={form.district || ''} onChange={e => setForm({...form, district: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">الهاتف</label>
            <input className="input-field" value={form.phone || ''} onChange={e => setForm({...form, phone: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">حجم الأسرة</label>
            <input type="number" className="input-field" value={form.household_size || ''} onChange={e => setForm({...form, household_size: parseInt(e.target.value)})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">درجة الضعف (1-10)</label>
            <input type="number" min="1" max="10" step="0.1" className="input-field" value={form.vulnerability_score || ''} onChange={e => setForm({...form, vulnerability_score: parseFloat(e.target.value)})} />
          </div>
          <div className="flex items-center gap-4 col-span-2">
            <label className="flex items-center gap-2"><input type="checkbox" checked={form.is_idp || false} onChange={e => setForm({...form, is_idp: e.target.checked})} /> نازح داخلياً</label>
            <label className="flex items-center gap-2"><input type="checkbox" checked={form.disability || false} onChange={e => setForm({...form, disability: e.target.checked})} /> ذو إعاقة</label>
            <label className="flex items-center gap-2"><input type="checkbox" checked={form.female_headed || false} onChange={e => setForm({...form, female_headed: e.target.checked})} /> أسرة تعيلها امرأة</label>
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium mb-1">ملاحظات</label>
            <textarea className="input-field" rows={2} value={form.notes || ''} onChange={e => setForm({...form, notes: e.target.value})} />
          </div>
          <div className="col-span-2 flex gap-3 justify-end">
            <button type="button" onClick={() => setShowModal(false)} className="btn-secondary">إلغاء</button>
            <button type="submit" className="btn-primary">{form.id ? 'تحديث' : 'إضافة'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
