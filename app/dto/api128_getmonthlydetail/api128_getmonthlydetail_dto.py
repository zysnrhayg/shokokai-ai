#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api128GetmonthlydetailDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,filtergroup,yearmonth,supportcount,prefecturecode,shokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#filter_group
		self.filtergroup = filtergroup
			#year_month
		self.yearmonth = yearmonth
			#support_count
		self.supportcount = supportcount
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
	
	def dict_to_json(dict):
		return Api128GetmonthlydetailDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("filtergroup",""),dict.get("yearmonth",""),dict.get("supportcount",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""))
	
	
	
