"""
Styling utilities for the groundwater dashboard.
"""

import streamlit as st


def apply_dashboard_styles():
    """Apply custom CSS styling to the entire dashboard."""
    
    custom_css = """
    <style>
    /* Main color palette */
    :root {
        --primary-color: #3498db;
        --secondary-color: #2c3e50;
        --accent-color: #e67e22;
        --success-color: #2ecc71;
        --warning-color: #f1c40f;
        --danger-color: #e74c3c;
        --light-bg: #ecf0f1;
        --border-color: #bdc3c7;
    }
    
    /* Body and general styling */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #7f8c8d;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    /* Cards styling */
    [data-testid="stContainer"] {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 16px;
        background-color: #ffffff;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #3498db;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput, .stNumberInput, .stSelectbox, .stMultiSelect {
        border-radius: 6px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 16px;
        background-color: transparent;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: #3498db;
        color: #3498db;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 20px 0;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 6px;
        padding: 12px 16px;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #f8f9fa;
    }
    
    .stSidebar > div:first-child {
        padding-top: 20px;
    }
    
    /* Sidebar header */
    .stSidebar .stMarkdown h1,
    .stSidebar .stMarkdown h2,
    .stSidebar .stMarkdown h3 {
        margin-top: 20px;
        margin-bottom: 10px;
        color: #2c3e50;
        font-weight: 700;
    }
    
    /* Text styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
    }
    
    code {
        background-color: #ecf0f1;
        padding: 2px 6px;
        border-radius: 3px;
        color: #e74c3c;
        font-family: 'Courier New', monospace;
    }
    
    /* Data frame styling */
    .stDataFrame {
        font-size: 0.95rem;
    }
    
    /* Sections */
    .section-header {
        border-top: 3px solid #3498db;
        padding-top: 15px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        
        .subtitle {
            font-size: 0.95rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #bdc3c7;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7f8c8d;
    }
    
    /* Animation for value changes */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-value {
        animation: slideIn 0.5s ease-in-out;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)


def get_risk_color(risk_category: str) -> str:
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


def get_risk_badge_html(risk_category: str, size: str = "normal") -> str:
    """
    Get HTML for a risk badge.
    
    Parameters:
    -----------
    risk_category : str
        Risk category name
    size : str
        Size: "small", "normal", or "large"
    
    Returns:
    --------
    html : str
        HTML badge code
    """
    color = get_risk_color(risk_category)
    
    size_map = {
        'small': {'padding': '4px 8px', 'font-size': '11px'},
        'normal': {'padding': '8px 16px', 'font-size': '14px'},
        'large': {'padding': '12px 24px', 'font-size': '16px'}
    }
    
    style = size_map.get(size, size_map['normal'])
    
    emoji_map = {
        'No Depletion': '✅',
        'Low': '⚠️',
        'Moderate': '🔴',
        'High': '🛑'
    }
    emoji = emoji_map.get(risk_category, '❓')
    
    badge_html = (
        f"<span style='"
        f"display: inline-block; "
        f"background-color: {color}; "
        f"color: white; "
        f"padding: {style['padding']}; "
        f"border-radius: 20px; "
        f"font-weight: bold; "
        f"font-size: {style['font-size']}; "
        f"white-space: nowrap;'>"
        f"{emoji} {risk_category}</span>"
    )
    return badge_html


def header_section(title: str, subtitle: str = ""):
    """
    Display a styled header section.
    
    Parameters:
    -----------
    title : str
        Section title
    subtitle : str, optional
        Section subtitle
    """
    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)
    
    st.markdown("---")


def create_section_header(title: str, icon: str = "📊"):
    """
    Create a styled section header.
    
    Parameters:
    -----------
    title : str
        Section title
    icon : str
        Emoji icon
    """
    st.markdown(f"<div class='section-header'><h2>{icon} {title}</h2></div>", 
                unsafe_allow_html=True)


def success_message(text: str):
    """Display a success message."""
    st.success(f"✅ {text}")


def warning_message(text: str):
    """Display a warning message."""
    st.warning(f"⚠️ {text}")


def error_message(text: str):
    """Display an error message."""
    st.error(f"❌ {text}")


def info_message(text: str):
    """Display an info message."""
    st.info(f"ℹ️ {text}")
