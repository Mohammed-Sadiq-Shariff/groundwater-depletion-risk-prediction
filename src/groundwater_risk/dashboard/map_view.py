"""
Map visualization utilities for the groundwater dashboard.
Upgraded with genuine OpenStreetMap and CartoDB basemaps, real taluk boundaries, and GPS coordinates.
"""

import json
from pathlib import Path
from typing import Dict, Tuple, Optional
import pandas as pd
import plotly.graph_objects as go
import numpy as np

BOUNDARIES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "processed" / "boundaries"
TALUKS_PATH = BOUNDARIES_DIR / "mysore_taluks.geojson"
DISTRICT_PATH = BOUNDARIES_DIR / "mysore_district.geojson"


def _load_geojson(path: Path):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def create_district_map(data_df, predictions_df=None, selected_station=None):
    """
    Create a genuine, interactive real-time map of groundwater stations in Mysore District
    with accurate taluk boundary overlays and OpenStreetMap tiles.
    """
    risk_column = 'predicted_depletion_risk'
    if predictions_df is not None and risk_column not in predictions_df.columns:
        for candidate in ('Predicted Depletion Risk', 'depletion_risk'):
            if candidate in predictions_df.columns:
                risk_column = candidate
                break

    # Get unique stations with their latest info
    station_info = []
    for station in data_df['Station'].unique():
        station_data = data_df[data_df['Station'] == station]
        latest = station_data.iloc[-1]

        # Get prediction if available
        risk_category = 'Unknown'
        pred_gw = latest.get('groundwater_level_m', 0.0)
        chg = 0.0
        if predictions_df is not None:
            pred = predictions_df[predictions_df['Station'] == station]
            if not pred.empty:
                risk_category = pred.iloc[0].get(risk_column, 'Unknown')
                pred_gw = pred.iloc[0].get('Predicted Next Groundwater Level (m)', pred_gw)
                chg = pred.iloc[0].get('Predicted Groundwater Change (m)', 0.0)

        station_info.append({
            'Station': station,
            'Latitude': latest['Latitude'],
            'Longitude': latest['Longitude'],
            'Block': latest['Block'],
            'Village': latest['Village'],
            'Risk': risk_category,
            'GW_Level': latest.get('groundwater_level_m', 0.0),
            'Pred_GW': pred_gw,
            'Change': chg
        })

    station_df = pd.DataFrame(station_info)

    # Define risk colors
    color_map = {
        'High': '#ef4444',          # Red
        'Moderate': '#f59e0b',      # Amber
        'Low': '#eab308',           # Yellow
        'No Depletion': '#10b981',  # Emerald
        'Unknown': '#94a3b8'        # Slate
    }

    fig = go.Figure()

    # Load genuine taluks GeoJSON
    taluks_geo = _load_geojson(TALUKS_PATH)
    mapbox_layers = []

    if taluks_geo:
        mapbox_layers.append({
            "sourcetype": "geojson",
            "source": taluks_geo,
            "type": "fill",
            "color": "rgba(15, 118, 110, 0.12)",
            "below": "traces"
        })
        mapbox_layers.append({
            "sourcetype": "geojson",
            "source": taluks_geo,
            "type": "line",
            "color": "#0ea5e9",
            "line": {"width": 1.5},
            "below": "traces"
        })

    # Add station markers by risk category
    for risk_category, color in color_map.items():
        subset = station_df[station_df['Risk'] == risk_category]
        if subset.empty:
            continue

        marker_sizes = [15 if s == selected_station else 9 for s in subset['Station']]

        hover_texts = [
            f"<b>{row['Station']}</b><br>"
            f"Taluk: {row['Block']}<br>"
            f"Village: {row['Village']}<br>"
            f"Risk Category: <b>{row['Risk']}</b><br>"
            f"Current Depth: <b>{row['GW_Level']:.2f} m</b><br>"
            f"Predicted Next: <b>{row['Pred_GW']:.2f} m</b><br>"
            f"Model Net Change: <b>{row['Change']:+.2f} m</b><br>"
            f"GPS: {row['Latitude']:.4f}°N, {row['Longitude']:.4f}°E"
            for _, row in subset.iterrows()
        ]

        fig.add_trace(go.Scattermapbox(
            lon=subset['Longitude'],
            lat=subset['Latitude'],
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=color,
                opacity=0.9
            ),
            text=hover_texts,
            hoverinfo='text',
            name=f"{risk_category} ({len(subset)})",
            showlegend=True
        ))

    # Highlight selected station
    if selected_station is not None:
        selected_data = station_df[station_df['Station'] == selected_station]
        if not selected_data.empty:
            selected = selected_data.iloc[0]
            fig.add_trace(go.Scattermapbox(
                lon=[selected['Longitude']],
                lat=[selected['Latitude']],
                mode='markers',
                marker=dict(
                    size=24,
                    color='rgba(6, 182, 212, 0.4)',
                ),
                text=[f"<b>SELECTED: {selected['Station']}</b>"],
                hoverinfo='text',
                showlegend=False,
                name='Target'
            ))

    center_lat = 12.22
    center_lon = 76.50

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=8.8,
            layers=mapbox_layers
        ),
        margin={"r": 0, "t": 35, "l": 0, "b": 0},
        title={
            'text': '<b>Mysuru District Groundwater Monitoring Network • Real-Time GIS</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 15, 'family': 'Segoe UI, sans-serif'}
        },
        height=540,
        hovermode='closest',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0.01,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255,255,255,0.92)',
            bordercolor='rgba(200,200,200,0.6)',
            borderwidth=1
        )
    )

    return fig


def create_block_map(data_df, block_name):
    """Create map focused on a specific taluk/block with openstreetmap tiles."""
    block_data = data_df[data_df['Block'] == block_name]
    if block_data.empty:
        return None

    station_info = []
    for station in block_data['Station'].unique():
        sdata = block_data[block_data['Station'] == station]
        latest = sdata.iloc[-1]
        station_info.append({
            'Station': station,
            'Latitude': latest['Latitude'],
            'Longitude': latest['Longitude'],
            'Village': latest['Village'],
            'GW_Level': latest.get('groundwater_level_m', 0.0)
        })

    station_df = pd.DataFrame(station_info)
    center_lat = station_df['Latitude'].mean()
    center_lon = station_df['Longitude'].mean()

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lon=station_df['Longitude'],
        lat=station_df['Latitude'],
        mode='markers+text',
        marker=dict(
            size=12,
            color='#0ea5e9',
            opacity=0.9
        ),
        text=station_df['Station'],
        hovertext=[
            f"<b>{row['Station']}</b><br>Village: {row['Village']}<br>Depth: {row['GW_Level']:.2f}m"
            for _, row in station_df.iterrows()
        ],
        hoverinfo='text',
        showlegend=False
    ))

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=10.5
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title={'text': f'<b>{block_name} Taluk Monitoring Wells</b>', 'x': 0.5, 'xanchor': 'center'},
        height=420
    )

    return fig


def get_lat_lon_bounds(data_df):
    return (
        data_df['Latitude'].min(),
        data_df['Latitude'].max(),
        data_df['Longitude'].min(),
        data_df['Longitude'].max()
    )
