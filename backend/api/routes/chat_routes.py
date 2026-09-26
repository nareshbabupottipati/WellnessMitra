from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database.db import get_db
from backend.database.crud import get_user
from backend.agents.orchestrator import fitness_graph

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    user_id:      Optional[str] = "usr_demo123"
    message:      str
    chat_history: Optional[List[dict]] = []


@router.post("/")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message to the WellnessMitra AI agent.
    The orchestrator classifies intent and routes to the correct sub-agent.
    """
    effective_user_id = req.user_id if (req.user_id and req.user_id.strip()) else "usr_demo123"
    user = get_user(db, effective_user_id)
    if not user:
        user = get_user(db, "usr_demo123")

    if user:
        user_profile = {
            "name":           user.name,
            "age":            user.age,
            "gender":         user.gender,
            "weight_kg":      user.weight_kg,
            "height_cm":      user.height_cm,
            "fitness_goal":   user.fitness_goal,
            "activity_level": user.activity_level,
            "dietary_pref":   user.dietary_pref,
            "allergies":      user.allergies or [],
            "location":       user.location,
            "days_per_week":  user.days_per_week,
            "medical_notes":  user.medical_notes or ""
        }
    else:
        user_profile = {
            "name":           "Friend",
            "age":            25,
            "gender":         "male",
            "weight_kg":      70.0,
            "height_cm":      170.0,
            "fitness_goal":   "general_fitness",
            "activity_level": "moderate",
            "dietary_pref":   "none",
            "allergies":      [],
            "location":       "Hyderabad, India",
            "days_per_week":  3,
            "medical_notes":  ""
        }

    initial_state = {
        "user_id":          req.user_id,
        "user_profile":     user_profile,
        "user_message":     req.message,
        "intent":           "",
        "workout_plan":     None,
        "meal_plan":        None,
        "nearby_gyms":      None,
        "progress_summary": None,
        "rag_context":      None,
        "chat_history":     req.chat_history,
        "response":         ""
    }

    result = fitness_graph.invoke(initial_state)

    return {
        "response":     result["response"],
        "intent":       result.get("intent", "general"),
        "chat_history": result.get("chat_history", [])
    }


@router.get("/{user_id}/history")
def get_history(user_id: str, db: Session = Depends(get_db)):
    """Get conversation hints — in production, store sessions in DB."""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "message": "Chat history stored client-side in this version."}
