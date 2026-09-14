
# BasicDao.vm

import utils.mysqldb_utils
from app.dto.ac_sendmailrequest_dto import AcSendmailrequestDto
from app.mapper.ac_sendmail.ac_sendmail_mapper import AcSendmailMapper

 # AcSendmailDao


class AcSendmailDao :

	 # call mapper interface
	def addac_sendmail(MAILFROM, MAILTO, CC, BCC, SUBJECT, CONTENT, BUSINESS_UNIT, MAIL_ID, MAIL_DT, MAIL_TM, WF_CATALOG, CHARSET, USER_ID, USER_NM, PRCS_ID) :
		utils.mysqldb_utils.insertSQL(AcSendmailMapper.addac_sendmail(MAILFROM, MAILTO, CC, BCC, SUBJECT, CONTENT, BUSINESS_UNIT, MAIL_ID, MAIL_DT, MAIL_TM, WF_CATALOG, CHARSET, USER_ID, USER_NM, PRCS_ID),{'MAILFROM':MAILFROM,'MAILTO':MAILTO,'CC':CC,'BCC':BCC,'SUBJECT':SUBJECT,'CONTENT':CONTENT,'BUSINESS_UNIT':BUSINESS_UNIT,'MAIL_ID':MAIL_ID,'MAIL_DT':MAIL_DT,'MAIL_TM':MAIL_TM,'WF_CATALOG':WF_CATALOG,'CHARSET':CHARSET,'USER_ID':USER_ID,'USER_NM':USER_NM,'PRCS_ID':PRCS_ID})
