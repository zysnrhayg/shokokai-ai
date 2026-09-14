class UsermenuMapper:
	def getusergroup( USERID):
		return "select M1.GROUP_ID from WF_GROUP_USER_TBL A inner join WF_GROUP_TBL M on M.GROUP_ID = A.GROUP_ID and M.BUSINESS_UNIT = A.BUSINESS_UNIT inner join WF_GROUP_TBL M1 on ( M.LEFTID >= M1.LEFTID and M.RIGHTID <= M1.RIGHTID and M.ENVIRONFLG = M1.ENVIRONFLG and M.BUSINESS_UNIT = M1.BUSINESS_UNIT ) where A.USERID = :USERID"
		
	def getbusinessusergroup(LOGINID,LOGINPASSWORD,DEPARTID,LOGINTABLEID,WHRLOGINID):
		return "SELECT g.USER_VALUE1 as GROUP_ID FROM "+LOGINTABLEID+" INNER JOIN wf_user_value_rel_map_tbl g ON "+LOGINTABLEID+"."+DEPARTID+" = g.USER_VALUE2 WHERE "+WHRLOGINID+" = '"+LOGINID+"'"
	
	def getusermenu(USERID,GROUPIDS):
		sql = "select BL.PROFILE_ID, BL.FATHER_ID, BL.PFOFILE_NM, C.PAGE_MNG_ID , BL.CONTENTS, BL.FROMFLG, C.OURURL , C.PC_MB_FLG , BL.RIGHTTYPE, BL.DISPLAYFLG, C.TRANSFLG, C.INSERTFLG, C.UPDATEFLG, C.FREE_FIELD4, BL.path from ( select AL.PROFILE_ID, AL.FATHER_ID, AL.PFOFILE_NM, AL.CONTENTS, AL.FROMFLG, AL.RIGHTTYPE, AL.DISPLAYFLG, AL.PATH from ( select distinct M1.PROFILE_ID, M1.PFOFILE_NM, M1.FATHER_ID, A.RIGHTTYPE, M1.FROMFLG, M1.CONTENTS, M1.PATH, M1.DISPLAYFLG from WF_PAGE_RIGHT_TBL A inner join WF_MENU_TBL M on M.PROFILE_ID = A.PAGEID and A.BUSINESS_UNIT = M.BUSINESS_UNIT inner join WF_MENU_TBL M1 on ( M1.PATH like CONCAT(M.PATH, '%') and M.BUSINESS_UNIT = M1.BUSINESS_UNIT) where ( A.USERID = :USERID or ( "
		if GROUPIDS != None:
			ids = list(GROUPIDS) if not isinstance(GROUPIDS, list) else (GROUPIDS or [])
			if len(ids) > 0 :
				sql += " A.GROUPID in ("
				varSql = ""
				for id_row in ids :
					gid = id_row.get("GROUP_ID", None) if isinstance(id_row, dict) else getattr(id_row, "GROUP_ID", None)
					if gid is not None:
						varSql = varSql + "'"+str(gid)+"',"
				idSql = varSql[:-1] if len(varSql) > 0 else ""
				if idSql:
					sql += idSql + " ) and "
		sql += " A.USERID = ''))) AL group by AL.PROFILE_ID having COUNT(*) = 1 and AL.RIGHTTYPE = '2') BL left join WF_PAGE_TBL C on BL.PROFILE_ID = C.PAGEID order by BL.PATH, BL.PROFILE_ID"
		return sql
