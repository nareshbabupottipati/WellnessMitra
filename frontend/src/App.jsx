import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import OnboardingPage from './pages/OnboardingPage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function ProtectedRoute({ children }) {
  const userId = localStorage.getItem('wm_user_id');
  return userId ? children : <Navigate to="/" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"          element={<OnboardingPage />} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/chat"      element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/workouts"  element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/nutrition" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/gyms"      element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/progress"  element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="*"          element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
