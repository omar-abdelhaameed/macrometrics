import React, { useState, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { fetchUser, updateUser } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../components/ToastProvider';

const ACTIVITY_LEVELS = [
  { value: 'sedentary', label: 'Sedentary', desc: 'Little or no exercise', icon: 'weekend' },
  { value: 'light', label: 'Lightly Active', desc: '1–3 days/week', icon: 'directions_walk' },
  { value: 'moderate', label: 'Moderate', desc: '3–5 days/week', icon: 'fitness_center' },
  { value: 'active', label: 'Active', desc: '6–7 days/week', icon: 'directions_run' },
  { value: 'very_active', label: 'Very Active', desc: 'Intense daily', icon: 'local_fire_department' },
];

// ── Unit conversion helpers ──
const KG_PER_LB = 0.453592;
const CM_PER_IN = 2.54;

function toDisplay(value, field, unit) {
  if (value == null) return '';
  if (unit === 'imperial') return Math.round(value * 10) / 10;
  // stored as lbs/cm — convert
  if (field === 'weight') return Math.round(value * KG_PER_LB * 10) / 10;
  if (field === 'height') return Math.round(value / CM_PER_IN * 10) / 10; // cm → inches backwards? No, stored as cm
  return Math.round(value * 10) / 10;
}

function fromDisplay(displayVal, field, unit) {
  const v = Number(displayVal);
  if (isNaN(v)) return null;
  if (unit === 'imperial') return v; // stored as lbs, cm directly when imperial
  // metric input → stored values
  if (field === 'weight') return Math.round(v / KG_PER_LB * 10) / 10; // kg → lbs
  return v; // height stays cm
}

export default function Profile() {
  const { user: authUser, updateUser: updateAuthUser } = useAuth();
  const [user, setUser] = useState(null);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  const unit = form.preferred_unit || user?.preferred_unit || 'metric';
  const unitLabels = unit === 'imperial'
    ? { weight: 'lbs', height: 'cm', weightShort: 'lbs' }
    : { weight: 'kg', height: 'cm', weightShort: 'kg' };

  useEffect(() => {
    fetchUser()
      .then(data => { setUser(data); setForm(data); setLoading(false); })
      .catch(() => { toast.error('Failed to load profile'); setLoading(false); });
  }, []);

  function handleChange(field, value) { setForm({ ...form, [field]: value }); }

  async function handleSave() {
    setSaving(true);
    try {
      const updated = await updateUser(form);
      setUser(updated);
      setForm(updated);
      setEditing(false);
      updateAuthUser(updated);
      toast.success('Profile updated successfully');
    } catch (err) { toast.error(err.message || 'Failed to save'); }
    setSaving(false);
  }

  function handleCancel() { setForm(user); setEditing(false); }

  if (loading || !user) {
    return <div className="profile-page"><div className="loading-spinner"><div className="spinner" /></div></div>;
  }

  // Computed stats (always in display units)
  const weightKg = user.current_weight_lbs ? user.current_weight_lbs * KG_PER_LB : null;
  const heightM = user.height_cm ? user.height_cm / 100 : null;
  const bmi = weightKg && heightM ? (weightKg / (heightM * heightM)).toFixed(1) : '—';
  const leanMass = user.current_weight_lbs && user.body_fat_pct
    ? (unit === 'imperial'
      ? (user.current_weight_lbs * (1 - user.body_fat_pct / 100)).toFixed(1) + ' lbs'
      : (user.current_weight_lbs * KG_PER_LB * (1 - user.body_fat_pct / 100)).toFixed(1) + ' kg')
    : '—';
  const fatMass = user.current_weight_lbs && user.body_fat_pct
    ? (unit === 'imperial'
      ? (user.current_weight_lbs * (user.body_fat_pct / 100)).toFixed(1) + ' lbs'
      : (user.current_weight_lbs * KG_PER_LB * (user.body_fat_pct / 100)).toFixed(1) + ' kg')
    : '—';
  const displayWeight = user.current_weight_lbs
    ? (unit === 'imperial' ? user.current_weight_lbs.toFixed(1) : (user.current_weight_lbs * KG_PER_LB).toFixed(1))
    : '—';
  const displayGoal = user.goal_weight_lbs
    ? (unit === 'imperial' ? user.goal_weight_lbs.toFixed(1) : (user.goal_weight_lbs * KG_PER_LB).toFixed(1))
    : '—';

  return (
    <motion.div className="profile-page" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Athlete Profile</h2>
            <p>Your body composition data and macro targets</p>
          </div>
          {!editing ? (
            <button 
              onClick={() => setEditing(true)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[var(--surface-container)] text-[var(--on-surface)] font-medium text-sm hover:bg-[var(--surface-container-high)] transition-all"
            >
              <span className="material-icons-outlined text-base">edit</span>
              Edit Profile
            </button>
          ) : (
            <div className="flex items-center gap-3">
              <button 
                onClick={handleCancel}
                className="px-5 py-2.5 rounded-xl bg-[var(--error)]/10 text-[var(--error)] font-medium text-sm hover:bg-[var(--error)]/20 transition-all"
              >
                Cancel
              </button>
              <button 
                onClick={handleSave} 
                disabled={saving}
                className="px-5 py-2.5 rounded-xl bg-[var(--primary-container)] text-[var(--surface)] font-medium text-sm hover:bg-[var(--primary-fixed-dim)] transition-all disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="profile-hero">
        <div className="profile-avatar">
          <span className="material-icons-outlined" style={{ fontSize: 48, color: 'var(--primary-container)' }}>person</span>
        </div>
        <div className="profile-identity">
          {editing ? (
            <>
              <input className="profile-edit-input profile-edit-input--lg" value={form.name} onChange={e => handleChange('name', e.target.value)} placeholder="Name" />
              <input className="profile-edit-input" value={form.email || ''} onChange={e => handleChange('email', e.target.value)} placeholder="Email" />
            </>
          ) : (
            <>
              <h3 className="profile-name">{user.name}</h3>
              <p className="profile-email">{user.email}</p>
              <div style={{ display: 'flex', gap: 'var(--spacing-2)', marginTop: 'var(--spacing-2)' }}>
                {user.primary_goal && <span className="profile-badge">{user.primary_goal.toUpperCase()}</span>}
                {user.gender && <span className="profile-badge profile-badge--dim">{user.gender}</span>}
                {user.age && <span className="profile-badge profile-badge--dim">Age {user.age}</span>}
              </div>
            </>
          )}
        </div>
      </div>

      {/* ── Body Composition ── */}
      <div className="profile-section">
        <div className="profile-section__title">
          <span className="material-icons-outlined" style={{ fontSize: 18 }}>monitor_weight</span>
          Body Composition
          <span className="profile-unit-badge">{unit === 'imperial' ? 'Imperial' : 'Metric'}</span>
        </div>
        <div className="profile-stats-grid">
          {[
            { label: `Current Weight`, field: 'current_weight_lbs', unit: unitLabels.weightShort, editable: true },
            { label: `Goal Weight`, field: 'goal_weight_lbs', unit: unitLabels.weightShort, editable: true },
            { label: 'Height', field: 'height_cm', unit: 'cm', editable: true },
            { label: 'Body Fat', field: 'body_fat_pct', unit: '%', editable: true, step: '0.1' },
            { label: 'BMI', value: bmi, computed: true },
            { label: 'Lean Mass', value: leanMass, computed: true },
            { label: 'Fat Mass', value: fatMass, computed: true },
            { label: 'Age', field: 'age', unit: 'yrs', editable: true },
          ].map(stat => (
            <div key={stat.label} className="profile-stat">
              <div className="profile-stat__label">{stat.label}</div>
              {editing && stat.editable ? (
                <div className="profile-stat__edit">
                  <input type="number" step={stat.step || '1'} value={form[stat.field] || ''} onChange={e => handleChange(stat.field, Number(e.target.value))} />
                  <span>{stat.unit}</span>
                </div>
              ) : (
                <div className={`profile-stat__value ${stat.computed ? 'profile-stat__value--computed' : ''}`}>
                  {stat.value !== undefined ? stat.value : (unit === 'imperial' || stat.field === 'height_cm' || stat.field === 'body_fat_pct' || stat.field === 'age'
                    ? (user[stat.field] || '—')
                    : displayWeight
                  )}
                  {!stat.computed && stat.unit && stat.value === undefined && <span> {stat.unit}</span>}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* ── Daily Macro Targets ── */}
      <div className="profile-section">
        <div className="profile-section__title">
          <span className="material-icons-outlined" style={{ fontSize: 18 }}>track_changes</span>
          Daily Macro Targets
        </div>
        <div className="profile-targets-grid">
          {[
            { label: 'Daily Calories', field: 'daily_calorie_target', icon: 'local_fire_department', color: 'var(--primary-container)', unit: 'kcal', bg: 'rgba(57, 255, 20, 0.08)' },
            { label: 'Protein', field: 'protein_target_g', icon: 'fitness_center', color: 'var(--macro-protein)', unit: 'g', bg: 'rgba(57, 255, 20, 0.08)' },
            { label: 'Carbs', field: 'carbs_target_g', icon: 'bolt', color: 'var(--macro-carbs)', unit: 'g', bg: 'rgba(86, 141, 255, 0.08)' },
            { label: 'Fats', field: 'fats_target_g', icon: 'water_drop', color: 'var(--macro-fats)', unit: 'g', bg: 'rgba(255, 180, 164, 0.08)' },
          ].map(target => (
            <div key={target.field} className="profile-target">
              <div className="profile-target__icon" style={{ background: target.bg, color: target.color }}>
                <span className="material-icons-outlined">{target.icon}</span>
              </div>
              <div className="profile-target__info">
                <div className="profile-target__label">{target.label}</div>
                {editing ? (
                  <input type="number" className="profile-target__input" value={form[target.field]} onChange={e => handleChange(target.field, Number(e.target.value))} />
                ) : (
                  <div className="profile-target__value">{user[target.field]}{target.unit}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Primary Goal ── */}
      <div className="profile-section">
        <div className="profile-section__title">
          <span className="material-icons-outlined" style={{ fontSize: 18 }}>track_changes</span>
          Primary Goal
        </div>
        <div className="activity-chips">
          {[
            { value: 'cut', label: 'Cut (Lose Fat)', desc: 'Caloric deficit for fat loss', icon: 'trending_down' },
            { value: 'maintain', label: 'Maintain', desc: 'Sustain current weight', icon: 'trending_flat' },
            { value: 'bulk', label: 'Bulk (Build Muscle)', desc: 'Caloric surplus for growth', icon: 'trending_up' },
          ].map((g) => (
            <button
              key={g.value}
              className={`activity-chip ${(editing ? form.primary_goal : user.primary_goal) === g.value ? 'active' : ''}`}
              onClick={() => editing && handleChange('primary_goal', g.value)}
              disabled={!editing}
            >
              <span className="material-icons-outlined" style={{ fontSize: 20, marginBottom: 2 }}>{g.icon}</span>
              <div className="activity-chip__label">{g.label}</div>
              <div className="activity-chip__desc">{g.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* ── Activity Level ── */}
      <div className="profile-section">
        <div className="profile-section__title">
          <span className="material-icons-outlined" style={{ fontSize: 18 }}>directions_run</span>
          Activity Level
        </div>
        <div className="activity-chips">
          {ACTIVITY_LEVELS.map(lvl => (
            <button
              key={lvl.value}
              className={`activity-chip ${(editing ? form.activity_level : user.activity_level) === lvl.value ? 'active' : ''}`}
              onClick={() => editing && handleChange('activity_level', lvl.value)}
              disabled={!editing}
            >
              <span className="material-icons-outlined" style={{ fontSize: 20, marginBottom: 2 }}>{lvl.icon}</span>
              <div className="activity-chip__label">{lvl.label}</div>
              <div className="activity-chip__desc">{lvl.desc}</div>
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
