import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from '../components/ToastProvider';
import {
  fetchSupplements,
  fetchSupplementCategories,
  fetchRecommendations,
  fetchMyStack,
  addToStack,
  removeFromStack,
  logSupplement,
} from '../api';

const categoryIcons = {
  'Protein': 'fitness_center',
  'Vitamin': 'medication',
  'Mineral': 'diamond',
  'Fatty Acid': 'water_drop',
  'Amino Acid': 'science',
  'Stimulant': 'bolt',
  'Herb': 'eco',
};

const TIME_OF_DAY_OPTIONS = [
  { value: 'morning', label: 'Morning', icon: 'wb_sunny' },
  { value: 'afternoon', label: 'Afternoon', icon: 'light_mode' },
  { value: 'evening', label: 'Evening', icon: 'wb_twilight' },
  { value: 'pre_workout', label: 'Pre-Workout', icon: 'fitness_center' },
  { value: 'post_workout', label: 'Post-Workout', icon: 'sports_gymnastics' },
  { value: 'night', label: 'Night', icon: 'bedtime' },
  { value: 'with_meal', label: 'With Meal', icon: 'restaurant' },
  { value: 'before_sleep', label: 'Before Sleep', icon: 'nightlight' },
];

export default function Supplements() {
  const [supplements, setSupplements] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [myStack, setMyStack] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [selectedSupplement, setSelectedSupplement] = useState(null);
  const [customDosage, setCustomDosage] = useState('');
  const [selectedTime, setSelectedTime] = useState('morning');
  const [activeTab, setActiveTab] = useState('stack'); // 'stack' or 'catalog'
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [supps, cats, recs, stack] = await Promise.all([
        fetchSupplements(),
        fetchSupplementCategories(),
        fetchRecommendations(),
        fetchMyStack(),
      ]);
      setSupplements(supps);
      setCategories(cats.categories || []);
      setRecommendations(recs);
      setMyStack(stack);
    } catch (err) {
      toast.error('Failed to load supplements');
    } finally {
      setLoading(false);
    }
  }

  async function handleAddToStack(supplement) {
    try {
      const dosage = customDosage || supplement.standard_dosage;
      await addToStack({
        supplement_id: supplement.id,
        custom_dosage_amount: dosage,
        time_of_day: selectedTime,
      });
      toast.success(`${supplement.name} added to your stack!`);
      setShowAddModal(false);
      setSelectedSupplement(null);
      setCustomDosage('');
      loadData();
    } catch (err) {
      if (err.message.includes('already')) {
        toast.warning('Supplement already in your stack');
      } else {
        toast.error('Failed to add supplement');
      }
    }
  }

  async function handleRemoveFromStack(stackItemId) {
    try {
      await removeFromStack(stackItemId);
      toast.info('Supplement removed from stack');
      loadData();
    } catch (err) {
      toast.error('Failed to remove supplement');
    }
  }

  async function handleToggleTaken(stackItem) {
    try {
      await logSupplement(stackItem.id);
      loadData();
    } catch (err) {
      toast.error('Failed to log supplement');
    }
  }

  function openAddModal(supplement) {
    setSelectedSupplement(supplement);
    setCustomDosage(supplement.standard_dosage.toString());
    setShowAddModal(true);
  }

  const checkedCount = myStack.filter(s => s.taken_today).length;
  const filteredSupplements = selectedCategory
    ? supplements.filter(s => s.category === selectedCategory)
    : supplements;

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
    >
      <div className="page-header">
        <div className="page-header-row">
          <div>
            <h2>Supplement Stack</h2>
            <p>Your personalized daily vitamin tracker</p>
          </div>
          <button 
            onClick={() => setShowRecommendations(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[var(--secondary-container)] text-[var(--on-secondary)] font-medium text-sm hover:bg-[var(--secondary-fixed-dim)]"
          >
            <span className="material-icons-outlined text-sm">auto_awesome</span>
            AI Recommendations
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-6 p-4 rounded-xl bg-[var(--surface-container)]">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-[var(--on-surface-variant)]">Today's Progress</span>
          <span className="font-semibold text-[var(--primary-container)]">{checkedCount}/{myStack.length}</span>
        </div>
        <div className="h-2 bg-[var(--surface-container-high)] rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-[var(--primary-container)]"
            initial={{ width: 0 }}
            animate={{ width: myStack.length > 0 ? `${(checkedCount / myStack.length) * 100}%` : '0%' }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Tab Switcher */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('stack')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeTab === 'stack'
              ? 'bg-[var(--primary-container)] text-[var(--surface)]'
              : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
          }`}
        >
          My Stack ({myStack.length})
        </button>
        <button
          onClick={() => setActiveTab('catalog')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            activeTab === 'catalog'
              ? 'bg-[var(--primary-container)] text-[var(--surface)]'
              : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
          }`}
        >
          Catalog ({supplements.length})
        </button>
      </div>

      {/* My Stack Tab */}
      {activeTab === 'stack' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {myStack.map((item, i) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className={`card cursor-pointer transition-all ${
                item.taken_today 
                  ? 'border-[var(--primary-container)]/50 bg-[var(--primary-container)]/5' 
                  : 'hover:border-[var(--surface-container-highest)]'
              }`}
              onClick={() => handleToggleTaken(item)}
            >
              <div className="flex items-start gap-4">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${
                  item.taken_today
                    ? 'bg-[var(--primary-container)]'
                    : 'bg-[var(--surface-container-high)]'
                }`}>
                  <span className={`material-icons-outlined ${
                    item.taken_today ? 'text-[var(--surface)]' : 'text-[var(--on-surface-variant)]'
                  }`}>
                    {categoryIcons[item.supplement.category] || 'medication'}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-[var(--on-surface)] truncate">{item.supplement.name}</h3>
                    {item.taken_today && (
                      <span className="material-icons-outlined text-[var(--primary-container)] text-sm">check_circle</span>
                    )}
                  </div>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--surface-container-high)] text-[var(--on-surface-variant)]">
                      {item.time_of_day.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="text-sm text-[var(--primary-container)] mt-2 font-medium">
                    {item.custom_dosage_amount} {item.supplement.unit}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                    item.taken_today
                      ? 'bg-[var(--primary-container)] border-[var(--primary-container)]'
                      : 'border-[var(--outline)]'
                  }`}>
                    {item.taken_today && (
                      <span className="material-icons-outlined text-[var(--surface)] text-sm">check</span>
                    )}
                  </div>
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleRemoveFromStack(item.id); }}
                    className="text-[var(--error)] hover:bg-[var(--error)]/10 p-1 rounded"
                  >
                    <span className="material-icons-outlined text-sm">delete</span>
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
          
          {myStack.length === 0 && (
            <div className="col-span-full text-center py-12">
              <span className="material-icons-outlined text-4xl text-[var(--on-surface-variant)] mb-2">medication</span>
              <p className="text-[var(--on-surface-variant)]">Your stack is empty</p>
              <button
                onClick={() => setActiveTab('catalog')}
                className="mt-4 px-4 py-2 rounded-xl bg-[var(--primary-container)] text-[var(--surface)]"
              >
                Browse Catalog
              </button>
            </div>
          )}
        </div>
      )}

      {/* Catalog Tab */}
      {activeTab === 'catalog' && (
        <>
          {/* Category Filter */}
          <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                !selectedCategory
                  ? 'bg-[var(--primary-container)] text-[var(--surface)]'
                  : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
              }`}
            >
              All ({supplements.length})
            </button>
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                  selectedCategory === cat
                    ? 'bg-[var(--primary-container)] text-[var(--surface)]'
                    : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Supplements Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredSupplements.map((supp, i) => {
              const inStack = myStack.some(s => s.supplement.id === supp.id);
              return (
                <motion.div
                  key={supp.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="card"
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 bg-[var(--surface-container-high)]">
                      <span className="material-icons-outlined text-[var(--on-surface-variant)]">
                        {categoryIcons[supp.category] || 'medication'}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-[var(--on-surface)] truncate">{supp.name}</h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--surface-container-high)] text-[var(--on-surface-variant)]">
                          {supp.category}
                        </span>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--secondary-container)]/30 text-[var(--secondary)]">
                          {supp.target_goal}
                        </span>
                      </div>
                      <p className="text-sm text-[var(--primary-container)] mt-2 font-medium">
                        {supp.standard_dosage} {supp.unit}
                      </p>
                    </div>
                    <button
                      onClick={() => openAddModal(supp)}
                      disabled={inStack}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                        inStack
                          ? 'bg-[var(--surface-container-high)] text-[var(--on-surface-variant)] cursor-not-allowed'
                          : 'bg-[var(--primary-container)] text-[var(--surface)] hover:bg-[var(--primary-fixed-dim)]'
                      }`}
                    >
                      {inStack ? 'Added' : 'Add +'}
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </>
      )}

      {/* AI Recommendations Modal */}
      <AnimatePresence>
        {showRecommendations && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setShowRecommendations(false)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="bg-[var(--surface-container)] rounded-2xl p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-[var(--secondary-container)] flex items-center justify-center">
                    <span className="material-icons-outlined text-[var(--on-secondary)]">auto_awesome</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-[var(--on-surface)]">AI Recommendations</h3>
                    <p className="text-sm text-[var(--on-surface-variant)]">Based on your goals & activity</p>
                  </div>
                </div>
                <button onClick={() => setShowRecommendations(false)} className="p-2 hover:bg-[var(--surface)] rounded-lg">
                  <span className="material-icons-outlined">close</span>
                </button>
              </div>

              <div className="space-y-4">
                {recommendations.map((rec, i) => {
                  const inStack = myStack.some(s => s.supplement.id === rec.id);
                  return (
                    <motion.div
                      key={rec.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="p-4 rounded-xl bg-[var(--surface)] border border-[var(--surface-container-high)]"
                    >
                      <div className="flex items-start gap-4">
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-[var(--secondary-container)]/30 flex-shrink-0">
                          <span className="material-icons-outlined text-[var(--secondary)]">
                            {categoryIcons[rec.category] || 'medication'}
                          </span>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <h4 className="font-semibold text-[var(--on-surface)]">{rec.name}</h4>
                            <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--primary-container)]/20 text-[var(--primary-container)]">
                              Priority {rec.priority}
                            </span>
                          </div>
                          <p className="text-sm text-[var(--on-surface-variant)] mt-1">{rec.reason}</p>
                          <p className="text-sm text-[var(--primary-container)] mt-2 font-medium">
                            {rec.standard_dosage} {rec.unit}
                          </p>
                        </div>
                        <button
                          onClick={() => {
                            openAddModal(rec);
                            setShowRecommendations(false);
                          }}
                          disabled={inStack}
                          className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                            inStack
                              ? 'bg-[var(--surface-container-high)] text-[var(--on-surface-variant)]'
                              : 'bg-[var(--primary-container)] text-[var(--surface)]'
                          }`}
                        >
                          {inStack ? 'Added' : 'Add'}
                        </button>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Add to Stack Modal */}
      <AnimatePresence>
        {showAddModal && selectedSupplement && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setShowAddModal(false)}
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="bg-[var(--surface-container)] rounded-2xl p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-semibold text-[var(--on-surface)] mb-4">
                Add {selectedSupplement.name}
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-[var(--on-surface-variant)] mb-2">Dosage ({selectedSupplement.unit})</label>
                  <input
                    type="number"
                    value={customDosage}
                    onChange={(e) => setCustomDosage(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface)] border border-[var(--surface-container-high)] focus:border-[var(--primary-container)] outline-none"
                    placeholder={selectedSupplement.standard_dosage}
                  />
                </div>

                <div>
                  <label className="block text-sm text-[var(--on-surface-variant)] mb-2">Time of Day</label>
                  <div className="grid grid-cols-2 gap-2">
                    {TIME_OF_DAY_OPTIONS.map(option => (
                      <button
                        key={option.value}
                        onClick={() => setSelectedTime(option.value)}
                        className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                          selectedTime === option.value
                            ? 'bg-[var(--primary-container)] text-[var(--surface)]'
                            : 'bg-[var(--surface)] text-[var(--on-surface-variant)]'
                        }`}
                      >
                        <span className="material-icons-outlined text-sm">{option.icon}</span>
                        {option.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface-variant)] font-medium hover:bg-[var(--surface-container-high)]"
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleAddToStack(selectedSupplement)}
                  className="flex-1 px-4 py-3 rounded-xl bg-[var(--primary-container)] text-[var(--surface)] font-medium hover:bg-[var(--primary-fixed-dim)]"
                >
                  Add to Stack
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
