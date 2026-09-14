import logging
from typing import Optional

logger = logging.getLogger(__name__)


class PageLabelUtil:
    """Placeholder page-label helper. Loads no bundles by default (extend to wire real i18n)."""

    MSG_CHANGE_CHAR = "@@"
    MSG_CHANGE_CHAR1 = "@1"
    MSG_CHANGE_CHAR2 = "@2"
    MSG_CHANGE_CHAR3 = "@3"
    MSG_CHANGE_CHAR4 = "@4"

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PageLabelUtil, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.prb_jpn = {}
        self.prb_chn = {}
        self.prb_eng = {}

    def _get_string(self, langid: Optional[str], key: str) -> str:
        if not langid or langid == "JPN":
            return self.prb_jpn.get(key, "")
        if langid == "CHN":
            return self.prb_chn.get(key, "")
        if langid == "ENG":
            return self.prb_eng.get(key, "")
        return self.prb_jpn.get(key, "")

    def get_page_label(self, key: str) -> Optional[str]:
        res = self._get_string("JPN", key)
        return res or None

    def get_page_label_with_lang(self, langid: str, key: str) -> Optional[str]:
        res = self._get_string(langid, key)
        if not res:
            return ""
        return res

    def get_page_label_with_lang_default(self, langid: str, key: str, default_value: str) -> str:
        res = self._get_string(langid, key)
        if not res:
            return default_value
        return res

    def get_page_label_with_code(self, langid: str, key: str) -> Optional[str]:
        res = self._get_string(langid, key)
        if not res:
            return None
        if "." in key:
            code = key.split(".")[1]
            return f"{res}[{code}]"
        return f"{res}[{key}]"

    def get_replace_message(self, message_id: str, char_string: str, replace: str, lang_id: str) -> str:
        message = self.get_page_label_with_lang(lang_id, message_id)
        if message:
            return message.replace(char_string, replace)
        return ""

    def get_contents_with_info(self, message_id: str, message_info: str, lang_id: str) -> str:
        message = self.get_page_label_with_lang(lang_id, message_id)
        if message:
            return f"{message}\n{message_info}"
        return message_info
