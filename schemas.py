from pydantic import BaseModel
from typing import Optional

class DeliveryCreate(BaseModel):
    delivery_person_id: int
    package_id: int
    post_office_id: int
    traffic_level: str
    weather_description: str
    temperature: float
    humidity: float
    precipitation: float
    distance: float
    delivery_time: float

class DeliveryOut(DeliveryCreate):
    id: int

class PredictionRequest(BaseModel):
    traffic_level: str
    delivery_person_id: int
    weather_description: str
    type_of_package: str
    type_of_vehicle: str
    delivery_person_age: int
    delivery_person_ratings: float
    po_latitude: float
    po_longitude: float
    delivery_location_latitude: float
    delivery_location_longitude: float
    temperature: float
    humidity: float
    precipitation: float
    distance: float