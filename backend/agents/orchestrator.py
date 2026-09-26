from langgraph.graph import StateGraph, END
from backend.agents import FitnessAgentState
from backend.agents.workout_agent import workout_agent_node
from backend.agents.nutrition_agent import nutrition_agent_node
from backend.agents.location_agent import location_agent_node
from backend.agents.progress_agent import progress_agent_node
from backend.agents.assistant_agent import assistant_agent_node
import google.generativeai as genai
from backend.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

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


def intent_classifier_node(state: FitnessAgentState) -> FitnessAgentState:
    """Classify user intent and route to the correct sub-agent."""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    prompt = INTENT_PROMPT.format(message=state["user_message"])
    response = model.generate_content(prompt)
    intent = response.text.strip().lower()
    # Fallback to general if unknown intent
    if intent not in {"workout", "nutrition", "gym_finder", "progress", "general"}:
        intent = "general"
    return {**state, "intent": intent}


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
