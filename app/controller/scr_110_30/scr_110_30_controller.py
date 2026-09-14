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




from app.dto.scr_110_30.scr_110_30_dto import Scr11030Dto
from app.service.scr_110_30.scr_110_30init_service import Scr11030initService
import utils.session_constant



scr_110_30_route = Blueprint('scr_110_30_route', __name__)
#
# EDIOS_MSREシステム
# class: scr_110_30controller
# page: テンプレート
#

@scr_110_30_route.route("/SCR_110_30", methods=["GET"])
def scr_110_30_page():
	if session.get(utils.session_constant.USER_ID, "") == "":
		return redirect(url_for("index"))
	return render_template("SCR_110_30.html")


#
# scr_110_30 - テンプレート - 画面初期化
# @param scr_110_30_dto
# @param result
# @throws Exception
#
@scr_110_30_route.route("/SCR_110_30Init.do", methods=["POST"])


def scr_110_30init() :
	"""scr_110_30 - テンプレート - 画面初期化"""
	data = request.get_json()
	# json 176
	scr_110_30_dto = Scr11030Dto.dict_to_json(data)
	scr_110_30init_serviceVar = Scr11030initService()
	jsonObjDe = scr_110_30init_serviceVar.sscr_110_30init(scr_110_30_dto)
	jsonObj = jsonObjDe.toJsonString()
	jsonObj = jsonObj.replace("\"null\"","null")
	# return json string
	return jsonObj









