#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api120GetthemesDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,themeid,themecode,label,filtergroup,fiscalyearid):
		super().__init__(mode,actflg,triggerid,row)
			#theme_id
		self.themeid = themeid
			#theme_code
		self.themecode = themecode
			#label
		self.label = label
			#filter_group
		self.filtergroup = filtergroup
			#FISCAL_YEAR_ID
		self.fiscalyearid = fiscalyearid
	
	def dict_to_json(dict):
		return Api120GetthemesDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("themeid",""),dict.get("themecode",""),dict.get("label",""),dict.get("filtergroup",""),dict.get("fiscalyearid",""))
	
	
	
