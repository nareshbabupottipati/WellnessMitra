from typing import TypedDict, Optional, List


class FitnessAgentState(TypedDict):
    user_id:          str
    user_profile:     dict
    user_message:     str
    intent:           str
    workout_plan:     Optional[dict]
    meal_plan:        Optional[dict]
    nearby_gyms:      Optional[list]
    progress_summary: Optional[dict]
    rag_context:      Optional[str]
    chat_history:     List[dict]
    response:         str
