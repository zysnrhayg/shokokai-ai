#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiJigyoshomeinokohokakonosodanrirekinamesDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,businessname,lastreportdate,prefecturecode,shokokaicd,limit):
		super().__init__(mode,actflg,triggerid,row)
			#business_name
		self.businessname = businessname
			#last_report_date
		self.lastreportdate = lastreportdate
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
			#LIMIT
		self.limit = limit
	
	def dict_to_json(dict):
		return ApiJigyoshomeinokohokakonosodanrirekinamesDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("businessname",""),dict.get("lastreportdate",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("limit",""))
	
	
	
