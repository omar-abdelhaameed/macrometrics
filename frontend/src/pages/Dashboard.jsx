import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { fetchDailySummary, fetchMeals } from '../api';
import { useToast } from '../components/ToastProvider';
import WaterTracker from '../components/WaterTracker';

const MACRO_COLORS = {
  protein: '#00F0FF',
  carbs: '#FF6B4A',
  fats: '#B4FF39',
};

function MacroRing({ consumed, target, color, label }) {
  const pct = Math.min((consumed / target) * 100, 100);
  const data = [
    { value: consumed },
    { value: Math.max(target - consumed, 0) },
  ];

  return (
    <motion.div 
      className="macro-ring flex flex-col items-center min-w-[100px]"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="relative w-[100px] h-[100px]">
        <ResponsiveContainer width={100} height={100}>
          <PieChart>
            <defs>
              <filter id={`glow-${label.replace(' ', '')}`}>
                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                <feMerge>
                  <feMergeNode in="coloredBlur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={32}
              outerRadius={44}
              startAngle={90}
              endAngle={-270}
              dataKey="value"
              stroke="none"
              filter={`url(#glow-${label.replace(' ', '')})`}
            >
              <Cell fill={color} />
              <Cell fill="rgba(255,255,255,0.04)" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-xl font-bold font-mono" style={{ color }}>{Math.round(consumed)}</div>
            <div className="text-[10px] text-[var(--on-surface-variant)]">g</div>
          </div>
        </div>
      </div>
      <span className="text-xs font-semibold text-[var(--on-surface-variant)] mt-3 uppercase tracking-wider">{label}</span>
      <span className="text-[10px] text-[var(--on-surface-variant)] mt-1">{Math.round(pct)}%</span>
    </motion.div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const today = new Date().toISOString().split('T')[0];
  const toast = useToast();

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchDailySummary(today).catch(() => null),
      fetchMeals(today).catch(() => []),
    ]).then(([sum, m]) => {
      if (sum) setSummary(sum);
      setMeals(m || []);
      setLoading(false);
    });
  }, [today]);

  if (loading || !summary) {
    return (
      <div className="loading-spinner">
        <div className="spinner" />
      </div>
    );
  }

  const caloriesRemaining = summary.calories_target - summary.calories_consumed;
  const caloriePct = Math.round((summary.calories_consumed / summary.calories_target) * 100);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <div className="page-header">
        <h2>Performance Dashboard</h2>
        <p className="text-[var(--on-surface-variant)]">Track your daily macros and hydration</p>
      </div>

      {/* Hero Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        <motion.div 
          className="stat-card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div className="stat-card__label">Calories</div>
          <div className="stat-card__value stat-card__value--primary">
            {Math.round(summary.calories_consumed)}
            <span className="stat-card__unit">kcal</span>
          </div>
          <div className="stat-card__sub">{caloriePct}% of target</div>
        </motion.div>

        <motion.div 
          className="stat-card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.15 }}
        >
          <div className="stat-card__label">Remaining</div>
          <div className="stat-card__value font-mono">
            {Math.round(caloriesRemaining)}
            <span className="stat-card__unit">kcal</span>
          </div>
          <div className="stat-card__sub">of {summary.calories_target}</div>
        </motion.div>

        <motion.div 
          className="stat-card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="stat-card__label">Protein</div>
          <div className="stat-card__value stat-card__value--protein font-mono">
            {Math.round(summary.protein_consumed)}
            <span className="stat-card__unit">g</span>
          </div>
          <div className="stat-card__sub">/ {summary.protein_target}g</div>
        </motion.div>

        <motion.div 
          className="stat-card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.25 }}
        >
          <div className="stat-card__label">Meals</div>
          <div className="stat-card__value font-mono">
            {meals.length}
            <span className="stat-card__unit">today</span>
          </div>
        </motion.div>
      </div>

      {/* Main Grid - 3 columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Macros Card */}
        <motion.div 
          className="card flex flex-col"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <h3 className="text-lg font-semibold text-[var(--on-surface)] mb-6 flex items-center gap-2">
            <span className="material-icons-outlined text-[var(--primary)]">donut_large</span>
            Macro Distribution
          </h3>
          
          <div className="flex-1 flex items-center justify-center">
            <div className="flex flex-wrap justify-center gap-6">
              <MacroRing 
                consumed={Math.round(summary.protein_consumed)} 
                target={summary.protein_target} 
                color={MACRO_COLORS.protein} 
                label="Protein" 
              />
              <MacroRing 
                consumed={Math.round(summary.carbs_consumed)} 
                target={summary.carbs_target} 
                color={MACRO_COLORS.carbs} 
                label="Carbs" 
              />
              <MacroRing 
                consumed={Math.round(summary.fats_consumed)} 
                target={summary.fats_target} 
                color={MACRO_COLORS.fats} 
                label="Fats" 
              />
            </div>
          </div>
        </motion.div>

        {/* Water Tracker */}
        <motion.div 
          className="card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.35 }}
        >
          <h3 className="text-lg font-semibold text-[var(--on-surface)] mb-6 flex items-center gap-2">
            <span className="material-icons-outlined text-[var(--water)]">water_drop</span>
            Hydration
          </h3>
          <WaterTracker />
        </motion.div>

        {/* Performance Insights */}
        <motion.div 
          className="card"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="text-lg font-semibold text-[var(--on-surface)] mb-6 flex items-center gap-2">
            <span className="material-icons-outlined text-[var(--secondary)]">insights</span>
            Performance Intel
          </h3>
          <div className="space-y-4">
            <div className="p-4 rounded-xl bg-[var(--surface-container-low)] border border-[rgba(255,255,255,0.03)]">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-8 h-8 rounded-lg bg-[rgba(0,240,255,0.1)] flex items-center justify-center">
                  <span className="material-icons-outlined text-[var(--primary)] text-sm">bolt</span>
                </div>
                <div className="text-sm font-semibold text-[var(--on-surface)]">Calorie Progress</div>
              </div>
              <div className="text-sm text-[var(--on-surface-variant)]">
                {summary.calories_consumed === 0 
                  ? 'Start logging meals to track progress.'
                  : `${caloriePct}% consumed. ${caloriesRemaining > 0 ? `${Math.round(caloriesRemaining)} kcal remaining.` : 'Target reached!'}`
                }
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[var(--surface-container-low)] border border-[rgba(255,255,255,0.03)]">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-8 h-8 rounded-lg bg-[rgba(180,255,57,0.1)] flex items-center justify-center">
                  <span className="material-icons-outlined text-[var(--fats)] text-sm">fitness_center</span>
                </div>
                <div className="text-sm font-semibold text-[var(--on-surface)]">Protein</div>
              </div>
              <div className="text-sm text-[var(--on-surface-variant)]">
                {summary.protein_consumed > 0
                  ? `${Math.round(summary.protein_remaining)}g remaining to hit ${summary.protein_target}g target.`
                  : 'Log a protein-rich meal to start tracking.'
                }
              </div>
            </div>

            {meals.length > 0 && (
              <div className="p-4 rounded-xl bg-[var(--surface-container-low)] border border-[rgba(255,255,255,0.03)]">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-8 h-8 rounded-lg bg-[rgba(255,107,74,0.1)] flex items-center justify-center">
                    <span className="material-icons-outlined text-[var(--carbs)] text-sm">restaurant</span>
                  </div>
                  <div className="text-sm font-semibold text-[var(--on-surface)]">Latest Meal</div>
                </div>
                <div className="text-sm text-[var(--on-surface-variant)]">
                  {meals[meals.length - 1]?.meal_type}: {Math.round(meals[meals.length - 1]?.total_calories || 0)} kcal
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}