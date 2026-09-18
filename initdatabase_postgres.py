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
        _apply_schema_patches(cfg)
        return "created"
    if not _schema_applied(cfg):
        _apply_ddl(cfg, ddl_path)
        _apply_schema_patches(cfg)
        return "schema_applied"
    _apply_schema_patches(cfg)
    return "exists"


def _apply_schema_patches(cfg: dict) -> None:
    """既存DB向けの不足スキーマを補完する（添付テーブル・文書ステータスCHECK）。"""
    with psycopg.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        dbname=cfg["dbname"],
        autocommit=True,
        connect_timeout=10,
    ) as conn:
        # C-8/C-9/R-4: 添付保存用テーブルが無い既存DBへ作成する
        conn.execute(
            """
            CREATE SEQUENCE IF NOT EXISTS public.trn_report_attachment_report_attachment_id_seq
                AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS public.trn_report_attachment (
                report_attachment_id integer NOT NULL
                    DEFAULT nextval('public.trn_report_attachment_report_attachment_id_seq'::regclass),
                report_id integer NOT NULL,
                file_path text NOT NULL,
                CONSTRAINT trn_report_attachment_pkey PRIMARY KEY (report_attachment_id),
                CONSTRAINT trn_report_attachment_report_id_fkey
                    FOREIGN KEY (report_id) REFERENCES public.trn_report(report_id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            ALTER SEQUENCE public.trn_report_attachment_report_attachment_id_seq
                OWNED BY public.trn_report_attachment.report_attachment_id
            """
        )
        # K-3: UIステータス（公開中/審査中/非公開）をCHECKへ追加する
        # 既に同一制約がある場合は作り直す（起動毎でも安全）
        try:
            conn.execute(
                """
                ALTER TABLE public.trn_knowledge_document_version
                    DROP CONSTRAINT IF EXISTS mst_knowledge_document_version_status_check
                """
            )
            conn.execute(
                """
                ALTER TABLE public.trn_knowledge_document_version
                    ADD CONSTRAINT mst_knowledge_document_version_status_check
                    CHECK (status = ANY (ARRAY[
                        '登録済み'::text, '旧版'::text, '処理中'::text, 'エラー'::text,
                        '公開中'::text, '審査中'::text, '非公開'::text
                    ]))
                """
            )
        except Exception:
            # 文書テーブルが無い環境でもアプリ起動を止めない
            pass


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(os.path.join(_ROOT, ".env"))
    status = ensure_database()
    print("database init:", status)
    sys.exit(0)
