#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api112GetdashboardkpiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,fiscalyearid,supportcount,aiactivitycount,prefecturecode,shokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#fiscal_year_id
		self.fiscalyearid = fiscalyearid
			#support_count
		self.supportcount = supportcount
			#ai_activity_count
		self.aiactivitycount = aiactivitycount
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
	
	def dict_to_json(dict):
		return Api112GetdashboardkpiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("fiscalyearid",""),dict.get("supportcount",""),dict.get("aiactivitycount",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""))
	
	
	
