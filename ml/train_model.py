import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset (replace with actual path)
df = pd.read_csv('dataset\Delivery_Time_new.csv')

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
            # Handle values with multiple decimal points like '3.816.666.667'
            parts = value.split('.')
            if len(parts) > 1:
                return float(parts[0] + '.' + ''.join(parts[1:]))
            else:
                return float(value)
    return np.nan

df["TARGET"] = df["TARGET"].astype(str).apply(clean_target)

# Drop rows where TARGET could not be converted
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

# --- Split data ---
X = df.drop(["TARGET", "ID", "Delivery_person_ID"], axis=1)
y = df["TARGET"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train model ---
model = RandomForestRegressor()
model.fit(X_train, y_train)

# --- Save model and encoders ---
joblib.dump(model, "ml/delivery_time_predictor.pkl")
joblib.dump(encoders, "ml/encoders.pkl")