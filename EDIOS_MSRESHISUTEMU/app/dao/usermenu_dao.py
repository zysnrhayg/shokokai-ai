from app.mapper.usermenu_mapper import UsermenuMapper
import utils.mysqldb_utils
class UsermenuDao:
	def getusergroup(USERID) :
		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(UsermenuMapper.getusergroup(USERID),{"USERID":USERID}))
		
	def getbusinessusergroup(LOGINID,LOGINPASSWORD,DEPARTID,LOGINTABLEID,WHRLOGINID) :
		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(UsermenuMapper.getbusinessusergroup(LOGINID,LOGINPASSWORD,DEPARTID,LOGINTABLEID,WHRLOGINID),{"LOGINID":LOGINID,"LOGINPASSWORD":LOGINPASSWORD,"DEPARTID":DEPARTID,"LOGINTABLEID":LOGINTABLEID,"WHRLOGINID":WHRLOGINID}))
	
	def getusermenu(USERID, groupIds) :
		return utils.mysqldb_utils.result_to_list_of_dict(utils.mysqldb_utils.querySQL(UsermenuMapper.getusermenu(USERID, groupIds),{"USERID":USERID,"groupIds":groupIds}))
	
