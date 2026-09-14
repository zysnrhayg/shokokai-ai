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
		
	def __init__(self,mode,actflg,triggerid,row,knowledgeentryid,title,content,themelabel,documentversion):
		super().__init__(mode,actflg,triggerid,row)
			#knowledge_entry_id
		self.knowledgeentryid = knowledgeentryid
			#title
		self.title = title
			#content
		self.content = content
			#theme_label
		self.themelabel = themelabel
			#document_version
		self.documentversion = documentversion
	
	def dict_to_json(dict):
		return Api154GetpublishedentriesDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgeentryid",""),dict.get("title",""),dict.get("content",""),dict.get("themelabel",""),dict.get("documentversion",""))
	
	
	
