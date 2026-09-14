#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api113GetkpithemebreakdownDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,fiscalyearid,themecode,label,badgeclass,supportcount,prefecturecode,shokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#fiscal_year_id
		self.fiscalyearid = fiscalyearid
			#theme_code
		self.themecode = themecode
			#label
		self.label = label
			#badge_class
		self.badgeclass = badgeclass
			#support_count
		self.supportcount = supportcount
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
	
	def dict_to_json(dict):
		return Api113GetkpithemebreakdownDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("fiscalyearid",""),dict.get("themecode",""),dict.get("label",""),dict.get("badgeclass",""),dict.get("supportcount",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""))
	
	
	
