import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';

export default function HR() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get('/hr/employees').then(r => { setEmployees(r.data); setLoading(false); }).catch(() => setLoading(false)); }, []);

  const columns = [
    { header: 'رقم الموظف', accessor: 'employee_id' },
    { header: 'الاسم', accessor: 'full_name', render: r => <span className="font-medium">{r.full_name}</span> },
    { header: 'القسم', accessor: 'department' },
    { header: 'المنصب', accessor: 'position' },
    { header: 'الموقع', accessor: 'location' },
    { header: 'نوع العقد', accessor: 'contract_type', render: r => ({full_time:'دوام كامل',part_time:'دوام جزئي',consultant:'استشاري'}[r.contract_type]||r.contract_type) },
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
  ];

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">الموارد البشرية</h1>
      <div className="card"><DataTable columns={columns} data={employees} /></div>
    </div>
  );
}
