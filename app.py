"""
Tender Management System - Main Application

This module serves as the entry point for the Tender Management System.
It handles the Streamlit UI, navigation, and coordinates between different components.
"""

import json
import logging
import os
import sys
import tempfile
import traceback
import pandas as pd
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Local application imports
from latex_pdf_generator import LatexPDFGenerator
from zip_generator import ZipGenerator
from tender_processor import TenderProcessor
from excel_parser import ExcelParser
from bidder_manager import BidderManager
from date_utils import DateUtils
from ui_components import UIComponents, show_balloons
from theme import apply_custom_css

# Configure logging
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_session_state() -> None:
    """
    Initialize the Streamlit session state with default values.
    
    This function sets up all the necessary session state variables
    used throughout the application.
    """
    # Application state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Data storage
        st.session_state.works: List[Dict[str, Any]] = []
        st.session_state.current_work: Optional[Dict[str, Any]] = None
        st.session_state.bidders: List[Dict[str, Any]] = []
        st.session_state.valid_bidders: Dict[str, List[Dict[str, Any]]] = {}
        st.session_state.generated_pdfs: Dict[str, bytes] = {}
        st.session_state.status_message: str = ""
        
        # Service instances
        st.session_state.latex_gen = LatexPDFGenerator()
        st.session_state.zip_gen = ZipGenerator()
        st.session_state.tender_processor = TenderProcessor()
        st.session_state.excel_parser = ExcelParser()
        st.session_state.bidder_manager = BidderManager()
        st.session_state.ui = UIComponents()
        
        logger.info("Application session state initialized")

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
apply_custom_css()

def handle_nit_upload():
    """
    Handle NIT document upload and processing with enhanced error handling.
    """
    st.header("📄 Upload NIT Document")
    
    # Display information card
    ui = UIComponents()
    ui.create_info_card(
        "NIT Document Upload", 
        "Upload your Notice Inviting Tender (NIT) Excel file to extract work details and estimated costs. "
        "The system supports multiple date formats and will automatically parse the tender information.",
        "📄"
    )
    
    # File uploader with allowed types
    uploaded_file = st.file_uploader(
        "Choose NIT Excel file", 
        type=['xlsx', 'xls'],
        help="Upload the official NIT Excel document (XLSX or XLS format)"
    )
    
    if uploaded_file is not None:
        try:
            # Show loading spinner while processing
            with st.spinner("Processing NIT document..."):
                # Create a temporary file to store the uploaded content
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    try:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    except Exception as file_error:
                        logger.error(f"Failed to save uploaded file: {str(file_error)}\n{traceback.format_exc()}")
                        st.error("❌ Failed to process the uploaded file. Please try again.")
                        return
                
                try:
                    # Initialize parser and parse the Excel file
                    parser = ExcelParser()
                    # Log file content for debugging
                    logger.info(f"Attempting to parse file: {tmp_file_path}")
                    logger.info(f"File size: {os.path.getsize(tmp_file_path)} bytes")
                    
                    # Try to read the Excel file with pandas first to verify it's valid
                    try:
                        test_df = pd.read_excel(tmp_file_path, engine='openpyxl')
                        logger.info(f"Successfully read Excel file with {len(test_df)} rows and {len(test_df.columns)} columns")
                        logger.debug(f"Columns: {test_df.columns.tolist()}")
                    except Exception as test_error:
                        logger.error(f"Failed to read Excel file with pandas: {str(test_error)}")
                        st.error(f"❌ The uploaded file is not a valid Excel file or is corrupted. Error: {str(test_error)}")
                        return
                        
                    works = parser.parse_nit_excel(tmp_file_path)
                    
                    # Clean up the temporary file
                    try:
                        os.unlink(tmp_file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to delete temporary file: {str(cleanup_error)}")
                    
                    if not works:
                        st.error("❌ No valid work items found in the uploaded document.")
                        return
                    
                    # Prepare the work data for the session
                    work_data = {
                        'works': works,
                        'total_works': len(works),
                        **works[0]['work_info']  # Include first work's info at the top level for backward compatibility
                    }
                    
                    # Store the work data in session state
                    st.session_state.current_work = work_data
                    
                    # Show success message
                    st.success("✅ NIT document uploaded and parsed successfully!")
                    
                    # Force a rerun to update the UI with the parsed data
                    st.rerun()
                    
                    # Display the parsed information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 NIT Information")
                        st.write(f"**Work Package:** {work_data['work_name']}")
                        st.write(f"**NIT Number:** {work_data['nit_number']}")
                        st.write(f"**Total Works:** {len(works)}")
                        st.write(f"**Estimated Cost:** ₹{float(work_data['estimated_cost']):,.2f}")
                        st.write(f"**Earnest Money:** ₹{float(work_data['earnest_money']):,.2f}")
                        st.write(f"**Time for Completion:** {work_data['time_completion']}")
                        
                    with col2:
                        st.subheader("📅 Important Dates")
                        st.write(f"**NIT Date:** {work_data['nit_date']}")
                        st.write(f"**Receipt of Tender:** {work_data['receipt_date']}")
                        st.write(f"**Opening of Tender:** {work_data['opening_date']}")
                        
                    # Show additional work items if available
                    if len(works) > 1:
                        st.subheader("📋 Additional Work Items")
                        for i, work in enumerate(works[1:], 2):
                            work_info = work['work_info']
                            st.write(f"**{i}.** {work_info.get('work_name', 'Unnamed Work')}")
                            st.write(f"   - Estimated Cost: ₹{float(work_info.get('estimated_cost', 0)):,.2f}")
                            st.write(f"   - Earnest Money: ₹{float(work_info.get('earnest_money', 0)):,.2f}")
                    
                except ValueError as ve:
                    st.error(f"❌ {str(ve)}")
                    logger.error(f"Validation error in NIT upload: {str(ve)}\n{traceback.format_exc()}")
                except pd.errors.EmptyDataError:
                    st.error("❌ The uploaded Excel file is empty or corrupted.")
                    logger.error("Empty or corrupted Excel file uploaded")
                except Exception as e:
                    st.error("❌ An unexpected error occurred while processing the NIT document.")
                    logger.error(f"Unexpected error in NIT upload: {str(e)}\n{traceback.format_exc()}")
                finally:
                    # Ensure temporary file is deleted even if an error occurs
                    try:
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to delete temporary file in finally block: {str(cleanup_error)}")
        
                    # Show individual work details if only one work exists
                    if len(works) == 1:
                        work = works[0]['work_info']
                        st.subheader("📋 Work Details")
                        st.write(f"**Work Name:** {work.get('work_name', 'Unnamed Work')}")
                        st.write(f"**Estimated Cost:** ₹{float(work.get('estimated_cost', 0)):,.2f}")
                        st.write(f"**Earnest Money:** ₹{float(work.get('earnest_money', 0)):,.2f}")
                        st.write(f"**Time of Completion:** {work.get('time_completion', '6 months')}")
                        st.info("💡 Go to 'Manage Bidders' to add bidders for this work.")
                        
                    # Show success animation
                    show_balloons()
                    
        except Exception as e:
            st.error("❌ An error occurred while processing your request. Please try again.")
            logger.error(f"Critical error in handle_nit_upload: {str(e)}\n{traceback.format_exc()}")
    else:
        st.info("ℹ️ Please upload an NIT document to begin.")
        
        # Show example format if no file is uploaded
        with st.expander("📋 Expected Excel Format"):
            st.write("""
            Your NIT Excel file should follow this format:
            
            | A              | B                    | C                  |
            |----------------|----------------------|--------------------|
            | NIT No.:       | NIT-123              |                    |
            | NIT Date:      | 01/01/2023           |                    |
            | Receipt Date:  | 15/01/2023           |                    |
            | Opening Date:  | 16/01/2023           |                    |
            |                |                      |                    |
            | ITEM NO.       | NAME OF WORK         | ESTIMATED COST RS. |
            | 1              | Road Construction    | 50.00              |
            | 2              | Bridge Construction  | 75.00              |
            
            Note: The first 4 rows should contain the metadata, followed by the work items.
            """)

def handle_bidder_management():
    """Handle bidder management operations with work selection."""
    st.header("👥 Manage Bidders")
    
    work_data = st.session_state.get("current_work")
    if work_data is None:
        st.warning("⚠️ Please upload a NIT document first.")
        return
    
    selected_work = None
    if st.session_state.current_work.get('works') and len(st.session_state.current_work['works']) > 1:
        st.subheader("📋 Step 1: Select Work for Bidding")
        work_options = [f"Item {work['work_info']['item_no']}: {work['work_info']['work_name']} (₹{float(work['work_info']['estimated_cost']):,.0f})" for work in st.session_state.current_work['works']]
        selected_work_index = st.selectbox(
            "Select which work to process bids for:",
            range(len(work_options)),
            format_func=lambda x: work_options[x],
            help="Choose the specific work item for which you want to add bidders"
        )
        selected_work = st.session_state.current_work['works'][selected_work_index]['work_info']
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Selected Work:** {selected_work['work_name']}")
            st.write(f"**Item Number:** {selected_work['item_no']}")
            st.write(f"**Estimated Cost:** ₹{selected_work['estimated_cost']:,.2f}")
        with col2:
            st.write(f"**Time Completion:** {selected_work['time_completion']} months")
            st.write(f"**Earnest Money:** ₹{selected_work['earnest_money']:,.2f}")
        st.markdown("---")
    else:
        if st.session_state.current_work.get('works'):
            selected_work = st.session_state.current_work['works'][0]['work_info']
        else:
            selected_work = {
                'item_no': '1',
                'work_name': st.session_state.current_work['work_name'],
                'estimated_cost': st.session_state.current_work['estimated_cost'],
                'earnest_money': st.session_state.current_work['earnest_money'],
                'time_completion': st.session_state.current_work.get('time_completion', '6 months')
            }
    
    if not selected_work:
        st.error("❌ No work selected or available.")
        return
    
    # Define database path
    DB_PATH = Path(__file__).parent / "bidder_database.json"
    
    # Load or create bidder database
    bidder_database = {}
    if DB_PATH.exists():
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                bidder_database = json.load(f)
        except Exception as e:
            st.error(f"❌ Error loading bidder database: {str(e)}")
            return
    
    st.info(f"📋 Available bidders in database: {len(bidder_database)}")
    
    st.subheader("📊 Step 2: Select Number of Bidders")
    num_bidders = st.number_input(
        f"How many bidders participated for {selected_work['work_name']}?", 
        min_value=1, 
        max_value=20, 
        value=3,
        help="Select the number of bidders who submitted tenders for this work"
    )
    
    if num_bidders:
        st.subheader("👥 Step 3: Add Bidders and Enter Percentages")
        if 'bidder_inputs' not in st.session_state:
            st.session_state.bidder_inputs = {}
        
        bidder_data_list = []
        all_valid = True
        
        for i in range(num_bidders):
            st.markdown(f"### Bidder {i+1}")
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                bidder_source = st.radio(
                    f"Bidder {i+1} source:",
                    ["Select from database", "Add new bidder"],
                    key=f"source_{i}",
                    horizontal=True
                )
                if bidder_source == "Select from database":
                    selected_bidder = st.selectbox(
                        f"Select Bidder {i+1}:",
                        options=[""] + list(bidder_database.keys()),
                        key=f"bidder_select_{i}",
                        help="Choose from registered bidders"
                    )
                    bidder_name = selected_bidder
                    bidder_address = bidder_database.get(selected_bidder, {}).get('address', '') if selected_bidder else ''
                    if selected_bidder and selected_bidder in bidder_database:
                        st.caption(f"📍 Address: {bidder_address}")
                else:
                    bidder_name = st.text_input(
                        f"Bidder {i+1} Name:",
                        key=f"new_bidder_name_{i}",
                        placeholder="Enter bidder company name"
                    )
                    bidder_address = st.text_input(
                        f"Bidder {i+1} Address:",
                        key=f"new_bidder_address_{i}",
                        placeholder="Enter complete address"
                    )
            
            with col2:
                percentage_str = st.text_input(
                    f"Percentage (%):",
                    placeholder="e.g., -5.50",
                    key=f"percentage_{i}",
                    help="Enter % above (+) or below (-) estimate"
                )
            
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
                                'work_name': selected_work['work_name'],
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
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Add All Bidders", type="primary", disabled=not all_valid or len(bidder_data_list) != num_bidders):
                st.session_state.bidders = bidder_data_list
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
    
    if st.session_state.bidders:
        st.subheader("📊 Current Selected Bidders")
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
        sorted_bidders = sorted(st.session_state.bidders, key=lambda x: x['bid_amount'])
        l1_bidder = sorted_bidders[0]
        st.success(f"🥇 L1 (Lowest) Bidder: {l1_bidder['name']} - ₹{l1_bidder['bid_amount']:,.2f} ({l1_bidder['percentage']:+.2f}%)")

def get_valid_bidders():
    # Ensure bidders exist and have valid bid amounts
    if not hasattr(st.session_state, 'bidders') or not st.session_state.bidders:
        st.error("❌ No bidders found. Please add bidders first.")
        return None
        
    valid_bidders = []
    for bidder in st.session_state.bidders:
        try:
            if 'bid_amount' in bidder and bidder['bid_amount'] is not None:
                # Convert bid_amount to string, clean it, and convert to float
                bid_amount = str(bidder['bid_amount']).replace(',', '').strip()
                if bid_amount.replace('.', '').isdigit():
                    bidder['bid_amount'] = float(bid_amount)
                    valid_bidders.append(bidder)
        except (ValueError, AttributeError) as e:
            logger.warning(f"Skipping bidder due to invalid bid amount: {bidder.get('name', 'Unknown')} - {bidder.get('bid_amount')}")
    
    if not valid_bidders:
        st.error("❌ No valid bidders with proper bid amounts found.")
        return None
            
    return valid_bidders

    if st.button("🗑️ Clear All Bidders", type="secondary"):
        st.session_state.bidders = []
        st.success("✅ Cleared all bidders")
        st.rerun()

def handle_report_generation():
    """Handle report generation with LaTeX-based PDF generation."""
    st.header("📊 Generate Reports")
    
    if 'current_work' not in st.session_state or not st.session_state.current_work:
        st.warning("⚠️ Please upload NIT document first.")
        return
    
    if 'bidders' not in st.session_state or not st.session_state.bidders:
        st.warning("⚠️ Please add bidders for this work first.")
        return
    
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
    
    # Ensure valid_bidders is properly initialized
    valid_bidders = []
    if 'bidders' in st.session_state and st.session_state.bidders:
        try:
            valid_bidders = [
                b for b in st.session_state.bidders 
                if b and 'bid_amount' in b and b['bid_amount'] is not None
            ]
            # Sort bidders by bid amount
            valid_bidders = sorted(valid_bidders, key=lambda x: float(str(x['bid_amount']).replace(',', '')))
        except Exception as e:
            logger.error(f"Error processing bidders: {str(e)}")
            st.error("❌ Error processing bidders. Please check the bid amounts.")
            return
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
        if st.button("📦 Generate All PDFs (LaTeX)", type="primary"):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                latex_gen = st.session_state.latex_gen
                
                # Get valid bidders
                valid_bidders = get_valid_bidders()
                if not valid_bidders:
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
                    # Get valid bidders first
                    valid_bidders = get_valid_bidders()
                    if not valid_bidders:
                        return
                        
                    zip_gen = st.session_state.zip_gen
                    if not hasattr(st.session_state, 'generated_pdfs') or not st.session_state.generated_pdfs:
                        # Generate PDFs if not already generated
                        latex_gen = st.session_state.latex_gen
                        try:
                            documents = latex_gen.generate_bulk_pdfs(formatted_work_data, valid_bidders)
                            if documents:
                                st.session_state.generated_pdfs = documents
                                documents = documents  # Make sure documents is defined
                            else:
                                st.error("❌ Failed to generate PDF documents. No documents were created.")
                                return
                        except Exception as e:
                            st.error(f"❌ Error generating PDFs: {str(e)}")
                            logger.error(f"Error in generate_bulk_pdfs: {str(e)}")
                            return
                    else:
                        documents = st.session_state.generated_pdfs
                    
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


def generate_pdf_with_pandoc(latex_content: str) -> bytes:
    """Helper function to generate PDF using Pandoc with error handling."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as tmp_tex:
            tmp_tex.write(latex_content.encode('utf-8'))
            tex_path = tmp_tex.name
        
        pdf_path = tex_path.replace('.tex', '.pdf')
        
        # Run pdflatex to generate PDF
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={os.path.dirname(tex_path)}', tex_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = f"LaTeX Error (Code {result.returncode}):\n{result.stderr}"
            logger.error(error_msg)
            raise RuntimeError(f"Failed to generate PDF: {error_msg}")
        
        # Read the generated PDF
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        return pdf_content
        
    except Exception as e:
        logger.error(f"Error in generate_pdf_with_pandoc: {str(e)}\n{traceback.format_exc()}")
        raise
    finally:
        # Clean up temporary files
        for ext in ['.tex', '.aux', '.log', '.out']:
            try:
                if os.path.exists(tex_path.replace('.tex', ext)):
                    os.remove(tex_path.replace('.tex', ext))
            except Exception as e:
                logger.warning(f"Could not remove temporary file: {e}")

def handle_document_generation():
    """Handle document generation with improved error handling."""
    if 'current_work' not in st.session_state or not st.session_state.current_work:
        st.error("❌ No work selected. Please upload NIT document and select a work.")
        return
    
    if 'bidders' not in st.session_state or not st.session_state.bidders:
        st.error("❌ No bidders found. Please add bidders first.")
        return
    
    latex_gen = st.session_state.latex_gen
    zip_gen = st.session_state.zip_gen
    work_data = st.session_state.current_work
    
    # Get work ID safely
    work_id = work_data.get('work_info', {}).get('item_no', '1')
    
    # Get valid bidders
    valid_bidders = get_valid_bidders()
    if not valid_bidders:
        st.error("❌ No valid bidders with proper bid amounts found.")
        return

    try:
        latex_gen.logger.info(f"handle_document_generation: Processing work {work_id} with {len(valid_bidders)} valid bidders")
        
        # Sort bidders by bid amount
        valid_bidders = sorted(valid_bidders, key=lambda x: float(str(x.get('bid_amount', '0')).replace(',', '') if isinstance(x.get('bid_amount'), str) else x.get('bid_amount', 0)))
        l1_bidder = valid_bidders[0] if valid_bidders else None
        
        st.subheader(f"Generate Documents for Work {work_id}")
        
        # Generate and download Comparative Statement
        if st.button(f"Generate Comparative Statement (Work {work_id})"):
            with st.spinner("Generating Comparative Statement..."):
                try:
                    latex_content = latex_gen.generate_comparative_statement_latex(work_data, valid_bidders)
                    pdf_bytes = generate_pdf_with_pandoc(latex_content)
                    st.success("✅ Comparative Statement generated successfully!")
                    st.download_button(
                        label="Download Comparative Statement",
                        data=pdf_bytes,
                        file_name=f"Comparative_Statement_Work_{work_id}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Failed to generate Comparative Statement: {str(e)}")
                    logger.error(f"Error in generate_comparative_statement_pdf: {str(e)}\n{traceback.format_exc()}")
        
        # Generate and download Letter of Acceptance
        if st.button(f"Generate Letter of Acceptance (Work {work_id})"):
            with st.spinner("Generating Letter of Acceptance..."):
                try:
                    latex_content = latex_gen.generate_letter_acceptance_latex(work_data, l1_bidder)
                    pdf_bytes = generate_pdf_with_pandoc(latex_content)
                    st.success("✅ Letter of Acceptance generated successfully!")
                    st.download_button(
                        label="Download Letter of Acceptance",
                        data=pdf_bytes,
                        file_name=f"Letter_of_Acceptance_Work_{work_id}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Failed to generate Letter of Acceptance: {str(e)}")
                    logger.error(f"Error in generate_letter_acceptance_pdf: {str(e)}\n{traceback.format_exc()}")
        
        # Generate and download Work Order
        if st.button(f"Generate Work Order (Work {work_id})"):
            with st.spinner("Generating Work Order..."):
                try:
                    latex_content = latex_gen.generate_work_order_latex(work_data, l1_bidder)
                    pdf_bytes = generate_pdf_with_pandoc(latex_content)
                    st.success("✅ Work Order generated successfully!")
                    st.download_button(
                        label="Download Work Order",
                        data=pdf_bytes,
                        file_name=f"Work_Order_Work_{work_id}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Failed to generate Work Order: {str(e)}")
                    logger.error(f"Error in generate_work_order_pdf: {str(e)}\n{traceback.format_exc()}")
        
        # Generate and download Scrutiny Sheet
        if st.button(f"Generate Scrutiny Sheet (Work {work_id})"):
            with st.spinner("Generating Scrutiny Sheet..."):
                try:
                    latex_content = latex_gen.generate_scrutiny_sheet_latex(work_data, valid_bidders)
                    pdf_bytes = generate_pdf_with_pandoc(latex_content)
                    st.success("✅ Scrutiny Sheet generated successfully!")
                    st.download_button(
                        label="Download Scrutiny Sheet",
                        data=pdf_bytes,
                        file_name=f"Scrutiny_Sheet_Work_{work_id}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Failed to generate Scrutiny Sheet: {str(e)}")
                    logger.error(f"Error in generate_scrutiny_sheet_pdf: {str(e)}\n{traceback.format_exc()}")
        
        # Generate and download all documents as ZIP
        if st.button(f"Generate All Documents as ZIP (Work {work_id})"):
            with st.spinner("Generating all documents..."):
                try:
                    documents = {}
                    
                    # Generate each document
                    try:
                        latex_content = latex_gen.generate_comparative_statement_latex(work_data, valid_bidders)
                        documents['comparative_statement'] = generate_pdf_with_pandoc(latex_content)
                    except Exception as e:
                        logger.error(f"Error generating Comparative Statement: {str(e)}")
                    
                    try:
                        latex_content = latex_gen.generate_letter_acceptance_latex(work_data, l1_bidder)
                        documents['letter_acceptance'] = generate_pdf_with_pandoc(latex_content)
                    except Exception as e:
                        logger.error(f"Error generating Letter of Acceptance: {str(e)}")
                    
                    try:
                        latex_content = latex_gen.generate_work_order_latex(work_data, l1_bidder)
                        documents['work_order'] = generate_pdf_with_pandoc(latex_content)
                    except Exception as e:
                        logger.error(f"Error generating Work Order: {str(e)}")
                    
                    try:
                        latex_content = latex_gen.generate_scrutiny_sheet_latex(work_data, valid_bidders)
                        documents['scrutiny_sheet'] = generate_pdf_with_pandoc(latex_content)
                    except Exception as e:
                        logger.error(f"Error generating Scrutiny Sheet: {str(e)}")
                    
                    if not documents:
                        st.error("❌ Failed to generate any documents. Please check the logs for errors.")
                        return
                    
                    # Create ZIP archive
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for doc_name, content in documents.items():
                            zip_file.writestr(f"{work_data['work_info']['nit_number']}_{doc_name}.pdf", content)
                    
                    zip_buffer.seek(0)
                    st.success(f"✅ Successfully generated {len(documents)} documents!")
                    
                    st.download_button(
                        label="Download All Documents (ZIP)",
                        data=zip_buffer,
                        file_name=f"{work_data['work_info']['nit_number']}_Work_{work_id}_documents.zip",
                        mime="application/zip"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Failed to generate documents: {str(e)}")
                    logger.error(f"Error in generate_all_documents: {str(e)}\n{traceback.format_exc()}")
    
    except Exception as e:
        st.error(f"Error generating documents for work {work_id}: {str(e)}")
        latex_gen.logger.error(f"Error in handle_document_generation for work {work_id}: {str(e)}")



def create_header():
    """Create the application header using UIComponents."""
    ui = UIComponents()
    ui.create_header()

def create_footer():
    """Create the application footer."""
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9rem;
        border-top: 1px solid #dee2e6;
    }
    </style>
    <div class='footer'>
        <p>© 2025 Tender Management System | Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)



def main():
    """Main application function."""
    # Set page config (MUST be the first Streamlit command)
    st.set_page_config(
        page_title="Tender Processing System",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS theme
    from theme import apply_custom_css
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Create header with enhanced UI
    create_header()
    
    # Initialize UI components
    ui = UIComponents()
    
    # Sidebar navigation with enhanced styling
    st.sidebar.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
    }
    .sidebar .sidebar-content .stRadio > div {
        padding: 10px 0;
    }
    .sidebar .sidebar-content label {
        font-size: 1.1em;
        padding: 8px 0;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .sidebar .sidebar-content label:hover {
        background-color: #e9ecef;
        padding-left: 10px;
    }
    .sidebar .sidebar-content .stRadio > div > div > div {
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.title("📋 Navigation")
    operation = st.sidebar.radio(
        "Select Operation:",
        ["📄 Upload NIT Document", "👥 Manage Bidders", "📊 Generate Reports", "📝 Generate Documents"],
        label_visibility="collapsed"
    )
    
    # Add some spacing
    st.sidebar.markdown("---")
    
    # Add a simple status indicator
    if 'current_work' in st.session_state and st.session_state.current_work:
        st.sidebar.success("✅ NIT Document Loaded")
    else:
        st.sidebar.warning("⚠️ No NIT Document Loaded")
    
    # Handle the selected operation
    try:
        if operation == "📄 Upload NIT Document":
            handle_nit_upload()
        elif operation == "👥 Manage Bidders":
            handle_bidder_management()
        elif operation == "📊 Generate Reports":
            handle_report_generation()
        elif operation == "📝 Generate Documents":
            handle_document_generation()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Error in {operation}: {str(e)}")
        logger.error(traceback.format_exc())
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()