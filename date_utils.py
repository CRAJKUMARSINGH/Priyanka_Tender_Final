from datetime import datetime, timedelta

class DateUtils:
    def get_current_date(self):
        """Return current date in DD-MM-YY format."""
        return datetime.now().strftime('%d-%m-%y')

    def get_current_datetime(self):
        """Return current datetime object."""
        return datetime.now()

    def parse_date(self, value: str):
        """Parse a date string into a datetime object using common formats."""
        if not value:
            return None
        # Try ISO first
        for fmt in ('%Y-%m-%d', '%d-%m-%y', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y', '%d/%m/%y'):
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                continue
        try:
            from dateutil.parser import parse as _parse
            return _parse(value)
        except Exception:
            return None

    def add_days(self, date_obj, days):
        """Add days to a datetime object."""
        return date_obj + timedelta(days=days)

    def add_months(self, date_obj, months):
        """Add months to a datetime object."""
        from dateutil.relativedelta import relativedelta
        return date_obj + relativedelta(months=months)

    def format_display_date(self, date_obj):
        """Format datetime object to DD-MM-YY."""
        return date_obj.strftime('%d-%m-%y')