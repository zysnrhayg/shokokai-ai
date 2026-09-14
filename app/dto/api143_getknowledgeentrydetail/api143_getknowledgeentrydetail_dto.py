#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api143GetknowledgeentrydetailDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,knowledgeentryid,knowledgecode,title,prefecturecode,theme,knowledgedocumentid,updatedat,status,body,documenttitle,prefecturename):
		super().__init__(mode,actflg,triggerid,row)
			#knowledge_entry_id
		self.knowledgeentryid = knowledgeentryid
			#knowledge_code
		self.knowledgecode = knowledgecode
			#title
		self.title = title
			#prefecture_code
		self.prefecturecode = prefecturecode
			#theme
		self.theme = theme
			#knowledge_document_id
		self.knowledgedocumentid = knowledgedocumentid
			#updated_at
		self.updatedat = updatedat
			#status
		self.status = status
			#body
		self.body = body
			#document_title
		self.documenttitle = documenttitle
			#prefecture_name
		self.prefecturename = prefecturename
	
	def dict_to_json(dict):
		return Api143GetknowledgeentrydetailDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgeentryid",""),dict.get("knowledgecode",""),dict.get("title",""),dict.get("prefecturecode",""),dict.get("theme",""),dict.get("knowledgedocumentid",""),dict.get("updatedat",""),dict.get("status",""),dict.get("body",""),dict.get("documenttitle",""),dict.get("prefecturename",""))
	
	
	
