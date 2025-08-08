import streamlit as st
from datetime import datetime

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
    ">
        <h1 style="
            color: white; 
            margin: 0; 
            font-size: 2.8em; 
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        ">
            🏗️ Tender Processing System
        </h1>
        <p style="
            color: #ecf0f1; 
            margin: 15px 0 0 0; 
            font-size: 1.3em;
            font-weight: 500;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        ">
            PWD Electric Division - Government Engineering Office
        </p>
        <div style="
            margin-top: 15px;
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            display: inline-block;
        ">
            <span style="color: #ffffff; font-size: 0.9em; font-weight: 500;">
                🔐 Secure • 📊 Efficient • 🎯 Accurate • 🌐 Modern • 📅 Enhanced Date Handling
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_footer():
    """Create the enhanced application footer with professional styling."""
    current_date = datetime.now().strftime('%d/%m/%Y')
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
        ">
            <h4 style="color: white; margin-bottom: 15px; font-weight: 700;">📋 System Information</h4>
            <p style="
                color: #f8f9fa; 
                line-height: 1.8;
                margin: 0;
                font-size: 1.05em;
                font-weight: 600;
            ">
                Professional Tender Processing System<br>
                Enhanced Date Handling & Document Generation<br>
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
        ">
            <p style="color: white; font-size: 0.9em; margin: 0; font-weight: 600;">
                💼 System Version<br>
                <strong style="font-size: 1.1em;">v2.1.1</strong><br>
                <span style="font-size: 0.8em; opacity: 0.9;">Date-Fixed Pro</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced copyright and additional info
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 20px; 
        color: #6c757d; 
        font-size: 0.85em; 
        border-top: 2px solid #dee2e6; 
        margin-top: 30px;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 8px;
    ">
        <p style="margin: 5px 0; font-weight: 600;">
            © 2024 PWD Electric Division Tender Processing System | Designed for Government Engineering Offices
        </p>
        <p style="margin: 10px 0; font-weight: 500;">
            🔒 Secure • 📊 Efficient • 🎯 Accurate • 🌐 Modern • 📅 Multi-Format Date Support • 📈 Enhanced Reporting
        </p>
        <p style="margin: 5px 0; font-size: 0.8em; color: #868e96;">
            Built with ❤️ for engineers, by engineers | Powered by Streamlit & Python | Date Bugs Fixed ✅
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
            🎉 Congratulations! 🎉
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
            <span style="color: white;">✨ Professional • 🎯 Accurate • ⚡ Fast • 📅 Date-Safe</span>
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

def create_success_message(message: str):
    """Create an enhanced styled success message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #28a745, #20c997);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #155724;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">✅</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_warning_message(message: str):
    """Create an enhanced styled warning message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #856404;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">⚠️</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_error_message(message: str):
    """Create an enhanced styled error message."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #dc3545, #c82333);
        padding: 18px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #721c24;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease;
    ">
        <p style="
            color: white; 
            margin: 0; 
            font-weight: 700;
            font-size: 1.1em;
            display: flex;
            align-items: center;
        ">
            <span style="font-size: 1.2em; margin-right: 10px;">❌</span>
            {message}
        </p>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(-100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
    """Create an enhanced metric display card with professional styling."""
    delta_html = f"""
    <p style='
        color: #28a745; 
        font-size: 0.95em; 
        margin: 8px 0 0 0;
        font-weight: 600;
    '>
        {delta}
    </p>
    """ if delta else ""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
        text-align: center;
        transition: all 0.3s ease;
    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 6px 16px rgba(0,0,0,0.15)'" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'">
        <p style="
            color: #6c757d; 
            margin: 0; 
            font-size: 0.95em;
            font-weight: 600;
        ">
            {icon} {label}
        </p>
        <h3 style="
            color: #2c3e50; 
            margin: 15px 0 0 0;
            font-weight: 700;
            font-size: 2em;
        ">
            {value}
        </h3>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
