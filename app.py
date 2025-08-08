import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import tempfile
import logging

# Import our enhanced custom modules
from theme import apply_custom_css, set_custom_theme, get_theme_colors, get_gradient_style
from ui_components import (
    custom_header, custom_footer, show_balloons, create_info_card, 
    create_header, create_footer, create_success_message, 
    create_warning_message, create_error_message, create_metric_card,
    show_date_parsing_status, create_progress_indicator
)
from tender_processor import TenderProcessor
from excel_parser import ExcelParser
from bidder_manager import BidderManager
from report_generator import ReportGenerator
from document_generator import DocumentGenerator
from comparative_statement_generator import ComparativeStatementGenerator
from letter_acceptance_generator import LetterAcceptanceGenerator
from work_order_generator import WorkOrderGenerator
from scrutiny_sheet_generator import ScrutinySheetGenerator
from date_utils import DateUtils
from pdf_generator import PDFGenerator
from latex_generator import LaTeXGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Page configuration with enhanced metadata
st.set_page_config(
    page_title="PWD Electric Division Tender Processing System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/support',
        'Report a bug': 'mailto:support@example.com',
        'About': "PWD Electric Division Tender Processing System v2.0"
    }
)

# Apply enhanced custom styling and theme
set_custom_theme()
apply_custom_css()

def main():
    """
    Enhanced main application function with professional UI and balloon themes.
    Aligned with reference PWD Electric Division Tender Processing System.
    """
    # Initialize session state
    initialize_session_state()
    
    # Create enhanced sidebar
    create_enhanced_sidebar()
    
    # Main content area
    st.title("PWD Electric Division Tender Processing System")
    
    # Show welcome message on first run
    if 'initialized' not in st.session_state:
        st.balloons()
        st.session_state.initialized = True
        
    # Main application logic
    if st.session_state.current_work:
        display_enhanced_work_info(st.session_state.current_work)
        
        # Handle different sections based on current view
        if st.session_state.current_view == "bidder_management":
            handle_enhanced_bidder_management()
        elif st.session_state.current_view == "report_generation":
            handle_enhanced_report_generation()
        elif st.session_state.current_view == "document_generation":
            handle_enhanced_document_generation()
    else:
        # Show NIT upload interface if no work is loaded
        handle_enhanced_nit_upload()


def initialize_session_state():
    """Initialize enhanced session state with progress tracking."""
    if 'current_work' not in st.session_state:
        st.session_state.current_work = None
    if 'bidders' not in st.session_state:
        st.session_state.bidders = []
    if 'ui_migration_complete' not in st.session_state:
        st.session_state.ui_migration_complete = True

    # Enhanced sidebar navigation with professional styling
    st.sidebar.markdown("### 🎯 Enhanced Navigation")
    st.sidebar.markdown("---")

    # Feature showcase in sidebar
    st.sidebar.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    ">
        <h4 style="margin: 0; color: #2c3e50;">✨ Enhanced Features</h4>
        <ul style="margin: 10px 0; padding-left: 20px; color: #6c757d;">
            <li>Professional UI Design</li>
            <li>Balloon Theme Integration</li>
            <li>Enhanced Branding</li>
            <li>Responsive Layout</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    operation = st.sidebar.radio(
        "Select Operation:",
        [
            "📄 Upload NIT Document",
            "👥 Manage Bidders", 
            "📊 Generate Reports",
            "📝 Generate Documents",
            "🎨 UI Showcase"
        ],
        help="Choose your operation from the enhanced menu"
    )

    # Main content area with enhanced routing
    if operation == "📄 Upload NIT Document":
        handle_nit_upload()
    elif operation == "👥 Manage Bidders":
        handle_bidder_management()
    elif operation == "📊 Generate Reports":
        handle_report_generation()
    elif operation == "📝 Generate Documents":
        handle_document_generation()
    elif operation == "🎨 UI Showcase":
        handle_ui_showcase()

    # Enhanced footer with professional branding
    create_footer()

def handle_nit_upload():
    """Enhanced NIT document upload with professional UI."""
    st.header("📄 Enhanced NIT Document Upload")

    # Feature grid showcase
    create_feature_grid()

    create_info_card(
        "Professional NIT Document Processing",
        "Upload your Notice Inviting Tender (NIT) Excel file with our enhanced processing engine. "
        "The system features improved date parsing, validation, and professional UI feedback. "
        "Experience the new balloon theme celebrations upon successful uploads!",
        "📄"
    )

    # Enhanced file uploader section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose NIT Excel file",
            type=['xlsx', 'xls'],
            help="Upload the official NIT Excel document for enhanced processing"
        )

    with col2:
        create_metric_card(
            "Upload Status",
            "Ready" if not uploaded_file else "Processing",
            "Enhanced file processing engine active",
            "📤"
        )

    if uploaded_file is not None:
        # Progress indicator
        progress_container = st.container()
        
        with progress_container:
            create_progress_card("Processing NIT Document", 25, "Initializing enhanced parser...")
            
        try:
            # Simulate enhanced processing with progress updates
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Update progress
            progress_container.empty()
            with progress_container:
                create_progress_card("Processing NIT Document", 50, "Parsing Excel data...")

            # Initialize ExcelParser and parse the uploaded file
            parser = ExcelParser()
            work_data = parser.parse_nit_excel(tmp_file_path)

            # Clean up temporary file
            os.unlink(tmp_file_path)

            # Update progress
            progress_container.empty() 
            with progress_container:
                create_progress_card("Processing NIT Document", 100, "Processing complete!")

            if work_data:
                # Store the work data in session state
                st.session_state.current_work = {
                    'work_info': {
                        'work_name': work_data.get('work_name', 'Unknown Work'),
                        'estimated_cost': work_data.get('estimated_cost', 0),
                        'earnest_money': work_data.get('earnest_money', 0),
                        'time_of_completion': work_data.get('time_completion', 'Not specified'),
                        'nit_number': work_data.get('nit_number', ''),
                        'nit_date': work_data.get('nit_date', ''),
                        'receipt_date': work_data.get('receipt_date', ''),
                        'opening_date': work_data.get('opening_date', '')
                    },
                    'works': work_data.get('works', [])
                }
                
                # Enhanced success feedback with balloon celebration
                show_celebration_message("NIT document processed successfully with enhanced UI!")
                show_balloons()

                # Enhanced information display
                st.markdown("### 📋 Processed Work Information")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    create_metric_card(
                        "Estimated Cost",
                        f"₹{work_data.get('estimated_cost', 0):,.2f}",
                        "Total project value",
                        "💰"
                    )

                with col2:
                    create_metric_card(
                        "Earnest Money",
                        f"₹{work_data.get('earnest_money', 0):,.2f}",
                        "Required deposit",
                        "🏦"
                    )

                with col3:
                    create_metric_card(
                        "Timeline",
                        work_data.get('time_completion', 'Not specified'),
                        "Project duration",
                        "⏱️"
                    )

                # Enhanced work details
                st.markdown("### 📝 Work Details")
                
                details_col1, details_col2 = st.columns(2)
                
                with details_col1:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa, #ffffff);
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid #1f77b4;
                        margin: 10px 0;
                    ">
                        <h4 style="margin: 0 0 15px 0; color: #2c3e50;">🏗️ Project Information</h4>
                        <p><strong>Work Name:</strong> {work_data.get('work_name', 'Not specified')}</p>
                        <p><strong>NIT Number:</strong> {work_data.get('nit_number', 'Not specified')}</p>
                        <p><strong>NIT Date:</strong> {work_data.get('nit_date', 'Not specified')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with details_col2:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa, #ffffff);
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid #28a745;
                        margin: 10px 0;
                    ">
                        <h4 style="margin: 0 0 15px 0; color: #2c3e50;">📅 Timeline Details</h4>
                        <p><strong>Receipt Date:</strong> {work_data.get('receipt_date', 'Not specified')}</p>
                        <p><strong>Opening Date:</strong> {work_data.get('opening_date', 'Not specified')}</p>
                        <p><strong>Time for Completion:</strong> {work_data.get('time_completion', 'Not specified')}</p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                create_status_indicator("error", "Failed to parse NIT document. Please check the file format.")

        except Exception as e:
            create_status_indicator("error", f"Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")
            
            # Clean up temporary file if it exists
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                try:
                    os.unlink(tmp_file_path)
                except Exception as cleanup_error:
                    logging.error(f"Error cleaning up temporary file: {cleanup_error}")
            
            # Show error message to user
            st.error(f"Error processing NIT file: {str(e)}")
            return

    operation = st.sidebar.radio(
        "Select Operation:",
        [
            "📄 Upload NIT Document",
            "👥 Manage Bidders", 
            "📊 Generate Reports",
            "📝 Generate Documents",
            "🎨 UI Showcase"
        ],
        help="Choose your operation from the enhanced menu"
    )

    # Main content area with enhanced routing
    if operation == "📄 Upload NIT Document":
        handle_nit_upload()
    elif operation == "👥 Manage Bidders":
        handle_bidder_management()
    elif operation == "📊 Generate Reports":
        handle_report_generation()
    elif operation == "📝 Generate Documents":
        handle_document_generation()
    elif operation == "🎨 UI Showcase":
        handle_ui_showcase()

    # Enhanced footer with professional branding
    create_footer()

def handle_nit_upload():
    """Enhanced NIT document upload with professional UI."""
    st.header("📄 Enhanced NIT Document Upload")

    # Feature grid showcase
    create_feature_grid()

    create_info_card(
        "Professional NIT Document Processing",
        "Upload your Notice Inviting Tender (NIT) Excel file with our enhanced processing engine. "
        "The system features improved date parsing, validation, and professional UI feedback. "
        "Experience the new balloon theme celebrations upon successful uploads!",
        "📄"
    )

    # Enhanced file uploader section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose NIT Excel file",
            type=['xlsx', 'xls'],
            help="Upload the official NIT Excel document for enhanced processing"
        )

    with col2:
        create_metric_card(
            "Upload Status",
            "Ready" if not uploaded_file else "Processing",
            "Enhanced file processing engine active",
            "📤"
        )

    if uploaded_file is not None:
        # Progress indicator
        progress_container = st.container()
        
        with progress_container:
            create_progress_card("Processing NIT Document", 25, "Initializing enhanced parser...")
            
        try:
            # Simulate enhanced processing with progress updates
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Update progress
            progress_container.empty()
            with progress_container:
                create_progress_card("Processing NIT Document", 50, "Parsing Excel data...")

            # Parse the uploaded Excel file using ExcelParser
            parser = ExcelParser()
            work_data = parser.parse_nit_excel(tmp_file_path)
            
            if not work_data:
                raise ValueError("No valid work data found in the uploaded file")

            # Update progress
            progress_container.empty() 
            with progress_container:
                create_progress_card("Processing NIT Document", 100, "Processing complete!")

            # Clean up temporary file
            os.unlink(tmp_file_path)

            if work_data:
                st.session_state.current_work = work_data
                
                # Enhanced success feedback with balloon celebration
                show_celebration_message("NIT document processed successfully with enhanced UI!")
                show_balloons()

                # Enhanced information display
                st.markdown("### 📋 Processed Work Information")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    create_metric_card(
                        "Estimated Cost",
                        f"₹{work_data['work_info']['estimated_cost']:,.2f}",
                        "Total project value",
                        "💰"
                    )

                with col2:
                    create_metric_card(
                        "Earnest Money",
                        f"₹{work_data['work_info']['earnest_money']:,.2f}",
                        "Required deposit",
                        "🏦"
                    )

                with col3:
                    create_metric_card(
                        "Timeline",
                        work_data['work_info']['time_of_completion'],
                        "Project duration",
                        "⏱️"
                    )

                # Enhanced work details
                st.markdown("### 📝 Work Details")
                
                details_col1, details_col2 = st.columns(2)
                
                with details_col1:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa, #ffffff);
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid #1f77b4;
                        margin: 10px 0;
                    ">
                        <h4 style="margin: 0 0 15px 0; color: #2c3e50;">🏗️ Project Information</h4>
                        <p><strong>Work Name:</strong> {work_data['work_name']}</p>
                        <p><strong>NIT Number:</strong> {work_data['nit_number']}</p>
                        <p><strong>Processing Status:</strong> <span style="color: #28a745;">✅ Enhanced Processing Complete</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                with details_col2:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #f8f9fa, #ffffff);
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid #28a745;
                        margin: 10px 0;
                    ">
                        <h4 style="margin: 0 0 15px 0; color: #2c3e50;">📅 Timeline Details</h4>
                        <p><strong>Date:</strong> {work_data['work_info']['date']}</p>
                        <p><strong>Completion Time:</strong> {work_data['work_info']['time_of_completion']}</p>
                        <p><strong>UI Version:</strong> <span style="color: #1f77b4;">Enhanced 2.0</span></p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                create_status_indicator("error", "Failed to parse NIT document. Please check the file format.")

        except Exception as e:
            create_status_indicator("error", f"Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")
    
    # Create professional footer
    create_footer()
    
    # Show celebration message for first-time users
    if 'first_visit' not in st.session_state:
        show_celebration_message("Welcome to the Enhanced Tender Processing System! 🎉")
        st.session_state.first_visit = False

def show_home():
    """Display the home page with an overview of the application."""
    # Get theme colors and gradients
    theme_colors = get_theme_colors()
    gradients = get_gradient_styles()
    
    # Apply theme to the title section
    st.markdown(
        f"""
        <div style="
            background: {gradients['header_gradient']};
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        ">
            <h1 style="margin: 0; color: white;">Welcome to Tender Management System</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Streamline your tender management process with our professional tools</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # System metrics row
    st.subheader("System Overview")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        create_metric_card(
            "Active Tenders",
            "12",
            "+2 from last month",
            "📋"
        )
    
    with metric_col2:
        create_metric_card(
            "Total Bidders",
            "48",
            "+5 this week",
            "👥"
        )
    
    with metric_col3:
        create_metric_card(
            "Documents Generated",
            "156",
            "+24 today",
            "📄"
        )
    
    with metric_col4:
        create_metric_card(
            "Success Rate",
            "92%",
            "+3% improvement",
            "📈"
        )
    
    # Status indicators
    st.markdown("### System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        create_status_indicator("success", "Document Processing: Operational")
        create_status_indicator("warning", "Storage: 78% used")
    
    with col2:
        create_status_indicator("success", "Database: Connected")
        create_status_indicator("error", "Backup: Overdue")
    
    # Progress cards
    st.markdown("### Current Progress")
    progress_col1, progress_col2 = st.columns(2)
    
    with progress_col1:
        create_progress_card(
            "Tender Processing",
            0.75,
            "3 of 4 steps completed"
        )
    
    with progress_col2:
        create_progress_card(
            "Document Generation",
            0.4,
            "2 of 5 steps completed"
        )
    
    # Feature grid
    st.markdown("### Key Features")
    create_feature_grid()
    
    # Recent activities with enhanced UI
    st.markdown("### Recent Activities")
    with st.expander("View Activity Log", expanded=True):
        st.info("No recent activities to display. Start by uploading an NIT document or managing bidders.")
    
    # Call to action with theme colors
    st.markdown("---")
    st.markdown("### Ready to get started?")
    
    # Create a container with theme gradient
    st.markdown(
        f"""
        <div style="
            background: {gradients['card_gradient']};
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            color: white;
            text-align: center;
        ">
            <h3 style="margin-top: 0; color: white;">Start Your Tender Journey</h3>
            <p>Click below to begin processing your first tender</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Center the button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(
            "🚀 Launch Tender Processing", 
            use_container_width=True,
            type="primary"
        ):
            st.session_state.current_work = "new_tender"
            show_celebration_message("Let's get started with your tender processing!")
            st.balloons()
            st.experimental_rerun()
    
    # Add theme-based footer note
    st.markdown(
        f"<div style='text-align: center; color: {theme_colors['gray']}; margin-top: 20px;'>"
        f"<small>Theme: Professional Blue | v2.0.0</small>"
        f"</div>",
        unsafe_allow_html=True
    )


def handle_nit_upload():
    """Handle NIT document upload and processing."""
    st.header("📄 Upload NIT Document")
    
    create_info_card(
        "NIT Document Upload", 
        "Upload your Notice Inviting Tender (NIT) Excel file to extract work details and estimated costs. "
        "The system supports multiple date formats and will automatically parse the tender information.",
        "📄"
    )
    
    uploaded_file = st.file_uploader(
        "Choose NIT Excel file", 
        type=['xlsx', 'xls'],
        help="Upload the official NIT Excel document"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Parse Excel file
            parser = ExcelParser()
            work_data = parser.parse_nit_excel(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            if work_data:
                # Prepare work_info for consistency
                work_info = {
                    'work_name': work_data.get('work_name', 'Unknown Work'),
                    'nit_number': work_data.get('nit_number', 'Unknown NIT'),
                    'estimated_cost': float(str(work_data.get('estimated_cost', 0)).replace(',', '')),
                    'earnest_money': float(str(work_data.get('earnest_money', 0)).replace(',', '')),
                    'time_completion': work_data.get('time_completion', '6 months'),
                    'nit_date': work_data.get('nit_date', 'Not found'),
                    'receipt_date': work_data.get('receipt_date', 'Not found'),
                    'opening_date': work_data.get('opening_date', 'Not found')
                }
                
                if work_data.get('works') and len(work_data['works']) > 0:
                    first_work = work_data['works'][0]
                    work_info.update({
                        'work_name': first_work.get('name', work_info['work_name']),
                        'item_no': first_work.get('item_no', '1'),
                        'estimated_cost': float(str(first_work.get('estimated_cost', work_info['estimated_cost'])).replace(',', '')),
                        'earnest_money': float(str(first_work.get('earnest_money', work_info['earnest_money'])).replace(',', '')),
                        'time_completion': first_work.get('time_completion', work_info['time_completion'])
                    })
                
                work_data['work_info'] = work_info
                st.session_state.current_work = work_data
                st.success("✅ NIT document uploaded and parsed successfully!")
                
                # Display parsed information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 NIT Information")
                    st.write(f"**Work Package:** {work_data['work_name']}")
                    st.write(f"**NIT Number:** {work_data['nit_number']}")
                    st.write(f"**Total Works:** {work_data.get('total_works', 1)}")
                    st.write(f"**Total Estimated Cost:** ₹{work_info['estimated_cost']:,.2f}")
                    st.write(f"**Total Earnest Money:** ₹{work_info['earnest_money']:,.2f}")
                
                with col2:
                    st.subheader("📅 Timeline Information")
                    st.write(f"**NIT Date:** {work_info.get('nit_date', 'Not found')}")
                    st.write(f"**Receipt Date:** {work_info.get('receipt_date', 'Not found')}")
                    st.write(f"**Opening Date:** {work_info.get('opening_date', 'Not found')}")
                    st.write(f"**Max Completion Time:** {work_info.get('time_completion', 6)} months")
                
                if work_data.get('works') and len(work_data['works']) > 1:
                    st.subheader("📋 Individual Works Details")
                    works_df = pd.DataFrame(work_data['works'])
                    works_df['estimated_cost_display'] = works_df['estimated_cost'].apply(lambda x: f"₹{x:,.0f}")
                    works_df['earnest_money_display'] = works_df['earnest_money'].apply(lambda x: f"₹{x:,.0f}")
                    display_df = works_df[['item_no', 'name', 'estimated_cost_display', 'time_completion', 'earnest_money_display']]
                    display_df.columns = ['Item No.', 'Work Name', 'Estimated Cost', 'Time (Months)', 'Earnest Money']
                    st.dataframe(display_df, use_container_width=True)
                    st.info(f"💡 This NIT contains {len(work_data['works'])} individual works. Go to 'Manage Bidders' to select a specific work for bidding.")
                elif work_data.get('works') and len(work_data['works']) == 1:
                    st.subheader("📋 Work Details")
                    work = work_data['works'][0]
                    st.write(f"**Work Name:** {work['name']}")
                    st.write(f"**Estimated Cost:** ₹{work['estimated_cost']:,.2f}")
                    st.write(f"**Time of Completion:** {work['time_completion']} months")
                    st.write(f"**Earnest Money:** ₹{work['earnest_money']:,.2f}")
                    st.info("💡 Go to 'Manage Bidders' to add bidders for this work.")
                    show_balloons()
                else:
                    st.error("❌ Failed to parse NIT document. Please check the file format.")
            else:
                st.error("❌ Failed to parse NIT document. Please check the file format.")
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")

def handle_bidder_management():
    """Enhanced bidder management with professional UI and functionality."""
    st.header("👥 Enhanced Bidder Management")

    if st.session_state.current_work is None:
        create_status_indicator("warning", "Please upload a NIT document first to enable bidder management.")
        return

    # Enhanced bidder management interface
    create_info_card(
        "Professional Bidder Database",
        "Manage your bidder database with enhanced selection tools, real-time calculations, "
        "and professional data presentation. Experience improved workflow with the new UI.",
        "👥"
    )
    
    # Bidder database with enhanced professional data
    bidder_database = {
        "ABC Construction Ltd.": {
            "address": "123 Business Street, Professional City",
            "last_used": "2024-08-01",
            "contact_person": "Mr. Rajesh Kumar",
            "email": "rajesh.kumar@abcconstruction.com",
            "phone": "+91 98765 43210",
            "registration_number": "U45201MH2010PTC207532",
            "pan_number": "AAECA1234A",
            "gstin": "27AAECA1234A1Z5",
            "average_rating": 4.5,
            "projects_completed": 42,
            "specialization": ["Road Construction", "Bridge Works", "Infrastructure"]
        },
        "XYZ Engineers Pvt. Ltd.": {
            "address": "456 Industrial Area, Corporate Town",
            "last_used": "2024-07-15",
            "contact_person": "Ms. Priya Sharma",
            "email": "priya.sharma@xyzengineers.com",
            "phone": "+91 98765 12340",
            "registration_number": "U74999MH2005PTC157759",
            "pan_number": "AAECB5678B",
            "gstin": "27AAECB5678B1Z6",
            "average_rating": 4.2,
            "projects_completed": 28,
            "specialization": ["Structural Engineering", "Project Management"]
        },
        "Professional Builders Co.": {
            "address": "789 Commercial Complex, Business District",
            "last_used": "2024-08-05",
            "contact_person": "Mr. Amit Patel",
            "email": "amit.patel@probuilders.co.in",
            "phone": "+91 98765 98765",
            "registration_number": "U45400MH2007PTC172345",
            "pan_number": "AAECC9012C",
            "gstin": "27AAECC9012C1Z7",
            "average_rating": 4.7,
            "projects_completed": 65,
            "specialization": ["Commercial Construction", "Interior Design"]
        },
        "InfraTech Solutions": {
            "address": "101 Tech Park, IT Hub",
            "last_used": "2024-07-28",
            "contact_person": "Mr. Sanjay Verma",
            "email": "sanjay.verma@infratech.in",
        },
        "Premier Infrastructure": {
            "address": "2020 Business Park, Downtown",
            "last_used": "2024-08-02"
        },
        "Global Engineering Solutions": {
            "address": "3030 Tech Park, Innovation District",
            "last_used": "2024-07-25"
        },
        "Metro Builders & Developers": {
            "address": "4040 Urban Center, City Plaza",
            "last_used": "2024-07-30"
        },
        "Summit Constructions": {
            "address": "5050 Hilltop Road, Uptown",
            "last_used": "2024-08-03"
        },
        "Pinnacle Infrastructure": {
            "address": "6060 Summit Avenue, Business Hub",
            "last_used": "2024-07-28"
        },
        "Apex Engineering Works": {
            "address": "7070 Industrial Zone, Sector 45",
            "last_used": "2024-08-04"
        }
    }
    
    available_bidders = list(bidder_database.keys())
    
    # Enhanced bidder statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "Available Bidders",
            str(len(available_bidders)),
            "In database",
            "👥"
        )
    
    with col2:
        create_metric_card(
            "Selected Bidders", 
            str(len(st.session_state.bidders)),
            "Currently active",
            "✅"
        )
    
    with col3:
        create_metric_card(
            "Processing Status",
            "Enhanced",
            "UI version 2.0",
            "🚀"
        )
    
    # Enhanced bidder selection interface
    st.markdown("### 🎯 Enhanced Bidder Selection")
    
    num_bidders = st.slider(
        "Select number of participating bidders:",
        min_value=1,
        max_value=10,
        value=min(3, len(available_bidders)),
        help="Choose how many bidders participated in this tender"
    )
    
    # Enhanced bidder input interface
    if num_bidders:
        st.markdown("### 📝 Bidder Details Entry")
        
        bidder_data_list = []
        all_valid = True
        
        # Get bidders that haven't been selected yet
        selected_bidder_names = [b['name'] for b in st.session_state.bidders]
        available_for_selection = [b for b in available_bidders if b not in selected_bidder_names]
        
        for i in range(num_bidders):
            with st.expander(f"🏢 Bidder {i+1} Details", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # If we're editing existing bidders, show them first
                    current_options = []
                    if i < len(st.session_state.bidders):
                        current_bidder = st.session_state.bidders[i]
                        current_options = [current_bidder['name']]
                    
                    selected_bidder = st.selectbox(
                        f"Select Bidder {i+1}:",
                        options=current_options + [""] + [b for b in available_for_selection if b not in current_options],
                        key=f"enhanced_bidder_select_{i}",
                        help="Choose from the enhanced bidder database"
                    )
                    
                    if selected_bidder and selected_bidder in bidder_database:
                        st.info(f"📍 **Address:** {bidder_database[selected_bidder]['address']}")
                        st.success(f"🗓️ **Last Used:** {bidder_database[selected_bidder]['last_used']}")
                
                with col2:
                    # If editing existing bidder, show their current percentage
                    default_percentage = ""
                    if i < len(st.session_state.bidders):
                        default_percentage = f"{st.session_state.bidders[i]['percentage']:+.2f}"
                        
                    percentage_str = st.text_input(
                        f"Percentage (%), e.g. -5.50:",
                        value=default_percentage,
                        key=f"enhanced_percentage_{i}",
                        help="Enter % above (+) or below (-) estimate"
                    )
                    
                    # Enhanced validation and calculation
                    if selected_bidder and percentage_str:
                        try:
                            percentage = float(percentage_str)
                            if -99.99 <= percentage <= 99.99:
                                # Handle different work data structures
                                work_data = st.session_state.get('current_work', {})
                                work_info = work_data.get('work_info', work_data)  # Fallback to work_data if work_info doesn't exist
                                estimated_cost = work_info.get('estimated_cost', 0)  # Default to 0 if not found
                                
                                if estimated_cost == 0:
                                    create_status_indicator("warning", "Warning: Estimated cost not found. Using 0 as default.")
                                    
                                bid_amount = estimated_cost * (1 + percentage / 100)
                                
                                # Enhanced bid amount display
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #d4edda, #c3e6cb);
                                    padding: 15px;
                                    border-radius: 8px;
                                    border-left: 4px solid #28a745;
                                    margin: 10px 0;
                                ">
                                    <h4 style="margin: 0; color: #155724;">💰 Calculated Bid Amount</h4>
                                    <p style="margin: 5px 0; font-size: 1.2rem; font-weight: bold; color: #155724;">
                                        ₹{bid_amount:,.2f}
                                    </p>
                                    <p style="margin: 0; color: #155724; font-size: 0.9rem;">
                                        ({percentage:+.2f}% from estimate)
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                bidder_data = {
                                    'name': selected_bidder,
                                    'address': bidder_database[selected_bidder]['address'],
                                    'percentage': percentage,
                                    'bid_amount': bid_amount,
                                    'earnest_money': st.session_state.current_work['work_info'].get('earnest_money', 0),
                                    'date_added': datetime.now().strftime("%Y-%m-%d")
                                }
                                bidder_data_list.append(bidder_data)
                            else:
                                create_status_indicator("error", "Percentage must be between -99.99% and +99.99%")
                                all_valid = False
                        except ValueError:
                            create_status_indicator("error", "Please enter a valid percentage value")
                            all_valid = False
                    elif selected_bidder or percentage_str:
                        all_valid = False
        
        # Enhanced action buttons
        st.markdown("### 🎯 Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Save All Bidders", type="primary", 
                        disabled=not all_valid or len(bidder_data_list) != num_bidders,
                        help="Save all bidders with their bid amounts"):
                st.session_state.bidders = bidder_data_list
                show_celebration_message(f"Successfully saved {len(bidder_data_list)} bidders!")
                show_balloons()
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All Bidders", type="secondary",
                        help="Clear all bidders and start over"):
                st.session_state.bidders = []
                create_status_indicator("info", "All bidders have been reset")
                st.rerun()
        
        with col3:
            if st.button("📋 Copy Bidder List", type="secondary",
                        help="Copy the current bidder list to clipboard"):
                if st.session_state.bidders:
                    bidder_text = "\n".join([f"{i+1}. {b['name']}: ₹{b['bid_amount']:,.2f} ({b['percentage']:+.2f}%)" 
                                           for i, b in enumerate(st.session_state.bidders)])
                    st.session_state.clipboard = bidder_text
                    create_status_indicator("success", "Bidder list copied to clipboard!")
                else:
                    create_status_indicator("warning", "No bidders to copy")
    
    # Display current bidders in an enhanced table
    if st.session_state.bidders:
        st.markdown("### 📊 Current Bidder Summary")
        
        # Sort bidders by bid amount (ascending)
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        
        # Create enhanced DataFrame with rank, bidder info, and bid details
        df_data = []
        for i, bidder in enumerate(sorted_bidders, 1):
            df_data.append({
                'Rank': i,
                'Bidder Name': bidder['name'],
                'Address': bidder.get('address', 'N/A'),
                'Percentage': f"{bidder['percentage']:+.2f}%",
                'Bid Amount': f"₹{bidder['bid_amount']:,.2f}",
                'Status': '✅ Active' if i == 1 else 'Active',
                '_bid_amount': bidder['bid_amount']  # For sorting
            })
        
        # Create and display the DataFrame
        if df_data:

            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)

            # Enhanced L1 bidder display
            sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x.get('bid_amount', float('inf')))
            if sorted_bidders:
                l1_bidder = sorted_bidders[0]
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #d4edda, #c3e6cb);
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 4px solid #28a745;
                    margin: 20px 0;
                    text-align: center;
                ">
                    <h3 style="margin: 0; color: #155724;">🥇 L1 (Lowest) Bidder</h3>
                    <h4 style="margin: 10px 0; color: #155724;">{l1_bidder.get('name', 'N/A')}</h4>
                    <p style="margin: 5px 0; font-size: 1.2rem; font-weight: bold; color: #155724;">
                        ₹{l1_bidder.get('bid_amount', 0):,.2f} ({l1_bidder.get('percentage', 0):+.2f}%)
                    </p>
                    <p style="margin: 0; color: #155724;">Enhanced calculation with professional accuracy</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear all bidders option
                if st.button("🗑️ Clear All Bidders", type="secondary"):
                    st.session_state.bidders = []
                    st.success("✅ Cleared all bidders")
                    st.rerun()
            st.rerun()

def handle_report_generation():
    """Handle report generation with simultaneous generation and download."""
    """Handle report generation with LaTeX-based PDF generation."""
    st.header("📊 Generate Reports")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
        return
    
    # Bulk Generation Section
    work_data = st.session_state.current_work
    work_info = {
        'work_name': work_data.get('work_name', 'Unknown Work'),
        'nit_number': work_data.get('nit_number', 'Unknown NIT'),
        'estimated_cost': float(str(work_data.get('estimated_cost', 0)).replace(',', '')),
        'earnest_money': float(str(work_data.get('earnest_money', 0)).replace(',', '')),
        'time_completion': work_data.get('time_completion', '6 months'),
        'nit_date': work_data.get('nit_date', 'Not found'),
        'receipt_date': work_data.get('receipt_date', 'Not found'),
        'opening_date': work_data.get('opening_date', 'Not found')
    }
    if work_data.get('works') and len(work_data['works']) > 0:
        first_work = work_data['works'][0]
        work_info.update({
            'work_name': first_work.get('name', work_info['work_name']),
            'item_no': first_work.get('item_no', '1'),
            'estimated_cost': float(str(first_work.get('estimated_cost', work_info['estimated_cost'])).replace(',', '')),
            'earnest_money': float(str(first_work.get('earnest_money', work_info['earnest_money'])).replace(',', '')),
            'time_completion': first_work.get('time_completion', work_info['time_completion'])
        })
    st.session_state.current_work['work_info'] = work_info
    formatted_work_data = {
        **work_data,
        'work_info': work_info
    }
    logging.info(f"Formatted work data in handle_report_generation: {formatted_work_data}")

    st.subheader("🚀 Generate All Reports Simultaneously")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📦 Generate All Reports", type="primary", help="Generate all reports at once"):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Initialize generators
                pdf_gen = PDFGenerator()
                doc_gen = DocumentGenerator()
                
                generated_files = {}
                
                # Generate Comparative Statement (PDF)
                status_text.text("Generating Comparative Statement PDF...")
                progress_bar.progress(20)
                comp_pdf = pdf_gen.generate_comparative_statement_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['comparative_statement_pdf'] = {
                    'content': comp_pdf,
                    'filename': f"comparative_statement_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Comparative Statement (DOC)
                status_text.text("Generating Comparative Statement DOC...")
                progress_bar.progress(40)
                comp_doc = doc_gen.generate_comparative_statement_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['comparative_statement_doc'] = {
                    'content': comp_doc,
                    'filename': f"comparative_statement_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                # Generate Scrutiny Sheet (PDF)
                status_text.text("Generating Scrutiny Sheet PDF...")
                progress_bar.progress(60)
                scrutiny_pdf = pdf_gen.generate_scrutiny_sheet_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['scrutiny_sheet_pdf'] = {
                    'content': scrutiny_pdf,
                    'filename': f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Scrutiny Sheet (DOC)
                status_text.text("Generating Scrutiny Sheet DOC...")
                progress_bar.progress(80)
                scrutiny_doc = doc_gen.generate_scrutiny_sheet_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_files['scrutiny_sheet_doc'] = {
                    'content': scrutiny_doc,
                    'filename': f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                progress_bar.progress(100)
                status_text.text("All reports generated successfully!")
                
                st.success("✅ All reports generated simultaneously in PDF and DOC formats!")
                
                # Store in session state for download
                st.session_state.generated_reports = generated_files
                
                # Display download section
                st.subheader("📥 Download Generated Reports")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Comparative Statement**")
                    st.download_button(
                        label="📋 Download PDF",
                        data=generated_files['comparative_statement_pdf']['content'],
                        file_name=generated_files['comparative_statement_pdf']['filename'],
                        mime="application/pdf",
                        key="download_comp_pdf"
                    )
                    st.download_button(
                        label="📋 Download DOC",
                        data=generated_files['comparative_statement_doc']['content'],
                        file_name=generated_files['comparative_statement_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_comp_doc"
                    )
                
                with col_b:
                    st.markdown("**Scrutiny Sheet**")
                    st.download_button(
                        label="🔍 Download PDF",
                        data=generated_files['scrutiny_sheet_pdf']['content'],
                        file_name=generated_files['scrutiny_sheet_pdf']['filename'],
                        mime="application/pdf",
                        key="download_scrutiny_pdf"
                    )
                    st.download_button(
                        label="🔍 Download DOC",
                        data=generated_files['scrutiny_sheet_doc']['content'],
                        file_name=generated_files['scrutiny_sheet_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_scrutiny_doc"
                    )
                
            except Exception as e:
                st.error(f"❌ Error in bulk report generation: {str(e)}")
                logging.error(f"Error in bulk report generation: {e}")
    
    with col2:
        if st.button("📄 Generate All Documents", type="primary", help="Generate all official documents at once"):
            try:
                progress_bar2 = st.progress(0)
                status_text2 = st.empty()
                
                # Initialize generators
                pdf_gen = PDFGenerator()
                doc_gen = DocumentGenerator()
                
                generated_docs = {}
                
                # Generate Letter of Acceptance (PDF)
                status_text2.text("Generating Letter of Acceptance PDF...")
                progress_bar2.progress(25)
                loa_pdf = pdf_gen.generate_letter_of_acceptance_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['letter_of_acceptance_pdf'] = {
                    'content': loa_pdf,
                    'filename': f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Letter of Acceptance (DOC)
                status_text2.text("Generating Letter of Acceptance DOC...")
                progress_bar2.progress(50)
                loa_doc = doc_gen.generate_letter_of_acceptance_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['letter_of_acceptance_doc'] = {
                    'content': loa_doc,
                    'filename': f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                # Generate Work Order (PDF)
                status_text2.text("Generating Work Order PDF...")
                progress_bar2.progress(75)
                wo_pdf = pdf_gen.generate_work_order_pdf(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['work_order_pdf'] = {
                    'content': wo_pdf,
                    'filename': f"work_order_{st.session_state.current_work['nit_number']}.pdf",
                    'mime': "application/pdf"
                }
                
                # Generate Work Order (DOC)
                status_text2.text("Generating Work Order DOC...")
                progress_bar2.progress(100)
                wo_doc = doc_gen.generate_work_order_doc(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                generated_docs['work_order_doc'] = {
                    'content': wo_doc,
                    'filename': f"work_order_{st.session_state.current_work['nit_number']}.docx",
                    'mime': "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                status_text2.text("All documents generated successfully!")
                
                st.success("✅ All documents generated simultaneously in PDF and DOC formats!")
                
                # Store in session state
                st.session_state.generated_documents = generated_docs
                
                # Display download section
                st.subheader("📥 Download Generated Documents")
                
                col_x, col_y = st.columns(2)
                
                with col_x:
                    st.markdown("**Letter of Acceptance**")
                    st.download_button(
                        label="📄 Download PDF",
                        data=generated_docs['letter_of_acceptance_pdf']['content'],
                        file_name=generated_docs['letter_of_acceptance_pdf']['filename'],
                        mime="application/pdf",
                        key="download_loa_pdf"
                    )
                    st.download_button(
                        label="📄 Download DOC",
                        data=generated_docs['letter_of_acceptance_doc']['content'],
                        file_name=generated_docs['letter_of_acceptance_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_loa_doc"
                    )
                
                with col_y:
                    st.markdown("**Work Order**")
                    st.download_button(
                        label="📋 Download PDF",
                        data=generated_docs['work_order_pdf']['content'],
                        file_name=generated_docs['work_order_pdf']['filename'],
                        mime="application/pdf",
                        key="download_wo_pdf"
                    )
                    st.download_button(
                        label="📋 Download DOC",
                        data=generated_docs['work_order_doc']['content'],
                        file_name=generated_docs['work_order_doc']['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_wo_doc"
                    )
                
            except Exception as e:
                st.error(f"❌ Error in bulk document generation: {str(e)}")
                logging.error(f"Error in bulk document generation: {e}")
    
    # Divider
    st.markdown("---")
    
    # Individual Generation Section (keep for specific needs)
    st.subheader("🎯 Generate Individual Reports")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("📋 Generate Comparative Statement", type="secondary"):
            try:
                comp_gen = ComparativeStatementGenerator()
                html_content = comp_gen.generate_comparative_statement(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Comparative statement generated!")
                
                st.download_button(
                    label="📥 Download Comparative Statement",
                    data=html_content,
                    file_name=f"comparative_statement_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="single_comp"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating comparative statement: {str(e)}")
                logging.error(f"Error generating comparative statement: {e}")
    
    with col4:
        if st.button("📊 Generate Detailed Report", type="secondary"):
            try:
                report_generator = ReportGenerator()
                html_content = report_generator.generate_detailed_report(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Detailed report generated!")
                
                st.download_button(
                    label="📥 Download Detailed Report",
                    data=html_content,
                    file_name=f"detailed_report_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="single_detailed"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating detailed report: {str(e)}")
                logging.error(f"Error generating detailed report: {e}")

def handle_document_generation():
    """Enhanced document generation with integrated LaTeX templates."""
    st.header("📝 Enhanced Document Generation with LaTeX Templates")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        create_status_indicator("warning", "Please upload NIT document and add bidders first to enable document generation.")
        return
    
    # Initialize LaTeX generator
    if 'latex_generator' not in st.session_state:
        st.session_state.latex_generator = LaTeXGenerator()
    
    create_info_card(
        "Professional LaTeX Document Suite",
        "Generate official tender documents using integrated LaTeX templates with professional formatting, "
        "automated data substitution, and PDF compilation. Experience government-standard document quality.",
        "📝"
    )
    
    # Enhanced document generation interface
    st.markdown("### 🎯 Generate Official Documents")
    
    # Document type selection with descriptions
    doc_types = {
        "📋 Comparative Statement": {
            "template": "comparative_statement",
            "description": "Professional bidder comparison with landscape format and tabular layout",
            "features": ["Bidder ranking table", "Cost analysis", "Professional formatting"]
        },
        "📜 Letter of Acceptance": {
            "template": "letter_of_acceptance", 
            "description": "Official acceptance letter with government letterhead format",
            "features": ["Official letterhead", "Legal formatting", "Automated data insertion"]
        },
        "🔍 Scrutiny Sheet": {
            "template": "scrutiny_sheet",
            "description": "Detailed tender scrutiny documentation with structured format",
            "features": ["Compliance checklist", "Financial details", "Professional layout"]
        },
        "📋 Work Order": {
            "template": "work_order",
            "description": "Comprehensive work commencement order with timeline details",
            "features": ["Timeline management", "Legal compliance", "Official signatures"]
        }
    }
    
    # Document selection interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_docs = st.multiselect(
            "Select documents to generate:",
            options=list(doc_types.keys()),
            default=list(doc_types.keys()),
            help="Choose which LaTeX documents to generate"
        )
    
    with col2:
        output_format = st.radio(
            "Output Format:",
            ["Both LaTeX & PDF", "LaTeX Only", "PDF Only"],
            help="Choose output format preference"
        )
    
    # Generation buttons
    st.markdown("### 🚀 Document Generation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Generate Selected Documents", type="primary", disabled=not selected_docs):
            progress_container = st.container()
            results_container = st.container()
            
            with progress_container:
                create_progress_card("LaTeX Document Generation", 0, "Initializing LaTeX generator...")
            
            try:
                generated_results = {}
                total_docs = len(selected_docs)
                
                for i, doc_display in enumerate(selected_docs):
                    doc_template = doc_types[doc_display]["template"]
                    progress = ((i + 1) / total_docs) * 100
                    
                    progress_container.empty()
                    with progress_container:
                        create_progress_card("LaTeX Document Generation", progress, f"Generating {doc_display}...")
                    
                    try:
                        # Generate LaTeX document with proper work data structure
                        work_data = {
                            'work_info': st.session_state.current_work.get('work_info', {}),
                            'bidders': st.session_state.bidders
                        }
                        
                        # Ensure work_info has required fields with defaults
                        work_info = work_data['work_info']
                        work_info.setdefault('item_no', '1')
                        work_info.setdefault('work_name', 'Unnamed Work')
                        work_info.setdefault('estimated_cost', 0)
                        work_info.setdefault('earnest_money', 0)
                        work_info.setdefault('date', datetime.now().strftime('%d-%m-%Y'))
                        work_info.setdefault('time_of_completion', '90 days')
                        
                        tex_path, tex_content = st.session_state.latex_generator.generate_document(
                            doc_template,
                            work_data,
                            st.session_state.bidders
                        )
                        
                        pdf_path = None
                        if output_format in ["Both LaTeX & PDF", "PDF Only"]:
                            pdf_path = st.session_state.latex_generator.compile_to_pdf(tex_path)
                        
                        generated_results[doc_display] = {
                            'template': doc_template,
                            'tex_path': tex_path,
                            'pdf_path': pdf_path,
                            'tex_content': tex_content,
                            'status': 'success'
                        }
                        
                    except Exception as e:
                        generated_results[doc_display] = {
                            'template': doc_template,
                            'status': 'error',
                            'error': str(e)
                        }
                
                progress_container.empty()
                with progress_container:
                    create_progress_card("LaTeX Document Generation", 100, "All documents generated successfully!")
                
                # Store results in session state for download
                st.session_state.generated_documents = generated_results
                
                show_celebration_message(f"Successfully generated {len(generated_results)} professional LaTeX documents!")
                show_balloons()
                
                # Display generation results
                with results_container:
                    st.markdown("### 📥 Generated Documents")
                    
                    success_count = sum(1 for result in generated_results.values() if result['status'] == 'success')
                    error_count = len(generated_results) - success_count
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    
                    with col_stat1:
                        create_metric_card("Generated", str(success_count), "Documents created", "✅")
                    
                    with col_stat2:
                        create_metric_card("Errors", str(error_count), "Generation issues", "❌")
                    
                    with col_stat3:
                        create_metric_card("Format", output_format, "Output type", "📄")
                    
                    # Document download interface
                    for doc_name, result in generated_results.items():
                        if result['status'] == 'success':
                            with st.expander(f"📄 {doc_name} - Ready for Download"):
                                col_dl1, col_dl2 = st.columns(2)
                                
                                with col_dl1:
                                    if result.get('tex_path') and output_format in ["Both LaTeX & PDF", "LaTeX Only"]:
                                        try:
                                            with open(result['tex_path'], 'r', encoding='utf-8') as f:
                                                tex_content = f.read()
                                            
                                            st.download_button(
                                                label="📄 Download LaTeX",
                                                data=tex_content,
                                                file_name=f"{result['template']}.tex",
                                                mime="text/plain",
                                                help="Download LaTeX source file"
                                            )
                                        except Exception as e:
                                            st.error(f"Error reading LaTeX file: {e}")
                                
                                with col_dl2:
                                    if result.get('pdf_path') and output_format in ["Both LaTeX & PDF", "PDF Only"]:
                                        try:
                                            with open(result['pdf_path'], 'rb') as f:
                                                pdf_content = f.read()
                                            
                                            st.download_button(
                                                label="📊 Download PDF",
                                                data=pdf_content,
                                                file_name=f"{result['template']}.pdf",
                                                mime="application/pdf",
                                                help="Download compiled PDF document"
                                            )
                                        except Exception as e:
                                            st.error(f"Error reading PDF file: {e}")
                                
                                # Preview LaTeX content
                                if st.checkbox(f"Preview LaTeX Source - {doc_name}", key=f"preview_{result['template']}"):
                                    st.code(result.get('tex_content', 'Content not available'), language='latex')
                        else:
                            create_status_indicator("error", f"Failed to generate {doc_name}: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                progress_container.empty()
                create_status_indicator("error", f"Document generation failed: {str(e)}")
                logging.error(f"Document generation error: {e}")
    
    with col2:
        if st.button("📋 Preview Templates", type="secondary"):
            st.markdown("### 📖 LaTeX Template Preview")
            
            template_files = [
                "comparative_statement.tex",
                "letter_of_acceptance.tex", 
                "scrutiny_sheet.tex",
                "work_order.tex"
            ]
            
            selected_template = st.selectbox(
                "Select template to preview:",
                template_files,
                help="Choose a LaTeX template to preview"
            )
            
            try:
                template_path = f"latex_templates/{selected_template}"
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                st.code(template_content, language='latex')
            except Exception as e:
                create_status_indicator("error", f"Error loading template: {e}")
    
    with col3:
        if st.button("🧹 Cleanup Old Files", type="secondary"):
            try:
                st.session_state.latex_generator.cleanup_old_files(days_old=7)
                create_status_indicator("success", "Old files cleaned up successfully!")
            except Exception as e:
                create_status_indicator("error", f"Cleanup failed: {e}")
    
    # Enhanced template information section
    st.markdown("### 📚 LaTeX Template Integration")
    
    integration_info = {
        "Professional Formatting": "LaTeX templates ensure government-standard document formatting with precise layouts",
        "Automated Data Binding": "Dynamic placeholder substitution with work and bidder information",
        "PDF Compilation": "Automatic PDF generation using pdflatex for professional output",
        "Template Customization": "Easily customizable templates for different government departments"
    }
    
    # Display features in a grid
    cols = st.columns(2)
    for i, (feature, description) in enumerate(integration_info.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"**{feature}**  \
                {description}", unsafe_allow_html=True)
                st.markdown("---")
    
    # Template customization section
    with st.expander("🎨 Customize Templates"):
        st.info("Advanced users can customize LaTeX templates in the 'latex_templates' directory.")
        st.code("""# Example template structure
\documentclass{article}
\title{<<work_name>>}
\begin{document}
    \section{<<work_name>>}
    \begin{itemize}
        \item NIT Number: <<nit_number>>
        \item Estimated Cost: <<estimated_cost>>
    \end{itemize}
\end{document}""", language='latex')
    
    # System requirements section
    with st.expander("⚙️ System Requirements"):
        st.markdown("""
        To generate PDF documents, ensure you have the following installed:
        - A LaTeX distribution (e.g., TeX Live, MiKTeX, or MacTeX)
        - `pdflatex` command available in system PATH
        - Required LaTeX packages (will be installed automatically)
        
        **Note:** For Windows, make sure LaTeX binaries are in your system PATH.
        """)
    st.header("📝 Generate Individual Documents")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
        return
    
    st.info("💡 Tip: Use 'Generate Reports' section for bulk generation of all documents simultaneously!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate Letter of Acceptance", type="secondary"):
            try:
                loa_gen = LetterAcceptanceGenerator()
                html_content = loa_gen.generate_letter_of_acceptance(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Letter of Acceptance generated!")
                
                st.download_button(
                    label="📥 Download Letter of Acceptance",
                    data=html_content,
                    file_name=f"letter_of_acceptance_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_loa"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating Letter of Acceptance: {str(e)}")
                logging.error(f"Error generating LOA: {e}")
    
    with col2:
        if st.button("📋 Generate Work Order", type="secondary"):
            try:
                wo_gen = WorkOrderGenerator()
                html_content = wo_gen.generate_work_order(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Work Order generated!")
                
                st.download_button(
                    label="📥 Download Work Order",
                    data=html_content,
                    file_name=f"work_order_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_wo"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating Work Order: {str(e)}")
                logging.error(f"Error generating work order: {e}")
    
    with col3:
        if st.button("🔍 Generate Scrutiny Sheet", type="secondary"):
            try:
                ss_gen = ScrutinySheetGenerator()
                html_content = ss_gen.generate_scrutiny_sheet(
                    st.session_state.current_work,
                    st.session_state.bidders
                )
                
                st.success("✅ Scrutiny Sheet generated!")
                
                st.download_button(
                    label="📥 Download Scrutiny Sheet",
                    data=html_content,
                    file_name=f"scrutiny_sheet_{st.session_state.current_work['nit_number']}.html",
                    mime="text/html",
                    key="individual_scrutiny"
                )
                
                st.markdown("---")
                st.subheader("📦 Generate All Documents")
                
                if st.button("📦 Generate All PDFs (LaTeX)", type="primary"):
                    try:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        latex_gen = LatexPDFGenerator()
                        valid_bidders = [b for b in st.session_state.bidders 
                                      if b.get('bid_amount') is not None 
                                      and str(b.get('bid_amount', '')).replace(',', '').replace('.', '').isdigit()]
                        if not valid_bidders:
                            st.error("❌ No valid bidders with proper bid amounts found.")
                            return
                            
                        # Ensure formatted_work_data is available
                        if 'formatted_work_data' not in locals():
                            formatted_work_data = st.session_state.current_work
                            
                        generated_pdfs = latex_gen.generate_bulk_pdfs(formatted_work_data, valid_bidders)
                        progress_bar.progress(100)
                        status_text.text("All PDFs generated successfully!")
                        
                        if generated_pdfs:
                            st.success(f"✅ Generated {len(generated_pdfs)} PDF documents!")
                            st.session_state.generated_pdfs = generated_pdfs
                            st.subheader("📥 Download Generated PDFs")
                            for doc_type, pdf_data in generated_pdfs.items():
                                doc_name = doc_type.replace('_', ' ').title()
                                st.download_button(
                                    label=f"📥 Download {doc_name} PDF",
                                    data=pdf_data,
                                    file_name=f"{doc_type}_{st.session_state.current_work['nit_number']}.pdf",
                                    mime="application/pdf",
                                    key=f"pdf_{doc_type}_{st.session_state.current_work['nit_number']}"
                                )
                        else:
                            st.error("❌ Failed to generate any PDF documents. Check app.log for details.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating PDFs: {str(e)}")
                        logging.error(f"Error generating PDFs: {e}", exc_info=True)

                # ZIP download button
                if st.button("🚀 Download All as ZIP", type="primary"):
                    try:
                        with st.spinner("Creating ZIP package..."):
                            zip_gen = ZipGenerator()
                            if st.session_state.get('generated_pdfs'):
                                documents = st.session_state.generated_pdfs
                            else:
                                # Generate PDFs if not already generated
                                formatted_work_data = st.session_state.current_work
                                valid_bidders = [b for b in st.session_state.bidders 
                                              if b.get('bid_amount') is not None 
                                              and str(b.get('bid_amount', '')).replace(',', '').replace('.', '').isdigit()]
                                documents = latex_gen.generate_bulk_pdfs(formatted_work_data, valid_bidders)
                            
                            if documents:
                                zip_data = zip_gen.create_tender_documents_zip(
                                    st.session_state.current_work['work_name'],
                                    st.session_state.current_work['nit_number'],
                                    documents
                                )
                                if zip_data:
                                    nit_number = st.session_state.current_work['nit_number'].replace('/', '_')
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    st.download_button(
                                        label="📦 Download Complete Package (ZIP)",
                                        data=zip_data,
                                        file_name=f"Tender_Documents_{nit_number}_{timestamp}.zip",
                                        mime="application/zip",
                                        type="primary"
                                    )
                                    st.success(f"✅ ZIP package created with {len(documents)} documents!")
                                    show_balloons()
                                else:
                                    st.error("❌ Failed to create ZIP package.")
                            else:
                                st.error("❌ No documents available to package.")
                    except Exception as e:
                        st.error(f"❌ Error creating ZIP package: {str(e)}")
                        logging.error(f"Error creating ZIP: {e}")

            except Exception as e:
                st.error(f"❌ Error generating Scrutiny Sheet: {str(e)}")
                logging.error(f"Error generating scrutiny sheet: {e}")

def handle_document_generation_latex():
    """Enhanced document generation with integrated LaTeX templates."""
    st.header("📝 Enhanced Document Generation with LaTeX Templates")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        create_status_indicator("warning", "Please upload NIT document and add bidders first to enable document generation.")
        return
    
    # Initialize LaTeX generator and required variables
    if 'latex_generator' not in st.session_state:
        st.session_state.latex_generator = LatexPDFGenerator()
    
    # Get work data and bidders
    work_data = st.session_state.current_work
    work_id = work_data.get('work_info', {}).get('item_no', '1')
    valid_bidders = st.session_state.get('bidders', [])
    
    # Initialize LaTeX generator if not already done
    if 'latex_gen' not in st.session_state:
        st.session_state.latex_gen = LatexPDFGenerator()
    
    create_info_card(
        "Professional LaTeX Document Suite",
        "Generate official tender documents using integrated LaTeX templates with professional formatting, "
        "automated data substitution, and PDF compilation. Experience government-standard document quality.",
        "📝"
    )
    
    # Enhanced document generation interface
    st.markdown("### 🎯 Generate Official Documents")
    
    # Document type selection with descriptions
    doc_types = {
        "📋 Comparative Statement": {
            "template": "comparative_statement",
            "description": "Professional bidder comparison with landscape format and tabular layout",
            "features": ["Bidder ranking table", "Cost analysis", "Professional formatting"]
        },
        "📜 Letter of Acceptance": {
            "template": "letter_of_acceptance", 
            "description": "Official acceptance letter with government letterhead format",
            "features": ["Official letterhead", "Legal formatting", "Automated data insertion"]
        },
        "🔍 Scrutiny Sheet": {
            "template": "scrutiny_sheet",
            "description": "Detailed tender scrutiny documentation with structured format",
            "features": ["Compliance checklist", "Financial details", "Professional layout"]
        },
        "📋 Work Order": {
            "template": "work_order",
            "description": "Comprehensive work commencement order with timeline details",
            "features": ["Timeline management", "Legal compliance", "Official signatures"]
        }
    }
    
    # Document selection interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_docs = st.multiselect(
            "Select documents to generate:",
            options=list(doc_types.keys()),
            default=list(doc_types.keys()),
            help="Choose which LaTeX documents to generate"
        )
    
    with col2:
        output_format = st.radio(
            "Output Format:",
            ["Both LaTeX & PDF", "LaTeX Only", "PDF Only"],
            help="Choose output format preference"
        )
    
    # Generation buttons
    st.markdown("### 🚀 Document Generation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Generate Selected Documents", type="primary", disabled=not selected_docs):
            progress_container = st.container()
            results_container = st.container()
            
            with progress_container:
                create_progress_card("LaTeX Document Generation", 0, "Initializing LaTeX generator...")
            
            try:
                generated_results = {}
                total_docs = len(selected_docs)
                
                for i, doc_display in enumerate(selected_docs):
                    doc_template = doc_types[doc_display]["template"]
                    progress = ((i + 1) / total_docs) * 100
                    
                    progress_container.empty()
                    with progress_container:
                        create_progress_card("LaTeX Document Generation", progress, f"Generating {doc_display}...")
                    
                    try:
                        # Generate document using the appropriate method based on template
                        if doc_template == "comparative_statement":
                            # Use the existing method for comparative statement
                            pdf_bytes = st.session_state.latex_gen.generate_comparative_statement_pdf(
                                st.session_state.current_work,
                                st.session_state.bidders
                            )
                            # Save to a temporary file for download
                            import tempfile
                            import os
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                                tmp_file.write(pdf_bytes)
                                pdf_path = tmp_file.name
                            
                            generated_results[doc_display] = {
                                'template': doc_template,
                                'pdf_path': pdf_path,
                                'status': 'success'
                            }
                        else:
                            # For other document types, use the template-based generation
                            tex_path, tex_content = st.session_state.latex_generator.generate_document(
                                doc_template,
                                st.session_state.current_work,
                                st.session_state.bidders
                            )
                            
                            pdf_path = None
                            if output_format in ["Both LaTeX & PDF", "PDF Only"]:
                                pdf_path = st.session_state.latex_generator.compile_to_pdf(tex_path)
                            
                            generated_results[doc_display] = {
                                'template': doc_template,
                                'tex_path': tex_path,
                                'pdf_path': pdf_path,
                                'tex_content': tex_content,
                                'status': 'success'
                            }
                            
                    except Exception as e:
                        generated_results[doc_display] = {
                            'template': doc_template,
                            'status': 'error',
                            'error': str(e)
                        }
                
                progress_container.empty()
                with progress_container:
                    create_progress_card("LaTeX Document Generation", 100, "All documents generated successfully!")
                
                # Store results in session state for download
                st.session_state.generated_documents = generated_results
                
                show_celebration_message(f"Successfully generated {len([r for r in generated_results.values() if r['status'] == 'success'])} professional documents!")
                show_balloons()
                
                # Display generation results
                with results_container:
                    st.markdown("### 📥 Generated Documents")
                    
                    success_count = sum(1 for result in generated_results.values() if result.get('status') == 'success')
                    error_count = len(generated_results) - success_count
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    
                    with col_stat1:
                        create_metric_card("Generated", str(success_count), "Documents created", "✅")
                    
                    with col_stat2:
                        create_metric_card("Errors", str(error_count), "Generation issues", "❌")
                    
                    with col_stat3:
                        create_metric_card("Format", output_format, "Output type", "📄")
                    
                    # Document download interface
                    for doc_name, result in generated_results.items():
                        if result.get('status') == 'success':
                            with st.expander(f"📄 {doc_name} - Ready for Download"):
                                col_dl1, col_dl2 = st.columns(2)
                                
                                # PDF Download
                                if result.get('pdf_path') and output_format in ["Both LaTeX & PDF", "PDF Only"]:
                                    with col_dl1:  # Fixed typo in column name (was col_dL1)
                                        try:
                                            with open(result['pdf_path'], 'rb') as f:
                                                pdf_content = f.read()
                                            
                                            st.download_button(
                                                label="📊 Download PDF",
                                                data=pdf_content,
                                                file_name=f"{result['template']}.pdf",
                                                mime="application/pdf",
                                                help="Download compiled PDF document"
                                            )
                                        except Exception as e:
                                            st.error(f"Error reading PDF file: {e}")
                                
                                # LaTeX Source Download
                                if result.get('tex_path') and output_format in ["Both LaTeX & PDF", "LaTeX Only"]:
                                    with col_dl2:
                                        try:
                                            with open(result['tex_path'], 'r', encoding='utf-8') as f:
                                                tex_content = f.read()
                                            
                                            st.download_button(
                                                label="📄 Download LaTeX",
                                                data=tex_content,
                                                file_name=f"{result['template']}.tex",
                                                mime="text/plain",
                                                help="Download LaTeX source file"
                                            )
                                        except Exception as e:
                                            st.error(f"Error reading LaTeX file: {e}")
                                
                                # Preview LaTeX content
                                if st.checkbox(f"Preview LaTeX Source - {doc_name}", key=f"preview_{result['template']}"):
                                    st.code(result.get('tex_content', 'Content not available'), language='latex')
                        else:
                            error_msg = f"Failed to generate {doc_name}: {result.get('error', 'Unknown error')}"
                            create_status_indicator("error", error_msg)
                
            except Exception as e:
                progress_container.empty()
                error_msg = f"Document generation failed: {str(e)}"
                create_status_indicator("error", error_msg)
                logging.error(f"Document generation error: {e}")
    
    with col2:
        if st.button("📋 Preview Templates", type="secondary"):
            st.markdown("### 📖 LaTeX Template Preview")
            
            template_files = [
                "comparative_statement.tex",
                "letter_of_acceptance.tex", 
                "scrutiny_sheet.tex",
                "work_order.tex"
            ]
            
            selected_template = st.selectbox(
                "Select template to preview:",
                template_files,
                help="Choose a LaTeX template to preview"
            )
            
            try:
                template_path = os.path.join("latex_templates", selected_template)
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                    st.code(template_content, language='latex')
                else:
                    st.warning(f"Template file not found: {template_path}")
            except Exception as e:
                create_status_indicator("error", f"Error loading template: {e}")
    
    with col3:
        if st.button("🧹 Cleanup Old Files", type="secondary"):
            try:
                # Implement cleanup logic if available in LatexPDFGenerator
                if hasattr(st.session_state.latex_generator, 'cleanup_old_files'):
                    st.session_state.latex_generator.cleanup_old_files(days_old=7)
                create_status_indicator("success", "Temporary files cleaned up successfully!")
            except Exception as e:
                create_status_indicator("error", f"Cleanup failed: {e}")
    
    # Enhanced template information section
    st.markdown("### 📚 LaTeX Template Integration")
    
    integration_info = {
        "Professional Formatting": "LaTeX templates ensure government-standard document formatting with precise layouts",
        "Automated Data Binding": "Dynamic placeholder substitution with work and bidder information",
        "PDF Compilation": "Automatic PDF generation using pdflatex for professional output",
        "Template Customization": "Easily customizable templates for different government departments"
    }
    
    # Create document generation buttons in a separate section
    st.markdown("### 📄 Generate Individual Documents")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"📝 Generate Letter of Acceptance"):
            try:
                pdf_bytes = latex_gen.generate_letter_acceptance_pdf(work_data, l1_bidder)
                st.download_button(
                    label="📥 Download Letter of Acceptance",
                    data=pdf_bytes,
                    file_name=f"Letter_of_Acceptance_Work_{work_id}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating Letter of Acceptance: {str(e)}")
                logging.error(f"Error in Letter of Acceptance generation: {e}")
    
    with col2:
        if st.button(f"📋 Generate Work Order"):
            try:
                pdf_bytes = latex_gen.generate_work_order_pdf(work_data, l1_bidder)
                st.download_button(
                    label="📥 Download Work Order",
                    data=pdf_bytes,
                    file_name=f"Work_Order_Work_{work_id}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating Work Order: {str(e)}")
                logging.error(f"Error in Work Order generation: {e}")
    
    with col3:
        if st.button(f"🔍 Generate Scrutiny Sheet"):
            try:
                pdf_bytes = latex_gen.generate_scrutiny_sheet_pdf(work_data, valid_bidders)
                st.download_button(
                    label="📥 Download Scrutiny Sheet",
                    data=pdf_bytes,
                    file_name=f"Scrutiny_Sheet_Work_{work_id}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating Scrutiny Sheet: {str(e)}")
                logging.error(f"Error in Scrutiny Sheet generation: {e}")
    
    # ZIP generation section
    st.markdown("---")
    st.markdown("### 📦 Generate Complete Package")
    
    if st.button(f"🚀 Generate & Download All Documents as ZIP"):
        try:
            with st.spinner("Generating documents and creating ZIP package..."):
                documents = latex_gen.generate_bulk_pdfs(work_data, valid_bidders)
                if documents:
                    zip_buffer = zip_gen.create_zip(documents)
                    st.download_button(
                        label="📦 Download Complete Package (ZIP)",
                        data=zip_buffer,
                        file_name=f"{work_data['work_info']['nit_number']}_Work_{work_id}_documents.zip",
                        mime="application/zip"
                    )
                    st.success("✅ All documents generated and packaged successfully!")
                else:
                    st.error("❌ Failed to generate documents for the ZIP package.")
        except Exception as e:
            st.error(f"❌ Error generating ZIP package: {str(e)}")
            logging.error(f"Error in ZIP package generation: {e}")


def handle_ui_showcase():
    """Showcase the enhanced UI features and migration results."""
    st.header("🎨 Enhanced UI Showcase")

    create_info_card(
        "UI Migration Complete",
        "This showcase demonstrates the successful migration of enhanced interface components, "
        "balloon theme, and professional branding from the source to destination repository.",
        "🎨"
    )

    # Current Progress
    st.markdown("### 📊 Current Progress")
    
    # Calculate tender processing progress (3/4 steps = 75%)
    tender_progress = 75
    
    # Calculate document generation progress (2/5 steps = 40%)
    doc_progress = 40
    
    # Tender Processing Progress
    st.markdown("#### Tender Processing")
    st.markdown(f"""
    <div style="
        background: #e9ecef;
        border-radius: 10px;
        height: 12px;
        margin: 10px 0;
        overflow: hidden;
    ">
        <div style="
            background: linear-gradient(135deg, #1f77b4, #2c3e50);
            height: 100%;
            width: {tender_progress}%;
            border-radius: 10px;
            transition: width 0.3s ease;
        "></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.9rem; color: #6c757d;">3 of 4 steps completed</span>
        <span style="font-weight: 600; color: #1f77b4;">{tender_progress}%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Document Generation Progress
    st.markdown("#### Document Generation")
    st.markdown(f"""
    <div style="
        background: #e9ecef;
        border-radius: 10px;
        height: 12px;
        margin: 10px 0;
        overflow: hidden;
    ">
        <div style="
            background: linear-gradient(135deg, #1f77b4, #2c3e50);
            height: 100%;
            width: {doc_progress}%;
            border-radius: 10px;
            transition: width 0.3s ease;
        "></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.9rem; color: #6c757d;">2 of 5 steps completed</span>
        <span style="font-weight: 600; color: #1f77b4;">{doc_progress}%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Migration status
    st.markdown("### ✅ Migration Status")
    
    migration_items = [
        {"item": "Enhanced Theme Styling", "status": "✅ Complete", "desc": "Professional CSS with gradients"},
        {"item": "Balloon Theme Integration", "status": "✅ Complete", "desc": "Celebration animations active"},
        {"item": "Professional Branding", "status": "✅ Complete", "desc": "Header and footer enhanced"},
        {"item": "UI Components", "status": "✅ Complete", "desc": "Cards, metrics, and indicators"},
        {"item": "Responsive Design", "status": "✅ Complete", "desc": "Mobile and desktop optimized"}
    ]

    for item in migration_items:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <strong>{item['item']}</strong><br>
                <span style="color: #6c757d; font-size: 0.9rem;">{item['desc']}</span>
            </div>
            <div style="color: #28a745; font-weight: bold;">
                {item['status']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # UI Feature demonstration
    st.markdown("### 🌟 Enhanced Features Demo")
    
    demo_col1, demo_col2 = st.columns(2)
    
    with demo_col1:
        if st.button("🎉 Test Balloon Animation"):
            show_balloons()
            show_celebration_message("Balloon theme integration working perfectly!")

        if st.button("📊 Show Metrics Demo"):
            col1, col2, col3 = st.columns(3)
            with col1:
                create_metric_card("Success Rate", "100%", "Migration complete", "✅")
            with col2:
                create_metric_card("UI Version", "2.0", "Enhanced edition", "🚀")
            with col3:
                create_metric_card("Features", "25+", "Professional components", "⭐")

    with demo_col2:
        if st.button("🎨 Test Status Indicators"):
            create_status_indicator("success", "Migration completed successfully!")
            create_status_indicator("info", "Enhanced UI features are now active")
            create_status_indicator("warning", "Remember to test all functionalities")

        if st.button("📈 Show Progress Demo"):
            create_progress_card("UI Migration Progress", 100, "All components successfully integrated")

    # Feature grid
    st.markdown("### 🏆 Professional Feature Grid")
    create_feature_grid()

def main():
    # Apply custom CSS and initialize
    apply_custom_css()
    initialize_session_state()
    
    # Create sidebar navigation
    st.sidebar.title("Navigation")
    menu = ["🏠 Home", "📤 Upload NIT", "👥 Manage Bidders", "📊 Generate Reports", "📝 Generate Documents", "🎨 UI Showcase"]
    choice = st.sidebar.selectbox("Go to", menu)
    
    # Route to the selected page using function-based components
    if choice == "🏠 Home":
        st.title("Tender Management System")
        show_home()
    elif choice == "📤 Upload NIT":
        st.title("Upload NIT Document")
        handle_nit_upload()
    elif choice == "👥 Manage Bidders" and hasattr(st.session_state, 'works') and st.session_state.works:
        st.title("Manage Bidders")
        work_options = [(work['work_info']['item_no'], work['work_info']['work_name']) for work in st.session_state.works]
        selected_work_id = st.selectbox("Select Work", options=[f"{item_no}: {work_name}" for item_no, work_name in work_options])
        selected_work_id = selected_work_id.split(":")[0]
        st.session_state.current_work = next((work for work in st.session_state.works if work['work_info']['item_no'] == selected_work_id), None)
        handle_bidder_management()
    elif choice == "📊 Generate Reports" and hasattr(st.session_state, 'works') and st.session_state.works:
        st.title("Generate Reports")
        work_options = [(work['work_info']['item_no'], work['work_info']['work_name']) for work in st.session_state.works]
        selected_work_id = st.selectbox("Select Work", options=[f"{item_no}: {work_name}" for item_no, work_name in work_options])
        selected_work_id = selected_work_id.split(":")[0]
        st.session_state.current_work = next((work for work in st.session_state.works if work['work_info']['item_no'] == selected_work_id), None)
        handle_report_generation()
    elif choice == "📝 Generate Documents" and hasattr(st.session_state, 'works') and st.session_state.works:
        st.title("Generate Documents")
        work_options = [(work['work_info']['item_no'], work['work_info']['work_name']) for work in st.session_state.works]
        selected_work_id = st.selectbox("Select Work", options=[f"{item_no}: {work_name}" for item_no, work_name in work_options])
        selected_work_id = selected_work_id.split(":")[0]
        st.session_state.current_work = next((work for work in st.session_state.works if work['work_info']['item_no'] == selected_work_id), None)
        handle_document_generation()
    elif choice == "🎨 UI Showcase":
        st.title("UI Showcase")
        handle_ui_showcase()
    else:
        # Default view if no works are uploaded yet
        st.title("Tender Management System")
        st.info("Please upload an NIT document to get started.")
        handle_nit_upload()

if __name__ == "__main__":
    main()
