import os
import sys
from enum import Enum

from . import openai_llm_provider

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402


class LlmProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"


class LlmFactory:
    @staticmethod
    def create_llm(
        llm_provider: LlmProvider | None = None,
        model: str | None = None,
        api_key: str | None = None,
    ):

        # use global preferred llm provider if None
        provider = llm_provider or cfg.PREFERRED_LLM_PROVIDER

        match provider:
            case LlmProvider.OPENAI:
                return openai_llm_provider.Open_ai_llm(
                    model=model or cfg.OPENAI_MODEL,
                    ai_gw_api_key=cfg.LITELLM_MASTER_KEY,
                    ai_gw_base_url=cfg.LLM_LITE_URL,
                    max_retries=cfg.LLM_MAX_RETRIES,
                )
            case LlmProvider.GEMINI:
                raise NotImplementedError("Llm provider has not been implemeneted")
            case LlmProvider.ANTHROPIC:
                raise NotImplementedError("Llm provider has not been implemeneted")
            case _:
                raise ValueError(f"Unsupported LLM provider: {provider}")
