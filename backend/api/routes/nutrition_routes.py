from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from backend.database.crud import search_foods, get_all_foods, get_food

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.get("/foods")
def list_or_search_foods(q: Optional[str] = Query(None, description="Search term for foods")):
    """
    Search or list food nutrition information from data/foods.json.
    Replaces external Edamam API with fast, local JSON data.
    """
    if q:
        results = search_foods(q, limit=25)
    else:
        results = get_all_foods()
    return {
        "total": len(results),
        "source": "local_json",
        "foods": results
    }


@router.get("/foods/{name}")
def get_food_detail(name: str):
    """Get nutritional breakdown for a specific food item."""
    food = get_food(name)
    if not food:
        raise HTTPException(status_code=404, detail=f"Food '{name}' not found in local database")
    return food
