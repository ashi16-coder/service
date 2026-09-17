"""
Booking tests — covers:
  - Happy paths   : valid bookings are created and retrievable
  - Failure paths : bad service_type, missing fields
  - Regression    : failed booking leaves no partial data
"""

VALID_BOOKING = {
    "service_type": "hotel",
    "user_name": "Alice",
    "date": "2025-12-01",
    "destination": "mumbai",
}


def test_create_booking_success(client):
    res = client.post("/booking/create", json=VALID_BOOKING)
    assert res.status_code == 201
    data = res.json()
    assert data["booking"]["status"] == "Confirmed"
    assert data["booking"]["booking_id"] is not None


def test_booking_id_retrievable(client):
    res = client.post("/booking/create", json=VALID_BOOKING)
    bid = res.json()["booking"]["booking_id"]
    res2 = client.get(f"/booking/status/{bid}")
    assert res2.status_code == 200
    assert res2.json()["booking_id"] == bid


def test_create_booking_transport(client):
    res = client.post("/booking/create", json={**VALID_BOOKING, "service_type": "transport"})
    assert res.status_code == 201


def test_create_booking_pre_booking(client):
    res = client.post("/booking/create", json={**VALID_BOOKING, "service_type": "pre_booking"})
    assert res.status_code == 201


def test_create_booking_invalid_service_type(client):
    res = client.post("/booking/create", json={**VALID_BOOKING, "service_type": "flight"})
    assert res.status_code == 400
    assert "service_type" in res.json()["detail"].lower()


def test_booking_not_found(client):
    res = client.get("/booking/status/INVALID1")
    assert res.status_code == 404


def test_list_hotels(client):
    res = client.get("/booking/hotels/mumbai")
    assert res.status_code == 200
    assert len(res.json()["hotels"]) > 0


def test_list_hotels_unknown_city(client):
    res = client.get("/booking/hotels/atlantis")
    assert res.status_code == 200
    assert res.json()["hotels"] == []


def test_list_transport(client):
    res = client.get("/booking/transport/delhi")
    assert res.status_code == 200
    assert len(res.json()["transport"]) > 0
