import pandas as pd
import logging
import traceback
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any, Optional, Union
import os
import json
from dateutil.parser import parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('excel_parser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ExcelParser:
    def __init__(self):
        self.excel_epoch = datetime(1899, 12, 30)  # Excel date origin (adjusted for Excel's leap year bug)

    def excel_date_to_string(self, excel_date):
        """Convert Excel serial date to DD-MM-YY string."""
        try:
            if isinstance(excel_date, (int, float)):
                date = self.excel_epoch + timedelta(days=excel_date)
                return date.strftime('%d-%m-%y')
            return str(excel_date)
        except Exception as e:
            print(f"Error converting Excel date {excel_date}: {str(e)}")
            return str(excel_date)

    def parse_nit_excel(self, file_path):
        """
        Parse statutory NIT Excel file.
        
        Args:
            file_path (str): Path to the Excel file to parse
            
        Returns:
            list: List of work dictionaries with parsed data
            
        Raises:
            Exception: If there's an error parsing the Excel file
        """
        logger.info(f"Starting to parse NIT Excel file: {file_path}")
        
        try:
            # Read Excel file with error handling
            logger.info("Reading Excel file...")
            try:
                df = pd.read_excel(file_path, header=None, engine='openpyxl')
                logger.info(f"Excel file read successfully. Shape: {df.shape}")
            except Exception as e:
                logger.error(f"Failed to read Excel file: {str(e)}\n{traceback.format_exc()}")
                raise ValueError("Failed to read the Excel file. Please ensure it's a valid Excel file.")
            
            if df.empty:
                error_msg = "The uploaded Excel file is empty"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
            # Log first few rows for debugging
            logger.debug(f"First 5 rows of raw data:\n{df.head().to_string()}")

            # Extract metadata from rows 1-4 (0-based indexing)
            try:
                nit_number = str(df.iloc[0, 2]) if df.shape[1] > 2 else "Unknown"
                nit_date = self.excel_date_to_string(df.iloc[1, 2]) if df.shape[1] > 2 else "Unknown"
                receipt_date = self.excel_date_to_string(df.iloc[2, 2]) if df.shape[1] > 2 else "Unknown"
                opening_date = self.excel_date_to_string(df.iloc[3, 2]) if df.shape[1] > 2 else "Unknown"
                
                logger.info(f"Extracted metadata - NIT: {nit_number}, Date: {nit_date}")
                logger.info(f"Receipt Date: {receipt_date}, Opening Date: {opening_date}")
                
            except Exception as meta_error:
                error_msg = f"Error extracting metadata: {str(meta_error)}"
                logger.error(f"{error_msg}\n{traceback.format_exc()}")
                raise ValueError("Error reading NIT metadata. Please ensure the Excel file has the correct format with metadata in the first 4 rows.")

            # Extract work data from rows 6+ (header at row 5, 0-based index 4)
            works = []
            try:
                logger.info("Reading work data from Excel...")
                work_df = pd.read_excel(file_path, header=4, engine='openpyxl')
                logger.info(f"Work data read successfully. Shape: {work_df.shape}")
                
                if work_df.empty:
                    error_msg = "No work data found in the Excel file"
                    logger.error(error_msg)
                    raise ValueError("No work data found. Please ensure the Excel file contains work items starting from row 6.")
                
                # Log column names for debugging
                logger.info(f"Available columns: {work_df.columns.tolist()}")
                
                for idx, row in work_df.iterrows():
                    try:
                        work_info = {
                            'item_no': str(row.get('ITEM NO.', row.get('ITEM NO', str(idx + 1)))),
                            'work_name': str(row.get('NAME OF WORK', row.get('WORK NAME', f'Work {idx + 1}'))),
                            'estimated_cost': float(str(row.get('ESTIMATED COST RS. IN LACS', '0')).replace(',', '')) * 100000,
                            'g_schedule_amount': float(str(row.get('G-SCHEDULE AMOUNT RS', '0')).replace(',', '')),
                            'time_completion': str(row.get('TIME OF COMPLETION IN MONTH', '6 months')),
                            'earnest_money': float(str(row.get('EARNEST MONEY RS.', '0')).replace(',', ''))
                        }
                        
                        works.append({
                            'work_info': {
                                'nit_number': nit_number,
                                'nit_date': nit_date,
                                'receipt_date': receipt_date,
                                'opening_date': opening_date,
                                **work_info
                            }
                        })
                        
                        logger.debug(f"Processed work item {idx + 1}: {work_info['work_name']}")
                        
                    except Exception as work_error:
                        logger.error(f"Error processing row {idx + 1}: {str(work_error)}\n{traceback.format_exc()}")
                        continue  # Skip this row but continue with others
                
                if not works:
                    error_msg = "No valid work items found in the Excel file"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                    
                logger.info(f"Successfully parsed {len(works)} work items from NIT document")
                return works
                
            except Exception as work_data_error:
                logger.error(f"Error processing work data: {str(work_data_error)}\n{traceback.format_exc()}")
                raise ValueError("Error processing work data. Please check the Excel file format and try again.")
                
        except Exception as e:
            logger.error(f"Unexpected error in parse_nit_excel: {str(e)}\n{traceback.format_exc()}")
            raise