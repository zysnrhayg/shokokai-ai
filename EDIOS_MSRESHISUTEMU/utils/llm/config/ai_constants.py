"""
AI 連携の固定定数（static/js/config.js の HV_AI_CONFIG と同期）。

環境変数（.env の HV_LLM_* / HV_AI_* / SAKURA_AI_TOKEN）は llm_config.py。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict

# config.js と同一キー・値（変更時は両方更新）
HV_AI_CONFIG: Dict[str, Any] = {
    "PROMPT_ID_API113_GENERATE_DAILY_RECORD_FEEDBACK": "api113_generate_daily_record_feedback_aiapi",
    "PROMPT_ID_API009_ANALYZE_JOURNAL": "api009_analyze_journal_aiapi",
    "PROMPT_ID_API155_ANALYZE_INTERVIEW_ALERT": "api155_analyze_interview_alert_suggestion_aiapi",
    "API_ID_API009_CALL_LOG": "API-009",
    "SCREEN_ID_API009_CALL_LOG": "SCR-110-80",
    "API_ID_API113_CALL_LOG": "API-113",
    "SCREEN_ID_API113_CALL_LOG": "SCR-110-140",
    "API_ID_API155_CALL_LOG": "API-155",
    "SCREEN_ID_API155_CALL_LOG": "SCR-110-140",
}

PROMPT_ID_API113_GENERATE_DAILY_RECORD_FEEDBACK = str(
    HV_AI_CONFIG["PROMPT_ID_API113_GENERATE_DAILY_RECORD_FEEDBACK"]
)
PROMPT_ID_API009_ANALYZE_JOURNAL = str(HV_AI_CONFIG["PROMPT_ID_API009_ANALYZE_JOURNAL"])
API_ID_API009_CALL_LOG = str(HV_AI_CONFIG["API_ID_API009_CALL_LOG"])
SCREEN_ID_API009_CALL_LOG = str(HV_AI_CONFIG["SCREEN_ID_API009_CALL_LOG"])
API_ID_API113_CALL_LOG = str(HV_AI_CONFIG["API_ID_API113_CALL_LOG"])
SCREEN_ID_API113_CALL_LOG = str(HV_AI_CONFIG["SCREEN_ID_API113_CALL_LOG"])
PROMPT_ID_API155_ANALYZE_INTERVIEW_ALERT = str(
    HV_AI_CONFIG["PROMPT_ID_API155_ANALYZE_INTERVIEW_ALERT"]
)
API_ID_API155_CALL_LOG = str(HV_AI_CONFIG["API_ID_API155_CALL_LOG"])
SCREEN_ID_API155_CALL_LOG = str(HV_AI_CONFIG["SCREEN_ID_API155_CALL_LOG"])

_CONFIG_JS_PATH = (
    Path(__file__).resolve().parents[3] / "static" / "js" / "config.js"
)


def _parse_hv_ai_config_from_js() -> Dict[str, Any]:
    """config.js から HV_AI_CONFIG オブジェクトを抽出する。"""
    text = _CONFIG_JS_PATH.read_text(encoding="utf-8")
    block_match = re.search(
        r"window\.HV_AI_CONFIG\s*=\s*\{([^}]+)\}",
        text,
        re.DOTALL,
    )
    if not block_match:
        raise RuntimeError("config.js に window.HV_AI_CONFIG が見つかりません")
    block = block_match.group(1)
    result: Dict[str, Any] = {}
    for m in re.finditer(
        r"(\w+)\s*:\s*(?:'([^']*)'|\"([^\"]*)\"|(\d+))",
        block,
    ):
        key = m.group(1)
        if m.group(2) is not None:
            result[key] = m.group(2)
        elif m.group(3) is not None:
            result[key] = m.group(3)
        else:
            result[key] = int(m.group(4))
    return result


def validate_ai_config_sync() -> None:
    """Python 定数と config.js の不一致時は起動時エラーとする。"""
    js_cfg = _parse_hv_ai_config_from_js()
    for key, py_val in HV_AI_CONFIG.items():
        if key not in js_cfg:
            raise RuntimeError(f"config.js にキーがありません: {key}")
        js_val = js_cfg[key]
        if isinstance(py_val, int):
            if int(js_val) != py_val:
                raise RuntimeError(
                    f"HV_AI_CONFIG 不一致: {key} python={py_val} js={js_val}"
                )
        elif str(js_val) != str(py_val):
            raise RuntimeError(
                f"HV_AI_CONFIG 不一致: {key} python={py_val} js={js_val}"
            )
