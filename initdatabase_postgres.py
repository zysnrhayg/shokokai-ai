# -*- coding: utf-8 -*-
"""Create the PostgreSQL database when missing and apply ddl_define.sql."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlparse

import psycopg

_ROOT = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
_DDL_PATH = os.path.join(_ROOT, "ddl_define.sql")
_PSQL_CANDIDATES = (
    os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "PostgreSQL", "18", "bin", "psql.exe"),
    os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "PostgreSQL", "16", "bin", "psql.exe"),
    os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "PostgreSQL", "15", "bin", "psql.exe"),
)


def _parse_database_uri(uri: str) -> dict:
    raw = (uri or "").strip()
    if raw.startswith("postgresql+psycopg://"):
        raw = "postgresql://" + raw[len("postgresql+psycopg://") :]
    elif raw.startswith("postgresql+psycopg2://"):
        raw = "postgresql://" + raw[len("postgresql+psycopg2://") :]
    parsed = urlparse(raw)
    dbname = unquote((parsed.path or "").lstrip("/"))
    if not dbname:
        raise RuntimeError("DATABASE_URI にデータベース名がありません。")
    return {
        "host": parsed.hostname or "127.0.0.1",
        "port": parsed.port or 5432,
        "user": unquote(parsed.username or "postgres"),
        "password": unquote(parsed.password or ""),
        "dbname": dbname,
    }


def _find_psql() -> str:
    found = shutil.which("psql")
    if found:
        return found
    for path in _PSQL_CANDIDATES:
        if os.path.isfile(path):
            return path
    raise RuntimeError("psql が見つかりません。PostgreSQL の bin を PATH に追加してください。")


def _admin_connect(cfg: dict):
    return psycopg.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        dbname="postgres",
        autocommit=True,
        connect_timeout=10,
    )


def _database_exists(cfg: dict) -> bool:
    with _admin_connect(cfg) as conn:
        row = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (cfg["dbname"],),
        ).fetchone()
    return row is not None


def _schema_applied(cfg: dict) -> bool:
    with psycopg.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        dbname=cfg["dbname"],
        connect_timeout=10,
    ) as conn:
        row = conn.execute("SELECT to_regclass('public.mst_user_account')").fetchone()
    return bool(row and row[0])


def _create_database(cfg: dict) -> None:
    from psycopg import sql

    with _admin_connect(cfg) as conn:
        conn.execute(
            sql.SQL("CREATE DATABASE {} OWNER {} ENCODING 'UTF8'").format(
                sql.Identifier(cfg["dbname"]),
                sql.Identifier(cfg["user"]),
            )
        )


def _apply_ddl(cfg: dict, ddl_path: str) -> None:
    if not os.path.isfile(ddl_path):
        raise RuntimeError("DDL ファイルが見つかりません: " + ddl_path)
    psql = _find_psql()
    env = os.environ.copy()
    env["PGPASSWORD"] = cfg["password"]
    env["PGCLIENTENCODING"] = "UTF8"
    result = subprocess.run(
        [
            psql,
            "-h",
            str(cfg["host"]),
            "-p",
            str(cfg["port"]),
            "-U",
            cfg["user"],
            "-d",
            cfg["dbname"],
            "-v",
            "ON_ERROR_STOP=1",
            "-f",
            ddl_path,
        ],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError("ddl_define.sql の適用に失敗しました:\n" + detail)


def ensure_database(uri: str | None = None, ddl_path: str | None = None) -> str:
    """Create the target database and apply ddl_define.sql when missing."""
    if uri is None:
        from config import get_database_uri

        uri = get_database_uri()
    if not uri:
        raise RuntimeError("DATABASE_URI が未設定です。")
    cfg = _parse_database_uri(uri)
    ddl_path = ddl_path or _DDL_PATH

    if not _database_exists(cfg):
        _create_database(cfg)
        _apply_ddl(cfg, ddl_path)
        return "created"
    if not _schema_applied(cfg):
        _apply_ddl(cfg, ddl_path)
        return "schema_applied"
    return "exists"


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(os.path.join(_ROOT, ".env"))
    status = ensure_database()
    print("database init:", status)
    sys.exit(0)
