import google.generativeai as genai
from backend.config import GOOGLE_API_KEY
from backend.rag.retriever import retrieve_context

genai.configure(api_key=GOOGLE_API_KEY)


def calculate_daily_calories(weight_kg, height_cm, age, gender, activity_level, goal):
    """Harris-Benedict BMR → TDEE → Goal-adjusted calorie target."""
    if str(gender).lower() == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)

    multipliers = {
        "sedentary": 1.2, "light": 1.375,
        "moderate": 1.55, "active": 1.725, "very_active": 1.9
    }
    tdee = bmr * multipliers.get(str(activity_level).lower(), 1.55)

    adjustments = {
        "weight_loss": -500, "muscle_gain": 300,
        "endurance": 200, "flexibility": 0
    }
    return round(tdee + adjustments.get(str(goal).lower(), 0))


NUTRITION_SYSTEM_PROMPT = """
You are a certified nutritionist and registered dietitian.

User Profile:
- Age: {age} | Gender: {gender}
- Weight: {weight} kg | Height: {height} cm
- Fitness Goal: {fitness_goal}
- Daily Calorie Target: {calories} kcal
- Dietary Preference: {dietary_pref}
- Food Allergies: {allergies}

Nutrition Knowledge Base:
{rag_context}

Create a balanced 7-day meal plan with:
1. Breakfast, Lunch, Dinner, and 2 Snacks each day
2. Approximate calories and macros (protein/carbs/fat) per meal
3. Simple preparation tips
4. Daily water intake recommendation
5. A brief list of foods to AVOID based on preferences and allergies

Use locally available Indian ingredients where possible. Keep meals practical and delicious.
"""


def nutrition_agent_node(state: dict) -> dict:
    profile = state["user_profile"]

    try:
        calories = calculate_daily_calories(
            float(profile.get("weight_kg", 70)),
            float(profile.get("height_cm", 170)),
            int(profile.get("age", 25)),
            profile.get("gender", "male"),
            profile.get("activity_level", "moderate"),
            profile.get("fitness_goal", "maintenance")
        )
    except Exception:
        calories = 2000

    rag_context = retrieve_context(
        query=f"meal plan {profile.get('dietary_pref')} {profile.get('fitness_goal')}",
        collection="nutrition"
    )

    prompt = NUTRITION_SYSTEM_PROMPT.format(
        age=profile.get("age", "N/A"),
        gender=profile.get("gender", "N/A"),
        weight=profile.get("weight_kg", "N/A"),
        height=profile.get("height_cm", "N/A"),
        fitness_goal=profile.get("fitness_goal", "general health"),
        calories=calories,
        dietary_pref=profile.get("dietary_pref", "none"),
        allergies=", ".join(profile.get("allergies", [])) or "none",
        rag_context=rag_context or "No additional context available."
    )

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)

    return {
        **state,
        "meal_plan": response.text,
        "response": response.text,
        "rag_context": rag_context
    }
