from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine, text

url = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url)
with engine.connect() as c:
    rows = c.execute(
        text(
            """
            SELECT user_id, prefecture_code, status, is_mfa_enabled,
                   CASE
                     WHEN password IS NULL OR password = '' THEN 'empty'
                     WHEN password LIKE '$2%' THEN 'bcrypt'
                     WHEN length(password) = 40 THEN 'sha1'
                     ELSE 'plain_or_other'
                   END AS pwd_type
            FROM mst_user_account
            WHERE deleted_at IS NULL AND status = 1
            ORDER BY user_account_id
            LIMIT 8
            """
        )
    ).mappings().all()
    for r in rows:
        print(dict(r))
    deleted = c.execute(
        text(
            """
            SELECT user_id, prefecture_code
            FROM mst_user_account
            WHERE deleted_at IS NOT NULL AND lower(user_id)=lower('000')
            LIMIT 1
            """
        )
    ).mappings().first()
    print("deleted_000", dict(deleted) if deleted else None)
