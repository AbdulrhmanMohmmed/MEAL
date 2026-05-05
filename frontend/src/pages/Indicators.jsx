import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Indicators() {
  const [iptt, setIptt] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/monitoring/iptt').then(r => { setIptt(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  if (!iptt || !iptt.indicators) return <div className="text-center py-8 text-gray-400">لا توجد بيانات</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">جدول تتبع أداء المؤشرات (IPTT)</h1>
      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="text-right py-3 px-3 sticky right-0 bg-white">المؤشر</th>
              <th className="text-right py-3 px-3">النوع</th>
              <th className="text-right py-3 px-3">الوحدة</th>
              <th className="text-right py-3 px-3">خط الأساس</th>
              <th className="text-right py-3 px-3">المستهدف</th>
              {iptt.months?.map(m => <th key={m} className="text-center py-3 px-2 text-xs">{m}</th>)}
              <th className="text-right py-3 px-3">الفعلي</th>
              <th className="text-right py-3 px-3">%</th>
            </tr>
          </thead>
          <tbody>
            {iptt.indicators.map((ind, i) => (
              <tr key={i} className="border-b border-gray-50 hover:bg-gray-50">
                <td className="py-3 px-3 sticky right-0 bg-white font-medium">{ind.name}</td>
                <td className="py-3 px-3 text-xs">{ind.type === 'output' ? 'مخرج' : ind.type === 'outcome' ? 'نتيجة' : 'أثر'}</td>
                <td className="py-3 px-3 text-xs">{ind.unit}</td>
                <td className="py-3 px-3">{ind.baseline}</td>
                <td className="py-3 px-3 font-medium">{ind.target}</td>
                {ind.monthly_values?.map((v, j) => <td key={j} className="text-center py-3 px-2 text-xs">{v || '-'}</td>)}
                <td className="py-3 px-3 font-bold">{ind.current}</td>
                <td className="py-3 px-3">
                  <span className={`font-bold ${ind.progress >= 80 ? 'text-emerald-600' : ind.progress >= 50 ? 'text-amber-600' : 'text-red-600'}`}>{ind.progress}%</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
