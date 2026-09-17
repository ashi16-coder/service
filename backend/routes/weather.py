from fastapi import APIRouter, HTTPException
import httpx, os
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()
log = get_logger("weather")
router = APIRouter(prefix="/weather", tags=["Weather"])

OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OWM_BASE = "https://api.openweathermap.org/data/2.5"


def _advice(condition: str, temp: float) -> str:
    c = condition.lower()
    if "rain" in c:    return "Carry an umbrella. Indoor attractions recommended."
    if "storm" in c:   return "Avoid outdoor activities. Stay indoors."
    if temp > 38:      return "Very hot — stay hydrated and avoid midday sun."
    return "Good weather for sightseeing!"


@router.get("/{city}")
async def get_weather(city: str):
    if not OWM_API_KEY:
        log.warning("OPENWEATHER_API_KEY not set — returning mock data for city=%s", city)
        return {"city": city, "temperature_c": 28, "feels_like_c": 30,
                "condition": "Partly Cloudy", "humidity_pct": 65, "wind_kph": 12,
                "advice": "Good weather! (mock — set OPENWEATHER_API_KEY)"}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OWM_BASE}/weather",
                                    params={"q": city, "appid": OWM_API_KEY, "units": "metric"})
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
        resp.raise_for_status()
        d = resp.json()
        condition = d["weather"][0]["description"].title()
        temp = d["main"]["temp"]
        log.info("Weather fetched for city=%s temp=%s", city, temp)
        return {"city": city, "temperature_c": temp, "feels_like_c": d["main"]["feels_like"],
                "condition": condition, "humidity_pct": d["main"]["humidity"],
                "wind_kph": round(d["wind"]["speed"] * 3.6, 1), "advice": _advice(condition, temp)}
    except HTTPException:
        raise
    except Exception as exc:
        log.error("Unexpected error fetching weather for city=%s: %s", city, exc, exc_info=True)
        raise HTTPException(status_code=502, detail="Weather service unavailable. Try again later.")
