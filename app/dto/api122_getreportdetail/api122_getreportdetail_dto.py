#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api122GetreportdetailDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,reportid,reportcode,formcode,fiscalyearid,prefecturecode,shokokaicd,themeid,industry,reportdate,summary,content,timestart,timeend,businessperson,businessname,staffmainname,staffsubname,registeredat,formfulllabel,primarythemecode):
		super().__init__(mode,actflg,triggerid,row)
			#report_id
		self.reportid = reportid
			#report_code
		self.reportcode = reportcode
			#form_code
		self.formcode = formcode
			#fiscal_year_id
		self.fiscalyearid = fiscalyearid
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#theme_id
		self.themeid = themeid
			#industry
		self.industry = industry
			#report_date
		self.reportdate = reportdate
			#summary
		self.summary = summary
			#content
		self.content = content
			#time_start
		self.timestart = timestart
			#time_end
		self.timeend = timeend
			#business_person
		self.businessperson = businessperson
			#business_name
		self.businessname = businessname
			#staff_main_name
		self.staffmainname = staffmainname
			#staff_sub_name
		self.staffsubname = staffsubname
			#registered_at
		self.registeredat = registeredat
			#form_full_label
		self.formfulllabel = formfulllabel
			#primary_theme_code
		self.primarythemecode = primarythemecode
	
	def dict_to_json(dict):
		return Api122GetreportdetailDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("reportid",""),dict.get("reportcode",""),dict.get("formcode",""),dict.get("fiscalyearid",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("themeid",""),dict.get("industry",""),dict.get("reportdate",""),dict.get("summary",""),dict.get("content",""),dict.get("timestart",""),dict.get("timeend",""),dict.get("businessperson",""),dict.get("businessname",""),dict.get("staffmainname",""),dict.get("staffsubname",""),dict.get("registeredat",""),dict.get("formfulllabel",""),dict.get("primarythemecode",""))
	
	
	
