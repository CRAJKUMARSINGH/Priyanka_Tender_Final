import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import tempfile
import logging

# Import our custom modules
from theme import apply_custom_css
from ui_components import create_header, create_footer, show_balloons, create_info_card
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Page configuration
st.set_page_config(
    page_title="Tender Processing System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

def main():
    """Main application function."""
    
    # Create header
    create_header()
    
    # Initialize session state
    if 'current_work' not in st.session_state:
        st.session_state.current_work = None
    if 'bidders' not in st.session_state:
        st.session_state.bidders = []
    if 'bidder_manager' not in st.session_state:
        st.session_state.bidder_manager = BidderManager()
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    
    operation = st.sidebar.radio(
        "Select Operation:",
        [
            "📄 Upload NIT Document", 
            "👥 Manage Bidders", 
            "📊 Generate Reports",
            "📝 Generate Documents"
        ]
    )
    
    # Main content area
    if operation == "📄 Upload NIT Document":
        handle_nit_upload()
    elif operation == "👥 Manage Bidders":
        handle_bidder_management()
    elif operation == "📊 Generate Reports":
        handle_report_generation()
    elif operation == "📝 Generate Documents":
        handle_document_generation()
    
    # Create footer
    create_footer()

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
                st.session_state.current_work = work_data
                st.success("✅ NIT document uploaded and parsed successfully!")
                
                # Display parsed information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Work Information")
                    st.write(f"**Work Name:** {work_data['work_name']}")
                    st.write(f"**NIT Number:** {work_data['nit_number']}")
                    st.write(f"**Estimated Cost:** ₹{work_data['work_info']['estimated_cost']:,.2f}")
                    st.write(f"**Earnest Money:** ₹{work_data['work_info']['earnest_money']}")
                
                with col2:
                    st.subheader("📅 Timeline Information")
                    st.write(f"**Date:** {work_data['work_info']['date']}")
                    st.write(f"**Time of Completion:** {work_data['work_info']['time_of_completion']}")
                    
                    # Validate and display parsed date
                    parsed_date = DateUtils.parse_date(work_data['work_info']['date'])
                    if parsed_date:
                        st.write(f"**Parsed Date:** {DateUtils.format_display_date(parsed_date)}")
                    else:
                        st.warning("⚠️ Date format not recognized. Please verify the date in the Excel file.")
                
                show_balloons()
            else:
                st.error("❌ Failed to parse NIT document. Please check the file format.")
                
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")

def handle_bidder_management():
    """Handle bidder management operations with original dropdown selection method."""
    st.header("👥 Manage Bidders")
    
    if st.session_state.current_work is None:
        st.warning("⚠️ Please upload a NIT document first.")
        return
    
    # Load bidder database
    bidder_database = {}
    try:
        with open('bidder_database.json', 'r', encoding='utf-8') as f:
            bidder_database = json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading bidder database: {str(e)}")
        return
    
    # Get list of available bidders
    available_bidders = list(bidder_database.keys())
    st.info(f"📋 Available bidders in database: {len(available_bidders)}")
    
    # Step 1: Select number of bidders
    st.subheader("📊 Step 1: Select Number of Bidders")
    num_bidders = st.number_input(
        "How many bidders participated?", 
        min_value=1, 
        max_value=20, 
        value=3,
        help="Select the number of bidders who submitted tenders"
    )
    
    # Step 2: Create input windows for each bidder
    if num_bidders:
        st.subheader("👥 Step 2: Select Bidders and Enter Percentages")
        
        # Initialize bidder inputs in session state
        if 'bidder_inputs' not in st.session_state:
            st.session_state.bidder_inputs = {}
        
        bidder_data_list = []
        all_valid = True
        
        for i in range(num_bidders):
            st.markdown(f"### Bidder {i+1}")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Dropdown to select bidder from database
                selected_bidder = st.selectbox(
                    f"Select Bidder {i+1}:",
                    options=[""] + available_bidders,
                    key=f"bidder_select_{i}",
                    help="Choose from registered bidders"
                )
                
                # Show bidder address if selected
                if selected_bidder and selected_bidder in bidder_database:
                    st.caption(f"📍 Address: {bidder_database[selected_bidder]['address']}")
            
            with col2:
                # Percentage input
                percentage_str = st.text_input(
                    f"Percentage (%):",
                    placeholder="e.g., -5.50",
                    key=f"percentage_{i}",
                    help="Enter % above (+) or below (-) estimate"
                )
            
            # Validate and calculate bid amount
            if selected_bidder and percentage_str:
                try:
                    percentage = float(percentage_str)
                    if -99.99 <= percentage <= 99.99:
                        processor = TenderProcessor()
                        bid_amount = processor.calculate_bid_amount(
                            st.session_state.current_work['work_info']['estimated_cost'],
                            percentage
                        )
                        
                        # Display calculated bid amount
                        st.success(f"💰 Calculated Bid Amount: ₹{bid_amount:,.2f}")
                        
                        bidder_data = {
                            'name': selected_bidder,
                            'address': bidder_database[selected_bidder]['address'],
                            'percentage': percentage,
                            'bid_amount': bid_amount,
                            'earnest_money': st.session_state.current_work['work_info']['earnest_money'],
                            'date_added': DateUtils().get_current_date()
                        }
                        bidder_data_list.append(bidder_data)
                    else:
                        st.error("❌ Percentage must be between -99.99% and +99.99%")
                        all_valid = False
                except ValueError:
                    st.error("❌ Please enter a valid percentage value")
                    all_valid = False
            elif selected_bidder or percentage_str:
                all_valid = False
            
            st.markdown("---")
        
        # Step 3: Add all bidders
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Add All Bidders", type="primary", disabled=not all_valid or len(bidder_data_list) != num_bidders):
                st.session_state.bidders = bidder_data_list
                
                # Update bidder database with last used dates
                for bidder_data in bidder_data_list:
                    if bidder_data['name'] in bidder_database:
                        bidder_database[bidder_data['name']]['last_used'] = DateUtils().get_current_date()
                
                # Save updated database
                try:
                    with open('bidder_database.json', 'w', encoding='utf-8') as f:
                        json.dump(bidder_database, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    st.warning(f"⚠️ Could not update bidder database: {str(e)}")
                
                st.success(f"✅ Added {len(bidder_data_list)} bidders successfully!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All", type="secondary"):
                st.session_state.bidders = []
                if 'bidder_inputs' in st.session_state:
                    del st.session_state.bidder_inputs
                st.success("✅ Reset all bidder selections")
                st.rerun()
    
    # Display current bidders
    if st.session_state.bidders:
        st.subheader("📊 Current Selected Bidders")
        
        # Create DataFrame for display
        df_data = []
        for i, bidder in enumerate(st.session_state.bidders):
            df_data.append({
                'S.No.': i + 1,
                'Bidder Name': bidder['name'],
                'Address': bidder.get('address', 'N/A'),
                'Percentage (%)': f"{bidder['percentage']:+.2f}%",
                'Bid Amount (₹)': f"₹{bidder['bid_amount']:,.2f}",
                'Earnest Money (₹)': f"₹{bidder['earnest_money']}"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Show L1 bidder
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        st.success(f"🥇 L1 (Lowest) Bidder: {l1_bidder['name']} - ₹{l1_bidder['bid_amount']:,.2f} ({l1_bidder['percentage']:+.2f}%)")
        
        # Clear all bidders option
        if st.button("🗑️ Clear All Bidders", type="secondary"):
            st.session_state.bidders = []
            st.success("✅ Cleared all bidders")
            st.rerun()

if __name__ == "__main__":
    main()
