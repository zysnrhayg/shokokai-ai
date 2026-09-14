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
from app.service.monthlyinitapi.monthlyinitapi_service import MonthlyinitapiService
from app.service.monthlyfiscalyearapi.monthlyfiscalyearapi_service import MonthlyfiscalyearapiService
from app.service.monthlyexportapi.monthlyexportapi_service import MonthlyexportapiService
from app.dto.vectordetailinitapi.vectordetailinitapi_dto import VectordetailinitapiDto
from app.dto.vectorforminitapi.vectorforminitapi_dto import VectorforminitapiDto
from app.dto.vectorformnewinitapi.vectorformnewinitapi_dto import VectorformnewinitapiDto
from app.dto.vectorsaveapi.vectorsaveapi_dto import VectorsaveapiDto
from app.dto.vectorsinitapi.vectorsinitapi_dto import VectorsinitapiDto
from app.dto.vectorsresyncapi.vectorsresyncapi_dto import VectorsresyncapiDto
from app.dto.vectorupdateapi.vectorupdateapi_dto import VectorupdateapiDto
from app.dto.monthlyinitapi.monthlyinitapi_dto import MonthlyinitapiDto
from app.dto.monthlyfiscalyearapi.monthlyfiscalyearapi_dto import MonthlyfiscalyearapiDto
from app.dto.monthlyexportapi.monthlyexportapi_dto import MonthlyexportapiDto
from app.service.aiformatapi.aiformatapi_service import AiformatapiService
from app.service.draftsaveapi.draftsaveapi_service import DraftsaveapiService
from app.service.voiceextendapi.voiceextendapi_service import VoiceextendapiService
from app.service.voiceinsertcontentapi.voiceinsertcontentapi_service import VoiceinsertcontentapiService
from app.service.voicerecordapi.voicerecordapi_service import VoicerecordapiService
from app.service.voiceuploadapi.voiceuploadapi_service import VoiceuploadapiService
from app.dto.aiformatapi.aiformatapi_dto import AiformatapiDto
from app.dto.aiinputinitapi.aiinputinitapi_dto import AiinputinitapiDto
from app.dto.draftsaveapi.draftsaveapi_dto import DraftsaveapiDto
from app.dto.voiceextendapi.voiceextendapi_dto import VoiceextendapiDto
from app.dto.voiceinsertcontentapi.voiceinsertcontentapi_dto import VoiceinsertcontentapiDto
from app.dto.voicerecordapi.voicerecordapi_dto import VoicerecordapiDto
from app.dto.voiceuploadapi.voiceuploadapi_dto import VoiceuploadapiDto
from app.service.knowledgeinitapi.knowledgeinitapi_service import KnowledgeinitapiService
from app.service.documentdetailinitapi.documentdetailinitapi_service import DocumentdetailinitapiService
from app.service.documentforminitapi.documentforminitapi_service import DocumentforminitapiService
from app.service.documentformnewinitapi.documentformnewinitapi_service import DocumentformnewinitapiService
from app.service.documentsaveapi.documentsaveapi_service import DocumentsaveapiService
from app.service.documentupdateapi.documentupdateapi_service import DocumentupdateapiService
from app.service.documentversiondownloadapi.documentversiondownloadapi_service import DocumentversiondownloadapiService
from app.service.documentversionnewapi.documentversionnewapi_service import DocumentversionnewapiService
from app.dto.knowledgeinitapi.knowledgeinitapi_dto import KnowledgeinitapiDto
from app.dto.documentdetailinitapi.documentdetailinitapi_dto import DocumentdetailinitapiDto
from app.dto.documentforminitapi.documentforminitapi_dto import DocumentforminitapiDto
from app.dto.documentformnewinitapi.documentformnewinitapi_dto import DocumentformnewinitapiDto
from app.dto.documentsaveapi.documentsaveapi_dto import DocumentsaveapiDto
from app.dto.documentupdateapi.documentupdateapi_dto import DocumentupdateapiDto
from app.dto.documentversiondownloadapi.documentversiondownloadapi_dto import DocumentversiondownloadapiDto
from app.dto.documentversionnewapi.documentversionnewapi_dto import DocumentversionnewapiDto

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



#
# monthlyexportapi - 月次報告月次帳票出力 - サーバー関数
# @param monthlyexportapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/monthlyexportapi.do", methods=['POST'])

def monthlyexportapi() :
	"""monthlyexportapi - 月次報告月次帳票出力 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	monthlyexportapi_dto = MonthlyexportapiDto.dict_to_json(data)
	monthlyexportapiVar_service = MonthlyexportapiService()

	monthlyexportapiVar_service.monthlyexportapi(monthlyexportapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# monthlyfiscalyearapi - 月次報告年度切替 - サーバー関数
# @param monthlyfiscalyearapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/monthlyfiscalyearapi.do", methods=['POST'])

def monthlyfiscalyearapi() :
	"""monthlyfiscalyearapi - 月次報告年度切替 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	monthlyfiscalyearapi_dto = MonthlyfiscalyearapiDto.dict_to_json(data)
	monthlyfiscalyearapiVar_service = MonthlyfiscalyearapiService()

	monthlyfiscalyearapiVar_service.monthlyfiscalyearapi(monthlyfiscalyearapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# monthlyinitapi - 月次報告画面初期表示 - サーバー関数
# @param monthlyinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/monthlyinitapi.do", methods=['POST'])

def monthlyinitapi() :
	"""monthlyinitapi - 月次報告画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	monthlyinitapi_dto = MonthlyinitapiDto.dict_to_json(data)
	monthlyinitapiVar_service = MonthlyinitapiService()

	monthlyinitapiVar_service.monthlyinitapi(monthlyinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# aiformatapi - 傾聴内容変換AI文字起こし AI整形 - サーバー関数
# @param aiformatapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/aiformatapi.do", methods=['POST'])

def aiformatapi() :
	"""aiformatapi - 傾聴内容変換AI文字起こし AI整形 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	aiformatapi_dto = AiformatapiDto.dict_to_json(data)
	aiformatapiVar_service = AiformatapiService()

	aiformatapiVar_service.aiformatapi(aiformatapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# aiinputinitapi - 傾聴内容変換AI画面初期表示 - サーバー関数
# @param aiinputinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/aiinputinitapi.do", methods=['POST'])

def aiinputinitapi() :
	"""aiinputinitapi - 傾聴内容変換AI画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	aiinputinitapi_dto = AiinputinitapiDto.dict_to_json(data)
	aiinputinitapiVar_service = AiinputinitapiService()

	aiinputinitapiVar_service.aiinputinitapi(aiinputinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# draftsaveapi - 傾聴内容変換AI下書き保存 - サーバー関数
# @param draftsaveapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/draftsaveapi.do", methods=['POST'])

def draftsaveapi() :
	"""draftsaveapi - 傾聴内容変換AI下書き保存 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	draftsaveapi_dto = DraftsaveapiDto.dict_to_json(data)
	draftsaveapiVar_service = DraftsaveapiService()

	draftsaveapiVar_service.draftsaveapi(draftsaveapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# formexportapi - 傾聴内容変換AI帳票出力 - サーバー関数
# @param formexportapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/formexportapi.do", methods=['POST'])

def formexportapi() :
	"""formexportapi - 傾聴内容変換AI帳票出力 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	formexportapi_dto = FormexportapiDto.dict_to_json(data)
	formexportapiVar_service = FormexportapiService()

	formexportapiVar_service.formexportapi(formexportapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# voiceextendapi - 傾聴内容変換AI録音時間 ＋30分延長 - サーバー関数
# @param voiceextendapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/voiceextendapi.do", methods=['POST'])

def voiceextendapi() :
	"""voiceextendapi - 傾聴内容変換AI録音時間 ＋30分延長 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	voiceextendapi_dto = VoiceextendapiDto.dict_to_json(data)
	voiceextendapiVar_service = VoiceextendapiService()

	voiceextendapiVar_service.voiceextendapi(voiceextendapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# voiceinsertcontentapi - 傾聴内容変換AI文字起こしを内容欄に反映 - サーバー関数
# @param voiceinsertcontentapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/voiceinsertcontentapi.do", methods=['POST'])

def voiceinsertcontentapi() :
	"""voiceinsertcontentapi - 傾聴内容変換AI文字起こしを内容欄に反映 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	voiceinsertcontentapi_dto = VoiceinsertcontentapiDto.dict_to_json(data)
	voiceinsertcontentapiVar_service = VoiceinsertcontentapiService()

	voiceinsertcontentapiVar_service.voiceinsertcontentapi(voiceinsertcontentapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# voicerecordapi - 傾聴内容変換AI音声録音 開始／停止 - サーバー関数
# @param voicerecordapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/voicerecordapi.do", methods=['POST'])

def voicerecordapi() :
	"""voicerecordapi - 傾聴内容変換AI音声録音 開始／停止 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	voicerecordapi_dto = VoicerecordapiDto.dict_to_json(data)
	voicerecordapiVar_service = VoicerecordapiService()

	voicerecordapiVar_service.voicerecordapi(voicerecordapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# voiceuploadapi - 傾聴内容変換AI音声ファイル アップロード - サーバー関数
# @param voiceuploadapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/voiceuploadapi.do", methods=['POST'])

def voiceuploadapi() :
	"""voiceuploadapi - 傾聴内容変換AI音声ファイル アップロード - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	voiceuploadapi_dto = VoiceuploadapiDto.dict_to_json(data)
	voiceuploadapiVar_service = VoiceuploadapiService()

	voiceuploadapiVar_service.voiceuploadapi(voiceuploadapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentdetailinitapi - ナレッジ文書詳細画面初期表示 - サーバー関数
# @param documentdetailinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentdetailinitapi.do", methods=['POST'])

def documentdetailinitapi() :
	"""documentdetailinitapi - ナレッジ文書詳細画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentdetailinitapi_dto = DocumentdetailinitapiDto.dict_to_json(data)
	documentdetailinitapiVar_service = DocumentdetailinitapiService()

	documentdetailinitapiVar_service.documentdetailinitapi(documentdetailinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentforminitapi - ナレッジ文書編集編集 - サーバー関数
# @param documentforminitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentforminitapi.do", methods=['POST'])

def documentforminitapi() :
	"""documentforminitapi - ナレッジ文書編集編集 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentforminitapi_dto = DocumentforminitapiDto.dict_to_json(data)
	documentforminitapiVar_service = DocumentforminitapiService()

	documentforminitapiVar_service.documentforminitapi(documentforminitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentformnewinitapi - ナレッジ文書新規＋ 文書を登録 - サーバー関数
# @param documentformnewinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentformnewinitapi.do", methods=['POST'])

def documentformnewinitapi() :
	"""documentformnewinitapi - ナレッジ文書新規＋ 文書を登録 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentformnewinitapi_dto = DocumentformnewinitapiDto.dict_to_json(data)
	documentformnewinitapiVar_service = DocumentformnewinitapiService()

	documentformnewinitapiVar_service.documentformnewinitapi(documentformnewinitapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentsaveapi - ナレッジ文書新規画面登録ボタン - サーバー関数
# @param documentsaveapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentsaveapi.do", methods=['POST'])

def documentsaveapi() :
	"""documentsaveapi - ナレッジ文書新規画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentsaveapi_dto = DocumentsaveapiDto.dict_to_json(data)
	documentsaveapiVar_service = DocumentsaveapiService()

	documentsaveapiVar_service.documentsaveapi(documentsaveapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentupdateapi - ナレッジ文書編集画面登録ボタン - サーバー関数
# @param documentupdateapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentupdateapi.do", methods=['POST'])

def documentupdateapi() :
	"""documentupdateapi - ナレッジ文書編集画面登録ボタン - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentupdateapi_dto = DocumentupdateapiDto.dict_to_json(data)
	documentupdateapiVar_service = DocumentupdateapiService()

	documentupdateapiVar_service.documentupdateapi(documentupdateapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentversiondownloadapi - ナレッジ文書詳細⬇ ダウンロード - サーバー関数
# @param documentversiondownloadapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentversiondownloadapi.do", methods=['POST'])

def documentversiondownloadapi() :
	"""documentversiondownloadapi - ナレッジ文書詳細⬇ ダウンロード - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentversiondownloadapi_dto = DocumentversiondownloadapiDto.dict_to_json(data)
	documentversiondownloadapiVar_service = DocumentversiondownloadapiService()

	documentversiondownloadapiVar_service.documentversiondownloadapi(documentversiondownloadapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# documentversionnewapi - ナレッジ文書詳細画面版登録 - サーバー関数
# @param documentversionnewapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/documentversionnewapi.do", methods=['POST'])

def documentversionnewapi() :
	"""documentversionnewapi - ナレッジ文書詳細画面版登録 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	documentversionnewapi_dto = DocumentversionnewapiDto.dict_to_json(data)
	documentversionnewapiVar_service = DocumentversionnewapiService()

	documentversionnewapiVar_service.documentversionnewapi(documentversionnewapi_dto, jsonObj)

	return jsonObj.toJsonString()



#
# knowledgeinitapi - ナレッジ文書一覧画面初期表示 - サーバー関数
# @param knowledgeinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/knowledgeinitapi.do", methods=['POST'])

def knowledgeinitapi() :
	"""knowledgeinitapi - ナレッジ文書一覧画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371


#UnitedControllerBuilder 963

	knowledgeinitapi_dto = KnowledgeinitapiDto.dict_to_json(data)
	knowledgeinitapiVar_service = KnowledgeinitapiService()

	knowledgeinitapiVar_service.knowledgeinitapi(knowledgeinitapi_dto, jsonObj)

	return jsonObj.toJsonString()


