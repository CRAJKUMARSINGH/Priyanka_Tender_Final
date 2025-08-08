import os
import logging
from datetime import datetime
import pypandoc
import weasyprint
from num2words import num2words
from date_utils import DateUtils
import re
from string import Template

class LatexPDFGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.date_utils = DateUtils()
        self.template_dir = os.path.join(os.path.dirname(__file__), 'latex_templates')
        
        # Ensure Pandoc is available for LaTeX->HTML conversion
        try:
            _ = pypandoc.get_pandoc_version()
        except Exception:
            try:
                pypandoc.download_pandoc()
                self.logger.info("Downloaded local Pandoc binary for conversions")
            except Exception as pandoc_error:
                self.logger.warning(f"Pandoc not available and download failed: {pandoc_error}")
        
    def _load_template(self, template_name):
        template_path = os.path.join(self.template_dir, template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"Template not found: {template_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading template {template_name}: {str(e)}")
            raise

    def _prepare_common_variables(self, work_data, l1_bidder=None, bidders=None):
        if not work_data or 'work_info' not in work_data:
            self.logger.error("Invalid work_data: missing or None")
            raise ValueError("Invalid work_data")
        
        work_info = work_data['work_info']
        variables = {
            'NIT_NUMBER': work_info.get('nit_number', 'Unknown'),
            'NIT_DATE': work_info.get('nit_date', 'Unknown'),
            'RECEIPT_DATE': work_info.get('receipt_date', 'Unknown'),
            'OPENING_DATE': work_info.get('opening_date', 'Unknown'),
            'ITEM_NO': work_info.get('item_no', '1'),
            'WORK_NAME': work_info.get('work_name', 'Unknown Work'),
            'ESTIMATED_COST': f"{work_info.get('estimated_cost', 0):,.2f}",
            'EARNEST_MONEY': f"{work_info.get('earnest_money', 0):,.2f}",
            'TIME_COMPLETION': work_info.get('time_completion', '6 months'),
        }
        
        if l1_bidder:
            variables.update({
                'L1_BIDDER_NAME': l1_bidder.get('name', 'Unknown'),
                'L1_BID_AMOUNT': f"{l1_bidder.get('bid_amount', 0):,.2f}",
                'L1_PERCENTAGE': f"{l1_bidder.get('percentage', 0):.2f}%",
                'L1_BID_AMOUNT_WORDS': num2words(l1_bidder.get('bid_amount', 0), lang='en_IN').title().replace(' And ', ' ')
            })
        
        if bidders and isinstance(bidders, list):
            rows = [
                f"{i+1} & {bidder.get('name', 'Unknown')} & {bidder.get('estimated_cost', 0):,.2f} & {bidder.get('percentage', 0):.2f}\\% & {bidder.get('bid_amount', 0):,.2f} \\\\" 
                for i, bidder in enumerate(bidders)
            ]
            variables['BIDDER_TABLE_ROWS'] = '\n'.join(rows)
        else:
            variables['BIDDER_TABLE_ROWS'] = ''
            self.logger.warning("No valid bidders provided for table")
        
        return variables

    def _render_template(self, template_text: str, variables: dict) -> str:
        placeholder_keys = (
            'NIT_NUMBER|NIT_DATE|RECEIPT_DATE|OPENING_DATE|ITEM_NO|WORK_NAME|'
            'ESTIMATED_COST|EARNEST_MONEY|TIME_COMPLETION|BIDDER_TABLE_ROWS|'
            'L1_BIDDER_NAME|L1_BID_AMOUNT|L1_PERCENTAGE|L1_BID_AMOUNT_WORDS|'
            'START_DATE|COMPLETION_DATE'
        )
        pattern = re.compile(r"\{(" + placeholder_keys + r")\}")
        converted = pattern.sub(r"${\1}", template_text)
        return Template(converted).safe_substitute(variables)

    def convert_latex_to_html(self, latex_content):
        try:
            html_content = pypandoc.convert_text(
                latex_content, 'html', format='latex', extra_args=['--standalone', '--mathjax']
            )
            # Only write debug HTML if explicitly enabled
            if os.getenv('LATEX_DEBUG') == '1':
                with open('debug_output.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                self.logger.info("Saved debug HTML to debug_output.html")
            return html_content
        except Exception as e:
            self.logger.error(f"Error converting LaTeX to HTML: {str(e)}")
            raise

    def generate_pdf(self, html_content):
        try:
            pdf = weasyprint.HTML(string=html_content).write_pdf()
            return pdf
        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}")
            raise

    def generate_comparative_statement_pdf(self, work_data, bidders):
        template = self._load_template('latex_code_for_comparative_statement.TeX')
        variables = self._prepare_common_variables(work_data, min(bidders, key=lambda x: x.get('bid_amount', float('inf'))) if bidders else None, bidders)
        latex_content = self._render_template(template, variables)
        html_content = self.convert_latex_to_html(latex_content)
        return self.generate_pdf(html_content)

    def generate_letter_acceptance_pdf(self, work_data, l1_bidder):
        template = self._load_template('latex_code_for_letter_of_acceptance.tex')
        variables = self._prepare_common_variables(work_data, l1_bidder)
        latex_content = self._render_template(template, variables)
        html_content = self.convert_latex_to_html(latex_content)
        return self.generate_pdf(html_content)

    def generate_work_order_pdf(self, work_data, l1_bidder):
        template = self._load_template('latex_code_for_work_order.TeX')
        variables = self._prepare_common_variables(work_data, l1_bidder)
        start_date = self.date_utils.add_days(self.date_utils.get_current_datetime(), 2)
        completion_date = self.date_utils.add_months(start_date, int(work_data['work_info'].get('time_completion', '6 months').split()[0]))
        variables.update({
            'START_DATE': self.date_utils.format_display_date(start_date),
            'COMPLETION_DATE': self.date_utils.format_display_date(completion_date)
        })
        latex_content = self._render_template(template, variables)
        html_content = self.convert_latex_to_html(latex_content)
        return self.generate_pdf(html_content)

    def generate_scrutiny_sheet_pdf(self, work_data, bidders):
        template = self._load_template('latex_code_for_scrutiny_sheet.TeX')
        variables = self._prepare_common_variables(work_data, None, bidders)
        latex_content = self._render_template(template, variables)
        html_content = self.convert_latex_to_html(latex_content)
        return self.generate_pdf(html_content)

    def generate_bulk_pdfs(self, work_data, bidders):
        documents = {}
        try:
            work_id = work_data['work_info']['item_no']
            l1_bidder = min(bidders, key=lambda x: x.get('bid_amount', float('inf'))) if bidders else None
            documents[f'Comparative_Statement_Work_{work_id}'] = self.generate_comparative_statement_pdf(work_data, bidders)
            documents[f'Letter_of_Acceptance_Work_{work_id}'] = self.generate_letter_acceptance_pdf(work_data, l1_bidder)
            documents[f'Work_Order_Work_{work_id}'] = self.generate_work_order_pdf(work_data, l1_bidder)
            documents[f'Scrutiny_Sheet_Work_{work_id}'] = self.generate_scrutiny_sheet_pdf(work_data, bidders)
            return documents
        except Exception as e:
            self.logger.error(f"Error generating bulk PDFs: {str(e)}")
            raise