#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api130GetexportformsDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,formcode,shortlabel,fulllabel,fiscalyearid):
		super().__init__(mode,actflg,triggerid,row)
			#form_code
		self.formcode = formcode
			#short_label
		self.shortlabel = shortlabel
			#full_label
		self.fulllabel = fulllabel
			#FISCAL_YEAR_ID
		self.fiscalyearid = fiscalyearid
	
	def dict_to_json(dict):
		return Api130GetexportformsDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("formcode",""),dict.get("shortlabel",""),dict.get("fulllabel",""),dict.get("fiscalyearid",""))
	
	
	
