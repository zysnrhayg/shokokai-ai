#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiRagsetteiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,ragsettingid,embeddingmodel,vectordb,chunksize,chunkoverlap,lastsyncedat,createdat,createdby,updatedat,updatedby,deletedat,deletedby):
		super().__init__(mode,actflg,triggerid,row)
			#rag_setting_id
		self.ragsettingid = ragsettingid
			#embedding_model
		self.embeddingmodel = embeddingmodel
			#vector_db
		self.vectordb = vectordb
			#chunk_size
		self.chunksize = chunksize
			#chunk_overlap
		self.chunkoverlap = chunkoverlap
			#last_synced_at
		self.lastsyncedat = lastsyncedat
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
		return ApiRagsetteiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("ragsettingid",""),dict.get("embeddingmodel",""),dict.get("vectordb",""),dict.get("chunksize",""),dict.get("chunkoverlap",""),dict.get("lastsyncedat",""),dict.get("createdat",""),dict.get("createdby",""),dict.get("updatedat",""),dict.get("updatedby",""),dict.get("deletedat",""),dict.get("deletedby",""))
	
	
	
