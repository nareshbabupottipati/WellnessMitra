from backend.config import generate_content_safe

PROGRESS_PROMPT = """
You are a supportive and data-driven fitness coach reviewing a user's progress.

User Goal: {goal}
30-Day Progress Summary:
- Total Workouts Completed: {workouts}
- Total Calories Burned (workouts): {calories_burned} kcal
- Weight Change: {weight_change} kg ({direction})
- Current Weight: {current_weight} kg
- Current BMI: {bmi}
- Workout Streak: {streak} days

Provide:
1. 🎯 A motivating personalized progress summary (2-3 sentences)
2. 🏆 Key achievements this month
3. 📈 Top 2 areas of improvement needed
4. 💡 Specific recommendations for the next 30 days
5. 🌟 An encouraging closing message

Keep the tone warm, specific, and action-oriented.
"""


def progress_agent_node(state: dict) -> dict:
    profile = state["user_profile"]

    # In a real app, fetch from DB. Using mock data for demo.
    progress_data = state.get("progress_summary") or {
        "total_workouts": 12,
        "total_calories_burned": 3600,
        "weight_change": -2.3,
        "current_weight": profile.get("weight_kg", 70),
        "streak": 5
    }

    weight_change = progress_data.get("weight_change", 0)
    direction = "lost" if weight_change < 0 else "gained"
    weight_kg = progress_data.get("current_weight", 70)
    height_m = float(profile.get("height_cm", 170)) / 100
    bmi = round(weight_kg / (height_m ** 2), 1) if height_m > 0 else "N/A"

    prompt = PROGRESS_PROMPT.format(
        goal=profile.get("fitness_goal", "general fitness"),
        workouts=progress_data.get("total_workouts", 0),
        calories_burned=progress_data.get("total_calories_burned", 0),
        weight_change=abs(weight_change),
        direction=direction,
        current_weight=weight_kg,
        bmi=bmi,
        streak=progress_data.get("streak", 0)
    )

    response_text = generate_content_safe(prompt)

    return {**state, "progress_summary": progress_data, "response": response_text}
