import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import {
  getMealPlan,
  getNearbyGyms,
  getProgressSummary,
  getUserProfile,
  getWorkoutLogs,
  logWeight,
  logWorkout,
} from '../services/api';
import './DashboardPage.css';

function bmiLabel(bmi) {
  if (bmi == null) return '—';
  if (bmi < 18.5) return 'Low';
  if (bmi < 25) return 'Normal';
  if (bmi < 30) return 'Over';
  return 'High';
}

const NAV_ITEMS = [
  { icon: '🏠', label: 'Dashboard', path: '/dashboard' },
  { icon: '💬', label: 'FitBot',    path: '/chat' },
  { icon: '💪', label: 'Workouts',  path: '/workouts' },
  { icon: '🥗', label: 'Nutrition', path: '/nutrition' },
  { icon: '📍', label: 'Gyms',      path: '/gyms' },
  { icon: '📊', label: 'Progress',  path: '/progress' },
];

const PAGE_COPY = {
  '/dashboard': ['Welcome back', 'Your AI fitness coach is ready to help.'],
  '/chat': ['FitBot', 'Ask for a workout, a meal plan, or a wellness tip.'],
  '/workouts': ['Workouts', 'Log a session. It is saved with your profile.'],
  '/nutrition': ['Nutrition', 'Build a meal plan from your saved profile.'],
  '/gyms': ['Nearby gyms', 'Places from OpenStreetMap around your city.'],
  '/progress': ['Progress', 'Log your weight and review the last 30 days.'],
};

const ACTIVITIES = [
  { name: 'Squat', kind: 'strength', sets: 3, reps: '12', weight: 0, duration: 12, calories: 90 },
  { name: 'Push-up', kind: 'strength', sets: 3, reps: '10', weight: 0, duration: 8, calories: 50 },
  { name: 'Lunges', kind: 'strength', sets: 3, reps: '10 each', weight: 0, duration: 10, calories: 70 },
  { name: 'Deadlift', kind: 'strength', sets: 3, reps: '8', weight: 20, duration: 12, calories: 110 },
  { name: 'Plank', kind: 'strength', sets: 3, reps: '40 sec', weight: 0, duration: 6, calories: 25 },
  { name: 'Running', kind: 'cardio', duration: 30, distance: 4, calories: 300 },
  { name: 'Cycling', kind: 'cardio', duration: 40, distance: 12, calories: 320 },
  { name: 'Brisk walk', kind: 'cardio', duration: 30, distance: 2.5, calories: 140 },
  { name: 'Jump rope', kind: 'cardio', duration: 15, distance: 1, calories: 180 },
  { name: 'Yoga', kind: 'flexibility', duration: 30, calories: 120 },
  { name: 'Stretching', kind: 'flexibility', duration: 15, calories: 50 },
];

function activityByName(name) {
  return { ...(ACTIVITIES.find(item => item.name === name) || ACTIVITIES[0]) };
}

function WorkoutPanel({ userId }) {
  const [logs, setLogs] = useState([]);
  const [form, setForm] = useState(() => activityByName('Squat'));
  const [status, setStatus] = useState('');

  const refresh = () => getWorkoutLogs(userId).then(data => setLogs(data.logs || [])).catch(() => setLogs([]));
  useEffect(() => { refresh(); }, [userId]);

  const chooseActivity = (name) => setForm(activityByName(name));

  const submit = async (event) => {
    event.preventDefault();
    setStatus('');
    const reps = form.kind === 'strength'
      ? String(form.reps)
      : form.kind === 'cardio'
        ? `${form.distance} km`
        : `${form.duration} min`;
    try {
      await logWorkout({
        user_id: userId,
        exercises: [{
          name: form.name,
          sets: form.kind === 'strength' ? Number(form.sets) : 1,
          reps,
          weight_kg: form.kind === 'strength' ? Number(form.weight) : null,
        }],
        duration_mins: Number(form.duration),
        calories_burned: Number(form.calories),
      });
      setStatus('Workout saved.');
      refresh();
    } catch {
      setStatus('Could not save the workout.');
    }
  };

  return (
    <section className="panel">
      <h2>Log a workout</h2>
      <form onSubmit={submit}>
        <label>
          Activity
          <select value={form.name} onChange={e => chooseActivity(e.target.value)}>
            <optgroup label="Strength">
              {ACTIVITIES.filter(item => item.kind === 'strength').map(item => (
                <option key={item.name}>{item.name}</option>
              ))}
            </optgroup>
            <optgroup label="Cardio">
              {ACTIVITIES.filter(item => item.kind === 'cardio').map(item => (
                <option key={item.name}>{item.name}</option>
              ))}
            </optgroup>
            <optgroup label="Flexibility">
              {ACTIVITIES.filter(item => item.kind === 'flexibility').map(item => (
                <option key={item.name}>{item.name}</option>
              ))}
            </optgroup>
          </select>
        </label>
        {form.kind === 'strength' && (
          <>
            <label>Sets<input type="number" min="1" value={form.sets} onChange={e => setForm({ ...form, sets: e.target.value })} /></label>
            <label>Reps<input value={form.reps} onChange={e => setForm({ ...form, reps: e.target.value })} /></label>
            <label>Weight (kg)<input type="number" min="0" step="0.5" value={form.weight} onChange={e => setForm({ ...form, weight: e.target.value })} /></label>
          </>
        )}
        {form.kind === 'cardio' && (
          <label>Distance (km)<input type="number" min="0" step="0.1" value={form.distance} onChange={e => setForm({ ...form, distance: e.target.value })} /></label>
        )}
        <label>Minutes<input type="number" min="1" value={form.duration} onChange={e => setForm({ ...form, duration: e.target.value })} /></label>
        <label>Calories<input type="number" min="0" value={form.calories} onChange={e => setForm({ ...form, calories: e.target.value })} /></label>
        <button className="primary" type="submit">Save workout</button>
      </form>
      {status && <p className="hint">{status}</p>}
      <div className="entry-list">
        {logs.length === 0 && <p className="hint">No workouts logged yet.</p>}
        {logs.map(log => (
          <div key={log.id} className="entry">
            {log.date} · {(log.exercises || []).map(item => item.name).join(', ') || 'Workout'} · {log.duration_mins} min · {log.calories_burned} kcal
          </div>
        ))}
      </div>
    </section>
  );
}

function NutritionPanel({ userId }) {
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getMealPlan(userId).then(setPlan).catch(() => setError('Could not load the meal plan.'));
  }, [userId]);

  return (
    <section className="panel">
      <h2>Today’s meals</h2>
      {plan && <p className="hint">🎯 {plan.calories} kcal · {plan.dietary_pref}</p>}
      {error && <p className="hint">{error}</p>}
      <div className="meal-grid">
        {(plan?.meals || []).map(meal => (
          <article key={meal.name} className="meal-card">
            <div className="meal-icon">{meal.icon}</div>
            <div>
              <div className="meal-title"><strong>{meal.name}</strong><span>{meal.kcal} kcal</span></div>
              <p>{meal.items}</p>
            </div>
          </article>
        ))}
      </div>
      {plan && <p className="hint">{plan.water}</p>}
    </section>
  );
}

function GymPanel({ userId }) {
  const [gyms, setGyms] = useState(null);
  const [location, setLocation] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    setGyms(null);
    setError('');
    getNearbyGyms(userId)
      .then(data => {
        setLocation(data.location || '');
        setGyms(data.gyms || []);
      })
      .catch(err => setError(err.response?.data?.detail || 'Could not load gyms.'));
  }, [userId]);

  return (
    <section className="panel">
      <h2>{gyms ? `${gyms.length} gyms` : 'Gyms'} near {location || 'you'}</h2>
      {gyms === null && !error && <p className="hint">Searching OpenStreetMap…</p>}
      {error && <p className="hint">{error}</p>}
      <div className="entry-list">
        {gyms && gyms.length === 0 && <p className="hint">No gyms found for this location.</p>}
        {(gyms || []).map((gym, index) => (
          <div key={`${gym.name}-${index}`} className="entry">
            <strong>{gym.name}</strong>
            <div>📍 {gym.address}{gym.distance_km != null ? ` · ${gym.distance_km} km` : ''}</div>
            <a href={gym.maps_url} target="_blank" rel="noreferrer">Open in OpenStreetMap</a>
          </div>
        ))}
      </div>
    </section>
  );
}

function ProgressPanel({ userId, onChange }) {
  const [weight, setWeight] = useState('');
  const [summary, setSummary] = useState(null);
  const [status, setStatus] = useState('');

  const refresh = () => getProgressSummary(userId).then(setSummary).catch(() => setSummary(null));
  useEffect(() => { refresh(); }, [userId]);

  const submit = async (event) => {
    event.preventDefault();
    setStatus('');
    try {
      await logWeight(userId, Number(weight));
      setWeight('');
      setStatus('Weight saved.');
      refresh();
      onChange();
    } catch {
      setStatus('Could not save weight.');
    }
  };

  return (
    <section className="panel">
      <h2>Weight log</h2>
      <form onSubmit={submit}>
        <input type="number" step="0.1" value={weight} onChange={e => setWeight(e.target.value)} placeholder="Weight (kg)" required />
        <button className="primary" type="submit">Save weight</button>
      </form>
      {status && <p className="hint">{status}</p>}
      {summary && (
        <div className="entry-list">
          <div className="entry">Current {summary.weight_current_kg} kg · change {summary.weight_change_kg} kg · BMI {summary.current_bmi}</div>
          <div className="entry">{summary.total_workouts} workouts · {summary.total_calories_burned} kcal burned</div>
        </div>
      )}
    </section>
  );
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const userId = localStorage.getItem('wm_user_id');
  const userName = localStorage.getItem('wm_user_name') || 'User';
  const [stats, setStats] = useState(null);
  const [statsVersion, setStatsVersion] = useState(0);

  useEffect(() => {
    if (!userId) return;
    getUserProfile(userId).catch(error => {
      if (error.response?.status === 404) {
        localStorage.removeItem('wm_user_id');
        localStorage.removeItem('wm_user_name');
        navigate('/?reset=1', { replace: true });
      }
    });
  }, [userId, navigate]);

  useEffect(() => {
    if (!userId) return;
    getProgressSummary(userId).then(setStats).catch(() => setStats(null));
  }, [userId, statsVersion]);

  if (!userId) {
    navigate('/');
    return null;
  }

  const [title, subtitle] = PAGE_COPY[pathname] || PAGE_COPY['/dashboard'];
  const heading = pathname === '/dashboard' ? `${title}, ${userName.split(' ')[0]}! 👋` : title;

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">🏋️ WellnessMitra</div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map(item => (
            <button
              key={item.path}
              className={`nav-item ${pathname === item.path ? 'active' : ''}`}
              onClick={() => navigate(item.path)}
            >
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

      <main className="dashboard-main">
        <div className="dashboard-header">
          <h1>{heading}</h1>
          <p className="dashboard-subtitle">{subtitle}</p>
        </div>

        {pathname === '/chat' && (
          <div className="chat-section tall"><ChatInterface userId={userId} /></div>
        )}
        {pathname === '/workouts' && <WorkoutPanel userId={userId} />}
        {pathname === '/nutrition' && <NutritionPanel userId={userId} />}
        {pathname === '/gyms' && <GymPanel userId={userId} />}
        {pathname === '/progress' && (
          <ProgressPanel userId={userId} onChange={() => setStatsVersion(version => version + 1)} />
        )}
        {pathname === '/dashboard' && (
          <div className="dashboard-grid">
            <div className="stats-row">
              {[
                { label: 'Weight Change', value: stats ? `${stats.weight_change_kg} kg` : '—', icon: '⚖️' },
                { label: 'Calories Burned', value: stats ? stats.total_calories_burned.toLocaleString() : '—', icon: '⚡' },
                { label: 'Workouts Done', value: stats ? String(stats.total_workouts) : '—', icon: '💪' },
                { label: 'BMI Status', value: stats ? bmiLabel(stats.current_bmi) : '—', icon: '✅' },
              ].map(stat => (
                <div key={stat.label} className="stat-card">
                  <div className="stat-icon">{stat.icon}</div>
                  <div className="stat-value">{stat.value}</div>
                  <div className="stat-label">{stat.label}</div>
                </div>
              ))}
            </div>
            <div className="chat-section"><ChatInterface userId={userId} /></div>
            <div className="quick-actions">
              <h3>Quick Actions</h3>
              {[
                { icon: '💪', label: 'Log Workout', path: '/workouts' },
                { icon: '🥗', label: 'Meal Plan', path: '/nutrition' },
                { icon: '⚖️', label: 'Log Weight', path: '/progress' },
                { icon: '📍', label: 'Find Gyms', path: '/gyms' },
              ].map(action => (
                <button key={action.path} className="quick-action-btn" onClick={() => navigate(action.path)}>
                  <span>{action.icon}</span> {action.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
