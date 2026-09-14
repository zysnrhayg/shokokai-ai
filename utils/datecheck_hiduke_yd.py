from voluptuous import Invalid, Datetime
import typing
#日付年月　py_datecheck_hiduke_ny.vm (YYYY/MM)、(YYYY-MM)、(YYYY.MM)
import datetime
class DateCheckHidukeGeTuNiChi(object):
    DEFAULT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(
        self, format: typing.Optional[str] = None, msg: typing.Optional[str] = None
    ) -> None:
        self.format = format or self.DEFAULT_FORMAT
        self.msg = msg
    
    def __call__(self, v):
        if v == None or v == "" :
            return v
        if "." in self.format or "-" in self.format :
            pass
        else:
            self.format = self.format.replace("/","")
            v =v.replace("/","")
        try:
            datetime.datetime.strptime(v, self.format)
        except (TypeError, ValueError):
            raise Invalid(
                self.msg
            )	
        return v
    
    def __repr__(self):
        return 'Date(format=%s)' % self.format
