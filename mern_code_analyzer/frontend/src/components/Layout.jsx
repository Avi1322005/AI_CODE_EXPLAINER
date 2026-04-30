import React, { useContext } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import { LayoutDashboard, Code2, LogOut, Sparkles, Sun, Moon } from 'lucide-react';

export default function Layout() {
  const { user, logout } = useContext(AuthContext);
  const { isDark, toggleTheme } = useContext(ThemeContext);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard className="w-5 h-5" /> },
    { name: 'AI Analyzer', path: '/analyze', icon: <Code2 className="w-5 h-5" /> },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black transition-colors duration-300 flex">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-gray-200 dark:border-white/5 flex flex-col relative z-20">
        <div className="p-6 flex items-center gap-3">
          <div className="relative">
            <div className="absolute inset-0 bg-lightPrimary-500 dark:bg-primary-500 rounded-xl blur shadow-glow shadow-lightPrimary-500/50 dark:shadow-primary-500/50" />
            <div className="relative bg-white dark:bg-dark-900 border border-gray-200 dark:border-white/10 p-2 rounded-xl">
              <Sparkles className="w-5 h-5 text-lightPrimary-600 dark:text-primary-400" />
            </div>
          </div>
          <span className="font-display font-bold text-black dark:text-white text-lg">AI Code</span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link 
                key={item.path} 
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${isActive ? 'bg-lightPrimary-500/10 dark:bg-primary-600/10 text-lightPrimary-600 dark:text-primary-400 border border-lightPrimary-500/20 dark:border-primary-500/20' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 hover:text-black dark:hover:text-gray-200 border border-transparent'}`}
              >
                {item.icon}
                <span className="font-medium text-sm">{item.name}</span>
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-gray-200 dark:border-white/5 mt-auto space-y-4">
          <button 
            onClick={toggleTheme} 
            className="w-full flex items-center justify-between px-4 py-2.5 rounded-xl border border-gray-200 dark:border-white/5 bg-gray-50 dark:bg-dark-900/50 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
          >
            <span className="text-sm font-medium">Theme</span>
            {isDark ? <Sun className="w-4 h-4 text-yellow-500" /> : <Moon className="w-4 h-4 text-gray-600" />}
          </button>

          <div className="flex items-center justify-between bg-gray-100 dark:bg-dark-900/50 rounded-xl p-3 border border-gray-200 dark:border-white/5">
            <div className="overflow-hidden">
              <p className="text-sm font-medium text-black dark:text-white truncate">{user?.name}</p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
            <button onClick={handleLogout} className="text-gray-500 dark:text-gray-400 hover:text-red-500 dark:hover:text-red-400 transition-colors p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-white/5">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative h-screen overflow-hidden">
        {/* Background Orbs (Dark Mode Only or Very Soft in Light) */}
        <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-gray-200/50 dark:bg-primary-600/10 blur-[120px] pointer-events-none z-0 transition-colors" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[30%] h-[40%] rounded-full bg-gray-200/50 dark:bg-purple-600/10 blur-[120px] pointer-events-none z-0 transition-colors" />
        
        <div className="relative z-10 w-full h-full p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
