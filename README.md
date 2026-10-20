# HydroSight: AI-Based Groundwater Depletion Risk Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg)](https://vitejs.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end, reproducible machine learning system and interactive decision-support application for assessing groundwater level fluctuations and categorical depletion risk across **92 monitoring stations in Mysuru District, Karnataka, India**.

Accompanies the research paper: **"AI-Based Groundwater Depletion Risk Prediction for Mysuru District Using Machine Learning"** (`paper_revision_v2/main_submission_v2.pdf`).

---

## 📌 System Architecture

HydroSight is structured as a decoupled, modern full-stack web application:

```
┌────────────────────────────────────────────────────────┐
│                   Data Sources (NWDP)                  │
│  - CGWB Manual Quarterly GWL (1991–2020 & 2021–2025)   │
│  - Karnataka Manual Daily Rainfall (15 CSVs, 1989–2025)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              Preprocessing & Feature Pipeline          │
│  - Station filtering, coordinate/date harmonization    │
│  - GWL lags (1–4), rolling stats, change metrics       │
│  - Rainfall accumulation windows (7, 30, 90, 180, 365d)│
│  - Strict chronological 70%/15%/15% split              │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│             Machine Learning Models (Scikit-Learn)     │
│  - Regression: HistGradientBoosting (GWL level)        │
│  - Classification: Random Forest (4 Depletion Classes) │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               Decoupled Full-Stack Web App             │
│  - Backend: FastAPI (REST API, Port 8000)              │
│  - Frontend: React + Vite + TypeScript (Port 5173)     │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset Provenance & Coverage

All groundwater and precipitation data originate from official government portals hosted on the **National Water Data Portal (NWDP)**:

1. **Groundwater Observations (CGWB)**:
   - **Historical Archive (1991–2020)**: NWDP Resource [`3dacbc24`](https://nwdp.nwic.gov.in/dataset/gwl-manual-quarterly-central-ground-water-board-department/resource/3dacbc24-b45c-4ffe-8099-f69728ca711b) (`gwl_manual_quarterly_cgwb_ka_1991_2020.csv`).
   - **Recent Archive (2021–2025)**: NWDP Resource [`7b76b032`](https://nwdp.nwic.gov.in/dataset/gwl-manual-quarterly-central-ground-water-board-department/resource/7b76b032-99a5-4725-8ab5-125346e7aebf) (`groundwater_karnataka_2021_2025.csv`).
   - **Filtered Dataset**: **4,185 records** across **92 unique monitoring wells** in Mysuru district (1997–2023), requiring $\ge 4$ historical observations per well for lag computation.
2. **Precipitation Data (NWIC)**:
   - Karnataka Manual Daily Rainfall: NWDP Dataset [`rainfall-manual-daily-karnataka`](https://nwdp.nwic.gov.in/dataset/rainfall-manual-daily-karnataka), assembled from 15 multi-year daily snapshot files (1989–2025).
   - *Limitation*: As transparently documented in the paper, a data gap in December 2023 is noted; affected rolling windows are retained as partial accumulations rather than imputing unverified zero rainfall.

---

## 🔬 Experimental Setup & Verified Metrics

### Chronological Splitting Strategy
To prevent temporal data leakage, all splits use strict date quantile partitioning:
- **Regression Split** (70%/15%/15% of unique observation dates):
  - **Train**: 2,624 records (1997-01-05 to 2015-08-25)
  - **Validation**: 904 records (2015-11-05 to 2019-08-19)
  - **Test**: 657 records (2019-11-11 to 2023-11-05)
- **Classification Split**:
  - Enforces `next_monitoring_date <= split_end`, purging 113 boundary-crossing transitions:
  - **Train**: 2,569 records | **Validation**: 846 records | **Test**: 657 records

### Verified Evaluation Results (Held-Out Test Set, N = 657)

#### 1. Next-Observation GWL Regression
Target: Depth to water level in metres below ground level (mbgl) at the next observation (horizon: 40–200 days, median 91 days).

| Model | MAE (m) | RMSE (m) | $R^2$ | Error Reduction vs Baselines |
| :--- | :---: | :---: | :---: | :--- |
| **Mean-Target Baseline** | 3.43 | 4.39 | — | — |
| **Persistence Baseline** | 2.15 | 3.39 | — | — |
| **HistGradientBoosting (Ours)** | **1.94** | **2.96** | **0.547** | **43.4%** vs Mean, **9.8%** vs Persistence |

- **Empirical 95% Bootstrap Confidence Intervals** (1,000 resamples, seed 42):
  - $\text{MAE} \in [1.77, 2.10]\,\text{m}$
  - $\text{RMSE} \in [2.61, 3.32]\,\text{m}$
  - $R^2 \in [0.423, 0.639]$
  - Mean Residual: $-0.01\,\text{m}$ (negligible systematic bias)

#### 2. Depletion Risk Categorization (Random Forest)
Predicts 4-class depletion severity ($\Delta_t = \text{GWL}_{t+1} - \text{GWL}_t$):
- **Accuracy**: **52.8%** (vs 45.8% majority class, 30.4% stratified random)
- **Macro F1**: **0.457** | **Weighted F1**: **0.529**
- **Per-Class F1**: No Depletion: **0.70** ($N=301$), Low: **0.38** ($N=129$), Moderate: **0.42** ($N=147$), High: **0.33** ($N=80$)

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 1. Environment Installation
```bash
# Clone the repository
git clone https://github.com/<username>/groundwater-depletion-risk.git
cd groundwater-depletion-risk

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### 2. Verify Metrics Directly (Instant Replication)
You can verify the reported test metrics, baseline comparisons, confusion matrices, and confidence intervals in seconds directly from the saved prediction artefacts:
```bash
python paper_revision_v2/verify_metrics.py
```

### 3. Launch the HydroSight Web Application
HydroSight runs as a decoupled application with FastAPI and React:

#### Step A: Start the FastAPI Backend
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*API Swagger Documentation will be live at `http://127.0.0.1:8000/docs`.*

#### Step B: Start the React + Vite Frontend
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
*The web dashboard will be accessible at `http://localhost:5173`.*

---

## 🔄 Retraining & Feature Engineering (Optional)

To regenerate features and retrain models from scratch:

```bash
# 1. Feature Engineering
python src/groundwater_risk/build_features.py
python src/groundwater_risk/create_model_features.py
python src/groundwater_risk/create_target.py

# 2. Model Training
python src/groundwater_risk/train_models.py      # Regression pipeline
python src/groundwater_risk/train_risk_model.py  # Classification pipeline

# 3. Generate Dashboard Predictions
python generate_all_predictions.py
```

---

## 📂 Repository Layout

```
groundwater-depletion-risk/
├── backend/                  # FastAPI backend server
│   ├── app/
│   │   ├── main.py           # API endpoints
│   │   ├── config.py         # Data and model path configurations
│   │   ├── services/         # Data loading, prediction, reporting logic
│   │   └── schemas/          # Pydantic data schemas
│   └── requirements.txt      # Backend dependencies
├── frontend/                 # React + Vite + TypeScript frontend
│   ├── src/                  # Dashboard views, charts, and maps
│   ├── package.json
│   └── vite.config.ts
├── src/groundwater_risk/     # Core ML engineering and training pipelines
│   ├── build_features.py
│   ├── create_model_features.py
│   ├── create_target.py
│   ├── train_models.py       # HistGradientBoosting regression training
│   └── train_risk_model.py   # Random Forest risk classification training
├── models/                   # Test predictions & evaluation artefacts
│   ├── test_predictions.csv
│   └── risk_test_predictions.csv
├── reports/                  # Precomputed summaries, feature importances, and figures
│   ├── model_evaluation_summary.csv
│   ├── feature_importance.csv
│   └── all_station_predictions.csv
├── paper_revision_v2/        # IEEE Conference manuscript & verification suite
│   ├── main.tex              # Camera-ready LaTeX manuscript (6 pages)
│   ├── references.bib        # Verified literature survey bibliography
│   ├── figures/              # High-resolution vector and raster figures
│   ├── verify_metrics.py     # Independent metric verification script
│   └── main_submission_v2.pdf# Final verified 6-page submission PDF
├── data/
│   └── metadata/             # NWDP source registers and provenance notes
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 📄 License and Citation

This repository is licensed under the [MIT License](LICENSE).

If you find this work or software useful in your research, please cite:
```bibtex
@inproceedings{shariff2026groundwater,
  author    = {Shariff, Mohammed Sadiq and Ali, Shumail and Prasad S P, Deeksha and D, Nagashree},
  title     = {AI-Based Groundwater Depletion Risk Prediction for Mysuru District Using Machine Learning},
  year      = {2026},
  note      = {Manuscript: paper\_revision\_v2/main\_submission\_v2.pdf}
}
```
