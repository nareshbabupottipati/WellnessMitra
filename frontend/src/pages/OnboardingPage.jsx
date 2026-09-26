import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { onboardUser } from '../services/api';
import './OnboardingPage.css';

const STEPS = ['Personal Info', 'Body Metrics', 'Fitness Goals', 'Diet & Health'];

const GOALS = [
  { value: 'weight_loss',   label: '🔥 Weight Loss',   desc: 'Burn fat and slim down' },
  { value: 'muscle_gain',   label: '💪 Muscle Gain',   desc: 'Build strength and mass' },
  { value: 'endurance',     label: '🏃 Endurance',      desc: 'Boost cardio fitness' },
  { value: 'flexibility',   label: '🧘 Flexibility',    desc: 'Improve mobility' },
];

const ACTIVITY_LEVELS = [
  { value: 'sedentary',   label: 'Sedentary',      desc: 'Desk job, little movement' },
  { value: 'light',       label: 'Lightly Active', desc: '1-3 days/week exercise' },
  { value: 'moderate',    label: 'Moderate',        desc: '3-5 days/week exercise' },
  { value: 'active',      label: 'Very Active',     desc: '6-7 days/week exercise' },
  { value: 'very_active', label: 'Extra Active',    desc: 'Athlete / physical job' },
];

const DIETS = ['none', 'vegetarian', 'vegan', 'keto', 'paleo'];

export default function OnboardingPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    name: '', age: '', gender: 'male', location: 'Hyderabad, India',
    weight_kg: '', height_cm: '',
    fitness_goal: '', activity_level: '', days_per_week: 3,
    dietary_pref: 'none', allergies: '', medical_notes: '',
  });

  const set = (key, val) => setForm(f => ({ ...f, [key]: val }));

  const next = () => setStep(s => Math.min(s + 1, 3));
  const prev = () => setStep(s => Math.max(s - 1, 0));

  const submit = async () => {
    setLoading(true);
    setError('');
    try {
      const payload = {
        ...form,
        age:          parseInt(form.age),
        weight_kg:    parseFloat(form.weight_kg),
        height_cm:    parseFloat(form.height_cm),
        days_per_week: parseInt(form.days_per_week),
        allergies:    form.allergies ? form.allergies.split(',').map(s => s.trim()) : [],
      };
      const res = await onboardUser(payload);
      localStorage.setItem('wm_user_id',   res.user_id);
      localStorage.setItem('wm_user_name', form.name);
      navigate('/dashboard');
    } catch (e) {
      setError('Could not create profile. Please check your inputs and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-card">
        <div className="onboarding-brand">🏋️ WellnessMitra</div>
        {searchParams.get('reset') && (
          <div className="error-msg">Your saved profile was cleared when the demo moved to JSON storage. Create it again to use FitBot.</div>
        )}
        <div className="step-indicator">
          {STEPS.map((s, i) => (
            <div key={i} className={`step-dot ${i === step ? 'active' : i < step ? 'done' : ''}`}>
              <span>{i < step ? '✓' : i + 1}</span>
              <label>{s}</label>
            </div>
          ))}
        </div>

        <div className="onboarding-body">
          {step === 0 && (
            <div className="step-content">
              <h2>👋 Tell us about yourself</h2>
              <input placeholder="Full Name" value={form.name} onChange={e => set('name', e.target.value)} />
              <div className="row-2">
                <input type="number" placeholder="Age" value={form.age} onChange={e => set('age', e.target.value)} />
                <select value={form.gender} onChange={e => set('gender', e.target.value)}>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <input placeholder="Location (City or area)" value={form.location} onChange={e => set('location', e.target.value)} />
            </div>
          )}

          {step === 1 && (
            <div className="step-content">
              <h2>📏 Body Metrics</h2>
              <input type="number" placeholder="Weight (kg)" value={form.weight_kg} onChange={e => set('weight_kg', e.target.value)} />
              <input type="number" placeholder="Height (cm)" value={form.height_cm} onChange={e => set('height_cm', e.target.value)} />
              {form.weight_kg && form.height_cm && (
                <div className="bmi-preview">
                  BMI: <strong>{(parseFloat(form.weight_kg) / ((parseFloat(form.height_cm)/100) ** 2)).toFixed(1)}</strong>
                </div>
              )}
            </div>
          )}

          {step === 2 && (
            <div className="step-content">
              <h2>🎯 Fitness Goals</h2>
              <div className="goal-grid">
                {GOALS.map(g => (
                  <div key={g.value} className={`goal-card ${form.fitness_goal === g.value ? 'selected' : ''}`}
                    onClick={() => set('fitness_goal', g.value)}>
                    <div className="goal-label">{g.label}</div>
                    <div className="goal-desc">{g.desc}</div>
                  </div>
                ))}
              </div>
              <div className="activity-group">
                <label>Activity Level</label>
                {ACTIVITY_LEVELS.map(a => (
                  <div key={a.value} className={`activity-row ${form.activity_level === a.value ? 'selected' : ''}`}
                    onClick={() => set('activity_level', a.value)}>
                    <strong>{a.label}</strong> — {a.desc}
                  </div>
                ))}
              </div>
              <div className="row-2">
                <label>Days/week available:</label>
                <input type="number" min="1" max="7" value={form.days_per_week}
                  onChange={e => set('days_per_week', e.target.value)} />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="step-content">
              <h2>🥗 Diet & Health</h2>
              <div className="diet-options">
                {DIETS.map(d => (
                  <button key={d} className={`diet-btn ${form.dietary_pref === d ? 'selected' : ''}`}
                    onClick={() => set('dietary_pref', d)}>
                    {d.charAt(0).toUpperCase() + d.slice(1)}
                  </button>
                ))}
              </div>
              <input placeholder="Allergies (comma-separated: nuts, gluten, dairy)"
                value={form.allergies} onChange={e => set('allergies', e.target.value)} />
              <textarea placeholder="Medical notes (optional: injuries, conditions...)"
                value={form.medical_notes} onChange={e => set('medical_notes', e.target.value)} />
              {error && <div className="error-msg">{error}</div>}
            </div>
          )}
        </div>

        <div className="onboarding-footer">
          {step > 0 && <button className="btn-outline" onClick={prev}>← Back</button>}
          {step < 3
            ? <button className="btn-primary" onClick={next}>Next →</button>
            : <button className="btn-primary" onClick={submit} disabled={loading}>
                {loading ? 'Creating Profile...' : '🚀 Get Started'}
              </button>
          }
        </div>
      </div>
    </div>
  );
}
