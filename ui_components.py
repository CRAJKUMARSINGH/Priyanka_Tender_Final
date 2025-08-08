import streamlit as st
import time
from datetime import datetime
from theme import apply_component_theme, get_theme_colors, get_gradient_styles

def create_header():
    """Create an enhanced professional header with branding."""
    # Apply header theme
    st.markdown(apply_component_theme('header'), unsafe_allow_html=True)
    
    # Enhanced header with gradient background and professional styling
    header_html = """
    <div class="custom-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">
            🏗️ Tender Processing System
        </h1>
        <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Professional Tender Management & Document Generation Platform
        </p>
        <div style="margin-top: 15px;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                ✨ Enhanced UI Version 2.0
            </span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def create_footer():
    """Create an enhanced professional footer with credits and system info."""
    colors = get_theme_colors()
    gradients = get_gradient_styles()
    
    # Enhanced footer with professional styling
    footer_html = f"""
    <div style="
        background: {gradients['header_gradient']};
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-top: 50px;
        text-align: center;
        box-shadow: 0 -4px 8px rgba(0,0,0,0.1);
    ">
        <div style="margin-bottom: 20px;">
            <h3 style="margin: 0; font-weight: 600;">💼 Tender Processing System</h3>
            <p style="margin: 10px 0; opacity: 0.9;">
                Professional Document Generation & Tender Management Platform
            </p>
        </div>
        
        <div style="
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        ">
            <div>
                <strong>📊 Features</strong><br>
                <span style="font-size: 0.9rem;">NIT Processing • Document Generation • Report Creation</span>
            </div>
            <div>
                <strong>🚀 Technology</strong><br>
                <span style="font-size: 0.9rem;">Streamlit • Python • Professional UI</span>
            </div>
            <div>
                <strong>⚡ Performance</strong><br>
                <span style="font-size: 0.9rem;">Fast Processing • Real-time Updates • Secure</span>
            </div>
        </div>
        
        <div style="
            border-top: 1px solid rgba(255,255,255,0.3);
            padding-top: 20px;
            margin-top: 20px;
        ">
            <p style="margin: 5px 0; font-size: 0.9rem;">
                <strong>🏢 Developed for Professional Tender Management</strong>
            </p>
            <p style="margin: 5px 0; font-size: 0.8rem; opacity: 0.8;">
                © 2024 Tender Processing System • Enhanced UI Migration • Version 2.0
            </p>
            <p style="margin: 5px 0; font-size: 0.8rem; opacity: 0.7;">
                🌟 Professional Branding & Balloon Theme Integration Complete
            </p>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def show_balloons():
    """Display enhanced balloon animation with professional styling."""
    # Streamlit's built-in balloon animation
    st.balloons()
    
    # Enhanced celebration message with professional styling
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
        animation: celebrationPulse 2s ease-in-out;
    ">
        <h3 style="margin: 0; font-weight: 600;">🎉 Success!</h3>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem;">
            Operation completed successfully with enhanced UI experience!
        </p>
    </div>
    
    <style>
    @keyframes celebrationPulse {{
        0% {{ transform: scale(0.95); opacity: 0.7; }}
        50% {{ transform: scale(1.02); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    </style>
    """
    st.markdown(celebration_html, unsafe_allow_html=True)

def create_info_card(title: str, content: str, icon: str = "ℹ️"):
    """Create an enhanced professional info card with styling."""
    # Apply card theme
    st.markdown(apply_component_theme('card'), unsafe_allow_html=True)
    colors = get_theme_colors()
    
    card_html = f"""
    <div class="custom-card">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
            <h3 style="margin: 0; color: {colors['dark']}; font-weight: 600;">{title}</h3>
        </div>
        <p style="margin: 0; color: {colors['gray']}; line-height: 1.6;">
            {content}
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

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
