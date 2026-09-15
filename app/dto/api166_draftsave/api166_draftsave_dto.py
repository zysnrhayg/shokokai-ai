#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api166DraftsaveDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,result,houkokushokoumokuisshiki):
		super().__init__(mode,actflg,triggerid,row)
			#result
		self.result = result
			#HOUKOKUSHOKOUMOKUISSHIKI
		self.houkokushokoumokuisshiki = houkokushokoumokuisshiki
	
	def dict_to_json(dict):
		return Api166DraftsaveDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("result",""),dict.get("houkokushokoumokuisshiki",""))
	
	
	
