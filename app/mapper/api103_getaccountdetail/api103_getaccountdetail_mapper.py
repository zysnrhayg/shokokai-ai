#Mapper.vm common function mapper
import utils.sql_utils

class api103_getaccountdetailMapper:
    def api103_getaccountdetail(user_account_id):
        params = ["user_account_id"]
        values = [user_account_id]
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
     , mst_user_account.is_mfa_enabled
     , mst_user_account.failed_login_count
     , mst_user_account.locked_until
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
LEFT JOIN mst_prefecture
  ON mst_prefecture.prefecture_code = mst_user_account.prefecture_code
LEFT JOIN mst_shokokai
  ON mst_shokokai.prefecture_code = mst_user_account.prefecture_code
 AND mst_shokokai.shokokai_cd = mst_user_account.shokokai_cd
WHERE mst_user_account.user_account_id = :user_account_id
  AND mst_user_account.deleted_at IS NULL""",
            params,
            values,
        )
