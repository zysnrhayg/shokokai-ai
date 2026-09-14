#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiGenponbunshoichiranDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,trnknowledgedocument,knowledgedocumentid,prefecturecode,activeversionnumber,documentcode,title,category,format,createdat,createdby,updatedat,updatedby,deletedat,deletedby,trnknowledgedocumentversionuploadeddate,trnknowledgedocumentversionfilesizekb,trnknowledgedocumentversionstatus,trnknowledgedocumentversionfilepath,prefecturename,linkedcount):
		super().__init__(mode,actflg,triggerid,row)
			#trn_knowledge_document. *
		self.trnknowledgedocument = trnknowledgedocument
			#knowledge_document_id
		self.knowledgedocumentid = knowledgedocumentid
			#prefecture_code
		self.prefecturecode = prefecturecode
			#active_version_number
		self.activeversionnumber = activeversionnumber
			#document_code
		self.documentcode = documentcode
			#title
		self.title = title
			#category
		self.category = category
			#format
		self.format = format
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
			#trn_knowledge_document_version.uploaded_date
		self.trnknowledgedocumentversionuploadeddate = trnknowledgedocumentversionuploadeddate
			#trn_knowledge_document_version.file_size_kb
		self.trnknowledgedocumentversionfilesizekb = trnknowledgedocumentversionfilesizekb
			#trn_knowledge_document_version.status
		self.trnknowledgedocumentversionstatus = trnknowledgedocumentversionstatus
			#trn_knowledge_document_version.file_path
		self.trnknowledgedocumentversionfilepath = trnknowledgedocumentversionfilepath
			#prefecture_name
		self.prefecturename = prefecturename
			#linked_count
		self.linkedcount = linkedcount
	
	def dict_to_json(dict):
		return ApiGenponbunshoichiranDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("trnknowledgedocument",""),dict.get("knowledgedocumentid",""),dict.get("prefecturecode",""),dict.get("activeversionnumber",""),dict.get("documentcode",""),dict.get("title",""),dict.get("category",""),dict.get("format",""),dict.get("createdat",""),dict.get("createdby",""),dict.get("updatedat",""),dict.get("updatedby",""),dict.get("deletedat",""),dict.get("deletedby",""),dict.get("trnknowledgedocumentversionuploadeddate",""),dict.get("trnknowledgedocumentversionfilesizekb",""),dict.get("trnknowledgedocumentversionstatus",""),dict.get("trnknowledgedocumentversionfilepath",""),dict.get("prefecturename",""),dict.get("linkedcount",""))
	
	
	
