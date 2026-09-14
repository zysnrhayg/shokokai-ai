from voluptuous import Invalid, Datetime
import typing
#日付年月日　py_datecheck_hiduke.vm　（yyyy-MM-dd,yyyy/MM/dd）
import datetime
class DateCheckHiduke(object):
    DEFAULT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    _ALIAS_FORMATS = {
        "HH:mm": "%H:%M",
        "HH:mm:ss": "%H:%M:%S",
        "hh:mm": "%H:%M",
        "hh:mm:ss": "%H:%M:%S",
        "yyyy/MM/dd": "%Y/%m/%d",
        "yyyy-MM-dd": "%Y-%m-%d",
        "yyyy/MM/dd HH:mm": "%Y/%m/%d %H:%M",
        "yyyy/MM/dd HH:mm:ss": "%Y/%m/%d %H:%M:%S",
    }

    def __init__(
        self, format: typing.Optional[str] = None, msg: typing.Optional[str] = None
    ) -> None:
        self.format = format or self.DEFAULT_FORMAT
        self.msg = msg

    @classmethod
    def _normalize_strptime_format(cls, fmt: str) -> str:
        fmt = (fmt or "").strip()
        if not fmt:
            return fmt
        # 已经是 strptime 风格（包含 %）则直接使用
        if "%" in fmt:
            return fmt
        return cls._ALIAS_FORMATS.get(fmt, fmt)
    
    def __call__(self, v):
        if v == None or v == "" :
            return v
        ok = False
        formats = [self.format]
        if self.format == None or self.format == '':
            formats = ["%Y-%m-%d", "%Y/%m/%d"]
        elif ',' in self.format:
            # 多个格式用逗号分隔，避免单个格式中出现重复 %Y 导致 strptime 内部正则重复命名组 re.error
            formats = [f.strip() for f in self.format.split(',') if f.strip()]
        formats = [self._normalize_strptime_format(f) for f in formats]
        for fmt in formats:
            try:
              datetime.datetime.strptime(v, fmt)
              ok = True  # いずれかの形式に一致すればOK
            except (TypeError, ValueError):
               pass
        if ok == False:
            raise Invalid(
                    self.msg
            )
        else :
            return v  # いずれかの形式に一致すればOK
    def __repr__(self):
        return 'Date(format=%s)' % self.format
