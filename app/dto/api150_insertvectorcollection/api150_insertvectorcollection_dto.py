#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api150InsertvectorcollectionDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,vectorcollectionid,collectioncode,name,vectorcount,baselinevectorcount,status):
		super().__init__(mode,actflg,triggerid,row)
			#vector_collection_id
		self.vectorcollectionid = vectorcollectionid
			#COLLECTION_CODE
		self.collectioncode = collectioncode
			#NAME
		self.name = name
			#VECTOR_COUNT
		self.vectorcount = vectorcount
			#BASELINE_VECTOR_COUNT
		self.baselinevectorcount = baselinevectorcount
			#STATUS
		self.status = status
	
	def dict_to_json(dict):
		return Api150InsertvectorcollectionDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("vectorcollectionid",""),dict.get("collectioncode",""),dict.get("name",""),dict.get("vectorcount",""),dict.get("baselinevectorcount",""),dict.get("status",""))
	
	
	
