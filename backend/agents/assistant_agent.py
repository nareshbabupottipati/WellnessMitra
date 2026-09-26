from backend.llm import generate_text
from backend.rag.retriever import retrieve_context

FITBOT_SYSTEM_PROMPT = """
You are FitBot, a friendly fitness and wellness coach for WellnessMitra.

User Profile:
- Name: {name}
- Age: {age} | Gender: {gender}
- Fitness Goal: {fitness_goal}
- Activity Level: {activity_level}
- Dietary Preference: {dietary_pref}

Relevant Knowledge:
{rag_context}

Be specific, concise, and safety-conscious. Recommend a doctor for medical concerns.
"""


def assistant_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    chat_history = state.get("chat_history") or []
    user_message = state["user_message"]
    rag_context = retrieve_context(query=user_message, collection="general")
    system = FITBOT_SYSTEM_PROMPT.format(
        name=profile.get("name", "there"),
        age=profile.get("age", "N/A"),
        gender=profile.get("gender", "N/A"),
        fitness_goal=profile.get("fitness_goal", "general wellness"),
        activity_level=profile.get("activity_level", "moderate"),
        dietary_pref=profile.get("dietary_pref", "none"),
        rag_context=rag_context or "No specific knowledge retrieved.",
    )
    history_lines = []
    for message in chat_history[-6:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        if content:
            history_lines.append(f"{role}: {content[:240]}")
    prompt = "\n".join(history_lines + [f"user: {user_message}"]).strip()
    try:
        text = generate_text(prompt, system=system)
    except Exception as exc:
        text = f"Gemini request failed: {exc}"
    if not text:
        text = (
            "Gemini is not configured yet. Here is a relevant note from the local knowledge files:\n\n"
            f"{rag_context}\n\n"
            "Add `GOOGLE_API_KEY` to `.env` and restart the API for full coach replies."
        )
    updated_history = chat_history + [
        {"role": "user", "content": user_message},
        {"role": "model", "content": text},
    ]
    return {**state, "chat_history": updated_history, "response": text, "rag_context": rag_context}
