#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api204FormexportDto(BaseEntity):

	def __init__(self,mode,actflg,triggerid,row,reportid,reportcode,formcode,formfulllabel,reportdate,timestart,timeend,staffmainname,staffsubname,industry,businessname,businessperson,content,summary,prefecturecode,shokokaicd,source=""):
		super().__init__(mode,actflg,triggerid,row)
			#report_id
		self.reportid = reportid
			#report_code
		self.reportcode = reportcode
			#form_code
		self.formcode = formcode
			#form_full_label
		self.formfulllabel = formfulllabel
			#report_date
		self.reportdate = reportdate
			#time_start
		self.timestart = timestart
			#time_end
		self.timeend = timeend
			#staff_main_name
		self.staffmainname = staffmainname
			#staff_sub_name
		self.staffsubname = staffsubname
			#industry
		self.industry = industry
			#business_name
		self.businessname = businessname
			#business_person
		self.businessperson = businessperson
			#content
		self.content = content
			#summary
		self.summary = summary
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#画面ソース（ai-input or manual-input）
		self.source = source

	def dict_to_json(dict):
		return Api204FormexportDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("reportid",""),dict.get("reportcode",""),dict.get("formcode",""),dict.get("formfulllabel",""),dict.get("reportdate",""),dict.get("timestart",""),dict.get("timeend",""),dict.get("staffmainname",""),dict.get("staffsubname",""),dict.get("industry",""),dict.get("businessname",""),dict.get("businessperson",""),dict.get("content",""),dict.get("summary",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("source",""))
	
	
	
