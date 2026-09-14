#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class AcSendmailrequestDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,fromm,to,cc,bcc,subject,content):
		super().__init__(mode,actflg,triggerid,row)
			#sender
		self.fromm = fromm
			#recipient
		self.to = to
			#CC
		self.cc = cc
			#
		self.bcc = bcc
			#Subject
		self.subject = subject
			#Content
		self.content = content
	
	def dict_to_json(dict):
		return AcSendmailrequestDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("fromm",""),dict.get("to",""),dict.get("cc",""),dict.get("bcc",""),dict.get("subject",""),dict.get("content",""))
	
	
	
