#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api137InsertknowledgedocumentDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,knowledgedocumentid,uploadeddate,filesizekb,status,filepath):
		super().__init__(mode,actflg,triggerid,row)
			#KNOWLEDGE_DOCUMENT_ID
		self.knowledgedocumentid = knowledgedocumentid
			#UPLOADED_DATE
		self.uploadeddate = uploadeddate
			#FILE_SIZE_KB
		self.filesizekb = filesizekb
			#STATUS
		self.status = status
			#FILE_PATH
		self.filepath = filepath
	
	def dict_to_json(dict):
		return Api137InsertknowledgedocumentDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgedocumentid",""),dict.get("uploadeddate",""),dict.get("filesizekb",""),dict.get("status",""),dict.get("filepath",""))
	
	
	
