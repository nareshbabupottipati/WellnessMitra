# 🏋️ WellnessMitra — AI Fitness & Wellness Agent

> **Built for:** Agentic AI Mini-Hackathon — Division of Flexible Learning, IIIT Hyderabad
> **Stack:** Python · Google Gemini · LangGraph · FastAPI · React

---

## 🌟 What is WellnessMitra?

**WellnessMitra** (Wellness Friend) is an AI-powered personal fitness assistant that provides **personalized fitness, nutrition, and wellness guidance** based on the user's profile and location. It uses a **multi-agent architecture** powered by Google Gemini to deliver expert-level coaching through a simple chat interface.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💪 **Workout Plans** | AI-generated personalized weekly workout plans |
| 🥗 **Nutrition Guidance** | Custom meal plans with macro tracking |
| 📍 **Gym Finder** | Nearby gym discovery using Google Places API |
| 📊 **Progress Tracking** | Log workouts, meals, weight — view analytics |
| 🤖 **AI Chat Assistant** | 24/7 conversational fitness coach with memory |
| 🧘 **Wellness Support** | Sleep, stress, mindfulness, and recovery advice |

---

## 🏗️ Architecture

```
User ──► FastAPI Backend ──► Orchestrator Agent (LangGraph)
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
        Workout Agent        Nutrition Agent       Location Agent
              │                     │                     │
        Progress Agent       Assistant Agent
              │
    ┌─────────┴─────────┐
    │   Shared Services  │
    │  RAG · Gemini LLM  │
    │  ChromaDB · SQLite │
    └────────────────────┘
```

---

## 📁 Project Structure

```
WellnessMitra/
├── backend/
│   ├── agents/          # Orchestrator + 5 sub-agents
│   ├── tools/           # Google Maps, Nutrition, Progress tools
│   ├── rag/             # RAG pipeline (ChromaDB + Gemini embeddings)
│   ├── models/          # SQLAlchemy DB models
│   ├── database/        # DB connection + CRUD
│   └── api/             # FastAPI routes
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # App pages
│   │   └── services/    # API helpers
├── docs/                # Documentation
└── .env.example         # Environment variable template
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/nareshbabupottipati/WellnessMitra.git
cd WellnessMitra
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Copy and configure environment variables
cp ../.env.example ../.env
# Edit .env and add your API keys

# Ingest RAG knowledge documents (run once)
python -m rag.ingestion

# Start the backend server
uvicorn api.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 4. Open the App

- **Frontend:** http://localhost:3000
- **API Docs (Swagger):** http://localhost:8000/docs

---

## 🔑 API Keys Required

| Service | Get API Key | Free Tier |
|---------|------------|-----------|
| Google Gemini | [aistudio.google.com](https://aistudio.google.com) | ✅ Yes |
| Google Maps | [console.cloud.google.com](https://console.cloud.google.com) | ✅ $200/mo credit |
| Edamam Food API | [developer.edamam.com](https://developer.edamam.com) | ✅ Yes |

---

## 🤖 Multi-Agent System

| Agent | Triggered By | Responsibility |
|-------|-------------|----------------|
| **Orchestrator** | All messages | Intent classification + routing |
| **Workout Agent** | Workout queries | Weekly plans, exercises, adaptations |
| **Nutrition Agent** | Diet queries | Meal plans, macros, recipes |
| **Location Agent** | Gym queries | Google Maps gym discovery |
| **Progress Agent** | Progress queries | Analytics, insights, reports |
| **Assistant Agent** | General / Wellness | Q&A, motivation, mental wellness |

---

## 📖 Documentation

- [Full Documentation](docs/DOCUMENTATION.md)
- [Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)

---

## 🛠️ Tech Stack

- **LLM:** Google Gemini 2.0 Flash
- **Agents:** LangGraph
- **Backend:** FastAPI + SQLAlchemy
- **Frontend:** React 18
- **Vector DB:** ChromaDB
- **Embeddings:** Google text-embedding-004
- **Maps:** Google Places API
- **Nutrition:** Edamam Food API

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Made with ❤️ for IIIT-H Agentic AI Hackathon*
