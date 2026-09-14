"""
Prompt テンプレートの {{ドット区切り}} プレースホルダ置換。

例: {{session.user_id}}, {{db_values.journal}}, {{extra_context.instruction}}
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

# {{ session.user_id }} のようなプレースホルダを検出
_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")


def build_llm_context(
    session: Optional[Dict[str, Any]] = None,
    db_values: Optional[Dict[str, Any]] = None,
    extra_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    テンプレート用の統一コンテキスト dict を組み立てる。

    トップレベルキーは session / db_values / extra_context の 3 つ固定。
    """
    return {
        "session": session or {},
        "db_values": db_values or {},
        "extra_context": extra_context or {},
    }


def resolve_path(context: Dict[str, Any], path: str) -> Any:
    """
    ドット区切りパスでネスト dict から値を取得する。

    Args:
        context: build_llm_context の戻り値
        path: 例 "session.user_id"

    Returns:
        見つからない場合は None
    """
    parts = path.split(".")
    cur: Any = context
    for part in parts:
        if not isinstance(cur, dict):
            return None
        if part not in cur:
            return None
        cur = cur[part]
    return cur


def _value_to_text(value: Any) -> str:
    """テンプレート埋め込み用に値を文字列化（list/dict は JSON）。"""
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def render_template(template: str, context: Dict[str, Any]) -> str:
    """
    テンプレート内の {{path}} を context の値で置換する。

    Args:
        template: プロンプト本文 / system_prompt 等
        context: build_llm_context の戻り値

    Returns:
        置換後の文字列。template が空なら ""
    """
    if not template:
        return ""

    def _repl(match: re.Match) -> str:
        return _value_to_text(resolve_path(context, match.group(1)))

    return _PLACEHOLDER_RE.sub(_repl, template)
