from sqlalchemy import Column, String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    
    code = Column(String, primary_key=True)  # The Station Code (e.g., NDLS)
    name = Column(String)
    state = Column(String)
    zone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationship: A station has many schedules
    schedules = relationship("TrainSchedule", back_populates="station")

class TrainSchedule(Base):
    __tablename__ = 'train_schedules'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_no = Column(String, index=True)  # String because some trains have letters
    station_code = Column(String, ForeignKey('stations.code'))
    station_name = Column(String)
    sequence = Column(Integer)
    arrival_time = Column(String)
    departure_time = Column(String)
    distance = Column(Float)
    source_station = Column(String)
    destination_station = Column(String)
    
    # Relationship: Link back to the Station table
    station = relationship("Station", back_populates="schedules")

# --- DATABASE CONNECTION ---
# For now, we use SQLite (creates a file 'railways.db'). 
# Later, we swap this string to connect to AWS/Postgres.
DATABASE_URL = "sqlite:///./railways.db"
engine = create_engine(DATABASE_URL)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database tables created successfully in {DATABASE_URL}")

if __name__ == "__main__":
    create_tables()