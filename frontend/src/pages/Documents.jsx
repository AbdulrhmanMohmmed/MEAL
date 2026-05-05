import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { FileText, Download } from 'lucide-react';

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get('/documents/').then(r => { setDocs(r.data); setLoading(false); }).catch(() => setLoading(false)); }, []);

  const catLabels = {report:'تقرير',proposal:'مقترح',policy:'سياسة',guideline:'دليل',template:'قالب',photo:'صورة',other:'أخرى'};
  const columns = [
    { header: 'الوثيقة', accessor: 'title', render: r => <div className="flex items-center gap-2"><FileText className="w-4 h-4 text-blue-600" /><span className="font-medium">{r.title}</span></div> },
    { header: 'التصنيف', accessor: 'category', render: r => catLabels[r.category] || r.category },
    { header: 'الوصف', accessor: 'description' },
    { header: 'التاريخ', accessor: 'created_at', render: r => r.created_at?.split('T')[0] || '' },
  ];

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">إدارة الوثائق</h1>
      <div className="card"><DataTable columns={columns} data={docs} /></div>
    </div>
  );
}
