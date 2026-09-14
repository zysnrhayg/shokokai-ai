#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api117GetnoticesDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,noticeid,title,content,rolecode,endat):
		super().__init__(mode,actflg,triggerid,row)
			#notice_id
		self.noticeid = noticeid
			#title
		self.title = title
			#content
		self.content = content
			#role_code
		self.rolecode = rolecode
			#end_at
		self.endat = endat
	
	def dict_to_json(dict):
		return Api117GetnoticesDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("noticeid",""),dict.get("title",""),dict.get("content",""),dict.get("rolecode",""),dict.get("endat",""))
	
	
	
