import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useTheme } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { updateUser } from '../api';
import { useToast } from '../components/ToastProvider';

export default function Settings() {
  const { theme, toggleTheme } = useTheme();
  const { user, updateUser: updateAuthUser, logout } = useAuth();
  const toast = useToast();
  const [settings, setSettings] = useState({
    notifications: { mealReminders: true, macroAlerts: true, weeklyReport: true, anomalyDetection: true },
    privacy: { shareProgress: false, publicProfile: false },
  });

  function updateSetting(path, value) {
    setSettings(prev => {
      const next = { ...prev };
      const keys = path.split('.');
      if (keys.length === 2) next[keys[0]] = { ...next[keys[0]], [keys[1]]: value };
      else next[keys[0]] = value;
      return next;
    });
  }

  async function handleModeChange() {
    toggleTheme();
    try { await updateUser({ theme_mode: theme === 'dark' ? 'light' : 'dark' }); } catch {}
  }

  async function handleUnitChange(newUnit) {
    try {
      const u = await updateUser({ preferred_unit: newUnit });
      updateAuthUser(u);
      toast.success(`Switched to ${newUnit} units`);
    } catch { toast.error('Failed to update units'); }
  }

  function handleLogout() { logout(); toast.success('Signed out'); }

  const currentUnit = user?.preferred_unit || 'metric';

  return (
    <motion.div className="settings-page" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Settings</h2>
            <p>Customize your MacroMetrics experience</p>
          </div>
        </div>
      </div>

      {/* ── Theme Mode ── */}
      <div className="settings-section">
        <div className="settings-section__header">
          <span className="material-icons-outlined">dark_mode</span>
          <div>
            <div className="settings-section__title">Display Mode</div>
          </div>
        </div>
        <div className="unit-toggle">
          <button className={`unit-option ${theme === 'dark' ? 'active' : ''}`} onClick={() => theme !== 'dark' && handleModeChange()}>
            <div className="unit-option__label">🌙 Dark</div>
          </button>
          <button className={`unit-option ${theme === 'light' ? 'active' : ''}`} onClick={() => theme !== 'light' && handleModeChange()}>
            <div className="unit-option__label">☀️ Light</div>
          </button>
        </div>
      </div>

      {/* ── Measurement Units ── */}
      <div className="settings-section">
        <div className="settings-section__header">
          <span className="material-icons-outlined">straighten</span>
          <div>
            <div className="settings-section__title">Measurement Units</div>
          </div>
        </div>
        <div className="unit-toggle">
          <button className={`unit-option ${currentUnit === 'metric' ? 'active' : ''}`} onClick={() => currentUnit !== 'metric' && handleUnitChange('metric')}>
            <div className="unit-option__label">📐 Metric</div>
          </button>
          <button className={`unit-option ${currentUnit === 'imperial' ? 'active' : ''}`} onClick={() => currentUnit !== 'imperial' && handleUnitChange('imperial')}>
            <div className="unit-option__label">📏 Imperial</div>
          </button>
        </div>
      </div>

      {/* ── Notifications ── */}
      <div className="settings-section">
        <div className="settings-section__header">
          <span className="material-icons-outlined">notifications</span>
          <div>
            <div className="settings-section__title">Notifications</div>
          </div>
        </div>
        <div className="settings-toggles">
          {[
            { key: 'mealReminders', label: 'Meal Reminders', desc: 'Get reminded to log your meals on schedule' },
            { key: 'macroAlerts', label: 'Macro Alerts', desc: 'Alert when approaching or exceeding targets' },
            { key: 'weeklyReport', label: 'Weekly Report', desc: 'Receive a weekly performance summary' },
            { key: 'anomalyDetection', label: 'Anomaly Detection', desc: 'Get notified about unusual patterns' },
          ].map(item => (
            <div key={item.key} className="settings-toggle-row">
              <div>
                <div className="settings-toggle__label">{item.label}</div>
                <div className="settings-toggle__desc">{item.desc}</div>
              </div>
              <button className={`toggle-switch ${settings.notifications[item.key] ? 'active' : ''}`} onClick={() => updateSetting(`notifications.${item.key}`, !settings.notifications[item.key])}>
                <div className="toggle-switch__thumb" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* ── Account ── */}
      <div className="settings-section">
        <div className="settings-section__header">
          <span className="material-icons-outlined">account_circle</span>
          <div>
            <div className="settings-section__title">Account</div>
          </div>
        </div>
        <div className="data-actions">
          <button className="data-action-btn data-action-btn--danger" onClick={handleLogout}>
            <span className="material-icons-outlined">logout</span>
            Sign Out
          </button>
        </div>
      </div>

      {/* ── About ── */}
      <div className="settings-about">
        <div className="settings-about__logo">MacroMetrics</div>
        <div className="settings-about__meta">v1.1.0 • Performance Lab</div>
      </div>
    </motion.div>
  );
}
