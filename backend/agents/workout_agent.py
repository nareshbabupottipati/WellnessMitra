from backend.llm import generate_text
from backend.rag.retriever import retrieve_context

WORKOUT_SYSTEM_PROMPT = """
You are an expert personal fitness trainer.

User Profile:
- Name: {name}
- Age: {age} | Gender: {gender}
- Weight: {weight} kg | Height: {height} cm
- Fitness Goal: {fitness_goal}
- Activity Level: {activity_level}
- Days Available Per Week: {days}
- Medical Notes: {medical_notes}

Fitness Knowledge Base:
{rag_context}

Create a safe weekly workout plan. For each exercise include sets, reps, rest, and a form tip.
Include a short warm-up and cool-down. Format the plan day by day.
"""


def workout_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    rag_context = retrieve_context(
        query=f"workout plan {profile.get('fitness_goal')} {state.get('user_message', '')}",
        collection="fitness",
    )
    prompt = WORKOUT_SYSTEM_PROMPT.format(
        name=profile.get("name", "User"),
        age=profile.get("age", "N/A"),
        gender=profile.get("gender", "N/A"),
        weight=profile.get("weight_kg", "N/A"),
        height=profile.get("height_cm", "N/A"),
        fitness_goal=profile.get("fitness_goal", "general fitness"),
        activity_level=profile.get("activity_level", "moderate"),
        days=profile.get("days_per_week", 3),
        medical_notes=profile.get("medical_notes", "none"),
        rag_context=rag_context or "No additional context available.",
    )
    try:
        text = generate_text(prompt)
    except Exception as exc:
        text = f"Gemini request failed: {exc}"
    if not text:
        text = (
            "Gemini is not configured, so this is a local starter plan from the knowledge notes.\n\n"
            f"{rag_context}\n\n"
            "Add `GOOGLE_API_KEY` to `.env` for a full personalized plan."
        )
    return {**state, "workout_plan": text, "response": text, "rag_context": rag_context}
