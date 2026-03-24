import React from 'react';

export default function NumberInput({ value, onChange, min = 1, max, step = 1, suffix = '' }) {
  const handleIncrement = () => {
    const newValue = Math.min((value || 0) + step, max || Infinity);
    onChange(newValue);
  };

  const handleDecrement = () => {
    const newValue = Math.max((value || 0) - step, min);
    onChange(newValue);
  };

  return (
    <div className="number-input-wrapper">
      <button
        type="button"
        className="number-input-btn"
        onClick={handleDecrement}
        disabled={value <= min}
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <path d="M5 12h14" />
        </svg>
      </button>
      <input
        type="number"
        value={value}
        onChange={(e) => {
          const val = Number(e.target.value);
          if (!isNaN(val)) {
            onChange(Math.min(Math.max(val, min), max || val));
          }
        }}
        min={min}
        max={max}
        step={step}
        className="w-16 px-2 py-1.5 rounded-lg bg-[var(--surface-container-high)] text-[var(--on-surface)] text-sm text-center outline-none border border-transparent focus:border-[var(--primary)] font-mono"
      />
      {suffix && <span className="text-xs text-[var(--on-surface-variant)]">{suffix}</span>}
      <button
        type="button"
        className="number-input-btn"
        onClick={handleIncrement}
        disabled={max && value >= max}
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <path d="M12 5v14M5 12h14" />
        </svg>
      </button>
    </div>
  );
}