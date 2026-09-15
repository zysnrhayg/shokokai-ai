#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class DashboardheatmappageapiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,page,pagesize,rolecode,fiscalyearcode,excludedkeys):
		super().__init__(mode,actflg,triggerid,row)
			#PAGE
		self.page = page
			#PAGE_SIZE
		self.pagesize = pagesize
			#ROLE_CODE
		self.rolecode = rolecode
			#FISCAL_YEAR_CODE
		self.fiscalyearcode = fiscalyearcode
			#EXCLUDED_KEYS
		self.excludedkeys = excludedkeys
	
	def dict_to_json(dict):
		return DashboardheatmappageapiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("page",""),dict.get("pagesize",""),dict.get("rolecode",""),dict.get("fiscalyearcode",""),dict.get("excludedkeys",""))
	
	
	
