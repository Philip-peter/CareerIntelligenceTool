from abc import ABC, abstractmethod


class JobProviderInterface(ABC):
    @abstractmethod
    def fetch_jobs(self):
        pass
