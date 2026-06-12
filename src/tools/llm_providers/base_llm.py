from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Union

from pydantic import BaseModel


class Basellm(ABC):
    @abstractmethod
    async def run_with_schema(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[BaseModel],
    ) -> Union[BaseModel, Dict[str, Any]]:
        """
        Run a llm completion.
        If output_schema is provided, return a validated Pydantic model.
        Otherwise return raw string.
        """
