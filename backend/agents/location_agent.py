import requests
from backend.config import GOOGLE_MAPS_API_KEY


def geocode_location(location: str) -> str:
    """Convert city name to lat,lng string."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    resp = requests.get(url, params={"address": location, "key": GOOGLE_MAPS_API_KEY}, timeout=10)
    data = resp.json()
    if data.get("results"):
        loc = data["results"][0]["geometry"]["location"]
        return f"{loc['lat']},{loc['lng']}"
    return location


def find_nearby_gyms(location: str, radius_meters: int = 5000) -> list:
    """Find gyms near a location using Google Places API."""
    # Geocode if not already lat,lng
    parts = location.replace(" ", "").split(",")
    if len(parts) != 2 or not all(p.replace(".", "").replace("-", "").isdigit() for p in parts):
        location = geocode_location(location)

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius_meters,
        "type": "gym",
        "key": GOOGLE_MAPS_API_KEY
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    gyms = []
    for place in data.get("results", [])[:6]:
        gyms.append({
            "name":     place.get("name"),
            "address":  place.get("vicinity"),
            "rating":   place.get("rating", "N/A"),
            "open_now": place.get("opening_hours", {}).get("open_now"),
            "place_id": place.get("place_id"),
            "maps_url": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
        })
    return gyms


def location_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    location = profile.get("location", "Hyderabad, India")

    try:
        gyms = find_nearby_gyms(location)
    except Exception as e:
        return {**state, "nearby_gyms": [], "response": f"Could not fetch gyms: {e}"}

    if not gyms:
        return {
            **state,
            "nearby_gyms": [],
            "response": f"No gyms found near **{location}**. Try a different location."
        }

    lines = [f"Here are the top gyms near **{location}**:\n"]
    for i, g in enumerate(gyms, 1):
        status = "🟢 Open Now" if g["open_now"] else ("🔴 Closed" if g["open_now"] is False else "⏱ Hours Unknown")
        lines.append(
            f"**{i}. {g['name']}**\n"
            f"   📍 {g['address']}\n"
            f"   ⭐ Rating: {g['rating']}  |  {status}\n"
            f"   🗺 [Open in Google Maps]({g['maps_url']})\n"
        )

    return {**state, "nearby_gyms": gyms, "response": "\n".join(lines)}
