# 🏋️ WellnessMitra — Local Run Guide

## ✅ Prerequisites

Make sure these are installed on your Windows machine:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

---

## 🚀 Quick Start (3 Steps)

### Step 1 — Get API Keys (Free)

| Key | Required? | Steps |
|-----|-----------|-------|
| **Google Gemini** | ✅ **Required** | Go to [aistudio.google.com](https://aistudio.google.com) → Sign in → Get API Key |
| **Google Maps** | ⚪ Optional | Go to [console.cloud.google.com](https://console.cloud.google.com) → Enable "Places API" + "Geocoding API" (for Gym Finder) |

> 💡 **No Database or Edamam Account Needed!**
> All user profiles, workouts, weight logs, meals, and food nutrition are stored directly in local JSON files in `data/*.json`.

---

### Step 2 — First-Time Setup (Run Once)

```
Double-click: setup.bat
```

This will automatically:
- ✅ Check Python and Node.js
- ✅ Create `.env` file and open it for editing (paste your `GOOGLE_API_KEY`)
- ✅ Create Python virtual environment (`venv/`)
- ✅ Install all Python packages (`backend/requirements.txt`)
- ✅ Install all frontend packages (`npm install`)
- ✅ Run RAG knowledge ingestion (builds ChromaDB vector store)

---

### Step 3 — Run the App

```
Double-click: start.bat
```

This opens two terminal windows (keep them open) and launches your browser automatically.

| Service | URL |
|---------|-----|
| 🌐 **Frontend (React)** | http://localhost:3000 |
| ⚡ **Backend (FastAPI)** | http://localhost:8000 |
| 📄 **API Docs (Swagger)** | http://localhost:8000/docs |

---

## 📁 JSON Data Storage

All data is human-readable and stored locally in the `data/` directory:

| JSON File | Purpose | Pre-populated? |
|-----------|---------|----------------|
| `data/foods.json` | Nutrition database (90+ Indian & global foods) | ✅ Yes |
| `data/users.json` | User profiles | ✅ Demo user `usr_demo123` included |
| `data/workout_logs.json` | Workout session logs | ✅ Sample workouts included |
| `data/weight_logs.json` | Weight measurements & BMI history | ✅ Sample progress trend included |
| `data/meal_logs.json` | Daily meal logs & macros | ✅ Sample meals included |

---

## 📁 Script Reference

| Script | Purpose |
|--------|---------|
| `setup.bat` | First-time setup — run once |
| `start.bat` | Start both backend + frontend |
| `start-backend.bat` | Start backend only |
| `start-frontend.bat` | Start frontend only |
| `stop.bat` | Stop all running services |

---

## 🔑 Editing Your API Keys

Open the `.env` file in Notepad and fill in your Gemini key:

```env
GOOGLE_API_KEY=AIzaSy...your-gemini-key
GOOGLE_MAPS_API_KEY=AIzaSy...your-maps-key-optional
DATA_DIR=./data
```

---

## 🧪 Testing the App

### Option A — Use the UI
1. Open http://localhost:3000
2. Complete the onboarding form (or explore existing demo profile)
3. Chat with FitBot using the quick prompt buttons

### Option B — Use Swagger API Docs
1. Open http://localhost:8000/docs
2. Create or view user profiles via `GET /users/usr_demo123/profile`
3. Search food nutrition via `GET /nutrition/foods?q=banana`
4. Send a chat message via `POST /chat/`

### Sample API Test (PowerShell)
```powershell
# 1. Check user profile
Invoke-RestMethod -Uri "http://localhost:8000/users/usr_demo123/profile"

# 2. Search local food database
Invoke-RestMethod -Uri "http://localhost:8000/nutrition/foods?q=paneer"

# 3. View 30-day progress
Invoke-RestMethod -Uri "http://localhost:8000/progress/usr_demo123/summary"
```

---

## 🛑 Troubleshooting

### Port 8000 or 3000 already in use
Run `stop.bat` to kill any leftover processes, then run `start.bat` again.

### Python / Node not recognized
Make sure Python 3.10+ and Node.js 18+ are added to your Windows PATH environment variable.
Restart your terminal / computer after installing them.
