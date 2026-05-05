import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import { Banknote, CheckCircle, Clock, Users } from 'lucide-react';

export default function Cash() {
  const [transfers, setTransfers] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get('/cash/transfers'), api.get('/cash/summary')]).then(([t, s]) => {
      setTransfers(t.data); setSummary(s.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  const methodLabels = { hawala:'حوالة', mobile_money:'محفظة إلكترونية', cash_in_hand:'نقدي', bank:'بنك', voucher:'قسيمة' };
  const columns = [
    { header: 'الرقم المرجعي', accessor: 'reference_number' },
    { header: 'المبلغ', accessor: 'amount', render: r => `$${r.amount}` },
    { header: 'الطريقة', accessor: 'method', render: r => methodLabels[r.method] || r.method },
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
    { header: 'التاريخ', accessor: 'transfer_date' },
    { header: 'التحقق', accessor: 'verified', render: r => r.verified ? <span className="text-emerald-600 font-bold">محقق</span> : <span className="text-amber-600">معلق</span> },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">التحويلات النقدية والقسائم (CVA)</h1>
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard title="إجمالي التحويلات" value={`$${(summary.total_amount||0).toLocaleString()}`} icon={Banknote} color="blue" />
          <StatCard title="تم الصرف" value={`$${(summary.disbursed||0).toLocaleString()}`} icon={CheckCircle} color="green" />
          <StatCard title="معلق" value={`$${(summary.pending||0).toLocaleString()}`} icon={Clock} color="amber" />
          <StatCard title="عدد التحويلات" value={summary.total_transfers} icon={Users} color="purple" />
        </div>
      )}
      <div className="card"><DataTable columns={columns} data={transfers} /></div>
    </div>
  );
}
