#Dao.vm common function
from app.mapper.getthemegroups.getthemegroups_mapper import getthemegroupsMapper
import utils.mysqldb_utils
import utils.date_util
 # getthemegroups

class GetthemegroupsDao :

# 関数定義_SQL文_全テーマ一覧
     
    def getthemegroups(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(getthemegroupsMapper.getthemegroups(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
