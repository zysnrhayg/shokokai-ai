#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api115GetheatmapshokokaiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,shokokaicd,name,yeartodatecount,prefecturecode,fiscalyearid,federationshokokaicd):
		super().__init__(mode,actflg,triggerid,row)
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#name
		self.name = name
			#year_to_date_count
		self.yeartodatecount = yeartodatecount
			#PREFECTURE_CODE
		self.prefecturecode = prefecturecode
			#FISCAL_YEAR_ID
		self.fiscalyearid = fiscalyearid
			#FEDERATION_SHOKOKAI_CD
		self.federationshokokaicd = federationshokokaicd
	
	def dict_to_json(dict):
		return Api115GetheatmapshokokaiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("shokokaicd",""),dict.get("name",""),dict.get("yeartodatecount",""),dict.get("prefecturecode",""),dict.get("fiscalyearid",""),dict.get("federationshokokaicd",""))
	
	
	
