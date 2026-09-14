#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api183AccountsfilterDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,useraccountid,prefecturecode,shokokaicd,userid,shokuinkj,email,status,corelinked,permissionlevel,lastloginat,prefecturename,shokokainame,keyword):
		super().__init__(mode,actflg,triggerid,row)
			#user_account_id
		self.useraccountid = useraccountid
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#user_id
		self.userid = userid
			#shokuin_kj
		self.shokuinkj = shokuinkj
			#email
		self.email = email
			#status
		self.status = status
			#core_linked
		self.corelinked = corelinked
			#permission_level
		self.permissionlevel = permissionlevel
			#last_login_at
		self.lastloginat = lastloginat
			#prefecture_name
		self.prefecturename = prefecturename
			#shokokai_name
		self.shokokainame = shokokainame
			#KEYWORD
		self.keyword = keyword
	
	def dict_to_json(dict):
		return Api183AccountsfilterDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("useraccountid",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("userid",""),dict.get("shokuinkj",""),dict.get("email",""),dict.get("status",""),dict.get("corelinked",""),dict.get("permissionlevel",""),dict.get("lastloginat",""),dict.get("prefecturename",""),dict.get("shokokainame",""),dict.get("keyword",""))
	
	
	
