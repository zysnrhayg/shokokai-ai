#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class DashboardheatmapcelltoggleapiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,cellkey,excluded):
		super().__init__(mode,actflg,triggerid,row)
			#CELL_KEY
		self.cellkey = cellkey
			#EXCLUDED
		self.excluded = excluded
	
	@staticmethod
	def dict_to_json(d):
		if d is None:
			d = {}
		o = DashboardheatmapcelltoggleapiDto(
			d.get("mode", ""),
			d.get("actflg", ""),
			d.get("triggerid", ""),
			d.get("row", ""),
			d.get("cellkey", ""),
			d.get("excluded", ""),
		)
		o.rolecode = d.get("rolecode", "")
		o.fiscalyearid = d.get("fiscalyearid", "")
		o.excludedkeys = d.get("excludedkeys", "")
		o.prefecturecode = d.get("prefecturecode") or d.get("prefecture_code", "")
		o.shokokaicd = d.get("shokokaicd") or d.get("shokokai_cd", "")
		return o
	
	
	
