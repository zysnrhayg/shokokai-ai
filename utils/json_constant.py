# constants.py

# The module contains a set of string constants used as identifiers in JSON responses and requests.
# These constants define various types of information such as error messages, success messages,
# URLs, HTML content, script actions, and more. Additionally, it includes constants for dropdown lists,
# asynchronous processing status flags, and server-side execution results.

JSONID_ERR = "e"  # エラー
JSONID_MSG = "i"  # メッセージ
JSONID_SUCCESS = "c"  # 成功のメッセージ
JSONID_INFO = "ei"  # エラーと情報系メッセージを詳細画面のserverInformに表示
JSONID_DATA = "b"  # body
JSONID_NUM = "s"  # 採番戻り

JSONID_URL = "u"  # URL
JSONID_MAP = "m"  # hashmap
JSONID_HTML = "h"  # html
JSONID_VALUE = "v"  # value
JSONID_REPLACE_SCRIPT = "p"  # スクリプト変え
JSONID_RUN_SCRIPT = "r"  # スクリプト実行
JSONID_DEFINE_SCRIPT = "f"  # スクリプト定義
JSONID_NEXT_FUNC_CONTINUE = "n"  # Ajax処理後のスクリプトを実行するかどうか定義

JSONID_ASYNC_RUN_STATUS = "a"  # 非同期処理時のステータスフラグ　非同期処理中にずっと返す
JSONID_ASYNC_REPORT_STATUS = "p"  # 非同期帳票出力時のステータスフラグ　非同期処理中にずっと返す

DROPDOWNLIST_WITH_NULL = "20"  # 空白付けてドロップリスト
DROPDOWNLIST_NO_NULL = "21"  # 空白なしてドロップリスト
JSONID_DROPDOWNLIST_FILTER_RESULT = "filter_result"
JSONID_DROPDOWNLIST_FIELTER_TARGET = "filter_target"

JSONID_FOR_RUNRESULT = "WF_RUNRESULT"  # サーバー側実行結果 0:初期値、1:成功 -1:失敗

RUNRESULT_SUCCESS = "1"  # サーバー側実行結果 0:初期値、1:成功 -1:失敗
RUNRESULT_FAIL = "-1"  # サーバー側実行結果 0:初期値、1:成功 -1:失敗

# For export API
JSONID_FILENAME = "FileName"
JSONID_FILESIZE = "FileSize"
JSONID_FILECREATEDTM = "FileCreateDateTime"
