from .service import ExternalStatusService


class StatusController:
    def __init__(self, service=None):
        self.service = service or ExternalStatusService()

    def get_status(self, item_id):
        try:
            return self.service.get_status(item_id)
        except TimeoutError:
            return {
                "status": "unavailable",
                "detail": "External service timed out.",
            }
        except Exception:
            return {
                "status": "unavailable",
                "detail": "External service is unavailable.",
            }
