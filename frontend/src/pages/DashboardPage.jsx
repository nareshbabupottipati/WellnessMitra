import React from 'react';
import { useNavigate } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import './DashboardPage.css';

const NAV_ITEMS = [
  { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
  { icon: '💬', label: 'FitBot',    path: '/chat' },
  { icon: '💪', label: 'Workouts',  path: '/workouts' },
  { icon: '🥗', label: 'Nutrition', path: '/nutrition' },
  { icon: '📍', label: 'Gyms',      path: '/gyms' },
  { icon: '📊', label: 'Progress',  path: '/progress' },
];

export default function DashboardPage() {
  const navigate = useNavigate();
  const userId   = localStorage.getItem('wm_user_id');
  const userName = localStorage.getItem('wm_user_name') || 'User';

  if (!userId) {
    navigate('/');
    return null;
  }

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">🏋️ WellnessMitra</div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map(item => (
            <button key={item.path} className="nav-item" onClick={() => navigate(item.path)}>
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-user">
          <div className="user-avatar-sm">👤</div>
          <div className="user-info">
            <div className="user-name">{userName}</div>
            <div className="user-id">{userId}</div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="dashboard-main">
        <div className="dashboard-header">
          <h1>Welcome back, {userName.split(' ')[0]}! 👋</h1>
          <p className="dashboard-subtitle">Your AI fitness coach is ready to help.</p>
        </div>

        <div className="dashboard-grid">
          {/* Stats row */}
          <div className="stats-row">
            {[
              { label: 'Workout Streak',  value: '5 days',  icon: '🔥' },
              { label: 'Calories Burned', value: '3,600',   icon: '⚡' },
              { label: 'Workouts Done',   value: '12',      icon: '💪' },
              { label: 'BMI Status',      value: 'Normal',  icon: '✅' },
            ].map((stat, i) => (
              <div key={i} className="stat-card">
                <div className="stat-icon">{stat.icon}</div>
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Chat */}
          <div className="chat-section">
            <ChatInterface userId={userId} />
          </div>

          {/* Quick Actions */}
          <div className="quick-actions">
            <h3>Quick Actions</h3>
            {[
              { icon: '💪', label: 'Log Workout',   action: () => navigate('/workouts') },
              { icon: '🥗', label: 'Log Meal',      action: () => navigate('/nutrition') },
              { icon: '⚖️', label: 'Log Weight',    action: () => navigate('/progress') },
              { icon: '📍', label: 'Find Gyms',     action: () => navigate('/gyms') },
            ].map((qa, i) => (
              <button key={i} className="quick-action-btn" onClick={qa.action}>
                <span>{qa.icon}</span> {qa.label}
              </button>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
