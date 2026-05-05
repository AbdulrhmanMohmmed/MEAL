import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { DollarSign, TrendingUp, TrendingDown, Percent } from 'lucide-react';

export default function Finance() {
  const [grants, setGrants] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get('/finance/grants'), api.get('/finance/summary')]).then(([g, s]) => {
      setGrants(g.data); setSummary(s.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  const columns = [
    { header: 'المنحة', accessor: 'name', render: r => <span className="font-medium">{r.name}</span> },
    { header: 'المانح', accessor: 'donor' },
    { header: 'المبلغ', accessor: 'amount', render: r => `$${(r.amount||0).toLocaleString()}` },
    { header: 'المصروف', accessor: 'spent', render: r => `$${(r.spent||0).toLocaleString()}` },
    { header: 'نسبة الصرف', accessor: 'utilization', render: r => (
      <div className="flex items-center gap-2">
        <div className="w-16 bg-gray-100 rounded-full h-2"><div className={`h-2 rounded-full ${r.utilization > 80 ? 'bg-emerald-500' : 'bg-blue-500'}`} style={{width:`${r.utilization}%`}} /></div>
        <span className="text-xs">{r.utilization}%</span>
      </div>
    )},
    { header: 'الحالة', accessor: 'status', render: r => <StatusBadge status={r.status} /> },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">الإدارة المالية</h1>
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard title="إجمالي المنح" value={`$${(summary.total_grants/1000).toFixed(0)}K`} icon={DollarSign} color="blue" />
          <StatCard title="المصروف" value={`$${(summary.total_spent/1000).toFixed(0)}K`} icon={TrendingDown} color="amber" />
          <StatCard title="المتبقي" value={`$${((summary.total_grants-summary.total_spent)/1000).toFixed(0)}K`} icon={TrendingUp} color="green" />
          <StatCard title="معدل الصرف" value={`${summary.burn_rate}%`} icon={Percent} color="purple" />
        </div>
      )}
      <div className="card">
        <h3 className="font-bold mb-4">الميزانية والصرف حسب المنحة</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={grants.map(g=>({name:g.name.substring(0,20),amount:g.amount,spent:g.spent}))}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" tick={{fontSize:10}} /><YAxis tick={{fontSize:11}} />
            <Tooltip formatter={v=>`$${v.toLocaleString()}`} />
            <Bar dataKey="amount" fill="#93c5fd" name="المبلغ" radius={[4,4,0,0]} />
            <Bar dataKey="spent" fill="#3b82f6" name="المصروف" radius={[4,4,0,0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="card"><h3 className="font-bold mb-4">المنح</h3><DataTable columns={columns} data={grants} /></div>
    </div>
  );
}
