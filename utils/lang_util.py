import simplejson as json
from datetime import date, datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
import traceback  # Used to get the stack trace information of exceptions
import re
from flask import request,session
import utils.config


def calc_age(y1: int, m1: int, d1: int, y2: int, m2: int, d2: int):
    """Calculate age

    :param y1, m1, d1: Birthdate
    :param y2, m2, d2: Current date
    """
    age = y2 - y1 - ((y2, y2) < (m1, d1))
    return age


def make_date(y, m, d):
    """Function to create a date

    :param y: Year
    :param m: Month
    :param d: Day
    :return: Date string in yyyymmdd format
    """
    # Convert year, month, day to integers and format them as two-digit numbers to create the date
    return "{:02d}{:02d}{:02d}".format(int(y), int(m), int(d))


def obj_2_dict(obj) -> dict:
    d = {}
    for field in [x for x in dir(obj) if not x.startswith("_") and x != "metadata"]:
        if field not in ["query_class", "from_dict", "to_dict", "query", "registry", "metadata", "to_form_dict"]:
            d[field] = obj.__getattribute__(field)
    return d


def custom_serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def toJson(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "toJson"):
        data_json = obj.toJson()
    elif isinstance(obj, [].__class__):
        arr = []
        for el in obj:
            # loads() is used to convert the string back to dict
            tmp = toJson(el)
            if tmp is str:
                arr.append(json.loads(tmp))
            else:
                arr.append(tmp)
        data_json = json.dumps(arr, default=custom_serialize)
    else:
        data_json = json.dumps(obj, default=custom_serialize)
    if data_json is dict:
        data_json = json.dumps(data_json)
    return data_json


def toDict(obj):
    if hasattr(obj, "toDict"):
        data_json = obj.toDict()
    elif isinstance(obj, [].__class__):
        arr = []
        for el in obj:
            # loads() is used to convert the string back to dict
            arr.append(toDict(el))
        data_json = json.dumps(arr)
    else:
        data_json = json.dumps(obj)
    return data_json


def isChinese(word):
    """Determine if the word is all Chinese characters"""
    for ch in word:
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


def isSingleBytes(word):
    """Determine if the word is single-byte characters"""
    for ch in word:
        if "\u0020" <= ch <= "\u007e" or "\uff61" <= ch <= "\uff9f":
            return True
    return False


_double_kana = re.compile("^[ァ-ヶ]+$")


def isDoubleKana(word):
    """Determine if the word is all double-byte Kana characters"""
    return re.fullmatch(_double_kana, word) is not None


def isDate(s: str = None, y: int = None, m: int = None, d: int = None):
    try:
        if s is not None:
            datetime.strptime(s, "%Y%m%d")
        else:
            date(y, m, d)
        return True
    except Exception:
        return False


_email_regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def isEmail(email):
    return re.fullmatch(_email_regex, email) is not None


def hasData(p) -> bool:
    if p is None:
        return False
    if p is str and len(p.strip()) == 0:
        return False
    return True
