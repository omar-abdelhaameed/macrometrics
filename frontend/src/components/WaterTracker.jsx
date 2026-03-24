import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const DEFAULT_TARGET = 3000; // 3L default

export default function WaterTracker() {
  const [current, setCurrent] = useState(0);
  const [target, setTarget] = useState(DEFAULT_TARGET);
  const [history, setHistory] = useState({});

  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    const saved = localStorage.getItem('water_log');
    if (saved) {
      const data = JSON.parse(saved);
      if (data.date === today) {
        setCurrent(data.current);
        setTarget(data.target || DEFAULT_TARGET);
      } else {
        setCurrent(0);
        localStorage.setItem('water_log', JSON.stringify({ date: today, current: 0, target }));
      }
    }
  }, []);

  const percentage = Math.min((current / target) * 100, 100);
  
  const addWater = (amount) => {
    const newValue = current + amount;
    setCurrent(newValue);
    
    const today = new Date().toISOString().split('T')[0];
    localStorage.setItem('water_log', JSON.stringify({ 
      date: today, 
      current: newValue, 
      target 
    }));
  };

  const subtractWater = () => {
    if (current > 0) {
      const newValue = Math.max(0, current - 250);
      setCurrent(newValue);
      
      const today = new Date().toISOString().split('T')[0];
      localStorage.setItem('water_log', JSON.stringify({ 
        date: today, 
        current: newValue, 
        target 
      }));
    }
  };

  return (
    <div className="flex flex-col items-center">
      <motion.div 
        className="relative w-32 h-72 rounded-[2.5rem] overflow-hidden glass"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Background grid */}
        <div className="absolute inset-0 opacity-20">
          {[...Array(8)].map((_, i) => (
            <div 
              key={i} 
              className="absolute w-full h-px bg-[var(--water)]"
              style={{ bottom: `${12.5 * i}%` }}
            />
          ))}
        </div>
        
        {/* Water fill */}
        <motion.div 
          className="absolute bottom-0 left-0 right-0"
          style={{ height: `${percentage}%` }}
          initial={{ height: 0 }}
          animate={{ height: `${percentage}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div className="absolute inset-0 bg-gradient-to-t from-[var(--water)] to-[var(--water-glow)]" />
          
          {/* Animated bubbles */}
          <div className="absolute inset-0 overflow-hidden">
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute bottom-0 w-2 h-2 rounded-full bg-white/30"
                style={{ left: `${20 + i * 15}%` }}
                animate={{
                  y: [-50, -200],
                  opacity: [0, 0.6, 0],
                }}
                transition={{
                  duration: 2 + i * 0.5,
                  repeat: Infinity,
                  delay: i * 0.3,
                }}
              />
            ))}
          </div>
        </motion.div>

        {/* Percentage display */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.span 
            className="text-3xl font-bold font-mono"
            style={{ 
              color: percentage > 50 ? 'var(--surface)' : 'var(--water)',
              textShadow: percentage > 50 ? 'none' : '0 0 20px var(--water-glow)'
            }}
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            key={percentage}
          >
            {Math.round(percentage)}%
          </motion.span>
        </div>

        {/* Glow effect when full */}
        {percentage >= 100 && (
          <motion.div 
            className="absolute inset-0"
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="absolute inset-0 bg-[var(--water)] blur-xl" />
          </motion.div>
        )}
      </motion.div>

      {/* Controls */}
      <div className="flex items-center gap-6 mt-6">
        <motion.button
          onClick={subtractWater}
          className="w-12 h-12 rounded-full bg-[var(--surface-container)] flex items-center justify-center text-[var(--on-surface-variant)] hover:bg-[var(--surface-container-high)] transition-all"
          whileTap={{ scale: 0.95 }}
          disabled={current === 0}
        >
          <span className="material-icons-outlined">remove</span>
        </motion.button>

        <div className="text-center min-w-[100px]">
          <motion.div 
            className="text-3xl font-bold font-mono text-[var(--water)]"
            key={current}
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
          >
            {current}
          </motion.div>
          <div className="text-xs text-[var(--on-surface-variant)]">/ {target} ml</div>
        </div>

        <motion.button
          onClick={() => addWater(250)}
          className="w-12 h-12 rounded-full bg-[var(--water)] flex items-center justify-center text-white shadow-lg"
          whileTap={{ scale: 0.95 }}
          style={{ boxShadow: '0 0 20px var(--water-glow)' }}
        >
          <span className="material-icons-outlined">add</span>
        </motion.button>
      </div>

      {/* Quick add buttons */}
      <div className="flex gap-3 mt-6">
        {[250, 500].map((amount) => (
          <motion.button
            key={amount}
            onClick={() => addWater(amount)}
            className="px-4 py-2 rounded-xl bg-[var(--surface-container)] text-sm text-[var(--on-surface-variant)] hover:bg-[var(--surface-container-high)] transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            +{amount}ml
          </motion.button>
        ))}
      </div>
    </div>
  );
}