#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api153ResyncvectorcollectionsDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,vectorcollectionid,vectorcount):
		super().__init__(mode,actflg,triggerid,row)
			#VECTOR_COLLECTION_ID
		self.vectorcollectionid = vectorcollectionid
			#VECTOR_COUNT
		self.vectorcount = vectorcount
	
	def dict_to_json(dict):
		return Api153ResyncvectorcollectionsDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("vectorcollectionid",""),dict.get("vectorcount",""))
	
	
	
