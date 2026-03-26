import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchIngredients, searchUSDA, saveFromUSDA, logMeal } from '../api';
import { useToast } from '../components/ToastProvider';
import NumberInput from '../components/NumberInput';

const MEAL_TYPES = [
  { value: 'breakfast', label: 'Breakfast', icon: '🌅' },
  { value: 'lunch', label: 'Lunch', icon: '☀️' },
  { value: 'dinner', label: 'Dinner', icon: '🌙' },
  { value: 'snack', label: 'Snack', icon: '🍿' },
  { value: 'pre_workout', label: 'Pre-Workout', icon: '⚡' },
  { value: 'post_workout', label: 'Post-Workout', icon: '💪' },
];

export default function MealLogger() {
  const [ingredients, setIngredients] = useState([]);
  const [query, setQuery] = useState('');
  const [searchMode, setSearchMode] = useState('usda'); // usda | local
  const [usdaResults, setUsdaResults] = useState([]);
  const [usdaLoading, setUsdaLoading] = useState(false);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [mealType, setMealType] = useState('lunch');
  const [logging, setLogging] = useState(false);
  const [activeMobileTab, setActiveMobileTab] = useState('search');
  const toast = useToast();

  useEffect(() => {
    fetchIngredients(query)
      .then(setIngredients)
      .catch(() => toast.error('Failed to load local ingredients'));
      
    // SaaS Autocomplete: trigger global search automatically when typing > 1 char
    if (searchMode === 'usda' && query.length >= 2) {
      const timeoutId = setTimeout(() => {
        handleUsdaSearch(query);
      }, 400); // 400ms debounce
      return () => clearTimeout(timeoutId);
    } else if (searchMode === 'usda' && query.length < 2) {
      setUsdaResults([]);
    }
  }, [query, searchMode]);

  async function handleUsdaSearch(searchQuery = query) {
    if (!searchQuery || searchQuery.length < 2) return;
    setUsdaLoading(true);
    try {
      const response = await searchUSDA(searchQuery);
      const results = response.results || response;
      setUsdaResults(results);
    } catch (err) {
      toast.error(err.message || 'Search failed');
    }
    setUsdaLoading(false);
  }

  async function handleSaveUsda(food) {
    try {
      const saved = await saveFromUSDA(food);
      toast.success(`${saved.name} saved to your foods`);
      setIngredients((prev) => [saved, ...prev]);
    } catch (err) {
      toast.error(err.message || 'Failed to save');
    }
  }

  function addIngredient(ing) {
    const exists = selectedIngredients.find((s) => s.id === ing.id);
    if (exists) return;
    setSelectedIngredients([...selectedIngredients, { ...ing, serving_size_g: 100 }]);
  }

  async function handleQuickAdd(food) {
    try {
      const saved = await saveFromUSDA(food);
      addIngredient(saved);
      toast.success(`${saved.name} added to meal!`);
    } catch (err) {
      toast.error(err.message || 'Failed to add');
    }
  }

  function updateServing(id, value) {
    setSelectedIngredients(selectedIngredients.map((s) =>
      s.id === id ? { ...s, serving_size_g: Number(value) } : s
    ));
  }

  function removeIngredient(id) {
    setSelectedIngredients(selectedIngredients.filter((s) => s.id !== id));
  }

  const totals = selectedIngredients.reduce((acc, ing) => {
    const factor = ing.serving_size_g / 100;
    return {
      calories: acc.calories + ing.calories_per_100g * factor,
      protein: acc.protein + ing.protein_per_100g * factor,
      carbs: acc.carbs + ing.carbs_per_100g * factor,
      fats: acc.fats + ing.fats_per_100g * factor,
    };
  }, { calories: 0, protein: 0, carbs: 0, fats: 0 });

  async function handleLogMeal() {
    if (selectedIngredients.length === 0) {
      toast.warning('Add at least one ingredient');
      return;
    }
    setLogging(true);
    try {
      await logMeal({
        date: new Date().toISOString().split('T')[0],
        meal_type: mealType,
        ingredients: selectedIngredients.map((s) => ({
          ingredient_id: s.id,
          serving_size_g: s.serving_size_g,
        })),
      });
      const label = MEAL_TYPES.find(t => t.value === mealType)?.label || mealType;
      toast.success(`${label} logged successfully!`);
      setSelectedIngredients([]);
    } catch (err) {
      toast.error(typeof err === 'string' ? err : err?.detail || err?.message || 'Failed to log meal');
    }
    setLogging(false);
  }

  return (
    <motion.div 
      className="meal-logger-page"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Meal Logger</h2>
            <p>Search ingredients, build meals, track macros</p>
          </div>
        </div>
      </div>

      {/* Mobile Tab Toggle */}
      <div className="flex lg:hidden mb-4 border-b border-[var(--outline-variant)]">
        <button
          onClick={() => setActiveMobileTab('search')}
          className={`flex-1 py-3 text-sm font-medium transition-colors ${
            activeMobileTab === 'search'
              ? 'text-[var(--primary)] border-b-2 border-[var(--primary)]'
              : 'text-[var(--on-surface-variant)]'
          }`}
        >
          Search
        </button>
        <button
          onClick={() => setActiveMobileTab('builder')}
          className={`flex-1 py-3 text-sm font-medium transition-colors ${
            activeMobileTab === 'builder'
              ? 'text-[var(--primary)] border-b-2 border-[var(--primary)]'
              : 'text-[var(--on-surface-variant)]'
          }`}
        >
          Builder
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-6 flex flex-col-reverse lg:grid">
        {/* ── Left: Meal Builder ── */}
        <div className={`meal-builder lg:block ${activeMobileTab === 'builder' ? 'block' : 'hidden'}`}>
          <div className="meal-builder__title">
            <span className="material-icons-outlined text-[var(--primary)]">restaurant</span>
            Meal Builder
          </div>

          <div className="meal-type-selector">
            {MEAL_TYPES.map((type) => (
              <button
                key={type.value}
                className={`meal-type-chip ${mealType === type.value ? 'active' : ''}`}
                onClick={() => setMealType(type.value)}
              >
                <span className="meal-type-icon">{type.icon}</span>
                <span className="meal-type-label">{type.label}</span>
              </button>
            ))}
          </div>

          {selectedIngredients.length === 0 ? (
            <div className="empty-state" style={{ padding: 'var(--spacing-8)' }}>
              <span className="material-icons-outlined">add_shopping_cart</span>
              <p>Click ingredients to add them</p>
            </div>
          ) : (
            selectedIngredients.map((ing) => (
              <div key={ing.id} className="builder-item">
                <div className="builder-item__info">
                  <div className="builder-item__name">{ing.name}</div>
                  <div className="builder-item__cals">
                    {Math.round(ing.calories_per_100g * ing.serving_size_g / 100)} kcal
                  </div>
                </div>
                <div className="builder-item__serving">
                  <NumberInput
                    value={ing.serving_size_g}
                    onChange={(val) => updateServing(ing.id, val)}
                    min={1}
                    max={2000}
                    step={10}
                    suffix="g"
                  />
                </div>
                <button className="builder-item__remove" onClick={() => removeIngredient(ing.id)}>
                  <span className="material-icons-outlined">close</span>
                </button>
              </div>
            ))
          )}

          {selectedIngredients.length > 0 && (
            <div className="meal-totals">
              <div className="meal-totals__row">
                <span className="meal-totals__label">Calories</span>
                <span className="meal-totals__value">{Math.round(totals.calories)} kcal</span>
              </div>
              <div className="meal-totals__row">
                <span className="meal-totals__label">Protein</span>
                <span className="meal-totals__value meal-totals__value--protein">{Math.round(totals.protein)}g</span>
              </div>
              <div className="meal-totals__row">
                <span className="meal-totals__label">Carbs</span>
                <span className="meal-totals__value meal-totals__value--carbs">{Math.round(totals.carbs)}g</span>
              </div>
              <div className="meal-totals__row">
                <span className="meal-totals__label">Fats</span>
                <span className="meal-totals__value meal-totals__value--fats">{Math.round(totals.fats)}g</span>
              </div>

              <button className="btn-log-meal" onClick={handleLogMeal} disabled={logging}>
                {logging ? 'Logging...' : `Log ${mealType.replace('_', ' ')}`}
              </button>
            </div>
          )}
        </div>

        {/* Sticky Mobile Summary Bar */}
        {selectedIngredients.length > 0 && (
          <div className="fixed bottom-0 left-0 right-0 p-4 bg-[var(--surface-container)] border-t border-[var(--outline-variant)] md:hidden flex items-center justify-between gap-4 z-50">
            <div className="flex flex-col">
              <span className="text-xs text-[var(--on-surface-variant)]">Total</span>
              <span className="text-lg font-bold text-[var(--primary)]">{Math.round(totals.calories)} kcal</span>
            </div>
            <button 
              className="px-6 py-3 rounded-xl bg-[var(--primary)] text-[var(--surface)] font-bold text-sm"
              onClick={handleLogMeal}
              disabled={logging}
            >
              {logging ? '...' : 'Log Meal'}
            </button>
          </div>
        )}

        {/* ── Left: Ingredient Search ── */}
        <div className={`ingredient-panel lg:block ${activeMobileTab === 'search' ? 'block' : 'hidden'}`}>
          <div className="search-mode-toggle">
            <button className={`search-mode-btn ${searchMode === 'usda' ? 'active' : ''}`} onClick={() => setSearchMode('usda')}>
              <span className="material-icons-outlined" style={{ fontSize: 16 }}>travel_explore</span>
              Food Search
            </button>
            <button className={`search-mode-btn ${searchMode === 'local' ? 'active' : ''}`} onClick={() => setSearchMode('local')}>
              <span className="material-icons-outlined" style={{ fontSize: 16 }}>favorite</span>
              Saved Foods
            </button>
          </div>

          <div className="flex gap-2 mb-4">
            <div className="search-bar flex-1 h-12 relative">
              <span className="material-icons-outlined text-[var(--on-surface-variant)] absolute left-3 top-1/2 -translate-y-1/2">search</span>
              <input
                type="text"
                placeholder={searchMode === 'local' ? 'Search your saved foods...' : 'Search foods, brands, or USDA database...'}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full h-full pl-10 pr-4 bg-transparent outline-none text-sm text-[var(--on-surface)]"
              />
              {usdaLoading && searchMode === 'usda' && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 border-2 border-[var(--primary)] border-t-transparent rounded-full animate-spin"></div>
              )}
            </div>
          </div>

          <div className="ingredient-list">
            {searchMode === 'local' ? (
              ingredients.length === 0 ? (
                <div className="empty-state">
                  <span className="material-icons-outlined">search_off</span>
                  <p>No ingredients found</p>
                </div>
              ) : (
                ingredients.map((ing) => (
                  <div
                    key={ing.id}
                    className={`ingredient-card ${selectedIngredients.find((s) => s.id === ing.id) ? 'selected' : ''}`}
                    onClick={() => addIngredient(ing)}
                  >
                    <div className="ingredient-card__name">{ing.name}</div>
                    <div className="ingredient-card__meta">{ing.category} • {ing.source}</div>
                    <div className="ingredient-card__macros">
                      <div className="ingredient-macro ingredient-macro--protein">
                        <span className="ingredient-macro__value">{ing.protein_per_100g}g</span>
                        <span className="ingredient-macro__label">P</span>
                      </div>
                      <div className="ingredient-macro ingredient-macro--carbs">
                        <span className="ingredient-macro__value">{ing.carbs_per_100g}g</span>
                        <span className="ingredient-macro__label">C</span>
                      </div>
                      <div className="ingredient-macro ingredient-macro--fats">
                        <span className="ingredient-macro__value">{ing.fats_per_100g}g</span>
                        <span className="ingredient-macro__label">F</span>
                      </div>
                    </div>
                  </div>
                ))
              )
            ) : (
              usdaResults.length === 0 ? (
                <div className="empty-state">
                  <span className="material-icons-outlined">travel_explore</span>
                  <p>{usdaLoading ? 'Searching database...' : 'Search the global food database'}</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                  {usdaResults.map((food, idx) => {
                    const lName = food.name.toLowerCase();
                    const isRaw = lName.includes('raw') || lName.includes('نيء');
                    const isCooked = lName.includes('cooked') || lName.includes('grilled') || lName.includes('boiled') || lName.includes('baked') || lName.includes('مطبوخ') || lName.includes('مشوي');
                    
                    return (
                    <motion.div 
                      key={food.fdc_id || food.name + idx} 
                      className="ingredient-card flex flex-col justify-between"
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.25, delay: Math.min(idx * 0.05, 0.3) }}
                    >
                      <div className="flex justify-between items-start gap-3 mb-4">
                        <div className="flex-1">
                          <div className="flex items-center flex-wrap gap-2 mb-1.5">
                            <div className="ingredient-card__name">
                              {food.name}
                            </div>
                            {isRaw && <span className="state-pill raw">Raw</span>}
                            {isCooked && <span className="state-pill cooked">Cooked</span>}
                          </div>
                          <div className="ingredient-card__meta">
                            {food.category} • {food.source}
                          </div>
                        </div>
                      </div>

                      <div>
                        <div className="ingredient-card__macros mb-4">
                          <div className="ingredient-macro ingredient-macro--protein">
                            <span className="ingredient-macro__value">{food.protein_per_100g || 0}g</span>
                            <span className="ingredient-macro__label">P</span>
                          </div>
                          <div className="ingredient-macro ingredient-macro--carbs">
                            <span className="ingredient-macro__value">{food.carbs_per_100g || 0}g</span>
                            <span className="ingredient-macro__label">C</span>
                          </div>
                          <div className="ingredient-macro ingredient-macro--fats">
                            <span className="ingredient-macro__value">{food.fats_per_100g || 0}g</span>
                            <span className="ingredient-macro__label">F</span>
                          </div>
                        </div>
                        
                        <div className="flex gap-2">
                          <button 
                            className="quick-add-btn flex-1 flex items-center justify-center gap-1 bg-[rgba(57,255,20,0.1)] hover:bg-[rgba(57,255,20,0.2)] text-[var(--primary)] py-2 rounded-lg font-bold text-xs transition-colors" 
                            onClick={() => handleQuickAdd(food)}
                          >
                            <span className="material-icons-outlined" style={{ fontSize: 14 }}>add</span>
                            Quick Add
                          </button>
                          <button 
                            className="usda-save-btn flex items-center justify-center p-2 rounded-lg border border-white/10 hover:bg-white/5 text-[var(--on-surface-variant)] hover:text-[var(--on-surface)] transition-colors" 
                            onClick={() => handleSaveUsda(food)}
                            title="Save to My Foods"
                          >
                            <span className="material-icons-outlined" style={{ fontSize: 16 }}>favorite_border</span>
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  )})}
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
