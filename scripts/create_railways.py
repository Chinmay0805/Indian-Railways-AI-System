import sqlite3
import os

DB_FILE = "railways.db"

def create_dummy_db():
    # 1. Remove old file if it exists (clean slate)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # 2. Connect and Create Table
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trains (
        train_number TEXT PRIMARY KEY,
        train_name TEXT,
        source_station_name TEXT,
        destination_station_name TEXT
    )
    ''')

    # 3. Insert Sample Data
    sample_data = [
        ('12951', 'Rajdhani Express', 'Mumbai Central', 'New Delhi'),
        ('12952', 'Rajdhani Express', 'New Delhi', 'Mumbai Central'),
        ('12009', 'Shatabdi Express', 'Mumbai Central', 'Ahmedabad'),
        ('12010', 'Shatabdi Express', 'Ahmedabad', 'Mumbai Central'),
        ('22222', 'CSMT Rajdhani', 'Mumbai CSMT', 'Hazrat Nizamuddin'),
        ('11019', 'Konark Express', 'Mumbai CSMT', 'Bhubaneswar'),
        ('12137', 'Punjab Mail', 'Mumbai CSMT', 'Firozpur'),
        ('12617', 'Mangala Lakshadweep', 'Ernakulam', 'Hazrat Nizamuddin')
    ]

    cursor.executemany('INSERT INTO trains VALUES (?,?,?,?)', sample_data)
    conn.commit()
    conn.close()
    
    print(f"✅ Success! Created '{DB_FILE}' with {len(sample_data)} sample trains.")

if __name__ == "__main__":
    create_dummy_db()