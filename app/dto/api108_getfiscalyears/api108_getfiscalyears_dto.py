#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api108GetfiscalyearsDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,fiscalyearid,fiscalyearcode,label,startmonth,endmonth):
		super().__init__(mode,actflg,triggerid,row)
			#fiscal_year_id
		self.fiscalyearid = fiscalyearid
			#fiscal_year_code
		self.fiscalyearcode = fiscalyearcode
			#label
		self.label = label
			#start_month
		self.startmonth = startmonth
			#end_month
		self.endmonth = endmonth
	
	def dict_to_json(dict):
		return Api108GetfiscalyearsDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("fiscalyearid",""),dict.get("fiscalyearcode",""),dict.get("label",""),dict.get("startmonth",""),dict.get("endmonth",""))
	
	
	
