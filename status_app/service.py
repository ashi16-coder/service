class StatusService:
    def get_status(self, item_id):
        raise NotImplementedError("Subclasses must implement get_status().")


class ExternalStatusService(StatusService):
    def get_status(self, item_id):
        # Placeholder integration point for real external status lookup.
        # This is intentionally left as a simple adapter boundary.
        return {"item_id": item_id, "status": "ok"}
