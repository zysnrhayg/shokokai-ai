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

	def __init__(self,mode,actflg,triggerid,row,knowledgedocumentid,prefecturecode,documentcode,title,category,format):
		super().__init__(mode,actflg,triggerid,row)
			#KNOWLEDGE_DOCUMENT_ID
		self.knowledgedocumentid = knowledgedocumentid
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#DOCUMENT_CODE
		self.documentcode = documentcode
			#TITLE
		self.title = title
			#CATEGORY
		self.category = category
			#FORMAT
		self.format = format

	def dict_to_json(dict):
		return Api137InsertknowledgedocumentDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("knowledgedocumentid",""),dict.get("prefecturecode",""),dict.get("documentcode",""),dict.get("title",""),dict.get("category",""),dict.get("format",""))
