#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiBekutorukorekushonichiranDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,trnvectorcollection,vectorcollectionid,ragsettingid,collectioncode,name,vectorcount,baselinevectorcount,status,synceddate,createdat,createdby,updatedat,updatedby,deletedat,deletedby):
		super().__init__(mode,actflg,triggerid,row)
			#trn_vector_collection. *
		self.trnvectorcollection = trnvectorcollection
			#vector_collection_id
		self.vectorcollectionid = vectorcollectionid
			#rag_setting_id
		self.ragsettingid = ragsettingid
			#collection_code
		self.collectioncode = collectioncode
			#name
		self.name = name
			#vector_count
		self.vectorcount = vectorcount
			#baseline_vector_count
		self.baselinevectorcount = baselinevectorcount
			#status
		self.status = status
			#synced_date
		self.synceddate = synceddate
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
	
	def dict_to_json(dict):
		return ApiBekutorukorekushonichiranDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("trnvectorcollection",""),dict.get("vectorcollectionid",""),dict.get("ragsettingid",""),dict.get("collectioncode",""),dict.get("name",""),dict.get("vectorcount",""),dict.get("baselinevectorcount",""),dict.get("status",""),dict.get("synceddate",""),dict.get("createdat",""),dict.get("createdby",""),dict.get("updatedat",""),dict.get("updatedby",""),dict.get("deletedat",""),dict.get("deletedby",""))
	
	
	
