"""Nearby gyms via the Photon geocoder (OpenStreetMap). No API key."""
import math
import re
import requests

HEADERS = {"User-Agent": "WellnessMitraPOC/1.0 (local fitness demo)"}
PHOTON = "https://photon.komoot.io/api/"
ALLOWED_TYPES = {"fitness_centre", "fitness_center", "gym", "fitness_station", "sports_centre"}
GENERIC_NAMES = {"gym", "gyms", "fitness", "fitness centre", "fitness center", "unnamed gym"}
_cache = {}


def _km(lat1, lon1, lat2, lon2) -> float:
    radius = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlon / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))


def geocode_location(location: str):
    response = requests.get(
        PHOTON,
        params={"q": location, "limit": 1},
        headers=HEADERS,
        timeout=12,
    )
    response.raise_for_status()
    features = response.json().get("features") or []
    if not features:
        return None
    lon, lat = features[0]["geometry"]["coordinates"]
    return float(lat), float(lon)


def _search(query: str, lat: float, lon: float) -> list:
    response = requests.get(
        PHOTON,
        params={"q": query, "lat": lat, "lon": lon, "limit": 40, "lang": "en"},
        headers=HEADERS,
        timeout=12,
    )
    response.raise_for_status()
    gyms = []
    for feature in response.json().get("features") or []:
        props = feature.get("properties") or {}
        name = (props.get("name") or "").strip()
        kind = (props.get("osm_value") or "").lower()
        if not name or kind not in ALLOWED_TYPES:
            continue
        point = feature.get("geometry", {}).get("coordinates") or []
        if len(point) < 2:
            continue
        gym_lon, gym_lat = float(point[0]), float(point[1])
        distance = _km(lat, lon, gym_lat, gym_lon)
        if distance > 18:
            continue
        street = props.get("street")
        city = props.get("city") or props.get("district") or props.get("locality")
        address = ", ".join(part for part in (street, city) if part) or "Nearby"
        gyms.append({
            "name": name,
            "address": address,
            "distance_km": round(distance, 1),
            "maps_url": f"https://www.openstreetmap.org/?mlat={gym_lat}&mlon={gym_lon}#map=16/{gym_lat}/{gym_lon}",
        })
    return gyms


def find_nearby_gyms(location: str, radius_meters: int = 18000) -> list:
    key = location.strip().lower()
    if key in _cache:
        return _cache[key]
    coords = geocode_location(location)
    if not coords:
        return []
    lat, lon = coords
    merged = _search("fitness", lat, lon) + _search("gym", lat, lon)
    unique = []
    seen = set()
    for gym in sorted(merged, key=lambda item: item["distance_km"]):
        name_key = re.sub(r"[^a-z0-9]", "", gym["name"].lower())
        if name_key in seen:
            continue
        seen.add(name_key)
        unique.append(gym)
    named = [gym for gym in unique if gym["name"].strip().lower() not in GENERIC_NAMES]
    chosen = (named or unique)[:12]
    _cache[key] = chosen
    return chosen


def location_agent_node(state: dict) -> dict:
    profile = state["user_profile"]
    location = profile.get("location", "Hyderabad, India")
    try:
        gyms = find_nearby_gyms(location)
    except Exception as exc:
        return {**state, "nearby_gyms": [], "response": f"Could not fetch gyms: {exc}"}

    if not gyms:
        return {
            **state,
            "nearby_gyms": [],
            "response": f"No named gyms found near **{location}**. Try a more specific area.",
        }

    lines = [f"Here are **{len(gyms)}** gyms near **{location}**:\n"]
    for index, gym in enumerate(gyms, 1):
        lines.append(
            f"**{index}. {gym['name']}** · {gym['distance_km']} km\n"
            f"   📍 {gym['address']}\n"
            f"   🗺 [Open in OpenStreetMap]({gym['maps_url']})\n"
        )
    return {**state, "nearby_gyms": gyms, "response": "\n".join(lines)}
