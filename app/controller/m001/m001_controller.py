from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template,session, Response, send_file
from flask_login import login_user, login_required, logout_user
import os
import json
import traceback
import utils.config
from utils.jsonwfc_object import JSONWFCObject
import utils.string_util
from utils.exception_util import ValidationError, NotFoundError, DBError
import resources.messages
from urllib.parse import unquote
import os.path




from app.dto.m001.m001_dto import M001Dto
from app.service.m001.m001init_service import M001initService
import utils.session_constant



m001_route = Blueprint('m001_route', __name__)
#
# EDI請求管理システム
# class: m001controller
# page: 会社詳細
#

@m001_route.route("/M001", methods=["GET"])
def m001_page():
	if session.get(utils.session_constant.USER_ID, "") == "":
		return redirect(url_for("index"))
	return redirect("/#home")


#
# m001 - 会社詳細 - 画面初期化
# @param m001_dto
# @param result
# @throws Exception
#
@m001_route.route("/M001Init.do", methods=["POST"])


def m001init() :
	"""m001 - 会社詳細 - 画面初期化"""
	data = request.get_json()
	# json 176
	m001_dto = M001Dto.dict_to_json(data)
	m001init_serviceVar = M001initService()
	jsonObjDe = m001init_serviceVar.sm001init(m001_dto)
	jsonObj = jsonObjDe.toJsonString()
	jsonObj = jsonObj.replace("\"null\"","null")
	# return json string
	return jsonObj









