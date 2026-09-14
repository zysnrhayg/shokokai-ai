"""

さくらの AI Engine 向け LLM HTTP クライアント。



- Chat Completions（docs/sakura.md 準拠）

- urllib 使用

- 同一エンドポイントに対するリトライのみ

"""



from __future__ import annotations



import json

import logging

import time

from typing import Any, Dict, Tuple

from urllib import error as urlerror

from urllib import request as urlrequest



from utils.llm.config.llm_config import load_llm_config, validate_provider_credentials



logger = logging.getLogger(__name__)



# プロンプト最大長（過大入力防止）

_MAX_MESSAGE_CHARS = 120000





class LlmClient:

    """さくら AI API を呼び出すクライアント。"""



    def __init__(self, config: Dict[str, Any] | None = None) -> None:

        """

        Args:

            config: None のとき load_llm_config() を使用

        """

        self.config = config if config is not None else load_llm_config()

        validate_provider_credentials(self.config)



    def chat_completion_json(

        self,

        *,

        system_text: str,

        user_text: str,

        model_name: str,

        temperature: float,

        max_tokens: int,

    ) -> Tuple[str, Dict[str, Any]]:

        """

        Chat Completions を実行し、応答本文（JSON 文字列想定）を返す。



        Args:

            system_text: システム指示（さくらでは user と連結して assistant に載せる）

            user_text: ユーザープロンプト本文

            model_name: DB 由来のモデル名（空なら HV_LLM_DEFAULT_MODEL / cotomi3）

            temperature: 温度

            max_tokens: 最大トークン数



        Returns:

            (choices[0].message.content 文字列, usage 辞書)

        """

        payload = {

            "system_content": system_text,

            "user_content": user_text,

            "temperature": float(temperature),

            "max_tokens": int(max_tokens),

            "model_name": model_name,

        }

        if not self.config.get("enabled"):

            if self.config.get("require_real_api"):

                raise RuntimeError("HV_LLM_ENABLED is false and HV_LLM_REQUIRE_REAL_API is true")

            return self._simulate_response(payload)



        last_error: Exception | None = None

        retries = int(self.config.get("max_retries", 2))

        backoff_ms = int(self.config.get("retry_backoff_ms", 300))

        for attempt in range(retries + 1):

            try:

                body = self._sakura_chat_response_text(payload)

                return self._parse_chat_completion_body(body)

            except (RuntimeError, TimeoutError, ValueError, urlerror.URLError) as exc:

                last_error = exc

                logger.warning("LLM call failed attempt=%s error=%s", attempt + 1, exc)

                if attempt < retries:

                    time.sleep(backoff_ms / 1000.0)

        raise RuntimeError(f"LLM call failed: {last_error}")



    def _simulate_response(self, payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:

        """HV_LLM_ENABLED=false 時のスタブ JSON（ローカル検証用）。"""

        stub = {

            "simulated": True,

            "note": "HV_LLM_ENABLED=false",

            "user_preview": (payload.get("user_content") or "")[:200],

        }

        return json.dumps(stub, ensure_ascii=False), {}



    def _resolve_model(self, model_name: str) -> str:

        """API に渡す model（優先: 引数 → HV_LLM_DEFAULT_MODEL）。"""

        name = (model_name or "").strip()

        if name:

            return name

        return (self.config.get("default_model_name") or "cotomi3").strip()



    @staticmethod

    def _build_sakura_messages(system_text: str, user_text: str) -> list:

        """

        さくらサンプル（docs/sakura.md）に合わせ assistant 1 件にプロンプトを載せる。



        system と user の両方がある場合は改行で連結する。

        """

        parts = []

        if (system_text or "").strip():

            parts.append(system_text.strip())

        if (user_text or "").strip():

            parts.append(user_text.strip())

        content = "\n\n".join(parts)[:_MAX_MESSAGE_CHARS]

        return [{"role": "assistant", "content": content}]



    def _sakura_chat_response_text(self, payload: Dict[str, Any]) -> str:

        """さくら AI Engine Chat Completions の生レスポンス JSON 文字列。"""

        token = self.config.get("sakura_api_token")

        if not token:

            raise RuntimeError("SAKURA_AI_TOKEN is not configured")

        url = str(self.config.get("sakura_api_url") or "").rstrip("/")

        if not url.endswith("/chat/completions"):

            if url.endswith("/v1"):

                url = f"{url}/chat/completions"

            else:

                url = f"{url}/chat/completions" if "/v1" in url else url



        model = self._resolve_model(str(payload.get("model_name") or ""))

        req_body = {

            "model": model,

            "messages": self._build_sakura_messages(

                str(payload.get("system_content") or ""),

                str(payload.get("user_content") or ""),

            ),

            "temperature": float(payload.get("temperature", 0.2)),

            "max_tokens": int(payload.get("max_tokens", 2048)),

        }

        req = urlrequest.Request(

            url=url,

            data=json.dumps(req_body).encode("utf-8"),

            headers={

                "Content-Type": "application/json",

                "Authorization": f"Bearer {token}",

            },

            method="POST",

        )

        timeout = int(self.config.get("timeout_seconds", 60))

        try:

            with urlrequest.urlopen(req, timeout=timeout) as resp:

                return resp.read().decode("utf-8")

        except (urlerror.URLError, TimeoutError) as exc:

            raise RuntimeError(f"Sakura AI request failed: {exc}") from exc



    @staticmethod

    def _parse_chat_completion_body(body: str) -> Tuple[str, Dict[str, Any]]:

        """

        API レスポンス JSON から assistant の content と usage を取り出す。

        """

        parsed = json.loads(body)

        choices = parsed.get("choices") or []

        if not choices:

            raise RuntimeError("LLM response has no choices")

        msg = (((choices[0] or {}).get("message") or {}).get("content") or "").strip()

        if not msg:

            raise RuntimeError("LLM message content is empty")

        usage = parsed.get("usage") if isinstance(parsed.get("usage"), dict) else {}

        return msg, usage



