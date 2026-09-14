#BasicService.vm
#make Service templete
import json
import utils.config
import threading
import utils.json_constant	
from flask import session 
from app.common.getautonum import GetAutonum
from datetime import datetime, timezone, timedelta
import utils.date_util
from utils.jsonwfc_object import JSONWFCObject
import resources.messages
from app.dao.ac_sendmail.ac_sendmail_dao import AcSendmailDao
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib
import utils.config
import utils.string_util




class AcSendmailService :

	#	# 
	# メールを送る
	# @param ac_sendmailRequest_Dto
	# @throws Exception
	#
	def addac_sendmail(ac_sendmailRequest_Dto) :
			#send mail
		loginID = ac_sendmailRequest_Dto.user_id
		BUSINESS_UNIT = utils.config.inout_businessunit
		MAIL_ID = utils.string_util.ChangeIntToString(random.randint(100000, 999999))
		MAIL_DT = utils.date_util.getPatternDateForDb()
		MAIL_TM = MAIL_DT
		WF_CATALOG = "01"
		CHARSET = "shift-jis"
		USER_ID = loginID
		USER_NM = loginID
		PRCS_ID = "0"
		AcSendmailDao.addac_sendmail(ac_sendmailRequest_Dto.fromm, ac_sendmailRequest_Dto.to, ac_sendmailRequest_Dto.cc, ac_sendmailRequest_Dto.bcc, ac_sendmailRequest_Dto.subject, ac_sendmailRequest_Dto.content, BUSINESS_UNIT, MAIL_ID, MAIL_DT, MAIL_TM, WF_CATALOG, CHARSET, USER_ID, USER_NM, PRCS_ID)
		try :
			msg = MIMEText(ac_sendmailRequest_Dto.content, "plain", "utf-8")
			msg['From'] = utils.config.mail_from
			msg['To'] = ac_sendmailRequest_Dto.to
			msg['Subject'] = ac_sendmailRequest_Dto.subject
			server = smtplib.SMTP(utils.config.mail_smtplib, utils.config.mail_smtplib_port)
			server.starttls()
			server.login(utils.config.mail_from, utils.config.mail_password)
			server.sendmail(utils.config.mail_from, "", msg.as_string())
			server.quit()
			utils.config.global_log.info("send mail success")
		except Exception as e :
			utils.config.global_log.exception("send mail failed")
			
	
	
