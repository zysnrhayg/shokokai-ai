"""
LLM 応答文字列の JSON 抽出と response_schema による検証。

- マークダウン ```json フェンスの除去
- JSON Schema のサブセット（type, required, properties, enum）
- レガシー形式: required_keys / allowed_keys（propm 互換の簡易ホワイトリスト）
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional, Tuple, Union

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.IGNORECASE)


def extract_json_object(raw: str) -> Optional[Dict[str, Any]]:
    """
    モデル出力から先頭の JSON オブジェクトを dict として取り出す。

    Args:
        raw: LLM の message.content 全文

    Returns:
        パース成功時 dict、失敗時 None
    """
    if not raw or not isinstance(raw, str):
        return None
    text = raw.strip()
    fence = _JSON_FENCE_RE.search(text)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def parse_llm_json(raw: str) -> Dict[str, Any]:
    """
    extract_json_object の厳密版。失敗時 ValueError。

    call_llm_common 内で必須パースに使用する。
    """
    obj = extract_json_object(raw)
    if obj is None:
        raise ValueError("LLM response is not a valid JSON object")
    return obj


def validate_response_schema(
    data: Dict[str, Any],
    schema: Union[Dict[str, Any], str, None],
) -> Tuple[bool, str]:
    """
    DB の response_schema に対して data を検証する。

    Args:
        data: parse_llm_json の結果
        schema: JSONB または JSON 文字列。空なら検証スキップ（True）

    Returns:
        (OK なら True, エラー時は False とメッセージ)
    """
    if not schema:
        return True, ""
    if isinstance(schema, str):
        try:
            schema = json.loads(schema)
        except json.JSONDecodeError as exc:
            return False, f"response_schema is invalid JSON: {exc}"
    if not isinstance(schema, dict):
        return False, "response_schema must be a JSON object"

    if "required_keys" in schema or "allowed_keys" in schema:
        return _validate_keys_only(data, schema)

    schema_type = schema.get("type")
    if schema_type and schema_type != "object":
        return False, f"unsupported schema type: {schema_type}"
    if schema_type == "object" or "properties" in schema or "required" in schema:
        return _validate_json_schema_object(data, schema)
    return True, ""


def _validate_keys_only(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, str]:
    """required_keys 必須・allowed_keys 以外のキー禁止。"""
    required = schema.get("required_keys") or []
    allowed = schema.get("allowed_keys")
    for key in required:
        if key not in data:
            return False, f"missing required key: {key}"
    if allowed is not None:
        extra = set(data.keys()) - set(allowed)
        if extra:
            return False, f"unexpected keys: {sorted(extra)}"
    return True, ""


def _validate_json_schema_object(
    data: Dict[str, Any],
    schema: Dict[str, Any],
    path: str = "",
) -> Tuple[bool, str]:
    """object 型スキーマの再帰検証。"""
    if not isinstance(data, dict):
        return False, f"{path or 'root'}: expected object"

    for req in schema.get("required") or []:
        if req not in data:
            return False, f"missing required property: {req}"

    properties = schema.get("properties") or {}
    for key, prop_schema in properties.items():
        if key not in data:
            continue
        ok, err = _validate_value(data[key], prop_schema, f"{path}.{key}" if path else key)
        if not ok:
            return False, err

    additional = schema.get("additionalProperties", True)
    if additional is False:
        extra = set(data.keys()) - set(properties.keys())
        if extra:
            return False, f"additional properties not allowed: {sorted(extra)}"

    return True, ""


def _validate_value(value: Any, prop_schema: Dict[str, Any], path: str) -> Tuple[bool, str]:
    """プロパティ 1 件の型・enum・ネスト object/array を検証。"""
    expected_type = prop_schema.get("type")
    if expected_type:
        if not _type_matches(value, expected_type):
            return False, f"{path}: expected type {expected_type}"
    if "enum" in prop_schema and value not in prop_schema["enum"]:
        return False, f"{path}: value not in enum"
    if expected_type == "object":
        return _validate_json_schema_object(value, prop_schema, path)
    if expected_type == "array":
        if not isinstance(value, list):
            return False, f"{path}: expected array"
        item_schema = prop_schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(value):
                ok, err = _validate_value(item, item_schema, f"{path}[{i}]")
                if not ok:
                    return False, err
    return True, ""


def _type_matches(value: Any, expected: str) -> bool:
    """JSON Schema の type 文字列と Python 型の対応。"""
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "null":
        return value is None
    return True
