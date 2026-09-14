from typing import List, Optional, Union
import locale
import re
from io import TextIOWrapper

locale.setlocale(locale.LC_ALL, '')

def dspText(input_str):
    if input_str is None or len(input_str) == 0:
        return input_str
    buf = []
    for ch in input_str:
        if ch == "'":
            buf.append("&#x27;")
        elif ch == "`":
            buf.append("&#x60;")
        elif ch == '"':
            buf.append("&quot;")
        elif ch == '<':
            buf.append("&lt;")
        elif ch == '>':
            buf.append("&gt;")
        else:
            buf.append(ch)
    return ''.join(buf)

def dspHtmlTag(input_str):
    if input_str is None or len(input_str) == 0:
        return input_str
    replacements = {
        "&#x27;": "'",
        "&#x60;": "`",
        "&quot;": '"',
        "&lt;": "<",
        "&gt;": ">",
        "&amp;": "&"
    }
    for key, value in replacements.items():
        input_str = input_str.replace(key, value)
    return input_str



def changeStringToInt(i_source):
    try:
        return int(i_source)
    except ValueError:
        return 0


def checkString2Int(i_source):
    try:
        i_source = i_source.replace(",", "").strip()
        int(i_source)
        return True
    except ValueError:
        return False
def changeStringToLong(i_source):
    if i_source is None or len(i_source.strip()) == 0:
        return 0

    try:
        i_source = i_source.replace(",", "").strip()
        return float(i_source)
    except ValueError:
        raise ValueError(f"Cannot convert '{i_source}' to long")


def changeStringToDouble(i_source):
    if i_source is None or len(i_source.strip()) == 0:
        return 0.0

    try:
        i_source = i_source.replace(",", "").strip()
        return float(i_source)
    except ValueError:
        raise ValueError(f"Cannot convert '{i_source}' to double")

def changeStringToFloat(i_source):
    if i_source is None or len(i_source.strip()) == 0:
        return 0.0

    try:
        i_source = i_source.replace(",", "").strip()
        return float(i_source)
    except ValueError:
        raise ValueError(f"Cannot convert '{i_source}' to float")

def changeStringToBoolean(i_source):
    if i_source is None or len(i_source.strip()) == 0:
        return False

    true_values = {'true', 'yes', '1'}
    return i_source.strip().lower() in true_values

def separateWord(i_source, i_separator, i_length):
    if (i_source is None or len(i_source.strip()) == 0 or
        i_separator is None or len(i_separator.strip()) == 0 or
        len(i_source) <= i_length):
        return i_source

    temp_string = i_source
    temp_after_dot = ""
    
    # Check if the string contains a dot and separate if it does
    if '.' in i_source:
        temp_string, temp_after_dot = i_source.split('.', 1)
    
    return_value = []
    
    # Insert separators
    while len(temp_string) > i_length:
        return_value.append(temp_string[-i_length:])
        temp_string = temp_string[:-i_length]

    # Append the remaining part and the part after the dot
    return_value.append(temp_string)
    return_value.append(temp_after_dot)

    return i_separator.join(return_value)

def separateWordList(i_source, i_length):
    if i_source is None or len(i_source.strip()) == 0:
        return [i_source]

    if len(i_source) <= i_length:
        return [i_source]

    return [i_source[i:i+i_length] for i in range(0, len(i_source), i_length)]


 
    def contactWord(source, separator):
        if source is None:
            return None
        return source.replace(separator, "")
    
    
    def changeDateFormat(source):
        return source.replace('-', '/')
    
    
    def isAllNumber(source):
        if source is None or len(source) < 1:
            return False
        
        parts = source.split('-')
        if len(parts) > 2:
            return False
        
        if '-' in source and source[0] != '-':
            return False
        
        dot_count = source.count('.')
        if dot_count > 1:
            return False
        
        if source.endswith('.'):
            return False
        
        return source.replace('.', '').isdigit()
    

    def isEvenNumber(number):
        return number % 2 == 0
    
    
    def isAlphabetNumber(source):
        if source is None or source.strip() == '':
            return True
        
        return source.isalnum()
    
    
    def addZeroToWord(source, length):
        if source is None or len(source) >= length:
            return source
        
        return source.zfill(length)
    
    
    def addSpaceToWord(source, length):
        if source is None or len(source) >= length:
            return source
        
        return source.rjust(length)
    
    
    def addSpace(length):
        return ' ' * length
    
    
    def addCharToWord(source, add_char, to_left, length):
        if source is None or add_char is None or source == '' or len(source) >= length:
            return source
        
        if to_left:
            return add_char * (length - len(source)) + source
        else:
            return source + add_char * (length - len(source))
    
    
    def isZenKakuWord(source):
        if source is None or source == '':
            return False
        
        try:
            return len(source.encode('shift_jis')) == len(source) * 2
        except (UnicodeEncodeError, UnicodeDecodeError):
            return False
    
    
    def changeWordToUnicode(source):
        return source.encode('utf-8').decode('unicode_escape')
    
    
    def changeWordFromUnicode(source, encode='utf-8'):
        return source.encode('utf-8').decode(encode)
    
    
    def isWordInArray(source, word):
        if not source or not word:
            return False
        return word in source
    
    
    def getStrParams(param_values):
        if not param_values:
            return ''
        
        return "(" + ", ".join(f"'{pv}'" for pv in param_values if pv) + ")"
    
    
    def getIntParams(param_values):
        if not param_values:
            return ''
        
        return "(" + ", ".join(pv for pv in param_values if pv) + ")"
    
    
def isNullOrBlank(source):
	return source is None or source == ''
    
    
def isNullOrBlankWithoutTrim(source):
	return source is None or source == ''
    
    
def getStringFromArray(source, separate):
	if source is None:
		return ''
	return separate.join(source)
    
    
def getStringFromCollect(source, separate):
	if source is None:
		return ''
	return separate.join(str(item) for item in source)
    
    
def replaceString(source, target_string, replace_string):
	return source.replace(target_string, replace_string)
    
    
def isMatchWithRegex(pattern, match_string):
	return re.fullmatch(pattern, match_string) is not None
    
    
def ChangeIntToString(value):
	return str(value)
    
    
def ChangeLongToString(value):
	return str(value)
    
    
def ChangeDoubleToString(value):
	return str(value)
    
    
def ChangeBooleanToString(value):
	return '1' if value else '0'
    
    
def changeBlankToNull(value):
	return '' if value == '' else value
    


def getSameString(source, length):
    return source * length

def changeNullToBlank(src):
    if src is None:
        return ""
    if isinstance(src, str):
        s = src.strip()
        if s == "" or s.lower() in ("none", "null"):
            return ""
        return src
    return src


def timeDisplayOrBlank(value):
    if value is None:
        return ""
    if isinstance(value, str) and value.strip() == "":
        return ""
    try:
        from datetime import datetime, timedelta
        if isinstance(value, timedelta):
            total = int(value.total_seconds())
            h, r = divmod(total, 3600)
            m, s = divmod(r, 60)
            return "%02d:%02d:%02d" % (h, m, s)
        if isinstance(value, datetime):
            return value.strftime("%H:%M:%S")
        s = str(value).strip()
        return s if s else ""
    except Exception:
        return str(value).strip() if value is not None else ""


def numberDisplayOrBlank(value):
    if value is None:
        return ""
    if isinstance(value, str) and value.strip() == "":
        return ""
    try:
        s = str(value).strip()
        if not s:
            return ""
        try:
            f = float(s)
            if f == int(f):
                return str(int(f))
            return s
        except ValueError:
            return s
    except Exception:
        return str(value).strip() if value is not None else ""


def float2DisplayOrBlank(value):
    """Format number as 2 decimals safely. Invalid values return blank."""
    if value is None:
        return ""
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return ""
    try:
        return "{:.2f}".format(float(value))
    except (TypeError, ValueError):
        return ""


def changeNullToBlankRemoveComma(src):
    return "" if src is None else src.replace(",", "")

def changeNullToZero(src):
    return 0 if src is None else int(src)

def changeNullToZeroDouble(src):
    return 0.0 if src is None else float(src)



def changeNullToSpace(src):
    return " " if src is None else src

def changeNullToDefaultVal(src, default_value):
    return default_value if src is None else src

def changeZeroToBlank(src):
    return "" if src == "0" else src

def quoteStrList(lst):
    return [f"'{s}'" for s in lst]

def split(str_, delim):
    return str_.split(delim) if str_ else []

def createBreaks(input_str, max_length):
    words = input_str.split()
    result = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) > max_length:
            result.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word

    result.append(current_line)
    return " ".join(result)

def escapeSQLTags(input_str):
    if not input_str:
        return input_str
    return input_str.replace("\\", "\\\\").replace("'", "''")

def escapeJSTags(input_str):
    if not input_str:
        return ""
    return (input_str.replace("\\", "\\\\")
                     .replace("'", "\\'")
                     .replace("\n", "\\n")
                     .replace("\t", "\\t")
                     .replace("/", "\\/"))

def escapeTags(input_str):
    if not input_str:
        return input_str
    return (input_str.replace("\n", "\\n")
                     .replace("\r", "\\r")
                     .replace("'", "\\'")
                     .replace("/", "\\/")
                     .replace("\\", "\\\\")
                     .replace("\t", "\\t"))

def escapeValueTags(input_str):
    if not input_str:
        return input_str
    return (input_str.replace("'", "\\'")
                     .replace('"', '\"')
                     .replace("\\", "\\\\")
                     .replace("\n", "\\n")
                     .replace("\t", "\\t"))

def recoveSQLTags(input_str):
    if not input_str:
        return input_str
    try:
        return input_str.replace("''", "'").replace("\\\\", "\\")
    except IndexError:
        return input_str

def escapeJsonKeyTags(input_str):
    if not input_str:
        return input_str
    try:
        return (input_str.replace("/", "\\\\/")
                         .replace("+", "\\\\+")
                         .replace("#", "\\\\#")
                         .replace(".", "\\\\.")
                         .replace("(", "\\\\(")
                         .replace(")", "\\\\)")
                         .replace("*", "\\\\*"))
    except Exception:
        return input_str

def escapeHTMLTags(input_str):
    if input_str is None:
        return ""
    input_str = str(input_str) if not isinstance(input_str, str) else input_str
    if not input_str:
        return input_str
    return (input_str.replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace("&", "&amp;")
                     .replace('"', "&quot;"))

def escapeHTMLSQLTags(input_str):
    if not input_str:
        return input_str
    return (input_str.replace("<", "&lt;")
                     .replace(">", "&gt;")
                     .replace("&", "&amp;")
                     .replace('"', "&quot;")
                     .replace("\\", "\\\\")
                     .replace("'", "''"))

def convertNewlines(input_str):
    return input_str.replace("\r\n", "\n").replace("\n", "<br/>")

def removeNewlines(input_str):
    return input_str.replace("\r\n", "").replace("\n", "")

def removeQuotes(input_str):
    return input_str.replace("'", "").replace('"', "")

def removeSpace(input_str):
    return re.sub(r'\s+', '', input_str)

def convertSpace(input_str):
    return input_str.replace(" ", "&nbsp;")


def replace(main_string, old_string, new_string):
    if main_string is None:
            main_string = ""
    if old_string is None :
        old_string = ""
    if new_string is None :
        new_string = ""
    return main_string.replace(old_string, new_string)


def nullOrBlank(param):
     return param is None or param.strip() == ""


def notNull(param):
     return "" if param is None else param.strip()


def parseInt(param):
    try:
         return int(param)
    except ValueError:
        try:
            return int(float(param))
        except ValueError:
            return 0


def parseLong(param):
    try:
        return int(param)
    except ValueError:
        try:
            return int(float(param))
        except ValueError:
            return 0


def parseFloat(param):
    try:
        return float(param)
    except ValueError:
        return 0.0


def parseDouble(param):
    return parseFloat(param)


def parseBoolean(param):
    if nullOrBlank(param):
        return False
    return param.lower() in ["1", "y", "t"]


def parseStringFromBooleanForJson(param):
    return "1" if param else "0"


def convertURL(input_string):
    import re
    if input_string is None or len(input_string) == 0:
        return input_string

    url_pattern = re.compile(
        r'((http|ftp|https)://[a-zA-Z0-9\./]+)'
    )
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', input_string)


def dspHtml(input_string):
    str_val = notNull(input_string)
    str_val = escape_html_tags(str_val)
    str_val = convertURL(str_val)
    str_val = convert_newlines(str_val)
    return str_val

   
def dspHtml4Content(input_string):
    str_val = notNull(input_string)
    str_val = escape_html_tags(str_val)
    str_val = remove_quotes(str_val)
    str_val = remove_newlines(str_val)
    return str_val


def join(params, delim):
    return delim.join(params) if params else ""


def escape_html_tags(input_string):
    import html
    return html.escape(input_string)


def escape_html(s: str) -> str:
    """Escape for HTML output to prevent XSS. Use for any user-supplied content before rendering to HTML."""
    if s is None:
        return ""
    return escape_html_tags(s)


def convert_newlines(input_string):
    return input_string.replace('\n', '<br>')


def remove_quotes(input_string):
    return input_string.replace('"', '').replace("'", "")

 
def remove_newlines(input_string):
    return input_string.replace('\n', '').replace('\r', '')


def change_null_to_blank(input_string):
    return "" if input_string is None else input_string

def dspHtmlBreak(input_str, chars):
    str_ =  notNull(input_str)
    str_ = createBreaks(str_, chars)
    str_ = escape_html_tags(str_)
    str_ = convertURL(str_)
    str_ = convert_newlines(str_)
    return str_

def dspHtmlForLabel(input_str):
    str_ = change_null_to_blank(input_str)
    # str_ = create_breaks(str_, 80)
    str_ = escape_html_tags(str_)
    str_ = notNull(str_)
    str_ = convert_newlines(str_)
    str_ = convertSpace(str_)
    return str_

def dspHtmlForLabelWithTag(input_str):
    str_ = change_null_to_blank(input_str)
    # str_ = escape_html_tags(str_)
    str_ = convertURL(str_)
    str_ = convert_newlines(str_)
    # str_ = convert_space(str_)
    return str_

def getStrDisplay(plng_display):
    if plng_display == 0:
        return "&nbsp;"
    return str(plng_display)

def getStrDspHtml(pstr_param):
    if pstr_param is None or pstr_param == "":
        return getStrDisplay(pstr_param)
    else:
        return dspHtml(pstr_param)

def getStrDisplay(pstr_display):
    if pstr_display is None:
        return "&nbsp;"
    if len(pstr_display.strip()) == 0:
        return "&nbsp;"
    return pstr_display

def getStrDisplayReplace(pstr_display, pstr_replace):
    if pstr_display is None:
        return "&nbsp;"
    if len(pstr_display.strip()) == 0:
        return pstr_replace
    return pstr_display

def joinArray(pstr_params, pstr_delim):
    if pstr_params is not None and len(pstr_params) > 0:
        return pstr_delim.join(pstr_params)
    return ""

def joinList(list_, delim):
    if not list_ or len(list_) < 1:
        return None
    return delim.join(list_)

def join_target_source(pstr_target, pstr_source, pstr_delim):
    if nullOrBlank(pstr_target):
        return pstr_source
    else:
        return f"{pstr_target}{pstr_delim}{pstr_source}"

def joinPos(pos, pstr_source, pstr_join):
    str_prv = ""
    str_aft = ""
    if not is_null_or_blank(pstr_source) and pos >= 0:
        str_prv = pstr_source[:pos]
        str_aft = pstr_source[pos:]
    return join_target_source(str_prv, str_aft, pstr_join)



def VectorToArray(pv_param: List[List[str]], pint_num: Optional[int] = None) -> List[str]:
    if pint_num is None:
        return [item[0] for item in pv_param]
    else:
        return [item[pint_num] if len(item) > pint_num else "" for item in pv_param]

def VectorToList(pv_param: List[str]) -> List[str]:
    return pv_param.copy()

def ArrayListToArrayDouble(pv_param: List[float]) -> List[float]:
    return pv_param.copy()

def ListToArray(pl_param: List[str]) -> List[str]:
    return pl_param.copy()

def getEmptyStringIfNull(s: Optional[str]) -> str:
    return s if s is not None else ""

def getSelectedString(code: str, codes: str, strings: str, delim: str) -> Optional[str]:
    a = codes.split(delim)
    b = strings.split(delim)
    for i in range(len(a)):
        if code == a[i]:
            return b[i]
    return None

def getCharCount(buf: str, c: str) -> int:
    return buf.count(c)

def trim4Script(s: str) -> str:
    return s.strip()

def getSqlInCondionString(al: List[List[str]], num: int, data_type: str) -> str:
    elements = [f"'{item[num]}'" if data_type != "NUM" else item[num] for item in al]
    return ",".join(elements)

def removeRightString(ori: str, remove_str: str) -> str:
    pos = ori.rfind(remove_str)
    if pos > -1 and ori[pos:].strip() == remove_str.strip():
        return ori[:pos]
    else:
        return ori

def getStringPos(ori: str, str_of_big: str) -> int:
    ori = ori.replace("\n", " ").upper()
    return ori.rfind(str_of_big)

def getStringPosWithCase(ori: str, s: str) -> int:
    ori = ori.replace("\n", " ")
    return ori.rfind(s)

def getStringPosFromList(ori: str, al_oper: List[str]) -> int:
    ori_upper = ori.upper()
    for str_of_big in al_oper:
        pos = ori_upper.rfind(str_of_big)
        if pos > -1:
            return pos
    return -1

def isContain(str1: str, str2: str) -> bool:
    return str2 in str1

def replaceContent(replace: List[str], ori: str) -> str:
    for i, rep in enumerate(replace):
        ori = ori.replace(f"@@{i + 1}", rep)
    return ori

def concatStrByComma(v: str, r: str) -> str:
    return v if not r else f"{r},{v}"

def subString(ori: str, last_pos: int) -> str:
    return ori[:-last_pos]

def concatSignCount(ori: str, divide_char: str) -> int:
    if not divide_char:
        return 1
    return ori.count(divide_char) + 1

def split2Array(ori: str, divide_char: str, return_val: Optional[List[str]] = None) -> List[str]:
    if return_val is None:
        return_val = []
    
    if divide_char == "\\t":
        return_val.extend(ori.split("\t"))
    else:
        divide_char = " " if divide_char == "\\b" else divide_char
        return_val.extend(ori.split(divide_char))

    return return_val

def FixByte(s: str, capacity: int, csn: str) -> str:
    encoded = s.encode(csn)
    trimmed = encoded[:capacity]
    return trimmed.decode(csn, errors="ignore").ljust(capacity)

def FixByteLen(s: str, csn: str) -> int:
    return len(s.encode(csn))

def substring(s: str, begin: int, end: int, csn: str) -> str:
    encoded = s.encode(csn)
    return encoded[begin:end].decode(csn, errors="ignore").strip()



def is_null_or_blank(s):
    return s is None or s.strip() == ""

def change_string_to_float(s):
    try:
        return float(s)
    except ValueError:
        return 0.0


def change_string_to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0

def change_string_to_double(s):
    try:
        return float(s)
    except ValueError:
        return 0.0

def setDefaultChkBoxVal(v, d):
    if is_null_or_blank(v):
        return d
    else:
        return v

def getColorValue(v):
    if is_null_or_blank(v):
        return 0
    else:
        v = v.replace("#", "")
        return int(v, 16)

def isValueContain(values, value):
    values.sort()
    return value in values


def jointValues(values):
    if values:
        return ','.join([v for v in values if v])
    return ""


def length(s):
    return 0 if is_null_or_blank(s) else len(s)


def getNumberFormat(i):
    return locale.format_string("%d", i, grouping=True)

def isHavinString(pattern, ori):
    return re.match(f".*{pattern}.*", ori, re.IGNORECASE) is not None

def isAlphanumberic(user_id):
    return re.match

def is_integer(value: str) -> bool:
        pattern = re.compile(r'^[-+]?\d+$', re.IGNORECASE)
        return bool(pattern.match(value))

def is_double(value: str) -> bool:
    pattern = re.compile(r'^[-+]?\d*\.\d+$|^[-+]?\d+$', re.IGNORECASE)
    return bool(pattern.match(value))

def is_mail_address(ori: str) -> bool:
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', re.IGNORECASE)
    return bool(pattern.match(ori))

def is_http(ori: str) -> bool:
    pattern = re.compile(r'^(http|https)://[^\s]+$', re.IGNORECASE)
    return bool(pattern.match(ori))


def get_number_with_comma(number: str) -> str:
    return locale.format_string("%f", float(number), grouping=True)


def get_comma_string_to_int(number: str) -> int:
    if number == None or number == '' :
        return 0
    return int(number.replace(",", ""))


def get_comma_string_to_float(number: str) -> float:
    if number == None or number == '' :
        return 0
    return int(number.replace(",", ""))

def get_comma_string_to_double(number: str) -> float:
    if number == None or number == '' :
        return 0
    return int(number.replace(",", ""))


def to_small_ascii(mode: bool, string: str) -> str:
    if not string:
        return ""
    buf = []
    for char in string:
        buf.append(to_small_ascii_by_one(mode, char))
    return "".join(buf)

def to_big_ascii(string: str) -> str:
    if not string:
        return ""
    buf = []
    for char in string:
        buf.append(to_big_ascii_one(char))
    return "".join(buf)

def to_big_ascii_not_numbers(string: str) -> str:
    if not string:
        return ""
    buf = []
    for char in string:
        buf.append(to_big_ascii_one_not_numbers(char))
    return "".join(buf)

def split_integer_array(input_str: str) -> List[int]:
    strarray = input_str.split(",")
    intarray = [int(i) for i in strarray]
    return intarray

def is_all_space(iSource: str) -> bool:
    if iSource:
        return not bool(iSource.replace(" ", "").replace("　", ""))
    return False

def to_small_ascii_by_one(mode: bool, char: str) -> str:
        # Conversion logic based on the mode. Example provided below:
        if ord(char) >= ord('Ａ') and ord(char) <= ord('Ｚ'):
            return chr(ord(char) - ord('Ａ') + ord('A'))
        elif ord(char) >= ord('ａ') and ord(char) <= ord('ｚ'):
            return chr(ord(char) - ord('ａ') + ord('a'))
        elif ord(char) >= ord('０') and ord(char) <= ord('９'):
            return chr(ord(char) - ord('０') + ord('0'))
        return char


def to_big_ascii_one(char: str) -> str:
        # Conversion logic for full-width characters. Example provided below:
        if ord(char) >= ord('A') and ord(char) <= ord('Z'):
            return chr(ord(char) - ord('A') + ord('Ａ'))
        elif ord(char) >= ord('a') and ord(char) <= ord('z'):
            return chr(ord(char) - ord('a') + ord('ａ'))
        elif ord(char) >= ord('0') and ord(char) <= ord('9'):
            return chr(ord(char) - ord('0') + ord('０'))
        return char


def to_big_ascii_one_not_numbers(char: str) -> str:
        # Conversion logic for full-width characters excluding numbers. Example provided below:
        if ord(char) >= ord('A') and ord(char) <= ord('Z'):
            return chr(ord(char) - ord('A') + ord('Ａ'))
        elif ord(char) >= ord('a') and ord(char) <= ord('z'):
            return chr(ord(char) - ord('a') + ord('ａ'))
        return char
    
def to_small_ascii_by_one(mode: bool, code: str) -> str:
    conversion_table = {
        '！': "!",
        '”': "&quot;" if mode else "\"",
        '＃': "#",
        '＄': "$",
        '￥': "\\",
        '％': "%",
        '＆': "&",
        '’': "\'",
        '（': "(",
        '）': ")",
        '＊': "*",
        '＋': "+",
        '，': ",",
        '－': "-",
        '．': ".",
        '／': "/",
        '０': "0",
        '１': "1",
        '２': "2",
        '３': "3",
        '４': "4",
        '５': "5",
        '６': "6",
        '７': "7",
        '８': "8",
        '９': "9",
        '：': ":",
        '；': ";",
        '＜': "&lt;" if mode else "<",
        '＝': "=",
        '＞': "&gt;" if mode else ">",
        '？': "?",
        '＠': "@",
        'Ａ': "A",
        'Ｂ': "B",
        'Ｃ': "C",
        'Ｄ': "D",
        'Ｅ': "E",
        'Ｆ': "F",
        'Ｇ': "G",
        'Ｈ': "H",
        'Ｉ': "I",
        'Ｊ': "J",
        'Ｋ': "K",
        'Ｌ': "L",
        'Ｍ': "M",
        'Ｎ': "N",
        'Ｏ': "O",
        'Ｐ': "P",
        'Ｑ': "Q",
        'Ｒ': "R",
        'Ｓ': "S",
        'Ｔ': "T",
        'Ｕ': "U",
        'Ｖ': "V",
        'Ｗ': "W",
        'Ｘ': "X",
        'Ｙ': "Y",
        'Ｚ': "Z",
        '＾': "^",
        '＿': "_",
        '‘': "`",
        'ａ': "a",
        'ｂ': "b",
        'ｃ': "c",
        'ｄ': "d",
        'ｅ': "e",
        'ｆ': "f",
        'ｇ': "g",
        'ｈ': "h",
        'ｉ': "i",
        'ｊ': "j",
        'ｋ': "k",
        'ｌ': "l",
        'ｍ': "m",
        'ｎ': "n",
        'ｏ': "o",
        'ｐ': "p",
        'ｑ': "q",
        'ｒ': "r",
        'ｓ': "s",
        'ｔ': "t",
        'ｕ': "u",
        'ｖ': "v",
        'ｗ': "w",
        'ｘ': "x",
        'ｙ': "y",
        'ｚ': "z",
        '｛': "{",
        '｜': "|",
        '｝': "}",
        '。': "｡",
        '「': "｢",
        '」': "｣",
        '、': "､",
        '・': "･",
        '　': "&nbsp;" if mode else " ",
        'あ': "あ",
        'ア': "ｱ",
        'い': "い",
        'イ': "ｲ",
        'う': "う",
        'ウ': "ｳ",
        'え': "え",
        'エ': "ｴ",
        'お': "お",
        'オ': "ｵ",
        'か': "か",
        'カ': "ｶ",
        'き': "き",
        'キ': "ｷ",
        'く': "く",
        'ク': "ｸ",
        'け': "け",
        'ケ': "ｹ",
        'こ': "こ",
        'コ': "ｺ",
        'さ': "さ",
        'サ': "ｻ",
        'し': "し",
        'シ': "ｼ",
        'す': "す",
        'ス': "ｽ",
        'せ': "せ",
        'セ': "ｾ",
        'そ': "そ",
        'ソ': "ｿ",
        'た': "た",
        'タ': "ﾀ",
        'ち': "ち",
        'チ': "ﾁ",
        'つ': "つ",
        'ツ': "ﾂ",
        'て': "て",
        'テ': "ﾃ",
        'と': "と",
        'ト': "ﾄ",
        'な': "な",
        'ナ': "ﾅ",
        'に': "に",
        'ニ': "ﾆ",
        'ぬ': "ぬ",
        'ヌ': "ﾇ",
        'ね': "ね",
        'ネ': "ﾈ",
        'の': "の",
        'ノ': "ﾉ",
        'は': "は",
        'ハ': "ﾊ",
        'ひ': "ひ",
        'ヒ': "ﾋ",
        'ふ': "ふ",
        'フ': "ﾌ",
        'へ': "ﾍ",
        'ほ': "ほ",
        'ホ': "ﾎ",
        'ま': "ま",
        'マ': "ﾏ",
        'み': "み",
        'ミ': "ﾐ",
        'む': "む",
        'ム': "ﾑ",
        'め': "め",
        'メ': "ﾒ",
        'も': "も",
        'モ': "ﾓ",
        'や': "や",
        'ヤ': "ﾔ",
        'ゆ': "ゆ",
        'ユ': "ﾕ",
        'よ': "よ",
        'ヨ': "ﾖ",
        'ら': "ら",
        'ラ': "ﾗ",
        'り': "り",
        'リ': "ﾘ",
        'る': "る",
        'ル': "ﾙ",
        'れ': "れ",
        'レ': "ﾚ",
        'ろ': "ろ",
        'ロ': "ﾛ",
        'わ': "わ",
        'ワ': "ﾜ",
        'を': "を",
        'ヲ': "ｦ",
        'ん': "ん",
        'ン': "ﾝ",
        'が': "が",
        'ガ': "ｶﾞ",
        'ぎ': "ぎ",
        'ギ': "ｷﾞ",
        'ぐ': "ぐ",
        'グ': "ｸﾞ",
        'げ': "げ",
        'ゲ': "ｹﾞ",
        'ご': "ご",
        'ゴ': "ｺﾞ",
        'ざ': "ざ",
        'ザ': "ｻﾞ",
        'じ': "じ",
        'ジ': "ｼﾞ",
        'ず': "ず",
        'ズ': "ｽﾞ",
        'ぜ': "ぜ",
        'ゼ': "ｾﾞ",
        'ぞ': "ぞ",
        'ゾ': "ｿﾞ",
        'だ': "だ",
        'ダ': "ﾀﾞ",
        'ぢ': "ぢ",
        'ヂ': "ﾁﾞ",
        'づ': "づ",
        'ヅ': "ﾂﾞ",
        'で': "で",
        'デ': "ﾃﾞ",
        'ど': "ど",
        'ド': "ﾄﾞ",
        'ば': "ば",
        'バ': "ﾊﾞ",
        'び': "び",
        'ビ': "ﾋﾞ",
        'ぶ': "ぶ",
        'ブ': "ﾌﾞ",
        'ベ': "ﾍﾞ",
        'ぼ': "ぼ",
        'ボ': "ﾎﾞ",
        'ぱ': "ぱ",
        'パ': "ﾊﾟ",
        'ぴ': "ぴ",
        'ピ': "ﾋﾟ",
        'ぷ': "ぷ",
        'プ': "ﾌﾟ",
        'ぺ': "ぺ",
        'ぽ': "ぽ",
        'ポ': "ﾎﾟ"
    }

    return conversion_table.get(code, code)
def to_big_ascii_one(code):
    conversion_dict = {
        "!": "！",
        '"': "”",
        "#": "＃",
        "$": "＄",
        "\\": "￥",
        "%": "％",
        "&": "＆",
        "'": "’",
        "(": "（",
        ")": "）",
        "*": "＊",
        "+": "＋",
        ",": "，",
        "-": "－",
        ".": "．",
        "/": "／",
        "0": "０",
        "1": "１",
        "2": "２",
        "3": "３",
        "4": "４",
        "5": "５",
        "6": "６",
        "7": "７",
        "8": "８",
        "9": "９",
        ":": "：",
        ";": "；",
        "<": "＜",
        "=": "＝",
        ">": "＞",
        "?": "？",
        "@": "＠",
        "A": "Ａ",
        "B": "Ｂ",
        "C": "Ｃ",
        "D": "Ｄ",
        "E": "Ｅ",
        "F": "Ｆ",
        "G": "Ｇ",
        "H": "Ｈ",
        "I": "Ｉ",
        "J": "Ｊ",
        "K": "Ｋ",
        "L": "Ｌ",
        "M": "Ｍ",
        "N": "Ｎ",
        "O": "Ｏ",
        "P": "Ｐ",
        "Q": "Ｑ",
        "R": "Ｒ",
        "S": "Ｓ",
        "T": "Ｔ",
        "U": "Ｕ",
        "V": "Ｖ",
        "W": "Ｗ",
        "X": "Ｘ",
        "Y": "Ｙ",
        "Z": "Ｚ",
        "^": "＾",
        "_": "＿",
        "`": "‘",
        "a": "ａ",
        "b": "ｂ",
        "c": "ｃ",
        "d": "ｄ",
        "e": "ｅ",
        "f": "ｆ",
        "g": "ｇ",
        "h": "ｈ",
        "i": "ｉ",
        "j": "ｊ",
        "k": "ｋ",
        "l": "ｌ",
        "m": "ｍ",
        "n": "ｎ",
        "o": "ｏ",
        "p": "ｐ",
        "q": "ｑ",
        "r": "ｒ",
        "s": "ｓ",
        "t": "ｔ",
        "u": "ｕ",
        "v": "ｖ",
        "w": "ｗ",
        "x": "ｘ",
        "y": "ｙ",
        "z": "ｚ",
        "{": "｛",
        "|": "｜",
        "}": "｝",
        "｡": "。",
        "｢": "「",
        "｣": "」",
        "､": "、",
        "･": "・",
        " ": "　",
        "ｱ": "ア",
        "ｲ": "イ",
        "ｳ": "ウ",
        "ｴ": "エ",
        "ｵ": "オ",
        "ｶ": "カ",
        "ｷ": "キ",
        "ｸ": "ク",
        "ｹ": "ケ",
        "ｺ": "コ",
        "ｻ": "サ",
        "ｼ": "シ",
        "ｽ": "ス",
        "ｾ": "セ",
        "ｿ": "ソ",
        "ﾀ": "タ",
        "ﾁ": "チ",
        "ﾂ": "ツ",
        "ﾃ": "テ",
        "ﾄ": "ト",
        "ﾅ": "ナ",
        "ﾆ": "ニ",
        "ﾇ": "ヌ",
        "ﾈ": "ネ",
        "ﾉ": "ノ",
        "ﾊ": "ハ",
        "ﾋ": "ヒ",
        "ﾌ": "フ",
        "ﾍ": "へ",
        "ﾎ": "ホ",
        "ﾏ": "マ",
        "ﾐ": "ミ",
        "ﾑ": "ム",
        "ﾒ": "メ",
        "ﾓ": "モ",
        "ﾔ": "ヤ",
        "ﾕ": "ユ",
        "ﾖ": "ヨ",
        "ﾗ": "ラ",
        "ﾘ": "リ",
        "ﾙ": "ル",
        "ﾚ": "レ",
        "ﾛ": "ロ",
        "ﾜ": "ワ",
        "ｦ": "ヲ",
        "ﾝ": "ン",
        "ｶﾞ": "ガ",
        "ｷﾞ": "ギ",
        "ｸﾞ": "グ",
        "ｹﾞ": "ゲ",
        "ｺﾞ": "ゴ",
        "ｻﾞ": "ザ",
        "ｼﾞ": "ジ",
        "ｽﾞ": "ズ",
        "ｾﾞ": "ゼ",
        "ｿﾞ": "ゾ",
        "ﾀﾞ": "ダ",
        "ﾁﾞ": "ヂ",
        "ﾂﾞ": "ヅ",
        "ﾃﾞ": "デ",
        "ﾄﾞ": "ド",
        "ﾊﾞ": "バ",
        "ﾋﾞ": "ビ",
        "ﾌﾞ": "ブ",
        "ﾍﾞ": "ベ",
        "ﾎﾞ": "ボ",
        "ﾊﾟ": "パ",
        "ﾋﾟ": "ピ",
        "ﾌﾟ": "プ",
        "ﾍﾟ": "ペ",
        "ﾎﾟ": "ポ",
    }
    
    return conversion_dict.get(code, code)

def to_big_ascii_one_not_numbers(code):
    conversion_dict = {
        "!": "！",
        '"': "”",
        "#": "＃",
        "$": "＄",
        "\\": "￥",
        "%": "％",
        "&": "＆",
        "'": "’",
        "(": "（",
        ")": "）",
        "*": "＊",
        "+": "＋",
        ",": "，",
        "-": "－",
        ".": "．",
        "/": "／",
        ":": "：",
        ";": "；",
        "<": "＜",
        "=": "＝",
        ">": "＞",
        "?": "？",
        "@": "＠",
        "A": "Ａ",
        "B": "Ｂ",
        "C": "Ｃ",
        "D": "Ｄ",
        "E": "Ｅ",
        "F": "Ｆ",
        "G": "Ｇ",
        "H": "Ｈ",
        "I": "Ｉ",
        "J": "Ｊ",
        "K": "Ｋ",
        "L": "Ｌ",
        "M": "Ｍ",
        "N": "Ｎ",
        "O": "Ｏ",
        "P": "Ｐ",
        "Q": "Ｑ",
        "R": "Ｒ",
        "S": "Ｓ",
        "T": "Ｔ",
        "U": "Ｕ",
        "V": "Ｖ",
        "W": "Ｗ",
        "X": "Ｘ",
        "Y": "Ｙ",
        "Z": "Ｚ",
        "^": "＾",
        "_": "＿",
        "`": "‘",
        "a": "ａ",
        "b": "ｂ",
        "c": "ｃ",
        "d": "ｄ",
        "e": "ｅ",
        "f": "ｆ",
        "g": "ｇ",
        "h": "ｈ",
        "i": "ｉ",
        "j": "ｊ",
        "k": "ｋ",
        "l": "ｌ",
        "m": "ｍ",
        "n": "ｎ",
        "o": "ｏ",
        "p": "ｐ",
        "q": "ｑ",
        "r": "ｒ",
        "s": "ｓ",
        "t": "ｔ",
        "u": "ｕ",
        "v": "ｖ",
        "w": "ｗ",
        "x": "ｘ",
        "y": "ｙ",
        "z": "ｚ",
        "{": "｛",
        "|": "｜",
        "}": "｝",
        "｡": "。",
        "｢": "「",
        "｣": "」",
        "､": "、",
        "･": "・",
        " ": "　",
        "ｱ": "ア",
        "ｲ": "イ",
        "ｳ": "ウ",
        "ｴ": "エ",
        "ｵ": "オ",
        "ｶ": "カ",
        "ｷ": "キ",
        "ｸ": "ク",
        "ｹ": "ケ",
        "ｺ": "コ",
        "ｻ": "サ",
        "ｼ": "シ",
        "ｽ": "ス",
        "ｾ": "セ",
        "ｿ": "ソ",
        "ﾀ": "タ",
        "ﾁ": "チ",
        "ﾂ": "ツ",
        "ﾃ": "テ",
        "ﾄ": "ト",
        "ﾅ": "ナ",
        "ﾆ": "ニ",
        "ﾇ": "ヌ",
        "ﾈ": "ネ",
        "ﾉ": "ノ",
        "ﾊ": "ハ",
        "ﾋ": "ヒ",
        "ﾌ": "フ",
        "ﾍ": "へ",
        "ﾎ": "ホ",
        "ﾏ": "マ",
        "ﾐ": "ミ",
        "ﾑ": "ム",
        "ﾒ": "メ",
        "ﾓ": "モ",
        "ﾔ": "ヤ",
        "ﾕ": "ユ",
        "ﾖ": "ヨ",
        "ﾗ": "ラ",
        "ﾘ": "リ",
        "ﾙ": "ル",
        "ﾚ": "レ",
        "ﾛ": "ロ",
        "ﾜ": "ワ",
        "ｦ": "ヲ",
        "ﾝ": "ン",
        "ｶﾞ": "ガ",
        "ｷﾞ": "ギ",
        "ｸﾞ": "グ",
        "ｹﾞ": "ゲ",
        "ｺﾞ": "ゴ",
        "ｻﾞ": "ザ",
        "ｼﾞ": "ジ",
        "ｽﾞ": "ズ",
        "ｾﾞ": "ゼ",
        "ｿﾞ": "ゾ",
        "ﾀﾞ": "ダ",
        "ﾁﾞ": "ヂ",
        "ﾂﾞ": "ヅ",
        "ﾃﾞ": "デ",
        "ﾄﾞ": "ド",
        "ﾊﾞ": "バ",
        "ﾋﾞ": "ビ",
        "ﾌﾞ": "ブ",
        "ﾍﾞ": "ベ",
        "ﾎﾞ": "ボ",
        "ﾊﾟ": "パ",
        "ﾋﾟ": "ピ",
        "ﾌﾟ": "プ",
        "ﾍﾟ": "ペ",
        "ﾎﾟ": "ポ",
    }
    
    return conversion_dict.get(code, code)



def finds(text: Optional[str], rex: str) -> Optional[List[str]]:
    if not text:
        return None
    
    exist_set = set()
    result = []
    pattern = re.compile(rex, re.IGNORECASE)
    
    for match in pattern.finditer(text):
        value = match.group().strip()
        if value not in exist_set:
            result.append(value)
            exist_set.add(value)
    
    return result


def inputStream2String(is_: TextIOWrapper) -> str:
    return is_.read()



def toCamel(flag: bool, *strings: str) -> str:
    if not strings:
        return ""
    
    result = []
    for i, s in enumerate(strings):
        if not s:
            continue
        
        if i == 0:
            result.append(s.capitalize() if flag else s)
        else:
            result.append(s.capitalize())
    
    return ''.join(result)
def nameAlllowercase(name: str) -> str:
    if not name:
        return ""
    
    if '_' not in name:
        return name.lower()
    
    segments = name.split('_')
    result = ''.join(seg for seg in segments if seg)
    
    return result.lower()


def _dict_key_variants(key):
    """設計書 / 生成器 key と DAO snake_case 列名の両方を試す。"""
    if key is None:
        return []
    k = str(key).strip()
    if not k:
        return []
    variants = [k]
    if "_" in k:
        compact = k.replace("_", "")
        if compact and compact not in variants:
            variants.append(compact)
    return variants


def dict_get(d, key, default=""):
    """DAO result dict から値を取得（prompt_text / prompttext 等の差を吸収）。"""
    if not isinstance(d, dict) or key is None:
        return default
    k = str(key).strip()
    if not k:
        return default
    for candidate in _dict_key_variants(k):
        if candidate in d:
            val = d[candidate]
            if val is not None:
                return val
    compact = k.replace("_", "").lower()
    for dk, dv in d.items():
        if dv is None:
            continue
        if str(dk).replace("_", "").lower() == compact:
            return dv
    return default


def _expand_dict_key_candidates(keys):
    expanded = []
    seen = set()
    for key in keys or []:
        for candidate in _dict_key_variants(key):
            if candidate not in seen:
                seen.add(candidate)
                expanded.append(candidate)
    return expanded


def build_id_name_string(rows, id_keys, name_keys=None) -> str:
    """
    リスト各行を '{id}:{name};' 形式で連結する（P04 EMOTIONS/FACTORS 等）。
    id_keys / name_keys は str または複数キー候補の list（DAO 戻り値の大小文字差を吸収）。
    """
    if not rows:
        return ""
    if isinstance(id_keys, str):
        id_keys = [id_keys]
    if name_keys is None:
        name_keys = []
    elif isinstance(name_keys, str):
        name_keys = [name_keys]
    id_keys = _expand_dict_key_candidates(id_keys)
    name_keys = _expand_dict_key_candidates(name_keys)

    parts = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        eid = ""
        for key in id_keys:
            val = row.get(key)
            if val is not None and str(val).strip():
                eid = str(val).strip()
                break
        name = ""
        for key in name_keys:
            val = row.get(key)
            if val is not None and str(val).strip():
                name = str(val).strip()
                break
        if eid:
            parts.append(f"{eid}:{name};")
    return "".join(parts)


def checkForDuplicates(entities: list, attribute_name: str) -> bool:
    seen_values = set()

    for entity in entities:
        if not hasattr(entity, attribute_name):
            return False
        
        value = getattr(entity, attribute_name)
        
        if value in seen_values:
            return False
        seen_values.add(value)
    
    return True
