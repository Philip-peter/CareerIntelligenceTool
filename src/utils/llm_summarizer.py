import os
import sys
from typing import Optional, Type

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402


class LlmSummarizer:
    def __init__(self) -> None:
        api_key = cfg.OPENAI_API_KEY
        if api_key is None:
            raise ValueError("LLM Error: api key is not set in environment variables")

        self.llm = ChatOpenAI(
            model="gpt-4o", api_key=SecretStr(api_key), max_retries=cfg.LLM_MAX_RETRIES
        )

    async def run(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Optional[Type[BaseModel]],
    ):
        try:
            messages = [("system", system_prompt), ("user", user_prompt)]
            if output_schema is None:
                response = await self.llm.ainvoke(messages)
            else:
                llm_structured_output = self.llm.with_structured_output(
                    output_schema, strict=False
                )
                response = await llm_structured_output.ainvoke(messages)
            return response
        except Exception as e:
            print(f"Encountered Error during LLM Summarization: {e}")
            return None
