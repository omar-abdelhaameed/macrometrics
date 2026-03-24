import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { loginUser } from '../api';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../components/ToastProvider';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    if (!email || !password) {
      toast.warning('Please enter both email and password');
      return;
    }
    setLoading(true);
    try {
      const data = await loginUser(email, password);
      login(data.access_token, data.user);
      toast.success('Signed in successfully');
      navigate('/');
    } catch (err) {
      toast.error('Invalid credentials');
    }
    setLoading(false);
  }

  return (
    <motion.div 
      className="auth-page"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
    >
      <div className="auth-card">
        <div className="auth-logo">
          <span className="material-icons-outlined" style={{ fontSize: 42, color: 'var(--primary-container)' }}>
            fitness_center
          </span>
          <h1>MacroMetrics</h1>
          <p>Performance Lab</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <h2>Sign In</h2>
          <p className="auth-subtitle">Track your gains with precision</p>

          <div className="auth-field">
            <label>Email</label>
            <div className="auth-input-wrap">
              <span className="material-icons-outlined">mail</span>
              <input
                type="email"
                placeholder="omar@macrometrics.app"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="auth-field">
            <label>Password</label>
            <div className="auth-input-wrap">
              <span className="material-icons-outlined">lock</span>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button type="submit" className="auth-submit" disabled={loading}>
            {loading ? (
              <span className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} />
            ) : (
              'Sign In'
            )}
          </button>

          <p className="auth-switch">
            Don't have an account? <Link to="/register">Create one</Link>
          </p>

          <div className="auth-demo-hint">
            <span className="material-icons-outlined" style={{ fontSize: 13, marginRight: 4 }}>info</span>
            Demo: omar@macrometrics.app / omar123
          </div>
        </form>
      </div>
    </motion.div>
  );
}
