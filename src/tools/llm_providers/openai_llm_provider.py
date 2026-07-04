import os
import sys
from typing import Dict, Type, TypeVar, Union

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from . import basellmprovider

T = TypeVar("T", bound=BaseModel)

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(root_dir)


class Open_ai_llm(basellmprovider.Basellm):
    def __init__(self, model, api_key, max_retries) -> None:
        super().__init__()
        self.llm = ChatOpenAI(
            model=model,
            api_key=SecretStr(api_key),
            max_retries=max_retries,
        )

    async def run_with_schema(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[T],
    ) -> T:
        """
        Invoke llm and return results using pydantic schema, if no response
        """
        try:
            messages = [("system", system_prompt), ("user", user_prompt)]

            # structured llm output
            llm_structured_output = self.llm.with_structured_output(
                schema=output_schema
            )

            response = await llm_structured_output.ainvoke(messages)

            # return default schema values if llm returned nothing
            if response is None:
                return output_schema()

            # Type Safety
            if isinstance(response, output_schema):
                return response

            if isinstance(response, Dict):
                return output_schema.model_validate(response)

            return output_schema()
        except Exception as e:
            print(f"Encountered Error during LLM Summarization: {e}")
            return output_schema()
