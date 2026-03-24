import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchSupplements, fetchSupplementCategories, fetchWeightPlateau } from '../api';
import { useToast } from '../components/ToastProvider';

const categoryIcons = {
  'Performance': 'speed',
  'Protein': 'fitness_center',
  'Vitamins': 'medication',
  'Healthy Fats': 'water_drop',
  'Minerals': 'diamond',
  'Amino Acids': 'science',
};

const DOSAGE_UNITS = ['Tablets', 'Grams', 'Scoops'];

export default function Supplements() {
  const [supplements, setSupplements] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [checkedSupplements, setCheckedSupplements] = useState({});
  const [customSupplements, setCustomSupplements] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSupplement, setNewSupplement] = useState({ name: '', dosage: '', unit: 'Tablets' });
  const [plateau, setPlateau] = useState(null);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    const savedCustom = localStorage.getItem('customSupplements');
    if (savedCustom) {
      setCustomSupplements(JSON.parse(savedCustom));
    }
    
    const today = new Date().toISOString().split('T')[0];
    const lastReset = localStorage.getItem('supplementsLastReset');
    
    if (lastReset !== today) {
      setCheckedSupplements({});
      localStorage.setItem('supplementsLastReset', today);
    } else {
      const saved = localStorage.getItem('checkedSupplements');
      if (saved) {
        setCheckedSupplements(JSON.parse(saved));
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('checkedSupplements', JSON.stringify(checkedSupplements));
  }, [checkedSupplements]);

  useEffect(() => {
    localStorage.setItem('customSupplements', JSON.stringify(customSupplements));
  }, [customSupplements]);

  useEffect(() => {
    Promise.all([
      fetchSupplements(),
      fetchSupplementCategories(),
      fetchWeightPlateau(7).catch(() => ({ is_plateau: false }))
    ]).then(([supps, cats, plateauData]) => {
      setSupplements(supps);
      setCategories(cats.categories || []);
      setPlateau(plateauData);
      setLoading(false);
    }).catch(err => {
      toast.error('Failed to load supplements');
      setLoading(false);
    });
  }, []);

  function toggleCheck(id) {
    const newState = { ...checkedSupplements, [id]: !checkedSupplements[id] };
    setCheckedSupplements(newState);
  }

  function handleAddCustomSupplement() {
    if (!newSupplement.name || !newSupplement.dosage) {
      toast.warning('Please enter name and dosage');
      return;
    }
    
    const custom = {
      id: Date.now(),
      name: newSupplement.name,
      default_daily_dose: `${newSupplement.dosage} ${newSupplement.unit}`,
      category: 'Custom',
      isCustom: true
    };
    
    setCustomSupplements([...customSupplements, custom]);
    setNewSupplement({ name: '', dosage: '', unit: 'Tablets' });
    setShowAddForm(false);
    toast.success(`${custom.name} added to your cabinet!`);
  }

  function handleDeleteCustom(id) {
    setCustomSupplements(customSupplements.filter(s => s.id !== id));
    const newChecked = { ...checkedSupplements };
    delete newChecked[id];
    setCheckedSupplements(newChecked);
    toast.info('Supplement removed');
  }

  const allSupplements = [...supplements, ...customSupplements];
  
  const filteredSupplements = selectedCategory
    ? allSupplements.filter(s => s.category === selectedCategory)
    : allSupplements;

  const checkedCount = Object.values(checkedSupplements).filter(Boolean).length;

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
            <h2>Supplement Cabinet</h2>
            <p>Your personalized daily supplement tracker</p>
          </div>
          <button 
            onClick={() => setShowAddForm(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[var(--primary-container)] text-[var(--surface)] font-medium text-sm hover:bg-[var(--primary-fixed-dim)]"
          >
            <span className="material-icons-outlined text-sm">add</span>
            Add Custom
          </button>
        </div>
      </div>

      {/* Refeed Alert */}
      {plateau?.is_plateau && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 rounded-xl bg-[var(--secondary-container)]/10 border border-[var(--secondary-container)]/30"
        >
          <div className="flex items-start gap-3">
            <span className="material-icons-outlined text-[var(--secondary-container)]">trending_up</span>
            <div>
              <h4 className="font-semibold text-[var(--on-surface)]">Plateau Detected</h4>
              <p className="text-sm text-[var(--on-surface-variant)] mt-1">
                {plateau.suggestion}
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Progress Bar */}
      <div className="mb-6 p-4 rounded-xl bg-[var(--surface-container)]">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-[var(--on-surface-variant)]">Daily Progress</span>
          <span className="font-semibold text-[var(--primary-container)]">{checkedCount}/{allSupplements.length}</span>
        </div>
        <div className="h-2 bg-[var(--surface-container-high)] rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-[var(--primary-container)]"
            initial={{ width: 0 }}
            animate={{ width: `${(checkedCount / allSupplements.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button
          onClick={() => setSelectedCategory(null)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
            !selectedCategory
              ? 'bg-[var(--primary-container)] text-[var(--surface)]'
              : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)] hover:text-[var(--on-surface)]'
          }`}
        >
          All ({allSupplements.length})
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
              selectedCategory === cat
                ? 'bg-[var(--primary-container)] text-[var(--surface)]'
                : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)] hover:text-[var(--on-surface)]'
            }`}
          >
            {cat} ({supplements.filter(s => s.category === cat).length})
          </button>
        ))}
        {customSupplements.length > 0 && (
          <button
            onClick={() => setSelectedCategory('Custom')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
              selectedCategory === 'Custom'
                ? 'bg-[var(--primary-container)] text-[var(--surface)]'
                : 'bg-[var(--surface-container)] text-[var(--on-surface-variant)] hover:text-[var(--on-surface)]'
            }`}
          >
            Custom ({customSupplements.length})
          </button>
        )}
      </div>

      {/* Supplements Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredSupplements.map((supp, i) => (
          <motion.div
            key={supp.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className={`card cursor-pointer transition-all ${
              checkedSupplements[supp.id] 
                ? 'border-[var(--primary-container)]/50 bg-[var(--primary-container)]/5' 
                : 'hover:border-[var(--surface-container-highest)]'
            }`}
            onClick={() => toggleCheck(supp.id)}
          >
            <div className="flex items-start gap-4">
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${
                checkedSupplements[supp.id]
                  ? 'bg-[var(--primary-container)]'
                  : 'bg-[var(--surface-container-high)]'
              }`}>
                <span className={`material-icons-outlined ${
                  checkedSupplements[supp.id] ? 'text-[var(--surface)]' : 'text-[var(--on-surface-variant)]'
                }`}>
                  {supp.isCustom ? 'add_circle' : (categoryIcons[supp.category] || 'medication')}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-[var(--on-surface)] truncate">{supp.name}</h3>
                  {checkedSupplements[supp.id] && (
                    <span className="material-icons-outlined text-[var(--primary-container)] text-sm">check_circle</span>
                  )}
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--surface-container-high)] text-[var(--on-surface-variant)]">
                    {supp.category}
                  </span>
                </div>
                <p className="text-sm text-[var(--primary-container)] mt-2 font-medium">
                  {supp.default_daily_dose}
                </p>
              </div>
              <div className="flex flex-col items-end gap-2">
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                  checkedSupplements[supp.id]
                    ? 'bg-[var(--primary-container)] border-[var(--primary-container)]'
                    : 'border-[var(--outline)]'
                }`}>
                  {checkedSupplements[supp.id] && (
                    <span className="material-icons-outlined text-[var(--surface)] text-sm">check</span>
                  )}
                </div>
                {supp.isCustom && (
                  <button 
                    onClick={(e) => { e.stopPropagation(); handleDeleteCustom(supp.id); }}
                    className="text-[var(--error)] hover:bg-[var(--error)]/10 p-1 rounded"
                  >
                    <span className="material-icons-outlined text-sm">delete</span>
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {filteredSupplements.length === 0 && (
        <div className="text-center py-12">
          <span className="material-icons-outlined text-4xl text-[var(--on-surface-variant)] mb-2">medication</span>
          <p className="text-[var(--on-surface-variant)]">No supplements found</p>
        </div>
      )}

      {/* Add Custom Supplement Modal */}
      <AnimatePresence>
        {showAddForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setShowAddForm(false)}
          >
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.9 }}
              className="bg-[var(--surface-container)] rounded-2xl p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-semibold text-[var(--on-surface)] mb-4">Add Custom Supplement</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-[var(--on-surface-variant)] mb-2">Supplement Name</label>
                  <input
                    type="text"
                    placeholder="e.g., Ashwagandha"
                    value={newSupplement.name}
                    onChange={(e) => setNewSupplement({ ...newSupplement, name: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface)] border border-[var(--surface-container-high)] focus:border-[var(--primary-container)] outline-none"
                  />
                </div>
                
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="block text-sm text-[var(--on-surface-variant)] mb-2">Dosage</label>
                    <input
                      type="number"
                      placeholder="e.g., 300"
                      value={newSupplement.dosage}
                      onChange={(e) => setNewSupplement({ ...newSupplement, dosage: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface)] border border-[var(--surface-container-high)] focus:border-[var(--primary-container)] outline-none"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm text-[var(--on-surface-variant)] mb-2">Unit</label>
                    <select
                      value={newSupplement.unit}
                      onChange={(e) => setNewSupplement({ ...newSupplement, unit: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface)] border border-[var(--surface-container-high)] focus:border-[var(--primary-container)] outline-none"
                    >
                      {DOSAGE_UNITS.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setShowAddForm(false)}
                  className="flex-1 px-4 py-3 rounded-xl bg-[var(--surface)] text-[var(--on-surface-variant)] font-medium hover:bg-[var(--surface-container-high)]"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAddCustomSupplement}
                  className="flex-1 px-4 py-3 rounded-xl bg-[var(--primary-container)] text-[var(--surface)] font-medium hover:bg-[var(--primary-fixed-dim)]"
                >
                  Add
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}