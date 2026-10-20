"""
Reusable UI components for the groundwater dashboard.
"""

import streamlit as st
from typing import Optional, Dict, Any


def metric_card(label: str, value: Any, suffix: str = "", icon: str = "📊", 
                color: str = "#3498db", help_text: Optional[str] = None):
    """
    Display a professional metric card.
    
    Parameters:
    -----------
    label : str
        Card label
    value : any
        Metric value
    suffix : str
        Suffix to append to value
    icon : str
        Emoji icon
    color : str
        Hex color code
    help_text : str, optional
        Hover help text
    """
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.write(icon)
        
        with col2:
            if help_text:
                st.markdown(f"**{label}**", help=help_text)
            else:
                st.markdown(f"**{label}**")
            
            # Format value
            if isinstance(value, float):
                formatted_value = f"{value:.2f}{suffix}"
            else:
                formatted_value = f"{value}{suffix}"
            
            st.markdown(
                f"<div style='font-size: 24px; font-weight: bold; color: {color};'>"
                f"{formatted_value}</div>",
                unsafe_allow_html=True
            )


def risk_status_badge(risk_category: str):
    """
    Display a colored risk status badge.
    
    Parameters:
    -----------
    risk_category : str
        Risk category name
    """
    color_map = {
        'No Depletion': ('#2ecc71', '✅'),
        'Low': ('#f1c40f', '⚠️'),
        'Moderate': ('#e67e22', '🔴'),
        'High': ('#e74c3c', '🛑'),
    }
    
    if risk_category in color_map:
        color, emoji = color_map[risk_category]
        badge_html = (
            f"<div style='display: inline-block; "
            f"background-color: {color}; "
            f"color: white; "
            f"padding: 8px 16px; "
            f"border-radius: 20px; "
            f"font-weight: bold; "
            f"font-size: 14px;'>"
            f"{emoji} {risk_category}</div>"
        )
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.markdown(f"**{risk_category}**")


def info_section(title: str, content: str, icon: str = "ℹ️"):
    """
    Display an information section.
    
    Parameters:
    -----------
    title : str
        Section title
    content : str
        Section content (markdown supported)
    icon : str
        Emoji icon
    """
    st.markdown(f"### {icon} {title}")
    st.markdown(content)


def stat_row(label: str, value: str, detail: str = ""):
    """
    Display a single statistic row.
    
    Parameters:
    -----------
    label : str
        Stat label
    value : str
        Stat value
    detail : str, optional
        Additional detail text
    """
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.markdown(f"**{label}**")
    
    with col2:
        st.markdown(f"__{value}__")
    
    if detail:
        with col3:
            st.markdown(f"`{detail}`")


def create_filter_sidebar():
    """
    Create a professional filter sidebar.
    
    Returns:
    --------
    filters : dict
        Dictionary with selected filter values
    """
    st.sidebar.markdown("## 🔍 Filters")
    st.sidebar.markdown("---")
    
    filters = {}
    
    # You'll need to pass available options to this function
    # For now, return empty dict to be filled by app
    return filters


def prediction_comparison_box(current_level: float, predicted_level: float, 
                              change: float, interpretation: str, direction: str):
    """
    Display groundwater prediction comparison.
    
    Parameters:
    -----------
    current_level : float
        Current groundwater depth
    predicted_level : float
        Predicted groundwater depth
    change : float
        Change value
    interpretation : str
        Human-readable interpretation
    direction : str
        Direction: 'improving', 'stable', or 'depleting'
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Current Level")
            st.markdown(f"<div style='font-size: 28px; font-weight: bold; color: #3498db;'>"
                       f"{current_level:.2f}m</div>",
                       unsafe_allow_html=True)
            st.markdown("_Depth below ground surface_")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🎯 Predicted Level")
            st.markdown(f"<div style='font-size: 28px; font-weight: bold; color: #2980b9;'>"
                       f"{predicted_level:.2f}m</div>",
                       unsafe_allow_html=True)
            st.markdown("_Next observation forecast_")
    
    with col3:
        # Color based on direction
        if direction == 'improving':
            color = '#2ecc71'  # Green
            emoji = '📈'
        elif direction == 'depleting':
            color = '#e74c3c'  # Red
            emoji = '📉'
        else:
            color = '#95a5a6'  # Gray
            emoji = '➡️'
        
        with st.container(border=True):
            st.markdown(f"### {emoji} Change")
            st.markdown(f"<div style='font-size: 28px; font-weight: bold; color: {color};'>"
                       f"{change:+.2f}m</div>",
                       unsafe_allow_html=True)
            st.markdown(f"_{direction.capitalize()}_")
    
    # Interpretation box
    st.info(f"📝 **Interpretation**: {interpretation}")


def model_metrics_display(metric_name: str, mae: float = None, rmse: float = None, 
                         r2: float = None, accuracy: float = None, 
                         macro_f1: float = None, weighted_f1: float = None):
    """
    Display model performance metrics in a professional format.
    
    Parameters:
    -----------
    metric_name : str
        Name of the model being evaluated
    mae : float, optional
        Mean Absolute Error
    rmse : float, optional
        Root Mean Squared Error
    r2 : float, optional
        R² Score
    accuracy : float, optional
        Classification accuracy
    macro_f1 : float, optional
        Macro F1 score
    weighted_f1 : float, optional
        Weighted F1 score
    """
    with st.container(border=True):
        st.markdown(f"### {metric_name}")
        
        metrics = []
        if mae is not None:
            metrics.append(("MAE", f"{mae:.4f}", "🎯"))
        if rmse is not None:
            metrics.append(("RMSE", f"{rmse:.4f}", "📏"))
        if r2 is not None:
            metrics.append(("R² Score", f"{r2:.4f}", "📊"))
        if accuracy is not None:
            metrics.append(("Accuracy", f"{accuracy:.2%}", "✅"))
        if macro_f1 is not None:
            metrics.append(("Macro F1", f"{macro_f1:.4f}", "🎲"))
        if weighted_f1 is not None:
            metrics.append(("Weighted F1", f"{weighted_f1:.4f}", "⚖️"))
        
        cols = st.columns(len(metrics))
        
        for col, (label, value, icon) in zip(cols, metrics):
            with col:
                st.markdown(f"{icon} **{label}**")
                st.markdown(f"<div style='font-size: 18px; font-weight: bold;'>"
                           f"{value}</div>",
                           unsafe_allow_html=True)


def station_detail_panel(station_info: Dict[str, Any]):
    """
    Display detailed station information.
    
    Parameters:
    -----------
    station_info : dict
        Dictionary with station details
    """
    with st.container(border=True):
        st.markdown("### 📍 Station Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            for key in ['Station', 'Block', 'Village', 'District']:
                if key in station_info:
                    st.markdown(f"**{key}:** `{station_info[key]}`")
        
        with col2:
            for key in ['Tehsil', 'Latitude', 'Longitude']:
                if key in station_info:
                    value = station_info[key]
                    if isinstance(value, float):
                        value = f"{value:.6f}"
                    st.markdown(f"**{key}:** `{value}`")
        
        if 'Date Range' in station_info:
            st.markdown(f"**Date Range:** {station_info['Date Range']}")
        
        if 'Records' in station_info:
            st.markdown(f"**Total Records:** {station_info['Records']}")


def loading_spinner(text: str = "Loading..."):
    """Display a loading spinner with text."""
    with st.spinner(text):
        pass


def empty_state(title: str, message: str, icon: str = "⚠️"):
    """
    Display an empty state message.
    
    Parameters:
    -----------
    title : str
        Empty state title
    message : str
        Empty state message
    icon : str
        Emoji icon
    """
    st.markdown(f"### {icon} {title}")
    st.markdown(message)
    st.stop()


def footer():
    """Display a professional footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 12px; margin-top: 20px;'>
    <p><strong>Groundwater Depletion Risk Prediction Dashboard</strong></p>
    <p>Machine Learning Model | Mysore District, India</p>
    <p>Data Source: CGWB | Last Updated: 2024</p>
    </div>
    """, unsafe_allow_html=True)
