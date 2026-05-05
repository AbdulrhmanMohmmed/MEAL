import { useState, useEffect } from 'react';
import api from '../services/api';
import StatusBadge from '../components/StatusBadge';

export default function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/dashboard/recent-activities').then(r => { setActivities(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-8 text-gray-400">جاري التحميل...</div>;
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">الأنشطة</h1>
      <div className="card">
        <div className="space-y-3">
          {activities.length === 0 ? <p className="text-center text-gray-400 py-8">لا توجد أنشطة</p> : activities.map((a, i) => (
            <div key={i} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0" />
              <div className="flex-1">
                <p className="font-medium">{a.description || a.title || a.name}</p>
                <p className="text-xs text-gray-400">{a.date || a.created_at}</p>
              </div>
              {a.type && <span className="badge bg-blue-100 text-blue-700">{a.type}</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
