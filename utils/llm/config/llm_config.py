"""LLM ランタイム設定（さくらの AI Engine）。.env のみ参照。"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

_DEFAULT_SAKURA_URL = "https://api.ai.sakura.ad.jp/v1/chat/completions"
_DEFAULT_MODEL = "cotomi3"


def _env_str(key: str, default: str = "") -> str:
    """環境変数（.env）のみ。"""
    raw = os.getenv(key)
    if raw is not None and str(raw).strip() != "":
        return str(raw).strip()
    return default


def _env_bool(key: str, default: bool = False) -> bool:
    raw = os.getenv(key)
    if raw is None or str(raw).strip() == "":
        return default
    return str(raw).strip().lower() in ("true", "1", "yes", "on")


def _env_int(key: str, default: int) -> int:
    raw = _env_str(key, str(default))
    try:
        return int(raw)
    except ValueError:
        return default


def _env_float(key: str, default: float) -> float:
    raw = _env_str(key, str(default))
    try:
        return float(raw)
    except ValueError:
        return default


def _env_json_dict(key: str) -> Dict[str, Any]:
    raw = _env_str(key, "")
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def load_llm_config() -> Dict[str, Any]:
    """LLM 用設定辞書（.env / 環境変数）。"""
    return {
        "enabled": _env_bool("HV_LLM_ENABLED", False),
        "require_real_api": _env_bool("HV_LLM_REQUIRE_REAL_API", True),
        "timeout_seconds": _env_int("HV_LLM_TIMEOUT_SECONDS", 60),
        "max_retries": _env_int("HV_LLM_MAX_RETRIES", 2),
        "retry_backoff_ms": _env_int("HV_LLM_RETRY_BACKOFF_MS", 300),
        "default_model_name": _env_str("HV_LLM_DEFAULT_MODEL", _DEFAULT_MODEL),
        "system_prompt": _env_str("HV_LLM_SYSTEM_PROMPT", ""),
        "temperature": _env_float("HV_LLM_TEMPERATURE", 0.2),
        "max_tokens": _env_int("HV_LLM_MAX_TOKENS", 2048),
        "response_schema": _env_json_dict("HV_LLM_RESPONSE_SCHEMA"),
        "sakura_api_url": _env_str("SAKURA_AI_URL", _DEFAULT_SAKURA_URL),
        "sakura_api_token": _env_str("SAKURA_AI_TOKEN"),
    }


def validate_provider_credentials(cfg: Dict[str, Any]) -> None:
    """LLM 有効時、SAKURA_AI_TOKEN / SAKURA_AI_URL を検証。"""
    if not cfg.get("enabled"):
        return
    if not cfg.get("sakura_api_token"):
        raise RuntimeError("HV_LLM_ENABLED is true but SAKURA_AI_TOKEN is not set in .env")
    if not cfg.get("sakura_api_url"):
        raise RuntimeError("SAKURA_AI_URL is not set in .env")
