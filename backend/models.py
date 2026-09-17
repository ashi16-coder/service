from pydantic import BaseModel
from typing import Optional


class LocationRequest(BaseModel):
    latitude: float
    longitude: float


class EmergencyRequest(BaseModel):
    type: str
    latitude: float
    longitude: float
    message: Optional[str] = None


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class BookingRequest(BaseModel):
    service_type: str
    user_name: str
    date: str
    destination: str
    details: Optional[str] = None
