#base_entity.py make BaseEntity
from flask import request, session
from flask import current_app as app
import utils.session_constant  
class BaseEntity:
    def __init__(self,mode,actflg,triggerid,row):
        self.mode = mode
        self.actflg = actflg
        self.triggerid = triggerid
        self.user_id = session.get(utils.session_constant.USER_ID,"")
        self.user_name = session.get("USER_NAME1","")
        self.row = row
   		
