#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiJigyoshomeinokohokakonosodanrirekihistoryDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,trnreportreportid,trnreportreportdate,trnreportsummary,formshortlabel,formbadgeclass,themelabel,trnreportprefecturecode,trnreportshokokaicd,trnreportbusinessname,limit):
		super().__init__(mode,actflg,triggerid,row)
			#trn_report.report_id
		self.trnreportreportid = trnreportreportid
			#trn_report.report_date
		self.trnreportreportdate = trnreportreportdate
			#trn_report.summary
		self.trnreportsummary = trnreportsummary
			#form_short_label
		self.formshortlabel = formshortlabel
			#form_badge_class
		self.formbadgeclass = formbadgeclass
			#theme_label
		self.themelabel = themelabel
			#TRN_REPORT_PREFECTURE_CODE
		self.trnreportprefecturecode = trnreportprefecturecode
			#TRN_REPORT_SHOKOKAI_CD
		self.trnreportshokokaicd = trnreportshokokaicd
			#TRN_REPORT_BUSINESS_NAME
		self.trnreportbusinessname = trnreportbusinessname
			#LIMIT
		self.limit = limit
	
	def dict_to_json(dict):
		return ApiJigyoshomeinokohokakonosodanrirekihistoryDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("trnreportreportid",""),dict.get("trnreportreportdate",""),dict.get("trnreportsummary",""),dict.get("formshortlabel",""),dict.get("formbadgeclass",""),dict.get("themelabel",""),dict.get("trnreportprefecturecode",""),dict.get("trnreportshokokaicd",""),dict.get("trnreportbusinessname",""),dict.get("limit",""))
	
	
	
