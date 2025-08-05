import streamlit as st
import logging
from latex_pdf_generator import LatexPDFGenerator
from zip_generator import ZipGenerator
from tender_processor import TenderProcessor
from excel_parser import ExcelParser
from bidder_manager import BidderManager
from date_utils import DateUtils
from ui_components import UIComponents
from theme import apply_custom_css

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
apply_custom_css()

def main():
    """Main application function."""
    create_header()
    
    if 'current_work' not in st.session_state:
        st.session_state.current_work = None
    if 'bidders' not in st.session_state:
        st.session_state.bidders = []
    if 'bidder_manager' not in st.session_state:
        st.session_state.bidder_manager = BidderManager()
    if 'generated_pdfs' not in st.session_state:
        st.session_state.generated_pdfs = {}
    
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
    
    if operation == "📄 Upload NIT Document":
        handle_nit_upload()
    elif operation == "👥 Manage Bidders":
        handle_bidder_management()
    elif operation == "📊 Generate Reports":
        handle_report_generation()
    elif operation == "📝 Generate Documents":
        handle_document_generation()
    
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
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            parser = ExcelParser()
            work_data = parser.parse_nit_excel(tmp_file_path)
            
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
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            logging.error(f"Error processing NIT file: {e}")

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
        work_options = [f"Item {work['item_no']}: {work['name']} (₹{work['estimated_cost']:,.0f})" for work in st.session_state.current_work['works']]
        selected_work_index = st.selectbox(
            "Select which work to process bids for:",
            range(len(work_options)),
            format_func=lambda x: work_options[x],
            help="Choose the specific work item for which you want to add bidders"
        )
        selected_work = st.session_state.current_work['works'][selected_work_index]
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
        selected_work = st.session_state.current_work['works'][0] if st.session_state.current_work.get('works') else {
            'item_no': '1',
            'name': st.session_state.current_work['work_name'],
            'estimated_cost': st.session_state.current_work['estimated_cost'],
            'earnest_money': st.session_state.current_work['earnest_money'],
            'time_completion': st.session_state.current_work.get('time_completion', '6 months')
        }
    
    if not selected_work:
        st.error("❌ No work selected or available.")
        return
    
    bidder_database = {}
    try:
        with open('bidder_database.json', 'r', encoding='utf-8') as f:
            bidder_database = json.load(f)
    except Exception as e:
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
        if st.button("🗑️ Clear All Bidders", type="secondary"):
            st.session_state.bidders = []
            st.success("✅ Cleared all bidders")
            st.rerun()

def handle_report_generation():
    """Handle report generation with LaTeX-based PDF generation."""
    st.header("📊 Generate Reports")
    
    if not st.session_state.current_work or not st.session_state.bidders:
        st.warning("⚠️ Please upload NIT document and add bidders first.")
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