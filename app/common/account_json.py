# account detail fields -> JSONWFCObject
import json
from app.common.account_list_row import account_row_to_selmap

def put_account_on_json(jsonObj, entity):
    """Set flat account fields for mockup SPA consumption."""
    row = account_row_to_selmap(entity)
    for key, value in row.items():
        if key == "qualification_codes":
            jsonObj.setValue(key, json.dumps(value, ensure_ascii=False))
        elif value is None:
            jsonObj.setValue(key, "")
        elif isinstance(value, bool):
            jsonObj.setValue(key, "true" if value else "false")
        else:
            jsonObj.setValue(key, value)
    jsonObj.setValue("account", json.dumps(row, ensure_ascii=False))
    return row
