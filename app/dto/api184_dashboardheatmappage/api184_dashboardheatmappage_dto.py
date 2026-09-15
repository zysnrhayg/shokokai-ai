#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api184DashboardheatmappageDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,fiscalyearcode,totalsupportcount,aiproposalcount,page,pagesize,rolecode,excludedkeys):
		super().__init__(mode,actflg,triggerid,row)
			#fiscal_year_code
		self.fiscalyearcode = fiscalyearcode
			#total_support_count
		self.totalsupportcount = totalsupportcount
			#ai_proposal_count
		self.aiproposalcount = aiproposalcount
			#PAGE
		self.page = page
			#PAGE_SIZE
		self.pagesize = pagesize
			#ROLE_CODE
		self.rolecode = rolecode
			#EXCLUDED_KEYS
		self.excludedkeys = excludedkeys
	
	def dict_to_json(dict):
		return Api184DashboardheatmappageDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("fiscalyearcode",""),dict.get("totalsupportcount",""),dict.get("aiproposalcount",""),dict.get("page",""),dict.get("pagesize",""),dict.get("rolecode",""),dict.get("excludedkeys",""))
	
	
	
