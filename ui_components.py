import streamlit as st
from tender_processor import TenderProcessor
from excel_parser import ExcelParser
from bidder_manager import BidderManager

class UIComponents:
    def __init__(self):
        self.tender_processor = TenderProcessor()
        self.excel_parser = ExcelParser()
        self.bidder_manager = BidderManager()

    def render_nit_upload(self):
        uploaded_file = st.file_uploader("Upload NIT Excel Document", type=['xlsx'])
        if uploaded_file:
            try:
                work_data = self.excel_parser.parse_nit_excel(uploaded_file)
                st.session_state.current_work = work_data
                st.success("NIT document uploaded successfully!")
            except Exception as e:
                st.error(f"Error processing NIT document: {str(e)}")
                self.tender_processor.logger.error(f"Error processing NIT: {str(e)}")

    def render_bidder_management(self):
        st.subheader("Add Bidder")
        with st.form("bidder_form"):
            name = st.text_input("Bidder Name")
            bid_amount = st.number_input("Bid Amount", min_value=0.0, step=1000.0)
            percentage = st.number_input("Percentage Above/Below", step=0.01)
            address = st.text_input("Bidder Address")
            earnest_money = st.number_input("Earnest Money", min_value=0.0, step=1000.0)
            work_item = st.text_input("Work Item", value=st.session_state.current_work.get('work_info', {}).get('item_no', '1') if st.session_state.get('current_work') else '1')
            work_name = st.text_input("Work Name", value=st.session_state.current_work.get('work_info', {}).get('work_name', '') if st.session_state.get('current_work') else '')
            estimated_cost = st.number_input("Estimated Cost", min_value=0.0, step=1000.0, value=st.session_state.current_work.get('work_info', {}).get('estimated_cost', 0.0) if st.session_state.get('current_work') else 0.0)
            submit = st.form_submit_button("Add Bidder")
            if submit:
                try:
                    self.bidder_manager.add_bidder(name, bid_amount, percentage, address, earnest_money, work_item, work_name, estimated_cost)
                    st.success(f"Bidder {name} added successfully!")
                except Exception as e:
                    st.error(f"Error adding bidder: {str(e)}")
                    self.bidder_manager.logger.error(f"Error adding bidder: {str(e)}")
        if st.session_state.get('valid_bidders'):
            st.subheader("Current Bidders")
            for bidder in st.session_state.valid_bidders:
                st.write(f"Name: {bidder['name']}, Bid Amount: {bidder['bid_amount']:,}, Percentage: {bidder['percentage']}%")

    def render_report_generation(self):
        st.subheader("Generate Report")
        if st.button("Generate Tender Report"):
            try:
                report = self.tender_processor.generate_report(st.session_state.current_work, st.session_state.get('valid_bidders', []))
                st.write("### Tender Report")
                st.write(report)
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
                self.tender_processor.logger.error(f"Error generating report: {str(e)}")