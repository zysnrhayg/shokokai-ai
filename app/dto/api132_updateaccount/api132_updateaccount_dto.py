#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api132UpdateaccountDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,prefecturecode,shokokaicd,userid,shokuinkj,email,status,permissionlevel,password,useraccountid):
		super().__init__(mode,actflg,triggerid,row)
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
			#USER_ID
		self.userid = userid
			#SHOKUIN_KJ
		self.shokuinkj = shokuinkj
			#EMAIL
		self.email = email
			#STATUS
		self.status = status
			#PERMISSION_LEVEL
		self.permissionlevel = permissionlevel
			#PASSWORD
		self.password = password
			#USER_ACCOUNT_ID
		self.useraccountid = useraccountid
	
	def dict_to_json(dict):
		return Api132UpdateaccountDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("userid",""),dict.get("shokuinkj",""),dict.get("email",""),dict.get("status",""),dict.get("permissionlevel",""),dict.get("password",""),dict.get("useraccountid",""))
	
	
	
