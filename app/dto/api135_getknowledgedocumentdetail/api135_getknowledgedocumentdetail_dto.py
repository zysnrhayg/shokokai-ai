#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api135GetknowledgedocumentdetailDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,title,prefecturecode,category,format,filesizekb,uploadeddate,status,linkedcount,knowledgedocumentid):
		super().__init__(mode,actflg,triggerid,row)
			#title
		self.title = title
			#prefecture_code
		self.prefecturecode = prefecturecode
			#category
		self.category = category
			#format
		self.format = format
			#file_size_kb
		self.filesizekb = filesizekb
			#uploaded_date
		self.uploadeddate = uploadeddate
			#status
		self.status = status
			#linked_count
		self.linkedcount = linkedcount
			#KNOWLEDGE_DOCUMENT_ID
		self.knowledgedocumentid = knowledgedocumentid
	
	def dict_to_json(dict):
		return Api135GetknowledgedocumentdetailDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("title",""),dict.get("prefecturecode",""),dict.get("category",""),dict.get("format",""),dict.get("filesizekb",""),dict.get("uploadeddate",""),dict.get("status",""),dict.get("linkedcount",""),dict.get("knowledgedocumentid",""))
	
	
	
