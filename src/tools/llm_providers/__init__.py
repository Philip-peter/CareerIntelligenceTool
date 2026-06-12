from typing import Any, Dict, Type, Union

from pydantic import BaseModel

from . import openai_llm


class llm_tool:
    def __init__(
        self,
        llm_client: str,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[BaseModel],
    ) -> None:
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.output_schema = output_schema

    async def analyse(self) -> Union[BaseModel, Dict[str, Any]]:
        match self.llm_client:
            case "open_ai":
                llm = openai_llm.Openai_llm()
                response = await llm.run_with_schema(
                    self.system_prompt, self.user_prompt, self.output_schema
                )
            case "anthropic":
                raise NotImplementedError()
            case "gemini":
                raise NotImplementedError()
            case _:
                raise ValueError("Enter valid llm client")

        return response
