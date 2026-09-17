"""
Safety, Food, Language tests — happy and failure paths.
"""

# ── Safety ────────────────────────────────────────────────────────────────────

def test_get_emergency_contacts(client):
    res = client.get("/safety/contacts")
    assert res.status_code == 200
    contacts = res.json()["emergency_contacts"]
    for key in ("police", "fire", "doctor", "women", "crowd"):
        assert key in contacts


def test_send_valid_alert(client):
    res = client.post("/safety/alert", json={"type": "police", "latitude": 12.9, "longitude": 77.5})
    assert res.status_code == 200
    assert res.json()["status"] == "Alert dispatched"


def test_send_invalid_alert_type(client):
    res = client.post("/safety/alert", json={"type": "unknown", "latitude": 12.9, "longitude": 77.5})
    assert res.status_code == 400
    assert "unknown" in res.json()["detail"].lower()


def test_crowd_alert_known_location(client):
    res = client.get("/safety/crowd/city_center")
    assert res.status_code == 200
    assert res.json()["density"] == "High"


def test_crowd_alert_unknown_location(client):
    res = client.get("/safety/crowd/nowhere")
    assert res.status_code == 200
    assert res.json()["alert"] is False


# ── Food ──────────────────────────────────────────────────────────────────────

def test_get_all_temple_food(client):
    res = client.get("/food/temple-food")
    assert res.status_code == 200
    assert len(res.json()["temple_food"]) > 0


def test_get_temple_food_by_city(client):
    res = client.get("/food/temple-food?city=Mumbai")
    assert res.status_code == 200
    for item in res.json()["temple_food"]:
        assert item["city"] == "Mumbai"


def test_famous_dishes_known_city(client):
    res = client.get("/food/famous-dishes/mumbai")
    assert res.status_code == 200
    assert len(res.json()["dishes"]) > 0


def test_famous_dishes_unknown_city(client):
    res = client.get("/food/famous-dishes/atlantis")
    assert res.status_code == 200
    assert res.json()["dishes"] == []


# ── Language ──────────────────────────────────────────────────────────────────

def test_list_languages(client):
    res = client.get("/language/languages")
    assert res.status_code == 200
    assert "hi" in res.json()["supported_languages"]


def test_get_phrases_valid(client):
    res = client.get("/language/phrases/hi")
    assert res.status_code == 200
    assert len(res.json()["phrases"]) > 0


def test_get_phrases_invalid_lang(client):
    res = client.get("/language/phrases/xx")
    assert res.status_code == 404


def test_translate_unsupported_language(client):
    res = client.post("/language/translate", json={"text": "Hello", "target_language": "zz"})
    assert res.status_code == 400
    assert "unsupported" in res.json()["detail"].lower()


def test_translate_mock_fallback(client):
    """With no API key set, translation returns mock data — not an error."""
    res = client.post("/language/translate", json={"text": "Hello", "target_language": "hi"})
    assert res.status_code == 200
    assert res.json()["original"] == "Hello"
