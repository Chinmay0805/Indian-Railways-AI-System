# Indian Railways AI-Powered Analytics & Intelligent Query Platform

![Status](https://img.shields.io/badge/Status-Phase_0_Architecture-blue)
![Tech Stack](https://img.shields.io/badge/Stack-Python_FastAPI_React_PostgreSQL-green)

## 📖 Project Objective
An end-to-end AI platform that analyzes train movement across Tier-1 cities, detects delay patterns, and allows users to query data using natural language (e.g., *"Why is the 12138 Punjab Mail delayed?"*).

The system integrates **Traditional Machine Learning (XGBoost)** for delay prediction with **Generative AI (RAG)** for unstructured policy and rule querying.

## 🏗️ System Architecture
The project follows a **Hybrid RAG Architecture** with a semantic router dispatching queries between a SQL Data Warehouse and a Vector Database.
*(See `docs/architecture_diagram.png` for visual representation)*

## ❓ Business Questions Solved
This platform answers three categories of user intents:

**1. Analytics & Reporting (SQL)**
- What are the top 10 busiest stations on Sunday?
- Which route has the highest average delay during Monsoons?
- Identify trains with >90% on-time performance.

**2. Predictive Intelligence (Machine Learning)**
- Predict the delay of Train X at Station Y given current weather Z.
- Forecast passenger traffic volume for the upcoming Diwali season.

**3. Knowledge Retrieval (RAG)**
- What are the refund rules for a Tatkal ticket cancelled 2 hours before departure?
- Explain the dynamic pricing logic for Vande Bharat Express.

## 🛠️ Tech Stack
- **Data Engineering:** Python, Pandas, SQLAlchemy
- **Database:** PostgreSQL (Structured), ChromaDB (Vector)
- **AI/ML:** Scikit-Learn, XGBoost, LangChain, OpenAI/Gemini API
- **Backend:** FastAPI, Pydantic
- **Frontend:** React.js, TailwindCSS, Recharts
- **DevOps:** Docker, GitHub Actions (Planned)

## 📂 Project Structure
```text
/data          -> Raw and processed datasets
/database      -> SQL schemas and migration scripts
/notebooks     -> Jupyter notebooks for EDA and prototyping
/backend       -> FastAPI application and ML inference
/frontend      -> React application
/docs          -> Architecture diagrams and design docs