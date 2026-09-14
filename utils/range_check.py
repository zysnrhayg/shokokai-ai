import typing
import datetime
from voluptuous.error import (
  Invalid
)
if typing.TYPE_CHECKING:
    from _typeshed import SupportsAllComparisons
class RangeCheck(object):
    

    def __init__(
        self,
        min:   None,
        max:   None,
        msg:  None,
    ) -> None:
        self.min = min
        self.max = max
        self.msg = msg

    def __call__(self, v):
        try:
            if v == None or v == '' :
                return v
            try:
                value = int(v)
                minValue = int(self.min)
                maValue = int(self.max)
                if value >= minValue and value <= maValue :
                    return v
                else :
                    raise Invalid(
                        self.msg or 'invalid value or type (must have a partial ordering)'
                    ) 
            except ValueError as e:
                formatDate = "%Y-%m-%d"
                dateChek = None
                dateMin = None
                dateMax = None
                if "/" in v :
                    formatDate = "%Y/%m/%d"
                dateChek = datetime.datetime.strptime(v, formatDate).date()
                if "/" in self.min :
                    formatDate = "%Y/%m/%d"
                dateMin = datetime.datetime.strptime(self.min, formatDate).date()   
                if "/" in self.max :
                    formatDate = "%Y/%m/%d"  
                dateMax = datetime.datetime.strptime(self.max, formatDate).date()
                if dateChek >= dateMin and dateChek <= dateMax:
                    return v
                else :
                    raise Invalid(
                        self.msg or 'invalid value or type (must have a partial ordering)'
                    ) 
        # Objects that lack a partial ordering, e.g. None or strings will raise TypeError
        except TypeError:
            raise Invalid(
                self.msg or 'invalid value or type (must have a partial ordering)'
            )

    def __repr__(self):
        return 'RangeCheck(min=%r, max=%r, msg=%r)' % (
            self.min,
            self.max,
            self.msg,
        )
