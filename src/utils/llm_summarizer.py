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

    def run(self, raw_message, output_schema: Optional[Type[BaseModel]]):
        try:
            if output_schema is None:
                response = self.llm.invoke(raw_message)
            else:
                llm_structured_output = self.llm.with_structured_output(
                    output_schema, strict=True
                )
                response = llm_structured_output.invoke(raw_message)
            return response
        except Exception as e:
            print(f"Encountered Error during LLM Summarization: {e}")
            return None
