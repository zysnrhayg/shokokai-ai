#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class ApiIchiranteburushiborikomiDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,mstuseraccountuseraccountid,mstuseraccountprefecturecode,mstuseraccountshokokaicd,mstuseraccountuserid,mstuseraccountshokuinkj,mstuseraccountemail,mstuseraccountstatus,mstuseraccountcorelinked,mstuseraccountpermissionlevel,mstuseraccountlastloginat,prefecturename,shokokainame,qualificationcodes,limit,offset):
		super().__init__(mode,actflg,triggerid,row)
			#mst_user_account.user_account_id
		self.mstuseraccountuseraccountid = mstuseraccountuseraccountid
			#mst_user_account.prefecture_code
		self.mstuseraccountprefecturecode = mstuseraccountprefecturecode
			#mst_user_account.shokokai_cd
		self.mstuseraccountshokokaicd = mstuseraccountshokokaicd
			#mst_user_account.user_id
		self.mstuseraccountuserid = mstuseraccountuserid
			#mst_user_account.shokuin_kj
		self.mstuseraccountshokuinkj = mstuseraccountshokuinkj
			#mst_user_account.email
		self.mstuseraccountemail = mstuseraccountemail
			#mst_user_account.status
		self.mstuseraccountstatus = mstuseraccountstatus
			#mst_user_account.core_linked
		self.mstuseraccountcorelinked = mstuseraccountcorelinked
			#mst_user_account.permission_level
		self.mstuseraccountpermissionlevel = mstuseraccountpermissionlevel
			#mst_user_account.last_login_at
		self.mstuseraccountlastloginat = mstuseraccountlastloginat
			#prefecture_name
		self.prefecturename = prefecturename
			#shokokai_name
		self.shokokainame = shokokainame
			#qualification_codes
		self.qualificationcodes = qualificationcodes
			#LIMIT
		self.limit = limit
			#OFFSET
		self.offset = offset
	
	def dict_to_json(dict):
		return ApiIchiranteburushiborikomiDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("mstuseraccountuseraccountid",""),dict.get("mstuseraccountprefecturecode",""),dict.get("mstuseraccountshokokaicd",""),dict.get("mstuseraccountuserid",""),dict.get("mstuseraccountshokuinkj",""),dict.get("mstuseraccountemail",""),dict.get("mstuseraccountstatus",""),dict.get("mstuseraccountcorelinked",""),dict.get("mstuseraccountpermissionlevel",""),dict.get("mstuseraccountlastloginat",""),dict.get("prefecturename",""),dict.get("shokokainame",""),dict.get("qualificationcodes",""),dict.get("limit",""),dict.get("offset",""))
	
	
	
