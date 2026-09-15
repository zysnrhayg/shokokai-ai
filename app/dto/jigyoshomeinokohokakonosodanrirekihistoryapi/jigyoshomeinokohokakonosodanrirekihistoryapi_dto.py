#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class JigyoshomeinokohokakonosodanrirekihistoryapiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,xx,trnreportprefecturecode,trnreportshokokaicd,trnreportbusinessname,limit):
		super().__init__(mode,actflg,triggerid,row)
			#XX
		self.xx = xx
			#TRN_REPORT_PREFECTURE_CODE
		self.trnreportprefecturecode = trnreportprefecturecode
			#TRN_REPORT_SHOKOKAI_CD
		self.trnreportshokokaicd = trnreportshokokaicd
			#TRN_REPORT_BUSINESS_NAME
		self.trnreportbusinessname = trnreportbusinessname
			#LIMIT
		self.limit = limit
	
	def dict_to_json(dict):
		return JigyoshomeinokohokakonosodanrirekihistoryapiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("xx",""),dict.get("trnreportprefecturecode", dict.get("prefecturecode","")),dict.get("trnreportshokokaicd", dict.get("shokokaicd","")),dict.get("trnreportbusinessname", dict.get("businessname","")),dict.get("limit",""))
	
	
	
