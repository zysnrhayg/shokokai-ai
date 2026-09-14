from voluptuous import Invalid, Datetime
import typing
#日付比較　py_datecheck_hiduke_compare.vm
import datetime
class DateCheckHidukeCompare(object):
    DEFAULT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(
        self, format: typing.Optional[str] = None, msg: typing.Optional[str] = None
    ) -> None:
        self.format = format or self.DEFAULT_FORMAT
        self.msg = msg
    
    def __call__(self, v):
        if v == None or v == "" :
            return v
        try:
            today = datetime.date.today()
            datetime_object = None
            if '-' in v :
                datetime_object = datetime.datetime.strptime(v, "%Y-%m-%d").date()
            elif '/' in v :
                datetime_object = datetime.datetime.strptime(v, "%Y/%m/%d").date()
            if self.format == '>' :
                if (datetime_object > today) == True :
                    return datetime_object > today
                else :
                    raise Invalid( self.msg)
            elif self.format == '<' :
                if (datetime_object < today) == True :
                    return datetime_object < today
                else :
                    raise Invalid( self.msg)
            elif self.format == '=' :
                 if (datetime_object == today) == True :
                    return datetime_object == today
                 else :
                    raise Invalid( self.msg)
            elif self.format == '>=' :
                 if (datetime_object >= today) == True :
                    return datetime_object >= today
                 else :
                    raise Invalid( self.msg)
            elif self.format == '<=' :
                 if (datetime_object <= today) == True :
                    return datetime_object <= today
                 else :
                    raise Invalid( self.msg)
        except (TypeError, ValueError):
            raise Invalid( self.msg)
        return False
    def __repr__(self):
        return 'Date(format=%s)' % self.format
