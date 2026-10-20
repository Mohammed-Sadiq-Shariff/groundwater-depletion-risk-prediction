"""
Data loading utilities with caching for the groundwater dashboard.
"""

import os
import pandas as pd
import numpy as np
import joblib
import streamlit as st
from pathlib import Path


@st.cache_data
def load_groundwater_data():
    """Load and cache the processed groundwater dataset."""
    data_path = Path("data/processed/mysore_model_dataset.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    df['Monitoring Date'] = pd.to_datetime(df['Monitoring Date'])
    return df


@st.cache_data
def load_rainfall_data():
    """Load and cache the rainfall dataset."""
    data_path = Path("data/processed/mysore_rainfall_1991_2025.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Rainfall data not found at {data_path}")
    
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


@st.cache_resource
def load_prediction_model():
    """Load and cache the groundwater prediction model."""
    model_path = Path("models/groundwater_prediction_model.joblib")
    if not model_path.exists():
        raise FileNotFoundError(f"Prediction model not found at {model_path}")
    
    return joblib.load(model_path)


@st.cache_resource
def load_risk_model():
    """Load and cache the depletion risk classification model."""
    model_path = Path("models/groundwater_depletion_risk_model.joblib")
    if not model_path.exists():
        raise FileNotFoundError(f"Risk model not found at {model_path}")
    
    return joblib.load(model_path)


@st.cache_resource
def load_feature_info():
    """Load and cache prediction model feature information."""
    info_path = Path("models/feature_info.joblib")
    if not info_path.exists():
        raise FileNotFoundError(f"Feature info not found at {info_path}")
    
    return joblib.load(info_path)


@st.cache_resource
def load_risk_feature_info():
    """Load and cache risk model feature information."""
    info_path = Path("models/risk_feature_info.joblib")
    if not info_path.exists():
        raise FileNotFoundError(f"Risk feature info not found at {info_path}")
    
    return joblib.load(info_path)


@st.cache_data
def load_model_evaluation():
    """Load cached model evaluation metrics."""
    eval_path = Path("reports/model_evaluation_summary.csv")
    if not eval_path.exists():
        raise FileNotFoundError(f"Model evaluation not found at {eval_path}")
    
    return pd.read_csv(eval_path)


@st.cache_data
def load_risk_evaluation():
    """Load cached risk model evaluation metrics."""
    eval_path = Path("models/risk_validation_results.csv")
    if not eval_path.exists():
        raise FileNotFoundError(f"Risk evaluation not found at {eval_path}")
    
    return pd.read_csv(eval_path)


@st.cache_data
def load_feature_importance():
    """Load and cache feature importance data."""
    importance_path = Path("reports/feature_importance.csv")
    if not importance_path.exists():
        raise FileNotFoundError(f"Feature importance not found at {importance_path}")
    
    return pd.read_csv(importance_path)


@st.cache_data
def load_risk_confusion_matrix():
    """Load risk model confusion matrix."""
    matrix_path = Path("models/risk_confusion_matrix.csv")
    if not matrix_path.exists():
        # Return None if not available - this is optional
        return None
    
    return pd.read_csv(matrix_path)


def get_unique_stations(df):
    """Get sorted list of unique stations."""
    return sorted(df['Station'].unique().tolist())


def get_unique_blocks(df):
    """Get sorted list of unique blocks."""
    return sorted(df['Block'].unique().tolist())


def get_station_info(df, station):
    """Get detailed information for a station."""
    station_data = df[df['Station'] == station]
    if station_data.empty:
        return None
    
    # Get most recent record
    latest = station_data.sort_values('Monitoring Date').iloc[-1]
    
    info = {
        'Station': latest['Station'],
        'District': latest['District'],
        'Tehsil': latest['Tehsil'],
        'Block': latest['Block'],
        'Village': latest['Village'],
        'Latitude': latest['Latitude'],
        'Longitude': latest['Longitude'],
        'Records': len(station_data),
        'Date Range': f"{station_data['Monitoring Date'].min().strftime('%Y-%m-%d')} to {station_data['Monitoring Date'].max().strftime('%Y-%m-%d')}"
    }
    
    return info


def get_station_timeseries(df, station):
    """Get time series data for a station."""
    station_data = df[df['Station'] == station].copy()
    station_data = station_data.sort_values('Monitoring Date')
    return station_data[['Monitoring Date', 'groundwater_level_m', 'rain_7d', 'rain_30d', 'rain_90d', 'rain_180d', 'rain_365d']]


def get_block_summary(df, block):
    """Get summary statistics for a block."""
    block_data = df[df['Block'] == block]
    
    if block_data.empty:
        return None
    
    return {
        'Block': block,
        'Stations': block_data['Station'].nunique(),
        'Average GW Level (m)': block_data['groundwater_level_m'].mean(),
        'Min GW Level (m)': block_data['groundwater_level_m'].min(),
        'Max GW Level (m)': block_data['groundwater_level_m'].max(),
        'Std GW Level (m)': block_data['groundwater_level_m'].std(),
        'Records': len(block_data)
    }


def get_district_summary(df):
    """Get district-level summary statistics."""
    return {
        'Total Stations': df['Station'].nunique(),
        'Total Blocks': df['Block'].nunique(),
        'Average GW Level (m)': df['groundwater_level_m'].mean(),
        'Min GW Level (m)': df['groundwater_level_m'].min(),
        'Max GW Level (m)': df['groundwater_level_m'].max(),
        'Total Records': len(df),
        'Date Range': f"{df['Monitoring Date'].min().strftime('%Y-%m-%d')} to {df['Monitoring Date'].max().strftime('%Y-%m-%d')}"
    }
