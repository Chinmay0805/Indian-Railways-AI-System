import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
import matplotlib.pyplot as plt


# --- CONFIGURATION ---
DATA_PATH = "data/processed/train_delay_history.csv"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_delay_predictor():
    print("1. Loading Data...")
    if not os.path.exists(DATA_PATH):
        print("❌ Error: 'train_delay_history.csv' not found. Run Phase 5 script first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # --- PREPROCESSING ---
    print("2. Preprocessing Features...")
    
    # 1. Convert 'Scheduled_Arrival' (15:30) to Minutes (930)
    # This makes time mathematical
    def time_to_minutes(t_str):
        try:
            if pd.isna(t_str): return 0
            h, m, *s = str(t_str).split(':')
            return int(h) * 60 + int(m)
        except:
            return 0
            
    df['Arrival_Min'] = df['Scheduled_Arrival'].apply(time_to_minutes)
    
    # 2. Encode Categorical Data (Zone, Station)
    # We save the encoders because we need them for the API later!
    le_zone = LabelEncoder()
    df['Zone_Encoded'] = le_zone.fit_transform(df['Zone'].astype(str))
    
    # We don't encode Station_Code for this simple model to avoid "High Cardinality" issues
    # (Too many unique stations makes the model slow for a student project).
    # We will stick to Zone, Distance, Time, and Seasonality.
    
    # Define Features (X) and Target (y)
    features = ['Distance', 'Is_Weekend', 'Month', 'Arrival_Min', 'Zone_Encoded']
    target = 'Delay_Minutes'
    
    X = df[features]
    y = df[target]
    
    # Split: 80% for Training, 20% for Testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # --- TRAINING ---
    print("3. Training Random Forest Model (this may take a moment)...")
    # n_estimators=100 means we use 100 decision trees
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # --- EVALUATION ---
    print("4. Evaluating Model...")
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"   ✅ Model Performance:")
    print(f"      Mean Absolute Error: {mae:.2f} minutes")
    print(f"      (On average, the prediction is off by {mae:.2f} min)")
    print(f"      R2 Score: {r2:.2f} (Variance explained)")
    
    # --- SAVING ---
    print("5. Saving Artifacts...")
    joblib.dump(model, f"{MODEL_DIR}/delay_model.pkl")
    joblib.dump(le_zone, f"{MODEL_DIR}/zone_encoder.pkl")
    print(f"   ✅ Model saved to {MODEL_DIR}/delay_model.pkl")

    feature_names = ['Distance', 'Is_Weekend', 'Month', 'Arrival_Min', 'Zone']
    importances = model.feature_importances_

    plt.barh(feature_names, importances)
    plt.title("What causes delays?")
    plt.show()


if __name__ == "__main__":
    train_delay_predictor()

