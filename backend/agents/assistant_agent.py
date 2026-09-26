import google.generativeai as genai
from backend.config import GOOGLE_API_KEY
from backend.rag.retriever import retrieve_context

genai.configure(api_key=GOOGLE_API_KEY)

FITBOT_SYSTEM_PROMPT = """
You are FitBot, a friendly, knowledgeable, and empathetic AI fitness & wellness coach for WellnessMitra.

You help users with:
- Workout advice, exercise form, and training tips
- Nutrition guidance and healthy eating habits
- Motivation, accountability, and mindset coaching
- Injury prevention and basic recovery advice
- Sleep quality, stress management, and mindfulness
- General wellness and lifestyle improvement

User Profile:
- Name: {name}
- Age: {age} | Gender: {gender}
- Fitness Goal: {fitness_goal}
- Activity Level: {activity_level}
- Dietary Preference: {dietary_pref}

Relevant Knowledge:
{rag_context}

Guidelines:
- Respond in a warm, encouraging, and professional tone
- Be specific and actionable, not generic
- Keep responses concise (3-5 sentences for simple Q&A, more for plans)
- Always prioritize safety — recommend consulting a doctor for medical concerns
- Remember: you are their friend and coach, not just a chatbot
"""


def assistant_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    chat_history = state.get("chat_history", [])
    user_message = state["user_message"]

    # Retrieve relevant fitness/wellness knowledge
    rag_context = retrieve_context(query=user_message, collection="general")

    system_instruction = FITBOT_SYSTEM_PROMPT.format(
        name=profile.get("name", "there"),
        age=profile.get("age", "N/A"),
        gender=profile.get("gender", "N/A"),
        fitness_goal=profile.get("fitness_goal", "general wellness"),
        activity_level=profile.get("activity_level", "moderate"),
        dietary_pref=profile.get("dietary_pref", "none"),
        rag_context=rag_context or "No specific knowledge retrieved."
    )

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction=system_instruction
    )

    # Build history in Gemini format
    history = [
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in chat_history
        if msg.get("role") in {"user", "model"}
    ]

    chat = model.start_chat(history=history)
    response = chat.send_message(user_message)

    updated_history = chat_history + [
        {"role": "user",  "content": user_message},
        {"role": "model", "content": response.text}
    ]

    return {
        **state,
        "chat_history": updated_history,
        "response": response.text,
        "rag_context": rag_context
    }
