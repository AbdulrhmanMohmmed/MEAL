const statusConfig = {
  active: { label: 'نشط', class: 'bg-emerald-100 text-emerald-700' },
  completed: { label: 'مكتمل', class: 'bg-blue-100 text-blue-700' },
  planned: { label: 'مخطط', class: 'bg-gray-100 text-gray-700' },
  suspended: { label: 'معلق', class: 'bg-amber-100 text-amber-700' },
  cancelled: { label: 'ملغي', class: 'bg-red-100 text-red-700' },
  in_progress: { label: 'قيد التنفيذ', class: 'bg-blue-100 text-blue-700' },
  pending: { label: 'معلق', class: 'bg-amber-100 text-amber-700' },
  approved: { label: 'موافق', class: 'bg-emerald-100 text-emerald-700' },
  rejected: { label: 'مرفوض', class: 'bg-red-100 text-red-700' },
  received: { label: 'مستلم', class: 'bg-blue-100 text-blue-700' },
  under_review: { label: 'قيد المراجعة', class: 'bg-amber-100 text-amber-700' },
  resolved: { label: 'محلول', class: 'bg-emerald-100 text-emerald-700' },
  closed: { label: 'مغلق', class: 'bg-gray-100 text-gray-700' },
  escalated: { label: 'مصعّد', class: 'bg-red-100 text-red-700' },
  disbursed: { label: 'صرف', class: 'bg-emerald-100 text-emerald-700' },
  draft: { label: 'مسودة', class: 'bg-gray-100 text-gray-700' },
  published: { label: 'منشور', class: 'bg-emerald-100 text-emerald-700' },
  open: { label: 'مفتوح', class: 'bg-amber-100 text-amber-700' },
  mitigated: { label: 'مخفف', class: 'bg-blue-100 text-blue-700' },
  on_track: { label: 'على المسار', class: 'bg-emerald-100 text-emerald-700' },
  at_risk: { label: 'في خطر', class: 'bg-amber-100 text-amber-700' },
  off_track: { label: 'خارج المسار', class: 'bg-red-100 text-red-700' },
  low: { label: 'منخفض', class: 'bg-emerald-100 text-emerald-700' },
  medium: { label: 'متوسط', class: 'bg-amber-100 text-amber-700' },
  high: { label: 'مرتفع', class: 'bg-orange-100 text-orange-700' },
  critical: { label: 'حرج', class: 'bg-red-100 text-red-700' },
};

export default function StatusBadge({ status }) {
  const config = statusConfig[status] || { label: status, class: 'bg-gray-100 text-gray-700' };
  return <span className={`badge ${config.class}`}>{config.label}</span>;
}
