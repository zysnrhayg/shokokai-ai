#py_entity.vm make dto templete
from utils.base_entity import BaseEntity
from voluptuous import Schema, Required, Range,MultipleInvalid,Length,Match,ALLOW_EXTRA,All
import re
from  utils.datecheck_hiduke import DateCheckHiduke
from  utils.datecheck_hiduke_ny import DateCheckHidukeNeGaTu
from  utils.datecheck_hiduke_yd import DateCheckHidukeGeTuNiChi
from  utils.datecheck_hiduke_compare import DateCheckHidukeCompare
from  utils.range_check import RangeCheck
class Api162ReportscsvexportDto(BaseEntity):
		
	def __init__(self,mode,actflg,triggerid,row,reportid,reportcode,industry,reportdate,summary,staffmainname,staffsubname,registeredat,prefecturecode,shokokaicd,prefecturename,shokokainame,themelabel,themebadgeclass,themefiltergroup,formcode,formshortlabel,formbadgeclass,roleprefecturecode,roleshokokaicd,yearmonth,fystartmonth,fyendmonth,form,theme,keyword):
		super().__init__(mode,actflg,triggerid,row)
			#report_id
		self.reportid = reportid
			#report_code
		self.reportcode = reportcode
			#industry
		self.industry = industry
			#report_date
		self.reportdate = reportdate
			#summary
		self.summary = summary
			#staff_main_name
		self.staffmainname = staffmainname
			#staff_sub_name
		self.staffsubname = staffsubname
			#registered_at
		self.registeredat = registeredat
			#prefecture_code
		self.prefecturecode = prefecturecode
			#shokokai_cd
		self.shokokaicd = shokokaicd
			#prefecture_name
		self.prefecturename = prefecturename
			#shokokai_name
		self.shokokainame = shokokainame
			#theme_label
		self.themelabel = themelabel
			#theme_badge_class
		self.themebadgeclass = themebadgeclass
			#theme_filter_group
		self.themefiltergroup = themefiltergroup
			#form_code
		self.formcode = formcode
			#form_short_label
		self.formshortlabel = formshortlabel
			#form_badge_class
		self.formbadgeclass = formbadgeclass
			#ROLE_PREFECTURE_CODE
		self.roleprefecturecode = roleprefecturecode
			#ROLE_SHOKOKAI_CD
		self.roleshokokaicd = roleshokokaicd
			#YEAR_MONTH
		self.yearmonth = yearmonth
			#FY_START_MONTH
		self.fystartmonth = fystartmonth
			#FY_END_MONTH
		self.fyendmonth = fyendmonth
			#FORM
		self.form = form
			#THEME
		self.theme = theme
			#KEYWORD
		self.keyword = keyword
	
	def dict_to_json(dict):
		return Api162ReportscsvexportDto(dict.get("mode",""),dict.get("actflg",""),dict.get("triggerid",""),dict.get("row",""),dict.get("reportid",""),dict.get("reportcode",""),dict.get("industry",""),dict.get("reportdate",""),dict.get("summary",""),dict.get("staffmainname",""),dict.get("staffsubname",""),dict.get("registeredat",""),dict.get("prefecturecode",""),dict.get("shokokaicd",""),dict.get("prefecturename",""),dict.get("shokokainame",""),dict.get("themelabel",""),dict.get("themebadgeclass",""),dict.get("themefiltergroup",""),dict.get("formcode",""),dict.get("formshortlabel",""),dict.get("formbadgeclass",""),dict.get("roleprefecturecode",""),dict.get("roleshokokaicd",""),dict.get("yearmonth",""),dict.get("fystartmonth",""),dict.get("fyendmonth",""),dict.get("form",""),dict.get("theme",""),dict.get("keyword",""))
	
	
	
