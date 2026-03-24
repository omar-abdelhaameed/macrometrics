import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

const NAV_ITEMS = [
  { path: '/', icon: 'dashboard', label: 'Dashboard' },
  { path: '/log', icon: 'restaurant_menu', label: 'Meal Logger' },
  { path: '/supplements', icon: 'medication', label: 'Supplements' },
  { path: '/analytics', icon: 'analytics', label: 'Analytics' },
];

// 1. مكون ثابت عشان يضمن إن كل زراير الصفحات مرصوصة مسطرة واحدة
function SidebarItem({ icon, label, path, isExpanded }) {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        `flex items-center h-12 px-3 mx-3 my-1 rounded-xl transition-all duration-200 group overflow-hidden ${
          isActive
            ? 'bg-[#10141C] border border-white/10 shadow-[0_0_15px_rgba(0,240,255,0.05)] text-white'
            : 'text-gray-400 hover:bg-white/5 hover:text-white'
        }`
      }
    >
      {/* الأيقونة: مساحة ثابتة عشان تفضل في النص دايماً */}
      <div className="flex items-center justify-center w-6 h-6 shrink-0">
        <span className="material-icons-outlined text-xl">{icon}</span>
      </div>

      {/* النص: بيظهر ويختفي بنعومة */}
      <motion.div
        className="flex items-center overflow-hidden whitespace-nowrap"
        initial={false}
        animate={{
          width: isExpanded ? '100%' : 0,
          opacity: isExpanded ? 1 : 0,
          marginLeft: isExpanded ? 16 : 0,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
      >
        <span className="font-medium text-sm tracking-wide">{label}</span>
      </motion.div>
    </NavLink>
  );
}

export default function Sidebar({ isExpanded, setIsExpanded }) {
  const { user } = useAuth();

  return (
    <motion.aside
      className="fixed left-0 top-0 z-50 flex flex-col h-screen bg-[#0A0A0A]/95 backdrop-blur-2xl border-r border-white/10"
      initial={false}
      animate={{ width: isExpanded ? 280 : 80 }}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
    >
      {/* --- اللوجو --- */}
      <div className="flex items-center h-20 px-3 mx-3 mt-4 mb-2 overflow-hidden">
        <div className="flex items-center justify-center w-6 h-6 shrink-0 text-cyan-400">
          <span className="material-icons-outlined text-2xl drop-shadow-[0_0_8px_rgba(0,240,255,0.8)]">
            fitness_center
          </span>
        </div>
        <motion.div
          className="overflow-hidden whitespace-nowrap flex flex-col justify-center"
          initial={false}
          animate={{
            width: isExpanded ? '100%' : 0,
            opacity: isExpanded ? 1 : 0,
            marginLeft: isExpanded ? 16 : 0,
          }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          <h1 className="text-lg font-bold text-white tracking-wider font-['Plus_Jakarta_Sans']">
            MACROMETRICS
          </h1>
          <span className="text-[10px] text-cyan-400 uppercase tracking-widest font-mono">
            Performance Lab
          </span>
        </motion.div>
      </div>

      {/* --- زراير الصفحات --- */}
      <nav className="flex-1 overflow-y-auto overflow-x-hidden scrollbar-hide py-2">
        {NAV_ITEMS.map((item) => (
          <SidebarItem key={item.path} {...item} isExpanded={isExpanded} />
        ))}
      </nav>

      {/* --- الجزء السفلي (البروفايل، الإعدادات، البريميوم) --- */}
      <div className="pb-6 pt-3 border-t border-white/10 flex flex-col gap-1 overflow-hidden">
        
        {/* 1. زرار البريميوم (أيقونة فقط في القفل، وواخد خلفية في الفتح) */}
        {user?.is_pro_user && (
          <div
            className={`flex items-center px-3 mx-3 my-1 h-12 rounded-xl transition-all duration-300 overflow-hidden ${
              isExpanded
                ? 'bg-gradient-to-r from-amber-500/10 to-transparent border border-amber-500/20'
                : 'bg-transparent border border-transparent'
            }`}
          >
            <div className="flex items-center justify-center w-6 h-6 shrink-0">
              <span className="material-icons-outlined text-xl text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.8)]">
                workspace_premium
              </span>
            </div>
            <motion.div
              className="overflow-hidden whitespace-nowrap flex items-center"
              initial={false}
              animate={{
                width: isExpanded ? '100%' : 0,
                opacity: isExpanded ? 1 : 0,
                marginLeft: isExpanded ? 16 : 0,
              }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              <span className="text-amber-400 font-bold text-sm tracking-widest uppercase">
                Premium Elite
              </span>
            </motion.div>
          </div>
        )}

        {/* 2. زرار البروفايل */}
        {user && (
          <NavLink
            to="/profile"
            className={({ isActive }) =>
              `flex items-center h-14 px-3 mx-3 my-1 rounded-xl transition-all duration-200 group overflow-hidden ${
                isActive
                  ? 'bg-[#10141C] border border-white/10 text-white'
                  : 'text-gray-400 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            {/* أيقونة البروفايل (نفس المحاذاة للكل) */}
            <div className="flex items-center justify-center w-6 h-6 shrink-0 bg-white/10 rounded-full text-white">
              <span className="material-icons-outlined text-sm">person</span>
            </div>

            {/* بيانات البروفايل (بتختفي تماماً في القفل) */}
            <motion.div
              className="flex flex-col justify-center overflow-hidden whitespace-nowrap"
              initial={false}
              animate={{
                width: isExpanded ? '100%' : 0,
                opacity: isExpanded ? 1 : 0,
                marginLeft: isExpanded ? 16 : 0,
              }}
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              <span className="text-sm font-semibold text-white leading-tight">
                {user.name || 'Athlete'}
              </span>
              <span className="text-[11px] text-gray-500 mt-0.5">
                {user.email}
              </span>
            </motion.div>
          </NavLink>
        )}

        {/* 3. زرار الإعدادات (تحت البروفايل علطول وبنفس التصميم) */}
        <SidebarItem
          icon="settings"
          label="Settings"
          path="/settings"
          isExpanded={isExpanded}
        />
      </div>
    </motion.aside>
  );
}