"""LLM ランタイム。公開 API は call_llm_common のみ。"""

from typing import Any

__all__ = ["call_llm_common"]


def __getattr__(name: str) -> Any:
    if name == "call_llm_common":
        from utils.llm.common.service import call_llm_common

        return call_llm_common
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
