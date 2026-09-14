import utils.config 
class LoginMapper :

		def loginInit(LOGINID,LOGINPASSWORD,GROUPID,LOGINTABLEID,WHRLOGINID,WHRLOGINPASSWORD ) :
			return "SELECT "+LOGINID+" as loginid,"+LOGINPASSWORD+" as password,"+GROUPID+" as groupid  FROM "+ utils.config.user_tableid +" WHERE "+LOGINID+" = :WHRLOGINID AND "+LOGINPASSWORD+" =:WHRLOGINPASSWORD"
		def loginGetByLoginId(LOGINID,LOGINPASSWORD,GROUPID,LOGINTABLEID,WHRLOGINID) :
			eff = utils.config.user_table_eff_status_fieldid or "enabled_flag"
			return "SELECT "+LOGINID+" as loginid,"+LOGINPASSWORD+" as password,"+GROUPID+" as groupid,"+eff+" as user_eff FROM "+ utils.config.user_tableid +" WHERE "+LOGINID+" = :WHRLOGINID"
		def loginInitNm(LOGINID,LOGINPASSWORD,USER_EFF,GROUPID,LOGINTABLEID,WHRLOGINID,WHRLOGINPASSWORD,USERID,USERNM1,USERNM2 ) :
			return "SELECT "+LOGINID+" as loginid,"+LOGINPASSWORD+" as password,"+USER_EFF+" as user_eff,"+GROUPID+" as groupid,"+USERID+" as userid,"+USERNM1+" as usernm1,"+USERNM2+" as usernm2 FROM "+ utils.config.user_tableid +" WHERE "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINID AND "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINPASSWORD"
		def loginInitSurname(LOGINID,LOGINPASSWORD,USER_EFF,GROUPID,LOGINTABLEID,WHRLOGINID,WHRLOGINPASSWORD, USERID,USERNM1 ) :
			return "SELECT "+LOGINID+" as loginid as LOGINID,"+LOGINPASSWORD+" as password,"+USER_EFF+" as user_eff,"+GROUPID+" as groupid,"+USERID+" as userid,:"+USERNM1+" as usernm1 FROM "+ utils.config.user_tableid +" WHERE "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINID AND "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINPASSWORD"
		def loginInitName(LOGINID,LOGINPASSWORD,USER_EFF,GROUPID,LOGINTABLEID,WHRLOGINID,WHRLOGINPASSWORD,USERID,USERNM2 ) :
			return "SELECT "+LOGINID+" as loginid,"+LOGINPASSWORD+" as password,"+USER_EFF+" as user_eff,"+GROUPID+" as groupid,"+USERID+" as userid,"+USERNM2+" as usernm2 FROM "+ utils.config.user_tableid +" WHERE "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINID AND "+ utils.config.user_table_userid_fieldid +"=:WHRLOGINPASSWORD"
		def loginAdminInit(LOGINID,PASSWORD):
			return "SELECT LOGINID,PASSWORD FROM ADMIN_USER_TBL WHERE LOGINID = :LOGINID AND PASSWORD = :PASSWORD"
		def getAdminByUsername(LOGINID)  :
			return "SELECT u.LOGINID as username, u.PASSWORD, g.GROUP_ID FROM ADMIN_USER_TBL u LEFT JOIN wf_group_user_tbl g ON u.loginid = g.USERID WHERE u.loginid = :LOGINID"
		def getBusinessUserByUsername(LOGINID,LOGINPASSWORD,DEPARTID,LOGINTABLEID,WHRLOGINID) :
			return "SELECT u.LOGINID as username, u.PASSWORD,g.GROUP_ID FROM ADMIN_USER_TBL u LEFT JOIN wf_group_user_tbl g ON u.LOGINID = g.USERID WHERE u.LOGINID = :LOGINID union all SELECT :WHRLOGINID},:LOGINPASSWORD,g.USER_VALUE1 as GROUP_ID FROM :LOGINTABLEID LEFT JOIN wf_user_value_rel_map_tbl g ON :LOGINTABLEID.:DEPARTID = g.USER_VALUE2 WHERE :WHRLOGINID = :LOGINID"
		def getPageRightByGroup(GROUPID) :
			return "SELECT  A.HAVINGID, M1.PROFILE_ID AS PAGEID, A.GROUPID, A.NORIGHTFLG, A.INSERTFLG, A.UPDATEFLG, A.DISPLAYFLG, A.DELETEFLG FROM wf_page_right_tbl A  INNER JOIN WF_MENU_TBL M ON M.PROFILE_ID = A.PAGEID AND A.BUSINESS_UNIT = M.BUSINESS_UNIT AND A.ENVIRONFLG = 0  INNER JOIN WF_MENU_TBL M1 ON ( M1.PATH LIKE CONCAT(M.PATH, '%') AND M.BUSINESS_UNIT = M1.BUSINESS_UNIT AND A.ENVIRONFLG = 0 )  1 = 1 AND GROUPID  = :GROUPID"
		def getPageMngId(PAGEID) :
			return "SELECT PAGE_MNG_ID FROM WF_PAGE_TBL WHERE PAGEID = :PAGEID"
		def updateUserPasswordAfterLogin(LOGINID, PASSWORD) :
			return "UPDATE "+utils.config.user_tableid+" SET "+utils.config.user_table_password_fieldid+" = :PASSWORD WHERE "+utils.config.user_table_userid_fieldid+" = :LOGINID"
		def updateAdminPasswordAfterLogin(LOGINID, PASSWORD) :
			return "UPDATE ADMIN_USER_TBL SET PASSWORD = :PASSWORD WHERE LOGINID = :LOGINID"

