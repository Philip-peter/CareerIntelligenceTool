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
    ) -> Union[BaseModel, Dict[Any, Any]]:
        """Invoke llm and return result using pydantic schema"""
