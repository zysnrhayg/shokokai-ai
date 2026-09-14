#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api121GetstaffoptionsDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,userid,shokuinkj,prefecturecode,shokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#user_id
		self.userid = userid
			#shokuin_kj
		self.shokuinkj = shokuinkj
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
	
	def dict_to_json(dict):
		return Api121GetstaffoptionsDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("userid",""),dict.get("shokuinkj",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""))
	
	
	
