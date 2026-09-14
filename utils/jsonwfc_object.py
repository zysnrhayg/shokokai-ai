#jsonwfc_object.py
#JSONWFCObject.vm make json common method
import json
from typing import Any, Dict, List, Optional, Union

class JSONWFCObject:
    response = {}
    def __init__(self):
        self.response = {}

    def setJosnObj(self,newJosonObj) :
        self.response = newJosonObj
        
    def setValue(self,key,value):
        if value == "None" : 
            value = ""
        self.response[key] = value
    
    def setHtml(self,key,value):
        if value == "None" : 
            value = ""
        self.response[key] = value
           
    def setReturnID(self,key,value):
        if value == "None" : 
            value = ""
        arrayList = self.response.get(key)
        if arrayList == None :
            arrayList = []
        arrayList.insert(len(arrayList),value)
        self.response[key] = arrayList
    	
    def setScript(self,key,value):
        if value == "None" : 
            value = ""
        v = self.response.get(key)
        if v == None :
            v = ""
        v = v+value
        self.response[key] = v

    def setAction(self, action_type: str, payload: Any = None) -> None:
        """Append a client/server action for template_figma.js (key ``a`` → applyResponseActions)."""
        if payload is None:
            payload = {}
        actions = self.response.get("a")
        if actions is None:
            actions = []
            self.response["a"] = actions
        elif not isinstance(actions, list):
            actions = [actions]
            self.response["a"] = actions
        actions.append({"type": action_type, "payload": payload})
    def toJsonString(self):
        return  json.dumps(self.response)
    
    def getJsonObj(self):
        return self.response
