from fastapi import APIRouter, HTTPException
from models import BookingRequest
from uuid import uuid4
from logger import get_logger

log = get_logger("booking")
router = APIRouter(prefix="/booking", tags=["Booking"])

bookings: dict = {}  # replace with DB in production

HOTELS = {
    "mumbai":   [{"name": "Sea View Inn",   "stars": 3, "price_per_night": "₹2500", "available": True},
                 {"name": "Grand Palace",   "stars": 5, "price_per_night": "₹8000", "available": True}],
    "delhi":    [{"name": "Capital Stays",  "stars": 3, "price_per_night": "₹2200", "available": True}],
    "amritsar": [{"name": "Golden Stay",    "stars": 3, "price_per_night": "₹1800", "available": True}],
}

TRANSPORT = {
    "mumbai":   [{"mode": "Local Train", "route": "CST → Dadar → Andheri", "fare": "₹10–50"},
                 {"mode": "Bus",         "route": "BEST Bus Network",       "fare": "₹5–30"}],
    "delhi":    [{"mode": "Metro",       "route": "Blue/Yellow/Red Lines",  "fare": "₹10–60"}],
    "amritsar": [{"mode": "E-Rickshaw",  "route": "Golden Temple Circuit",  "fare": "₹20–50"}],
}


@router.get("/hotels/{city}")
def list_hotels(city: str):
    hotels = HOTELS.get(city.lower())
    if not hotels:
        return {"city": city, "hotels": [], "message": f"No hotel data for '{city}'. Available: {list(HOTELS)}"}
    return {"city": city, "hotels": hotels}


@router.get("/transport/{city}")
def list_transport(city: str):
    options = TRANSPORT.get(city.lower())
    if not options:
        return {"city": city, "transport": [], "message": f"No transport data for '{city}'. Available: {list(TRANSPORT)}"}
    return {"city": city, "transport": options}


@router.post("/create", status_code=201)
def create_booking(req: BookingRequest):
    if req.service_type not in ("hotel", "transport", "pre_booking"):
        raise HTTPException(status_code=400,
            detail="service_type must be 'hotel', 'transport', or 'pre_booking'.")
    try:
        booking_id = str(uuid4())[:8].upper()
        record = {
            "booking_id": booking_id, "service_type": req.service_type,
            "user_name": req.user_name, "destination": req.destination,
            "date": req.date, "details": req.details, "status": "Confirmed",
        }
        # atomic: only store after full record is built — no partial writes
        bookings[booking_id] = record
        log.info("Booking created id=%s type=%s dest=%s", booking_id, req.service_type, req.destination)
        return {"message": "Booking confirmed!", "booking": record}
    except Exception as exc:
        log.error("Unexpected error creating booking: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Booking failed. Please try again later.")


@router.get("/status/{booking_id}")
def get_booking(booking_id: str):
    record = bookings.get(booking_id.upper())
    if not record:
        raise HTTPException(status_code=404, detail=f"Booking '{booking_id}' not found.")
    return record
