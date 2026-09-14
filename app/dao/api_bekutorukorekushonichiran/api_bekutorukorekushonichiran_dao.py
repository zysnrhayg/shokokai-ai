#Dao.vm common function
from app.mapper.api_bekutorukorekushonichiran.api_bekutorukorekushonichiran_mapper import api_bekutorukorekushonichiranMapper
import utils.mysqldb_utils
import utils.date_util
 # api_bekutorukorekushonichiran

class ApiBekutorukorekushonichiranDao :

# 関数定義_SQL文_ベクトルコレクション一覧
     
    def api_bekutorukorekushonichiran(self,dtoObj) :
        returnVal = utils.mysqldb_utils.querySQL(api_bekutorukorekushonichiranMapper.api_bekutorukorekushonichiran(),{})
        return utils.mysqldb_utils.result_to_list_of_dict(returnVal)
    
