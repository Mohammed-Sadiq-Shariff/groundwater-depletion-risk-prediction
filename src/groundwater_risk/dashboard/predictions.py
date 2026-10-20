"""
Prediction utilities for groundwater levels and depletion risk.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import streamlit as st


def prepare_prediction_features(row, model_feature_names):
    """
    Prepare features for model prediction from a data row.
    
    Parameters:
    -----------
    row : dict or pd.Series
        A row of data containing groundwater and rainfall features
    model_feature_names : list
        List of feature names expected by the model
    
    Returns:
    --------
    X : np.ndarray
        Features array ready for model prediction
    """
    if isinstance(row, pd.Series):
        row_dict = row.to_dict()
    else:
        row_dict = row
    
    X = np.zeros((1, len(model_feature_names)))
    
    for i, feature in enumerate(model_feature_names):
        if feature in row_dict:
            value = row_dict[feature]
            # Handle NaN values
            if pd.isna(value):
                X[0, i] = 0
            else:
                X[0, i] = value
        else:
            X[0, i] = 0
    
    return X


def predict_groundwater_level(model, row, feature_names):
    """
    Predict the next groundwater level.
    
    Parameters:
    -----------
    model : trained sklearn model
        Groundwater prediction model
    row : dict or pd.Series
        A row of data with required features
    feature_names : list
        List of feature names used by the model
    
    Returns:
    --------
    prediction : float
        Predicted groundwater level (in meters)
    """
    X = prepare_prediction_features(row, feature_names)
    prediction = model.predict(X)[0]
    return prediction


def predict_depletion_risk(model, row, feature_names):
    """
    Predict the depletion risk category and probabilities.
    
    Parameters:
    -----------
    model : trained sklearn model
        Risk classification model
    row : dict or pd.Series
        A row of data with required features
    feature_names : list
        List of feature names used by the model
    
    Returns:
    --------
    risk_class : str
        Predicted risk category
    probabilities : dict
        Dictionary with probability for each risk class
    """
    X = prepare_prediction_features(row, feature_names)
    
    # Get prediction
    risk_class = model.predict(X)[0]
    
    # Get probabilities if available
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X)[0]
        classes = model.classes_
        probabilities = {cls: float(prob * 100) for cls, prob in zip(classes, proba)}
    else:
        # Fallback for models without probability
        probabilities = {risk_class: 100.0}
    
    return risk_class, probabilities


def get_risk_color(risk_category):
    """
    Get the color for a risk category.
    
    Parameters:
    -----------
    risk_category : str
        Risk category name
    
    Returns:
    --------
    color : str
        Hex color code
    """
    colors = {
        'No Depletion': '#2ecc71',  # Green
        'Low': '#f1c40f',            # Yellow
        'Moderate': '#e67e22',       # Orange
        'High': '#e74c3c',           # Red
    }
    return colors.get(risk_category, '#95a5a6')  # Gray default


def get_risk_emoji(risk_category):
    """Get emoji for risk category."""
    emojis = {
        'No Depletion': '✅',
        'Low': '⚠️',
        'Moderate': '🔴',
        'High': '🛑',
    }
    return emojis.get(risk_category, '❓')


def interpret_groundwater_change(current_level, predicted_level):
    """
    Interpret groundwater change direction and severity.
    
    Note: Groundwater level is measured as depth below ground surface.
    - Negative change (depth decreasing) = water table recovering/improving
    - Positive change (depth increasing) = water table deepening/worsening
    
    Parameters:
    -----------
    current_level : float
        Current groundwater depth (meters)
    predicted_level : float
        Predicted groundwater depth (meters)
    
    Returns:
    --------
    change : float
        Predicted change (negative = recovery)
    interpretation : str
        Human-readable interpretation
    direction : str
        'improving', 'stable', or 'depleting'
    """
    change = predicted_level - current_level
    
    if abs(change) < 0.1:
        interpretation = "Water table expected to remain relatively stable"
        direction = "stable"
    elif change < 0:
        # Negative change = depth decreasing = water table rising = good
        interpretation = f"Water table expected to rise (recover) by {abs(change):.2f}m"
        direction = "improving"
    else:
        # Positive change = depth increasing = water table falling = bad
        interpretation = f"Water table expected to deepen further by {change:.2f}m"
        direction = "depleting"
    
    return change, interpretation, direction


def calculate_change_confidence(model_r2):
    """
    Calculate confidence level in predictions based on model R² score.
    
    Parameters:
    -----------
    model_r2 : float
        Model R² score
    
    Returns:
    --------
    confidence : str
        Confidence level description
    """
    if model_r2 >= 0.8:
        return "Very High"
    elif model_r2 >= 0.6:
        return "High"
    elif model_r2 >= 0.4:
        return "Moderate"
    else:
        return "Low"


def format_probability_dict(prob_dict):
    """
    Format probability dictionary for display.
    
    Parameters:
    -----------
    prob_dict : dict
        Dictionary with risk classes and probabilities
    
    Returns:
    --------
    formatted : dict
        Dictionary with risk classes and formatted percentage strings
    """
    return {key: f"{value:.1f}%" for key, value in prob_dict.items()}
