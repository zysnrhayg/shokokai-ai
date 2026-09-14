from typing import Dict

from exts import db


# Execute SQL query
def execute_query(query, param: Dict):
    try:
        result = db.session.execute(str(query), param).fetchone()
        return result[0] if result else None
    finally:
        db.session.close()
