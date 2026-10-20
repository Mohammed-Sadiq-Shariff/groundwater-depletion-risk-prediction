"""
Chart and visualization utilities for the groundwater dashboard.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple


def create_groundwater_trend_chart(timeseries_df, station_name):
    """
    Create an interactive time series chart for groundwater depth.
    
    Parameters:
    -----------
    timeseries_df : pd.DataFrame
        DataFrame with columns: Monitoring Date, groundwater_level_m
    station_name : str
        Name of the station
    
    Returns:
    --------
    fig : plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeseries_df['Monitoring Date'],
        y=timeseries_df['groundwater_level_m'],
        mode='lines+markers',
        name='Groundwater Depth',
        line=dict(color='#3498db', width=2),
        marker=dict(size=4, opacity=0.6),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Depth: %{y:.2f}m<extra></extra>',
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    # Add trend line
    if len(timeseries_df) > 1:
        z = np.polyfit(np.arange(len(timeseries_df)), timeseries_df['groundwater_level_m'].values, 1)
        p = np.poly1d(z)
        trend_line = p(np.arange(len(timeseries_df)))
        
        fig.add_trace(go.Scatter(
            x=timeseries_df['Monitoring Date'],
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color='#e74c3c', width=1, dash='dash'),
            hoverinfo='skip',
            showlegend=False
        ))
    
    fig.update_layout(
        title={
            'text': f'<b>Groundwater Depth Trend - {station_name}</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Monitoring Date',
        yaxis_title='Depth Below Ground (meters)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
    )
    
    return fig


def create_rainfall_distribution_chart(timeseries_df):
    """
    Create a multi-period rainfall chart.
    
    Parameters:
    -----------
    timeseries_df : pd.DataFrame
        DataFrame with rainfall columns (rain_7d, rain_30d, rain_90d, rain_180d, rain_365d)
    
    Returns:
    --------
    fig : plotly figure
    """
    fig = go.Figure()
    
    rainfall_cols = ['rain_7d', 'rain_30d', 'rain_90d', 'rain_180d', 'rain_365d']
    colors = ['#3498db', '#2980b9', '#1abc9c', '#27ae60', '#16a085']
    labels = ['7-Day', '30-Day', '90-Day', '180-Day', '365-Day']
    
    for col, color, label in zip(rainfall_cols, colors, labels):
        if col in timeseries_df.columns:
            fig.add_trace(go.Scatter(
                x=timeseries_df['Monitoring Date'],
                y=timeseries_df[col],
                mode='lines',
                name=label,
                line=dict(color=color, width=2),
                hovertemplate=f'<b>{label}</b><br>%{{x|%Y-%m-%d}}<br>Rainfall: %{{y:.1f}}mm<extra></extra>'
            ))
    
    fig.update_layout(
        title={
            'text': '<b>Rainfall Analysis - Multiple Time Periods</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Monitoring Date',
        yaxis_title='Rainfall (mm)',
        hovermode='x unified',
        template='plotly_white',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
    )
    
    return fig


def create_rainfall_vs_groundwater_chart(timeseries_df):
    """
    Create a dual-axis chart showing rainfall vs groundwater relationship.
    
    Parameters:
    -----------
    timeseries_df : pd.DataFrame
        DataFrame with both rainfall and groundwater columns
    
    Returns:
    --------
    fig : plotly figure
    """
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Groundwater Depth vs 30-Day Rainfall',),
        specs=[[{'secondary_y': False}], [{'secondary_y': False}]]
    )
    
    # Groundwater trend
    fig.add_trace(
        go.Scatter(
            x=timeseries_df['Monitoring Date'],
            y=timeseries_df['groundwater_level_m'],
            mode='lines',
            name='Groundwater Depth',
            line=dict(color='#3498db', width=2),
            hovertemplate='<b>Groundwater</b><br>%{x|%Y-%m-%d}<br>Depth: %{y:.2f}m<extra></extra>'
        ),
        row=1, col=1, secondary_y=False
    )
    
    # Rainfall
    fig.add_trace(
        go.Bar(
            x=timeseries_df['Monitoring Date'],
            y=timeseries_df['rain_30d'],
            name='30-Day Rainfall',
            marker=dict(color='#2ecc71', opacity=0.7),
            hovertemplate='<b>Rainfall (30-day)</b><br>%{x|%Y-%m-%d}<br>%{y:.1f}mm<extra></extra>'
        ),
        row=2, col=1, secondary_y=False
    )
    
    fig.update_xaxes(title_text='Monitoring Date', row=2, col=1)
    fig.update_yaxes(title_text='Depth Below Ground (m)', row=1, col=1)
    fig.update_yaxes(title_text='Rainfall (mm)', row=2, col=1)
    
    fig.update_layout(
        title={
            'text': '<b>Groundwater Depth vs Rainfall Pattern</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        hovermode='x unified',
        template='plotly_white',
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        showlegend=True
    )
    
    return fig


def create_risk_probability_chart(probabilities_dict, predicted_class):
    """
    Create a horizontal bar chart for risk probabilities.
    
    Parameters:
    -----------
    probabilities_dict : dict
        Dictionary with risk classes and probabilities
    predicted_class : str
        The predicted risk class (to highlight)
    
    Returns:
    --------
    fig : plotly figure
    """
    categories = list(probabilities_dict.keys())
    values = list(probabilities_dict.values())
    
    # Define colors based on risk category
    color_map = {
        'No Depletion': '#2ecc71',
        'Low': '#f1c40f',
        'Moderate': '#e67e22',
        'High': '#e74c3c'
    }
    
    colors = [color_map.get(cat, '#95a5a6') for cat in categories]
    
    # Make predicted class slightly darker/more opaque
    colors = [
        c if cat != predicted_class else c.replace(')', ', 1.0)')
        if 'rgba' in c else c
        for c, cat in zip(colors, categories)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=2)),
        text=[f'{v:.1f}%' for v in values],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Probability: %{x:.1f}%<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Depletion Risk Classification</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Probability (%)',
        yaxis_title='Risk Category',
        height=350,
        margin=dict(l=150, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        xaxis=dict(range=[0, 100], showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
        template='plotly_white'
    )
    
    return fig


def create_feature_importance_chart(feature_importance_df, top_n=15):
    """
    Create a horizontal bar chart for feature importance.
    
    Parameters:
    -----------
    feature_importance_df : pd.DataFrame
        DataFrame with columns: feature, importance_mean
    top_n : int
        Number of top features to display
    
    Returns:
    --------
    fig : plotly figure
    """
    # Filter to top features (by absolute value)
    df = feature_importance_df.copy()
    df['abs_importance'] = df['importance_mean'].abs()
    df = df.sort_values('abs_importance', ascending=False).head(top_n)
    df = df.sort_values('importance_mean', ascending=True)
    
    colors = ['#e74c3c' if x < 0 else '#3498db' for x in df['importance_mean']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['feature'],
        x=df['importance_mean'],
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v:.4f}' for v in df['importance_mean']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Top Features in Groundwater Prediction</b><br><sub>Permutation Importance</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Importance Score',
        yaxis_title='Feature',
        height=500,
        margin=dict(l=250, r=0, t=70, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        template='plotly_white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)')
    )
    
    return fig


def create_block_summary_chart(block_data_list):
    """
    Create a chart summarizing block statistics.
    
    Parameters:
    -----------
    block_data_list : list
        List of dictionaries with block summary data
    
    Returns:
    --------
    fig : plotly figure
    """
    df = pd.DataFrame(block_data_list)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Block'],
        y=df['Average GW Level (m)'],
        name='Avg GW Depth (m)',
        marker=dict(color='#3498db'),
        hovertemplate='<b>%{x}</b><br>Avg GW Depth: %{y:.2f}m<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Average Groundwater Level by Block</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title='Block',
        yaxis_title='Groundwater Depth (meters)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
        template='plotly_white',
        xaxis=dict(tickangle=-45),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.2)'),
        showlegend=False
    )
    
    return fig


def create_risk_distribution_chart(predictions_df):
    """
    Create a pie/donut chart showing risk distribution.
    
    Parameters:
    -----------
    predictions_df : pd.DataFrame
        DataFrame with the risk classification column
    
    Returns:
    --------
    fig : plotly figure
    """
    risk_column = 'predicted_depletion_risk'
    if risk_column not in predictions_df.columns:
        for candidate in ('Predicted Depletion Risk', 'depletion_risk'):
            if candidate in predictions_df.columns:
                risk_column = candidate
                break

    risk_counts = predictions_df[risk_column].value_counts()
    
    color_map = {
        'No Depletion': '#2ecc71',
        'Low': '#f1c40f',
        'Moderate': '#e67e22',
        'High': '#e74c3c'
    }
    
    colors = [color_map.get(risk, '#95a5a6') for risk in risk_counts.index]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>Stations: %{value}<br>Percentage: %{percent}<extra></extra>',
        textposition='inside',
        textinfo='label+percent'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Risk Distribution Across Stations</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        font=dict(family='Segoe UI, sans-serif', size=11),
    )
    
    return fig


# Import for subplot
from plotly.subplots import make_subplots
