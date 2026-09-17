# Load SQL statement from file
def read_sql_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# ---------------------------------------------------------------------------
# アップロードファイル保存ユーティリティ
# settings.toml の UPLOAD_DIR（既定: <プロジェクトルート>/uploads）配下へ実保存する
# ---------------------------------------------------------------------------
import os
import re
import uuid
from datetime import datetime, timezone, timedelta


def get_upload_root():
    """アップロードルートディレクトリ（UPLOAD_DIR）の絶対パスを返す。"""
    from config import get_upload_dir
    return get_upload_dir()


def save_upload_file(file_storage, subdir):
    """
    アップロードファイルを <UPLOAD_DIR>/<subdir>/YYYYMM/ 配下へ実保存する。

    @param file_storage werkzeug FileStorage（request.files の各要素）
    @param subdir 保存先サブディレクトリ（例: 'report', 'knowledge'）
    @return DB保存用の相対パス（uploads/<subdir>/YYYYMM/<ファイル名>、区切りは'/'固定）。
            ファイルが無い場合は空文字を返す。
    """
    if file_storage is None:
        return ""
    original_name = os.path.basename(getattr(file_storage, "filename", "") or "")
    if not original_name:
        return ""

    # 保存先ディレクトリ（<UPLOAD_DIR>/<subdir>/YYYYMM）を用意する
    jst_now = datetime.now(timezone(timedelta(hours=9)))
    upload_root = get_upload_root()
    save_dir = os.path.join(upload_root, subdir, jst_now.strftime("%Y%m"))
    os.makedirs(save_dir, exist_ok=True)

    # ファイル名の重複防止のためユニーク名を生成する（元ファイル名は安全化して保持）
    base, ext = os.path.splitext(original_name)
    safe_base = re.sub(r"[^\w\-]", "_", base)[:50] or "file"
    save_name = safe_base + "_" + jst_now.strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8] + ext
    save_path = os.path.join(save_dir, save_name)
    file_storage.save(save_path)

    # DB保存用の相対パス（UPLOAD_DIR名から始まる、区切りは'/'に統一）
    upload_dir_name = os.path.basename(upload_root.rstrip("\\/"))
    rel = os.path.relpath(save_path, upload_root).replace("\\", "/")
    return upload_dir_name + "/" + rel


def get_upload_abs_path(rel_path):
    """DB保存用の相対パス（uploads/...）から実ファイルの絶対パスを返す。"""
    rel = str(rel_path or "").replace("\\", "/").strip("/")
    if not rel:
        return ""
    upload_root = get_upload_root()
    upload_dir_name = os.path.basename(upload_root.rstrip("\\/"))
    if rel == upload_dir_name or rel.startswith(upload_dir_name + "/"):
        rel = rel[len(upload_dir_name) + 1:]
    return os.path.join(upload_root, rel)
