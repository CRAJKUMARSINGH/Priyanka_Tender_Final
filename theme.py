import streamlit as st

def apply_custom_css():
    """Apply enhanced custom CSS while preserving Streamlit's default styling."""

    # Professional CSS enhancements that maintain Streamlit's core design
    custom_css = """
    <style>
    /* Enhanced app background */
    .stApp {
        background-color: #ffffff;
    }

    /* Professional sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Enhanced file uploader styling */
    .css-1cpxqw2 {
        border-radius: 8px;
        border: 2px dashed #1f77b4;
        padding: 20px;
        background-color: #f8f9fa;
    }

    /* Success message styling */
    .element-container .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        padding: 15px;
        font-weight: 500;
    }

    /* Warning message styling */
    .element-container .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 5px;
        padding: 15px;
        font-weight: 500;
    }

    /* Error message styling */
    .element-container .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 5px;
        padding: 15px;
        font-weight: 500;
    }

    /* Info message styling */
    .element-container .stInfo {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 5px;
        padding: 15px;
        font-weight: 500;
    }

    /* Enhanced button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Primary button styling */
    .stButton > button[data-baseweb="button"][data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #1f77b4, #2c3e50);
        border: none;
        color: white;
    }

    /* Download button enhancements */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #218838, #1ea080);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Metric containers with enhanced styling */
    .metric-container {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        margin: 15px 0;
        transition: transform 0.2s ease;
    }

    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }

    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        font-weight: 600;
    }

    /* Professional DataFrame styling */
    .dataframe {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .dataframe th {
        background: linear-gradient(135deg, #343a40, #495057);
        color: white;
        font-weight: bold;
        text-align: center;
        padding: 12px 8px;
    }

    .dataframe td {
        padding: 12px 8px;
        border-bottom: 1px solid #dee2e6;
        text-align: center;
    }

    /* Enhanced radio button styling */
    .stRadio > div {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Professional select box styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #ced4da;
        transition: border-color 0.3s ease;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
    }

    /* Enhanced text input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #ced4da;
        padding: 10px 15px;
        transition: all 0.3s ease;
        font-size: 14px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
        transform: translateY(-1px);
    }

    /* Enhanced number input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #ced4da;
        padding: 10px 15px;
        transition: all 0.3s ease;
        font-size: 14px;
    }

    .stNumberInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
        transform: translateY(-1px);
    }

    /* Enhanced progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1f77b4, #28a745);
        border-radius: 10px;
        height: 12px;
    }

    /* Professional sidebar styling */
    .css-1544g2n {
        padding-top: 2rem;
        background: linear-gradient(180deg, #f8f9fa, #ffffff);
    }

    /* Hide Streamlit branding for professional appearance */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}

    /* Custom scrollbar for better UX */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1f77b4, #2c3e50);
        border-radius: 6px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0f5799, #1a252f);
    }

    /* Enhanced table responsiveness */
    .element-container .stDataFrame {
        width: 100%;
        overflow-x: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 8px;
    }

    /* Professional spacing for columns */
    .element-container .css-ocqkz7 {
        gap: 1.5rem;
    }

    /* Enhanced form styling */
    .stForm {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Enhanced spinner styling */
    .stSpinner > div {
        border-top-color: #1f77b4 !important;
    }

    /* Professional alert styling */
    .element-container .alert {
        border-radius: 8px;
        padding: 15px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0px 0px;
        color: #495057;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f77b4, #2c3e50);
        color: white;
    }

    /* Card-like containers for better organization */
    .stContainer > div {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Enhanced header text styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
    }

    /* Professional status indicators */
    .status-success {
        color: #28a745;
        font-weight: bold;
    }

    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }

    .status-error {
        color: #dc3545;
        font-weight: bold;
    }

    .status-info {
        color: #17a2b8;
        font-weight: bold;
    }

    /* Date input enhancement */
    .stDateInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #ced4da;
        padding: 10px 15px;
        transition: all 0.3s ease;
        font-size: 14px;
    }

    .stDateInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
    }

    /* File uploader enhancement for date-related files */
    .stFileUploader > div > div {
        border-radius: 8px;
        border: 2px dashed #1f77b4;
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        transition: all 0.3s ease;
    }

    .stFileUploader > div > div:hover {
        border-color: #0f5799;
        background: linear-gradient(135deg, #e9ecef, #f8f9fa);
    }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

def get_theme_colors():
    """Return the enhanced theme color palette for consistency."""
    return {
        'primary': '#1f77b4',
        'secondary': '#2c3e50',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'white': '#ffffff',
        'gray': '#6c757d',
        'border': '#dee2e6'
    }

def get_gradient_styles():
    """Return enhanced gradient styles for professional appearance."""
    return {
        'primary_gradient': 'linear-gradient(135deg, #1f77b4, #2c3e50)',
        'success_gradient': 'linear-gradient(135deg, #28a745, #20c997)',
        'warning_gradient': 'linear-gradient(135deg, #ffc107, #fd7e14)',
        'info_gradient': 'linear-gradient(135deg, #17a2b8, #6f42c1)',
        'header_gradient': 'linear-gradient(90deg, #1f77b4, #2c3e50)',
        'card_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'background_gradient': 'linear-gradient(135deg, #f8f9fa, #ffffff)',
        'sidebar_gradient': 'linear-gradient(180deg, #f8f9fa, #ffffff)'
    }

def apply_component_theme(component_type: str = 'default'):
    """Apply specific theming for different component types with enhanced styling."""
    colors = get_theme_colors()
    gradients = get_gradient_styles()

    if component_type == 'header':
        return f"""
        <style>
        .custom-header {{
            background: {gradients['header_gradient']};
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        </style>
        """

    elif component_type == 'card':
        return f"""
        <style>
        .custom-card {{
            background: {gradients['background_gradient']};
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-left: 4px solid {colors['primary']};
            margin: 20px 0;
            transition: transform 0.2s ease;
        }}
        .custom-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }}
        </style>
        """

    elif component_type == 'metric':
        return f"""
        <style>
        .custom-metric {{
            background: {gradients['background_gradient']};
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-left: 4px solid {colors['primary']};
            margin: 15px 0;
            transition: all 0.3s ease;
        }}
        .custom-metric:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }}
        .custom-metric h3 {{
            color: {colors['dark']};
            margin: 15px 0 0 0;
            font-weight: 600;
        }}
        .custom-metric .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {colors['primary']};
            margin: 10px 0;
        }}
        </style>
        """

    return ""

def set_custom_theme():
    """Apply Streamlit page theme settings if needed (placeholder to satisfy imports)."""
    # This function can be expanded to call st.set_page_config theme in future
    return None

# Backward-compatible alias expected by app.py
get_gradient_style = get_gradient_styles
