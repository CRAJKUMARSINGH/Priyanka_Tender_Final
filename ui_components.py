import streamlit as st
from datetime import datetime
from date_utils import DateUtils

def create_header():
    """Create the enhanced application header with professional styling."""
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 25px; 
        background: linear-gradient(135deg, #1f77b4, #2c3e50); 
        border-radius: 12px; 
        margin-bottom: 30px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
            border-radius: 50%;
        "></div>
        
        <div style="
            position: absolute;
            bottom: -30px;
            left: -30px;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 70%);
            border-radius: 50%;
        "></div>
        
        <h1 style="
            color: white; 
            margin: 0; 
            font-size: 2.8em; 
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        ">
            🏗️ Tender Processing System
        </h1>
        <p style="
            color: #ecf0f1; 
            margin: 15px 0 0 0; 
            font-size: 1.3em;
            font-weight: 500;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            font-style: italic;
            position: relative;
            z-index: 1;
        ">
            An Initiative by Public Works Department, Government of Rajasthan
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """Create the enhanced application footer with professional styling and date utilities."""
    date_utils = DateUtils()
    current_date = date_utils.get_current_date()
    current_time = datetime.now().strftime('%H:%M:%S')
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            text-align: center; 
            padding: 15px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 10px;
            border-left: 4px solid #17a2b8;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <p style="color: #495057; font-size: 0.9em; margin: 0; font-weight: 600;">
                🕒 Current Time<br>
                <strong style="color: #2c3e50;">{current_date}</strong><br>
                <strong style="color: #2c3e50;">{current_time}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            text-align: center; 
            padding: 25px; 
            background: linear-gradient(135deg, #667eea, #764ba2); 
            border-radius: 12px; 
            border-left: 4px solid #1f77b4;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
        ">
            <p style="
                color: #f8f9fa; 
                margin: 0;
                font-size: 1.3em;
                font-weight: 700;
                line-height: 1.4;
            ">
                PWD Electric Division - Udaipur
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            text-align: center; 
            padding: 15px;
            background: linear-gradient(135deg, #28a745, #20c997);
            border-radius: 10px;
            border-left: 4px solid #28a745;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <p style="color: white; font-size: 0.9em; margin: 0; font-weight: 600;">
                System Status: <span style="color: #d4edda;">Operational</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_balloons():
    """Show celebration balloons with enhanced custom message."""
    st.balloons()
    
    # Enhanced celebration message with better styling
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 20px; 
        background: linear-gradient(135deg, #ff6b6b, #feca57); 
        border-radius: 12px; 
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    ">
        <h3 style="
            color: white; 
            margin: 0; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 700;
            font-size: 1.8em;
        ">
            Congratulations! 
        </h3>
        <p style="
            color: white; 
            margin: 10px 0 0 0; 
            font-size: 1.2em; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            font-weight: 600;
        ">
            Operation completed successfully with enhanced date handling accuracy!
        </p>
        <div style="
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.9;
        ">
            <span style="color: white;"> Professional • Accurate • Fast • Date-Safe</span>
        </div>
    </div>
    
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

def create_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Create an enhanced informational card with professional styling."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.2)'" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.15)'">
        <h4 style="
            color: white; 
            margin: 0 0 15px 0;
            font-weight: 700;
            font-size: 1.3em;
        ">
            {icon} {title}
        </h4>
        <p style="
            color: #f8f9fa; 
            margin: 0; 
            line-height: 1.7;
            font-size: 1.05em;
            font-weight: 500;
        ">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)