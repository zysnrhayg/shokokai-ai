#Mapper.vm common function mapper
import sqlite3
#Mapper.vm

import utils.sql_utils

class api_jigyoshomeinokohokakonosodanrirekinamesMapper:
    def api_jigyoshomeinokohokakonosodanrirekinames(prefecture_code,shokokai_cd,limit):
        params = ["prefecture_code","shokokai_cd","limit"]
        values = [prefecture_code,shokokai_cd,limit]
        return utils.sql_utils.formatSQL("""SELECT business_name , MAX(report_date ) AS last_report_date FROM trn_report WHERE :prefecturecode = %s AND :shokokaicd = %s AND status != '削除' AND business_name IS NOT NULL AND business_name != '' AND business_name ILIKE %s GROUP BY business_name ORDER BY last_report_date DESC NULLS LAST :limit %s;""",params,values)
