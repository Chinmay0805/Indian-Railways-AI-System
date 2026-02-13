import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import numpy as np

# --- CONFIGURATION ---
DATA_PATH = "data/processed/train_delay_history.csv"
MODEL_PATH = "models/delay_model.pkl"
ENCODER_PATH = "models/zone_encoder.pkl"
IMG_PATH = "docs/model_evaluation.png"

def evaluate():
    print("1. Loading Artifacts...")
    if not os.path.exists(DATA_PATH) or not os.path.exists(MODEL_PATH):
        print("❌ Error: Missing data or model. Run previous phases first.")
        return

    # Load Data
    df = pd.read_csv(DATA_PATH)
    
    # Load Model & Encoder
    model = joblib.load(MODEL_PATH)
    le_zone = joblib.load(ENCODER_PATH)

    # --- PREPROCESSING (Same as Training) ---
    # We must treat the test data EXACTLY like training data
    def time_to_minutes(t_str):
        try:
            if pd.isna(t_str): return 0
            h, m, *s = str(t_str).split(':')
            return int(h) * 60 + int(m)
        except:
            return 0
            
    df['Arrival_Min'] = df['Scheduled_Arrival'].apply(time_to_minutes)
    
    # Handle unknown zones in test data safely
    # (If a new zone appears that wasn't in training, we map it to 'Unknown' or 0)
    df['Zone_Encoded'] = df['Zone'].apply(lambda x: 
                                          le_zone.transform([x])[0] if x in le_zone.classes_ 
                                          else -1)
    
    # Filter out rows where Zone was unknown (-1)
    df = df[df['Zone_Encoded'] != -1]

    features = ['Distance', 'Is_Weekend', 'Month', 'Arrival_Min', 'Zone_Encoded']
    target = 'Delay_Minutes'
    
    X = df[features]
    y = df[target]

    # Split (Use a different random_state to ensure it's a fair test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)

    # --- PREDICTION ---
    print("2. Generating Predictions...")
    y_pred = model.predict(X_test)

    # --- METRICS ---
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("\n📊 FINAL REPORT CARD")
    print("-" * 30)
    print(f"   Mean Absolute Error (MAE): {mae:.2f} min")
    print(f"   Root Mean Sq Error (RMSE): {rmse:.2f} min")
    print(f"   R2 Score (Accuracy):       {r2:.2f}")
    print("-" * 30)

    # --- VISUALIZATION ---
    print("3. Generating Residual Plot...")
    plt.figure(figsize=(14, 6))

    # Subplot 1: Actual vs Predicted
    plt.subplot(1, 2, 1)
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5, color='blue')
    # Draw a perfect diagonal line (Ideal predictions)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel("Actual Delay (Minutes)")
    plt.ylabel("Predicted Delay (Minutes)")
    plt.title(f"Actual vs Predicted (R2: {r2:.2f})")

    # Subplot 2: Residuals (Errors)
    # Ideally, this should look like a random cloud around 0
    residuals = y_test - y_pred
    plt.subplot(1, 2, 2)
    sns.histplot(residuals, kde=True, color='purple')
    plt.xlabel("Prediction Error (Minutes)")
    plt.title("Distribution of Errors (Residuals)")
    plt.axvline(0, color='red', linestyle='--')

    plt.tight_layout()
    plt.savefig(IMG_PATH)
    print(f"   ✅ Evaluation chart saved to {IMG_PATH}")

if __name__ == "__main__":
    evaluate()