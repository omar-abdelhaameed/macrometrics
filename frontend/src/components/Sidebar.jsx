import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const NAV_ITEMS = [
  { path: '/', icon: 'dashboard', label: 'Dashboard' },
  { path: '/log', icon: 'restaurant_menu', label: 'Meal Logger' },
  { path: '/supplements', icon: 'medication', label: 'Supplements' },
  { path: '/analytics', icon: 'analytics', label: 'Analytics' },
  { path: '/profile', icon: 'person', label: 'Profile' },
];

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h1>MacroMetrics</h1>
        <span>Performance Lab</span>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            <span className="material-icons-outlined">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <NavLink
          to="/settings"
          className={({ isActive }) => isActive ? 'active flex items-center gap-3 px-4 py-3 rounded-xl text-[var(--on-surface-variant)] hover:bg-[var(--surface-container)]' : 'flex items-center gap-3 px-4 py-3 rounded-xl text-[var(--on-surface-variant)] hover:bg-[var(--surface-container)]'}
        >
          <span className="material-icons-outlined">settings</span>
        </NavLink>
        
        {user && (
          <div className="mt-4 pt-4 border-t border-white/5">
            <NavLink
              to="/profile"
              className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-xl transition-colors ${isActive ? 'bg-white/5' : 'hover:bg-white/5'}`}
            >
              <div className="w-10 h-10 rounded-full bg-[var(--surface-container-high)] flex items-center justify-center relative">
                <span className="material-icons-outlined" style={{ fontSize: 20 }}>person</span>
                {user.is_pro_user && (
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-amber-500 rounded-full flex items-center justify-center border-2 border-[var(--surface)] text-[8px] font-black text-white">
                    ★
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5 min-w-0">
                  <div className="text-sm font-bold text-[var(--on-surface)] truncate">{user.name}</div>
                  {user.is_pro_user && (
                    <span className="px-1 py-0.5 rounded-md bg-amber-500/10 text-amber-500 text-[8px] font-black uppercase tracking-tighter border border-amber-500/20">
                      PRO
                    </span>
                  )}
                </div>
                <div className="text-[10px] text-[var(--on-surface-variant)] truncate opacity-60 font-medium">{user.email}</div>
              </div>
            </NavLink>
            
            {!user.is_pro_user && (
              <button 
                className="mt-3 w-full group py-2.5 px-4 rounded-xl relative overflow-hidden transition-all hover:scale-[1.02] active:scale-[0.98]"
                style={{ background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' }}
              >
                <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div className="flex items-center justify-center gap-2">
                  <span className="material-icons-outlined text-white text-sm">stars</span>
                  <span className="text-[11px] font-black text-white uppercase tracking-wider">UPGRADE TO PRO</span>
                </div>
              </button>
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
