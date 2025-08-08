import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import tempfile
import logging

# Import our custom modules
from theme import set_custom_theme, apply_custom_css
from ui_components import custom_header, custom_footer, show_balloons, create_info_card, create_header, create_footer
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
from latex_pdf_generator import LatexPDFGenerator
from zip_generator import ZipGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# Set custom theme and page configuration
set_custom_theme()

# Apply additional custom CSS
apply_custom_css()

def initialize_session_state():
    if 'works' not in st.session_state:
        st.session_state.works = []
    if 'current_work' not in st.session_state:
        st.session_state.current_work = None
    if 'valid_bidders' not in st.session_state:
        st.session_state.valid_bidders = {}
    if 'latex_gen' not in st.session_state:
        st.session_state.latex_gen = LatexPDFGenerator()
    if 'zip_gen' not in st.session_state:
        st.session_state.zip_gen = ZipGenerator()
    if 'tender_processor' not in st.session_state:
        st.session_state.tender_processor = TenderProcessor()
    if 'excel_parser' not in st.session_state:
        st.session_state.excel_parser = ExcelParser()
    if 'bidder_manager' not in st.session_state:
        st.session_state.bidder_manager = BidderManager()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Page configuration
st.set_page_config(
    page_title="Tender Processing System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
apply_custom_css()

def main():
    """Main application function that sets up the Streamlit interface and handles navigation."""
    # Apply custom theme and CSS first
    set_custom_theme()
    apply_custom_css()
    
    # Create professional header
    create_header()
    
    # Initialize session state
    initialize_session_state()
    
    # Main app interface with improved layout
    st.title("Tender Management System")
    st.markdown("---")
    
    # Navigation with icons
    menu_options = [
        "🏠 Home", 
        "📤 NIT Upload", 
        "👥 Manage Bidders", 
        "📊 Generate Reports", 
        "📝 Generate Documents"
    ]
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", menu_options)
    
    # Main content area
    st.sidebar.markdown("---")
    st.sidebar.info(
        "ℹ️ Use the navigation menu to move between different sections of the application."
    )
    
    # Route to the appropriate page based on user selection
    if "Home" in choice:
        show_home()
    elif "NIT Upload" in choice:
        handle_nit_upload()
    elif "Manage Bidders" in choice:
        handle_bidder_management()
    elif "Generate Reports" in choice:
        handle_report_generation()
    elif "Generate Documents" in choice:
        handle_document_generation()
    
    # Create professional footer
    create_footer()
    # Uncomment the line below to use the enhanced footer instead
    # create_footer()

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
                st.rerun()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 NIT Information")
                    st.write(f"**Work Package:** {work_data['work_name']}")
                    st.write(f"**NIT Number:** {work_data['nit_number']}")
                    st.write(f"**Total Works:** {work_data.get('total_works', 1)}")
                    st.write(f"**Total Estimated Cost:** ₹{work_data['estimated_cost']:,.2f}")
                    st.write(f"**Total Earnest Money:** ₹{work_data['earnest_money']:,.2f}")
                
                with col2:
                    st.subheader("📅 Timeline Information")
                    st.write(f"**NIT Date:** {work_data.get('nit_date', 'Not found')}")
                    st.write(f"**Receipt Date:** {work_data.get('receipt_date', 'Not found')}")
                    st.write(f"**Opening Date:** {work_data.get('opening_date', 'Not found')}")
                    st.write(f"**Max Completion Time:** {work_data.get('time_completion', 6)} months")
                
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
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")

def handle_bidder_management():
    """Handle bidder management operations with work selection and dropdown method."""
    st.header("👥 Manage Bidders")
    
    work_data = st.session_state.get("current_work")
    if work_data is None:
        st.warning("⚠️ Please upload a NIT document first.")
        return
    
    # Handle work selection if multiple works exist
    selected_work = None
    if work_data.get('works') and len(work_data['works']) > 1:
        st.subheader("📋 Step 1: Select Work for Bidding")
        work_options = [f"Item {work['item_no']}: {work['name']} (₹{work['estimated_cost']:,.0f})" for work in work_data['works']]
        selected_work_index = st.selectbox(
            "Select which work to process bids for:",
            range(len(work_options)),
            format_func=lambda x: work_options[x],
            help="Choose the specific work item for which you want to add bidders"
        )
        selected_work = work_data['works'][selected_work_index]
        
        # Display work details in columns
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Selected Work:** {selected_work['name']}")
            st.write(f"**Item Number:** {selected_work['item_no']}")
            st.write(f"**Estimated Cost:** ₹{selected_work['estimated_cost']:,.2f}")
        with col2:
            st.write(f"**Time Completion:** {selected_work['time_completion']} months")
            st.write(f"**Earnest Money:** ₹{selected_work['earnest_money']:,.2f}")
        st.markdown("---")
    else:
        # Handle case with single work
        selected_work = work_data['works'][0] if work_data.get('works') else {
            'item_no': '1',
            'name': work_data['work_name'],
            'estimated_cost': st.session_state.current_work['estimated_cost'],
            'earnest_money': st.session_state.current_work['earnest_money'],
            'time_completion': st.session_state.current_work.get('time_completion', '6 months')
        }
    
    if not selected_work:
        st.error("❌ No work selected or available.")
        return
    
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
    bidder_database = {}
    try:
        with open('bidder_database.json', 'r', encoding='utf-8') as f:
            bidder_database = json.load(f)
    except Exception as e:
<<<<<<< HEAD
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
=======
        st.warning(f"⚠️ Could not load bidder database: {str(e)}. Creating new database.")
        bidder_database = {}
    
    st.info(f"📋 Available bidders in database: {len(bidder_database)}")
    
    st.subheader("📊 Step 2: Select Number of Bidders")
    num_bidders = st.number_input(
        f"How many bidders participated for {selected_work['name']}?", 
        min_value=1, 
        max_value=20, 
        value=3,
        help="Select the number of bidders who submitted tenders for this work"
    )
    
    if num_bidders:
        st.subheader("👥 Step 3: Add Bidders and Enter Percentages")
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
        if 'bidder_inputs' not in st.session_state:
            st.session_state.bidder_inputs = {}
        
        bidder_data_list = []
        all_valid = True
        
        for i in range(num_bidders):
            st.markdown(f"### Bidder {i+1}")
            
            # Use a radio button to choose between selecting from database or adding new bidder
            bidder_source = st.radio(
                f"Bidder {i+1} source:",
                ["Select from database", "Add new bidder"],
                key=f"source_{i}",
                horizontal=True
            )
            
            if bidder_source == "Select from database":
                # Display dropdown to select from existing bidders
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Dropdown to select bidder from database
                    selected_bidder = st.selectbox(
                        f"Select Bidder {i+1}:",
                        options=[""] + list(bidder_database.keys()),
                        key=f"bidder_select_{i}",
                        help="Choose from registered bidders"
                    )
                    
                    # Show bidder address if selected
                    if selected_bidder and selected_bidder in bidder_database:
                        st.caption(f"📍 Address: {bidder_database[selected_bidder]['address']}")
                
                with col2:
                    # Percentage input for selected bidder
                    percentage_str = st.text_input(
                        f"Percentage (%):",
                        placeholder="e.g., -5.50",
                        key=f"percentage_{i}",
                        help="Enter % above (+) or below (-) estimate"
                    )
                
                # Set bidder name and address for validation
                bidder_name = selected_bidder
                bidder_address = bidder_database.get(selected_bidder, {}).get('address', '') if selected_bidder else ''
                
            else:
                # Form to add a new bidder
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    bidder_name = st.text_input(
                        f"Bidder {i+1} Name:",
                        key=f"new_bidder_name_{i}",
                        placeholder="Enter bidder company name"
                    )
                    bidder_address = st.text_area(
                        f"Bidder {i+1} Address:",
                        key=f"new_bidder_address_{i}",
                        placeholder="Enter complete address",
                        height=60
                    )
                
                with col2:
                    # Percentage input for new bidder
                    percentage_str = st.text_input(
                        f"Percentage (%):",
                        placeholder="e.g., -5.50",
                        key=f"percentage_{i}",
                        help="Enter % above (+) or below (-) estimate"
                    )
            
                )
            
<<<<<<< HEAD
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
=======
            with col3:
                if bidder_name and bidder_address and percentage_str:
                    try:
                        percentage = float(percentage_str)
                        if -99.99 <= percentage <= 99.99:
                            processor = TenderProcessor()
                            bid_amount = processor.calculate_bid_amount(selected_work['estimated_cost'], percentage)
                            st.metric("Bid Amount", f"₹{bid_amount:,.0f}")
                            st.caption(f"{percentage:+.2f}% of ₹{selected_work['estimated_cost']:,.0f}")
                            bidder_data = {
                                'name': bidder_name,
                                'address': bidder_address,
                                'percentage': percentage,
                                'bid_amount': bid_amount,
                                'earnest_money': selected_work['earnest_money'],
                                'date_added': DateUtils().get_current_date(),
                                'work_item': selected_work['item_no'],
                                'work_name': selected_work['name'],
                                'estimated_cost': selected_work['estimated_cost']
                            }
                            bidder_data_list.append(bidder_data)
                        else:
                            st.error("❌ Percentage must be between -99.99% and +99.99%")
                            all_valid = False
                    except ValueError:
                        st.error("❌ Please enter a valid percentage value")
                        all_valid = False
                elif bidder_name or percentage_str:
                    all_valid = False
            
            st.markdown("---")
        
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Add All Bidders", type="primary", disabled=not all_valid or len(bidder_data_list) != num_bidders):
                st.session_state.bidders = bidder_data_list
<<<<<<< HEAD
                
                # Update bidder database with last used dates
                for bidder_data in bidder_data_list:
                    if bidder_data['name'] in bidder_database:
                        bidder_database[bidder_data['name']]['last_used'] = DateUtils().get_current_date()
                
                # Save updated database
=======
                for bidder_data in bidder_data_list:
                    if bidder_data['name'] in bidder_database:
                        bidder_database[bidder_data['name']]['last_used'] = DateUtils().get_current_date()
                    else:
                        bidder_database[bidder_data['name']] = {
                            'address': bidder_data['address'],
                            'date_added': DateUtils().get_current_date(),
                            'last_used': DateUtils().get_current_date(),
                            'total_tenders': 1
                        }
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
                try:
                    with open('bidder_database.json', 'w', encoding='utf-8') as f:
                        json.dump(bidder_database, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    st.warning(f"⚠️ Could not update bidder database: {str(e)}")
<<<<<<< HEAD
                
=======
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
                st.success(f"✅ Added {len(bidder_data_list)} bidders successfully!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All", type="secondary"):
                st.session_state.bidders = []
                if 'bidder_inputs' in st.session_state:
                    del st.session_state.bidder_inputs
                st.success("✅ Reset all bidder selections")
                st.rerun()
    
<<<<<<< HEAD
    # Display current bidders
    if st.session_state.bidders:
        st.subheader("📊 Current Selected Bidders")
        
        # Create DataFrame for display
=======
    if st.session_state.bidders:
        st.subheader("📊 Current Selected Bidders")
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
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
<<<<<<< HEAD
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Show L1 bidder
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        st.success(f"🥇 L1 (Lowest) Bidder: {l1_bidder['name']} - ₹{l1_bidder['bid_amount']:,.2f} ({l1_bidder['percentage']:+.2f}%)")
        
        # Clear all bidders option
=======
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        st.success(f"🥇 L1 (Lowest) Bidder: {l1_bidder['name']} - ₹{l1_bidder['bid_amount']:,.2f} ({l1_bidder['percentage']:+.2f}%)")
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
        if st.button("🗑️ Clear All Bidders", type="secondary"):
            st.session_state.bidders = []
            st.success("✅ Cleared all bidders")
            st.rerun()

def handle_report_generation():
<<<<<<< HEAD
    """Handle report generation with simultaneous generation and download."""
=======
    """Handle report generation with LaTeX-based PDF generation."""
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
    st.header("📊 Generate Reports")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
        return
    
<<<<<<< HEAD
    # Bulk Generation Section
=======
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

>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
    st.subheader("🚀 Generate All Reports Simultaneously")
    
    col1, col2 = st.columns(2)
    
    with col1:
<<<<<<< HEAD
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
    """Handle official document generation with individual options."""
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
                
            except Exception as e:
                st.error(f"❌ Error generating Scrutiny Sheet: {str(e)}")
                logging.error(f"Error generating scrutiny sheet: {e}")



if __name__ == "__main__":
    main()
=======
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
                            file_name=f"{doc_type}_{work_info['nit_number']}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{doc_type}_{work_info['nit_number']}"
                        )
                else:
                    st.error("❌ Failed to generate any PDF documents. Check app.log for details.")
            except Exception as e:
                st.error(f"❌ Error generating PDFs: {str(e)}")
                logging.error(f"Error generating PDFs: {e}", exc_info=True)
    
    with col2:
        if st.button("🚀 Download All as ZIP", type="primary"):
            try:
                with st.spinner("Creating ZIP package..."):
                    zip_gen = ZipGenerator()
                    if st.session_state.generated_pdfs:
                        documents = st.session_state.generated_pdfs
                    else:
                        documents = latex_gen.generate_bulk_pdfs(formatted_work_data, valid_bidders)
                    
                    if documents:
                        zip_data = zip_gen.create_tender_documents_zip(
                            work_info['work_name'],
                            work_info['nit_number'],
                            documents
                        )
                        if zip_data:
                            nit_number = work_info['nit_number'].replace('/', '_')
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


def handle_document_generation():
    if 'current_work' not in st.session_state or not st.session_state.current_work:
        st.error("No work selected. Please upload NIT document and select a work.")
        return
    
    latex_gen = st.session_state.latex_gen
    zip_gen = st.session_state.zip_gen
    work_data = st.session_state.current_work
    work_id = work_data['work_info']['item_no']
    valid_bidders = st.session_state.valid_bidders.get(work_id, [])

    try:
        latex_gen.logger.info(f"handle_document_generation: valid_bidders for work {work_id} type: {type(valid_bidders)}, value: {valid_bidders}")
        if not valid_bidders:
            st.error(f"No valid bidders for work {work_id}. Please add bidders.")
            return
        if not isinstance(valid_bidders, list):
            st.error(f"Invalid bidder data type for work {work_id}: {type(valid_bidders)}. Please ensure bidders are correctly added.")
            latex_gen.logger.error(f"Invalid valid_bidders type for work {work_id}: {type(valid_bidders)}")
            return
        
        l1_bidder = min(valid_bidders, key=lambda x: x.get('bid_amount', float('inf')))
        
        st.subheader(f"Generate Documents for Work {work_id}")
        if st.button(f"Generate Comparative Statement (Work {work_id})"):
            pdf_bytes = latex_gen.generate_comparative_statement_pdf(work_data, valid_bidders)
            st.download_button(
                label="Download Comparative Statement",
                data=pdf_bytes,
                file_name=f"Comparative_Statement_Work_{work_id}.pdf",
                mime="application/pdf"
            )
        
        if st.button(f"Generate Letter of Acceptance (Work {work_id})"):
            pdf_bytes = latex_gen.generate_letter_acceptance_pdf(work_data, l1_bidder)
            st.download_button(
                label="Download Letter of Acceptance",
                data=pdf_bytes,
                file_name=f"Letter_of_Acceptance_Work_{work_id}.pdf",
                mime="application/pdf"
            )
        
        if st.button(f"Generate Work Order (Work {work_id})"):
            pdf_bytes = latex_gen.generate_work_order_pdf(work_data, l1_bidder)
            st.download_button(
                label="Download Work Order",
                data=pdf_bytes,
                file_name=f"Work_Order_Work_{work_id}.pdf",
                mime="application/pdf"
            )
        
        if st.button(f"Generate Scrutiny Sheet (Work {work_id})"):
            pdf_bytes = latex_gen.generate_scrutiny_sheet_pdf(work_data, valid_bidders)
            st.download_button(
                label="Download Scrutiny Sheet",
                data=pdf_bytes,
                file_name=f"Scrutiny_Sheet_Work_{work_id}.pdf",
                mime="application/pdf"
            )
        
        if st.button(f"Generate All Documents as ZIP (Work {work_id})"):
            documents = latex_gen.generate_bulk_pdfs(work_data, valid_bidders)
            zip_buffer = zip_gen.create_zip(documents)
            st.download_button(
                label="Download All Documents (ZIP)",
                data=zip_buffer,
                file_name=f"{work_data['work_info']['nit_number']}_Work_{work_id}_documents.zip",
                mime="application/zip"
            )
    
    except Exception as e:
        st.error(f"Error generating documents for work {work_id}: {str(e)}")
        latex_gen.logger.error(f"Error in handle_document_generation for work {work_id}: {str(e)}")



def main():
    apply_custom_css()
    initialize_session_state()
    ui = UIComponents()
    
    st.title("Tender Management System")
    st.header("Upload NIT Document")
    ui.render_nit_upload()
    
    if st.session_state.works:
        st.header("Select Work")
        work_options = [(work['work_info']['item_no'], work['work_info']['work_name']) for work in st.session_state.works]
        selected_work_id = st.selectbox("Select Work", options=[f"{item_no}: {work_name}" for item_no, work_name in work_options])
        selected_work_id = selected_work_id.split(":")[0]
        st.session_state.current_work = next((work for work in st.session_state.works if work['work_info']['item_no'] == selected_work_id), None)
        
        st.header(f"Manage Bidders for Work {selected_work_id}")
        ui.render_bidder_management(selected_work_id)
        
        st.header(f"Generate Reports for Work {selected_work_id}")
        ui.render_report_generation()
        
        st.header(f"Generate Documents for Work {selected_work_id}")
        handle_document_generation()

if __name__ == "__main__":
    main()
>>>>>>> 4450922c8f3b32619b264d80490734ef8b8a24d6
