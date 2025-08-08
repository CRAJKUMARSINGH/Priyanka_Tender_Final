import streamlit as st
import time
from datetime import datetime
from theme import apply_component_theme, get_theme_colors, get_gradient_styles

def create_header():
    """Create the enhanced application header with professional styling (reference-aligned)."""
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
    """Create the enhanced application footer with professional styling and date utilities (reference-aligned)."""
    from datetime import datetime as _dt
    from date_utils import DateUtils as _DU
    _date_utils = _DU()
    _current_date = _date_utils.get_current_date()
    _current_time = _dt.now().strftime('%H:%M:%S')
    
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
                <strong style="color: #2c3e50;">{_current_date}</strong><br>
                <strong style="color: #2c3e50;">{_current_time}</strong>
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
    """Show celebration balloons with enhanced custom message (reference-aligned)."""
    st.balloons()
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
    """Create an enhanced informational card with professional styling (reference-aligned)."""
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

def create_metric_card(title: str, value: str, description: str = "", icon: str = "📊"):
    """Create an enhanced metric card with professional styling."""
    # Apply metric theme
    st.markdown(apply_component_theme('metric'), unsafe_allow_html=True)
    
    metric_html = f"""
    <div class="custom-metric">
        <div style="font-size: 1.5rem; margin-bottom: 10px;">{icon}</div>
        <div class="metric-value">{value}</div>
        <h3>{title}</h3>
        <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 0.9rem;">
            {description}
        </p>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

def create_status_indicator(status: str, message: str):
    """Create an enhanced status indicator with professional styling."""
    colors = get_theme_colors()
    
    status_config = {
        'success': {'color': colors['success'], 'icon': '✅', 'bg': '#d4edda'},
        'warning': {'color': colors['warning'], 'icon': '⚠️', 'bg': '#fff3cd'},
        'error': {'color': colors['danger'], 'icon': '❌', 'bg': '#f8d7da'},
        'info': {'color': colors['info'], 'icon': 'ℹ️', 'bg': '#d1ecf1'}
    }
    
    config = status_config.get(status, status_config['info'])
    
    status_html = f"""
    <div style="
        background: {config['bg']};
        border-left: 4px solid {config['color']};
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.2rem; margin-right: 10px;">{config['icon']}</span>
        <span style="font-weight: 500; color: {colors['dark']};">{message}</span>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)

def create_progress_card(title: str, progress: float, description: str = ""):
    """Create an enhanced progress card with professional styling."""
    colors = get_theme_colors()
    gradients = get_gradient_styles()
    
    progress_html = f"""
    <div style="
        background: {gradients['background_gradient']};
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 4px solid {colors['primary']};
        margin: 15px 0;
    ">
        <h4 style="margin: 0 0 15px 0; color: {colors['dark']};">{title}</h4>
        
        <div style="
            background: #e9ecef;
            border-radius: 10px;
            height: 12px;
            margin: 10px 0;
            overflow: hidden;
        ">
            <div style="
                background: {gradients['primary_gradient']};
                height: 100%;
                width: {progress}%;
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.9rem; color: {colors['gray']};">{description}</span>
            <span style="font-weight: 600; color: {colors['primary']};">{progress:.1f}%</span>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

def create_action_button(label: str, icon: str = "🚀", button_type: str = "primary"):
    """Create an enhanced action button with professional styling."""
    colors = get_theme_colors()
    
    button_style = f"""
    <style>
    .custom-action-button {{
        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        margin: 5px;
    }}
    
    .custom-action-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    if button_type == "primary":
        return st.button(f"{icon} {label}", type="primary")
    elif button_type == "secondary":
        return st.button(f"{icon} {label}", type="secondary")
    else:
        return st.button(f"{icon} {label}")

def show_celebration_message(message: str = "Operation completed successfully!"):
    """Show a celebration message with enhanced styling."""
    colors = get_theme_colors()
    
    celebration_html = f"""
    <div style="
        background: linear-gradient(135deg, {colors['success']}, #20c997);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: celebrationSlide 1s ease-out;
    ">
        <div style="font-size: 2rem; margin-bottom: 10px;">🎉</div>
        <h3 style="margin: 0; font-weight: 600;">Celebration!</h3>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem;">
            {message}
        </p>
    </div>
    
    <style>
    @keyframes celebrationSlide {{
        0% {{ transform: translateY(-20px); opacity: 0; }}
        100% {{ transform: translateY(0); opacity: 1; }}
    }}
    </style>
    """
    st.markdown(celebration_html, unsafe_allow_html=True)

def create_feature_grid():
    """Create a feature grid showcasing system capabilities."""
    colors = get_theme_colors()
    
    features = [
        {"icon": "📄", "title": "Document Processing", "desc": "Advanced NIT processing"},
        {"icon": "👥", "title": "Bidder Management", "desc": "Comprehensive bidder database"},
        {"icon": "📊", "title": "Report Generation", "desc": "Professional document creation"},
        {"icon": "🔍", "title": "Data Analysis", "desc": "Intelligent data processing"}
    ]
    
    cols = st.columns(len(features))
    
    for i, feature in enumerate(features):
        with cols[i]:
            feature_html = f"""
            <div style="
                background: linear-gradient(135deg, #ffffff, #f8f9fa);
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-left: 4px solid {colors['primary']};
                margin: 10px 0;
                transition: transform 0.2s ease;
                height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 10px;">{feature['icon']}</div>
                <h4 style="margin: 0; color: {colors['dark']}; font-weight: 600;">{feature['title']}</h4>
                <p style="margin: 10px 0 0 0; color: {colors['gray']}; font-size: 0.9rem;">
                    {feature['desc']}
                </p>
            </div>
            """
            st.markdown(feature_html, unsafe_allow_html=True)

def create_system_status():
    """Create a system status indicator with enhanced styling."""
    colors = get_theme_colors()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    status_html = f"""
    <div style="
        background: linear-gradient(135deg, {colors['light']}, {colors['white']});
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {colors['success']};
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <span style="color: {colors['success']}; font-weight: 600;">🟢 System Online</span>
            <span style="margin-left: 20px; color: {colors['gray']};">Enhanced UI Active</span>
        </div>
        <div style="color: {colors['gray']}; font-size: 0.9rem;">
            {current_time}
        </div>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)
