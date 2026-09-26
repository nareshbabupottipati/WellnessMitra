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

| Key | Steps |
|-----|-------|
| **Google Gemini** | Go to [aistudio.google.com](https://aistudio.google.com) → Sign in → Get API Key |
| **Google Maps** | Go to [console.cloud.google.com](https://console.cloud.google.com) → Enable "Places API" + "Geocoding API" → Create Key |
| **Edamam** | Go to [developer.edamam.com](https://developer.edamam.com) → Register → Food Database API → Get App ID + App Key |

---

### Step 2 — First-Time Setup (Run Once)

```
Double-click: setup.bat
```

This will automatically:
- ✅ Check Python and Node.js
- ✅ Create `.env` file and open it for editing (add your keys here)
- ✅ Create Python virtual environment (`venv/`)
- ✅ Install all Python packages (`requirements.txt`)
- ✅ Install all frontend packages (`npm install`)
- ✅ Run RAG knowledge ingestion (builds ChromaDB vector store)

---

### Step 3 — Run the App

```
Double-click: start.bat
```

This opens two terminal windows (keep them open) and launches the browser automatically.

| Service | URL |
|---------|-----|
| 🌐 **Frontend (React)** | http://localhost:3000 |
| ⚡ **Backend (FastAPI)** | http://localhost:8000 |
| 📄 **API Docs (Swagger)** | http://localhost:8000/docs |

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

Open the `.env` file in Notepad and fill in your keys:

```env
GOOGLE_API_KEY=AIzaSy...your-key
GOOGLE_MAPS_API_KEY=AIzaSy...your-key
EDAMAM_APP_ID=abc123...
EDAMAM_APP_KEY=def456...
```

---

## 🧪 Testing the App

### Option A — Use the UI
1. Open http://localhost:3000
2. Complete the 4-step onboarding form
3. Chat with FitBot using the quick prompt buttons

### Option B — Use Swagger API Docs
1. Open http://localhost:8000/docs
2. Create a user via `POST /users/onboard`
3. Send a chat message via `POST /chat/`

### Sample API Test (PowerShell)
```powershell
# 1. Create user
$user = @{
    name="Rahul"; age=28; gender="male"
    weight_kg=80; height_cm=175
    fitness_goal="weight_loss"; activity_level="moderate"
    dietary_pref="vegetarian"; location="Hyderabad, India"
    days_per_week=4
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/users/onboard" -Method POST -Body $user -ContentType "application/json"
$userId = $result.user_id
Write-Host "User ID: $userId"

# 2. Chat with FitBot
$chat = @{ user_id=$userId; message="Give me a 3-day workout plan"; chat_history=@() } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat/" -Method POST -Body $chat -ContentType "application/json"
```

---

## ❗ Troubleshooting

| Problem | Fix |
|---------|-----|
| `setup.bat` can't find Python | Install from [python.org](https://python.org), check "Add to PATH" ✅ |
| `setup.bat` can't find Node | Install from [nodejs.org](https://nodejs.org) |
| Backend won't start | Check `.env` has valid `GOOGLE_API_KEY` |
| Gym finder not working | Enable Places API + Geocoding API in Google Cloud Console |
| RAG ingestion fails | Check `GOOGLE_API_KEY` is valid and has billing enabled |
| Frontend shows blank page | Wait 30 seconds for React to compile, then refresh |
| Port already in use | Run `stop.bat` first, then `start.bat` |

---

## 📂 Project Structure

```
WellnessMitra/
├── setup.bat             ← Run first (installs everything)
├── start.bat             ← Run to launch the app
├── stop.bat              ← Run to stop everything
├── .env                  ← Your API keys (created by setup.bat)
├── backend/
│   ├── agents/           ← AI agents (workout, nutrition, etc.)
│   ├── api/              ← FastAPI routes
│   ├── rag/              ← RAG pipeline + knowledge docs
│   └── database/         ← SQLite models
└── frontend/
    └── src/              ← React components and pages
```

---

*Built for IIIT-H Agentic AI Mini-Hackathon 2026* 🏋️
