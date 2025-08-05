import streamlit as st

def set_theme():
    st.markdown("""
        <style>
        .stButton>button { background-color: #4CAF50; color: white; }
        .stTextInput>div>input { border: 1px solid #4CAF50; }
        .stNumberInput>div>input { border: 1px solid #4CAF50; }
        .stFileUploader { border: 1px solid #4CAF50; }
        </style>
    """, unsafe_allow_html=True)