# MySQL データベース初期化処理。
import os
import mysql.connector
import logging

logger = logging.getLogger(__name__)

def check_database_exists(db_name):
    required = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_PORT")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "データベース初期化に必要な設定がありません: " + ", ".join(missing)
        )
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=int(os.environ["DB_PORT"])
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        result = cursor.fetchone()
        cursor.close()
        if result == None :
            with open("ddl_define.sql", 'r',encoding="UTF-8") as f:
                sql_script = f.read()
            cursor1 = conn.cursor()
            cursor1.execute(sql_script)
            cursor1.close()
            return 1
        else :
            tables=["wf_page_right_tbl","wf_page_tbl","wf_menu_tbl","wf_group_tbl"]
            deleteSystemTables(tables,conn)
            with open("ddl_define.sql", 'r',encoding="UTF-8") as f:
                lines = f.readlines()
                executeSystemTable(lines,conn)   
            return 2
    except (mysql.connector.Error, OSError, ValueError) as error:
        logger.exception("データベース初期化の確認に失敗しました: %s", error)
        raise
    finally:
        if conn is not None:
            conn.close()

# DB name: from env var, else default from project (same as run.py / mysqldb_utils when unset)
db_name = os.getenv("DB_NAME") or 'EDISEIKYUUKANRISHISUTEMU'
def installDb():
    flag = check_database_exists(db_name)
    if flag == 1 :
        logger.info("init database Success.")
    elif flag == 2 :
        logger.info("database already exists.")
    elif flag == 0 :
        logger.error("init database failed.")
    
def deleteSystemTables(tables,conn):
    for table in tables:
        cursor = conn.cursor()
        sql = " DROP TABLE IF EXISTS " + table
        cursor.execute(SSchema)
        cursor.execute(sql)
        cursor.close()

SSchema ="USE " +db_name + "; "

def executeSystemTable(lines,conn):  
    sFlag = "0"
    sSQL = ""
    for line in lines :
        arr = runSQL(line,conn,sFlag,sSQL)
        if arr != None and len(arr) > 0:
            sFlag = arr[0]
            sSQL = arr[1]
                
def runSQL(sql,conn,sFlag,sSQL):
    arr = []
    if "wf_page_right_tbl" in sql.lower() or "wf_page_tbl"  in sql.lower() or "wf_menu_tbl" in sql.lower() or "wf_group_tbl" in sql.lower() :
        if "into" in sql.lower()  :
            if "into wf_page_right_tbl" in sql.lower()  or "into wf_page_tbl" in sql.lower() or "into wf_menu_tbl" in sql.lower() or "into wf_group_tbl" in sql.lower():
                cursor = conn.cursor()
                cursor.execute(SSchema)
                cursor.execute(sql)
                cursor.close()
                conn.commit()
                arr.insert(len(arr),"0")
                arr.insert(len(arr),"")
        else :
            sSQL = sSQL + sql
            arr.insert(len(arr),"1")
            arr.insert(len(arr),sSQL)
    else :
       if sFlag == "1" :       
            if sql.find(";") > 0 :
                cursor = conn.cursor()
                cursor.execute(SSchema)
                cursor.execute(sSQL+sql)
                cursor.close()
                arr.insert(len(arr),"0")
                arr.insert(len(arr),"")
            else : 
                sSQL = sSQL + sql
                arr.insert(len(arr),"1")
                arr.insert(len(arr),sSQL)
    return arr
