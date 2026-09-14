<<<<<<< HEAD
#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api102GetshokokaiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,prefecturecode,shokokaicd,name,onlyfederation,excludefederation):
		super().__init__(mode,actflg,triggerid,row)
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#name
		self.name = name
			#ONLY_FEDERATION
		self.onlyfederation = onlyfederation
			#EXCLUDE_FEDERATION
		self.excludefederation = excludefederation
	
	def dict_to_json(dict):
		return Api102GetshokokaiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("name",""),dict.get("onlyfederation",""),dict.get("excludefederation",""))
	
	
	
=======
#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api102GetshokokaiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,prefecturecode,shokokaicd,name,onlyfederation,excludefederation):
		super().__init__(mode,actflg,triggerid,row)
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#name
		self.name = name
			#ONLY_FEDERATION
		self.onlyfederation = onlyfederation
			#EXCLUDE_FEDERATION
		self.excludefederation = excludefederation
	
	def dict_to_json(dict):
		return Api102GetshokokaiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("name",""),dict.get("onlyfederation",""),dict.get("excludefederation",""))
	
	
	
>>>>>>> f99884143b83701ade7248d8bbf4384c923a6e35
