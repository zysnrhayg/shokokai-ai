#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api149GetvectorcollectiondetailDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,vectorcollectionid,name,vectorcount,synceddate,status):
		super().__init__(mode,actflg,triggerid,row)
			#vector_collection_id
		self.vectorcollectionid = vectorcollectionid
			#name
		self.name = name
			#vector_count
		self.vectorcount = vectorcount
			#synced_date
		self.synceddate = synceddate
			#status
		self.status = status
	
	def dict_to_json(dict):
		return Api149GetvectorcollectiondetailDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("vectorcollectionid",""),dict.get("name",""),dict.get("vectorcount",""),dict.get("synceddate",""),dict.get("status",""))
	
	
	
