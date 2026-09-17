from fastapi import APIRouter
from logger import get_logger

log = get_logger("food")
router = APIRouter(prefix="/food", tags=["Food"])

TEMPLE_FOOD = [
    {"temple": "ISKCON Temple",   "city": "Mumbai",   "food": "Prasad Thali",   "timings": "12:00–13:00", "free": True},
    {"temple": "Golden Temple",   "city": "Amritsar", "food": "Langar",         "timings": "All day",     "free": True},
    {"temple": "Tirupati Balaji", "city": "Tirupati", "food": "Laddu Prasadam", "timings": "06:00–21:00", "free": False},
    {"temple": "Shirdi Sai Baba", "city": "Shirdi",   "food": "Anna Prasad",    "timings": "12:00–14:00", "free": True},
]

FAMOUS_DISHES = {
    "mumbai":   [{"dish": "Vada Pav",        "type": "Street Food", "avg_price": "₹15–30"},
                 {"dish": "Pav Bhaji",        "type": "Street Food", "avg_price": "₹60–120"}],
    "delhi":    [{"dish": "Butter Chicken",  "type": "Main Course", "avg_price": "₹200–400"},
                 {"dish": "Chole Bhature",   "type": "Breakfast",   "avg_price": "₹80–150"}],
    "amritsar": [{"dish": "Amritsari Kulcha","type": "Breakfast",   "avg_price": "₹60–100"}],
    "chennai":  [{"dish": "Dosa",            "type": "Breakfast",   "avg_price": "₹40–80"},
                 {"dish": "Chettinad Curry", "type": "Main Course", "avg_price": "₹180–350"}],
    "kolkata":  [{"dish": "Kathi Roll",      "type": "Street Food", "avg_price": "₹50–100"}],
}


@router.get("/temple-food")
def get_temple_food(city: str = None):
    data = TEMPLE_FOOD if not city else [t for t in TEMPLE_FOOD if t["city"].lower() == city.lower()]
    return {"temple_food": data}


@router.get("/famous-dishes/{city}")
def get_famous_dishes(city: str):
    dishes = FAMOUS_DISHES.get(city.lower())
    if not dishes:
        return {"city": city, "dishes": [], "message": f"No data for '{city}'. Available: {list(FAMOUS_DISHES)}"}
    return {"city": city, "dishes": dishes}
