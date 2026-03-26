import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { ToastProvider } from './components/ToastProvider';
import Sidebar from './components/Sidebar';
import AIChat from './components/AIChat';
import Dashboard from './pages/Dashboard';
import MealLogger from './pages/MealLogger';
import Supplements from './pages/Supplements';
import Analytics from './pages/Analytics';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Premium from './pages/Premium';
import Login from './pages/Login';
import Register from './pages/Register';
import './index.css';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}

function AuthRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) return <Navigate to="/" replace />;
  return children;
}

function AppLayout() {
  const [isSidebarExpanded, setIsSidebarExpanded] = React.useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);
  const [windowWidth, setWindowWidth] = React.useState(
    typeof window !== 'undefined' ? window.innerWidth : 1024
  );

  React.useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const isMobile = windowWidth < 768;

  return (
    <div className="min-h-screen bg-[var(--surface)]">
      {/* Mobile hamburger button */}
      <button
        className={`fixed top-4 left-4 z-[65] p-2 rounded-lg bg-[var(--surface-container)] text-[var(--on-surface)] lg:hidden ${isMobileMenuOpen ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
        onClick={() => setIsMobileMenuOpen(true)}
      >
        <span className="material-icons-outlined">menu</span>
      </button>

      <Sidebar 
        isExpanded={isSidebarExpanded} 
        setIsExpanded={setIsSidebarExpanded}
        isMobileMenuOpen={isMobileMenuOpen}
        setIsMobileMenuOpen={setIsMobileMenuOpen}
        isMobile={isMobile}
      />
      
      <main 
        className="p-4 md:p-8 min-h-screen transition-all duration-300 ease-in-out"
        style={{ 
          paddingLeft: isMobile 
            ? '0px' 
            : (isSidebarExpanded ? '280px' : '100px'),
          paddingTop: isMobile ? '60px' : '32px'
        }}
      >
        <Routes>
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/log" element={<ProtectedRoute><MealLogger /></ProtectedRoute>} />
          <Route path="/supplements" element={<ProtectedRoute><Supplements /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
          <Route path="/premium" element={<ProtectedRoute><Premium /></ProtectedRoute>} />
        </Routes>
      </main>
      <AIChat />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<AuthRoute><Login /></AuthRoute>} />
              <Route path="/register" element={<AuthRoute><Register /></AuthRoute>} />
              <Route path="/*" element={<AppLayout />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;