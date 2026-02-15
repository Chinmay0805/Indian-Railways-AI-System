# 🚆 Indian Railways AI-Powered Analytics & Intelligent Query Platform


![Python](https://img.shields.io/badge/-3.11%2B-blue)
![ML](https://img.shields.io/badge/-Scikit_Learn-orange)
![Database](https://img.shields.io/badge/-SQLite%2FPostgreSQL-orange)


##  Project Overview
An end-to-end AI platform that analyzes train movement across India, detects delay patterns, and predicts future congestion. 

The system currently ingests data from open sources, processes it into a **SQL Data Warehouse**, and utilizes **Random Forest** and **Holt-Winters** algorithms to forecast delays.

###  Key Features Built
- **Data Engineering Pipeline:** - Automated ETL scripts to clean and merge raw CSV/JSON data.
  - Transformation of 8,000+ stations and 69,000+ schedule rows.
- **SQL Data Warehouse:** - Designed a normalized relational schema (Stations ↔ Schedules).
  - Implemented using **SQLAlchemy** (ORM) for scalability.
- **Predictive Modelling (Machine Learning):**
  - **Random Forest Regressor** trained to predict train delays.
  - **R2 Score:** *89* (Validated on unseen test data).
- **Time-Series Forecasting:**
  - **Holt-Winters Exponential Smoothing** to predict system-wide delays for the next 30 days.
  - Accounts for seasonality (e.g., weekends, winter fog).

---

## 🏗️ System Architecture
The project follows a modular Data Science architecture:

```mermaid
    indian-railways-ai/
├── data/
│   ├── raw/                  # Original datasets
│   ├── processed/            # Cleaned CSVs (ETL output)
│   └── reference_docs/       # PDFs for RAG System
├── database/
│   ├── models.py             # SQLAlchemy Schema
│   └── load_data.py          # Script to populate DB
├── scripts/
│   ├── process_data.py       # Data Cleaning & Validation
│   ├── generate_training.py  # Synthetic History Generator
│   ├── train_model.py        # ML Training (Random Forest)
│   ├── forecast_delays.py    # Time Series Forecasting
│   └── evaluate_model.py     # Performance Report Card
├── notebooks/                # EDA and Experiments
├── models/                   # Saved .pkl models
├── docs/                     # Images and Diagrams
└── README.md                 # Project Documentation

```

## Roadmap & Progress

 Phase 0: Architecture Design

 Phase 1-2: Data Collection & Cleaning

 Phase 3: SQL Warehouse Implementation

 Phase 4: Exploratory Data Analysis (EDA)

 Phase 5: Feature Engineering

 Phase 6: Machine Learning Model (Random Forest)

 Phase 7: Time Series Forecasting

 Phase 8: Model Evaluation

 Phase 9: RAG System (Chat with Data) ⏳ (In Progress)

 Phase 10: Dashboard (Power BI)

 Phase 11: Backend API (FastAPI)

 Phase 12: Frontend (React)

 Phase 13: Cloud Deployment
