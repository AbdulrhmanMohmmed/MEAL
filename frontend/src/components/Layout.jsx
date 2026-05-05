import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  LayoutDashboard, Users, FolderKanban, DollarSign, UserCog, Package,
  BarChart3, ClipboardList, FileText, MessageSquareWarning, GraduationCap,
  Target, MapPin, ShieldAlert, BookOpen, Bell, LogOut, Menu, X,
  Banknote, FileSearch, Wifi, WifiOff, ChevronDown
} from 'lucide-react';

const menuGroups = [
  {
    title: 'الرئيسية',
    items: [
      { path: '/', label: 'لوحة المعلومات', icon: LayoutDashboard },
    ]
  },
  {
    title: 'إدارة البرامج',
    items: [
      { path: '/projects', label: 'المشاريع', icon: FolderKanban },
      { path: '/beneficiaries', label: 'المستفيدين', icon: Users },
      { path: '/activities', label: 'الأنشطة', icon: ClipboardList },
    ]
  },
  {
    title: 'MEAL',
    items: [
      { path: '/monitoring', label: 'المتابعة والتقييم', icon: BarChart3 },
      { path: '/indicators', label: 'المؤشرات (IPTT)', icon: Target },
      { path: '/accountability', label: 'المساءلة (CFM)', icon: MessageSquareWarning },
      { path: '/learning', label: 'التعلم', icon: GraduationCap },
      { path: '/meal-plan', label: 'خطة MEAL', icon: BookOpen },
      { path: '/logframe', label: 'الإطار المنطقي', icon: FileSearch },
      { path: '/field-visits', label: 'الزيارات الميدانية', icon: MapPin },
    ]
  },
  {
    title: 'العمليات',
    items: [
      { path: '/finance', label: 'المالية', icon: DollarSign },
      { path: '/cash', label: 'التحويلات النقدية', icon: Banknote },
      { path: '/inventory', label: 'المخازن', icon: Package },
      { path: '/hr', label: 'الموارد البشرية', icon: UserCog },
    ]
  },
  {
    title: 'أدوات',
    items: [
      { path: '/data-collection', label: 'جمع البيانات', icon: ClipboardList },
      { path: '/reports', label: 'التقارير', icon: FileText },
      { path: '/documents', label: 'الوثائق', icon: FileText },
      { path: '/risks', label: 'المخاطر', icon: ShieldAlert },
    ]
  }
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [collapsed, setCollapsed] = useState({});
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const toggleGroup = (title) => {
    setCollapsed(prev => ({ ...prev, [title]: !prev[title] }));
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-0 -mr-64'} transition-all duration-300 bg-slate-900 text-white flex flex-col overflow-hidden flex-shrink-0`}>
        <div className="p-4 border-b border-slate-700">
          <h1 className="text-lg font-bold text-blue-400">MEAL System</h1>
          <p className="text-xs text-slate-400 mt-1">نظام المتابعة والتقييم v2.0</p>
        </div>

        <nav className="flex-1 overflow-y-auto py-2">
          {menuGroups.map((group) => (
            <div key={group.title} className="mb-1">
              <button
                onClick={() => toggleGroup(group.title)}
                className="w-full flex items-center justify-between px-4 py-2 text-xs font-bold text-slate-400 uppercase tracking-wider hover:text-slate-300"
              >
                {group.title}
                <ChevronDown className={`w-3 h-3 transition-transform ${collapsed[group.title] ? 'rotate-180' : ''}`} />
              </button>
              {!collapsed[group.title] && group.items.map((item) => {
                const Icon = item.icon;
                const active = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-3 px-4 py-2.5 mx-2 rounded-lg text-sm transition-colors ${
                      active
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }`}
                  >
                    <Icon className="w-4 h-4 flex-shrink-0" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-700">
          <div className="flex items-center gap-2 mb-3">
            {isOnline ? (
              <><Wifi className="w-4 h-4 text-emerald-400" /><span className="text-xs text-emerald-400">متصل</span></>
            ) : (
              <><WifiOff className="w-4 h-4 text-amber-400" /><span className="text-xs text-amber-400">غير متصل</span></>
            )}
          </div>
          <div className="text-sm text-slate-300 truncate">{user?.full_name}</div>
          <div className="text-xs text-slate-500">{user?.role}</div>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between flex-shrink-0">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-gray-100 rounded-lg">
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <h2 className="text-lg font-bold text-gray-800">
              {menuGroups.flatMap(g => g.items).find(i => i.path === location.pathname)?.label || 'MEAL System'}
            </h2>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 hover:bg-gray-100 rounded-lg">
              <Bell className="w-5 h-5 text-gray-600" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <button onClick={logout} className="flex items-center gap-2 text-sm text-gray-600 hover:text-red-600 transition-colors">
              <LogOut className="w-4 h-4" />
              <span>خروج</span>
            </button>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
