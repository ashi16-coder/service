from fastapi import APIRouter
from models import LocationRequest
from logger import get_logger

log = get_logger("live_data")
router = APIRouter(prefix="/live", tags=["Live Data"])

NEARBY_PLACES = [
    {"name": "City Museum",  "type": "attraction", "distance_km": 1.2, "rating": 4.5},
    {"name": "Central Park", "type": "park",       "distance_km": 0.8, "rating": 4.2},
    {"name": "Old Fort",     "type": "heritage",   "distance_km": 2.5, "rating": 4.8},
    {"name": "Local Market", "type": "shopping",   "distance_km": 0.5, "rating": 4.0},
]


@router.post("/location")
def get_live_data(req: LocationRequest):
    log.info("Live data requested for lat=%s lng=%s", req.latitude, req.longitude)
    return {
        "current_location": {"lat": req.latitude, "lng": req.longitude},
        "nearby_places": NEARBY_PLACES,
        "route_tip": "Head north on Main Street to reach the heritage zone.",
    }
