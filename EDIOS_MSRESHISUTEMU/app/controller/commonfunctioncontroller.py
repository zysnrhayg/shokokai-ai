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


from app.dto.aiproposalgenerateapi.aiproposalgenerateapi_dto import AiproposalgenerateapiDto
from app.dto.aiproposalinitapi.aiproposalinitapi_dto import AiproposalinitapiDto
from app.dto.aiproposalregenerateapi.aiproposalregenerateapi_dto import AiproposalregenerateapiDto
from app.dto.knowledgesearchapi.knowledgesearchapi_dto import KnowledgesearchapiDto
from app.service.aiproposalgenerateapi.aiproposalgenerateapi_service import AiproposalgenerateapiService
from app.service.aiproposalinitapi.aiproposalinitapi_service import AiproposalinitapiService
from app.service.aiproposalregenerateapi.aiproposalregenerateapi_service import AiproposalregenerateapiService
from app.service.knowledgesearchapi.knowledgesearchapi_service import KnowledgesearchapiService

commonfunction_route = Blueprint("commonfunction_route", __name__)


#
# aiproposalgenerateapi - AI支援提案AI提案を生成 - サーバー関数
# @param aiproposalgenerateapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/aiproposalgenerateapi.do", methods=['POST'])

def aiproposalgenerateapi() :
	"""aiproposalgenerateapi - AI支援提案AI提案を生成 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	aiproposalgenerateapi_dto = AiproposalgenerateapiDto.dict_to_json(data)
	aiproposalgenerateapiVar_service = AiproposalgenerateapiService()

	aiproposalgenerateapiVar_service.aiproposalgenerateapi(aiproposalgenerateapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# aiproposalinitapi - AI支援提案画面初期表示 - サーバー関数
# @param aiproposalinitapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/aiproposalinitapi.do", methods=['POST'])

def aiproposalinitapi() :
	"""aiproposalinitapi - AI支援提案画面初期表示 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	aiproposalinitapi_dto = AiproposalinitapiDto.dict_to_json(data)
	aiproposalinitapiVar_service = AiproposalinitapiService()

	aiproposalinitapiVar_service.aiproposalinitapi(aiproposalinitapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# aiproposalregenerateapi - AI支援提案違う内容を見る - サーバー関数
# @param aiproposalregenerateapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/aiproposalregenerateapi.do", methods=['POST'])

def aiproposalregenerateapi() :
	"""aiproposalregenerateapi - AI支援提案違う内容を見る - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	aiproposalregenerateapi_dto = AiproposalregenerateapiDto.dict_to_json(data)
	aiproposalregenerateapiVar_service = AiproposalregenerateapiService()

	aiproposalregenerateapiVar_service.aiproposalregenerateapi(aiproposalregenerateapi_dto, jsonObj)
	
	return jsonObj.toJsonString()



#
# knowledgesearchapi - AI支援提案ナレッジを検索 - サーバー関数
# @param knowledgesearchapi_dto
# @param result
# @throws Exception
#

@commonfunction_route.route("/knowledgesearchapi.do", methods=['POST'])

def knowledgesearchapi() :
	"""knowledgesearchapi - AI支援提案ナレッジを検索 - サーバー関数"""

	data = request.get_json()
	jsonObj = JSONWFCObject()

	# validate parameter 371

	
#UnitedControllerBuilder 963

	knowledgesearchapi_dto = KnowledgesearchapiDto.dict_to_json(data)
	knowledgesearchapiVar_service = KnowledgesearchapiService()

	knowledgesearchapiVar_service.knowledgesearchapi(knowledgesearchapi_dto, jsonObj)
	
	return jsonObj.toJsonString()
