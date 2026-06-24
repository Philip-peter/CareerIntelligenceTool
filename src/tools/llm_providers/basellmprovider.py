from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Basellm(ABC):
    @abstractmethod
    async def run_with_schema(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Type[T],
    ) -> T:
        """Invoke llm and return result using pydantic schema"""
