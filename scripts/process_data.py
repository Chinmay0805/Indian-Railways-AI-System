import pandas as pd
import json
import os
import requests

# --- CONFIGURATION ---
BASE_DIR = "data"
RAW_STATIC_DIR = os.path.join(BASE_DIR, "raw","static")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Ensure folders exist
os.makedirs(RAW_STATIC_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# File Paths
STATION_FILE = os.path.join(RAW_STATIC_DIR, "stations.json")
# We will search for schedules, not just hardcode one path

def download_station_data():
    """Downloads station data if missing."""
    print("1. Checking Station Data...")
    url = "https://raw.githubusercontent.com/datameet/railways/master/stations.json"
    
    if not os.path.exists(STATION_FILE):
        print("   ⬇️ Downloading fresh station data...")
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(STATION_FILE, 'wb') as f:
                    f.write(r.content)
                print("   ✅ Download Complete.")
            else:
                print(f"   ❌ Download Failed (Status: {r.status_code})")
        except Exception as e:
            print(f"   ❌ Network Error: {e}")

def process_stations():
    print("\n2. Processing Stations...")
    try:
        with open(STATION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        station_list = []
        features = data.get('features', [])
        
        for feature in features:
            if not feature: continue # Skip empty features
            
            # --- THE FIX FOR NONETYPE ERROR ---
            geom = feature.get('geometry')
            if not geom: continue # Skip stations with no location
            
            props = feature.get('properties', {})
            coords = geom.get('coordinates', [0, 0])
            
            station_list.append({
                "Station_Code": props.get("code", "Unknown"),
                "Station_Name": props.get("name", "Unknown"),
                "State": props.get("state", "Unknown"),
                "Zone": props.get("zone", "Unknown"),
                "Latitude": coords[1] if len(coords) > 1 else 0,
                "Longitude": coords[0] if len(coords) > 1 else 0
            })
            
        df = pd.DataFrame(station_list)
        # Drop rows where Station Code is missing or empty
        df = df[df['Station_Code'] != "Unknown"]
        df.drop_duplicates(subset=['Station_Code'], inplace=True)
        
        output_path = os.path.join(PROCESSED_DIR, "clean_stations.csv")
        df.to_csv(output_path, index=False)
        print(f"   ✅ Success! Saved {len(df)} stations to {output_path}")
        
    except Exception as e:
        print(f"   ❌ Station Processing Error: {e}")

def find_schedule_file():
    """Hunts for the schedule CSV in common locations."""
    possible_paths = [
        os.path.join(RAW_STATIC_DIR, "schedules.csv"),
        os.path.join(BASE_DIR, "raw", "schedules.csv"),
        "schedules.csv" # Root folder
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def process_schedules():
    print("\n3. Processing Schedules...")
    
    csv_path = find_schedule_file()
    
    if not csv_path:
        print("   ❌ ERROR: Could not find 'schedules.csv'.")
        print(f"      Please check it is in: {RAW_STATIC_DIR}")
        return

    print(f"   Found file at: {csv_path}")

    try:
        df = pd.read_csv(csv_path, low_memory=False)
        
        # Mapping for the specific file structure you showed me
        col_map = {
            'Train No.': 'Train_No',
            'train Name': 'Train_Name',
            'station Code': 'Station_Code',
            'Station Name': 'Station_Name',
            'islno': 'Sequence',
            'Arrival tim': 'Arrival_Time', 
            'Departure': 'Departure_Time',
            'Distance': 'Distance',
            'Source Station Name': 'Source_Station',
            'Destination Station Name': 'Destination_Station'
        }
        
        # Rename and Normalize
        df.rename(columns=col_map, inplace=True)
        
        # Select Columns
        required_cols = ['Train_No', 'Station_Code', 'Station_Name', 'Sequence', 'Arrival_Time', 'Departure_Time', 'Distance', 'Source_Station', 'Destination_Station']
        existing_cols = [c for c in required_cols if c in df.columns]
        df = df[existing_cols]
        
        # Clean Time Strings (remove ' and None)
        for col in ['Arrival_Time', 'Departure_Time']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace("'", "").str.replace("None", "00:00:00")

        output_path = os.path.join(PROCESSED_DIR, "clean_schedules.csv")
        df.to_csv(output_path, index=False)
        print(f"   ✅ Success! Saved {len(df)} schedule rows to {output_path}")

    except Exception as e:
        print(f"   ❌ Schedule Error: {e}")

if __name__ == "__main__":
    download_station_data()
    process_stations()
    process_schedules()