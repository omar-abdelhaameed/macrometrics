import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { registerUser } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../components/ToastProvider';

const STEPS = ['basics', 'body', 'targets'];

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

const slideVariants = {
  enter: (dir) => ({ x: dir > 0 ? 80 : -80, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (dir) => ({ x: dir < 0 ? 80 : -80, opacity: 0 }),
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
      if (form.password.length < 6) { toast.warning('Min 6 characters for password'); return; }
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
    ? { weight: 'lbs', height: 'inches' } : { weight: 'kg', height: 'cm' };

  return (
    <div className="auth-page">
      <div className="auth-card auth-card--wide">
        <div className="auth-logo">
          <span className="material-icons-outlined" style={{ fontSize: 36, color: 'var(--primary-container)' }}>fitness_center</span>
          <h1>MacroMetrics</h1>
          <p>Performance Lab</p>
        </div>

        {/* Step indicator */}
        <div className="onboard-steps">
          {STEPS.map((s, i) => (
            <div key={s} className={`onboard-step ${i <= step ? 'active' : ''} ${i < step ? 'done' : ''}`}>
              <div className="onboard-step__dot">
                {i < step ? <span className="material-icons-outlined" style={{ fontSize: 14 }}>check</span> : i + 1}
              </div>
              <span className="onboard-step__label">{s === 'basics' ? 'Account' : s === 'body' ? 'Body Stats' : 'Your Goal'}</span>
            </div>
          ))}
        </div>

        <form onSubmit={(e) => e.preventDefault()} className="auth-form">
          <AnimatePresence mode="wait" custom={dir}>
            <motion.div
              key={step}
              custom={dir}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.25, ease: 'easeInOut' }}
            >
              {/* ── STEP 0: Account Basics ── */}
              {step === 0 && (
                <>
                  <h2>Create Your Account</h2>
                  <p className="auth-subtitle">Let's start with the basics</p>
                  <div className="auth-fields-grid">
                    <div className="auth-field">
                      <label>Full Name</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">person</span>
                        <input type="text" placeholder="Omar" value={form.name} onChange={e => set('name', e.target.value)} />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label>Email</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">mail</span>
                        <input type="email" placeholder="omar@example.com" value={form.email} onChange={e => set('email', e.target.value)} />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label>Password</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">lock</span>
                        <input type="password" placeholder="Min 6 characters" value={form.password} onChange={e => set('password', e.target.value)} />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label>Confirm Password</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">lock</span>
                        <input type="password" placeholder="Confirm" value={form.confirmPassword} onChange={e => set('confirmPassword', e.target.value)} />
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* ── STEP 1: Body Stats ── */}
              {step === 1 && (
                <>
                  <h2>Body Stats</h2>
                  <p className="auth-subtitle">Help us personalize your experience</p>

                  <div className="auth-field">
                    <label>Gender</label>
                    <div className="onboard-pills">
                      {GENDERS.map(g => (
                        <button type="button" key={g.value} className={`onboard-pill ${form.gender === g.value ? 'active' : ''}`} onClick={() => set('gender', g.value)}>
                          <span className="material-icons-outlined" style={{ fontSize: 18 }}>{g.icon}</span>
                          {g.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="auth-fields-grid auth-fields-grid--3">
                    <div className="auth-field">
                      <label>Age</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">cake</span>
                        <input type="number" placeholder="26" value={form.age} onChange={e => set('age', e.target.value)} min="13" max="99" />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label>Weight ({unitLabel.weight})</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">monitor_weight</span>
                        <input type="number" placeholder={form.preferred_unit === 'imperial' ? '185' : '84'} value={form.current_weight_lbs} onChange={e => set('current_weight_lbs', e.target.value)} />
                      </div>
                    </div>
                    <div className="auth-field">
                      <label>Height ({unitLabel.height})</label>
                      <div className="auth-input-wrap">
                        <span className="material-icons-outlined">height</span>
                        <input type="number" placeholder={form.preferred_unit === 'imperial' ? '71' : '180'} value={form.height_cm} onChange={e => set('height_cm', e.target.value)} />
                      </div>
                    </div>
                  </div>

                  <div className="auth-field" style={{ marginTop: 'var(--spacing-4)' }}>
                    <label>Preferred Units</label>
                    <div className="onboard-pills">
                      <button type="button" className={`onboard-pill ${form.preferred_unit === 'metric' ? 'active' : ''}`} onClick={() => set('preferred_unit', 'metric')}>
                        <span className="material-icons-outlined" style={{ fontSize: 16 }}>straighten</span>
                        Metric (kg, cm)
                      </button>
                      <button type="button" className={`onboard-pill ${form.preferred_unit === 'imperial' ? 'active' : ''}`} onClick={() => set('preferred_unit', 'imperial')}>
                        <span className="material-icons-outlined" style={{ fontSize: 16 }}>square_foot</span>
                        Imperial (lbs, in)
                      </button>
                    </div>
                  </div>

                  <div className="auth-field" style={{ marginTop: 'var(--spacing-4)' }}>
                    <label>Activity Level</label>
                    <div className="onboard-activity">
                      {ACTIVITY_LEVELS.map(lvl => (
                        <button type="button" key={lvl.value} className={`onboard-activity-btn ${form.activity_level === lvl.value ? 'active' : ''}`} onClick={() => set('activity_level', lvl.value)}>
                          <span className="material-icons-outlined" style={{ fontSize: 20 }}>{lvl.icon}</span>
                          <div className="onboard-activity-btn__label">{lvl.label}</div>
                          <div className="onboard-activity-btn__desc">{lvl.desc}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {/* ── STEP 2: Primary Goal ── */}
              {step === 2 && (
                <>
                  <h2>Primary Goal</h2>
                  <p className="auth-subtitle">We'll automatically calculate your optimal macro targets</p>
                  <div className="onboard-activity" style={{ marginTop: 'var(--spacing-6)' }}>
                    {[
                      { value: 'cut', label: 'Cut (Lose Fat)', desc: 'Caloric deficit for fat loss', icon: 'trending_down' },
                      { value: 'maintain', label: 'Maintain', desc: 'Sustain current weight', icon: 'trending_flat' },
                      { value: 'bulk', label: 'Bulk (Build Muscle)', desc: 'Caloric surplus for growth', icon: 'trending_up' },
                    ].map((g) => (
                      <button type="button" key={g.value} className={`onboard-activity-btn ${form.primary_goal === g.value ? 'active' : ''}`} onClick={() => set('primary_goal', g.value)}>
                        <span className="material-icons-outlined" style={{ fontSize: 24, marginBottom: 'var(--spacing-2)' }}>{g.icon}</span>
                        <div className="onboard-activity-btn__label">{g.label}</div>
                        <div className="onboard-activity-btn__desc">{g.desc}</div>
                      </button>
                    ))}
                  </div>
                </>
              )}
            </motion.div>
          </AnimatePresence>

          {/* ── Navigation Buttons ── */}
          <div className="onboard-nav">
            {step > 0 && (
              <button type="button" className="onboard-nav__back" onClick={prevStep}>
                <span className="material-icons-outlined" style={{ fontSize: 18 }}>arrow_back</span>
                Back
              </button>
            )}
            <div style={{ flex: 1 }} />
            {step < STEPS.length - 1 ? (
              <button type="button" className="auth-submit" style={{ maxWidth: 200 }} onClick={nextStep}>
                Continue
                <span className="material-icons-outlined" style={{ fontSize: 18, marginLeft: 6 }}>arrow_forward</span>
              </button>
            ) : (
              <button type="button" className="auth-submit" style={{ maxWidth: 200 }} disabled={loading} onClick={handleSubmit}>
                {loading ? <span className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} /> : 'Create Account'}
              </button>
            )}
          </div>

          <p className="auth-switch">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
