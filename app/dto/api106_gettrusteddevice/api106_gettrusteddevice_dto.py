#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api106GettrusteddeviceDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,trusteddeviceid,useraccountid,expiresat,tokenhash):
		super().__init__(mode,actflg,triggerid,row)
			#trusted_device_id
		self.trusteddeviceid = trusteddeviceid
			#user_account_id
		self.useraccountid = useraccountid
			#expires_at
		self.expiresat = expiresat
			#TOKEN_HASH
		self.tokenhash = tokenhash
	
	def dict_to_json(dict):
		return Api106GettrusteddeviceDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("trusteddeviceid",""),dict.get("useraccountid",""),dict.get("expiresat",""),dict.get("tokenhash",""))
	
	
	
