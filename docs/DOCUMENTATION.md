
# 🏋️ Fitness & Wellness Agent
### Complete Project Documentation

> **Event:** Agentic AI Mini-Hackathon — Division of Flexible Learning, IIIT Hyderabad
> **Version:** 1.0.0
> **Last Updated:** September 2026

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Multi-Agent Design](#4-multi-agent-design)
5. [Modules & Features](#5-modules--features)
   - [Module 1 — User Profile & Onboarding](#module-1--user-profile--onboarding)
   - [Module 2 — Workout Recommendation](#module-2--workout-recommendation)
   - [Module 3 — Diet & Nutrition](#module-3--diet--nutrition)
   - [Module 4 — Gym & Facility Finder](#module-4--gym--facility-finder)
   - [Module 5 — Progress Tracking](#module-5--progress-tracking)
   - [Module 6 — Conversational AI Assistant](#module-6--conversational-ai-assistant)
   - [Module 7 — Notifications & Reminders](#module-7--notifications--reminders)
   - [Module 8 — Wellness & Mental Health](#module-8--wellness--mental-health)
6. [RAG Pipeline](#6-rag-pipeline)
7. [Data Models](#7-data-models)
8. [API Reference](#8-api-reference)
9. [Project Structure](#9-project-structure)
10. [Environment Setup & Installation](#10-environment-setup--installation)
11. [Running the Application](#11-running-the-application)
12. [Frontend UI Guide](#12-frontend-ui-guide)
13. [Testing Guide](#13-testing-guide)
14. [Demo Walkthrough](#14-demo-walkthrough)
15. [Future Enhancements](#15-future-enhancements)

---

## 1. Project Overview

### 1.1 Problem Statement

> *"An AI-powered personal fitness assistant that provides personalized fitness, nutrition, and wellness guidance based on the user's profile and location."*
> — IIIT-H Agentic AI Mini-Hackathon

### 1.2 What It Does

The **Fitness & Wellness Agent** is an intelligent, multi-agent AI system that acts as a **personal fitness coach, nutritionist, and wellness advisor** — all in one. It understands each user's unique health profile, goals, dietary needs, and location to deliver hyper-personalized guidance through natural conversation.

### 1.3 Key Differentiators

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent AI** | Specialized sub-agents for each domain (workout, nutrition, location, progress) |
| 💬 **Conversational UX** | Chat-first interface with persistent memory across sessions |
| 📍 **Location-Aware** | Real-time nearby gym discovery using Google Places API |
| 📚 **RAG-Powered** | Domain knowledge retrieval for accurate, evidence-based advice |
| 📊 **Progress Intelligence** | AI-generated insights from tracked fitness and nutrition data |
| 🔄 **Adaptive** | Adjusts recommendations based on user feedback and progress |

### 1.4 Target Users

- Individuals starting their fitness journey
- People wanting structured workout and meal plans
- Users looking for gyms or fitness facilities nearby
- Anyone seeking a personalized, conversational wellness companion

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
│    Onboarding · Dashboard · Chat · Workouts · Nutrition · Maps  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼──────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│              REST API · Auth · Session Management               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                            │
│         Intent Classification → Agent Routing (LangGraph)       │
└──┬──────────┬───────────┬──────────┬────────────┬──────────────┘
   │          │           │          │            │
┌──▼───┐ ┌───▼────┐ ┌────▼───┐ ┌────▼────┐ ┌────▼──────┐
│Work- │ │Nutri-  │ │Loca-   │ │Progress │ │Assistant  │
│out   │ │tion    │ │tion    │ │Agent    │ │Agent      │
│Agent │ │Agent   │ │Agent   │ │         │ │           │
└──┬───┘ └───┬────┘ └────┬───┘ └────┬────┘ └────┬──────┘
   │          │           │          │            │
┌──▼──────────▼───────────▼──────────▼────────────▼──────────────┐
│                    SHARED SERVICES LAYER                        │
│   RAG Retriever │ Google Gemini LLM │ Tool Registry             │
└──────────┬──────────────┬───────────────────────────────────────┘
           │              │
    ┌──────▼──────┐  ┌────▼──────────────────────────────────┐
    │  ChromaDB   │  │  External APIs                        │
    │ (Vector DB) │  │  Google Maps · Edamam · Gemini        │
    └─────────────┘  └───────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │  SQLite /   │
    │  PostgreSQL │
    │  (User DB)  │
    └─────────────┘
```

### 2.2 Data Flow

```
User Message
    │
    ▼
[FastAPI] → Validate user session & fetch profile
    │
    ▼
[Orchestrator] → Classify intent (workout / nutrition / gym / progress / general)
    │
    ▼
[Sub-Agent] → Retrieve RAG context + Call external tools
    │
    ▼
[Gemini LLM] → Generate personalized response
    │
    ▼
[FastAPI] → Return response + updated chat history
    │
    ▼
[Frontend] → Display to user
```

---

## 3. Tech Stack

### 3.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **LLM** | Google Gemini 2.0 Flash | Latest | NLU, reasoning, generation |
| **Agent Framework** | LangGraph | 0.2.x | Multi-agent orchestration & state |
| **Embeddings** | Google text-embedding-004 | Latest | RAG vector embeddings |
| **Backend** | FastAPI | 0.111.x | REST API server |
| **Frontend** | React | 18.x | User interface |
| **Vector DB** | ChromaDB | 0.5.x | Knowledge retrieval (RAG) |
| **Database** | SQLite (dev) / PostgreSQL (prod) | — | User data & logs |
| **Maps** | Google Places API | v1 | Nearby gym discovery |
| **Nutrition** | Edamam Food API | v2 | Food & nutrition database |

### 3.2 Python Dependencies

```txt
# backend/requirements.txt
google-generativeai>=0.7.0
google-adk>=0.1.0
langgraph>=0.2.0
langchain-google-genai>=1.0.0
langchain-community>=0.2.0
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
chromadb>=0.5.0
pypdf>=4.0.0
requests>=2.31.0
```

---

## 4. Multi-Agent Design

### 4.1 Agent Overview

| Agent | Trigger Intent | Responsibility |
|-------|---------------|----------------|
| **Orchestrator** | All messages | Classifies intent, routes to correct sub-agent |
| **Workout Agent** | `workout` | Generates personalized workout plans |
| **Nutrition Agent** | `nutrition` | Creates meal plans, macros, dietary advice |
| **Location Agent** | `gym_finder` | Finds nearby gyms using Google Maps |
| **Progress Agent** | `progress` | Analyzes logs, generates fitness insights |
| **Assistant Agent** | `general` / `wellness` | Handles all other Q&A, motivation, wellness |

### 4.2 LangGraph State Schema

```python
class FitnessAgentState(TypedDict):
    user_id:          str            # Unique user identifier
    user_profile:     dict           # Full health profile
    user_message:     str            # Current user input
    intent:           str            # Classified intent
    workout_plan:     Optional[dict] # Generated workout plan
    meal_plan:        Optional[dict] # Generated meal plan
    nearby_gyms:      Optional[list] # Gym search results
    progress_summary: Optional[dict] # Progress analytics
    rag_context:      Optional[str]  # Retrieved knowledge
    chat_history:     List[dict]     # Conversation memory
    response:         str            # Final response to user
```

### 4.3 Intent Classification & Routing

```
User Message → Gemini LLM → Intent Label → Routing
─────────────────────────────────────────────────────
"Give me a leg day workout"       → workout    → Workout Agent
"What should I eat for lunch?"    → nutrition  → Nutrition Agent
"Find gyms near Hitech City"      → gym_finder → Location Agent
"How much weight did I lose?"     → progress   → Progress Agent
"I'm feeling burnt out today"     → general    → Assistant Agent
"Suggest breathing exercises"     → wellness   → Assistant Agent
```

### 4.4 LangGraph Flow Diagram

```
                    ┌─────────────────┐
                    │  START (input)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Intent          │
                    │ Classifier      │
                    └────────┬────────┘
          ┌──────────────────┼──────────────────────┐
          │          ┌───────┘     └───────┐         │
    ┌─────▼────┐ ┌───▼──────┐ ┌───▼─────┐ ┌▼──────┐ ┌▼────────┐
    │ Workout  │ │Nutrition │ │Location │ │Progr- │ │Assist-  │
    │  Agent   │ │  Agent   │ │  Agent  │ │ess    │ │ant      │
    └─────┬────┘ └───┬──────┘ └───┬─────┘ └┬──────┘ └┬────────┘
          └──────────┴────────────┴─────────┴─────────┘
                                   │
                              ┌────▼────┐
                              │   END   │
                              └─────────┘
```

---

## 5. Modules & Features

---

### Module 1 — User Profile & Onboarding

**Purpose:** Capture essential user data to enable fully personalized agent behavior across all modules.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-1.1 | Health Profile Setup | Collect age, weight, height, gender |
| UC-1.2 | Fitness Goal Selection | Weight loss / Muscle gain / Endurance / Flexibility |
| UC-1.3 | Activity Level Assessment | Sedentary → Very Active scale |
| UC-1.4 | Dietary Preferences | Vegan / Vegetarian / Keto / Paleo / None |
| UC-1.5 | Allergy & Restriction Input | Food allergies and medical limitations |
| UC-1.6 | Location Setup | City or coordinates for gym discovery |
| UC-1.7 | Schedule Availability | Days per week + preferred workout times |
| UC-1.8 | Profile Update | Modify any profile data post-onboarding |

#### Key Calculations at Onboarding

```
BMI        = weight(kg) / height(m)²
BMR (Male) = 88.36 + (13.4 × weight) + (4.8 × height) − (5.7 × age)
BMR (Fem.) = 447.6 + (9.2 × weight)  + (3.1 × height) − (4.3 × age)
TDEE       = BMR × Activity Multiplier
```

| Activity Level | Multiplier |
|----------------|-----------|
| Sedentary | 1.2 |
| Lightly Active | 1.375 |
| Moderately Active | 1.55 |
| Very Active | 1.725 |
| Extra Active | 1.9 |

---

### Module 2 — Workout Recommendation

**Purpose:** Generate AI-personalized workout plans tailored to user goals, fitness level, equipment, and schedule.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-2.1 | Weekly Plan Generation | Full 5–7 day workout plan |
| UC-2.2 | Daily Workout Details | Sets, reps, rest periods, target muscles |
| UC-2.3 | Equipment Adaptation | Adjust for home / gym / no equipment |
| UC-2.4 | Warm-up & Cool-down | Pre/post workout routines |
| UC-2.5 | Intensity Adaptation | Easier/harder based on user feedback |
| UC-2.6 | Exercise Substitution | Alternatives for injuries or limitations |
| UC-2.7 | Progression Planning | Week-over-week load progression |
| UC-2.8 | Workout Logging | Log completed workouts with notes |

#### Workout Plan Structure (Output)

```json
{
  "week_1": {
    "monday": {
      "focus": "Upper Body Strength",
      "exercises": [
        {
          "name": "Push-ups",
          "sets": 3,
          "reps": "12-15",
          "rest_seconds": 60,
          "muscles": ["chest", "triceps", "shoulders"],
          "form_tip": "Keep core tight, elbows at 45°"
        }
      ],
      "warm_up": ["Arm circles 30s", "Shoulder rolls 30s"],
      "cool_down": ["Chest stretch 30s", "Tricep stretch 30s"],
      "estimated_duration_mins": 45,
      "calories_burn_estimate": 300
    }
  }
}
```

---

### Module 3 — Diet & Nutrition

**Purpose:** Provide complete, personalized meal plans and nutritional guidance aligned with user fitness goals.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-3.1 | Calorie Target Calculation | TDEE-based daily calorie goal |
| UC-3.2 | Weekly Meal Plan | 7-day plan with all meals and snacks |
| UC-3.3 | Macro Distribution | Protein / Carbs / Fat breakdown per meal |
| UC-3.4 | Dietary Filter | Respect vegan/vegetarian/keto preferences |
| UC-3.5 | Allergy Avoidance | Exclude allergens from all recommendations |
| UC-3.6 | Food Nutrition Lookup | Search nutritional info for any food item |
| UC-3.7 | Recipe Suggestions | Simple recipes with ingredients & steps |
| UC-3.8 | Grocery List | Auto-generate shopping list from meal plan |
| UC-3.9 | Meal Logging | Track daily food intake |
| UC-3.10 | Hydration Guidance | Daily water intake recommendation |

#### Macro Goals by Fitness Objective

| Goal | Protein | Carbs | Fat | Calorie Adjustment |
|------|---------|-------|-----|--------------------|
| Weight Loss | 35% | 40% | 25% | TDEE − 500 kcal |
| Muscle Gain | 30% | 45% | 25% | TDEE + 300 kcal |
| Endurance | 20% | 60% | 20% | TDEE + 200 kcal |
| Maintenance | 25% | 50% | 25% | TDEE |

---

### Module 4 — Gym & Facility Finder

**Purpose:** Discover and compare nearby gyms, fitness centers, yoga studios, and outdoor fitness spots.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-4.1 | Nearby Gym Search | Find gyms within a configurable radius |
| UC-4.2 | Facility Type Filter | Gym / Yoga / Swimming / Crossfit / Park |
| UC-4.3 | Gym Details | Name, address, rating, hours, amenities |
| UC-4.4 | Open Now Filter | Show only currently open facilities |
| UC-4.5 | Distance Sorting | Nearest gyms shown first |
| UC-4.6 | Maps Deep-link | Direct link to Google Maps for directions |
| UC-4.7 | Outdoor Spot Discovery | Parks, running tracks, sports grounds |

#### Google Places API Integration

```
API:     Google Places Nearby Search
Params:  location (lat,lng) · radius (meters) · type=gym
Output:  name · address · rating · open_now · place_id
Maps URL: https://www.google.com/maps/place/?q=place_id:{id}
```

---

### Module 5 — Progress Tracking

**Purpose:** Log, visualize, and analyze fitness and nutrition data to show measurable progress.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-5.1 | Workout Logging | Log exercises, duration, calories burned |
| UC-5.2 | Weight Tracking | Record daily/weekly body weight + BMI |
| UC-5.3 | Meal Logging | Track food items and calorie intake |
| UC-5.4 | Progress Dashboard | Charts: weight trend, workout frequency, calories |
| UC-5.5 | Goal Progress Bar | Visual % completion toward fitness goal |
| UC-5.6 | Weekly Report | AI-generated weekly summary and insights |
| UC-5.7 | Streak Tracking | Consecutive workout days counter |
| UC-5.8 | Plateau Detection | Alert user when progress stalls |
| UC-5.9 | Milestone Badges | Celebrate achievements (first 10 workouts, etc.) |

#### Analytics Metrics

```
Workout Metrics:   total sessions · avg duration · total calories burned
Nutrition Metrics: avg daily calories · macro adherence %
Body Metrics:      weight change · BMI change · trend (improving/plateau/declining)
Consistency Score: workouts completed / workouts planned × 100
```

---

### Module 6 — Conversational AI Assistant

**Purpose:** Primary chat interface offering real-time, multi-turn, personalized fitness and wellness guidance.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-6.1 | Fitness Q&A | Answer any fitness/health question |
| UC-6.2 | Exercise Form Guidance | Explain correct form to prevent injury |
| UC-6.3 | Daily Plan Chat | "Plan my workout for today" via conversation |
| UC-6.4 | Motivation & Coaching | Encouragement and accountability messages |
| UC-6.5 | Injury Advice | General guidance for common minor injuries |
| UC-6.6 | Plateau Solutions | Suggest changes when progress stalls |
| UC-6.7 | Multi-turn Memory | Remember context across conversation turns |
| UC-6.8 | Persona Consistency | Always responds as "FitBot" — warm & professional |

#### Memory Architecture

```
Per Session:   Full chat history passed to Gemini (sliding window)
Cross Session: Last N messages + user profile stored in DB
RAG Context:   Top-3 relevant knowledge chunks injected per message
```

---

### Module 7 — Notifications & Reminders

**Purpose:** Keep users consistent with smart, timely automated nudges.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-7.1 | Workout Reminders | Push notification at scheduled workout time |
| UC-7.2 | Meal Reminders | Notify at breakfast / lunch / dinner times |
| UC-7.3 | Hydration Alerts | Hourly water intake reminders |
| UC-7.4 | Weekly Check-in | Sunday evening goal review prompt |
| UC-7.5 | Streak Warnings | "Don't break your 7-day streak!" alert |
| UC-7.6 | Rest Day Reminders | Auto-detect overtraining and suggest rest |

---

### Module 8 — Wellness & Mental Health

**Purpose:** Holistic wellness support covering sleep, stress, mindfulness, and mental well-being.

#### Use Cases

| ID | Use Case | Description |
|----|----------|-------------|
| UC-8.1 | Sleep Guidance | Optimal sleep duration + hygiene tips |
| UC-8.2 | Stress Management | Breathing exercises, journaling prompts |
| UC-8.3 | Mindfulness Sessions | Guided meditation scripts (5–15 min) |
| UC-8.4 | Recovery Advice | Post-workout recovery optimization |
| UC-8.5 | Burnout Detection | Identify signs of overtraining or mental fatigue |
| UC-8.6 | Mood Check-in | Daily mood logging with AI response |

---

## 6. RAG Pipeline

### 6.1 Overview

The RAG (Retrieval-Augmented Generation) pipeline provides agents with accurate, domain-specific knowledge beyond the LLM's general training data. This ensures recommendations are grounded in established fitness and nutrition science.

### 6.2 Knowledge Document Categories

| Collection | Document | Content |
|-----------|----------|---------|
| `fitness` | `fitness_exercises.txt` | 200+ exercises: description, muscles, benefits, form cues |
| `fitness` | `workout_programs.txt` | HIIT, Strength, Cardio, Yoga, Pilates programs |
| `nutrition` | `nutrition_guidelines.txt` | Macros, micronutrients, meal timing, supplementation |
| `nutrition` | `dietary_plans.txt` | Vegan, keto, Mediterranean diet guides |
| `general` | `wellness_tips.txt` | Sleep, stress, hydration, recovery |
| `general` | `injury_prevention.txt` | Common injuries, prevention, rehab exercises |

### 6.3 Pipeline Steps

```
Step 1: LOAD
  Read raw .txt / .pdf documents from knowledge_docs/

Step 2: CHUNK
  RecursiveCharacterTextSplitter
  chunk_size=500 tokens · overlap=50 tokens

Step 3: EMBED
  Google text-embedding-004 → 768-dim vectors

Step 4: STORE
  ChromaDB persistent store (./chroma_db/)
  Separate collection per domain

Step 5: RETRIEVE (at query time)
  Embed user query → cosine similarity search → top-3 chunks

Step 6: INJECT
  Prepend retrieved chunks into agent system prompt as context
```

### 6.4 Retrieval Quality

| Parameter | Value | Reason |
|-----------|-------|--------|
| Chunk Size | 500 tokens | Enough context without noise |
| Overlap | 50 tokens | Prevents information loss at boundaries |
| Top-K | 3 chunks | Balanced context without overloading prompt |
| Similarity | Cosine | Standard for semantic similarity |

---

## 7. Data Models

### 7.1 User

```python
class User:
    id:             str      # UUID
    name:           str
    age:            int
    gender:         str      # male | female | other
    weight_kg:      float
    height_cm:      float
    fitness_goal:   str      # weight_loss | muscle_gain | endurance | flexibility
    activity_level: str      # sedentary | light | moderate | active | very_active
    dietary_pref:   str      # vegan | vegetarian | keto | paleo | none
    allergies:      list     # ["nuts", "gluten", "dairy"]
    location:       str      # "Hyderabad, India" or "17.385,78.486"
    days_per_week:  int      # workout days available (1-7)
    medical_notes:  str      # optional free text
    created_at:     datetime
    updated_at:     datetime
```

### 7.2 Workout Log

```python
class WorkoutLog:
    id:              int      # auto-increment
    user_id:         str      # FK → User
    date:            date
    exercises:       list     # [{"name", "sets", "reps", "weight_kg"}]
    duration_mins:   int
    calories_burned: float
    intensity:       str      # low | medium | high
    notes:           str
```

### 7.3 Meal Log

```python
class MealLog:
    id:             int
    user_id:        str
    date:           date
    meal_type:      str      # breakfast | lunch | dinner | snack
    foods:          list     # [{"name", "quantity_g", "calories", "protein", "carbs", "fat"}]
    total_calories: float
    total_protein:  float
    total_carbs:    float
    total_fat:      float
```

### 7.4 Weight Log

```python
class WeightLog:
    id:         int
    user_id:    str
    date:       date
    weight_kg:  float
    bmi:        float        # auto-calculated
```

### 7.5 Chat Session

```python
class ChatSession:
    id:          str         # session UUID
    user_id:     str
    created_at:  datetime
    messages:    list        # [{"role": "user"|"model", "content": str, "timestamp": datetime}]
```

---

## 8. API Reference

### 8.1 Base URL

```
Development:  http://localhost:8000
Production:   https://api.fitwellness-agent.com
```

### 8.2 Endpoints

#### 👤 User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/onboard` | Create new user profile |
| `GET` | `/users/{user_id}/profile` | Get user profile |
| `PUT` | `/users/{user_id}/profile` | Update user profile |

**POST /users/onboard — Request Body**
```json
{
  "name": "Rahul Sharma",
  "age": 28,
  "gender": "male",
  "weight_kg": 80.5,
  "height_cm": 175,
  "fitness_goal": "weight_loss",
  "activity_level": "moderate",
  "dietary_pref": "vegetarian",
  "allergies": ["nuts"],
  "location": "Hyderabad, India",
  "days_per_week": 4
}
```

**Response**
```json
{
  "status": "success",
  "user_id": "usr_a1b2c3d4",
  "bmi": 26.3,
  "daily_calorie_target": 1850
}
```

---

#### 💬 Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat/` | Send message to fitness agent |
| `GET` | `/chat/{user_id}/history` | Get conversation history |
| `DELETE` | `/chat/{user_id}/history` | Clear conversation history |

**POST /chat/ — Request Body**
```json
{
  "user_id": "usr_a1b2c3d4",
  "message": "Create a 3-day beginner workout plan for me",
  "chat_history": []
}
```

**Response**
```json
{
  "response": "Here's your personalized 3-day beginner workout plan...",
  "intent": "workout",
  "chat_history": [
    {"role": "user",  "content": "Create a 3-day beginner workout plan for me"},
    {"role": "model", "content": "Here's your personalized 3-day beginner workout plan..."}
  ]
}
```

---

#### 💪 Workout Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workouts/generate` | Generate personalized workout plan |
| `POST` | `/workouts/log` | Log a completed workout |
| `GET` | `/workouts/{user_id}/logs` | Get workout history |
| `GET` | `/workouts/{user_id}/plan` | Get current workout plan |

---

#### 🥗 Nutrition Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/nutrition/meal-plan` | Generate 7-day meal plan |
| `POST` | `/nutrition/log-meal` | Log a meal |
| `GET` | `/nutrition/{user_id}/logs` | Get meal history |
| `GET` | `/nutrition/food-info?q={food}` | Look up food nutritional info |

---

#### 📍 Gym Finder Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/gyms/nearby?location={loc}&radius={r}` | Find nearby gyms |
| `GET` | `/gyms/{place_id}/details` | Get gym details |

**GET /gyms/nearby — Response**
```json
{
  "location": "Hyderabad, India",
  "gyms": [
    {
      "name": "Gold's Gym Banjara Hills",
      "address": "Road No. 12, Banjara Hills",
      "rating": 4.3,
      "open_now": true,
      "distance_km": 1.2,
      "maps_url": "https://www.google.com/maps/place/?q=place_id:ChIJ..."
    }
  ]
}
```

---

#### 📊 Progress Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/progress/weight` | Log body weight |
| `GET` | `/progress/{user_id}/summary` | Get 30-day progress summary |
| `GET` | `/progress/{user_id}/charts` | Get chart data (weight, calories) |
| `GET` | `/progress/{user_id}/report` | AI-generated weekly report |

---

## 9. Project Structure

```
fitness-wellness-agent/
│
├── backend/
│   ├── agents/
│   │   ├── __init__.py              # FitnessAgentState TypedDict
│   │   ├── orchestrator.py          # LangGraph graph builder + intent classifier
│   │   ├── workout_agent.py         # Workout plan generation
│   │   ├── nutrition_agent.py       # Meal plan + calorie calculator
│   │   ├── location_agent.py        # Google Maps gym search
│   │   ├── progress_agent.py        # Analytics + AI insights
│   │   └── assistant_agent.py       # Conversational Q&A + memory
│   │
│   ├── tools/
│   │   ├── maps_tool.py             # Google Places API wrapper
│   │   ├── nutrition_tool.py        # Edamam Food API wrapper
│   │   └── progress_tool.py         # DB read/write helpers
│   │
│   ├── rag/
│   │   ├── ingestion.py             # Document loader + embedder
│   │   ├── retriever.py             # Vector search function
│   │   └── knowledge_docs/
│   │       ├── fitness_exercises.txt
│   │       ├── workout_programs.txt
│   │       ├── nutrition_guidelines.txt
│   │       ├── wellness_tips.txt
│   │       └── injury_prevention.txt
│   │
│   ├── models/
│   │   ├── user.py                  # User SQLAlchemy model
│   │   ├── workout.py               # WorkoutLog model
│   │   ├── nutrition.py             # MealLog model
│   │   └── weight.py                # WeightLog model
│   │
│   ├── database/
│   │   ├── db.py                    # SQLAlchemy engine + session
│   │   └── crud.py                  # CRUD operations
│   │
│   ├── api/
│   │   ├── main.py                  # FastAPI app + CORS + router inclusion
│   │   └── routes/
│   │       ├── user_routes.py
│   │       ├── chat_routes.py
│   │       ├── workout_routes.py
│   │       ├── nutrition_routes.py
│   │       ├── gym_routes.py
│   │       └── progress_routes.py
│   │
│   ├── config.py                    # Environment config loader
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx    # Chat bubble UI
│   │   │   ├── WorkoutCard.jsx      # Workout plan display
│   │   │   ├── MealCard.jsx         # Meal plan display
│   │   │   ├── GymCard.jsx          # Gym listing card
│   │   │   ├── ProgressChart.jsx    # Recharts weight/calorie graphs
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── OnboardingPage.jsx   # Multi-step profile form
│   │   │   ├── DashboardPage.jsx    # Overview + quick actions
│   │   │   ├── ChatPage.jsx         # Main AI chat interface
│   │   │   ├── WorkoutPage.jsx      # Workout plan + log
│   │   │   ├── NutritionPage.jsx    # Meal plan + food log
│   │   │   ├── GymFinderPage.jsx    # Map + gym listings
│   │   │   └── ProgressPage.jsx     # Charts + analytics
│   │   ├── services/
│   │   │   └── api.js               # Axios API call helpers
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
├── chroma_db/                       # ChromaDB persistent vector store
├── .env                             # API keys & config
└── README.md
```

---

## 10. Environment Setup & Installation

### 10.1 Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10+ |
| Node.js | 18+ |
| npm | 9+ |
| Git | Any |

### 10.2 API Keys Required

| API | Where to Get | Free Tier |
|-----|-------------|-----------|
| Google Gemini | [aistudio.google.com](https://aistudio.google.com) | ✅ Yes |
| Google Maps / Places | [console.cloud.google.com](https://console.cloud.google.com) | ✅ $200/mo credit |
| Edamam Food API | [developer.edamam.com](https://developer.edamam.com) | ✅ Yes (1000 calls/mo) |

### 10.3 `.env` Configuration

```env
# ── Google AI ──────────────────────────────────────
GOOGLE_API_KEY=AIza...your_gemini_key

# ── Google Maps ────────────────────────────────────
GOOGLE_MAPS_API_KEY=AIza...your_maps_key

# ── Edamam Nutrition API ───────────────────────────
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key

# ── Database ───────────────────────────────────────
DATABASE_URL=sqlite:///./fitness_agent.db

# ── Application ────────────────────────────────────
APP_ENV=development
APP_SECRET_KEY=your_random_secret_key_here
CORS_ORIGINS=http://localhost:3000
```

### 10.4 Backend Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/fitness-wellness-agent.git
cd fitness-wellness-agent

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / Mac

# 3. Install Python dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment
cp ../.env.example ../.env
# Edit .env with your API keys

# 5. Ingest RAG knowledge documents (run once)
python -m rag.ingestion
```

### 10.5 Frontend Installation

```bash
cd frontend
npm install
```

---

## 11. Running the Application

### 11.1 Start Backend

```bash
# From project root
cd backend
uvicorn api.main:app --reload --port 8000
```

**Verify:** Open http://localhost:8000/docs — Swagger UI should show all API endpoints.

### 11.2 Start Frontend

```bash
# From project root
cd frontend
npm start
```

**Verify:** Open http://localhost:3000 — React app should load.

### 11.3 Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "agents": "ready", "rag": "loaded"}
```

---

## 12. Frontend UI Guide

### 12.1 Page Map

| Page | Route | Description |
|------|-------|-------------|
| Onboarding | `/onboard` | 4-step profile setup wizard |
| Dashboard | `/dashboard` | Overview: calories, streak, quick actions |
| Chat | `/chat` | Main AI assistant conversation |
| Workout | `/workout` | Weekly plan + log completed workouts |
| Nutrition | `/nutrition` | Meal plan + food diary + macros |
| Gym Finder | `/gyms` | Map + nearby gym listings |
| Progress | `/progress` | Charts: weight, calories, workouts |

### 12.2 Onboarding Flow (4 Steps)

```
Step 1: Personal Info   → Name, Age, Gender, Location
Step 2: Body Metrics    → Weight, Height (BMI auto-calculated)
Step 3: Fitness Goals   → Goal type + Activity level + Days/week
Step 4: Diet & Health   → Dietary preference + Allergies + Medical notes
                          → "Get Started" → Dashboard
```

### 12.3 Chat Interface Features

```
┌─────────────────────────────────────────────┐
│  🤖 FitBot                            ⚙️   │
├─────────────────────────────────────────────┤
│                                             │
│  🤖 Hi! I'm FitBot. How can I help?         │
│                                             │
│  👤 Give me a chest workout for today        │
│                                             │
│  🤖 Great! Here's your chest workout:       │
│     1. Bench Press — 3×10                   │
│     2. Push-ups — 3×15                      │
│     ...                                     │
│                                             │
├─────────────────────────────────────────────┤
│  [Ask anything about fitness...        ] 📤 │
│  💪 Workout  🥗 Nutrition  📍 Gyms  📊 Log  │
└─────────────────────────────────────────────┘
```

---

## 13. Testing Guide

### 13.1 Testing Each Agent

```bash
# Test user onboarding
curl -X POST http://localhost:8000/users/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul", "age": 28, "gender": "male",
    "weight_kg": 80, "height_cm": 175,
    "fitness_goal": "weight_loss", "activity_level": "moderate",
    "dietary_pref": "vegetarian", "allergies": [],
    "location": "Hyderabad, India", "days_per_week": 4
  }'

# Test Workout Agent
curl -X POST http://localhost:8000/chat/ \
  -d '{"user_id":"usr_001","message":"Create a 3-day workout plan","chat_history":[]}'

# Test Nutrition Agent
curl -X POST http://localhost:8000/chat/ \
  -d '{"user_id":"usr_001","message":"What should I eat to lose weight?","chat_history":[]}'

# Test Gym Finder Agent
curl -X POST http://localhost:8000/chat/ \
  -d '{"user_id":"usr_001","message":"Find gyms near me","chat_history":[]}'

# Test Progress Agent
curl -X POST http://localhost:8000/chat/ \
  -d '{"user_id":"usr_001","message":"Show my progress this month","chat_history":[]}'

# Test Assistant Agent (Wellness)
curl -X POST http://localhost:8000/chat/ \
  -d '{"user_id":"usr_001","message":"I feel stressed and cant sleep","chat_history":[]}'
```

### 13.2 Swagger UI Testing

Open http://localhost:8000/docs and test all endpoints interactively.

### 13.3 Pre-Demo Checklist

- [ ] `.env` file configured with valid API keys
- [ ] RAG ingestion completed (`python -m rag.ingestion`)
- [ ] Database initialized (tables auto-created on startup)
- [ ] Test user profile created via `/users/onboard`
- [ ] All 5 intents tested via `/chat/`
- [ ] Gym search returns results for your demo location
- [ ] Frontend loads at http://localhost:3000
- [ ] Progress charts render correctly

---

## 14. Demo Walkthrough

### Recommended 10-Minute Demo Flow

```
00:00 — 01:00  │ INTRO
                │ "Meet FitBot — your AI personal trainer, nutritionist & wellness coach"
                │ Show the architecture slide (multi-agent system)

01:00 — 02:30  │ ONBOARDING
                │ Fill out the 4-step profile form live
                │ Highlight: BMI calculation, calorie target shown instantly

02:30 — 04:00  │ WORKOUT AGENT
                │ Type: "Create a 4-day muscle building workout plan"
                │ Show: Structured weekly plan with exercises, sets, reps

04:00 — 05:30  │ NUTRITION AGENT
                │ Type: "Design a vegetarian meal plan for weight loss"
                │ Show: 7-day plan with macros, calorie breakdown

05:30 — 06:30  │ GYM FINDER AGENT
                │ Type: "Find gyms near Hitech City, Hyderabad"
                │ Show: List of gyms with ratings + Google Maps links

06:30 — 07:30  │ PROGRESS AGENT
                │ Log a mock workout → Show dashboard chart
                │ Type: "How am I doing this month?"
                │ Show: AI-generated progress summary

07:30 — 08:30  │ WELLNESS ASSISTANT
                │ Type: "I'm feeling burnt out and stressed after workouts"
                │ Show: Empathetic, personalized wellness advice

08:30 — 09:30  │ MULTI-TURN MEMORY
                │ Continue conversation showing context retention
                │ "What did you recommend earlier for stress?"

09:30 — 10:00  │ CLOSE
                │ Highlight: Multi-agent routing · RAG accuracy · Personalization
```

---

## 15. Future Enhancements

| Enhancement | Priority | Complexity |
|-------------|----------|-----------|
| 📱 Mobile App (React Native) | High | Medium |
| ⌚ Wearable Integration (Fitbit/Apple Watch) | High | High |
| 🍽️ Food Photo Calorie Estimation (Vision AI) | Medium | Medium |
| 🏃 Real-time Form Correction (Pose Detection) | Medium | High |
| 👥 Social Features (Challenges, Leaderboards) | Medium | Medium |
| 🩺 Doctor / Nutritionist Integration | Low | High |
| 🌐 Multilingual Support | Low | Low |
| 🔊 Voice Interface | Medium | Medium |
| 📅 Google Calendar Sync | Low | Low |
| 💊 Supplement Tracking | Low | Low |

---

## Appendix — Glossary

| Term | Definition |
|------|-----------|
| **BMR** | Basal Metabolic Rate — calories burned at rest |
| **TDEE** | Total Daily Energy Expenditure — total calories burned per day |
| **BMI** | Body Mass Index — weight(kg) / height(m)² |
| **Macro** | Macronutrient — Protein, Carbohydrates, or Fat |
| **RAG** | Retrieval-Augmented Generation — fetching relevant knowledge before generating |
| **LangGraph** | Framework for building stateful multi-agent AI workflows |
| **ChromaDB** | Open-source vector database for semantic search |
| **HIIT** | High-Intensity Interval Training |
| **Multi-Agent** | Multiple specialized AI agents working together under an orchestrator |

---

*Documentation generated for the IIIT-H Agentic AI Mini-Hackathon.*
*Built with ❤️ using Google Gemini · LangGraph · FastAPI · React*
