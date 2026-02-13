import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os

# --- CONFIGURATION ---
INPUT_FILE = "data/processed/train_delay_history.csv"
OUTPUT_IMG = "docs/forecast_plot.png"
OUTPUT_CSV = "data/processed/forecast_results.csv"

# Ensure directories exist
os.makedirs("docs", exist_ok=True)

def run_forecasting():
    print("1. Loading & Aggregating Data...")
    if not os.path.exists(INPUT_FILE):
        print("❌ Error: History file not found.")
        return

    # Load individual train delays
    df = pd.read_csv(INPUT_FILE)
    
    # Convert 'Date' to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # AGGREGATION: We need ONE number per day (Total Delay Minutes)
    daily_data = df.groupby('Date')['Delay_Minutes'].sum()
    
    # Set the frequency to 'Daily' (D)
    daily_data.index.freq = 'D'
    
    print(f"   Analyzed {len(daily_data)} days of historical data.")

    # --- MODEL TRAINING ---
    print("2. Training Holt-Winters Model...")
    # 'add' means additive seasonality (Delay + Seasonal Effect)
    # seasonal_periods=7 means we expect a weekly pattern (Weekends vs Weekdays)
    model = ExponentialSmoothing(
        daily_data, 
        trend='add', 
        seasonal='add', 
        seasonal_periods=7
    ).fit()

    # --- FORECASTING ---
    print("3. Forecasting Next 30 Days...")
    forecast = model.forecast(30)
    
    # --- VISUALIZATION ---
    print("4. Generating Plot...")
    plt.figure(figsize=(12, 6))
    
    # Plot past data (Last 30 days only, to keep chart readable)
    daily_data[-30:].plot(label='Historical (Last 30 Days)', color='blue')
    
    # Plot forecast
    forecast.plot(label='Forecast (Next 30 Days)', color='red', linestyle='--')
    
    plt.title("Indian Railways: Daily Delay Forecast (Resource Planning)")
    plt.xlabel("Date")
    plt.ylabel("Total Delay Minutes (System-wide)")
    plt.legend()
    plt.grid(True)
    
    # Save Plot
    plt.savefig(OUTPUT_IMG)
    print(f"   ✅ Plot saved to {OUTPUT_IMG}")
    
    # Save Data
    forecast_df = pd.DataFrame({'Date': forecast.index, 'Predicted_Delay': forecast.values})
    forecast_df.to_csv(OUTPUT_CSV, index=False)
    print(f"   ✅ Forecast data saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    run_forecasting()