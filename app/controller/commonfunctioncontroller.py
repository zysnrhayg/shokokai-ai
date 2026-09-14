from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template,session, Response
from flask_login import login_user, login_required, logout_user
import os
import json
import traceback
import utils.config
from utils.jsonwfc_object import JSONWFCObject
import utils.string_util
from utils.exception_util import ValidationError, NotFoundError, DBError
import resources.messages


from app.service.entryupdateapi.entryupdateapi_service import EntryupdateapiService
from app.service.dashboardinitapi.dashboardinitapi_service import DashboardinitapiService
from app.service.verify2faapi.verify2faapi_service import Verify2faapiService
from app.service.vectordetailinitapi.vectordetailinitapi_service import VectordetailinitapiService
from app.service.vectorforminitapi.vectorforminitapi_service import VectorforminitapiService
from app.service.vectorformnewinitapi.vectorformnewinitapi_service import VectorformnewinitapiService
from app.service.vectorsaveapi.vectorsaveapi_service import VectorsaveapiService
from app.service.vectorsinitapi.vectorsinitapi_service import VectorsinitapiService
from app.service.vectorsresyncapi.vectorsresyncapi_service import VectorsresyncapiService
from app.service.vectorupdateapi.vectorupdateapi_service import VectorupdateapiService
from app.dto.vectordetailinitapi.vectordetailinitapi_dto import VectordetailinitapiDto
from app.dto.vectorforminitapi.vectorforminitapi_dto import VectorforminitapiDto
from app.dto.vectorformnewinitapi.vectorformnewinitapi_dto import VectorformnewinitapiDto
from app.dto.vectorsaveapi.vectorsaveapi_dto import VectorsaveapiDto
from app.dto.vectorsinitapi.vectorsinitapi_dto import VectorsinitapiDto
from app.dto.vectorsresyncapi.vectorsresyncapi_dto import VectorsresyncapiDto
from app.dto.vectorupdateapi.vectorupdateapi_dto import VectorupdateapiDto

commonfunction_route = Blueprint('commonfunction_route', __name__)

#
# entriesinitapi - 知識データ一覧画面初期表示 - サーバー関数
# @param entriesinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entriesinitapi.do", methods=['POST'])

def entriesinitapi() :
	"""entriesinitapi - 知識データ一覧画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entriesinitapi_dto = EntriesinitapiDto.dict_to_json(data)
	entriesinitapiVar_service = EntriesinitapiService()

	entriesinitapiVar_service.entriesinitapi(entriesinitapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# entrydetailinitapi - 知識データ詳細画面初期表示 - サーバー関数
# @param entrydetailinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entrydetailinitapi.do", methods=['POST'])

def entrydetailinitapi() :
	"""entrydetailinitapi - 知識データ詳細画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entrydetailinitapi_dto = EntrydetailinitapiDto.dict_to_json(data)
	entrydetailinitapiVar_service = EntrydetailinitapiService()

	entrydetailinitapiVar_service.entrydetailinitapi(entrydetailinitapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# entryforminitapi - 知識データ編集編集 - サーバー関数
# @param entryforminitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entryforminitapi.do", methods=['POST'])

def entryforminitapi() :
	"""entryforminitapi - 知識データ編集編集 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entryforminitapi_dto = EntryforminitapiDto.dict_to_json(data)
	entryforminitapiVar_service = EntryforminitapiService()

	entryforminitapiVar_service.entryforminitapi(entryforminitapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# entryformnewinitapi - 知識データ新規＋ 知識データを登録 - サーバー関数
# @param entryformnewinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entryformnewinitapi.do", methods=['POST'])

def entryformnewinitapi() :
	"""entryformnewinitapi - 知識データ新規＋ 知識データを登録 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entryformnewinitapi_dto = EntryformnewinitapiDto.dict_to_json(data)
	entryformnewinitapiVar_service = EntryformnewinitapiService()

	entryformnewinitapiVar_service.entryformnewinitapi(entryformnewinitapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# entrysaveapi - 知識データ新規画面登録ボタン - サーバー関数
# @param entrysaveapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entrysaveapi.do", methods=['POST'])

def entrysaveapi() :
	"""entrysaveapi - 知識データ新規画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entrysaveapi_dto = EntrysaveapiDto.dict_to_json(data)
	entrysaveapiVar_service = EntrysaveapiService()

	entrysaveapiVar_service.entrysaveapi(entrysaveapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# entryupdateapi - 知識データ編集画面登録ボタン - サーバー関数
# @param entryupdateapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/entryupdateapi.do", methods=['POST'])

def entryupdateapi() :
	"""entryupdateapi - 知識データ編集画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	entryupdateapi_dto = EntryupdateapiDto.dict_to_json(data)
	entryupdateapiVar_service = EntryupdateapiService()

	entryupdateapiVar_service.entryupdateapi(entryupdateapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# dashboardinitapi - ダッシュボード（商工会）ダッシュボードを開く（初期データ取 - サーバー関数
# @param dashboardinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/dashboardinitapi.do", methods=['POST'])

def dashboardinitapi() :
	"""dashboardinitapi - ダッシュボード（商工会）ダッシュボードを開く（初期データ取 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	dashboardinitapi_dto = DashboardinitapiDto.dict_to_json(data)
	dashboardinitapiVar_service = DashboardinitapiService()

	dashboardinitapiVar_service.dashboardinitapi(dashboardinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# loginapi - ログイン画面ログインボタン - サーバー関数
# @param loginapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/loginapi.do", methods=['POST'])

def loginapi() :
	"""loginapi - ログイン画面ログインボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	loginapi_dto = LoginapiDto.dict_to_json(data)
	loginapiVar_service = LoginapiService()

	loginapiVar_service.loginapi(loginapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# logininitapi - ログイン画面 - サーバー関数
# @param logininitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/logininitapi.do", methods=['POST'])

def logininitapi() :
	"""logininitapi - ログイン画面 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	logininitapi_dto = LogininitapiDto.dict_to_json(data)
	logininitapiVar_service = LogininitapiService()

	logininitapiVar_service.logininitapi(logininitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# logoutapi - ログアウト - サーバー関数
# @param logoutapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/logoutapi.do", methods=['POST'])

def logoutapi() :
	"""logoutapi - ログアウト - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	logoutapi_dto = LogoutapiDto.dict_to_json(data)
	logoutapiVar_service = LogoutapiService()

	logoutapiVar_service.logoutapi(logoutapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# verify2faapi - 二要素認証画面認証ボタン - サーバー関数
# @param verify2faapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/verify2faapi.do", methods=['POST'])

def verify2faapi() :
	"""verify2faapi - 二要素認証画面認証ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	verify2faapi_dto = Verify2faapiDto.dict_to_json(data)
	verify2faapiVar_service = Verify2faapiService()

	verify2faapiVar_service.verify2faapi(verify2faapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectordetailinitapi - ベクトル詳細画面初期表示 - サーバー関数
# @param vectordetailinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectordetailinitapi.do", methods=['POST'])

def vectordetailinitapi() :
	"""vectordetailinitapi - ベクトル詳細画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectordetailinitapi_dto = VectordetailinitapiDto.dict_to_json(data)
	vectordetailinitapiVar_service = VectordetailinitapiService()

	vectordetailinitapiVar_service.vectordetailinitapi(vectordetailinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorforminitapi - ベクトルコレクション編集編集 - サーバー関数
# @param vectorforminitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorforminitapi.do", methods=['POST'])

def vectorforminitapi() :
	"""vectorforminitapi - ベクトルコレクション編集編集 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorforminitapi_dto = VectorforminitapiDto.dict_to_json(data)
	vectorforminitapiVar_service = VectorforminitapiService()

	vectorforminitapiVar_service.vectorforminitapi(vectorforminitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorformnewinitapi - ベクトルコレクション新規＋ コレクションを登録 - サーバー関数
# @param vectorformnewinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorformnewinitapi.do", methods=['POST'])

def vectorformnewinitapi() :
	"""vectorformnewinitapi - ベクトルコレクション新規＋ コレクションを登録 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorformnewinitapi_dto = VectorformnewinitapiDto.dict_to_json(data)
	vectorformnewinitapiVar_service = VectorformnewinitapiService()

	vectorformnewinitapiVar_service.vectorformnewinitapi(vectorformnewinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorsaveapi - ベクトル新規画面登録ボタン - サーバー関数
# @param vectorsaveapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorsaveapi.do", methods=['POST'])

def vectorsaveapi() :
	"""vectorsaveapi - ベクトル新規画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorsaveapi_dto = VectorsaveapiDto.dict_to_json(data)
	vectorsaveapiVar_service = VectorsaveapiService()

	vectorsaveapiVar_service.vectorsaveapi(vectorsaveapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorsinitapi - ベクトル一覧画面初期表示 - サーバー関数
# @param vectorsinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorsinitapi.do", methods=['POST'])

def vectorsinitapi() :
	"""vectorsinitapi - ベクトル一覧画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorsinitapi_dto = VectorsinitapiDto.dict_to_json(data)
	vectorsinitapiVar_service = VectorsinitapiService()

	vectorsinitapiVar_service.vectorsinitapi(vectorsinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorsresyncapi - ベクトル一覧画面再同期ボタン - サーバー関数
# @param vectorsresyncapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorsresyncapi.do", methods=['POST'])

def vectorsresyncapi() :
	"""vectorsresyncapi - ベクトル一覧画面再同期ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorsresyncapi_dto = VectorsresyncapiDto.dict_to_json(data)
	vectorsresyncapiVar_service = VectorsresyncapiService()

	vectorsresyncapiVar_service.vectorsresyncapi(vectorsresyncapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# vectorupdateapi - ベクトル編集画面登録ボタン - サーバー関数
# @param vectorupdateapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/vectorupdateapi.do", methods=['POST'])

def vectorupdateapi() :
	"""vectorupdateapi - ベクトル編集画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	vectorupdateapi_dto = VectorupdateapiDto.dict_to_json(data)
	vectorupdateapiVar_service = VectorupdateapiService()

	vectorupdateapiVar_service.vectorupdateapi(vectorupdateapi_dto, jsonObj)

	return jsonObj.toJsonString()


