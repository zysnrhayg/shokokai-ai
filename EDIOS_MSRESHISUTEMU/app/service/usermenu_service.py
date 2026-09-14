from app.dao.usermenu_dao import UsermenuDao
import utils.config
import utils.string_util
class UsermenuService:
  def getusermenu(loginid) :
		#login_tableid取得
    login_tableid = utils.config.user_tableid
        # login_id取得
    login_id = utils.config.user_table_userid_fieldid
        # login_password取得
    login_password = utils.config.user_table_password_fieldid
        # userId取得
    userId = utils.config.user_table_user_fieldid
        # user_eff取得
    user_eff = utils.config.user_table_eff_status_fieldid
        # user_Group取得
    user_Group = utils.config.user_table_group_fieldid
        
    groupIds = None
    if "admin" == loginid :
        groupIds = UsermenuDao.getusergroup(loginid)
    else :
      groupIds = UsermenuDao.getbusinessusergroup(loginid,login_password,user_Group,login_tableid,login_id)
        
 
    return UsermenuDao.getusermenu(loginid,groupIds)
