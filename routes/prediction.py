from fastapi import APIRouter
from schemas import PredictionRequest
import joblib
from models import PredictionLog
from db import SessionLocal
import json

router = APIRouter()

model = joblib.load("ml/delivery_time_predictor.pkl")
encoders = joblib.load("ml/encoders.pkl")

@router.post("/predict")
def predict_delivery_time(request: PredictionRequest):
    data = request.dict()
    features = data.copy()

    # Encode categorical
    for col in ["Traffic_Level", "weather_description", "type_of_package", "Type_of_vehicle"]:
        features[col] = encoders[col].transform([features[col]])[0]

    input_data = [[
        features["Traffic_Level"], features["Delivery_person_Age"], features["Delivery_person_Ratings"],
        features["PO_latitude"], features["PO_longitude"], features["Delivery_location_latitude"],
        features["Delivery_location_longitude"], features["temperature"], features["humidity"],
        features["precipitation"], features["Distance (km)"], features["weather_description"],
        features["type_of_package"], features["Type_of_vehicle"]
    ]]

    pred = model.predict(input_data)[0]

    # Save prediction log
    db = SessionLocal()
    log = PredictionLog(features_json=json.dumps(data), predicted_time=pred)
    db.add(log)
    db.commit()
    db.close()

    return {"predicted_delivery_time": round(pred, 2)}