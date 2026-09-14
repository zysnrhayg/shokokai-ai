#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api154GetpublishedentriesDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,knowledgeentryid,knowledgecode,title,content,updateddate,knowledgedocumentid,keyword,prefecturecode):
		super().__init__(mode,actflg,triggerid,row)
			#knowledge_entry_id
		self.knowledgeentryid = knowledgeentryid
			#knowledge_code
		self.knowledgecode = knowledgecode
			#title
		self.title = title
			#content
		self.content = content
			#updated_date
		self.updateddate = updateddate
			#knowledge_document_id
		self.knowledgedocumentid = knowledgedocumentid
			#KEYWORD
		self.keyword = keyword
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
	
	def dict_to_json(dict):
		return Api154GetpublishedentriesDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgeentryid",""),dict.get("knowledgecode",""),dict.get("title",""),dict.get("content",""),dict.get("updateddate",""),dict.get("knowledgedocumentid",""),dict.get("keyword",""),dict.get("prefecturecode",""))
	
	
	
