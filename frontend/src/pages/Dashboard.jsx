import React, { useState, useEffect } from 'react';
import {
  PieChart, Pie, Cell, ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip
} from 'recharts';
import { motion } from 'framer-motion';
import { fetchDailySummary, fetchMeals } from '../api';
import { useToast } from '../components/ToastProvider';

const MACRO_COLORS = {
  protein: '#39FF14',
  carbs: '#568DFF',
  fats: '#FFB4A4',
};

function MacroRing({ consumed, target, color, label }) {
  const pct = Math.min((consumed / target) * 100, 100);
  const data = [
    { value: consumed },
    { value: Math.max(target - consumed, 0) },
  ];

  return (
    <div className="macro-ring">
      <div className="macro-ring__chart" style={{ '--glow-color': `${color}33` }}>
        <ResponsiveContainer width={110} height={110}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={38}
              outerRadius={48}
              startAngle={90}
              endAngle={-270}
              dataKey="value"
              stroke="none"
            >
              <Cell fill={color} />
              <Cell fill="rgba(255,255,255,0.06)" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <span className="macro-ring__label">{label}</span>
      <span className="macro-ring__value">{consumed}g</span>
      <span className="macro-ring__target">{Math.round(pct)}% of {target}g</span>
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [meals, setMeals] = useState([]);
  const [plateau, setPlateau] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('Today');
  const today = new Date().toISOString().split('T')[0];
  const toast = useToast();

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchDailySummary(today).catch((err) => { toast.error('Failed to load daily summary'); return null; }),
      fetchMeals(today).catch((err) => { toast.error('Failed to load meals'); return []; }),
      import('../api').then(m => m.fetchWeightPlateau(7)).catch(() => null)
    ]).then(([sum, m, plat]) => {
      if (sum) setSummary(sum);
      setMeals(m || []);
      if (plat) setPlateau(plat);
      setLoading(false);
    });
  }, [today]);

  if (loading || !summary) {
    return (
      <div className="dashboard-page">
        <div className="loading-spinner"><div className="spinner" /></div>
      </div>
    );
  }

  const caloriesRemaining = summary.calories_target - summary.calories_consumed;
  const caloriePct = Math.round((summary.calories_consumed / summary.calories_target) * 100);

  // Build weekly data from meals array if we have them
  const weeklyData = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return { day: d.toLocaleDateString('en', { weekday: 'short' }), value: 0 };
  });

  return (
    <motion.div 
      className="dashboard-page"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      {/* ── Header */}
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Performance Dashboard</h2>
            <p>Track your daily macros and metabolic performance</p>
          </div>
          <div className="view-tabs">
            {['Today', 'Weekly Overview', 'Monthly Report'].map((tab) => (
              <button key={tab} className={`view-tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ── Hero Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-card__accent" style={{ background: 'var(--primary-container)' }} />
          <div className="stat-card__label">Calories Consumed</div>
          <div className="stat-card__value stat-card__value--primary">
            {Math.round(summary.calories_consumed)}
            <span className="stat-card__unit">kcal</span>
          </div>
          <div className="stat-card__sub">{caloriePct}% of daily target</div>
        </div>
        <div className="stat-card">
          <div className="stat-card__accent" style={{ background: 'var(--secondary-container)' }} />
          <div className="stat-card__label">Remaining</div>
          <div className="stat-card__value">
            {Math.round(caloriesRemaining)}
            <span className="stat-card__unit">kcal</span>
          </div>
          <div className="stat-card__sub">Target: {summary.calories_target} kcal</div>
        </div>
        <div className="stat-card">
          <div className="stat-card__accent" style={{ background: 'var(--macro-protein)' }} />
          <div className="stat-card__label">Protein</div>
          <div className="stat-card__value" style={{ color: 'var(--macro-protein)' }}>
            {Math.round(summary.protein_consumed)}
            <span className="stat-card__unit">/ {summary.protein_target}g</span>
          </div>
          <div className="stat-card__sub">{Math.round(summary.protein_consumed / summary.protein_target * 100)}% complete</div>
        </div>
        <div className="stat-card">
          <div className="stat-card__accent" style={{ background: 'var(--macro-carbs)' }} />
          <div className="stat-card__label">Meals Logged</div>
          <div className="stat-card__value">
            {meals.length}
            <span className="stat-card__unit">meals</span>
          </div>
          <div className="stat-card__sub">Today</div>
        </div>
      </div>

      {/* ── Main Grid */}
      <div className="dashboard-grid">
        <div className="card">
          <div className="card__title">
            Macro Distribution
            <span className="material-icons-outlined">tune</span>
          </div>
          <div className="macro-rings-container">
            <MacroRing consumed={Math.round(summary.protein_consumed)} target={summary.protein_target} color={MACRO_COLORS.protein} label="Protein" />
            <MacroRing consumed={Math.round(summary.carbs_consumed)} target={summary.carbs_target} color={MACRO_COLORS.carbs} label="Carbs" />
            <MacroRing consumed={Math.round(summary.fats_consumed)} target={summary.fats_target} color={MACRO_COLORS.fats} label="Fats" />
          </div>
          <div className="macro-legend">
            {[
              { label: 'Protein', color: MACRO_COLORS.protein },
              { label: 'Carbs', color: MACRO_COLORS.carbs },
              { label: 'Fats', color: MACRO_COLORS.fats },
            ].map((item) => (
              <div key={item.label} className="macro-legend-item">
                <div className="macro-legend-dot" style={{ background: item.color }} />
                <span className="macro-legend-text">{item.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card__title">
            Daily Timeline
            <span className="material-icons-outlined">schedule</span>
          </div>
          <div className="timeline">
            {meals.length === 0 ? (
              <div className="empty-state">
                <span className="material-icons-outlined">restaurant</span>
                <p>No meals logged yet today</p>
              </div>
            ) : (
              meals.map((meal, i) => (
                <div key={i} className="timeline-item">
                  <div className="timeline-dot" />
                  <div className="timeline-content">
                    <div className="timeline-time">{meal.meal_type}</div>
                    <div className="timeline-name">
                      {meal.ingredients?.map(ing => ing.ingredient_name).join(', ') || 'Meal'}
                    </div>
                    <div className="timeline-macros">
                      {Math.round(meal.total_calories)} kcal • P: {Math.round(meal.total_protein)}g • C: {Math.round(meal.total_carbs)}g • F: {Math.round(meal.total_fats)}g
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* ── Bottom Row */}
      <div className="dashboard-grid">
        <div className="card">
          <div className="card__title">
            Metabolic Intensity
            <span className="material-icons-outlined">local_fire_department</span>
          </div>
          <p style={{ fontSize: 'var(--label-sm)', color: 'var(--on-surface-variant)', marginBottom: 'var(--spacing-4)' }}>
            Last 30 Days Calibration
          </p>
          <div className="heatmap-grid">
            {Array.from({ length: 28 }, (_, i) => {
              const level = meals.length > 0 ? Math.floor(Math.random() * 5) + 1 : 1;
              return <div key={i} className={`heatmap-cell heatmap-cell--l${level}`} />;
            })}
          </div>
          <div className="heatmap-labels">
            <span>Low</span>
            <span>Moderate</span>
            <span>High</span>
            <span>Peak</span>
          </div>
        </div>

        <div className="card">
          <div className="card__title">
            Performance Intel
            <span className="material-icons-outlined">notification_important</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-4)' }}>
            {plateau && plateau.is_plateau && (
              <div className="alert-panel" style={{ border: '1px solid var(--primary)', background: 'rgba(57,255,20,0.05)' }}>
                <div className="alert-panel__icon" style={{ color: 'var(--primary)', background: 'transparent' }}>
                  <span className="material-icons-outlined">psychology</span>
                </div>
                <div>
                  <div className="alert-panel__title" style={{ color: 'var(--primary)' }}>AI Coach: Plateau Detected</div>
                  <div className="alert-panel__text">
                    {plateau.suggestion} Ask the AI Coach to adjust your macros or schedule a refeed!
                  </div>
                </div>
              </div>
            )}
            <div className="alert-panel">
              <div className="alert-panel__icon alert-panel__icon--green">
                <span className="material-icons-outlined">timer</span>
              </div>
              <div>
                <div className="alert-panel__title">
                  {summary.calories_consumed === 0 ? 'Ready to Track' : 'Progress Update'}
                </div>
                <div className="alert-panel__text">
                  {summary.calories_consumed === 0
                    ? 'Start logging meals to unlock real-time performance insights.'
                    : `You've consumed ${caloriePct}% of your daily calories. ${caloriesRemaining > 0 ? `${Math.round(caloriesRemaining)} kcal remaining.` : 'Target reached!'}`
                  }
                </div>
              </div>
            </div>
            <div className="alert-panel">
              <div className="alert-panel__icon alert-panel__icon--orange">
                <span className="material-icons-outlined">trending_up</span>
              </div>
              <div>
                <div className="alert-panel__title">Protein Tracking</div>
                <div className="alert-panel__text">
                  {summary.protein_consumed > 0
                    ? `${Math.round(summary.protein_remaining)}g protein remaining to hit your ${summary.protein_target}g target.`
                    : 'Log a high-protein meal to start building your daily profile.'
                  }
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Weekly Calorie Chart */}
      <div className="card" style={{ marginTop: 'var(--spacing-6)' }}>
        <div className="card__title">
          Weekly Calorie Trend
          <span className="material-icons-outlined">show_chart</span>
        </div>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={weeklyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(53,53,52,0.5)" />
            <XAxis dataKey="day" tick={{ fill: '#BACCB0', fontSize: 11 }} />
            <YAxis tick={{ fill: '#BACCB0', fontSize: 11 }} domain={[0, 'auto']} />
            <Tooltip
              contentStyle={{
                background: '#353534',
                border: 'none',
                borderRadius: 8,
                color: '#E5E2E1',
                boxShadow: '0 0 20px rgba(0,0,0,0.3)',
              }}
            />
            <Line type="monotone" dataKey="value" stroke="#39FF14" strokeWidth={2}
              dot={{ fill: '#39FF14', r: 4, strokeWidth: 0 }}
              activeDot={{ r: 6, fill: '#39FF14', stroke: '#131313', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
