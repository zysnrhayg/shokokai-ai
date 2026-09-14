from typing import Dict, List, Optional
from flask import request, session
import urllib.parse
from config import settings
import utils.config

# 初期化状態
_device_initialized = False
_system_param_initialized = False

# 判定用設定値
browser_with_encode: List[str] = []
browser_without_encode: List[str] = []
mobile_device: List[str] = []
mobile_app: List[str] = []
mobile_html: List[str] = []
system_param: Dict[str, str] = {}
logger = utils.config.global_log
def system_param_init():
    global system_param, _system_param_initialized
    if _system_param_initialized:
        return
    _system_param_initialized = True
    s_prefix = 'SYSTEM_PARAM'
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        system_param[value.upper()] = value.upper()
        i += 1

def device_init():
    global browser_with_encode, browser_without_encode, mobile_device, mobile_app, mobile_html, _device_initialized
    if _device_initialized:
        return
    _device_initialized = True
    s_prefix = 'BROWSER_WITH_ENCODE'
    browser_with_encode = []
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        browser_with_encode.append(value.upper())
        i += 1

    s_prefix = 'BROWSER_WITHOUT_ENCODE'
    browser_without_encode = []
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        browser_without_encode.append(value.upper())
        i += 1

    s_prefix = 'MOBILE_DEVICE'
    mobile_device = []
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        mobile_device.append(value.upper())
        i += 1

    s_prefix = 'MOBILE_APP'
    mobile_app = []
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        mobile_app.append(value.upper())
        i += 1

    s_prefix = 'MOBILE_HTML'
    mobile_html = []
    i = 1
    while True:
        value = get_config_value(f"{s_prefix}{i}")
        if not value:
            break
        mobile_html.append(value.upper())
        i += 1

def is_no_encode():
    user_agent = request.headers.get('User-Agent', '').strip()
    character_encoding = request.charset
    if character_encoding:
        return True
    return False

def get_mobile_device():
    user_agent = request.headers.get('User-Agent', '').strip()
    if not _device_initialized:
        device_init()
    
    for ua in mobile_device:
        if ua.upper() in user_agent.upper():
            return ua
    for ua in mobile_app:
        if ua.upper() in user_agent.upper():
            return ua
    return "WEB"

def is_mobile_device():
    user_agent = request.headers.get('User-Agent', '').strip()
    if not _device_initialized:
        device_init()
    
    for ua in mobile_device:
        if ua.upper() in user_agent.upper():
            return True
    return False

def is_mobile_app():
    user_agent = request.headers.get('User-Agent', '').strip()
    if not _device_initialized:
        device_init()
    
    for ua in mobile_app:
        if ua.upper() in user_agent.upper():
            for mh in mobile_html:
                if mh.upper() in user_agent.upper():
                    return False
            return True
    return False

def get_contents_of_session() -> Dict[str, str]:
    return {key: str(value) for key, value in session.items()}

def get_session_value(key: str) -> Optional[str]:
    return session.get(key)

def log_contents_of_session() -> str:
    sb = []
    sb.append("-------------------セッションの内容を抽出スタート-----------------")
    sb.append(f"Session Id: {session.get('_id')}")
    for key, val in session.items():
        sb.append(f"    Key: {key}        Value: {'NULL' if val is None else str(val)[:100]}")
    sb.append("-------------------セッションの内容を抽出エンド-------------------")
    return "\n".join(sb)

def clear_page_session(recogn_id: str):
    for key in list(session.keys()):
        if recogn_id in key:
            session.pop(key)

def get_parameter_by_utf8(param: str) -> Optional[str]:
    param_value = request.args.get(param)
    if param_value is None:
        return None
    if is_no_encode():
        return param_value
    try:
        return param_value.encode('iso-8859-1').decode('utf-8').strip()
    except UnicodeDecodeError:
        return None

def get_parameter_by_utf8_without_trim(param: str) -> Optional[str]:
    param_value = request.args.get(param)
    if param_value is None:
        return None
    if is_no_encode():
        return param_value
    try:
        return param_value.encode('iso-8859-1').decode('utf-8')
    except UnicodeDecodeError:
        return None

def escape_html_tags(value: str) -> str:
    import html
    return html.escape(value)

def get_parameter_by_utf8_escape_tag(param: str) -> Optional[str]:
    param_value = request.args.get(param)
    if param_value is None:
        return None
    if is_no_encode():
        return escape_html_tags(param_value)
    try:
        return escape_html_tags(param_value.encode('iso-8859-1').decode('utf-8').strip())
    except UnicodeDecodeError:
        return None

# 設定値取得処理。
def get_config_value(key: str) -> Optional[str]:
    # settings.toml または環境変数の設定値を取得する。
    value = settings.get(key)
    if value is None:
        return None
    return str(value)

def get_parameter_by_utf8(param_name, is_required=True):
    param = request.args.get(param_name, '')
    if not param:
        if is_required:
            logger.error("必須リクエストパラメータを取得できません: %s", param_name)
            raise ValueError(f"必須リクエストパラメータがありません: {param_name}")
        else:
            return ""
    try:
        return urllib.parse.unquote(param, encoding='utf-8').strip()
    except UnicodeDecodeError:
        logger.error("リクエストパラメータを UTF-8 として復号できません: %s", param_name)
        raise ValueError(f"リクエストパラメータの文字コードが不正です: {param_name}")

def get_parameter_by_utf8_escape_tag(param_name, is_required=True):
    param = get_parameter_by_utf8(param_name, is_required)
    if param:
        return escape_html_sql_tags(param)
    return param

def escape_html_sql_tags(value):
    from html import escape
    return escape(value)

def get_parameter_by_encode(param_name, encode='utf-8', is_required=True):
    param = request.args.get(param_name, '')
    if not param:
        if is_required:
            raise ValueError(f"{param_name} not found.")
        else:
            return ""
    try:
        return param.encode('iso-8859-1').decode(encode).strip()
    except UnicodeDecodeError:
        raise ValueError(f"{param_name} not found.")

def get_array_of_check_box(param_name):
    return request.args.getlist(param_name)

def get_array_of_check_box_by_utf8(param_name):
    values = get_array_of_check_box(param_name)
    return [get_parameter_by_utf8(value) for value in values]

def get_all_parameters_for_trace_log():
    sb = []
    sb.append("\n*-----Reading All Request Parameters-----*\n")
    sb.append(f"Session Id: {request.cookies.get('session_id')}\n")
    sb.append(f"CharacterEncoding: {request.charset}\n")
    sb.append(f"RemoteUser: {request.remote_user}\n")
    for param_name in request.args:
        param_values = request.args.getlist(param_name)
        if len(param_values) == 1:
            param_value = get_parameter_by_utf8(param_name)
            sb.append(f"{param_name}: {param_value}\n")
        else:
            for i, value in enumerate(param_values):
                sb.append(f"{' ' * (len(param_name) + 2)}{get_parameter_by_utf8(param_name)}\n")
    sb.append("*----------------------------------------*")
    return ''.join(sb)

def get_all_parameters_for_my_http_request():
    my_http_request = {}
    for param_name in request.args:
        param_values = request.args.getlist(param_name)
        if len(param_values) == 1:
            my_http_request[param_name] = get_parameter_by_utf8(param_name)
        else:
            my_http_request[param_name] = param_values
    return my_http_request

def get_all_parameters():
    sb = []
    sb.append("\n*-----Reading All Request Parameters-----*\n")
    sb.append(f"Session Id: {request.cookies.get('session_id')}\n")
    sb.append(f"CharacterEncoding: {request.charset}\n")
    sb.append(f"RemoteUser: {request.remote_user}\n")
    for param_name in request.args:
        param_values = request.args.getlist(param_name)
        if len(param_values) == 1:
            param_value = get_parameter_by_utf8(param_name)
            sb.append(f"{param_name}: {param_value}\n")
        else:
            for i, value in enumerate(param_values):
                sb.append(f"{' ' * (len(param_name) + 2)}{get_parameter_by_utf8(param_name)}\n")
    sb.append("*----------------------------------------*")
    return ''.join(sb)

def get_request_param(ori):
    if not ori:
        return {}
    arg = {}
    pairs = ori.split('&')
    for pair in pairs:
        kv = pair.split('=')
        arg[kv[0]] = kv[1]
    return arg

def check_prev_loc(prev_loc, page_id):
    if prev_loc:
        p = prev_loc.find("prevLoc=")
        if p > -1:
            v = prev_loc[:p]
            if "linkID" in v and "pageID=" in v:
                a = prev_loc[p + 8:]
                if "linkID" in a and "pageID=" in a:
                    p = a.find("prevLoc=")
                    preprepage = a[p + 8:]
                    p = preprepage.find("pageID=") + 7
                    e = preprepage.find("&amp;")
                    preprepage_id = preprepage[p:e]
                    if preprepage_id == page_id:
                        prev_loc = preprepage[p + 8:]
                        p = prev_loc.find("prevLoc=")
                        prev_loc = prev_loc[p + 8:]
                        try:
                            prev_loc = urllib.parse.unquote(prev_loc, encoding='utf-8')
                        except UnicodeDecodeError:
                            pass
                elif "saasforce.jsp" in a:
                    prev_loc = ""
            elif "fromHome" in v:
                prev_loc = ""
    return prev_loc

def access_url():
    p = request.path
    if p:
        p = p.replace("/w/", "").replace("/c/", "")
        try:
            o = ciphertest_passwd_deencrypt(p)
        except Exception as e:
            logger.error(f"Error decrypting path: {e}")
            return ""
        splitstr = "-@-@"
        if splitstr in o and len(o.split(splitstr)) >= 3:
            return p
    return ""

def ciphertest_passwd_deencrypt(p):
    # 復号方式がない状態で暗号文を平文として扱うことを禁止する。
    raise NotImplementedError("アップロードパスの復号方式が設定されていません。")

def get_request_info():
    try:
        return request.data.decode('utf-8')
    except UnicodeDecodeError:
        logger.exception("リクエスト本文を UTF-8 として読み込めません。")
        raise

def get_lang_id(session):
    language_id = session.get('language_id', '')
    if not language_id:
        langid = request.locale.language
        if langid == 'ja':
            language_id = 'JPN'
        elif langid == 'en':
            language_id = 'ENG'
        elif langid == 'zh':
            language_id = 'CHN'
        else:
            language_id = 'JPN'
    return language_id

def is_json_type():
    content_type = request.content_type
    return content_type and 'application/json' in content_type
