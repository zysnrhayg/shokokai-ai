#save_data_check_utils.py
#py_save_data_check_utils.vm check save data util method
import re

class SaveDataCheckUtil:
    @staticmethod
    def getCheckItem_str(item):
        return f"項目「{item or ''}」："

    @staticmethod
    def getNoSaveItemErr():
        return "全ての項目が非DB保存項目になっています。"

    @staticmethod
    def getPriKeyNotDefinition_err(field_id):
        return f"{SaveDataCheckUtil.getCheckItem_str(field_id)}対象テーブルのキー項目が画面に定義されていません。\n"

    @staticmethod
    def getKeyRepeatErr(table_id):
        return f"「{table_id}」該当するデータが既に存在します。\n"

    @staticmethod
    def getKeyNullCheckErr(value, item_name):
        if not value:
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}キー項目に空白が設定されています。\n"
        return ''

    @staticmethod
    def getMustNullCheckErr(value, item_name):
        if not value:
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}必須項目に入力していません。\n"
        return ''

    @staticmethod
    def getNotNullCheckErr(value, item_name):
        if not value:
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}非空項目に入力していません。\n"
        return ''

    @staticmethod
    def getMaxLengthCheckErr(value, int_max_len, item_name):
        if int_max_len != 0 and len(value) > int_max_len:
            return (f"{SaveDataCheckUtil.getCheckItem_str(item_name)}該当項目の長さを超えて入力されています。"
                    f"入力値:({value or ''}) 最大長さ:({int_max_len})\n")
        return ''

    @staticmethod
    def getMinLengthCheckErr(value, int_min_len, item_name):
        if int_min_len != 0 and len(value) < int_min_len:
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}最小長さより短い値が入力されています。\n"
        return ''

    @staticmethod
    def getRegexCheckErr(value, regex, item_name):
        if value and regex and not re.match(regex, value):
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}入力の内容が正しくありません。\n"
        return ''

    @staticmethod
    def getDateCheckErr(value, item_name):
        date_regex = r'^\d{4}/\d{2}/\d{2}$'  # 模拟日期格式检查 [yyyy/mm/dd]
        if value and not re.match(date_regex, value):
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}入力された日付が正しくありません。[yyyy/mm/dd]の形式で入力してください。\n"
        return ''

    @staticmethod
    def getTimeCheckErr(value, item_name):
        # 支持 [hh:mm:ss] 与 [hh:mm]（画面常传 12:00、16:00）
        if not value:
            return ''
        if not isinstance(value, str):
            value = str(value).strip()
        time_regex_ss = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        time_regex_mm = re.compile(r'^\d{2}:\d{2}$')
        if time_regex_ss.match(value) or time_regex_mm.match(value):
            return ''
        return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}入力された時刻が正しくありません。[hh:mm:ss]の形式で入力してください。\n"

    @staticmethod
    def getEmailCheckErr(value, item_name):
        if not value:
            return ''
        from utils.lang_util import isEmail
        if not isEmail(value):
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}メールアドレスの形式が正しくありません。\n"
        return ''

    @staticmethod
    def getDatetimeCheckErr(value, item_name):
        datetime_regex = r'^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$'  # 模拟日期时间格式检查 [yyyy/mm/dd hh:mm:ss]
        if value and not re.match(datetime_regex, value):
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}入力された日時が正しくありません。[yyyy/mm/dd hh:mm:ss]の形式で入力してください。\n"
        return ''

    @staticmethod
    def getIntCheckErr(value, item_name):
        if not value:
            return ''
        if isinstance(value, int):
            return ''  # 整数视为通过
        s = str(value).strip()
        if not s or s.isdigit():
            return ''
        return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}整数以外の文字が入っています。※0123456789の数字のみ入力可能です。\n"

    @staticmethod
    def getDoubleCheckErr(value, item_name):
        try:
            if value:
                float(value)  # 检查是否为有效的浮点数
        except ValueError:
            return f"{SaveDataCheckUtil.getCheckItem_str(item_name)}数字以外の文字が入っています。\n"
        return ''

    @staticmethod
    def addMsg(msg, s_buffer):
        if msg and s_buffer is not None:
            s_buffer.append(msg)
