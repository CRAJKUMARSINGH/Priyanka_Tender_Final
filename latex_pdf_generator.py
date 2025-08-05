import re
import logging
from weasyprint import HTML
from date_utils import DateUtils
from num2words import num2words
import os
import pypandoc
class LatexPDFGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.template_dir = "latex_templates"
        self.date_utils = DateUtils()

    def load_template(self, template_name):
        template_path = os.path.join(self.template_dir, f"{template_name}.tex")
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"Template not found: {template_path}")
            raise FileNotFoundError(f"Template {template_name}.tex not found in {self.template_dir}")
        except Exception as e:
            self.logger.error(f"Error loading template {template_name}: {str(e)}")
            raise

    def _prepare_common_variables(self, work_data, bidder_data=None):
        work_info = work_data.get('work_info', {})
        variables = {
            'WORK_NAME': work_info.get('work_name', 'Unknown Work'),
            'NIT_NUMBER': work_info.get('nit_number', 'Unknown NIT'),
            'NIT_DATE': work_info.get('nit_date', 'Not found'),
            'RECEIPT_DATE': work_info.get('receipt_date', 'Not found'),
            'OPENING_DATE': work_info.get('opening_date', 'Not found'),
            'ESTIMATED_COST': f"{work_info.get('estimated_cost', 0):,.0f}",
            'EARNEST_MONEY': f"{work_info.get('earnest_money', 0):,.0f}",
            'TIME_COMPLETION': work_info.get('time_completion', '6 months'),
            'ITEM_NO': work_info.get('item_no', '1'),
            'CURRENT_DATE': self.date_utils.get_current_date(),
            'NUM_TENDERS_SOLD': '0',
            'NUM_TENDERS_RECEIVED': '0',
            'VALIDITY_DATE': self.date_utils.format_display_date(
                self.date_utils.add_days(self.date_utils.get_current_datetime(), 20)
            )
        }
        if bidder_data is not None:
            self.logger.info(f"bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            if not isinstance(bidder_data, (list, dict)):
                self.logger.error(f"Invalid bidder_data type: {type(bidder_data)}, value: {bidder_data}")
                raise ValueError(f"bidder_data must be a list or dict, got {type(bidder_data)}")
            bidder_list = [bidder_data] if isinstance(bidder_data, dict) else bidder_data
            if bidder_list:
                l1_bidder = min(bidder_list, key=lambda x: x.get('bid_amount', float('inf')))
                variables.update({
                    'L1_BIDDER_NAME': l1_bidder.get('name', 'Unknown Bidder'),
                    'L1_BIDDER_ADDRESS': l1_bidder.get('address', 'Unknown Address'),
                    'L1_BID_AMOUNT': f"{l1_bidder.get('bid_amount', 0):,.0f}",
                    'L1_BID_AMOUNT_WORDS': self._number_to_words(int(l1_bidder.get('bid_amount', 0))),
                    'L1_PERCENTAGE': f"{l1_bidder.get('percentage', 0):.2f}% {'BELOW' if l1_bidder.get('percentage', 0) < 0 else 'ABOVE'}"
                })
                if 'time_completion' in work_info:
                    start_date = self.date_utils.add_days(self.date_utils.get_current_datetime(), 2)
                    months = int(''.join(filter(str.isdigit, work_info['time_completion']))) if work_info['time_completion'] else 6
                    completion_date = self.date_utils.add_months(start_date, months)
                    variables.update({
                        'START_DATE': self.date_utils.format_display_date(start_date),
                        'COMPLETION_DATE': self.date_utils.format_display_date(completion_date),
                        'AGREEMENT_NO': f"{work_info.get('nit_number', 'Unknown')}/2025-26"
                    })
                variables['NUM_TENDERS_SOLD'] = str(len(bidder_list))
                variables['NUM_TENDERS_RECEIVED'] = str(len(bidder_list))
                rows = []
                for i, bidder in enumerate(bidder_list, 1):
                    rows.append(
                        f"{i} & {bidder.get('name', 'Unknown')} & {work_info.get('estimated_cost', 0):,.0f} & "
                        f"{bidder.get('percentage', 0):.2f}\\% {'BELOW' if bidder.get('percentage', 0) < 0 else 'ABOVE'} & "
                        f"{bidder.get('bid_amount', 0):,.0f} \\\\"
                    )
                variables['BIDDER_TABLE_ROWS'] = "\n".join(rows)
            else:
                self.logger.warning("bidder_data is empty")
                variables['BIDDER_TABLE_ROWS'] = ""
        return variables

    def _number_to_words(self, number):
        try:
            return num2words(number, lang='en_IN').replace(',', '').title() + " Only"
        except Exception as e:
            self.logger.error(f"Error converting number to words: {str(e)}")
            return "Unknown Amount"

#Corrections applied
    def convert_latex_to_html(self, latex_content):

        try:
            html_content = pypandoc.convert_text(
                latex_content, 'html', format='latex', extra_args=['--standalone', '--mathjax']
            )
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info("Saved debug HTML to debug_output.html")
            return html_content
        except Exception as e:
            self.logger.error(f"Error converting LaTeX to HTML: {str(e)}")
            raise

    def _create_letter_acceptance_html(self, work_data, bidder_data):
        try:
            template = self.load_template("latex_code_for_letter_of_acceptance")
            variables = self._prepare_common_variables(work_data, bidder_data)
            latex_content = template
            for key, value in variables.items():
                latex_content = latex_content.replace(f"{{{key}}}", str(value))
            return self.convert_latex_to_html(latex_content)
        except Exception as e:
            self.logger.error(f"Error creating Letter of Acceptance HTML: {str(e)}")
            raise

    def generate_work_order_pdf(self, work_data, bidder_data):
        try:
            self.logger.info(f"generate_work_order_pdf: bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            template = self.load_template("latex_code_for_work_order")
            variables = self._prepare_common_variables(work_data, bidder_data)
            latex_content = template
            for key, value in variables.items():
                latex_content = latex_content.replace(f"{{{key}}}", str(value))
            html_content = self.convert_latex_to_html(latex_content)
            pdf_bytes = HTML(string=html_content).write_pdf()
            return pdf_bytes
        except Exception as e:
            self.logger.error(f"Error generating Work Order PDF: {str(e)}")
            raise

    def generate_letter_acceptance_pdf(self, work_data, bidder_data):
        try:
            self.logger.info(f"generate_letter_acceptance_pdf: bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            html_content = self._create_letter_acceptance_html(work_data, bidder_data)
            pdf_bytes = HTML(string=html_content).write_pdf()
            return pdf_bytes
        except Exception as e:
            self.logger.error(f"Error generating Letter of Acceptance PDF: {str(e)}")
            raise

    def generate_comparative_statement_pdf(self, work_data, bidder_data):
        try:
            self.logger.info(f"generate_comparative_statement_pdf: bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            template = self.load_template("latex_code_for_comparative_statement")
            variables = self._prepare_common_variables(work_data, bidder_data)
            latex_content = template
            for key, value in variables.items():
                latex_content = latex_content.replace(f"{{{key}}}", str(value))
            html_content = self.convert_latex_to_html(latex_content)
            pdf_bytes = HTML(string=html_content).write_pdf()
            return pdf_bytes
        except Exception as e:
            self.logger.error(f"Error generating Comparative Statement PDF: {str(e)}")
            raise

    def generate_scrutiny_sheet_pdf(self, work_data, bidder_data):
        try:
            self.logger.info(f"generate_scrutiny_sheet_pdf: bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            template = self.load_template("latex_code_for_scrutiny_sheet")
            variables = self._prepare_common_variables(work_data, bidder_data)
            latex_content = template
            for key, value in variables.items():
                latex_content = latex_content.replace(f"{{{key}}}", str(value))
            html_content = self.convert_latex_to_html(latex_content)
            pdf_bytes = HTML(string=html_content).write_pdf()
            return pdf_bytes
        except Exception as e:
            self.logger.error(f"Error generating Scrutiny Sheet PDF: {str(e)}")
            raise

    def generate_bulk_pdfs(self, work_data, bidder_data):
        try:
            self.logger.info(f"generate_bulk_pdfs: bidder_data type: {type(bidder_data)}, value: {bidder_data}")
            if not isinstance(bidder_data, (list, dict)):
                self.logger.error(f"Invalid bidder_data type in generate_bulk_pdfs: {type(bidder_data)}")
                raise ValueError("bidder_data must be a list or dict")
            bidder_list = [bidder_data] if isinstance(bidder_data, dict) else bidder_data
            documents = {}
            l1_bidder = min(bidder_list, key=lambda x: x.get('bid_amount', float('inf')))
            documents['comparative_statement'] = self.generate_comparative_statement_pdf(work_data, bidder_list)
            documents['letter_of_acceptance'] = self.generate_letter_acceptance_pdf(work_data, l1_bidder)
            documents['work_order'] = self.generate_work_order_pdf(work_data, l1_bidder)
            documents['scrutiny_sheet'] = self.generate_scrutiny_sheet_pdf(work_data, bidder_list)
            return documents
        except Exception as e:
            self.logger.error(f"Error generating bulk PDFs: {str(e)}")
            raise