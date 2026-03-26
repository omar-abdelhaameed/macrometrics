import React from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';

const PLANS = {
  free: {
    name: 'Free',
    price: '$0',
    period: '/month',
    description: 'Essential tracking for beginners',
    features: [
      { text: 'Basic macro tracking', included: true },
      { text: 'Manual food logging', included: true },
      { text: 'Daily summary dashboard', included: true },
      { text: 'One meal type per day', included: true },
      { text: 'Basic analytics (7-day)', included: true },
      { text: 'Golden Foods database', included: true },
      { text: 'AI Coach ', included: false },
      { text: 'USDA database (900k+ foods)', included: false },
      { text: 'Advanced analytics (30-day+)', included: false },
      { text: 'Supplement tracking', included: false },
      { text: 'AI supplement recommendations', included: false },
      { text: 'Priority support', included: false },
    ],
  },
  premium: {
    name: 'Premium',
    price: '$10',
    period: '/month',
    description: 'Elite performance for serious athletes',
    popular: true,
    features: [
      { text: 'Basic macro tracking', included: true },
      { text: 'Manual food logging', included: true },
      { text: 'Daily summary dashboard', included: true },
      { text: 'One meal type per day', included: true },
      { text: 'Basic analytics (7-day)', included: true },
      { text: 'Golden Foods database', included: true },
      { text: 'AI Coach (Gemini)', included: true },
      { text: 'USDA database (900k+ foods)', included: true },
      { text: 'Advanced analytics (30-day+)', included: true },
      { text: 'Supplement tracking', included: true },
      { text: 'AI supplement recommendations', included: true },
      { text: 'Priority support', included: true },
    ],
  },
};

function FeatureRow({ feature }) {
  return (
    <div className="premium-feature-row">
      <span className={`material-icons-outlined premium-feature-icon ${feature.included ? 'included' : 'excluded'}`}>
        {feature.included ? 'check_circle' : 'cancel'}
      </span>
      <span className={`premium-feature-text ${feature.included ? 'included' : 'excluded'}`}>
        {feature.text}
      </span>
    </div>
  );
}

function PlanCard({ plan, isCurrentUserPro }) {
  const isPremium = plan.name === 'Premium';
  
  return (
    <motion.div 
      className={`premium-plan-card ${isPremium ? 'premium-plan-card--featured' : ''} ${isCurrentUserPro && isPremium ? 'premium-plan-card--current' : ''}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {isPremium && plan.popular && (
        <div className="premium-plan-badge">Most Popular</div>
      )}
      
      <div className="premium-plan-header">
        <h3 className="premium-plan-name">{plan.name}</h3>
        <div className="premium-plan-price">
          <span className="premium-plan-amount">{plan.price}</span>
          <span className="premium-plan-period">{plan.period}</span>
        </div>
        <p className="premium-plan-desc">{plan.description}</p>
      </div>
      
      <div className="premium-plan-features">
        {plan.features.map((feature, idx) => (
          <FeatureRow key={idx} feature={feature} />
        ))}
      </div>
      
      <div className="premium-plan-cta">
        {isPremium ? (
          <div className="premium-coming-soon">
            <span className="material-icons-outlined">schedule</span>
            <span>Coming Soon</span>
          </div>
        ) : (
          <div className="premium-current-plan">
            Current Plan
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default function Premium() {
  const { user } = useAuth();
  
  return (
    <motion.div 
      className="premium-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="premium-hero">
        <motion.h1 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          Upgrade to <span className="premium-highlight">Premium</span>
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          Unlock your full potential with elite features designed for serious athletes
        </motion.p>
      </div>
      
      <div className="premium-plans-grid">
        <PlanCard plan={PLANS.free} isCurrentUserPro={user?.is_pro_user} />
        <PlanCard plan={PLANS.premium} isCurrentUserPro={user?.is_pro_user} />
      </div>
      
      <motion.div 
        className="premium-footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <p>All plans include our core nutrition engine with clinical-grade macro calculations</p>
      </motion.div>
    </motion.div>
  );
}