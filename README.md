# 🚆 Indian Railways AI-Powered Analytics & Intelligent Query Platform

![Python](https://img.shields.io/badge/-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_1.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Chroma-cc5500?style=for-the-badge&logo=database&logoColor=white)


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


