from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DateFormat(Enum):
    """Date/Time format definitions."""
    HH24MI = "%H%M"
    HH24MISS = "%H%M%S"
    YYYYMM = "%Y%m"
    YYYYMMDD = "%Y%m%d"
    YYYYMMDD2 = "%Y/%m/%d"
    YYYYMMDDHH24MI = "%Y%m%d%H%M"
    YYYYMMDDHH24MISS = "%Y%m%d%H%M%S"
    YYYYMMDDHH24MISSMS = "%Y%m%d%H%M%S%f"


class DateUtil:
    """Common Utility for Date/Time operations."""

    @classmethod
    def JST(cls) -> timezone:
        """Retrieve Japan Standard Time (JST) timezone.

        Returns:
            timezone: JST timezone.
        """
        return timezone(timedelta(hours=+9), 'JST')
 
 
    @classmethod
    def jst_now(cls) -> datetime:
        """Retrieve current time in Japan Standard Time (JST).

        Returns:
            datetime: Current JST time.
        """
        return datetime.now(tz=cls.JST())


    @classmethod
    def jst_dt_str(cls, fmt: DateFormat = DateFormat.YYYYMMDD) -> str:
        """Format current JST time.

        Args:
            fmt (DateFormat, optional): Time format. Defaults to YYYYMMDD.

        Returns:
            str: Formatted current JST time as string.
        """
        return cls.jst_now().strftime(fmt.value)


    @classmethod
    def conv_to_ampm(cls, in_value: str) -> str:
        """Convert HH24MM time string to AM/PM format.
        Converts 0000~1159 to AM, 1200~2359 to PM.

        Args:
            in_value (str): Time string in HH24MM format.

        Returns:
            str: Time in 'AM/PM HH時MM分' format.
        """
        # 1. Convert string to time, raise error if invalid.
        tar_tm: datetime = datetime.strptime(in_value, DateFormat.HH24MI)

        # 2. Extract the first two digits (hours) and convert to integer.
        hh_out: str = int(in_value[:2])
        hh_in: int = hh_out
        apmp: str = "AM"

        if hh_in >= 12:
            # 3. If hour is 12 or above, convert to PM, subtract 12 from the hour.
            apmp = "PM"
            hh_out = str(hh_in - 12)

        return f'{apmp}{hh_out}時{int(tar_tm.strftime("%M"))}分'


    @classmethod
    def conv_fiscal_year(cls, date: datetime = None) -> int:
        """Retrieve the fiscal year.
        Returns the same year for dates in April-December, and the previous year for dates in January-March.

        Args:
            date (datetime): Date to get fiscal year from. Defaults to current JST date if omitted.

        Returns:
            int: Fiscal year.
        """
        # Use current JST time if date is not provided.
        if date is None:
            date = cls.jst_now()
        if date.month in {1, 2, 3}:
            return date.year - 1
        else:
            return date.year


    @classmethod
    def extract_day(cls, date_string) -> int:
        """Parse the day from a date string."""
        try:
            date_formats = ['%Y%m%d', '%Y/%m/%d', '%Y-%m-%d']
            for date_format in date_formats:
                try:
                    date_obj = datetime.strptime(date_string, date_format)
                    return int(date_obj.day)
                except ValueError:
                    pass
            raise ValueError("Invalid date format")
        except Exception as e:
            return 0


    @classmethod
    def modify_date(cls, date_string, months=0, days=0, dateformat='%Y/%m/%d') -> str:
        """Modify a date by adding/subtracting months and/or days.

        Args:
            date_string (str): Input date string.
            months (int): Optional months to add/subtract. Defaults to 0.
            days (int): Optional days to set. Defaults to 0.
            dateformat (str): Optional output date format. Defaults to '%Y/%m/%d'.

        Returns:
            str: Modified date in specified format.
        """
        try:
            # Try to parse the date string with different formats.
            date_formats = ['%Y%m%d', '%Y/%m/%d', '%Y-%m-%d']
            for date_format in date_formats:
                try:
                    # Parse the date string using the given format.
                    date_obj = datetime.strptime(date_string, date_format)
                    # Add/subtract months and days as specified.
                    modified_date = date_obj
                    if days != 0:
                        modified_date = modified_date.replace(day=days)  # Reset day to 1 and apply changes to months.

                    if months != 0:
                        modified_date += relativedelta(months=months)
                    return modified_date.strftime(dateformat)
                except ValueError:
                    pass
            # Raise error if the date string cannot be parsed.
            raise ValueError("Invalid date format")
        except Exception as e:
            logger.exception("DateUtil.modify_date failed")
            return None
