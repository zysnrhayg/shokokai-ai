#logincontroller.py  make logincontroller
#templete logincontroller.vm 
from flask import Blueprint, Flask, request, jsonify, redirect, url_for, render_template,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import utils.config
from utils.jsonwfc_object import JSONWFCObject
from app.dto.login_dto import LoginDto
from app.service.login_service import LoginService
import utils.string_util
login_route = Blueprint('login_route', __name__)
import utils.session_constant  
from app.service.usermenu_service import UsermenuService
from app.dto.usermenutreeresponse import UserMenuTreeResponse
from app.dto.usermenutreeresponse import UserMenu
import json
from types import SimpleNamespace
from dataclasses import asdict
import resources.messages

@login_route.route("/login.do", methods=["POST"])
def pythonLogin() :
	jsonObj = JSONWFCObject()
	data = request.get_json() or {}
	userid = data.get("userid")
	pwd = data.get("pwd")
	isMobile = data.get("isMobile")
	if utils.string_util.isNullOrBlank(userid) == True:
		jsonObj.setValue("c", resources.messages.getMessageById("msg_login_userid_required"))
		return jsonify({"c": resources.messages.getMessageById("msg_login_userid_required")}), 400
	if utils.string_util.isNullOrBlank(pwd) == True :
		jsonObj.setValue("c", resources.messages.getMessageById("msg_login_pwd_required"))
		return jsonify({"c": resources.messages.getMessageById("msg_login_pwd_required")}), 400
	loginService = LoginService()
	return 	loginService.dologin(userid,pwd)
def load_user(user_id):
	pass
@login_route.route("/getMenu.do", methods=["POST"])
def getInfo() :
	loginid = session.get(utils.session_constant.USER_ID,"")
	userMenuEntities = UsermenuService.getusermenu(loginid)
	
	if userMenuEntities == None :
		return "{\"roles\":[],\"code\":\"-1\"}"
	# getMenu 链返回 list（usermenu_dao result_to_list_of_dict），归一化为 list，元素为 dict 时转为 SimpleNamespace
	userMenuEntitieList = list(userMenuEntities) if isinstance(userMenuEntities, list) else list((userMenuEntities.fetchall() if hasattr(userMenuEntities, "fetchall") else []) or [])
	if userMenuEntitieList == None or len(userMenuEntitieList) <= 0 :
		return "{\"roles\":[],\"code\":\"-1\"}"
		
	user_menu_tree_response = UserMenuTreeResponse()
	menus_map = {}
	jsonObject = JSONWFCObject()
	jsonObject.setValue("code","200")
	res = []
	# Parent node
	if userMenuEntitieList != None :
		for user_menu_entity in userMenuEntitieList:
			if isinstance(user_menu_entity, dict):
				user_menu_entity = SimpleNamespace(**user_menu_entity)
			user_menu = UserMenu(user_menu_entity)
			toMap = user_menu.tomap()
			# user_menu_tree_response.set_roles(user_menu_tree_response.get_roles() + [user_menu])  # Adding user menu to roles
			# menus_map[user_menu.get_name()] = user_menu
			strMap = str(toMap).replace("\"","")
			strMap = strMap.replace("None","''")
			res.insert(len(res),strMap)
		
 	
	jsonObject.setValue("roles",res)
	return jsonObject.toJsonString().replace("\"{","{").replace("}\"","}").replace("'","\"").replace("\"null\"","null")