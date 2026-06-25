from abc import ABC, abstractmethod
from typing import Any


class JobProviderInterface(ABC):
    @abstractmethod
    def fetch_jobs(self, user_preferences) -> Any:  # temporary annotation
        pass
