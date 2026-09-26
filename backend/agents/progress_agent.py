from backend.llm import generate_text
from backend.store import get_weight_logs, get_workout_logs

PROGRESS_PROMPT = """
You are a supportive fitness coach reviewing a user's logged progress.

User Goal: {goal}
Progress Summary:
- Total Workouts: {workouts}
- Total Calories Burned: {calories_burned} kcal
- Weight Change: {weight_change} kg ({direction})
- Current Weight: {current_weight} kg
- Current BMI: {bmi}

Write a short motivating summary, two improvements, and one next step.
"""


def _summary(state: dict) -> dict:
    profile = state["user_profile"]
    user_id = state["user_id"]
    workouts = get_workout_logs(user_id, 30)
    weights = get_weight_logs(user_id, 30)
    calories = sum(log.calories_burned or 0 for log in workouts)
    start = weights[0].weight_kg if weights else profile.get("weight_kg")
    current = weights[-1].weight_kg if weights else profile.get("weight_kg")
    change = round((current or 0) - (start or 0), 2) if start is not None and current is not None else 0
    return {
        "total_workouts": len(workouts),
        "total_calories_burned": round(calories),
        "weight_change": change,
        "current_weight": current,
        "weight_start": start,
    }


def progress_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    progress = _summary(state)
    weight_change = progress["weight_change"]
    direction = "lost" if weight_change < 0 else "gained"
    height_m = float(profile.get("height_cm") or 170) / 100
    current = progress["current_weight"] or 0
    bmi = round(current / (height_m ** 2), 1) if height_m and current else "N/A"
    local = (
        f"Logged progress (last 30 days):\n"
        f"- Workouts: **{progress['total_workouts']}**\n"
        f"- Calories burned: **{progress['total_calories_burned']}**\n"
        f"- Weight: **{progress['weight_start']} kg** → **{progress['current_weight']} kg** "
        f"({abs(weight_change)} kg {direction})\n"
        f"- BMI: **{bmi}**"
    )
    prompt = PROGRESS_PROMPT.format(
        goal=profile.get("fitness_goal", "general fitness"),
        workouts=progress["total_workouts"],
        calories_burned=progress["total_calories_burned"],
        weight_change=abs(weight_change),
        direction=direction,
        current_weight=current,
        bmi=bmi,
    )
    try:
        text = generate_text(prompt)
    except Exception as exc:
        text = f"{local}\n\nGemini request failed: {exc}"
    if not text:
        text = local + "\n\nAdd `GOOGLE_API_KEY` to `.env` for a coached write-up."
    return {**state, "progress_summary": progress, "response": text}
