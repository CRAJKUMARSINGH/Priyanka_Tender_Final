import streamlit as st
from typing import Dict, Any, Optional

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
    
    /* Input field styling */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea {
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, 
    .stNumberInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
    }
    
    /* File uploader styling */
    .stFileUploader>div {
        border: 2px dashed #1f77b4;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .stFileUploader>div:hover {
        background-color: #e9ecef;
        border-color: #155a8a;
    }
    
    /* Balloon animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    .balloon {
        animation: float 6s ease-in-out infinite;
        display: inline-block;
        margin: 0 5px;
    }
    
    /* Pulse animation for success */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)