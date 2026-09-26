from backend.config import generate_content_safe
from backend.rag.retriever import retrieve_context
from backend.database.crud import search_foods, get_all_foods, get_food


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

Verified Local Food Database (JSON):
{food_db_context}

Nutrition Knowledge Base:
{rag_context}

Create a balanced 7-day meal plan (or respond accurately to the specific food/nutrition query):
1. Breakfast, Lunch, Dinner, and 2 Snacks each day
2. Approximate calories and macros (protein/carbs/fat) per meal using the verified JSON food data
3. Simple preparation tips
4. Daily water intake recommendation
5. A brief list of foods to AVOID based on preferences and allergies

Use locally available Indian ingredients from the food database where possible. Keep meals practical and delicious.
"""


def nutrition_agent_node(state: dict) -> dict:
    profile = state.get("user_profile", {})
    user_msg = state.get("user_message", "")

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

    # Look up matching foods in local JSON database
    all_foods = get_all_foods()
    matching_foods = []
    if user_msg:
        for f in all_foods:
            if f.get("name", "").lower() in user_msg.lower():
                matching_foods.append(f)

    # If no specific matches, sample staple foods suitable for preferences
    if not matching_foods:
        matching_foods = all_foods[:12]

    food_db_lines = []
    for f in matching_foods[:15]:
        p = f.get("per_100g", {})
        food_db_lines.append(
            f"- {f.get('name')}: {p.get('calories')} kcal, "
            f"Protein: {p.get('protein')}g, Carbs: {p.get('carbs')}g, "
            f"Fat: {p.get('fat')}g, Fiber: {p.get('fiber', 0)}g per 100g"
        )
    food_db_context = "\n".join(food_db_lines)

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
        food_db_context=food_db_context,
        rag_context=rag_context or "No additional context available."
    )

    response_text = generate_content_safe(prompt)

    return {
        **state,
        "meal_plan": response_text,
        "response": response_text,
        "rag_context": rag_context
    }
