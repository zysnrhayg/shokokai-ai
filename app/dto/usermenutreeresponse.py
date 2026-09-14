from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import json
class UserMenuTreeResponse:
    def __init__(self, code: Optional[str] = None):
        self.code = code or ""
        self.roles: List['UserMenu'] = []

    def get_roles(self) -> List['UserMenu']:
        return self.roles

    def set_roles(self, roles: List['UserMenu']):
        self.roles = roles

    def get_code(self) -> str:
        return self.code

    def set_code(self, code: str):
        self.code = code
        
      
class UserMenu:
    def __init__(self, user_menu_entity: 'UserMenuEntity'):
        self.user_menu_entity = user_menu_entity
        self.path = (
            "/" + user_menu_entity.PROFILE_ID
            if not user_menu_entity.PAGE_MNG_ID
            else user_menu_entity.PAGE_MNG_ID
        )
        self.name = user_menu_entity.PROFILE_ID or ""
        self.transflg = user_menu_entity.TRANSFLG or ""
        self.meta: Dict[str, str] = {"": user_menu_entity.PFOFILE_NM}
        self.children: List['UserMenu'] = []

    def get_path(self) -> str:
        return self.path

    def get_transflg(self) -> str:
        return self.transflg

    def set_path(self, path: str):
        self.path = path

    def set_transflg(self, transflg: str):
        self.transflg = transflg

    def get_component(self) -> Optional[str]:
        return getattr(self, 'component', None)

    def set_component(self, component: str):
        self.component = component

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_meta(self) -> Dict[str, str]:
        return self.meta

    def set_meta(self, meta: Dict[str, str]):
        self.meta = meta

    def get_children(self) -> List['UserMenu']:
        return self.children

    def set_children(self, children: List['UserMenu']):
        self.children = children

    def get_user_menu_entity(self) -> 'UserMenuEntity':
        return self.user_menu_entity

    def set_user_menu_entity(self, user_menu_entity: 'UserMenuEntity'):
        self.user_menu_entity = user_menu_entity
    def tomap(self):
        map = {}
        map["transflg"] = self.get_transflg()
        map["path"] = self.get_path()
        map["component"] = self.get_component()
        map["name"] = self.get_name()
        map["meta"] = {"":self.user_menu_entity.PFOFILE_NM}
        tempMap = {}
        tempMap["page_MNG_ID"] = self.user_menu_entity.PAGE_MNG_ID
        tempMap["profile_ID"] = self.user_menu_entity.PROFILE_ID
        tempMap["transflg"] = self.user_menu_entity.TRANSFLG
        tempMap["pfofile_NM"] = self.user_menu_entity.PFOFILE_NM
        tempMap["displayflg"] = int(self.user_menu_entity.DISPLAYFLG)
        tempMap["father_ID"] = self.user_menu_entity.FATHER_ID
        map["userMenuEntity"] = tempMap
        childList = []
        childReulst = self.get_children()
        self.childrenchange(childList,childReulst)
        if len(childList) > 0 :
            map["children"] = childList
        else :
            map["children"] = "null"
        return map
    
    def childrenchange(self,childList,childReulst):
        if childReulst != None :
            for child in childReulst :
                childMap = {}
                childMap["transflg"] = child.get_transflg()
                childMap["path"] = child.get_path()
                childMap["component"] = child.get_component()
                childMap["name"] = child.get_name()
                childMap["meta"] = {"",child.get_user_menu_entity().PFOFILE_NM}
                tempMap = {}
                tempMap["page_MNG_ID"] = child.get_user_menu_entity().PAGE_MNG_ID
                tempMap["profile_ID"] = child.get_user_menu_entity().PROFILE_ID
                tempMap["transflg"] = child.get_user_menu_entity().TRANSFLG
                tempMap["pfofile_NM"] = child.get_user_menu_entity().PFOFILE_NM
                tempMap["displayflg"] = int(child.get_user_menu_entity().DISPLAYFLG)
                tempMap["father_ID"] = child.get_user_menu_entity().FATHER_ID
    
                childMap["userMenuEntity"] = tempMap
                childList = []
                childReulst = child.get_children()
                self.childrenchange(childList,childReulst)
                if len(childList) > 0 :
                    childMap["children"] = childList
                else :
                    childMap["children"] = "null"
# Dummy UserMenuEntity for example purposes
class UserMenuEntity:
    def __init__(self, PAGE_MNG_ID: Optional[str], PROFILE_ID: str, TRANSFLG: Optional[str], PFOFILE_NM: str,FATHER_ID: str,DISPLAYFLG: str):
        self.PAGE_MNG_ID = PAGE_MNG_ID
        self.PROFILE_ID = PROFILE_ID
        self.TRANSFLG = TRANSFLG
        self.PFOFILE_NM = PFOFILE_NM 
        self.DISPLAYFLG = DISPLAYFLG
        self.FATHER_ID = FATHER_ID
