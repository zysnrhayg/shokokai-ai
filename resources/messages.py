messageMap = {}
error_csrf_invalid = "CSRF validation failed"
messageMap["error_csrf_invalid"] = error_csrf_invalid
error_internal = "Internal server error"
messageMap["error_internal"] = error_internal
error_operation_failed = "Operation failed"
messageMap["error_operation_failed"] = error_operation_failed
msg_delete_completed = "削除が完了しました。"
messageMap["msg_delete_completed"] = msg_delete_completed
msg_delete_primary_key_required = "主キーを設定していないため、システム管理者に確認してください。"
messageMap["msg_delete_primary_key_required"] = msg_delete_primary_key_required
msg_login_pwd_required = "パスワードを入力してください。"
messageMap["msg_login_pwd_required"] = msg_login_pwd_required
msg_login_userid_required = "IDを入力してください。"
messageMap["msg_login_userid_required"] = msg_login_userid_required
msg_session_timeout = "長時間利用されていないため、タイムアウトしました。再度ログインしてください。"
messageMap["msg_session_timeout"] = msg_session_timeout

def getMessageById(msgid) :
	if msgid not in messageMap:
		return msgid
	else :
		messaege = messageMap[msgid]
		return messaege
