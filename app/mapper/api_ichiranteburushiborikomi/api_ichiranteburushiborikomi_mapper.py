#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_ichiranteburushiborikomiMapper:
    def api_ichiranteburushiborikomi(mst_user_account_prefecture_code,mst_user_account_shokokai_cd,limit,offset):
        params = ["mst_user_account_prefecture_code","mst_user_account_shokokai_cd","limit","offset"]
        values = [mst_user_account_prefecture_code,mst_user_account_shokokai_cd,limit,offset]
        return utils.sql_utils.formatSQL(
            """SELECT mst_user_account.user_account_id
     , mst_user_account.prefecture_code
     , mst_user_account.shokokai_cd
     , mst_user_account.user_id
     , mst_user_account.shokuin_kj
     , mst_user_account.email
     , mst_user_account.status
     , mst_user_account.core_linked
     , mst_user_account.permission_level
     , mst_user_account.last_login_at
     , mst_prefecture.name AS prefecture_name
     , mst_shokokai.name AS shokokai_name
     , COALESCE(
         (
           SELECT array_agg(mst_qualification.qualification_code ORDER BY mst_qualification.qualification_code)
           FROM mst_user_account_qualification
           INNER JOIN mst_qualification
             ON mst_qualification.qualification_id = mst_user_account_qualification.qualification_id
           WHERE mst_user_account_qualification.user_account_id = mst_user_account.user_account_id
         ),
         ARRAY[]::text[]
       ) AS qualification_codes
FROM mst_user_account
INNER JOIN mst_prefecture
  ON mst_prefecture.prefecture_code = mst_user_account.prefecture_code
INNER JOIN mst_shokokai
  ON mst_shokokai.prefecture_code = mst_user_account.prefecture_code
 AND mst_shokokai.shokokai_cd = mst_user_account.shokokai_cd
WHERE mst_user_account.deleted_at IS NULL
<ifmst_user_account_prefecture_code> AND mst_user_account.prefecture_code = :mstuseraccountprefecturecode </ifmst_user_account_prefecture_code>
<ifmst_user_account_shokokai_cd> AND mst_user_account.shokokai_cd = :mstuseraccountshokokaicd </ifmst_user_account_shokokai_cd>
ORDER BY mst_prefecture.sort_order NULLS LAST
       , mst_shokokai.sort_order NULLS FIRST
       , mst_user_account.user_id
<iflimit> LIMIT :limit </iflimit>
<ifoffset> OFFSET :offset </ifoffset>""",
            params,
            values,
        )
