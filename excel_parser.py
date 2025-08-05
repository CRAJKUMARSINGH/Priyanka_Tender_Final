import pandas as pd
from datetime import datetime, timedelta

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

    def parse_nit_excel(self, file):
        """Parse statutory NIT Excel file."""
        try:
            # Read Excel file
            df = pd.read_excel(file, header=None)

            # Extract metadata from rows 1-4 (0-based indexing)
            nit_number = df.iloc[0, 2] if df.shape[1] > 2 else "Unknown"
            nit_date = self.excel_date_to_string(df.iloc[1, 2]) if df.shape[1] > 2 else "Unknown"
            receipt_date = self.excel_date_to_string(df.iloc[2, 2]) if df.shape[1] > 2 else "Unknown"
            opening_date = self.excel_date_to_string(df.iloc[3, 2]) if df.shape[1] > 2 else "Unknown"

            # Extract work data from rows 6+ (header at row 5, 0-based index 4)
            work_df = pd.read_excel(file, header=4, skiprows=0)
            works = []
            for _, row in work_df.iterrows():
                work_info = {
                    'item_no': str(row.get('ITEM NO.', '1')),
                    'work_name': str(row.get('NAME OF WORK', 'Unknown Work')),
                    'estimated_cost': float(row.get('ESTIMATED COST RS. IN LACS', 0) * 100000),
                    'g_schedule_amount': float(row.get('G-SCHEDULE AMOUNT RS', 0)),
                    'time_completion': str(row.get('TIME OF COMPLETION IN MONTH', '6 months')),
                    'earnest_money': float(row.get('EARNEST MONEY RS.', 0))
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

            return works  # Return list of work dictionaries
        except Exception as e:
            print(f"Error parsing NIT Excel: {str(e)}")
            raise