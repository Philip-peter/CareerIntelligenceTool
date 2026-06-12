import os
import sys

# ignore Pydantic serializer warnings
import warnings
from typing import Type

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from . import base_llm

warnings.filterwarnings(
    "ignore", message="Pydantic serializer warnings:", category=UserWarning
)

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)

from config import cfg  # noqa: E402


class Openai_llm(base_llm.Basellm):
    def __init__(self) -> None:
        super().__init__()

        self.model = cfg.OPENAI_MODEL
        self.api_key = cfg.OPENAI_API_KEY
        if self.api_key is None:
            raise ValueError("LLM Error: api key is not set in environment variables")

        self.llm = ChatOpenAI(
            model=self.model,
            api_key=SecretStr(self.api_key),
            max_retries=cfg.LLM_MAX_RETRIES,
        )

    async def run_with_schema(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[BaseModel],
    ):

        try:
            messages = [("system", system_prompt), ("user", user_prompt)]

            # structured llm output
            llm_structured_output = self.llm.with_structured_output(
                schema=output_schema, strict=True, method="json_schema"
            )
            response = await llm_structured_output.ainvoke(messages)

            # return default schema values if llm returned nothing
            if not response:
                return output_schema()

            return response
        except Exception as e:
            print(f"Encountered Error during LLM Summarization: {e}")
            return output_schema()
