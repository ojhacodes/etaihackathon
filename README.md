# AQI Sentinel 🌍
*Hyperlocal Air Quality Forecasting & Attribution Platform*

AQI Sentinel is an AI-powered Urban Air Quality Intelligence platform designed for city administrators. Moving beyond simple reactive dashboards, this platform provides **predictive forecasting**, **geospatial source attribution**, and **actionable enforcement intelligence** to help cities reduce pollution at its source.

## 🚀 Key Features
- **Hyperlocal Forecasting (72H):** Predicts AQI up to 3 days in advance using LightGBM models trained on historical and meteorological data.
- **Dynamic Source Attribution:** Uses SHAP values cross-referenced with ground-truth emission inventories (like UrbanEmissions.info APnA) to separate weather impacts from actual human-made pollution sources (e.g., Vehicle Exhaust vs. Industrial).
- **Intervention Recommendation Engine:** Automatically generates actionable insights and advisories (e.g., "Implement heavy-vehicle restrictions") based on the dominant pollution source in a specific grid.
- **Multi-City Scalability:** Architecture is designed to easily onboard new cities. Currently prototyped for Delhi, Mumbai, and Bengaluru.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Leaflet (Maps), Recharts
- **Backend:** Python, FastAPI, Uvicorn
- **AI/ML:** LightGBM, SHAP, Pandas, Scikit-Learn

## ⚙️ Running Locally

### 1. Start the Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn api.main:app --reload --env-file .env
```
*(Backend runs on `http://localhost:8000`)*

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
*(Frontend runs on `http://localhost:5173`)*

## 🏆 Hackathon Value Proposition
This project directly addresses the need for **actionable intelligence**. By showing exactly *what* is causing the pollution and recommending *what* to do about it, AQI Sentinel empowers policymakers to make data-driven decisions that actively improve public health.
