from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.agents.orchestrator import fitness_graph
from backend.store import get_user

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id: str
    message: str
    chat_history: Optional[List[dict]] = []


@router.post("/")
def chat(req: ChatRequest):
    user = get_user(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please complete onboarding first.")

    user_profile = {
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "weight_kg": user.weight_kg,
        "height_cm": user.height_cm,
        "fitness_goal": user.fitness_goal,
        "activity_level": user.activity_level,
        "dietary_pref": user.dietary_pref,
        "allergies": user.allergies or [],
        "location": user.location,
        "days_per_week": user.days_per_week,
        "medical_notes": user.medical_notes or "",
    }
    result = fitness_graph.invoke({
        "user_id": req.user_id,
        "user_profile": user_profile,
        "user_message": req.message,
        "intent": "",
        "workout_plan": None,
        "meal_plan": None,
        "nearby_gyms": None,
        "progress_summary": None,
        "rag_context": None,
        "chat_history": req.chat_history or [],
        "response": "",
    })
    return {
        "response": result["response"],
        "intent": result.get("intent", "general"),
        "chat_history": result.get("chat_history", []),
    }


@router.get("/{user_id}/history")
def get_history(user_id: str):
    if not get_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "message": "Chat history is kept in the browser for this demo."}
