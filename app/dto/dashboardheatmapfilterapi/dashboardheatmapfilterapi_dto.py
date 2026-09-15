#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class DashboardheatmapfilterapiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,groupvalues,includeall):
		super().__init__(mode,actflg,triggerid,row)
			#GROUP_VALUES
		self.groupvalues = groupvalues
			#INCLUDE_ALL
		self.includeall = includeall
	
	@staticmethod
	def dict_to_json(d):
		if d is None:
			d = {}
		o = DashboardheatmapfilterapiDto(
			d.get("mode", ""),
			d.get("actflg", ""),
			d.get("triggerid", ""),
			d.get("row", ""),
			d.get("groupvalues", ""),
			d.get("includeall", ""),
		)
		o.rolecode = d.get("rolecode", "")
		o.fiscalyearid = d.get("fiscalyearid", "")
		o.prefecturecode = d.get("prefecturecode") or d.get("prefecture_code", "")
		o.shokokaicd = d.get("shokokaicd") or d.get("shokokai_cd", "")
		return o
	
	
	
