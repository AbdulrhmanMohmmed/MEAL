import { useState, useEffect } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import StatCard from '../components/StatCard';
import { Package, AlertTriangle, Warehouse } from 'lucide-react';

export default function Inventory() {
  const [warehouses, setWarehouses] = useState([]);
  const [items, setItems] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get('/inventory/warehouses'), api.get('/inventory/items'), api.get('/inventory/alerts')]).then(([w, i, a]) => {
      setWarehouses(w.data); setItems(i.data); setAlerts(a.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;

  const catLabels = {food:'غذائي',medicine:'طبي',shelter:'مأوى',wash:'مياه',nfi:'غير غذائي',education:'تعليمي',other:'أخرى'};
  const itemColumns = [
    { header: 'المادة', accessor: 'name', render: r => <span className="font-medium">{r.name}</span> },
    { header: 'التصنيف', accessor: 'category', render: r => catLabels[r.category] || r.category },
    { header: 'الكمية', accessor: 'quantity', render: r => <span className={r.is_low_stock ? 'text-red-600 font-bold' : ''}>{r.quantity} {r.unit}</span> },
    { header: 'الحد الأدنى', accessor: 'min_stock' },
    { header: 'الحالة', render: r => r.is_low_stock ? <span className="badge bg-red-100 text-red-700">مخزون منخفض</span> : <span className="badge bg-emerald-100 text-emerald-700">جيد</span> },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">المخازن وسلسلة الإمداد</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard title="المستودعات" value={warehouses.length} icon={Warehouse} color="blue" />
        <StatCard title="إجمالي المواد" value={items.length} icon={Package} color="green" />
        <StatCard title="تنبيهات مخزون" value={alerts.length} icon={AlertTriangle} color="red" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {warehouses.map(w => (
          <div key={w.id} className="card">
            <h4 className="font-bold">{w.name}</h4>
            <p className="text-sm text-gray-500">{w.governorate} - {w.location}</p>
            <div className="mt-3 flex gap-4 text-sm">
              <span>المواد: <strong>{w.items_count}</strong></span>
              {w.low_stock_alerts > 0 && <span className="text-red-600">تنبيهات: <strong>{w.low_stock_alerts}</strong></span>}
            </div>
          </div>
        ))}
      </div>

      <div className="card"><h3 className="font-bold mb-4">قائمة المواد</h3><DataTable columns={itemColumns} data={items} /></div>
    </div>
  );
}
