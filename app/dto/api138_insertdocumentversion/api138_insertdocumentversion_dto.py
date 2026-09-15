#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api138InsertdocumentversionDto(BaseEntity):

	def __init__(self,mode,actflg,triggerid,row,knowledgedocumentid,versionnumber,uploadedby,filesizekb,status,filepath):
		super().__init__(mode,actflg,triggerid,row)
			#KNOWLEDGE_DOCUMENT_ID
		self.knowledgedocumentid = knowledgedocumentid
			#VERSION_NUMBER
		self.versionnumber = versionnumber
			#UPLOADED_BY
		self.uploadedby = uploadedby
			#FILE_SIZE_KB
		self.filesizekb = filesizekb
			#STATUS
		self.status = status
			#FILE_PATH
		self.filepath = filepath

	def dict_to_json(dict):
		return Api138InsertdocumentversionDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgedocumentid",""),dict.get("versionnumber",""),dict.get("uploadedby",""),dict.get("filesizekb",""),dict.get("status",""),dict.get("filepath",""))
