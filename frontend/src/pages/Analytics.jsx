import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import { fetchAnalyticsSummary, fetchWeightTrend, fetchMacroComposition } from '../api';
import { useToast } from '../components/ToastProvider';

const MACRO_COLORS = ['#39FF14', '#568DFF', '#FFB4A4'];

export default function Analytics() {
  const [activeTab, setActiveTab] = useState('Today');
  const [summary, setSummary] = useState(null);
  const [weightData, setWeightData] = useState([]);
  const [macroComp, setMacroComp] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchAnalyticsSummary(30).catch((err) => { toast.error('Failed to load analytics'); return null; }),
      fetchWeightTrend(30).catch(() => []),
      fetchMacroComposition(30).catch(() => []),
    ]).then(([sum, wt, mc]) => {
      if (sum) setSummary(sum);
      setWeightData(wt || []);
      setMacroComp(mc || []);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="loading-spinner"><div className="spinner" /></div>
      </div>
    );
  }

  const s = summary || { avg_daily_calories: 0, total_weight_change: 0, streak: 0, logged_days: 0 };

  return (
    <motion.div 
      className="analytics-page"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Analytics & Progress</h2>
            <p>30-day performance insights and body composition data</p>
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
      <div className="analytics-stats">
        <div className="stat-card">
          <div className="stat-card__label">Avg. Daily Calories</div>
          <div className="stat-card__value stat-card__value--primary">
            {Math.round(s.avg_daily_calories).toLocaleString()}
            <span className="stat-card__unit">kcal</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__label">Total Weight Change</div>
          <div className="stat-card__value" style={{ color: s.total_weight_change <= 0 ? 'var(--macro-protein)' : 'var(--macro-fats)' }}>
            {s.total_weight_change > 0 ? '+' : ''}{s.total_weight_change}
            <span className="stat-card__unit">lbs</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__label">Streak</div>
          <div className="stat-card__value">
            {s.streak}
            <span className="stat-card__unit">days</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__label">Days Logged</div>
          <div className="stat-card__value">
            {s.logged_days}
            <span className="stat-card__unit">/ {s.period_days}</span>
          </div>
        </div>
      </div>

      {/* ── Charts Row */}
      <div className="analytics-chart-section">
        <div className="lg:col-span-2">
          <div className="chart-card">
            <div className="chart-card__title">Weight Trends vs. Caloric Intake</div>
            <div className="chart-card__subtitle">30-Day performance correlation matrix</div>
            {weightData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={weightData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(53,53,52,0.5)" />
                  <XAxis dataKey="date" tick={{ fill: '#BACCB0', fontSize: 11 }} axisLine={{ stroke: '#3C4B35' }} />
                  <YAxis yAxisId="weight" orientation="left" tick={{ fill: '#39FF14', fontSize: 11 }} domain={['auto', 'auto']}
                    label={{ value: 'Weight (lbs)', angle: -90, position: 'insideLeft', fill: '#39FF14', fontSize: 11 }}
                  />
                  <YAxis yAxisId="calories" orientation="right" tick={{ fill: '#568DFF', fontSize: 11 }} domain={['auto', 'auto']}
                    label={{ value: 'Calories', angle: 90, position: 'insideRight', fill: '#568DFF', fontSize: 11 }}
                  />
                  <Tooltip contentStyle={{ background: '#353534', border: 'none', borderRadius: 8, color: '#E5E2E1', boxShadow: '0 0 20px rgba(0,0,0,0.3)' }} />
                  <Line yAxisId="weight" type="monotone" dataKey="weight" stroke="#39FF14" strokeWidth={2} dot={{ fill: '#39FF14', r: 4, strokeWidth: 0 }} connectNulls />
                  <Line yAxisId="calories" type="monotone" dataKey="calories" stroke="#568DFF" strokeWidth={2} strokeDasharray="5 5" dot={{ fill: '#568DFF', r: 3, strokeWidth: 0 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="empty-state">
                <span className="material-icons-outlined">analytics</span>
                <p>Log meals for a few days to see trends</p>
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="chart-card">
            <div className="chart-card__title">Macro Composition</div>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie data={macroComp} cx="50%" cy="50%" innerRadius={55} outerRadius={75} dataKey="value" stroke="none" paddingAngle={3}>
                  {macroComp.map((entry, index) => (
                    <Cell key={index} fill={MACRO_COLORS[index]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: '#353534', border: 'none', borderRadius: 8, color: '#E5E2E1' }} formatter={(value) => `${value}%`} />
              </PieChart>
            </ResponsiveContainer>
            <div className="macro-legend" style={{ justifyContent: 'center' }}>
              {macroComp.map((item, i) => (
                <div key={item.name} className="macro-legend-item">
                  <div className="macro-legend-dot" style={{ background: MACRO_COLORS[i] }} />
                  <span className="macro-legend-text">{item.name} {item.value}%</span>
                </div>
              ))}
            </div>
          </div>

          <div className="insight-card">
            <div className="insight-card__label">
              <span className="material-icons-outlined" style={{ fontSize: 14, verticalAlign: 'middle', marginRight: 4 }}>auto_awesome</span>
              Insight Engine
            </div>
            <div className="insight-card__text">
              {s.logged_days > 0
                ? `Over the last ${s.period_days} days, you've logged ${s.logged_days} days with an average of ${Math.round(s.avg_daily_calories).toLocaleString()} kcal/day. ${s.streak > 0 ? `Current streak: ${s.streak} days!` : 'Start a new streak by logging today.'}`
                : 'Start logging meals to unlock personalized insights and projections.'
              }
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
