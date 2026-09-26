from langgraph.graph import StateGraph, END
from backend.agents import FitnessAgentState
from backend.agents.workout_agent import workout_agent_node
from backend.agents.nutrition_agent import nutrition_agent_node
from backend.agents.location_agent import location_agent_node
from backend.agents.progress_agent import progress_agent_node
from backend.agents.assistant_agent import assistant_agent_node
from backend.config import generate_content_safe

INTENT_PROMPT = """
Classify this user message into ONE of these intents:
- workout:    User asks about exercises, workouts, or training plans
- nutrition:  User asks about diet, meals, food, or calories
- gym_finder: User wants to find gyms or fitness centers nearby
- progress:   User asks about their progress, stats, or history
- general:    General fitness/wellness questions, motivation, or anything else

User message: "{message}"

Respond with ONLY the intent word (lowercase). No explanation.
"""


def classify_intent_fast(message: str) -> str:
    msg = message.lower()
    if any(k in msg for k in ["gym", "gyms", "fitness center", "find gym", "locate gym"]):
        return "gym_finder"
    if any(k in msg for k in ["workout", "routine", "exercise", "training plan", "sets", "reps", "muscle gain plan", "leg day"]):
        return "workout"
    if any(k in msg for k in ["meal", "diet", "nutrition", "calorie", "protein", "carbs", "food plan", "macros"]):
        return "nutrition"
    if any(k in msg for k in ["progress", "weight log", "summary", "stats", "streak"]):
        return "progress"
    return ""


def intent_classifier_node(state: FitnessAgentState) -> FitnessAgentState:
    """Classify user intent and route to the correct sub-agent."""
    fast = classify_intent_fast(state["user_message"])
    if fast:
        return {**state, "intent": fast}

    try:
        prompt = INTENT_PROMPT.format(message=state["user_message"])
        text = generate_content_safe(prompt)
        intent = text.strip().lower()
        if intent not in {"workout", "nutrition", "gym_finder", "progress", "general"}:
            intent = "general"
        return {**state, "intent": intent}
    except Exception:
        return {**state, "intent": "general"}


def route_to_agent(state: FitnessAgentState) -> str:
    routing = {
        "workout":    "workout_agent",
        "nutrition":  "nutrition_agent",
        "gym_finder": "location_agent",
        "progress":   "progress_agent",
        "general":    "assistant_agent",
    }
    return routing.get(state["intent"], "assistant_agent")


def build_fitness_graph():
    graph = StateGraph(FitnessAgentState)

    graph.add_node("intent_classifier", intent_classifier_node)
    graph.add_node("workout_agent",     workout_agent_node)
    graph.add_node("nutrition_agent",   nutrition_agent_node)
    graph.add_node("location_agent",    location_agent_node)
    graph.add_node("progress_agent",    progress_agent_node)
    graph.add_node("assistant_agent",   assistant_agent_node)

    graph.set_entry_point("intent_classifier")

    graph.add_conditional_edges(
        "intent_classifier",
        route_to_agent,
        {
            "workout_agent":   "workout_agent",
            "nutrition_agent": "nutrition_agent",
            "location_agent":  "location_agent",
            "progress_agent":  "progress_agent",
            "assistant_agent": "assistant_agent",
        }
    )

    for agent in ["workout_agent", "nutrition_agent", "location_agent",
                  "progress_agent", "assistant_agent"]:
        graph.add_edge(agent, END)

    return graph.compile()


# Singleton — compiled once at startup
fitness_graph = build_fitness_graph()
