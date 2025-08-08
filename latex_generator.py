"""
LaTeX Document Generator for Tender Processing System
Enhanced with professional templates integration
"""

import os
import re
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple

class LaTeXGenerator:
    """Enhanced LaTeX document generator with template integration."""
    
    def __init__(self):
        self.templates_dir = Path("latex_templates")
        self.output_dir = Path("generated_documents")
        self.output_dir.mkdir(exist_ok=True)
        
        # Ensure templates directory exists
        self.templates_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def number_to_words(self, amount: float) -> str:
        """Convert number to words for Indian currency format."""
        try:
            # Basic implementation for common amounts
            if amount == 0:
                return "Zero Rupees Only"
            
            # Convert to integer for simplicity
            rupees = int(amount)
            
            # Basic conversion (can be enhanced)
            ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
            teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", 
                    "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
            tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
            
            if rupees < 10:
                return f"{ones[rupees]} Rupees Only"
            elif rupees < 20:
                return f"{teens[rupees - 10]} Rupees Only"
            elif rupees < 100:
                return f"{tens[rupees // 10]} {ones[rupees % 10]} Rupees Only".strip()
            elif rupees < 1000:
                hundreds = rupees // 100
                remainder = rupees % 100
                result = f"{ones[hundreds]} Hundred"
                if remainder > 0:
                    if remainder < 10:
                        result += f" {ones[remainder]}"
                    elif remainder < 20:
                        result += f" {teens[remainder - 10]}"
                    else:
                        result += f" {tens[remainder // 10]} {ones[remainder % 10]}".strip()
                return f"{result} Rupees Only"
            elif rupees < 100000:
                thousands = rupees // 1000
                remainder = rupees % 1000
                result = f"{self._convert_hundreds(thousands)} Thousand"
                if remainder > 0:
                    result += f" {self._convert_hundreds(remainder)}"
                return f"{result} Rupees Only"
            elif rupees < 10000000:
                lakhs = rupees // 100000
                remainder = rupees % 100000
                result = f"{self._convert_hundreds(lakhs)} Lakh"
                if remainder > 0:
                    if remainder >= 1000:
                        result += f" {self._convert_hundreds(remainder // 1000)} Thousand"
                        remainder = remainder % 1000
                    if remainder > 0:
                        result += f" {self._convert_hundreds(remainder)}"
                return f"{result} Rupees Only"
            else:
                crores = rupees // 10000000
                remainder = rupees % 10000000
                result = f"{self._convert_hundreds(crores)} Crore"
                if remainder > 0:
                    if remainder >= 100000:
                        result += f" {self._convert_hundreds(remainder // 100000)} Lakh"
                        remainder = remainder % 100000
                    if remainder >= 1000:
                        result += f" {self._convert_hundreds(remainder // 1000)} Thousand"
                        remainder = remainder % 1000
                    if remainder > 0:
                        result += f" {self._convert_hundreds(remainder)}"
                return f"{result} Rupees Only"
        except Exception as e:
            self.logger.error(f"Error converting number to words: {e}")
            return f"Rupees {amount:.2f} Only"
    
    def _convert_hundreds(self, num: int) -> str:
        """Helper method to convert numbers less than 1000 to words."""
        if num == 0:
            return ""
        
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", 
                "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        
        result = ""
        
        if num >= 100:
            result += f"{ones[num // 100]} Hundred "
            num %= 100
        
        if num >= 20:
            result += f"{tens[num // 10]} "
            num %= 10
        elif num >= 10:
            result += f"{teens[num - 10]} "
            num = 0
        
        if num > 0:
            result += f"{ones[num]} "
        
        return result.strip()
    
    def generate_bidder_table_rows(self, bidders: List[Dict], estimated_cost: float) -> str:
        """Generate bidder table rows for LaTeX."""
        rows = []
        for i, bidder in enumerate(bidders, 1):
            name = bidder.get('name', 'Unknown')
            percentage = bidder.get('percentage', 0)
            bid_amount = bidder.get('bid_amount', 0)
            
            # Escape LaTeX special characters
            name = self.escape_latex(name)
            
            row = f"{i} & {name} & {estimated_cost:,.2f} & {percentage:+.2f}\\% & {bid_amount:,.2f} \\\\"
            rows.append(row)
        
        return "\n        ".join(rows)
    
    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        # Basic LaTeX character escaping
        replacements = {
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '^': '\\^{}',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '\\': '\\textbackslash{}'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def prepare_template_data(self, work_data: Dict, bidders: List[Dict]) -> Dict[str, str]:
        """Prepare data dictionary for template substitution."""
        if not work_data or not bidders:
            raise ValueError("Work data and bidders information required")
        
        # Sort bidders by bid amount to find L1
        sorted_bidders = sorted(bidders, key=lambda x: x.get('bid_amount', float('inf')))
        l1_bidder = sorted_bidders[0]
        
        # Generate dates
        current_date = datetime.now().strftime("%d-%m-%Y")
        receipt_date = work_data.get('work_info', {}).get('date', current_date)
        validity_date = (datetime.now() + timedelta(days=20)).strftime("%d-%m-%Y")
        start_date = (datetime.now() + timedelta(days=7)).strftime("%d-%m-%Y")
        completion_days = int(work_data.get('work_info', {}).get('time_of_completion', '90').split()[0])
        completion_date = (datetime.now() + timedelta(days=completion_days + 7)).strftime("%d-%m-%Y")
        
        # Prepare template data
        template_data = {
            'WORK_NAME': self.escape_latex(work_data.get('work_name', 'Unknown Work')),
            'NIT_NUMBER': self.escape_latex(work_data.get('nit_number', 'Unknown NIT')),
            'NIT_DATE': receipt_date,
            'ITEM_NO': '1',
            'ESTIMATED_COST': f"{work_data.get('work_info', {}).get('estimated_cost', 0):,.2f}",
            'EARNEST_MONEY': f"{work_data.get('work_info', {}).get('earnest_money', 0):,.2f}",
            'TIME_COMPLETION': work_data.get('work_info', {}).get('time_of_completion', '90 days'),
            'RECEIPT_DATE': receipt_date,
            'L1_BIDDER_NAME': self.escape_latex(l1_bidder.get('name', 'Unknown')),
            'L1_BIDDER_ADDRESS': self.escape_latex(l1_bidder.get('address', 'Unknown Address')),
            'L1_PERCENTAGE': f"{l1_bidder.get('percentage', 0):+.2f}\\%",
            'L1_BID_AMOUNT': f"{l1_bidder.get('bid_amount', 0):,.2f}",
            'L1_BID_AMOUNT_WORDS': self.number_to_words(l1_bidder.get('bid_amount', 0)),
            'BIDDER_TABLE_ROWS': self.generate_bidder_table_rows(bidders, work_data.get('work_info', {}).get('estimated_cost', 0)),
            'NUM_TENDERS_SOLD': str(len(bidders) + 2),
            'NUM_TENDERS_RECEIVED': str(len(bidders)),
            'VALIDITY_DATE': validity_date,
            'CURRENT_DATE': current_date,
            'AGREEMENT_NO': f"AGR/{work_data.get('nit_number', 'UNKNOWN')}/{datetime.now().year}",
            'START_DATE': start_date,
            'COMPLETION_DATE': completion_date
        }
        
        return template_data
    
    def load_template(self, template_name: str) -> str:
        """Load LaTeX template from file."""
        template_path = self.templates_dir / f"{template_name}.tex"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error loading template {template_name}: {e}")
            raise
    
    def substitute_template(self, template_content: str, data: Dict[str, str]) -> str:
        """Substitute placeholders in template with actual data."""
        result = template_content
        
        for placeholder, value in data.items():
            pattern = f"{{{placeholder}}}"
            result = result.replace(pattern, str(value))
        
        return result
    
    def generate_document(self, template_name: str, work_data: Dict, bidders: List[Dict], output_filename: Optional[str] = None) -> Tuple[str, str]:
        """Generate a complete LaTeX document from template."""
        try:
            # Load template
            template_content = self.load_template(template_name)
            
            # Prepare data
            template_data = self.prepare_template_data(work_data, bidders)
            
            # Substitute placeholders
            document_content = self.substitute_template(template_content, template_data)
            
            # Generate output filename if not provided
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{template_name}_{timestamp}.tex"
            
            # Save generated document
            output_path = self.output_dir / output_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(document_content)
            
            self.logger.info(f"Generated LaTeX document: {output_path}")
            return str(output_path), document_content
            
        except Exception as e:
            self.logger.error(f"Error generating document {template_name}: {e}")
            raise
    
    def compile_to_pdf(self, tex_file_path: str) -> Optional[str]:
        """Compile LaTeX file to PDF using pdflatex."""
        try:
            tex_path = Path(tex_file_path)
            if not tex_path.exists():
                raise FileNotFoundError(f"LaTeX file not found: {tex_file_path}")
            
            # Create temporary directory for compilation
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy tex file to temp directory
                temp_tex = temp_path / tex_path.name
                temp_tex.write_text(tex_path.read_text(encoding='utf-8'), encoding='utf-8')
                
                # Compile with pdflatex
                cmd = [
                    'pdflatex',
                    '-interaction=nonstopmode',
                    '-output-directory', str(temp_path),
                    str(temp_tex)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_path)
                
                if result.returncode == 0:
                    # Move PDF to output directory
                    pdf_name = tex_path.stem + '.pdf'
                    temp_pdf = temp_path / pdf_name
                    output_pdf = self.output_dir / pdf_name
                    
                    if temp_pdf.exists():
                        output_pdf.write_bytes(temp_pdf.read_bytes())
                        self.logger.info(f"PDF generated successfully: {output_pdf}")
                        return str(output_pdf)
                    else:
                        self.logger.error("PDF file not generated")
                        return None
                else:
                    self.logger.error(f"LaTeX compilation failed: {result.stderr}")
                    return None
                    
        except FileNotFoundError:
            self.logger.warning("pdflatex not found. Install LaTeX distribution for PDF generation.")
            return None
        except Exception as e:
            self.logger.error(f"Error compiling PDF: {e}")
            return None
    
    def generate_all_documents(self, work_data: Dict, bidders: List[Dict]) -> Dict[str, Dict[str, str]]:
        """Generate all standard tender documents."""
        results = {}
        
        document_types = [
            'comparative_statement',
            'letter_of_acceptance', 
            'scrutiny_sheet',
            'work_order'
        ]
        
        for doc_type in document_types:
            try:
                tex_path, content = self.generate_document(doc_type, work_data, bidders)
                pdf_path = self.compile_to_pdf(tex_path)
                
                results[doc_type] = {
                    'tex_path': tex_path,
                    'pdf_path': pdf_path or 'PDF generation failed',
                    'content': content,
                    'status': 'success' if pdf_path else 'tex_only'
                }
                
            except Exception as e:
                self.logger.error(f"Error generating {doc_type}: {e}")
                results[doc_type] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def get_generated_files(self) -> List[Dict[str, str]]:
        """Get list of all generated files."""
        files = []
        
        for file_path in self.output_dir.iterdir():
            if file_path.is_file():
                files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'type': file_path.suffix[1:],
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    
    def cleanup_old_files(self, days_old: int = 7):
        """Clean up generated files older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for file_path in self.output_dir.iterdir():
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        self.logger.info(f"Cleaned up old file: {file_path.name}")
                    except Exception as e:
                        self.logger.error(f"Error cleaning up {file_path.name}: {e}")