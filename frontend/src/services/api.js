import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// ── User API ─────────────────────────────────────────────────────────────────

export const onboardUser = (userData) =>
  api.post('/users/onboard', userData).then(r => r.data);

export const getUserProfile = (userId) =>
  api.get(`/users/${userId}/profile`).then(r => r.data);

export const updateUserProfile = (userId, updates) =>
  api.put(`/users/${userId}/profile`, updates).then(r => r.data);

// ── Chat API ──────────────────────────────────────────────────────────────────

export const sendChatMessage = (userId, message, chatHistory = []) =>
  api.post('/chat/', {
    user_id: (userId && String(userId).trim()) || 'usr_demo123',
    message,
    chat_history: chatHistory || []
  }).then(r => r.data);

// ── Workout API ────────────────────────────────────────────────────────────────

export const logWorkout = (data) =>
  api.post('/workouts/log', data).then(r => r.data);

export const getWorkoutLogs = (userId, days = 30) =>
  api.get(`/workouts/${userId}/logs?days=${days}`).then(r => r.data);

// ── Progress API ───────────────────────────────────────────────────────────────

export const logWeight = (userId, weightKg) =>
  api.post('/progress/weight', { user_id: userId, weight_kg: weightKg }).then(r => r.data);

export const getProgressSummary = (userId, days = 30) =>
  api.get(`/progress/${userId}/summary?days=${days}`).then(r => r.data);

export default api;
