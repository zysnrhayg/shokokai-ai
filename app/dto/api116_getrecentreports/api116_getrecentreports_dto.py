#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api116GetrecentreportsDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,reportid,reportdate,themelabel,formlabel,prefecturecode,shokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#report_id
		self.reportid = reportid
			#report_date
		self.reportdate = reportdate
			#theme_label
		self.themelabel = themelabel
			#form_label
		self.formlabel = formlabel
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#SHOKOKAI_CD
		self.shokokaicd = shokokaicd
	
	def dict_to_json(dict):
		return Api116GetrecentreportsDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("reportid",""),dict.get("reportdate",""),dict.get("themelabel",""),dict.get("formlabel",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""))
	
	
	
