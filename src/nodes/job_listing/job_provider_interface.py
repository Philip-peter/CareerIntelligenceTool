from abc import ABC, abstractmethod
from typing import Any


class JobProviderInterface(ABC):
    @abstractmethod
    def fetch_jobs(self) -> Any:  # temporary annotation
        pass
