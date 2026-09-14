#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api105AuthenticateuserDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,useraccountid,prefecturecode,shokokaicd,userid,shokuinkj,password,status,totpsecret,ismfaenabled,failedlogincount,lockeduntil):
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
			#password
		self.password = password
			#status
		self.status = status
			#totp_secret
		self.totpsecret = totpsecret
			#is_mfa_enabled
		self.ismfaenabled = ismfaenabled
			#failed_login_count
		self.failedlogincount = failedlogincount
			#locked_until
		self.lockeduntil = lockeduntil
	
	def dict_to_json(dict):
		return Api105AuthenticateuserDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("useraccountid",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("userid",""),dict.get("shokuinkj",""),dict.get("password",""),dict.get("status",""),dict.get("totpsecret",""),dict.get("ismfaenabled",""),dict.get("failedlogincount",""),dict.get("lockeduntil",""))
	
	
	
