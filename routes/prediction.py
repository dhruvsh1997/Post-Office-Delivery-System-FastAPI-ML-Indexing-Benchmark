from fastapi import APIRouter
from schemas import PredictionRequest
import joblib
from models import PredictionLog
from db import SessionLocal
import json
import boto3
import os

router = APIRouter()

BUCKET = "post.delivery.app.storage"
PREFIX = "PostDeliveryFolder"
s3 = boto3.client("s3")

model_path = "ml/delivery_time_predictor.pkl"
encoders_path = "ml/encoders.pkl"

# Download artifacts if not present locally
os.makedirs("ml", exist_ok=True)
# Download model if not present
if not os.path.exists(model_path):
    s3.download_file(BUCKET, f"{PREFIX}/delivery_time_predictor.pkl", model_path)
    print(f"Downloaded model to {model_path}")
else:
    print(f"Model already exists at {model_path}, skipping download.")

# Download encoders if not present
if not os.path.exists(encoders_path):
    s3.download_file(BUCKET, f"{PREFIX}/encoders.pkl", encoders_path)
    print(f"Downloaded encoders to {encoders_path}")
else:
    print(f"Encoders already exist at {encoders_path}, skipping download.")

model = joblib.load(model_path)
encoders = joblib.load(encoders_path)

@router.post("/predict")
def predict_delivery_time(request: PredictionRequest):
    data = request.dict()
    features = data.copy()

    for col in ["Traffic_Level", "weather_description", "type_of_package", "Type_of_vehicle"]:
        features[col.lower()] = int(encoders[col].transform([features[col.lower()]])[0])

    input_data = [[
        features["traffic_level"], features["delivery_person_age"], features["delivery_person_ratings"],
        features["po_latitude"], features["po_longitude"], features["delivery_location_latitude"],
        features["delivery_location_longitude"], features["temperature"], features["humidity"],
        features["precipitation"], features["distance"], features["weather_description"],
        features["type_of_package"], features["type_of_vehicle"]
    ]]

    pred = float(model.predict(input_data)[0])

    db = SessionLocal()
    log = PredictionLog(features_json=json.dumps(data), predicted_time=pred)
    db.add(log)
    db.commit()
    db.close()

    return {"predicted_delivery_time": round(pred, 2)}
