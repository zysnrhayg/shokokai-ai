#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api183_accountsfilterMapper:
    def api183_accountsfilter(prefecture_code,shokokai_cd,permission_level,status,core_linked,keyword):
        params = ["prefecture_code","shokokai_cd","permission_level","status","core_linked","keyword"]
        values = [prefecture_code,shokokai_cd,permission_level,status,core_linked,keyword]
        return utils.sql_utils.formatSQL("""SELECT mst_user_account.user_account_id , mst_user_account.:prefecturecode , mst_user_account.:shokokaicd , mst_user_account.user_id , mst_user_account.shokuin_kj , mst_user_account.email , mst_user_account.:status , mst_user_account.:corelinked , mst_user_account.:permissionlevel , mst_user_account.last_login_at , mst_prefecture.name AS prefecture_name , mst_shokokai.name AS shokokai_name FROM mst_user_account JOIN mst_prefecture ON mst_prefecture.prefecture_code = mst_user_account.prefecture_code JOIN mst_shokokai ON mst_shokokai.prefecture_code = mst_user_account.prefecture_code AND mst_shokokai.shokokai_cd = mst_user_account.shokokai_cd WHERE ( (%s = 'national' AND mst_user_account.shokokai_cd = %s ) OR (%s = 'pref' AND mst_user_account.prefecture_code = %s AND mst_user_account.shokokai_cd <> %s ) OR (%s = 'shokokai' AND mst_user_account.prefecture_code = %s AND mst_user_account.shokokai_cd = %s ) ) / * 都道府県 * / AND ( %s IS NULL OR %s = '' OR mst_user_account.prefecture_code = %s ) / * 商工会 * / AND ( %s IS NULL OR %s = '' OR mst_user_account.shokokai_cd = %s ) / * 権限レベル * / AND ( %s IS NULL OR %s = '' OR mst_user_account.permission_level = %s ) / * ステータス * / AND ( %s IS NULL OR mst_user_account.status = %s ) / * コア連携 * / AND ( %s IS NULL OR %s = '' OR mst_user_account.core_linked = %s ) / * キーワード：ユーザID・職員名・メールアドレス * / AND ( %s IS NULL OR %s = '' OR mst_user_account.user_id ILIKE '%%' || %s || '%%' OR mst_user_account.shokuin_kj ILIKE '%%' || %s || '%%' OR mst_user_account.email ILIKE '%%' || %s || '%%' ) ORDER BY mst_prefecture.sort_order , mst_shokokai.sort_order NULLS FIRST , mst_user_account.user_id;""",params,values)
