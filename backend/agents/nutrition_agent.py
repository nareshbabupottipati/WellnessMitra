

def calculate_daily_calories(weight_kg, height_cm, age, gender, activity_level, goal):
    if str(gender).lower() == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    tdee = bmr * multipliers.get(str(activity_level).lower(), 1.55)
    adjustments = {
        "weight_loss": -500,
        "muscle_gain": 300,
        "endurance": 200,
        "flexibility": 0,
    }
    return round(tdee + adjustments.get(str(goal).lower(), 0))


MEAL_LIBRARY = {
    "vegetarian": [
        ("Breakfast", "🌅", "Vegetable upma, curd, and a banana", 420),
        ("Lunch", "🥗", "Brown rice, dal, mixed veg curry, salad", 620),
        ("Snack", "🍎", "Roasted chana and a fruit", 180),
        ("Dinner", "🌙", "2 chapatis, paneer bhurji, cucumber salad", 540),
    ],
    "vegan": [
        ("Breakfast", "🌅", "Oats with soy milk, berries, and seeds", 400),
        ("Lunch", "🥗", "Millet bowl, chickpea curry, greens", 610),
        ("Snack", "🍎", "Apple and a handful of peanuts", 190),
        ("Dinner", "🌙", "Tofu stir-fry with vegetables and rice", 530),
    ],
    "keto": [
        ("Breakfast", "🌅", "Eggs, spinach, and avocado", 430),
        ("Lunch", "🥗", "Grilled paneer or chicken salad with olive oil", 580),
        ("Snack", "🥜", "Almonds and cheese", 200),
        ("Dinner", "🌙", "Fish or tofu with sautéed vegetables", 540),
    ],
    "paleo": [
        ("Breakfast", "🌅", "Omelette with vegetables and fruit", 410),
        ("Lunch", "🥗", "Grilled chicken, sweet potato, salad", 640),
        ("Snack", "🍎", "Banana and walnuts", 210),
        ("Dinner", "🌙", "Baked fish, vegetables, and olive oil", 520),
    ],
    "none": [
        ("Breakfast", "🌅", "Eggs, toast, and fruit", 430),
        ("Lunch", "🥗", "Rice, dal, chicken or paneer, salad", 650),
        ("Snack", "🍎", "Yogurt and a fruit", 180),
        ("Dinner", "🌙", "Chapati, grilled protein, vegetables", 540),
    ],
}


def build_meal_plan(profile: dict) -> dict:
    try:
        calories = calculate_daily_calories(
            float(profile.get("weight_kg", 70)),
            float(profile.get("height_cm", 170)),
            int(profile.get("age", 25)),
            profile.get("gender", "male"),
            profile.get("activity_level", "moderate"),
            profile.get("fitness_goal", "maintenance"),
        )
    except Exception:
        calories = 2000
    pref = str(profile.get("dietary_pref") or "none").lower()
    meals = MEAL_LIBRARY.get(pref, MEAL_LIBRARY["none"])
    return {
        "calories": calories,
        "dietary_pref": pref,
        "water": "💧 About 2.5–3 litres through the day",
        "meals": [
            {"name": name, "icon": icon, "items": items, "kcal": kcal}
            for name, icon, items, kcal in meals
        ],
    }


def format_meal_plan(plan: dict) -> str:
    lines = [
        f"**Daily target: {plan['calories']} kcal** · {plan['dietary_pref']}",
        "",
    ]
    for meal in plan["meals"]:
        lines.append(f"{meal['icon']} **{meal['name']}** · {meal['kcal']} kcal")
        lines.append(meal["items"])
        lines.append("")
    lines.append(plan["water"])
    return "\n".join(lines).strip()


def nutrition_agent_node(state: dict) -> dict:
    plan = build_meal_plan(state["user_profile"])
    text = format_meal_plan(plan)
    return {**state, "meal_plan": plan, "response": text, "rag_context": None}
