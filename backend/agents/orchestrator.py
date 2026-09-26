import re

from langgraph.graph import END, StateGraph

from backend.agents import FitnessAgentState
from backend.agents.assistant_agent import assistant_agent_node
from backend.agents.location_agent import location_agent_node
from backend.agents.nutrition_agent import nutrition_agent_node
from backend.agents.progress_agent import progress_agent_node
from backend.agents.workout_agent import workout_agent_node

INTENT_RULES = (
    ("gym_finder", ("gym", "gyms", "fitness center", "fitness centre")),
    ("nutrition", ("diet", "meal", "meals", "food", "calorie", "calories", "nutrition", "protein")),
    ("workout", ("workout", "workouts", "exercise", "exercises", "training")),
    ("progress", ("progress", "bmi", "streak", "stats")),
)


def classify_intent(message: str) -> str:
    text = message.lower()
    for intent, words in INTENT_RULES:
        if any(re.search(rf"\b{re.escape(word)}\b", text) for word in words):
            return intent
    return "general"


def intent_classifier_node(state: FitnessAgentState) -> FitnessAgentState:
    return {**state, "intent": classify_intent(state["user_message"])}


def route_to_agent(state: FitnessAgentState) -> str:
    routing = {
        "workout": "workout_agent",
        "nutrition": "nutrition_agent",
        "gym_finder": "location_agent",
        "progress": "progress_agent",
        "general": "assistant_agent",
    }
    return routing.get(state["intent"], "assistant_agent")


def build_fitness_graph():
    graph = StateGraph(FitnessAgentState)
    graph.add_node("intent_classifier", intent_classifier_node)
    graph.add_node("workout_agent", workout_agent_node)
    graph.add_node("nutrition_agent", nutrition_agent_node)
    graph.add_node("location_agent", location_agent_node)
    graph.add_node("progress_agent", progress_agent_node)
    graph.add_node("assistant_agent", assistant_agent_node)
    graph.set_entry_point("intent_classifier")
    graph.add_conditional_edges(
        "intent_classifier",
        route_to_agent,
        {
            "workout_agent": "workout_agent",
            "nutrition_agent": "nutrition_agent",
            "location_agent": "location_agent",
            "progress_agent": "progress_agent",
            "assistant_agent": "assistant_agent",
        },
    )
    for agent in (
        "workout_agent",
        "nutrition_agent",
        "location_agent",
        "progress_agent",
        "assistant_agent",
    ):
        graph.add_edge(agent, END)
    return graph.compile()


fitness_graph = build_fitness_graph()
