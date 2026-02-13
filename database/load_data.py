import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Station, TrainSchedule, engine
import os

# Create a Session to talk to the DB
Session = sessionmaker(bind=engine)
session = Session()

PROCESSED_DIR = "data/processed"

def load_stations():
    print("1. Loading Stations into Database...")
    df = pd.read_csv(f"{PROCESSED_DIR}/clean_stations.csv")
    
    # Convert DataFrame to List of Objects
    stations_data = []
    for _, row in df.iterrows():
        stations_data.append(Station(
            code=row['Station_Code'],
            name=row['Station_Name'],
            state=row['State'],
            zone=row['Zone'],
            latitude=row['Latitude'],
            longitude=row['Longitude']
        ))
    
    # Bulk Insert (Much faster than one by one)
    try:
        session.bulk_save_objects(stations_data)
        session.commit()
        print(f"   ✅ Inserted {len(stations_data)} stations.")
    except Exception as e:
        session.rollback()
        print(f"   ❌ Error loading stations: {e}")

def load_schedules():
    print("2. Loading Schedules into Database...")
    csv_path = f"{PROCESSED_DIR}/clean_schedules.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: File not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # --- DEBUGGING STEP: PRINT COLUMNS ---
    print(f"   🔍 Found Columns: {list(df.columns)}")
    
    # Normalize columns (Strip spaces to be safe)
    df.columns = [c.strip() for c in df.columns]
    
    # Optimization: Loading 69k rows can be slow. We do it in chunks.
    batch_size = 5000
    total_rows = len(df)
    
    # Initialize session
    Session = sessionmaker(bind=engine)
    session = Session()

    for start in range(0, total_rows, batch_size):
        end = start + batch_size
        batch = df[start:end]
        
        schedules_data = []
        for _, row in batch.iterrows():
            # USE .get() to handle missing columns gracefully
            schedules_data.append(TrainSchedule(
                train_no=str(row.get('Train_No', 'Unknown')),
                station_code=row.get('Station_Code', 'Unknown'),
                station_name=row.get('Station_Name', ''),
                sequence=row.get('Sequence', 0),
                arrival_time=str(row.get('Arrival_Time', '00:00:00')),
                departure_time=str(row.get('Departure_Time', '00:00:00')),
                distance=row.get('Distance', 0.0),
                source_station=row.get('Source_Station', ''),
                destination_station=row.get('Destination_Station', '')
            ))
        
        try:
            session.bulk_save_objects(schedules_data)
            session.commit()
            print(f"   ... Inserted batch {start}-{end}")
        except Exception as e:
            session.rollback()
            print(f"   ❌ Error in batch {start}: {e}")
            break # Stop if a batch fails
            
    session.close()
    print("   ✅ All Schedules loaded.")

    
if __name__ == "__main__":
    # 1. Create Tables first
    from models import create_tables
    create_tables()
    
    # 2. Load Data
    load_stations()
    load_schedules()
    print("\n🎉 PHASE 3 COMPLETE: Database is live!")