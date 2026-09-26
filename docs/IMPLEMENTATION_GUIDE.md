# 🏋️ Fitness & Wellness Agent — Step-by-Step Implementation Guide

> **Platform:** IIIT-H Agentic AI Mini-Hackathon
> **Stack:** Python · Google Gemini · LangGraph · FastAPI · React · Google Maps API

---

## 📋 Table of Contents

1. [Tech Stack Overview](#1-tech-stack-overview)
2. [Project Structure](#2-project-structure)
3. [Environment Setup](#3-environment-setup)
4. [Agent Architecture Design](#4-agent-architecture-design)
5. [Module 1 — User Profile & Onboarding](#5-module-1--user-profile--onboarding)
6. [Module 2 — Workout Recommendation Agent](#6-module-2--workout-recommendation-agent)
7. [Module 3 — Diet & Nutrition Agent](#7-module-3--diet--nutrition-agent)
8. [Module 4 — Location-Based Gym Finder Agent](#8-module-4--location-based-gym-finder-agent)
9. [Module 5 — Progress Tracking Agent](#9-module-5--progress-tracking-agent)
10. [Module 6 — Conversational AI Assistant](#10-module-6--conversational-ai-assistant)
11. [RAG Pipeline Setup](#11-rag-pipeline-setup)
12. [Orchestrator Agent](#12-orchestrator-agent)
13. [Backend API (FastAPI)](#13-backend-api-fastapi)
14. [Frontend UI (React)](#14-frontend-ui-react)
15. [Testing & Demo](#15-testing--demo)

---

## 1. Tech Stack Overview

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | Google Gemini 2.0 Flash | Core reasoning & generation |
| **Agent Framework** | LangGraph / Google ADK | Multi-agent orchestration |
| **Backend** | FastAPI (Python) | REST API server |
| **Frontend** | React + TailwindCSS | User Interface |
| **Vector DB** | ChromaDB / FAISS | RAG knowledge retrieval |
| **Database** | SQLite / PostgreSQL | User profiles & logs |
| **Maps** | Google Places API | Nearby gym discovery |
| **Nutrition** | Edamam API / USDA | Food & nutrition data |
| **Memory** | LangGraph Checkpointer | Conversation context |
| **Embeddings** | Google text-embedding-004 | RAG embeddings |

---

## 2. Project Structure

```
fitness-wellness-agent/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # Master orchestrator agent
│   │   ├── workout_agent.py         # Workout recommendation agent
│   │   ├── nutrition_agent.py       # Diet & nutrition agent
│   │   ├── location_agent.py        # Gym finder agent
│   │   ├── progress_agent.py        # Progress tracking agent
│   │   └── assistant_agent.py       # Conversational assistant agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── maps_tool.py             # Google Maps API tool
│   │   ├── nutrition_tool.py        # Nutrition API tool
│   │   ├── workout_tool.py          # Exercise database tool
│   │   └── progress_tool.py         # DB read/write tool
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py             # Load & embed knowledge docs
│   │   ├── retriever.py             # Query vector store
│   │   └── knowledge_docs/          # Fitness/nutrition PDFs & text
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # User profile schema
│   │   ├── workout.py               # Workout log schema
│   │   └── nutrition.py             # Meal log schema
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py                    # DB connection & setup
│   │   └── crud.py                  # Create/Read/Update/Delete ops
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── user_routes.py
│   │   │   ├── workout_routes.py
│   │   │   ├── nutrition_routes.py
│   │   │   ├── gym_routes.py
│   │   │   ├── progress_routes.py
│   │   │   └── chat_routes.py
│   │   └── main.py                  # FastAPI app entrypoint
│   ├── config.py                    # Config & API keys
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
├── .env
└── README.md
```

---

## 3. Environment Setup

### Step 3.1 — Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install core packages
pip install google-genai google-adk langgraph langchain-google-genai
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv
pip install chromadb langchain-community pypdf requests
```

### Step 3.2 — Create `.env` File

```env
# Google AI
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_maps_api_key_here

# Nutrition API (free tier: https://developer.edamam.com)
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key

# Database
DATABASE_URL=sqlite:///./fitness_agent.db

# App
APP_SECRET_KEY=your_secret_key
```

### Step 3.3 — Create `config.py`

```python
# backend/config.py
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitness_agent.db")
```

---

## 4. Agent Architecture Design

### Step 4.1 — Define Agent State (Shared Context)

```python
# backend/agents/__init__.py
from typing import TypedDict, Optional, List

class FitnessAgentState(TypedDict):
    user_id: str
    user_profile: dict              # age, weight, height, goals, prefs
    user_message: str               # latest user input
    intent: str                     # detected intent
    workout_plan: Optional[dict]
    meal_plan: Optional[dict]
    nearby_gyms: Optional[list]
    progress_summary: Optional[dict]
    rag_context: Optional[str]      # retrieved knowledge
    chat_history: List[dict]        # conversation memory
    response: str                   # final response to user
```

### Step 4.2 — Intent Classification

```python
# Intent types the orchestrator routes to agents
INTENTS = {
    "workout":    "workout_agent",
    "nutrition":  "nutrition_agent",
    "gym_finder": "location_agent",
    "progress":   "progress_agent",
    "general":    "assistant_agent",
    "wellness":   "assistant_agent",
}
```

---

## 5. Module 1 — User Profile & Onboarding

### Step 5.1 — Define User Model

```python
# backend/models/user.py
from sqlalchemy import Column, String, Integer, Float, JSON
from backend.database.db import Base

class User(Base):
    __tablename__ = "users"
    id            = Column(String, primary_key=True)
    name          = Column(String)
    age           = Column(Integer)
    gender        = Column(String)
    weight_kg     = Column(Float)
    height_cm     = Column(Float)
    fitness_goal  = Column(String)   # weight_loss | muscle_gain | endurance | flexibility
    activity_level= Column(String)   # sedentary | light | moderate | active | very_active
    dietary_pref  = Column(String)   # vegan | vegetarian | keto | paleo | none
    allergies     = Column(JSON)     # ["nuts", "gluten"]
    location      = Column(String)   # city or lat,lng
    medical_notes = Column(String)
```

### Step 5.2 — CRUD Operations

```python
# backend/database/crud.py
from sqlalchemy.orm import Session
from backend.models.user import User

def create_user(db: Session, user_data: dict) -> User:
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: str, updates: dict) -> User:
    db.query(User).filter(User.id == user_id).update(updates)
    db.commit()
    return get_user(db, user_id)
```

### Step 5.3 — Onboarding API Route

```python
# backend/api/routes/user_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.crud import create_user, get_user

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/onboard")
def onboard_user(user_data: dict, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    return {"status": "success", "user_id": user.id}

@router.get("/{user_id}/profile")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    return get_user(db, user_id)
```

---

## 6. Module 2 — Workout Recommendation Agent

### Step 6.1 — Define Workout Tool

```python
# backend/tools/workout_tool.py
from google.genai import types

def get_workout_plan(
    fitness_goal: str,
    activity_level: str,
    available_equipment: str,
    days_per_week: int,
    duration_minutes: int
) -> dict:
    """
    Returns a structured weekly workout plan for the user.
    fitness_goal: weight_loss | muscle_gain | endurance | flexibility
    activity_level: sedentary | light | moderate | active | very_active
    available_equipment: home | gym | none
    """
    # This tool is called by the LLM — it validates params & returns structured plan
    return {
        "goal": fitness_goal,
        "days_per_week": days_per_week,
        "plan": "Will be filled by LLM response"
    }

# Tool declaration for Gemini
workout_tool_declaration = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_workout_plan",
            description="Generate a personalized weekly workout plan",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "fitness_goal":        types.Schema(type=types.Type.STRING),
                    "activity_level":      types.Schema(type=types.Type.STRING),
                    "available_equipment": types.Schema(type=types.Type.STRING),
                    "days_per_week":       types.Schema(type=types.Type.INTEGER),
                    "duration_minutes":    types.Schema(type=types.Type.INTEGER),
                },
                required=["fitness_goal", "activity_level"]
            )
        )
    ]
)
```

### Step 6.2 — Workout Agent Node

```python
# backend/agents/workout_agent.py
import google.generativeai as genai
from backend.config import GOOGLE_API_KEY
from backend.rag.retriever import retrieve_context

genai.configure(api_key=GOOGLE_API_KEY)

WORKOUT_SYSTEM_PROMPT = """
You are an expert personal fitness trainer. Based on the user's profile:
- Age: {age}, Weight: {weight}kg, Height: {height}cm
- Fitness Goal: {fitness_goal}
- Activity Level: {activity_level}
- Available Equipment: {equipment}
- Days per week available: {days}

Create a detailed, safe, and effective weekly workout plan.
Include:
1. Exercise name, sets, reps/duration, rest period
2. Target muscle groups
3. Warm-up and cool-down
4. Progression tips

Use any retrieved fitness knowledge: {rag_context}
"""

def workout_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    rag_context = retrieve_context(
        query=f"workout plan for {profile['fitness_goal']} {profile['activity_level']}",
        collection="fitness"
    )

    prompt = WORKOUT_SYSTEM_PROMPT.format(
        age=profile.get("age"),
        weight=profile.get("weight_kg"),
        height=profile.get("height_cm"),
        fitness_goal=profile.get("fitness_goal"),
        activity_level=profile.get("activity_level"),
        equipment=state["user_message"],
        days=profile.get("days_per_week", 3),
        rag_context=rag_context
    )

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)

    return {
        **state,
        "workout_plan": response.text,
        "response": response.text
    }
```

---

## 7. Module 3 — Diet & Nutrition Agent

### Step 7.1 — Nutrition API Tool

```python
# backend/tools/nutrition_tool.py
import requests
from backend.config import EDAMAM_APP_ID, EDAMAM_APP_KEY

def search_food_nutrition(food_item: str) -> dict:
    """Search nutritional info for a food item via Edamam API."""
    url = "https://api.edamam.com/api/food-database/v2/parser"
    params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "ingr": food_item,
        "nutrition-type": "cooking"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("hints"):
        food = data["hints"][0]["food"]
        nutrients = food.get("nutrients", {})
        return {
            "food": food.get("label"),
            "calories": nutrients.get("ENERC_KCAL", 0),
            "protein_g": nutrients.get("PROCNT", 0),
            "carbs_g": nutrients.get("CHOCDF", 0),
            "fat_g": nutrients.get("FAT", 0),
            "fiber_g": nutrients.get("FIBTG", 0)
        }
    return {"error": "Food not found"}
```

### Step 7.2 — Nutrition Agent Node

```python
# backend/agents/nutrition_agent.py
from backend.rag.retriever import retrieve_context

NUTRITION_SYSTEM_PROMPT = """
You are a certified nutritionist and dietitian. Based on the user's profile:
- Weight: {weight}kg, Height: {height}cm, Age: {age}
- Fitness Goal: {fitness_goal}
- Dietary Preference: {dietary_pref}
- Allergies: {allergies}
- Daily Calorie Target: {calories} kcal

Create a balanced 7-day meal plan with:
1. Breakfast, Lunch, Dinner, and 2 Snacks per day
2. Macro breakdown (protein, carbs, fat) for each meal
3. Cooking instructions or recipe links
4. Daily water intake recommendation
5. Foods to AVOID based on allergies/preferences

Nutrition knowledge base: {rag_context}
"""

def calculate_daily_calories(weight_kg, height_cm, age, gender, activity_level, goal):
    """Harris-Benedict BMR formula"""
    if gender == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)

    activity_multipliers = {
        "sedentary": 1.2, "light": 1.375,
        "moderate": 1.55, "active": 1.725, "very_active": 1.9
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    goal_adjustments = {
        "weight_loss": -500, "muscle_gain": +300, "endurance": +200
    }
    return tdee + goal_adjustments.get(goal, 0)

def nutrition_agent_node(state: dict) -> dict:
    import google.generativeai as genai
    from backend.config import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)

    profile = state["user_profile"]
    calories = calculate_daily_calories(
        profile["weight_kg"], profile["height_cm"],
        profile["age"], profile.get("gender", "male"),
        profile["activity_level"], profile["fitness_goal"]
    )

    rag_context = retrieve_context(
        query=f"meal plan {profile['dietary_pref']} {profile['fitness_goal']}",
        collection="nutrition"
    )

    prompt = NUTRITION_SYSTEM_PROMPT.format(
        weight=profile["weight_kg"], height=profile["height_cm"],
        age=profile["age"], fitness_goal=profile["fitness_goal"],
        dietary_pref=profile.get("dietary_pref", "none"),
        allergies=profile.get("allergies", []),
        calories=round(calories),
        rag_context=rag_context
    )

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)

    return {**state, "meal_plan": response.text, "response": response.text}
```

---

## 8. Module 4 — Location-Based Gym Finder Agent

### Step 8.1 — Google Maps / Places Tool

```python
# backend/tools/maps_tool.py
import requests
from backend.config import GOOGLE_MAPS_API_KEY

def find_nearby_gyms(location: str, radius_meters: int = 5000) -> list:
    """
    Find gyms near a location using Google Places API.
    location: "lat,lng" or city name
    """
    # Step 1: Geocode if city name is given
    if not "," in location or not location.replace(",","").replace(".","").replace("-","").isdigit():
        geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geo_resp = requests.get(geo_url, params={"address": location, "key": GOOGLE_MAPS_API_KEY})
        geo_data = geo_resp.json()
        if geo_data["results"]:
            loc = geo_data["results"][0]["geometry"]["location"]
            location = f"{loc['lat']},{loc['lng']}"

    # Step 2: Search for gyms
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius_meters,
        "type": "gym",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(places_url, params=params)
    data = response.json()

    gyms = []
    for place in data.get("results", [])[:5]:
        gyms.append({
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "rating": place.get("rating"),
            "open_now": place.get("opening_hours", {}).get("open_now"),
            "place_id": place.get("place_id"),
            "maps_url": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
        })
    return gyms
```

### Step 8.2 — Location Agent Node

```python
# backend/agents/location_agent.py
from backend.tools.maps_tool import find_nearby_gyms

def location_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    location = profile.get("location", "Hyderabad, India")

    gyms = find_nearby_gyms(location)

    formatted = "\n".join([
        f"🏋️ {g['name']} | ⭐ {g['rating']} | 📍 {g['address']} | "
        f"{'🟢 Open' if g['open_now'] else '🔴 Closed'} | [Maps]({g['maps_url']})"
        for g in gyms
    ])

    response = f"Here are the top gyms near **{location}**:\n\n{formatted}"
    return {**state, "nearby_gyms": gyms, "response": response}
```

---

## 9. Module 5 — Progress Tracking Agent

### Step 9.1 — Define Progress Models

```python
# backend/models/workout.py
from sqlalchemy import Column, String, Float, Integer, Date, JSON
from backend.database.db import Base
import datetime

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    user_id         = Column(String, index=True)
    date            = Column(Date, default=datetime.date.today)
    exercises       = Column(JSON)       # [{"name": "Push-up", "sets": 3, "reps": 15}]
    duration_mins   = Column(Integer)
    calories_burned = Column(Float)
    notes           = Column(String)

class WeightLog(Base):
    __tablename__ = "weight_logs"
    id      = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True)
    date    = Column(Date, default=datetime.date.today)
    weight_kg = Column(Float)
    bmi     = Column(Float)
```

### Step 9.2 — Progress Agent Node

```python
# backend/agents/progress_agent.py
import google.generativeai as genai
from backend.database.crud import get_workout_logs, get_weight_logs
from backend.config import GOOGLE_API_KEY

def progress_agent_node(state: dict) -> dict:
    genai.configure(api_key=GOOGLE_API_KEY)

    user_id = state["user_id"]
    workout_logs = get_workout_logs(user_id, days=30)
    weight_logs = get_weight_logs(user_id, days=30)

    # Summarize progress
    total_workouts = len(workout_logs)
    total_calories = sum(log.calories_burned for log in workout_logs)
    weight_start = weight_logs[0].weight_kg if weight_logs else None
    weight_current = weight_logs[-1].weight_kg if weight_logs else None
    weight_change = (weight_current - weight_start) if weight_start else 0

    summary = {
        "total_workouts_30d": total_workouts,
        "total_calories_burned": total_calories,
        "weight_change_kg": round(weight_change, 2),
        "current_weight": weight_current
    }

    prompt = f"""
    Analyze this user's 30-day fitness progress and provide:
    1. A motivating summary
    2. Key achievements
    3. Areas to improve
    4. Recommendations for next 30 days
    
    Progress Data: {summary}
    User Goal: {state['user_profile'].get('fitness_goal')}
    """

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)

    return {**state, "progress_summary": summary, "response": response.text}
```

---

## 10. Module 6 — Conversational AI Assistant

### Step 10.1 — Assistant with Memory

```python
# backend/agents/assistant_agent.py
import google.generativeai as genai
from backend.config import GOOGLE_API_KEY
from backend.rag.retriever import retrieve_context

genai.configure(api_key=GOOGLE_API_KEY)

ASSISTANT_SYSTEM_PROMPT = """
You are FitBot, a friendly and expert AI fitness & wellness coach.
You help users with:
- Exercise advice and form corrections
- Nutrition guidance and healthy eating habits
- Motivation and mental wellness support
- Injury prevention and recovery advice
- Sleep and stress management tips

User Profile: {profile}
Relevant Knowledge: {rag_context}

Respond in a warm, encouraging, and professional tone.
Keep responses concise but actionable.
"""

def assistant_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    chat_history = state.get("chat_history", [])
    user_message = state["user_message"]

    # Retrieve relevant context from RAG
    rag_context = retrieve_context(query=user_message, collection="general")

    # Build conversation history for Gemini
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=ASSISTANT_SYSTEM_PROMPT.format(
            profile=profile,
            rag_context=rag_context
        )
    )

    # Pass chat history for multi-turn memory
    chat = model.start_chat(history=[
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in chat_history
    ])

    response = chat.send_message(user_message)

    # Update history
    updated_history = chat_history + [
        {"role": "user", "content": user_message},
        {"role": "model", "content": response.text}
    ]

    return {**state, "chat_history": updated_history, "response": response.text}
```

---

## 11. RAG Pipeline Setup

### Step 11.1 — Prepare Knowledge Documents

Create files in `backend/rag/knowledge_docs/`:
```
knowledge_docs/
├── fitness_exercises.txt          # Exercise descriptions, form, benefits
├── nutrition_guidelines.txt       # Macros, vitamins, meal timing
├── workout_programs.txt           # Programs: HIIT, strength, cardio, yoga
├── wellness_tips.txt              # Sleep, stress, recovery, hydration
└── injury_prevention.txt          # Common injuries, prevention, rehab
```

### Step 11.2 — Ingest Documents into ChromaDB

```python
# backend/rag/ingestion.py
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from backend.config import GOOGLE_API_KEY

def ingest_documents():
    """Load knowledge docs, chunk them, embed, and store in ChromaDB."""
    client = chromadb.PersistentClient(path="./chroma_db")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    docs_path = Path("backend/rag/knowledge_docs")
    for doc_file in docs_path.glob("*.txt"):
        collection_name = doc_file.stem.split("_")[0]   # "fitness", "nutrition", etc.
        collection = client.get_or_create_collection(collection_name)

        text = doc_file.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            embedding = embeddings.embed_query(chunk)
            collection.add(
                ids=[f"{doc_file.stem}_{i}"],
                documents=[chunk],
                embeddings=[embedding]
            )
        print(f"✅ Ingested {len(chunks)} chunks from {doc_file.name}")

if __name__ == "__main__":
    ingest_documents()
```

### Step 11.3 — Retriever Function

```python
# backend/rag/retriever.py
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import GOOGLE_API_KEY

_client = None

def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path="./chroma_db")
    return _client

def retrieve_context(query: str, collection: str = "general", top_k: int = 3) -> str:
    """Retrieve relevant knowledge chunks for a query."""
    try:
        client = get_chroma_client()
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=GOOGLE_API_KEY
        )
        col = client.get_or_create_collection(collection)
        query_embedding = embeddings.embed_query(query)
        results = col.query(query_embeddings=[query_embedding], n_results=top_k)

        if results["documents"]:
            return "\n\n".join(results["documents"][0])
        return ""
    except Exception:
        return ""
```

---

## 12. Orchestrator Agent

### Step 12.1 — Build LangGraph Orchestrator

```python
# backend/agents/orchestrator.py
from langgraph.graph import StateGraph, END
from backend.agents import FitnessAgentState
from backend.agents.workout_agent import workout_agent_node
from backend.agents.nutrition_agent import nutrition_agent_node
from backend.agents.location_agent import location_agent_node
from backend.agents.progress_agent import progress_agent_node
from backend.agents.assistant_agent import assistant_agent_node
import google.generativeai as genai
from backend.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def intent_classifier_node(state: FitnessAgentState) -> FitnessAgentState:
    """Classify user intent to route to the right agent."""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    prompt = f"""
    Classify this user message into ONE of these intents:
    - workout: User asks about exercises, workouts, training plans
    - nutrition: User asks about diet, meals, food, calories
    - gym_finder: User wants to find gyms or fitness centers nearby
    - progress: User asks about their progress, stats, or history
    - general: General fitness/wellness questions or motivation
    
    User message: "{state['user_message']}"
    
    Respond with ONLY the intent word (lowercase).
    """
    response = model.generate_content(prompt)
    intent = response.text.strip().lower()
    return {**state, "intent": intent}

def route_to_agent(state: FitnessAgentState) -> str:
    """Router function for conditional edges."""
    routing = {
        "workout":    "workout_agent",
        "nutrition":  "nutrition_agent",
        "gym_finder": "location_agent",
        "progress":   "progress_agent",
        "general":    "assistant_agent",
    }
    return routing.get(state["intent"], "assistant_agent")

def build_fitness_graph():
    """Build and compile the multi-agent LangGraph."""
    graph = StateGraph(FitnessAgentState)

    # Add all agent nodes
    graph.add_node("intent_classifier", intent_classifier_node)
    graph.add_node("workout_agent",    workout_agent_node)
    graph.add_node("nutrition_agent",  nutrition_agent_node)
    graph.add_node("location_agent",   location_agent_node)
    graph.add_node("progress_agent",   progress_agent_node)
    graph.add_node("assistant_agent",  assistant_agent_node)

    # Set entry point
    graph.set_entry_point("intent_classifier")

    # Conditional routing
    graph.add_conditional_edges(
        "intent_classifier",
        route_to_agent,
        {
            "workout_agent":   "workout_agent",
            "nutrition_agent": "nutrition_agent",
            "location_agent":  "location_agent",
            "progress_agent":  "progress_agent",
            "assistant_agent": "assistant_agent",
        }
    )

    # All agents end after responding
    for agent in ["workout_agent", "nutrition_agent", "location_agent",
                  "progress_agent", "assistant_agent"]:
        graph.add_edge(agent, END)

    return graph.compile()

# Singleton compiled graph
fitness_graph = build_fitness_graph()
```

---

## 13. Backend API (FastAPI)

### Step 13.1 — Chat API Route

```python
# backend/api/routes/chat_routes.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.agents.orchestrator import fitness_graph
from backend.database.db import get_db
from backend.database.crud import get_user

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: list = []

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = get_user(db, request.user_id)
    if not user:
        return {"error": "User not found. Please complete onboarding first."}

    user_profile = {
        "age": user.age, "gender": user.gender,
        "weight_kg": user.weight_kg, "height_cm": user.height_cm,
        "fitness_goal": user.fitness_goal,
        "activity_level": user.activity_level,
        "dietary_pref": user.dietary_pref,
        "allergies": user.allergies,
        "location": user.location
    }

    initial_state = {
        "user_id": request.user_id,
        "user_profile": user_profile,
        "user_message": request.message,
        "chat_history": request.chat_history,
        "intent": "",
        "response": ""
    }

    result = fitness_graph.invoke(initial_state)

    return {
        "response": result["response"],
        "intent": result["intent"],
        "chat_history": result.get("chat_history", [])
    }
```

### Step 13.2 — Main App Entry Point

```python
# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import user_routes, chat_routes, workout_routes, gym_routes
from backend.database.db import Base, engine

Base.metadata.create_all(bind=engine)   # Create all DB tables

app = FastAPI(
    title="Fitness & Wellness Agent API",
    description="AI-powered personal fitness assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_routes.router)
app.include_router(chat_routes.router)
app.include_router(workout_routes.router)
app.include_router(gym_routes.router)
```

### Step 13.3 — Run the Backend

```bash
# Run FastAPI server
uvicorn backend.api.main:app --reload --port 8000

# Ingest RAG knowledge docs (run once)
python -m backend.rag.ingestion
```

---

## 14. Frontend UI (React)

### Step 14.1 — Create React App

```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom recharts @heroicons/react
```

### Step 14.2 — Key Pages to Build

```
src/pages/
├── OnboardingPage.jsx    # Multi-step user profile form
├── DashboardPage.jsx     # Progress overview + quick actions
├── WorkoutPage.jsx       # View & log workout plans
├── NutritionPage.jsx     # View meal plan + food logging
├── GymFinderPage.jsx     # Map + gym listings
├── ChatPage.jsx          # Chat interface (main AI assistant)
└── ProgressPage.jsx      # Charts & analytics
```

### Step 14.3 — Chat Interface Component

```jsx
// src/components/ChatInterface.jsx
import { useState } from 'react';
import axios from 'axios';

export default function ChatInterface({ userId }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '👋 Hi! I\'m FitBot. How can I help your fitness journey today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://localhost:8000/chat/', {
        user_id: userId,
        message: input,
        chat_history: history
      });

      const botMsg = { role: 'assistant', content: res.data.response };
      setMessages(prev => [...prev, botMsg]);
      setHistory(res.data.chat_history);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant', content: '⚠️ Error connecting to FitBot. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === 'assistant' && <span className="avatar">🤖</span>}
            <div className="bubble">{msg.content}</div>
          </div>
        ))}
        {loading && <div className="message assistant"><div className="bubble typing">FitBot is thinking...</div></div>}
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask FitBot anything about fitness, nutrition, or wellness..."
        />
        <button onClick={sendMessage} disabled={loading}>Send</button>
      </div>
    </div>
  );
}
```

---

## 15. Testing & Demo

### Step 15.1 — Test Each Agent

```bash
# Test via FastAPI Swagger UI
open http://localhost:8000/docs

# Test onboarding
curl -X POST http://localhost:8000/users/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user_001",
    "name": "Rahul",
    "age": 28,
    "gender": "male",
    "weight_kg": 80,
    "height_cm": 175,
    "fitness_goal": "weight_loss",
    "activity_level": "moderate",
    "dietary_pref": "vegetarian",
    "location": "Hyderabad, India"
  }'

# Test chat
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "message": "Give me a 3-day workout plan", "chat_history": []}'
```

### Step 15.2 — Demo Flow for Hackathon

```
1. 📋 Show Onboarding Form (user fills profile)
2. 💪 Ask: "Create a workout plan for this week"  → Workout Agent
3. 🥗 Ask: "What should I eat for breakfast today?" → Nutrition Agent
4. 📍 Ask: "Find gyms near me"                     → Location Agent
5. 📊 Ask: "How is my progress this month?"        → Progress Agent
6. 🧘 Ask: "I'm feeling stressed and can't sleep"  → Assistant Agent (Wellness)
7. 📈 Show Dashboard with progress charts
```

### Step 15.3 — Checklist Before Demo

- [ ] `.env` configured with valid API keys
- [ ] RAG documents ingested (`python -m backend.rag.ingestion`)
- [ ] Database initialized (tables created)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Test user profile created
- [ ] All 5 chat intents tested

---

## ⚡ Quick Start Commands

```bash
# 1. Clone / setup project
cd fitness-wellness-agent

# 2. Backend setup
cd backend
pip install -r requirements.txt
python -m backend.rag.ingestion          # Ingest knowledge docs

# 3. Start backend
uvicorn backend.api.main:app --reload --port 8000

# 4. Frontend setup
cd ../frontend
npm install
npm start                                 # Runs on localhost:3000
```

---

> **💡 Tip:** For the hackathon demo, prioritize the Chat Interface (Module 6) as it showcases all agents through a unified conversational UX. The Orchestrator's intent routing will impress judges by demonstrating true multi-agent behavior.
