#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api145UpdateknowledgeentryDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,title,prefecturecode,theme,knowledgedocumentid,status,body,updatedby,knowledgeentryid):
		super().__init__(mode,actflg,triggerid,row)
			#TITLE
		self.title = title
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#THEME
		self.theme = theme
			#KNOWLEDGE_DOCUMENT_ID
		self.knowledgedocumentid = knowledgedocumentid
			#STATUS
		self.status = status
			#BODY
		self.body = body
			#UPDATED_BY
		self.updatedby = updatedby
			#KNOWLEDGE_ENTRY_ID
		self.knowledgeentryid = knowledgeentryid
	
	def dict_to_json(dict):
		return Api145UpdateknowledgeentryDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("title",""),dict.get("prefecturecode",""),dict.get("theme",""),dict.get("knowledgedocumentid",""),dict.get("status",""),dict.get("body",""),dict.get("updatedby",""),dict.get("knowledgeentryid",""))
	
	
	
