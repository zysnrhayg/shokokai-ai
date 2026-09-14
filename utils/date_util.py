#DateUtil.vm
from datetime import datetime, timezone, timedelta
import calendar
import pytz
import locale
import random
import logging

logger = logging.getLogger(__name__)
def getSystemYearMonth():
    return datetime.now().strftime("%Y/%m")
def getSystemToday ():
    return datetime.now().strftime("%Y/%m/%d")
    
def getYear() -> int:
    return datetime.now().year

def getMonth() -> int:
    return datetime.now().month

def getMonthFromDate(d: str) -> int:
    date = datetime.strptime(d, "%Y/%m/%d")
    return date.month

def getWeekday() -> str:
    weekdays = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
    return weekdays[datetime.now().weekday()]

def getHeaderTodayDisplay() -> str:
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    today = datetime.now()
    return today.strftime("%Y/%m/%d") + "（" + weekdays[today.weekday()] + "）"

def getDay() -> int:
    return datetime.now().day

def getHour () -> int:
    return datetime.now().hour

def getMinute() -> int:
    return datetime.now().minute

def getSecond() -> int:
    return datetime.now().second

def getMilliSecond() -> int:
    return int(datetime.now().timestamp() * 1000)


ONE_DAY_SEC = 86400
ONE_HOUR_SEC = 3600
ONE_MINUTE_SEC = 60

#string fomat convert to date format
def parse_date(date_str: str, date_format: str = "%Y/%m/%d") -> datetime:
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        try:
            return  datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None
#日付比較 date1　> date2で場合はTrueを戻す
def after(date1: str, date2: str) -> bool:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return d1 > d2
    return False

def before(date1: str, date2: str) -> bool:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return d1 < d2
    return False

def equals(date1: str, date2: str) -> bool:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return d1 == d2
    return False

def diffYear(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs(d1.year - d2.year)
    return -1

def diffMonth(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)
    return -1

def diffDay(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs((d1 - d2).days)
    return -1

def diffHour(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs(int((d1 - d2).total_seconds() / ONE_HOUR_SEC))
    return -1

def diffMinute(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs(int((d1 - d2).total_seconds() / ONE_MINUTE_SEC))
    return -1

def diffSecond(time1: str, time2: str) -> int:
    t1 = parse_date(time1, "%H:%M:%S")
    t2 = parse_date(time2, "%H:%M:%S")
    if t1 and t2:
        return abs(int((t1 - t2).total_seconds()))
    return -1

def getDiffForNow(dtm1: str) -> str:
    if not dtm1:
        return ""
    d1 = parse_date(dtm1)
    if not d1:
        return ""
    d2 = datetime.now(pytz.timezone("Asia/Tokyo"))
    if d1 > d2:
        return ""
    delta = (d2 - d1).total_seconds() / ONE_MINUTE_SEC
    if delta < 60:
        return f"{int(delta)}m"
    elif delta < 60 * 24:
        return f"{int(delta // 60)}h"
    else:
        return f"{int(delta // (60 * 24))}d"


ONE_DAY_SEC = 86400  # Number of seconds in one day

def parse_time(time_str: str, time_format: str = "%H:%M:%S") -> datetime:
    try:
        return datetime.strptime(time_str, time_format).time()
    except ValueError:
        return ""

def getSecond(time: str) -> int:
    return diff_second(time, "00:00:00")

def diff_second(time1: str, time2: str) -> int:
    t1 = parse_time(time1)
    t2 = parse_time(time2)
    if t1 and t2:
        # Convert time to timedelta from midnight
        t1_seconds = t1.hour * 3600 + t1.minute * 60 + t1.second
        t2_seconds = t2.hour * 3600 + t2.minute * 60 + t2.second
        return abs(t1_seconds - t2_seconds)
    return -1


def diffDayValue(date1: str, date2: str) -> int:
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    if d1 and d2:
        return abs((d1 - d2).days)
    return -1


def get_db_date_time(dt: datetime) -> str:
    return dt.strftime("%Y/%m/%d %H:%M:%S")

def DateAddHour(amount: int) -> str:
    dt = datetime.now() + timedelta(hours=amount)
    return get_db_date_time(dt)

def DateAddSecond(seconds: int) -> str:
    dt = datetime.now() + timedelta(seconds=seconds)
    return get_db_date_time(dt)

def date_add_unit(date_str: str, pattern: str, field: str, amount: int) -> datetime:
    dt = datetime.strptime(date_str, pattern)
    if field == 'H':
        return dt + timedelta(hours=amount)
    elif field == 'S':
        return dt + timedelta(seconds=amount)
    else:
        raise ValueError("Unsupported field")

def getHourAgo(h) :
	now = datetime.datetime.now()
	one_hour = datetime.timedelta(hours=h)
	one_hour_ago = now - one_hour
	return one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

def getHourAfter(h) :
	now = datetime.datetime.now()
	one_hour = datetime.timedelta(hours=h)
	one_hour_after = now + one_hour
	return one_hour_after.strftime("%Y-%m-%d %H:%M:%S")

def getMinuteAgo(m) :
	now = datetime.datetime.now()
	one_minute = datetime.timedelta(minutes=m)
	one_minute_ago  = now - one_minute
	return one_minute_ago.strftime("%Y-%m-%d %H:%M:%S")

def getMinuteAfter(m) :
	now = datetime.datetime.now()
	one_minute = datetime.timedelta(minutes=m)
	one_minute_after  = now + one_minute
	return one_minute_after.strftime("%Y-%m-%d %H:%M:%S")

def getSecondsAgo(s) :
	now = datetime.datetime.now()
	one_second  = datetime.timedelta(seconds=s)
	one_second_ago   = now - one_second 
	return one_second_ago .strftime("%Y-%m-%d %H:%M:%S")


def get_next_month_rd(d):
  today = datetime.date.today()
  if today.month == 12:
    next_month = 1
    next_year = today.year + 1
  else:
    next_month = today.month + 1
    next_year = today.year

  try:
    next_month_3rd = datetime.date(next_year, next_month, d)
    return next_month_3rd
  except ValueError:
    if next_month == 2:
      return datetime.date(next_year, next_month, 28)  
    elif next_month in [4, 6, 9, 11]:
      return datetime.date(next_year, next_month, 30)
    else:
      return datetime.date(next_year, next_month, 31)
      
def getSecondsAfter(s) :
	now = datetime.datetime.now()
	one_second  = datetime.timedelta(seconds=s)
	one_second_after   = now + one_second 
	return one_second_after .strftime("%Y-%m-%d %H:%M:%S")
					
def getFirstDayFromYM(year: str, month: str) -> str:
    month = month.zfill(2)
    return f"{year}/{month}/01"

def getFirstDayFromDate(date_value: str, pattern_ori: str) -> str:
    if not date_value:
        return ""
    try:
        dt = datetime.strptime(date_value, pattern_ori)
        return dt.strftime("%Y/%m") + "/01"
    except ValueError:
        return ""

def getFirstDayFromDateUnit(pattern_ori: str, count: int, lang_id: str) -> str:
    today = datetime.now()
    if pattern_ori == "year":
        first_day = today.replace(year=today.year + count, month=1, day=1)
    elif pattern_ori == "month":
        first_day = today.replace(month=today.month + count, day=1)
    elif pattern_ori == "week":
        if lang_id == "JPN":
            first_weekday = calendar.SUNDAY
        else:
            first_weekday = calendar.MONDAY
        weekday = (today.weekday() + 1) % 7  # Adjust for Sunday start if needed
        days_to_first_weekday = (first_weekday - weekday) % 7
        first_day = today + timedelta(days=days_to_first_weekday)
        first_day = first_day + timedelta(weeks=count)
    else:
        raise ValueError("Unsupported pattern_ori")

    return first_day.strftime("%Y/%m/%d")



def getLastDayOfMonth(year: int, month: int, day: int) -> str:
    dt = datetime(year, month, day)
    # Get the last day of the month
    last_day = (dt.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    return last_day.strftime("%Y-%m-%d")

def getLasttDayFromDate(pattern_ori: str, count: int, lang_id: str) -> str:
    now = datetime.now()
    if pattern_ori == "year":
        # Year
        end_of_year = now.replace(year=now.year + count + 1, month=1, day=1) - timedelta(days=1)
        return end_of_year.strftime("%Y/%m/%d")
    elif pattern_ori == "month":
        # Month
        end_of_month = now.replace(month=now.month + count + 1, day=1) - timedelta(days=1)
        return end_of_month.strftime("%Y/%m/%d")
    elif pattern_ori == "week":
        # Week
        first_weekday = calendar.SUNDAY if lang_id != "CHN" else calendar.MONDAY
        last_weekday = calendar.SATURDAY if lang_id != "CHN" else calendar.SUNDAY
        weekday = (now.weekday() + 1) % 7  # Adjust for Sunday start if needed
        days_to_week_start = (first_weekday - weekday) % 7
        week_start = now + timedelta(days=days_to_week_start)
        week_end = week_start + timedelta(weeks=count) - timedelta(days=1)
        return week_end.strftime("%Y/%m/%d")
    else:
        raise ValueError("Unsupported pattern_ori")

def getPatternDateStr(str_pattern):
    if str_pattern == "yyyy-MM-dd HH:mm:ss":
        str_pattern = "%Y-%m-%d %H:%M:%S"
    return datetime.now().strftime(str_pattern)

def getPatternDatelocale(str_pattern: str, locale_name: str) -> str:
    # Note: Python's locale module may not directly support formatting dates.
    # This is a placeholder for handling locale-specific formats if needed.
    locale.setlocale(locale.LC_TIME, locale_name)
    return datetime.now().strftime(str_pattern)

def getPatternDateForDb():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getPatternDateWeekForDb():
    week_names = ["月", "火", "水", "木", "金", "土", "日"]
    now = datetime.now()
    return now.strftime("%Y/%m/%d") + " (" + week_names[now.weekday()] + ")"


def getPatternDateTimeWeekForDb():
    week_names = ["月", "火", "水", "木", "金", "土", "日"]
    now = datetime.now()
    return now.strftime("%Y/%m/%d") + " (" + week_names[now.weekday()] + ") " + now.strftime("%H:%M:%S")

from datetime import datetime, timedelta, date as _date
import locale
import re

# 画面日付（date picker 等）
FORM_DATE_JAVA_PATTERN = "yyyy/MM/dd"
# 画面日時（保存校验 M250 tourokunichiji 等: yyyy/MM/ddTHH:mm:ss）
FORM_DATETIME_JAVA_PATTERN = "yyyy/MM/dd'T'HH:mm:ss"

# DB / TO_CHAR / API から返る日付文字列の代表的入力形式
_INPUT_DATE_FORMATS = (
	"%Y-%m-%d %H:%M:%S.%f",
	"%Y-%m-%d %H:%M:%S",
	"%Y-%m-%d",
	"%Y/%m/%d %H:%M:%S.%f",
	"%Y/%m/%d %H:%M:%S",
	"%Y/%m/%d %H:%M",
	"%Y/%m/%dT%H:%M:%S",
	"%Y/%m/%d",
)


def java_pattern_to_strftime(java_pattern: str) -> str:
	"""Java SimpleDateFormat 形式 (yyyy/MM/dd、'T' リテラル等) を Python strftime 形式へ変換。"""
	if not java_pattern:
		return "%Y/%m/%d"
	if java_pattern.startswith("%"):
		return java_pattern
	# Java の引用符リテラル: 'T' → T
	result = re.sub(r"'([^']*)'", r"\1", java_pattern)
	for java_token, py_token in (
		("yyyy", "%Y"), ("YYYY", "%Y"),
		("MM", "%m"), ("dd", "%d"),
		("HH", "%H"), ("mm", "%M"), ("ss", "%S"),
	):
		result = result.replace(java_token, py_token)
	return result


def parse_flexible_datetime(date_value):
	"""DB・TO_CHAR・Python 由来の日付/日時を datetime に正規化。解析不能時は None。"""
	if date_value is None:
		return None
	if isinstance(date_value, datetime):
		return date_value
	if isinstance(date_value, _date):
		return datetime.combine(date_value, datetime.min.time())
	text = str(date_value).strip()
	if not text or text.lower() == "none":
		return None
	if len(text) == 8 and text.isdigit():
		try:
			return datetime.strptime(text, "%Y%m%d")
		except ValueError:
			pass
	for fmt in _INPUT_DATE_FORMATS:
		try:
			return datetime.strptime(text, fmt)
		except ValueError:
			continue
	return None


def format_display_date(date_value, output_pattern="yyyy/MM/dd") -> str:
	"""
	画面表示用の共通日付フォーマット。
	入力は複数形式を自動判定し、output_pattern (Java 形式) で出力する。
	"""
	dt = parse_flexible_datetime(date_value)
	if dt is None:
		return ""
	try:
		return dt.strftime(java_pattern_to_strftime(output_pattern))
	except (ValueError, TypeError):
		logger.exception("format_display_date failed for pattern %s", output_pattern)
		return ""


def format_form_date(date_value) -> str:
	"""画面日付フィールド用（yyyy/MM/dd）。"""
	return format_display_date(date_value, FORM_DATE_JAVA_PATTERN)


def format_form_datetime(date_value) -> str:
	"""画面日時フィールド用（yyyy/MM/ddTHH:mm:ss）。保存校验と同一形式。"""
	return format_display_date(date_value, FORM_DATETIME_JAVA_PATTERN)


def normalize_form_datetime(date_value) -> str:
	"""日付のみ入力も可。保存/API 前に canonical 日時文字列へ正規化。"""
	return format_form_datetime(date_value)


def get_patterndate(date_value, str_pattern="yyyy/MM/dd"):
	"""後方互換ラッパー。str_pattern は Java 形式の出力パターン。"""
	return format_display_date(date_value, str_pattern or "yyyy/MM/dd")
	
def getPatternDate(date_value, str_pattern):
    if not date_value:
        return ""
    try:
        if str_pattern == "yyyy-MM-dd" :
            if date_value.find("/") != -1 :
               date_value =  date_value.replace('/','-')
            if len(date_value) == 8 :
               year = date_value[:4]
               month = date_value[4:6]
               day = date_value[6:]
               date_value =  f'{year}-{month}-{day}'
            dt = datetime.strptime(date_value, "%Y-%m-%d")
            return  dt.strftime(date_value)
        dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")  # Adjust this format as needed
        return dt.strftime(date_value)
    except Exception as e:
       logger.exception("getPatternDate failed")
       return None


def get_pattern_datetime(date_value: str, str_pattern: str) -> str:
	return format_display_date(date_value, str_pattern)

def get_pattern_time(date_value: str, str_pattern: str) -> str:
    if not date_value:
        return ""
    try:
        dt = datetime.strptime(date_value, "%H:%M:%S")  # Adjust this format as needed
        return dt.strftime(str_pattern)
    except ValueError:
        return ""

def get_pattern_date_from_calendar(date_value: datetime, str_pattern: str) -> str:
    if date_value is None:
        return ""
    return date_value.strftime(str_pattern)

def get_current_date(days: int, str_pattern: str) -> str:
    now = datetime.now() + timedelta(days=days)
    return now.strftime(str_pattern)

def get_base_date(date: str, months: int, str_pattern: str) -> str:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")  # Adjust this format as needed
        new_date = dt + timedelta(days=months * 30)  # Approximate month length
        return new_date.strftime(str_pattern)
    except ValueError:
        return ""

def add_date(date: str, days: int, str_pattern: str) -> str:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")  # Adjust this format as needed
        new_date = dt + timedelta(days=days)
        return new_date.strftime(str_pattern)
    except ValueError:
        return date

def add_month(date: str, months: int, str_pattern: str) -> str:
    try:
        if date.find("/") != -1 :
            date =  date.replace('/','-')
        if len(date) == 8 :
            year = date[:4]
            month = date[4:6]
            day = date[6:]
            date =  f'{year}-{month}-{day}'    
        
        dt = datetime.strptime(date, "%Y-%m-%d")  # Adjust this format as needed
        new_month = (dt.month - 1 + months) % 12 + 1
        new_year = dt.year + (dt.month - 1 + months) // 12
        new_date = dt.replace(year=new_year, month=new_month)
        return new_date.strftime(str_pattern)
    except ValueError:
        return date

def add_year(date: str, years: int, str_pattern: str) -> str:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")  # Adjust this format as needed
        new_date = dt.replace(year=dt.year + years)
        return new_date.strftime(str_pattern)
    except ValueError:
        return date

def get_db_pattern_datetime() -> str:
    return get_pattern_date(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "yyyy/MM/dd HH:mm:ss")

def getDBPatternDate() -> str:
    date_value = datetime.now().strftime("%Y-%m-%d")
    str_pattern = "yyyy/MM/dd"
    if not date_value:
        return ""
    try:
        dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")  # Adjust this format as needed
        return dt.strftime(str_pattern)
    except ValueError:
        return date_value

def get_pattern_datetime1(v: str) -> str:
    return get_pattern_date(v, "%Y/%m/%d %H:%M")

def get_pattern_datetime2(v: str) -> str:
    return get_pattern_date(v, "%m/%d %H:%M")

def get_pattern_datetime3(v: str) -> str:
    return get_pattern_date(v, "%m/%d")

def get_lang_datetime1(language_id: str, v: str) -> str:
    pattern = "yyyy年m月d日 HH:mm"  # Example pattern; adjust as needed
    return get_pattern_date(v, pattern)

def get_lang_datetime2(language_id: str, v: str) -> str:
    pattern = "yyyy年m月d日"  # Example pattern; adjust as needed
    return get_pattern_date(v, pattern)

def get_lang_datetime3(language_id: str, v: str) -> str:
    pattern = "m月d日"  # Example pattern; adjust as needed
    return get_pattern_date(v, pattern)

def get_std_pattern_date() -> str:
    return get_pattern_date(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")

def get_timestamp_pattern_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")[:-3]

def get_log_pattern_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S_%f")[:-3]

def get_file_pattern_datetime() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_file_pattern_datetime_millisecond() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]

def get_full_pattern_date() -> str:
    return f"({get_time_zone_name()}) {datetime.now().strftime('%Y/%m/%d %a %H:%M:%S')}"

def get_time_zone_name() -> str:
    return datetime.now().astimezone().tzname()

def get_time_zone_offset_hour() -> int:
    return int(datetime.now().astimezone().utcoffset().total_seconds() / 3600)

def get_date(year: int, month: int) -> datetime:
    return datetime(year, month, 1)

def get_db_date(d: datetime) -> str:
    return d.strftime("%Y-%m-%d")

def get_db_datetime(d: datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")

def get_time_from_second(s: int) -> str:
    hh, remainder = divmod(s, 3600)
    mm, ss = divmod(remainder, 60)
    return f"{hh:02}:{mm:02}:{ss:02}"

def get_period(year: str, month: str) -> list[str]:
    year = int(year)
    month = int(month)
    
    cal = datetime.datetime(year, month, 1)
    weekday = cal.weekday()
    
    # Calculate the start of the period
    if weekday == 6:  # Sunday
        begin_date = cal - datetime.timedelta(days=6)
    else:
        begin_date = cal - datetime.timedelta(days=weekday + 1)
    
    # Calculate the end of the period
    next_month = cal + datetime.timedelta(days=31)
    end_of_month = next_month.replace(day=1) - datetime.timedelta(days=1)
    end_weekday = end_of_month.weekday()
    
    if end_weekday == 6:  # Sunday
        end_date = end_of_month
    else:
        end_date = end_of_month + datetime.timedelta(days=(6 - end_weekday))
    
    return [begin_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

def get_random_by_time() -> str:
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S%f")
    return encrypt(timestamp)  # Assuming `encrypt` is defined elsewhere

def get_time_string() -> str:
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

def to_era_date(value: str) -> str:
    date = datetime.datetime.strptime(value, "%GGy年M月d日")
    return date.strftime("%Y/%m/%d")

def get_pattern_date_times(v: str) -> str:
    return get_pattern_date(v, "%Y-%m-%d %H:%M:%S")

def diff_time_in_millis(date1: str, date2: str) -> int:
    dt1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
    return abs(int((dt1 - dt2).total_seconds() * 1000))

def diff_time_compare(date1: str, date2: str) -> int:
    dt1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    dt2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
    return int((dt1 - dt2).total_seconds())

def get_monday_by_date(date: str) -> str:
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    monday = dt - datetime.timedelta(days=(dt.weekday() + 1) % 7)
    return monday.strftime("%Y-%m-%d")

def get_sunday_by_date(date: str) -> str:
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    sunday = dt + datetime.timedelta(days=(6 - dt.weekday()))
    return sunday.strftime("%Y-%m-%d")

def get_time_value(time: str) -> float:
    dt = datetime.datetime.strptime(time, "%H:%M:%S")
    return dt.hour / 24 + dt.minute / 1440

def get_hhmm(minutes: float) -> str:
    if minutes == 0:
        return ""
    hh = int(minutes // 60)
    mm = int(minutes % 60)
    return f"{hh:02}:{mm:02}"

def is_date(ori: str) -> bool:
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    return bool(pattern.match(ori))

def is_datetime(ori: str) -> bool:
    pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    return bool(pattern.match(ori))

def is_time(ori: str) -> bool:
    pattern = re.compile(r"\d{2}:\d{2}:\d{2}")
    return bool(pattern.match(ori))

def check_date(datestr: str) -> bool:
    pattern = re.compile(r"\d{4}/\d{2}/\d{2}")
    return bool(pattern.match(datestr))

def check_simple_date(datestr: str) -> bool:
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    return bool(pattern.match(datestr))

def check_time(timestr: str) -> bool:
    pattern = re.compile(r"\d{2}:\d{2}:\d{2}")
    return bool(pattern.match(timestr))

def check_date_time(datetimestr: str) -> bool:
    pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    return bool(pattern.match(datetimestr))

def date_to_wareki(date: datetime.date, format_str: str) -> str:
    return date.strftime(format_str)

def convert_to_wareki_report(value: datetime.date, add_wd: bool) -> str:
    if add_wd:
        return date_to_wareki(value, "%Gy年%m月%d日(%a)")
    else:
        return date_to_wareki(value, "%Gy年%m月%d日")

def convert_to_wareki_report_str(value: str, add_wd: bool) -> str:
    date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return convert_to_wareki_report(date, add_wd)

def get_pattern_date(date_value: str, from_pattern: str, to_pattern: str) -> str:
    try:
        date = datetime.datetime.strptime(date_value, from_pattern)
        return date.strftime(to_pattern)
    except ValueError:
        return date_value

def get_pattern_date_time(date_value: str, from_pattern: str, to_pattern: str) -> str:
    try:
        date = datetime.datetime.strptime(date_value, from_pattern)
        return date.strftime(to_pattern)
    except ValueError:
        return date_value

def get_first_day_from_date(specified_date: str, str_pattern_ori: str, count: int, lang_id: str) -> str:
    sdf = "%Y/%m/%d"
    c = datetime.datetime.strptime(specified_date, sdf)
    if str_pattern_ori == "year":
        c = c.replace(month=1, day=1)
        c = c + datetime.timedelta(days=365 * count)
    elif str_pattern_ori == "month":
        c = c.replace(day=1)
        c = c + datetime.timedelta(days=31 * count)
    elif str_pattern_ori == "week":
        c = c + datetime.timedelta(days=7 * count)
        if lang_id == "JPN":
            c = c - datetime.timedelta(days=c.weekday() + 1)
        else:
            c = c - datetime.timedelta(days=c.weekday())
    return c.strftime(sdf)

def get_last_day_from_date(specified_date: str, str_pattern_ori: str, count: int, lang_id: str) -> str:
    sdf = "%Y/%m/%d"
    c = datetime.datetime.strptime(specified_date, sdf)
    if str_pattern_ori == "year":
        c = c.replace(month=1, day=1)
        c = c + datetime.timedelta(days=365 * (count + 1))
        c = c - datetime.timedelta(days=1)
    elif str_pattern_ori == "month":
        c = c.replace(day=1)
        c = c + datetime.timedelta(days=31 * (count + 1))
        c = c - datetime.timedelta(days=1)
    elif str_pattern_ori == "week":
        c = c + datetime.timedelta(days=7 * count)
        if lang_id == "CHN":
            c = c + datetime.timedelta(days=(6 - c.weekday()))
        else:
            c = c + datetime.timedelta(days=(6 - c.weekday() + 1))
    return c.strftime(sdf)

# Encrypt function stub (replace with actual implementation)
def encrypt(data: str) -> str:
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(len(data)))
