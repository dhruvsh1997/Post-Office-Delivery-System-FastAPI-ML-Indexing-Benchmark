from fastapi import APIRouter
from schemas import PredictionRequest
import joblib
from models import PredictionLog
from db import SessionLocal
import json
import numpy as np

router = APIRouter()

model = joblib.load("ml/delivery_time_predictor.pkl")
encoders = joblib.load("ml/encoders.pkl")

@router.post("/predict")
def predict_delivery_time(request: PredictionRequest):
    data = request.dict()
    features = data.copy()
    # breakpoint()
    # Encode categorical
    for col in ["Traffic_Level", "weather_description", "type_of_package", "Type_of_vehicle"]:
        features[col.lower()] = int(encoders[col].transform([features[col.lower()]])[0])

    input_data = [[
        features["traffic_level"], features["delivery_person_age"], features["delivery_person_ratings"],
        features["po_latitude"], features["po_longitude"], features["delivery_location_latitude"],
        features["delivery_location_longitude"], features["temperature"], features["humidity"],
        features["precipitation"], features["distance"], features["weather_description"],
        features["type_of_package"], features["type_of_vehicle"]
    ]]

    # Ensure prediction is a native Python float
    pred = float(model.predict(input_data)[0])
    breakpoint()
    # Save prediction log
    db = SessionLocal()
    log = PredictionLog(
        features_json=json.dumps(data),
        predicted_time=pred
    )
    db.add(log)
    db.commit()
    db.close()


    return {"predicted_delivery_time": round(pred, 2)}