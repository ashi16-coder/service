from fastapi import APIRouter, HTTPException
from models import EmergencyRequest
from logger import get_logger

log = get_logger("safety")
router = APIRouter(prefix="/safety", tags=["Safety & Danger"])

EMERGENCY_CONTACTS = {
    "police": {"name": "Police",         "number": "100",  "icon": "👮"},
    "fire":   {"name": "Fire Brigade",   "number": "101",  "icon": "🚒"},
    "doctor": {"name": "Ambulance",      "number": "108",  "icon": "🩺"},
    "women":  {"name": "Women Helpline", "number": "1091", "icon": "👩"},
    "crowd":  {"name": "Crowd Control",  "number": "100",  "icon": "👥"},
}

CROWD_DATA = {
    "city_center":  {"density": "High",   "alert": True,  "advice": "Avoid peak hours 5–8 PM."},
    "old_fort":     {"density": "Medium", "alert": False, "advice": "Manageable crowd levels."},
    "central_park": {"density": "Low",    "alert": False, "advice": "Enjoy your visit!"},
}


@router.get("/contacts")
def get_all_contacts():
    return {"emergency_contacts": EMERGENCY_CONTACTS}


@router.post("/alert")
def send_alert(req: EmergencyRequest):
    if req.type not in EMERGENCY_CONTACTS:
        raise HTTPException(status_code=400,
            detail=f"Unknown emergency type '{req.type}'. Valid: {list(EMERGENCY_CONTACTS)}")
    contact = EMERGENCY_CONTACTS[req.type]
    log.warning("EMERGENCY ALERT type=%s lat=%s lng=%s msg=%s",
                req.type, req.latitude, req.longitude, req.message)
    return {"status": "Alert dispatched", "contact": contact,
            "your_location": {"lat": req.latitude, "lng": req.longitude},
            "instruction": f"Help is on the way. Call {contact['number']} if urgent."}


@router.get("/crowd/{location}")
def get_crowd(location: str):
    data = CROWD_DATA.get(location.lower().replace(" ", "_"))
    if not data:
        return {"location": location, "density": "Unknown", "alert": False,
                "advice": "No crowd data available for this location."}
    return {"location": location, **data}
