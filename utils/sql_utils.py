# sql_utils.py
#
# SECURITY: formatSQL is ONLY for "conditional fragment inclusion" logic (e.g. <ifX>...</ifX>).
# - Do NOT concatenate user input into the 'sql' string. params/values only control which
#   <if> fragments are kept; they do NOT replace proper SQL parameterization.
# - All user-supplied values MUST be passed as bound parameters to execute(), not in sql.
#
# When the value is empty, replace the characters in the query field
import re
import logging
_logger = logging.getLogger(__name__)

def formatSQL(sql,params,values):
    if isinstance(sql, tuple):
        sql = ''.join(sql)
    if "'" in sql and "<if" not in sql:
        # Static SQL literals (e.g. to_timestamp(..., 'YYYY-MM-DD HH24:MI:SS')) are common; if named
        # binds are present, user values should be in params, not the template string.
        if re.search(r":[A-Za-z_][A-Za-z0-9_]*", sql):
            _logger.debug(
                "formatSQL: sql contains single-quote with named binds (likely SQL literal); ensure no user input is concatenated"
            )
        else:
            _logger.warning("formatSQL: sql contains single-quote; ensure no user input is concatenated")
    if len(params) == 0:
        return delIf(sql)
    for i in range(0, len(params)):
        keyStringStart = "<if" + params[i] + ">"
        keyStringEnd = "</if" + params[i] + ">"
        # 未输入检索条件时可能为 "" 或 None，都视为空并移除该条件块
        val_empty = values[i] is None or (isinstance(values[i], str) and values[i].strip() == "")
        if not val_empty:
            continue
        # 同一参数可能对应多个 <ifX>...</ifX> 块（如 KIIWAADO 对应多列 LIKE），需全部移除
        while True:
            start_index = sql.find(keyStringStart)
            end_index = sql.find(keyStringEnd)
            if start_index < 0 or end_index < 0 or end_index < start_index:
                break
            sql = sql[0:start_index] + sql[end_index + len(keyStringEnd):len(sql)]

    if sql.find("<if") > 0 and sql.find("</if") > 0:
        for i in range(0,len(params)) :
            sql = sql.replace("<if"+params[i]+">","")  
            sql = sql.replace("</if"+params[i]+">","")  
    
    if "AND (  AND" in sql:
        sql = sql.replace("AND (  AND", "AND ( ")
    # 标准检索等：所有条件被移除后可能留下 AND ( 仅空格 )，导致语法错误，整段去掉
    sql = re.sub(r"AND\s*\(\s*\)", "", sql)
    return sql


def delIf(a):
    if isinstance(a, tuple):
        a = ''.join(a)
    if "<if" in a:
        startIndex = a.find("<if")
        endIndex = a.find(">")
        sql = a[0:startIndex] + a[endIndex+1:len(a)]
        
        startIndex = sql.find("</if")
        endIndex = sql.find(">")
        sql = sql[0:startIndex] + sql[endIndex+1:len(sql)]
        
        if "<if" in sql :
            return delIf(sql)
        else :
           return sql
    else :
        return a
