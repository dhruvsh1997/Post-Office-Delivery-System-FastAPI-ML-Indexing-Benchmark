import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import boto3
import os
# BUCKET = "post.delivery.app.storage"
# PREFIX = "PostDeliveryFolder"

# # Load dataset from S3
# s3 = boto3.client("s3")
# local_dataset = "dataset/Delivery_Time_new.csv"
# s3.download_file(BUCKET, f"{PREFIX}/Delivery_Time_new.csv", local_dataset)

s3 = boto3.client("s3")
BUCKET = "post.delivery.app.storage"
PREFIX = "PostDeliveryFolder"

# Local dataset directory
local_dataset_dir = "dataset/"
local_dataset_file = os.path.join(local_dataset_dir, "Delivery_Time_new.csv")

# Download dataset if not already present
if not os.path.exists(local_dataset_dir):
    os.makedirs(local_dataset_dir, exist_ok=True)
    s3.download_file(BUCKET, f"{PREFIX}/Delivery_Time_new.csv", local_dataset_file)
    print(f"Downloaded dataset to {local_dataset_file}")
else:
    print(f"Dataset already exists at {local_dataset_file}, skipping download.")

df = pd.read_csv(local_dataset_file)

# --- Clean TARGET column ---
def clean_target(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        if value == '#VALUE!':
            return np.nan
        try:
            return float(value)
        except ValueError:
            parts = value.split('.')
            if len(parts) > 1:
                return float(parts[0] + '.' + ''.join(parts[1:]))
            else:
                return float(value)
    return np.nan

df["TARGET"] = df["TARGET"].astype(str).apply(clean_target)
df.dropna(subset=["TARGET"], inplace=True)

# --- Clean geolocation columns ---
cols_to_clean = ['PO_latitude', 'PO_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
for col in cols_to_clean:
    df[col] = df[col].astype(str).str.replace('.', '', n=1, regex=False).astype(float)

# --- Encode categorical variables ---
categorical_cols = ["Traffic_Level", "weather_description", "type_of_package", "Type_of_vehicle"]
encoders = {}
for col in categorical_cols:
    enc = LabelEncoder()
    df[col] = enc.fit_transform(df[col].astype(str))
    encoders[col] = enc

X = df.drop(["TARGET", "ID", "Delivery_person_ID"], axis=1)
y = df["TARGET"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save locally
model_path = "ml/delivery_time_predictor.pkl"
encoders_path = "ml/encoders.pkl"
joblib.dump(model, model_path)
joblib.dump(encoders, encoders_path)

# Upload to S3
s3.upload_file(model_path, BUCKET, f"{PREFIX}/delivery_time_predictor.pkl")
s3.upload_file(encoders_path, BUCKET, f"{PREFIX}/encoders.pkl")
