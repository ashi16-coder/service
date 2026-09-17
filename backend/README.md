# Tourism Support API

One-stop backend for travel info, weather, safety, language, food, and booking.

---

## Quick Start (Fresh Setup)

```bash
# 1. Clone / enter the project
cd d:/sih/backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install exact pinned dependencies
pip install -r requirements.txt

# 4. Copy env file and fill in your values
cp .env.example .env

# 5. Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE tourism_db;"

# 6. Start the server (tables are auto-created on startup)
uvicorn main:app --reload --port 8000
```

Interactive docs → http://localhost:8000/docs

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | ✅ Yes | `postgresql://postgres:password@localhost:5432/tourism_db` | PostgreSQL connection string |
| `SECRET_KEY` | ✅ Yes | `change_this_secret_in_production` | JWT signing secret — **change in production** |
| `OPENWEATHER_API_KEY` | ⬜ Optional | _(mock data used)_ | OpenWeatherMap API key |
| `GOOGLE_TRANSLATE_API_KEY` | ⬜ Optional | _(mock data used)_ | Google Cloud Translation API key |

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Running Tests

```bash
# Tests use an isolated SQLite DB — no PostgreSQL needed
pytest tests/ -v
```

---

## Example Requests

### Auth

**Register**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "tourist@example.com", "password": "secret123", "mobile": "9876543210"}'
```
```json
{
  "message": "Registration successful.",
  "user": { "id": 1, "email": "tourist@example.com", "mobile": "9876543210" }
}
```

**Login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "tourist@example.com", "password": "secret123"}'
```
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer",
  "user": { "id": 1, "email": "tourist@example.com", "mobile": "9876543210" }
}
```

---

### Live Data

**Get nearby places**
```bash
curl -X POST http://localhost:8000/live/location \
  -H "Content-Type: application/json" \
  -d '{"latitude": 12.9716, "longitude": 77.5946}'
```
```json
{
  "current_location": { "lat": 12.9716, "lng": 77.5946 },
  "nearby_places": [
    { "name": "City Museum", "type": "attraction", "distance_km": 1.2, "rating": 4.5 }
  ],
  "route_tip": "Head north on Main Street to reach the heritage zone."
}
```

---

### Weather

**Get weather for a city**
```bash
curl http://localhost:8000/weather/Mumbai
```
```json
{
  "city": "Mumbai",
  "temperature_c": 28,
  "feels_like_c": 30,
  "condition": "Partly Cloudy",
  "humidity_pct": 65,
  "wind_kph": 12,
  "advice": "Good weather for sightseeing!"
}
```

---

### Safety

**Get all emergency contacts**
```bash
curl http://localhost:8000/safety/contacts
```
```json
{
  "emergency_contacts": {
    "police": { "name": "Police", "number": "100", "icon": "👮" },
    "fire":   { "name": "Fire Brigade", "number": "101", "icon": "🚒" },
    "doctor": { "name": "Ambulance", "number": "108", "icon": "🩺" }
  }
}
```

**Send emergency alert**
```bash
curl -X POST http://localhost:8000/safety/alert \
  -H "Content-Type: application/json" \
  -d '{"type": "doctor", "latitude": 12.97, "longitude": 77.59, "message": "Need medical help"}'
```
```json
{
  "status": "Alert dispatched",
  "contact": { "name": "Ambulance", "number": "108", "icon": "🩺" },
  "instruction": "Help is on the way. Call 108 if urgent."
}
```

**Crowd alert**
```bash
curl http://localhost:8000/safety/crowd/city_center
```
```json
{ "location": "city_center", "density": "High", "alert": true, "advice": "Avoid peak hours 5–8 PM." }
```

---

### Language

**List supported languages**
```bash
curl http://localhost:8000/language/languages
```

**Get common phrases**
```bash
curl http://localhost:8000/language/phrases/hi
```
```json
{
  "language": "Hindi",
  "phrases": [
    { "english": "Where is the hospital?", "local": "अस्पताल कहाँ है?", "phonetic": "Aspataal kahaan hai?" }
  ]
}
```

**Translate text**
```bash
curl -X POST http://localhost:8000/language/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Where is the nearest hospital?", "target_language": "hi"}'
```
```json
{ "original": "Where is the nearest hospital?", "translated": "निकटतम अस्पताल कहाँ है?", "target_language": "Hindi" }
```

---

### Food

**Temple food (all cities)**
```bash
curl http://localhost:8000/food/temple-food
```

**Temple food (by city)**
```bash
curl "http://localhost:8000/food/temple-food?city=Mumbai"
```

**Famous dishes**
```bash
curl http://localhost:8000/food/famous-dishes/delhi
```
```json
{
  "city": "delhi",
  "dishes": [
    { "dish": "Butter Chicken", "type": "Main Course", "avg_price": "₹200–400" },
    { "dish": "Chole Bhature",  "type": "Breakfast",   "avg_price": "₹80–150" }
  ]
}
```

---

### Booking

**List hotels**
```bash
curl http://localhost:8000/booking/hotels/mumbai
```

**List transport**
```bash
curl http://localhost:8000/booking/transport/delhi
```

**Create booking**
```bash
curl -X POST http://localhost:8000/booking/create \
  -H "Content-Type: application/json" \
  -d '{"service_type": "hotel", "user_name": "Alice", "date": "2025-12-01", "destination": "mumbai"}'
```
```json
{
  "message": "Booking confirmed!",
  "booking": { "booking_id": "A1B2C3D4", "status": "Confirmed", "service_type": "hotel" }
}
```

**Check booking status**
```bash
curl http://localhost:8000/booking/status/A1B2C3D4
```
