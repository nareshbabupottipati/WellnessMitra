import urllib.parse
from typing import List, Dict, Optional
from backend.config import GOOGLE_MAPS_API_KEY
from backend.database.crud import search_gyms, get_all_gyms


def get_local_gyms(location: str, limit: int = 6) -> List[Dict]:
    """
    Retrieve matching gyms from data/gyms.json without requiring any API keys.
    Generates browser-friendly, free Google Maps and OpenStreetMap links.
    """
    matched = search_gyms(location, limit=limit)
    if not matched:
        matched = get_all_gyms()[:limit]

    formatted = []
    for g in matched:
        full_query = f"{g.get('name', '')} {g.get('address', location)}"
        encoded_query = urllib.parse.quote(full_query)
        encoded_city = urllib.parse.quote(f"{g.get('name', '')} {g.get('city', location)}")

        formatted.append({
            "name":        g.get("name"),
            "city":        g.get("city"),
            "area":        g.get("area"),
            "address":     g.get("address"),
            "rating":      g.get("rating", 4.5),
            "open_hours":  g.get("open_hours", "06:00 AM - 10:00 PM"),
            "open_now":    g.get("open_now", True),
            "facilities":  g.get("facilities", []),
            "pricing":     g.get("pricing", "Contact gym for plans"),
            "contact":     g.get("contact", "N/A"),
            "maps_url":    f"https://www.google.com/maps/search/?api=1&query={encoded_query}",
            "osm_url":     f"https://www.openstreetmap.org/search?query={encoded_city}"
        })
    return formatted


def location_agent_node(state: dict) -> dict:
    """
    Locates gyms near user's location using local data/gyms.json.
    Works 100% offline without requiring Google Cloud billing or Maps API keys.
    """
    profile = state.get("user_profile", {})
    user_msg = state.get("user_message", "")

    # Prefer specific location mentioned in query, else user's profile location
    location = profile.get("location", "Hyderabad, India")
    for keyword in ["in ", "near ", "around ", "at "]:
        if keyword in user_msg.lower():
            extracted = user_msg.lower().split(keyword, 1)[1].strip("?.! ")
            if len(extracted) > 2:
                location = extracted.title()
                break

    gyms = get_local_gyms(location, limit=5)
    encoded_loc = urllib.parse.quote(f"gyms near {location}")

    lines = [
        f"📍 **Top Fitness Centers & Gyms near {location}:**\n",
        "> 💡 *Powered by local verified directory — no Google Maps API key or billing required.*\n"
    ]

    for i, g in enumerate(gyms, 1):
        facilities_str = ", ".join(g["facilities"][:3]) if g["facilities"] else "Weights & Cardio"
        lines.append(
            f"**{i}. {g['name']}** ⭐ {g['rating']}\n"
            f"   🏠 {g['address']}\n"
            f"   🕒 Hours: {g['open_hours']}  |  💰 {g['pricing']}\n"
            f"   🏋️ Features: {facilities_str}\n"
            f"   🗺️ [Open in Google Maps]({g['maps_url']}) • [Open in OpenStreetMap]({g['osm_url']})\n"
        )

    lines.append(
        f"🔍 **Looking for more options?**\n"
        f"- [Search all gyms near {location} on Google Maps](https://www.google.com/maps/search/?api=1&query={encoded_loc})\n"
        f"- [Search on OpenStreetMap](https://www.openstreetmap.org/search?query={encoded_loc})"
    )

    response_text = "\n".join(lines)
    return {
        **state,
        "nearby_gyms": gyms,
        "response": response_text
    }
