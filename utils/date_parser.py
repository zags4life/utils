# date_parser.py

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

DATE_FORMATS = (
    '%m-%d-%Y', 
    '%m-%d-%y',
    '%m/%d/%Y', 
    '%m/%d/%y',
    '%m%d%Y', 
    '%m%d%y',
    '%m/%d',
    '%m-%d',
    '%m%d',
    '%Y%m%d',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%y%m%d',
    )

def parse_date(date):
    if not date:
        return None

    for format in DATE_FORMATS:
        try:
            formatted = datetime.strptime(date, format)

            if formatted.year == 1900:
                formatted = datetime(
                    year=datetime.now().year,
                    month=formatted.month,
                    day=formatted.day)
            return formatted.date()
        except ValueError:
            pass
    logger.error("Failed to parse date '{}'".format(date))