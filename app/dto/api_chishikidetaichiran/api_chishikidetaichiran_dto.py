#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiChishikidetaichiranDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,knowledgeentryid,knowledgedocumentid,prefecturecode,knowledgecode,title,updateddate,status,content,createdat,createdby,updatedat,updatedby,deletedat,deletedby,documenttitle,prefecturename):
		super().__init__(mode,actflg,triggerid,row)
			#knowledge_entry_id
		self.knowledgeentryid = knowledgeentryid
			#knowledge_document_id
		self.knowledgedocumentid = knowledgedocumentid
			#prefecture_code
		self.prefecturecode = prefecturecode
			#knowledge_code
		self.knowledgecode = knowledgecode
			#title
		self.title = title
			#updated_date
		self.updateddate = updateddate
			#status
		self.status = status
			#content
		self.content = content
			#created_at
		self.createdat = createdat
			#created_by
		self.createdby = createdby
			#updated_at
		self.updatedat = updatedat
			#updated_by
		self.updatedby = updatedby
			#deleted_at
		self.deletedat = deletedat
			#deleted_by
		self.deletedby = deletedby
			#document_title
		self.documenttitle = documenttitle
			#prefecture_name
		self.prefecturename = prefecturename
	
	def dict_to_json(dict):
		return ApiChishikidetaichiranDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgeentryid",""),dict.get("knowledgedocumentid",""),dict.get("prefecturecode",""),dict.get("knowledgecode",""),dict.get("title",""),dict.get("updateddate",""),dict.get("status",""),dict.get("content",""),dict.get("createdat",""),dict.get("createdby",""),dict.get("updatedat",""),dict.get("updatedby",""),dict.get("deletedat",""),dict.get("deletedby",""),dict.get("documenttitle",""),dict.get("prefecturename",""))
	
	
	
