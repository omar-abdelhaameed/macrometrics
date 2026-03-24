import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { registerUser } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../components/ToastProvider';

const STEPS = ['basics', 'body', 'goals'];

const ACTIVITY_LEVELS = [
  { value: 'sedentary', label: 'Sedentary', desc: 'Little or no exercise', icon: 'weekend' },
  { value: 'light', label: 'Lightly Active', desc: '1–3 days/week', icon: 'directions_walk' },
  { value: 'moderate', label: 'Moderate', desc: '3–5 days/week', icon: 'fitness_center' },
  { value: 'active', label: 'Active', desc: '6–7 days/week', icon: 'directions_run' },
  { value: 'very_active', label: 'Very Active', desc: 'Intense daily', icon: 'local_fire_department' },
];

const GENDERS = [
  { value: 'male', label: 'Male', icon: 'male' },
  { value: 'female', label: 'Female', icon: 'female' },
];

const GOALS = [
  { 
    value: 'cut', 
    label: 'Cut', 
    desc: 'Lose fat & get lean', 
    icon: 'trending_down',
    color: '#00F0FF',
    glow: 'rgba(0, 240, 255, 0.2)'
  },
  { 
    value: 'maintain', 
    label: 'Maintain', 
    desc: 'Stay where you are', 
    icon: 'trending_flat',
    color: '#B4FF39',
    glow: 'rgba(180, 255, 57, 0.2)'
  },
  { 
    value: 'bulk', 
    label: 'Bulk', 
    desc: 'Build muscle & strength', 
    icon: 'trending_up',
    color: '#FF6B4A',
    glow: 'rgba(255, 107, 74, 0.2)'
  },
];

const slideVariants = {
  enter: (dir) => ({ x: dir > 0 ? 100 : -100, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (dir) => ({ x: dir < 0 ? 100 : -100, opacity: 0 }),
};

export default function Register() {
  const [step, setStep] = useState(0);
  const [dir, setDir] = useState(1);
  const [form, setForm] = useState({
    name: '', email: '', password: '', confirmPassword: '',
    age: '', gender: 'male',
    current_weight_lbs: '', height_cm: '',
    activity_level: 'moderate',
    primary_goal: 'maintain',
    preferred_unit: 'metric',
  });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  function set(field, value) { setForm(f => ({ ...f, [field]: value })); }

  function nextStep() {
    if (step === 0) {
      if (!form.name || !form.email || !form.password) { toast.warning('Fill all required fields'); return; }
      if (form.password.length < 8) { toast.warning('Min 8 characters for password'); return; }
      if (form.password !== form.confirmPassword) { toast.error('Passwords do not match'); return; }
    }
    if (step === 1) {
      if (!form.age || !form.current_weight_lbs || !form.height_cm) { toast.warning('Please fill in all body stats'); return; }
    }
    setDir(1); setStep(s => Math.min(s + 1, STEPS.length - 1));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function prevStep() { 
    setDir(-1); setStep(s => Math.max(s - 1, 0)); 
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (step < STEPS.length - 1) {
      nextStep();
      return;
    }
    setLoading(true);
    try {
      const { confirmPassword, ...payload } = form;
      payload.age = payload.age ? Number(payload.age) : null;
      payload.current_weight_lbs = payload.current_weight_lbs ? Number(payload.current_weight_lbs) : null;
      payload.height_cm = payload.height_cm ? Number(payload.height_cm) : null;
      if (form.preferred_unit === 'metric') {
        if (payload.current_weight_lbs) {
          payload.current_weight_lbs = Math.round(payload.current_weight_lbs * 2.20462);
        }
      } else {
        if (payload.height_cm) {
          payload.height_cm = Math.round(payload.height_cm * 2.54);
        }
      }
      const data = await registerUser(payload);
      login(data.access_token, data.user);
      toast.success(`Welcome, ${data.user.name}! Your account is ready.`);
      navigate('/');
    } catch (err) { toast.error(err.message || 'Registration failed'); }
    setLoading(false);
  }

  const unitLabel = form.preferred_unit === 'imperial'
    ? { weight: 'lbs', height: 'in' } : { weight: 'kg', height: 'cm' };

  return (
    <div className="auth-page">
      <motion.div 
        className="auth-card auth-card--wide"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        {/* Logo */}
        <div className="auth-logo">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-[var(--primary)] to-[var(--secondary)] flex items-center justify-center shadow-lg" style={{ boxShadow: '0 0 30px var(--protein-glow)' }}>
            <span className="material-icons-outlined text-3xl text-[var(--surface)]">fitness_center</span>
          </div>
          <h1 className="text-3xl font-bold">MacroMetrics</h1>
          <p className="text-xs uppercase tracking-[0.25em] text-[var(--on-surface-variant)]">Performance Lab</p>
        </div>

        {/* Step indicator */}
        <div className="onboard-steps mb-10">
          {STEPS.map((s, i) => (
            <div key={s} className={`onboard-step ${i <= step ? 'active' : ''} ${i < step ? 'done' : ''}`}>
              <div className="onboard-step__dot">
                {i < step ? <span className="material-icons-outlined" style={{ fontSize: 14 }}>check</span> : i + 1}
              </div>
              <span className="onboard-step__label">
                {s === 'basics' ? 'Account' : s === 'body' ? 'Body Stats' : 'Your Goal'}
              </span>
            </div>
          ))}
        </div>

        <form onSubmit={(e) => e.preventDefault()}>
          <AnimatePresence mode="wait" custom={dir}>
            <motion.div
              key={step}
              custom={dir}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.3, ease: 'easeInOut' }}
            >
              {/* STEP 0: Account Basics */}
              {step === 0 && (
                <div className="space-y-5">
                  <div>
                    <h2 className="text-2xl font-bold text-[var(--on-surface)] mb-2">Create Account</h2>
                    <p className="text-sm text-[var(--on-surface-variant)]">Let's start with your basics</p>
                  </div>
                  
                  <div className="auth-field">
                    <label className="text-sm text-[var(--on-surface-variant)] mb-2 block">Full Name</label>
                    <div className="auth-input-wrap">
                      <span className="material-icons-outlined">person</span>
                      <input 
                        type="text" 
                        placeholder="Your name" 
                        value={form.name} 
                        onChange={e => set('name', e.target.value)}
                        className="w-full"
                      />
                    </div>
                  </div>
                  
                  <div className="auth-field">
                    <label className="text-sm text-[var(--on-surface-variant)] mb-2 block">Email</label>
                    <div className="auth-input-wrap">
                      <span className="material-icons-outlined">mail</span>
                      <input 
                        type="email" 
                        placeholder="you@example.com" 
                        value={form.email} 
                        onChange={e => set('email', e.target.value)}
                        className="w-full"
                      />
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="auth-field">
                      <label className="text-sm text-[var(--on-surface-variant)] mb-2 block">Password</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">lock</span>
                        <input 
                          type="password" 
                          placeholder="Min 8 chars" 
                          value={form.password} 
                          onChange={e => set('password', e.target.value)}
                          className="w-full"
                        />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label className="text-sm text-[var(--on-surface-variant)] mb-2 block">Confirm</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">lock</span>
                        <input 
                          type="password" 
                          placeholder="Confirm" 
                          value={form.confirmPassword} 
                          onChange={e => set('confirmPassword', e.target.value)}
                          className="w-full"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 1: Body Stats */}
              {step === 1 && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-2xl font-bold text-[var(--on-surface)] mb-2">Body Stats</h2>
                    <p className="text-sm text-[var(--on-surface-variant)]">Help us personalize your targets</p>
                  </div>

                  {/* Gender */}
                  <div className="auth-field">
                    <label className="text-sm text-[var(--on-surface-variant)] mb-3 block">Gender</label>
                    <div className="flex gap-3">
                      {GENDERS.map(g => (
                        <button
                          type="button"
                          key={g.value}
                          onClick={() => set('gender', g.value)}
                          className={`flex-1 py-4 rounded-2xl text-center transition-all border ${
                            form.gender === g.value 
                              ? 'bg-[rgba(0,240,255,0.1)] border-[var(--primary)] text-[var(--primary)]' 
                              : 'bg-[var(--surface-container)] border-transparent text-[var(--on-surface-variant)]'
                          }`}
                        >
                          <span className="material-icons-outlined text-2xl mb-1">{g.icon}</span>
                          <div className="text-sm font-medium">{g.label}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-3 gap-4">
                    <div className="auth-field">
                      <label className="text-xs text-[var(--on-surface-variant)] mb-2 block">Age</label>
                      <div className="auth-input-wrap py-3">
                        <span className="material-icons-outlined text-lg">cake</span>
                        <input 
                          type="number" 
                          placeholder="26" 
                          value={form.age} 
                          onChange={e => set('age', e.target.value)}
                          className="w-full font-mono"
                        />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label className="text-xs text-[var(--on-surface-variant)] mb-2 block">Weight ({unitLabel.weight})</label>
                      <div className="auth-input-wrap py-3">
                        <span className="material-icons-outlined text-lg">monitor_weight</span>
                        <input 
                          type="number" 
                          placeholder="80" 
                          value={form.current_weight_lbs} 
                          onChange={e => set('current_weight_lbs', e.target.value)}
                          className="w-full font-mono"
                        />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label className="text-xs text-[var(--on-surface-variant)] mb-2 block">Height ({unitLabel.height})</label>
                      <div className="auth-input-wrap py-3">
                        <span className="material-icons-outlined text-lg">height</span>
                        <input 
                          type="number" 
                          placeholder="180" 
                          value={form.height_cm} 
                          onChange={e => set('height_cm', e.target.value)}
                          className="w-full font-mono"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Unit Toggle */}
                  <div className="flex gap-3">
                    <button
                      type="button"
                      onClick={() => set('preferred_unit', 'metric')}
                      className={`flex-1 py-3 rounded-xl text-sm font-medium transition-all ${
                        form.preferred_unit === 'metric'
                          ? 'bg-[var(--primary)] text-[var(--surface)]'
                          : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
                      }`}
                    >
                      Metric (kg, cm)
                    </button>
                    <button
                      type="button"
                      onClick={() => set('preferred_unit', 'imperial')}
                      className={`flex-1 py-3 rounded-xl text-sm font-medium transition-all ${
                        form.preferred_unit === 'imperial'
                          ? 'bg-[var(--primary)] text-[var(--surface)]'
                          : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
                      }`}
                    >
                      Imperial (lbs, in)
                    </button>
                  </div>

                  {/* Activity Level */}
                  <div className="auth-field">
                    <label className="text-sm text-[var(--on-surface-variant)] mb-3 block">Activity Level</label>
                    <div className="flex flex-wrap gap-2">
                      {ACTIVITY_LEVELS.map(lvl => (
                        <button
                          key={lvl.value}
                          type="button"
                          onClick={() => set('activity_level', lvl.value)}
                          className={`px-4 py-2 rounded-xl text-sm transition-all ${
                            form.activity_level === lvl.value
                              ? 'bg-[var(--primary)] text-[var(--surface)] font-medium'
                              : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
                          }`}
                        >
                          {lvl.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 2: Goals - VISUAL CARDS */}
              {step === 2 && (
                <div className="space-y-6">
                  <div>
                    <h2 className="text-2xl font-bold text-[var(--on-surface)] mb-2">Your Goal</h2>
                    <p className="text-sm text-[var(--on-surface-variant)]">We'll calculate your optimal macros</p>
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    {GOALS.map((goal) => (
                      <motion.button
                        key={goal.value}
                        type="button"
                        onClick={() => set('primary_goal', goal.value)}
                        className={`relative p-6 rounded-2xl border-2 transition-all text-center overflow-hidden ${
                          form.primary_goal === goal.value
                            ? 'border-[var(--on-surface)]'
                            : 'border-transparent'
                        }`}
                        style={{
                          background: form.primary_goal === goal.value ? goal.glow : 'var(--surface-container)',
                        }}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        {form.primary_goal === goal.value && (
                          <motion.div
                            className="absolute inset-0"
                            style={{ background: goal.glow }}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                          />
                        )}
                        <div className="relative z-10">
                          <div 
                            className="w-14 h-14 mx-auto mb-3 rounded-xl flex items-center justify-center"
                            style={{ 
                              background: form.primary_goal === goal.value ? goal.color : 'var(--surface-container-high)',
                              boxShadow: form.primary_goal === goal.value ? `0 0 20px ${goal.glow}` : 'none'
                            }}
                          >
                            <span 
                              className="material-icons-outlined text-2xl"
                              style={{ color: form.primary_goal === goal.value ? '#0A0A0A' : 'var(--on-surface-variant)' }}
                            >
                              {goal.icon}
                            </span>
                          </div>
                          <div 
                            className="text-lg font-bold mb-1"
                            style={{ color: form.primary_goal === goal.value ? goal.color : 'var(--on-surface)' }}
                          >
                            {goal.label}
                          </div>
                          <div className="text-xs text-[var(--on-surface-variant)]">
                            {goal.desc}
                          </div>
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div className="flex items-center gap-4 mt-10">
            {step > 0 && (
              <button 
                type="button" 
                onClick={prevStep}
                className="px-6 py-3 rounded-xl bg-[var(--surface-container)] text-[var(--on-surface-variant)] font-medium hover:bg-[var(--surface-container-high)] transition-all flex items-center gap-2"
              >
                <span className="material-icons-outlined">arrow_back</span>
                Back
              </button>
            )}
            <div className="flex-1" />
            {step < STEPS.length - 1 ? (
              <button 
                type="button" 
                onClick={nextStep}
                className="auth-submit px-8 py-3"
              >
                Continue
                <span className="material-icons-outlined ml-1">arrow_forward</span>
              </button>
            ) : (
              <button 
                type="button" 
                className="auth-submit px-8 py-3"
                disabled={loading}
                onClick={handleSubmit}
              >
                {loading ? (
                  <div className="spinner" style={{ width: 20, height: 20 }} />
                ) : (
                  <>
                    Create Account
                    <span className="material-icons-outlined ml-1">rocket_launch</span>
                  </>
                )}
              </button>
            )}
          </div>

          <p className="auth-switch mt-8">
            Already have an account? <Link to="/login" className="text-[var(--primary)] hover:underline">Sign in</Link>
          </p>
        </form>
      </motion.div>
    </div>
  );
}