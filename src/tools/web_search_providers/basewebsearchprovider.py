from abc import ABC, abstractmethod


class BaseWebSearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> str:
        """Base web search provider"""
