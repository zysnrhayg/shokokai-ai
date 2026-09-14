"""

LLM 共通呼び出しエントリ（非侵襲）。



処理概要:

  1. 第1引数 = 业务表取得のプロンプト本文テンプレート → {{session.*}} / {{db_values.*}} 展開

  2. system / model / temperature / max_tokens / response_schema は .env（load_llm_config）のみ

  3. LlmClient 呼び出し → 任意 JSON 検証

"""



from __future__ import annotations



import json

import logging

from typing import Any, Dict, Optional



from utils.llm.client.llm_client import LlmClient

from utils.llm.config.llm_config import load_llm_config

from utils.llm.template import renderer as template_renderer

from utils.llm.validator import json_validator



logger = logging.getLogger(__name__)





class LlmCommonService:

    """call_llm_common の実装クラス。"""



    def __init__(self, llm_client: LlmClient | None = None) -> None:

        self._client = llm_client or LlmClient(load_llm_config())



    def call_llm_common(

        self,

        user_prompt_template: str,

        session: Dict[str, Any],

        db_values: Dict[str, Any],

        extra_context: Optional[Dict[str, Any]] = None,

    ) -> Dict[str, Any]:

        """

        共通 LLM 呼び出し（パラメータは設計書 3 項のみ）。



        Args:

            user_prompt_template: 业务 Dao（如 API124）取得的 prompt 文本模板

            session / db_values / extra_context: テンプレート {{session.*}} / {{db_values.*}} 用

        """

        cfg = load_llm_config()

        model_label = (cfg.get("default_model_name") or "").strip() or "(default from HV_LLM_DEFAULT_MODEL / cotomi3)"

        try:

            context = template_renderer.build_llm_context(

                session=session,

                db_values=db_values,

                extra_context=extra_context,

            )



            system_prompt = template_renderer.render_template(

                cfg.get("system_prompt") or "", context

            )

            user_prompt = template_renderer.render_template(

                user_prompt_template or "", context

            )



            schema = self._normalize_schema(cfg.get("response_schema"))

            schema_instruction = self._schema_instruction(schema)

            if schema_instruction:

                user_prompt = f"{user_prompt}\n\n{schema_instruction}".strip()



            temperature = float(cfg.get("temperature") or 0.2)

            max_tokens = int(cfg.get("max_tokens") or 2048)

            model_for_api = (cfg.get("default_model_name") or "").strip()



            raw_text, _usage = self._client.chat_completion_json(

                system_text=system_prompt,

                user_text=user_prompt,

                model_name=model_for_api,

                temperature=temperature,

                max_tokens=max_tokens,

            )



            parsed = json_validator.parse_llm_json(raw_text)

            ok, err = json_validator.validate_response_schema(parsed, schema)

            if not ok:

                raise ValueError(f"response does not match response_schema: {err}")



            return {

                "success": True,

                "model": model_label,

                "result": parsed,

                "raw_response": raw_text,

                "error": None,

            }

        except Exception as exc:

            logger.exception("call_llm_common failed")

            return {

                "success": False,

                "model": model_label,

                "result": None,

                "raw_response": None,

                "error": str(exc),

            }



    @staticmethod

    def _normalize_schema(raw: Any) -> Dict[str, Any]:

        if raw is None or raw == "":

            return {}

        if isinstance(raw, dict):

            return raw

        if isinstance(raw, str):

            try:

                parsed = json.loads(raw)

                return parsed if isinstance(parsed, dict) else {}

            except json.JSONDecodeError:

                return {}

        return {}



    @staticmethod

    def _schema_instruction(schema: Dict[str, Any]) -> str:

        if not schema:

            return ""

        return (

            "Respond with a single JSON object only. Required schema:\n"

            f"{json.dumps(schema, ensure_ascii=False, indent=2)}"

        )





def call_llm_common(

    user_prompt_template: str,

    session: dict,

    db_values: dict,

    extra_context: dict | None = None,

) -> dict:

    """設計書 3 パラメータ専用ショートカット。"""

    return LlmCommonService().call_llm_common(

        user_prompt_template=user_prompt_template,

        session=session,

        db_values=db_values,

        extra_context=extra_context,

    )

