from status_app.routes import StatusController


class FakeService:
    def get_status(self, item_id):
        return {"item_id": item_id, "status": "ok"}


def test_route_returns_result_from_service():
    controller = StatusController(service=FakeService())

    response = controller.get_status("abc-123")

    assert response == {"item_id": "abc-123", "status": "ok"}


def test_route_handles_timeout_from_service():
    class TimeoutService:
        def get_status(self, item_id):
            raise TimeoutError("request timed out")

    controller = StatusController(service=TimeoutService())

    response = controller.get_status("abc-123")

    assert response == {
        "status": "unavailable",
        "detail": "External service timed out.",
    }


def test_route_handles_failure_from_service():
    class FailingService:
        def get_status(self, item_id):
            raise RuntimeError("upstream failed")

    controller = StatusController(service=FailingService())

    response = controller.get_status("abc-123")

    assert response == {
        "status": "unavailable",
        "detail": "External service is unavailable.",
    }
