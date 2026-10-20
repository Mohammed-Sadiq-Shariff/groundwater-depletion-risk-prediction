# Groundwater Depletion Risk Prediction Dashboard

## Overview

The Groundwater Depletion Risk Prediction Dashboard is a professional, interactive Streamlit application that provides real-time visualization and forecasting of groundwater depletion risk across Mysore District, India.

This dashboard leverages machine learning models trained on 28+ years of groundwater monitoring data to:
- Predict next-period groundwater levels
- Classify depletion risk (No Depletion, Low, Moderate, High)
- Analyze historical trends and rainfall correlations
- Provide district and block-level summaries
- Display model performance metrics and feature importance

## Features

### 1. **Interactive Geographical Map**
- Displays all 97 monitoring stations across Mysore District
- Color-coded markers by predicted depletion risk:
  - 🟢 **Green** = No Depletion
  - 🟡 **Yellow** = Low Risk
  - 🟠 **Orange** = Moderate Risk
  - 🔴 **Red** = High Risk
- Click-to-select stations
- Zoom and pan controls
- Hover tooltips showing station details
- Auto-fit view based on visible stations

### 2. **Station-Level Predictions**
- Current groundwater depth
- Predicted next observation depth
- Predicted change direction and magnitude
- Depletion risk classification
- Risk probability distribution (4-class breakdown)
- Confidence metrics based on model R² score

### 3. **Historical Analysis**
- 28+ years of groundwater trend data (1996-2024)
- Interactive time-series charts
- Trend line overlay
- Seasonal pattern analysis
- Multi-period rainfall correlation

### 4. **Rainfall Analysis**
- 7-day, 30-day, 90-day, 180-day, 365-day rainfall periods
- Multi-period rainfall trends
- Correlation between rainfall and groundwater levels
- Dual-axis visualization

### 5. **District & Block Summaries**
- Total stations and spatial coverage
- Average groundwater levels by block
- Risk distribution pie charts
- Station count and block statistics

### 6. **Model Performance**
- Real evaluation metrics from trained models:
  - **Prediction Model:** HistGradientBoosting Regressor
    - MAE, RMSE, R² score
  - **Risk Model:** Random Forest Classifier
    - Accuracy, Macro F1, Weighted F1
- Interpretation guidance for each metric

### 7. **Feature Importance**
- Top 15 permutation importance features
- Positive and negative correlations
- Scientific interpretation
- Identifies most predictive variables

### 8. **Station Risk Table**
- Searchable, sortable data table
- All predictions and probabilities
- CSV export functionality
- Filterable by risk level and block

## Architecture

```
app.py                                Main Streamlit application
│
└── src/groundwater_risk/dashboard/
    ├── __init__.py                  Package initialization
    ├── data_loader.py               Data loading with caching
    ├── predictions.py               Model predictions & interpretation
    ├── charts.py                    Plotly visualizations
    ├── map_view.py                  Geographic mapping
    ├── components.py                Reusable UI components
    └── styles.py                    CSS styling & theming
```

## Data Pipeline

### Input Data
- **Groundwater Data:** `data/processed/mysore_model_dataset.csv`
  - 97 monitoring stations
  - 28+ years of observations
  - Includes computed rainfall features
  
- **Rainfall Data:** `data/processed/mysore_rainfall_1991_2025.csv`
  - Multi-period aggregations

### Models
- **Prediction Model:** `models/groundwater_prediction_model.joblib`
  - HistGradientBoosting Regressor
  - 30 features (lags, rolling statistics, rainfall, seasonal)
  - MAE: ~1.94m, RMSE: ~2.96m, R²: ~0.55

- **Risk Model:** `models/groundwater_depletion_risk_model.joblib`
  - Random Forest Classifier (4-class)
  - Accuracy: ~58.3%
  - Predicts: No Depletion, Low, Moderate, High

### Evaluation Artifacts
- `reports/model_evaluation_summary.csv` - Prediction metrics
- `models/risk_validation_results.csv` - Risk classification metrics
- `reports/feature_importance.csv` - Permutation importance

## How to Run

### Prerequisites
```bash
# Create a Python 3.9+ environment
python -m venv env
source env/Scripts/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Launch Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Usage Guide

### Sidebar Navigation
1. **Select Station:** Choose a monitoring station from the dropdown
2. **Filter by Block:** Optionally filter to a specific administrative block
3. **Filter by Risk:** Show only stations with a specific predicted risk level
4. **Date Range:** Adjust the historical data period for analysis
5. **Dashboard Info:** Quick statistics about data coverage

### Main Dashboard
1. **KPI Cards:** Overview metrics
2. **Map:** Click a station marker to select it
3. **Prediction Panel:** View current predictions for selected station
4. **Station Information:** Coordinates, coverage details
5. **Trends & Analysis:** Multiple tabs for different analysis views
6. **District Overview:** Risk distribution and summary stats
7. **Data Table:** Export all predictions

## Interpretation Guide

### Groundwater Levels
- Measurements are **depth below ground surface** (meters)
- **Lower values** = shallower water table = better/healthier
- **Higher values** = deeper water table = worse/depleting
- Typical ranges in Mysore: 5-15 meters

### Groundwater Change
- **Negative change** (↑ improving) = water table rising/recovering
- **Positive change** (↓ depleting) = water table falling/worsening
- Magnitude indicates severity of predicted change

### Risk Categories
- **No Depletion:** Stable/recovering groundwater, low risk
- **Low:** Slight depletion trend, manageable
- **Moderate:** Significant depletion, intervention recommended
- **High:** Severe depletion, immediate action needed

### Model Confidence
- **R² > 0.8:** Very High confidence
- **R² 0.6-0.8:** High confidence
- **R² 0.4-0.6:** Moderate confidence
- **R² < 0.4:** Low confidence

Confidence is based on the prediction model's R² score on test data.

## Technical Details

### Caching Strategy
- Data loaded once per session using `@st.cache_data`
- Models loaded once per session using `@st.cache_resource`
- Predictions cached in session state
- Minimal API overhead

### Performance Optimization
- Efficient pandas operations
- Vectorized numpy computations
- Lazy loading of visualizations
- Responsive plotly charts
- No synthetic or interpolated data

### Map Implementation
- **Technology:** Plotly Scattermapbox
- **Basemap:** OpenStreetMap (no API key required)
- **Auto-fit:** Dynamic zoom based on station spread
- **Interactive:** Hover, zoom, pan, select

## Limitations & Assumptions

1. **Data Limitations:**
   - Some stations have gaps in historical records
   - Earlier years (1996-2000) have sparse data
   - Rainfall data may have spatial resolution constraints

2. **Model Limitations:**
   - Predictions valid only for immediate next observation (~3 months)
   - Model trained on historical patterns; cannot predict unprecedented events
   - Risk classification accuracy ~58% (4-class problem)

3. **Interpretation Constraints:**
   - Predictions should not replace expert hydrogeological analysis
   - Local factors (pumping, recharge) not explicitly modeled
   - Climate variability may affect forecast accuracy

4. **Spatial Scope:**
   - Dashboard covers Mysore District only
   - Based on CGWB monitoring stations
   - Some areas may lack station coverage

## Model Details

### Feature Set (30 features)
**Temporal:**
- groundwater_level_m (previous observation)
- gw_lag_1, gw_lag_2, gw_lag_3, gw_lag_4
- gw_rolling_mean_3, gw_rolling_mean_4
- gw_rolling_std_3
- gw_change_1, gw_change_2

**Rainfall:**
- rain_7d, rain_30d, rain_90d, rain_180d, rain_365d

**Seasonal:**
- month, quarter, year
- month_sin, month_cos (trigonometric encoding)
- season

**Geographic:**
- Latitude, Longitude
- Station (categorical), Block (categorical), Village (categorical)
- Tehsil, District

**Statistics:**
- station_historical_mean
- station_historical_std

### Model Evaluation
- **Train/Test Split:** 80/20
- **Test Records:** 657
- **Mean Absolute Error:** 1.94m
- **Root Mean Squared Error:** 2.96m
- **R² Score:** 0.547

### Risk Model Evaluation
**Random Forest Classifier:**
- **Accuracy:** 58.3%
- **Macro F1 Score:** 0.445
- **Weighted F1 Score:** 0.565
- **Classes:** No Depletion, Low, Moderate, High

## Updating & Maintenance

### Adding New Data
1. Update `data/processed/mysore_model_dataset.csv` with new observations
2. Update `data/processed/mysore_rainfall_1991_2025.csv` with rainfall data
3. Run `src/groundwater_risk/train_models.py` to retrain models (if needed)
4. Update `reports/model_evaluation_summary.csv` and risk metrics

### Updating Models
1. Prepare new training data with features
2. Run training script: `src/groundwater_risk/train_models.py`
3. Save new models to `models/` directory
4. Update feature info files
5. Test dashboard with new models

### Deployment
- **Local Testing:** `streamlit run app.py`
- **Server Deployment:** Use Streamlit Cloud or self-hosted server
- **Docker:** Create Dockerfile for containerized deployment

## Requirements

See `requirements.txt` for full dependency list:
- Python >= 3.9
- Streamlit >= 1.20
- Pandas >= 1.5
- NumPy >= 1.20
- Plotly >= 5.10
- Scikit-learn >= 1.0
- JobLib >= 1.2
- Folium >= 0.13
- GeoPandas >= 0.11

## Support & Documentation

### External Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [CGWB Groundwater Data](https://cgwb.gov.in/)

### Project Files
- [Project Plan](project_plan.md) - Overall objectives and timeline
- [Methodology](methodology.md) - Data processing and modeling approach
- [Data Dictionary](data_dictionary.md) - Detailed data documentation

## License

See LICENSE file in project root.

---

**Last Updated:** January 2025
**Dashboard Version:** 1.0
**Data Coverage:** 1996-2024 (Mysore District, Karnataka, India)
