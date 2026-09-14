from voluptuous import Invalid, Datetime
import typing
#日付月日　py_datecheck_hiduke_yd.vm (MMDD,MM/DD)、(MM-DD)、(MM.DD)
import datetime
class DateCheckHidukeNeGaTu(object):
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
            datetime.datetime.strptime(v, self.format)
        except (TypeError, ValueError):
            raise Invalid(
                self.msg
            )
        return v
    def __repr__(self):
        return 'Date(format=%s)' % self.format
