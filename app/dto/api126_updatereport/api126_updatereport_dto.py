#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api126UpdatereportDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,formcode,fiscalyearid,themeid,industry,reportdate,summary,content,timestart,timeend,businessperson,businessname,staffmainname,staffsubname,status,reportid):
		super().__init__(mode,actflg,triggerid,row)
			#FORM_CODE
		self.formcode = formcode
			#FISCAL_YEAR_ID
		self.fiscalyearid = fiscalyearid
			#THEME_ID
		self.themeid = themeid
			#INDUSTRY
		self.industry = industry
			#REPORT_DATE
		self.reportdate = reportdate
			#SUMMARY
		self.summary = summary
			#CONTENT
		self.content = content
			#TIME_START
		self.timestart = timestart
			#TIME_END
		self.timeend = timeend
			#BUSINESS_PERSON
		self.businessperson = businessperson
			#BUSINESS_NAME
		self.businessname = businessname
			#STAFF_MAIN_NAME
		self.staffmainname = staffmainname
			#STAFF_SUB_NAME
		self.staffsubname = staffsubname
			#STATUS
		self.status = status
			#REPORT_ID
		self.reportid = reportid
	
	def dict_to_json(dict):
		return Api126UpdatereportDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("formcode",""),dict.get("fiscalyearid",""),dict.get("themeid",""),dict.get("industry",""),dict.get("reportdate",""),dict.get("summary",""),dict.get("content",""),dict.get("timestart",""),dict.get("timeend",""),dict.get("businessperson",""),dict.get("businessname",""),dict.get("staffmainname",""),dict.get("staffsubname",""),dict.get("status",""),dict.get("reportid",""))
	
	
	
