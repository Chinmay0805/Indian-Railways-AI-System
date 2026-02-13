import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine


# Connect to your Warehouse
db_path = "sqlite:///railways.db"
engine = create_engine(db_path)

def generate_history():
    print("1. Reading Schedules from DB...")
    # Get all schedules (Limit to top 50 trains to keep it fast for now)
    query = """
    SELECT train_no, station_code, arrival_time, distance, zone 
    FROM train_schedules 
    JOIN stations ON train_schedules.station_code = stations.code
    WHERE train_no IN (SELECT DISTINCT train_no FROM train_schedules LIMIT 50)
    """
    df_schedule = pd.read_sql(query, engine)
    
    print(f"   Loaded {len(df_schedule)} schedule rows. Generating history...")
    
    history_data = []
    
    # Simulate the last 90 days
    start_date = datetime.now() - timedelta(days=90)
    
    for day_offset in range(90):
        current_date = start_date + timedelta(days=day_offset)
        
        # FEATURE 1: Temporal (Day of Week, Month)
        day_of_week = current_date.weekday() # 0=Mon, 6=Sun
        is_weekend = 1 if day_of_week >= 5 else 0
        month = current_date.month
        
        # FEATURE 2: Seasonality (Simple Logic)
        season_factor = 0
        if month in [12, 1]: season_factor = 60 # Winter Fog (High Delay)
        elif month in [7, 8]: season_factor = 40 # Monsoon (Medium Delay)
        
        # Loop through schedules and create a "Trip" for this date
        # (We sample 20% of rows to keep the file size manageable)
        daily_sample = df_schedule.sample(frac=0.2)
        
        for _, row in daily_sample.iterrows():
            # Base delay (Random noise)
            delay = int(np.random.exponential(scale=10)) # Most trains are on time
            
            # Add Logic: High traffic zones get more delay
            if row['zone'] in ['NR', 'NCR', 'ECR']:
                delay += random.randint(5, 20)
            
            # Add Logic: Weekends have different traffic patterns
            if is_weekend:
                delay -= 5 # Less office traffic?
                
            # Add Logic: Seasonality
            delay += int(np.random.normal(season_factor, 5))
            
            # Ensure no negative delays (early arrival is rare/capped)
            delay = max(0, delay)
            
            history_data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Train_No': row['train_no'],
                'Station_Code': row['station_code'],
                'Zone': row['zone'],
                'Scheduled_Arrival': row['arrival_time'],
                'Distance': row['distance'],
                # --- THE FEATURES ---
                'Is_Weekend': is_weekend,
                'Day_Of_Week': day_of_week,
                'Month': month,
                # --- THE TARGET (LABEL) ---
                'Delay_Minutes': delay
            })
            
    # Save to CSV
    df_history = pd.DataFrame(history_data)
    output_path = "data/processed/train_delay_history.csv"
    df_history.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df_history)} rows of training data at {output_path}")

    
    # (Optional) Check what matters most


  


if __name__ == "__main__":
    generate_history()