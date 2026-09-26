import google.generativeai as genai
from backend.config import GOOGLE_API_KEY
from backend.rag.retriever import retrieve_context

genai.configure(api_key=GOOGLE_API_KEY)

WORKOUT_SYSTEM_PROMPT = """
You are an expert personal fitness trainer and certified strength & conditioning coach.

User Profile:
- Name: {name}
- Age: {age} | Gender: {gender}
- Weight: {weight} kg | Height: {height} cm
- Fitness Goal: {fitness_goal}
- Activity Level: {activity_level}
- Days Available Per Week: {days}
- Equipment: {equipment}
- Medical Notes: {medical_notes}

Fitness Knowledge Base:
{rag_context}

Create a detailed, safe, and progressive weekly workout plan. For each exercise include:
1. Exercise name and target muscles
2. Sets x Reps (or duration)
3. Rest period
4. Form tips
5. Beginner modifications if needed

Also include warm-up (5 min) and cool-down (5 min) routines.
Format the plan day by day in a clear, readable structure.
"""


def workout_agent_node(state: dict) -> dict:
    profile = state["user_profile"]

    rag_context = retrieve_context(
        query=f"workout plan {profile.get('fitness_goal')} {profile.get('activity_level')}",
        collection="fitness"
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
        equipment=state.get("user_message", "not specified"),
        medical_notes=profile.get("medical_notes", "none"),
        rag_context=rag_context or "No additional context available."
    )

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)

    return {
        **state,
        "workout_plan": response.text,
        "response": response.text,
        "rag_context": rag_context
    }
