import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

const NAV_ITEMS = [
  { path: '/', icon: 'dashboard', label: 'Dashboard' },
  { path: '/log', icon: 'restaurant_menu', label: 'Meal Logger' },
  { path: '/supplements', icon: 'medication', label: 'Supplements' },
  { path: '/analytics', icon: 'analytics', label: 'Analytics' },
  { path: '/premium', icon: 'workspace_premium', label: 'Premium' },
];

function SidebarItem({ icon, label, path, isExpanded, onNavigate }) {
  const handleClick = () => {
    if (onNavigate) onNavigate();
  };

  return (
    <NavLink
      to={path}
      onClick={handleClick}
      className={({ isActive }) =>
        `sidebar-link flex items-center h-12 px-3 mx-3 my-1 rounded-xl transition-all duration-200 overflow-hidden ${isActive ? 'active' : ''}`
      }
    >
      <div className="flex items-center justify-center w-6 h-6 shrink-0">
        <span className="material-icons-outlined text-xl">{icon}</span>
      </div>

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

export default function Sidebar({ 
  isExpanded, 
  setIsExpanded,
  isMobileMenuOpen,
  setIsMobileMenuOpen,
  isMobile
}) {
  const { user } = useAuth();

  const handleNavigate = () => {
    if (isMobile) {
      setIsMobileMenuOpen(false);
    }
  };

  // Mobile backdrop
  const Backdrop = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 z-[74] md:hidden"
      onClick={() => setIsMobileMenuOpen(false)}
    />
  );

  // Mobile sidebar content
  const MobileSidebar = () => (
    <motion.div
      initial={{ x: '-100%' }}
      animate={{ x: 0 }}
      exit={{ x: '-100%' }}
      transition={{ type: 'spring', damping: 25, stiffness: 200 }}
      className="fixed top-0 left-0 w-72 h-full bg-[var(--surface-container-low)] border-r border-[var(--outline-variant)] z-[75] flex flex-col md:hidden"
    >
      {/* Logo */}
      <div className="flex items-center h-20 px-4 mt-2 mb-2 overflow-hidden">
        <div className="flex items-center justify-center w-7 h-7 shrink-0 text-[var(--primary)]">
          <span className="material-icons-outlined text-2xl" style={{ filter: 'drop-shadow(0 0 8px var(--primary))' }}>
            fitness_center
          </span>
        </div>
        <div className="overflow-hidden whitespace-nowrap flex flex-col justify-center ml-3">
          <h1
            className="text-base font-bold tracking-wider font-['Plus_Jakarta_Sans'] whitespace-nowrap"
            style={{
              background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            MACROMETRICS
          </h1>
          <span className="text-[9px] text-[var(--on-surface-variant)] uppercase tracking-[0.2em] font-mono whitespace-nowrap">
            Performance Lab
          </span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto py-2">
        {NAV_ITEMS.map((item) => (
          <SidebarItem 
            key={item.path} 
            {...item} 
            isExpanded={true} 
            onNavigate={handleNavigate}
          />
        ))}
      </nav>

      {/* Bottom */}
      <div className="sidebar-bottom pb-6 pt-3 border-t border-[var(--outline-variant)] flex flex-col gap-1">
        {user && (
          <NavLink
            to="/profile"
            onClick={handleNavigate}
            className={({ isActive }) =>
              `sidebar-link flex items-center h-14 px-3 mx-3 my-1 rounded-xl transition-all duration-200 overflow-hidden ${isActive ? 'active' : ''}`
            }
          >
            <div className="sidebar-user-avatar-wrap flex items-center justify-center w-6 h-6 shrink-0 bg-[var(--surface-container-high)] rounded-full">
              <span className="material-icons-outlined text-sm text-[var(--on-surface-variant)]">person</span>
            </div>
            <div className="flex flex-col justify-center overflow-hidden whitespace-nowrap ml-4">
              <span className="text-sm font-semibold text-[var(--on-surface)]">
                {user.name || 'Athlete'}
              </span>
              <span className="text-[11px] text-[var(--on-surface-variant)] mt-0.5">
                {user.email}
              </span>
            </div>
          </NavLink>
        )}
        <SidebarItem
          icon="settings"
          label="Settings"
          path="/settings"
          isExpanded={true}
          onNavigate={handleNavigate}
        />
      </div>
    </motion.div>
  );

  // Desktop sidebar (current behavior)
  const DesktopSidebar = () => (
    <motion.aside
      className="sidebar hidden md:block"
      initial={false}
      animate={{ width: isExpanded ? 280 : 80 }}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
    >
      {/* Logo */}
      <div className="flex items-center h-20 px-4 mt-2 mb-2 overflow-hidden">
        <div className="flex items-center justify-center w-7 h-7 shrink-0 text-[var(--primary)]">
          <span className="material-icons-outlined text-2xl" style={{ filter: 'drop-shadow(0 0 8px var(--primary))' }}>
            fitness_center
          </span>
        </div>
        <motion.div
          className="overflow-hidden whitespace-nowrap flex flex-col justify-center"
          initial={false}
          animate={{
            width: isExpanded ? '100%' : 0,
            opacity: isExpanded ? 1 : 0,
            marginLeft: isExpanded ? 12 : 0,
          }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          <h1
            className="text-base font-bold tracking-wider font-['Plus_Jakarta_Sans'] whitespace-nowrap"
            style={{
              background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            MACROMETRICS
          </h1>
          <span className="text-[9px] text-[var(--on-surface-variant)] uppercase tracking-[0.2em] font-mono whitespace-nowrap">
            Performance Lab
          </span>
        </motion.div>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto overflow-x-hidden scrollbar-hide py-2">
        {NAV_ITEMS.map((item) => (
          <SidebarItem key={item.path} {...item} isExpanded={isExpanded} />
        ))}
      </nav>

      {/* Bottom */}
      <div className="sidebar-bottom pb-6 pt-3 border-t border-[var(--outline-variant)] flex flex-col gap-1 overflow-hidden">
        {user && (
          <NavLink
            to="/profile"
            className={({ isActive }) =>
              `sidebar-link flex items-center h-14 px-3 mx-3 my-1 rounded-xl transition-all duration-200 overflow-hidden ${isActive ? 'active' : ''}`
            }
          >
            <div className="sidebar-user-avatar-wrap flex items-center justify-center w-6 h-6 shrink-0 bg-[var(--surface-container-high)] rounded-full">
              <span className="material-icons-outlined text-sm text-[var(--on-surface-variant)]">person</span>
            </div>
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
              <span className="text-sm font-semibold text-[var(--on-surface)] leading-tight">
                {user.name || 'Athlete'}
              </span>
              <span className="text-[11px] text-[var(--on-surface-variant)] mt-0.5">
                {user.email}
              </span>
            </motion.div>
          </NavLink>
        )}
        <SidebarItem
          icon="settings"
          label="Settings"
          path="/settings"
          isExpanded={isExpanded}
        />
      </div>
    </motion.aside>
  );

  return (
    <>
      <AnimatePresence>
        {isMobileMenuOpen && <Backdrop />}
      </AnimatePresence>
      <AnimatePresence>
        {isMobileMenuOpen ? <MobileSidebar key="mobile" /> : <DesktopSidebar key="desktop" />}
      </AnimatePresence>
    </>
  );
}